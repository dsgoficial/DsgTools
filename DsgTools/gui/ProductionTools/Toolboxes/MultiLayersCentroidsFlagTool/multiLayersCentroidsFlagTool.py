# -*- coding: utf-8 -*-
"""
/***************************************************************************
InspectFeatures
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2025-02-26
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Matheus Alves Silva @ Brazilian Army
        email                : matheus.alvessilva@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QSpinBox,
    QAction,
    QDockWidget,
    QTableWidgetItem,
    QMenu,
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt, QDateTime
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from processing.gui.MultipleInputDialog import MultipleInputDialog
from qgis.core import (
    QgsMapLayer,
    Qgis,
    QgsVectorLayer,
    QgsSpatialIndex,
    QgsProcessingAlgorithm,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsMapLayerUtils,
    QgsWkbTypes,
    QgsFeature,
    QgsProject,
)
from qgis.gui import QgsMessageBar

from DsgTools.gui.ProductionTools.Toolboxes.MultiLayersCentroidsFlagTool.multiLayersCentroidsFlagTool_ui import (
    Ui_MultiLayersCentroidsFlagDockWidget,
)
from collections import defaultdict


class MultiLayersCentroidsFlagDockWidget(
    QDockWidget, Ui_MultiLayersCentroidsFlagDockWidget
):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(MultiLayersCentroidsFlagDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.iface = iface
        self.lyrsFlags = None
        self.flagsMapLayerComboBox.setAllowEmptyLayer(True)
        self.flagsMapLayerComboBox.setCurrentIndex(-1)
        self.flagsMapLayerComboBox.layerChanged.connect(self.updateTable)
        QgsProject.instance().layersWillBeRemoved.connect(self.syncLayers)
        self.attributeTable.cellClicked.connect(self.zoomToFeature)
        self.pointLayerDict = dict()
        self.lyrsNRowPointDict = defaultdict(dict)
        self.columns = []
        self.tableContextMenu()
        self.updateTable()

    def syncLayers(self, layerIdsRemoved):
        for id in layerIdsRemoved:
            if id not in self.pointLayerDict:
                continue
            del self.pointLayerDict[id]
        self.updateTable()

    def pointsInSelectedPolygonFlags(self, lyrFlags):
        if lyrFlags is None:
            return
        selectedPolygons = [feat for feat in lyrFlags.getSelectedFeatures()]
        selectedCrs = lyrFlags.crs()
        if selectedPolygons == []:
            return
        lyrsPointsInsideFlagPolygonDict = defaultdict(list)
        for polygonFeat in selectedPolygons:
            for lyrid, pointLyr in self.pointLayerDict.items():
                geom = polygonFeat.geometry()
                pointCrs = pointLyr.crs()
                if pointCrs != selectedCrs:
                    transform = QgsCoordinateTransform(
                        selectedCrs, pointCrs, QgsProject.instance()
                    )
                    geom.transform(transform)
                bbox = geom.boundingBox()
                for pointFeat in pointLyr.getFeatures(bbox):
                    pointGeom = pointFeat.geometry()
                    if not pointGeom.intersects(geom):
                        continue
                    lyrsPointsInsideFlagPolygonDict[lyrid].append(pointFeat)
                lyrsPointsInsideFlagPolygonDict[lyrid].sort(key=lambda x: x.id())
        return lyrsPointsInsideFlagPolygonDict

    def columnsTable(self, lyrsPointsInsideFlagPolygonDict):
        self.columns = []
        if lyrsPointsInsideFlagPolygonDict is None:
            return
        for lyrid, featList in lyrsPointsInsideFlagPolygonDict.items():
            if featList == []:
                continue
            lyrFields = [
                self.tr(f"{field.name()}")
                for field in self.pointLayerDict[lyrid].fields()
            ]
            for field in lyrFields:
                if field in self.columns:
                    continue
                self.columns.append(field)

    def valuesInTable(self, lyrsPointsInsideFlagPolygonDict, currentSelection=None):
        if lyrsPointsInsideFlagPolygonDict is None:
            return
        nRows = sum(
            [len(points) for points in lyrsPointsInsideFlagPolygonDict.values()]
        )
        self.attributeTable.setRowCount(nRows)
        row = 0
        for lyrid in lyrsPointsInsideFlagPolygonDict:
            lyrFields = [
                self.tr(f"{field.name()}")
                for field in self.pointLayerDict[lyrid].fields()
            ]
            for feat in lyrsPointsInsideFlagPolygonDict[lyrid]:
                self.lyrsNRowPointDict[row] = (lyrid, feat)
                self.attributeTable.setItem(
                    row, 0, QTableWidgetItem(self.pointLayerDict[lyrid].name())
                )
                for nColumn, field in enumerate(self.columns):
                    if field in lyrFields:
                        field_idx = (
                            self.pointLayerDict[lyrid].fields().indexFromName(field)
                        )
                        widget_setup = self.pointLayerDict[lyrid].editorWidgetSetup(
                            field_idx
                        )
                        attr = feat[field]
                        if isinstance(attr, QDateTime):
                            attr = attr.toString("dd/MM/yyyy HH:mm:ss")
                        if widget_setup.type() == "ValueMap":
                            config = widget_setup.config()
                            map_values = config["map"]
                            attr = next(
                                (k for k, v in map_values.items() if v == str(attr)),
                                None,
                            )
                    else:
                        attr = "-"
                    self.attributeTable.setItem(
                        row, nColumn + 1, QTableWidgetItem(str(attr))
                    )
                row += 1
        if currentSelection is not None:
            self.attributeTable.selectRow(currentSelection)

    def setHeader(self, fieldList):
        self.attributeTable.setColumnCount(len(fieldList))
        self.attributeTable.setHorizontalHeaderLabels(fieldList)

    def clearTable(self):
        for row in range(self.attributeTable.rowCount()):
            self.attributeTable.removeRow(row)
        self.attributeTable.setRowCount(0)

    def updateTable(self):
        self.clearTable()
        lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        lyrsPointsInsideFlagPolygonDict = self.pointsInSelectedPolygonFlags(lyrFlags)
        try:
            self.lyrFlags.selectionChanged.disconnect(self.updateTable)
        except:
            pass
        self.lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        if (
            self.flagsMapLayerComboBox.currentIndex() == -1
            or self.pointLayerDict == dict()
            or self.lyrFlags is None
        ):
            return
        self.lyrFlags.selectionChanged.connect(self.updateTable)
        self.columnsTable(lyrsPointsInsideFlagPolygonDict)
        if lyrsPointsInsideFlagPolygonDict is None:
            self.setHeader([])
            return
        self.setHeader([self.tr("Camada")] + self.columns)
        self.valuesInTable(lyrsPointsInsideFlagPolygonDict)

    def tableContextMenu(self):
        self.attributeTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attributeTable.customContextMenuRequested.connect(self.showMenuContext)

    def showMenuContext(self, position):
        index = self.attributeTable.indexAt(position)
        if not index.isValid():
            return
        contextMenu = QMenu()
        action1 = QAction(
            self.tr(
                "Set all point features from all layers to the attributes like this feature"
            ),
            self,
        )
        action1.triggered.connect(lambda: self.setAllFeatureAttributesAllLayers(index))
        contextMenu.addAction(action1)
        contextMenu.exec_(self.attributeTable.viewport().mapToGlobal(position))

    def zoomToFeature(self, row):
        lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        lyrid, feat = self.lyrsNRowPointDict[row]
        geom = feat.geometry()
        lyrPoint = self.pointLayerDict[lyrid]
        pointCrs = lyrPoint.crs()
        selectedCrs = lyrFlags.crs()
        if pointCrs != selectedCrs:
            transform = QgsCoordinateTransform(
                pointCrs, selectedCrs, QgsProject.instance()
            )
            geom.transform(transform)
        bbox = geom.boundingBox()
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().zoomScale(500)
        self.iface.mapCanvas().refresh()

    def setAllFeatureAttributesAllLayers(self, index):
        lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        lyrsPointsInsideFlagPolygonDict = self.pointsInSelectedPolygonFlags(lyrFlags)
        if lyrFlags is None or self.pointLayerDict == dict():
            return
        if len(self.lyrsNRowPointDict) == 0:
            return
        lyridReference, referenceFeat = self.lyrsNRowPointDict[index.row()]
        lyrPointsReference = self.pointLayerDict[lyridReference]
        referenceCrs = lyrPointsReference.crs()
        referenceDict = {
            field.name(): referenceFeat[field.name()]
            for i, field in enumerate(referenceFeat.fields())
            if i not in lyrPointsReference.primaryKeyAttributes()
        }
        for row, (lyrid, feat) in self.lyrsNRowPointDict.items():
            if row == index.row():
                continue
            lyrPointsReference.startEditing()
            lyrPointsReference.beginEditCommand("Updating flags")
            if lyrid == lyridReference:
                self.setLayerFeatures(
                    feat, referenceDict, lyrid, lyrPointsReference, row
                )
            else:
                originalLyr = self.pointLayerDict[lyrid]
                newFeat = QgsFeature(lyrPointsReference.fields())
                newGeom = feat.geometry()
                if originalLyr.crs() != referenceCrs:
                    coordinateTransformer = QgsCoordinateTransform(
                        QgsCoordinateReferenceSystem(originalLyr.crs()),
                        QgsCoordinateReferenceSystem(referenceCrs),
                        QgsProject.instance(),
                    )
                    newGeom.transform(coordinateTransformer)
                newFeat.setGeometry(newGeom)
                self.setLayerFeatures(
                    newFeat, referenceDict, lyrid, lyrPointsReference, row
                )
                lyrPointsReference.addFeature(newFeat)
                lyrPoint = self.pointLayerDict[lyrid]
                lyrPoint.startEditing()
                lyrPoint.beginEditCommand("Updating flags")
                lyrPoint.deleteFeature(feat.id())
                lyrPoint.endEditCommand()
            lyrPointsReference.endEditCommand()
        self.updateTable()
        lyrsPointsInsideFlagPolygonDict = self.pointsInSelectedPolygonFlags(lyrFlags)
        self.valuesInTable(lyrsPointsInsideFlagPolygonDict, index.row())

    def setLayerFeatures(self, feat, referenceDict, lyrid, lyrPoints, row):
        for fieldName, value in referenceDict.items():
            feat[fieldName] = value
            lyrPoints.updateFeature(feat)
            self.lyrsNRowPointDict[row] = (lyrid, feat)

    @pyqtSlot(bool)
    def on_multiLayersCentroidsPushButton_clicked(self) -> None:
        pointLyrs = sorted(
            [
                i
                for i in QgsProject.instance().mapLayers().values()
                if isinstance(i, QgsVectorLayer)
                and i.geometryType() == QgsWkbTypes.PointGeometry
            ],
            key=lambda x: x.id(),
        )
        dlg = MultipleInputDialog(
            [i.name() for i in pointLyrs if i.id()],
            [
                idx
                for idx, lyrName in enumerate(pointLyrs)
                if lyrName in self.pointLayerDict.values()
            ],
        )
        dlg.exec()
        if dlg.selectedoptions is None:
            return
        selectedDict = {pointLyrs[i].id(): pointLyrs[i] for i in dlg.selectedoptions}
        self.pointLayerDict.update(selectedDict)
        keysToRemove = [k for k in self.pointLayerDict.keys() if k not in selectedDict]
        for key in keysToRemove:
            self.pointLayerDict.pop(key)
        self.updateTable()

    @pyqtSlot(bool)
    def on_refreshFlagsPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if not isinstance(activeLayer, QgsVectorLayer):
            return
        self.flagsMapLayerComboBox.setLayer(activeLayer)

    def unload(self):
        QgsProject.instance().layersWillBeRemoved.disconnect(self.syncLayers)
        self.attributeTable.cellClicked.disconnect(self.zoomToFeature)
