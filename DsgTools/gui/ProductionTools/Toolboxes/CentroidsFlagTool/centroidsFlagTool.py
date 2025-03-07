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
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from qgis.core import (
    QgsMapLayer,
    Qgis,
    QgsVectorLayer,
    QgsSpatialIndex,
    QgsProcessingAlgorithm,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsProject,
)
from qgis.gui import QgsMessageBar

from .centroidsFlagTool_ui import Ui_CentroidFlagsDockWidget
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from collections import defaultdict


class CentroidFlagsDockWidget(QDockWidget, Ui_CentroidFlagsDockWidget):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(CentroidFlagsDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.iface = iface
        self.algRunner = AlgRunner()
        self.lyrPoints = None
        self.lyrFlags = None
        self.flagsMapLayerComboBox.setAllowEmptyLayer(True)
        self.flagsMapLayerComboBox.setCurrentIndex(-1)
        self.flagsMapLayerComboBox.layerChanged.connect(self.updateTable)
        self.pointsMapLayerComboBox.setAllowEmptyLayer(True)
        self.pointsMapLayerComboBox.setCurrentIndex(-1)
        self.pointsMapLayerComboBox.layerChanged.connect(self.updateTable)
        self.pointDict = None
        self.tableContextMenu()
        self.updateTable()

    def pointsInSelectedPolygonFlags(self, lyrPoints, lyrFlags):
        selectedPolygons = [feat for feat in lyrFlags.getSelectedFeatures()]
        if selectedPolygons == []:
            return
        pointsInsideFlagPolygonList = []
        for polygonFeat in selectedPolygons:
            geom = polygonFeat.geometry()
            bbox = geom.boundingBox()
            for pointFeat in lyrPoints.getFeatures(bbox):
                pointGeom = pointFeat.geometry()
                if not pointGeom.intersects(geom):
                    continue
                pointsInsideFlagPolygonList.append(pointFeat)
        return sorted(pointsInsideFlagPolygonList, key=lambda x: x.id())

    def tableContextMenu(self):
        self.attributeTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attributeTable.customContextMenuRequested.connect(self.showMenuContext)

    def showMenuContext(self, position):
        index = self.attributeTable.indexAt(position)
        if not index.isValid():
            return
        contextMenu = QMenu()
        action1 = QAction(
            self.tr("Set all point feature attributes like this feature"), self
        )
        action1.triggered.connect(lambda: self.setAllFeatureAttributes(index))
        contextMenu.addAction(action1)
        contextMenu.exec_(self.attributeTable.viewport().mapToGlobal(position))

    def setAllFeatureAttributes(self, index):
        lyrPoints = self.pointsMapLayerComboBox.currentLayer()
        lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        if lyrPoints is None or lyrFlags is None:
            return
        if self.pointDict is None:
            return
        referenceFeat = self.pointDict[index.row()]
        referenceDict = {
            field.name(): referenceFeat[field.name()]
            for i, field in enumerate(referenceFeat.fields())
            if i not in lyrPoints.primaryKeyAttributes()
        }
        lyrPoints.startEditing()
        lyrPoints.beginEditCommand("Updating flags")
        for idx, feat in self.pointDict.items():
            if idx == index.row():
                continue
            for fieldName, value in referenceDict.items():
                feat[fieldName] = value
            lyrPoints.updateFeature(feat)
            self.pointDict[idx] = feat
        lyrPoints.endEditCommand()
        self.valuesInTable(
            fieldList=[f.name() for f in lyrPoints.fields()],
            lyrPoints=lyrPoints,
            lyrFlags=lyrFlags,
            currentSelection=index.row(),
        )

    def updateTable(self):
        self.clearTable()
        self.lyrPoints = self.pointsMapLayerComboBox.currentLayer()
        if self.lyrFlags is not None:
            try:
                self.lyrFlags.selectionChanged.disconnect(self.updateTable)
            except:
                pass
        self.lyrFlags = self.flagsMapLayerComboBox.currentLayer()
        if (
            self.pointsMapLayerComboBox.currentIndex() == -1
            or self.flagsMapLayerComboBox.currentIndex() == -1
        ):
            return
        self.lyrFlags.selectionChanged.connect(self.updateTable)
        if self.lyrPoints is None:
            self.setHeader([])
            return
        self.setHeader(
            [self.tr(f"{field.name()}") for field in self.lyrPoints.fields()]
        )
        self.valuesInTable(
            [self.tr(f"{field.name()}") for field in self.lyrPoints.fields()],
            self.lyrPoints,
            self.lyrFlags,
        )

    def valuesInTable(self, fieldList, lyrPoints, lyrFlags, currentSelection=None):
        pointList = self.pointsInSelectedPolygonFlags(lyrPoints, lyrFlags)
        if pointList is None:
            return
        nRows = len(pointList)
        self.attributeTable.setRowCount(nRows)
        self.pointDict = dict()
        for nRow, feat in enumerate(pointList):
            self.pointDict[nRow] = feat
            for nColumn, field in enumerate(fieldList):
                attr = feat[field]
                self.attributeTable.setItem(nRow, nColumn, QTableWidgetItem(str(attr)))
        if currentSelection is not None:
            self.attributeTable.selectRow(currentSelection)

    def setHeader(self, fieldList):
        self.attributeTable.setColumnCount(len(fieldList))
        self.attributeTable.setHorizontalHeaderLabels(fieldList)

    def clearTable(self):
        for row in range(self.attributeTable.rowCount()):
            self.attributeTable.removeRow(row)
        self.attributeTable.setRowCount(0)

    @pyqtSlot(bool)
    def on_refreshPointsPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if not isinstance(activeLayer, QgsVectorLayer):
            return
        self.pointsMapLayerComboBox.setLayer(activeLayer)

    @pyqtSlot(bool)
    def on_refreshFlagsPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if not isinstance(activeLayer, QgsVectorLayer):
            return
        self.flagsMapLayerComboBox.setLayer(activeLayer)

    def unload(self):
        pass

    def getToolState(self) -> dict:
        pass

    def setToolState(self, stateDict: dict) -> bool:
        pass
