# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-11
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Marcel Fernandes - Cartographic Engineer @ Brazilian Army
        email                : 
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
from typing import List, Optional

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsFeature,
)
from qgis.gui import QgsMapTool, QgsMessageBar, QgisInterface
from qgis.PyQt import QtCore, QtGui, uic
from qgis.PyQt.Qt import QObject, QVariant
from qgis.PyQt.QtCore import QObject, QSettings, Qt, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QSpinBox, QWidget
from qgis.PyQt.QtXml import QDomDocument
from qgis.core.additions.edit import edit

from .CenterPointAndBoundariesToolbar_ui import Ui_CenterPointAndBoundariesToolbar
from enum import Enum


class CenterPointAndBoundariesToolbar(QWidget, Ui_CenterPointAndBoundariesToolbar):
    idxChanged = pyqtSignal(int)
    ZoomToNext, PanToNext, DoNothing = range(3)

    def __init__(self, iface: QgisInterface, parent: Optional[QWidget] = None):
        """
        Constructor
        """
        super(CenterPointAndBoundariesToolbar, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        # self.iface.currentLayerChanged.connect(self.enableScale)

        self.canvas = self.iface.mapCanvas()
        self.mMapLayerComboBox.layerChanged.connect(self.visitedFieldComboBox.setLayer)
        self.mMapLayerComboBox.layerChanged.connect(self.rankFieldComboBox.setLayer)
        self.setToolTip("")
        self.visitedFieldComboBox.setToolTip(self.tr("Set visited field"))
        self.visitedFieldComboBox.setAllowEmptyFieldName(True)
        self.rankFieldComboBox.setToolTip(self.tr("Set rank field"))
        self.rankFieldComboBox.setAllowEmptyFieldName(True)
        self.zoomComboBox.setCurrentIndex(CenterPointAndBoundariesToolbar.ZoomToNext)
        icon_path = ":/plugins/DsgTools/icons/attributeSelector.png"
        text = self.tr("DSGTools: Mark tile as done")
        self.applyPushButtonAction = self.add_action(
            icon_path, text, self.applyPushButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.applyPushButtonAction, "")

        text = self.tr("DSGTools: Mark tile as done")
        self.previousTileAction = self.add_action(
            icon_path=":/plugins/DsgTools/icons/backInspect.png",
            text=self.tr("DSGTools: Go to previous tile"),
            callback=self.previousTileButton.click,
            parent=self.parent,
        )
        self.iface.registerMainWindowAction(self.previousTileAction, "")

        self.nextTileAction = self.add_action(
            icon_path=":/plugins/DsgTools/icons/nextInspect.png",
            text=self.tr("DSGTools: Go to next tile"),
            callback=self.nextTileButton.click,
            parent=self.parent,
        )
        self.iface.registerMainWindowAction(self.nextTileAction, "")

        self.resetPushButtonAction = self.add_action(
            icon_path=":/plugins/DsgTools/icons/reset.png",
            text=self.tr("DSGTools: Reset visited tiles on review toolbar"),
            callback=self.resetPushButton.click,
            parent=self.parent,
        )
        self.iface.registerMainWindowAction(self.resetPushButtonAction, "")

        self.mMapLayerComboBox.setAllowEmptyLayer(True)
        self.mMapLayerComboBox.setCurrentIndex(0)
        self.currentTile = None
        self.originalValueList = self.getValueListFromQsettings()

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: QAction,
        parent: Optional[QWidget] = None,
    ) -> QAction:
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def enableTool(self, enabled: bool = True) -> None:
        allowed = (
            False
            if enabled == None or not isinstance(enabled, QgsVectorLayer)
            else True
        )
        toggled = self.reviewPushButton.isChecked()
        enabled = allowed and toggled
        self.applyPushButton.setEnabled(enabled)

    @pyqtSlot(int, name="on_rankFieldComboBox_currentIndexChanged")
    def validateRankField(self, idx: int) -> bool:
        if idx in (-1, 0):
            return False
        fieldName = self.rankFieldComboBox.itemText(idx)
        fieldList = [
            field
            for field in self.rankFieldComboBox.fields()
            if field.name() == fieldName
        ]
        if len(fieldList) == 0 or fieldList[0].type() != QVariant.Int:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr(
                    "Invalid rank field! Select an integer field with unique ordered items."
                ),
                level=Qgis.Warning,
                duration=2,
            )
            self.rankFieldComboBox.setCurrentIndex(0)
            return False
        return True

    @pyqtSlot(int, name="on_visitedFieldComboBox_currentIndexChanged")
    def validateVisitedField(self, idx: int) -> bool:
        if idx in (-1, 0):
            return False
        fieldName = self.visitedFieldComboBox.itemText(idx)
        fieldList = [
            field
            for field in self.visitedFieldComboBox.fields()
            if field.name() == fieldName
        ]
        if len(fieldList) == 0 or fieldList[0].type() != QVariant.Bool:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr("Invalid attribute filter! Select a boolean field."),
                level=Qgis.Warning,
                duration=2,
            )
            self.visitedFieldComboBox.setCurrentIndex(0)
            return False
        return True

    def on_preparePushButton_clicked(self) -> None:
        currentLayer = self.mMapLayerComboBox.currentLayer()
        if currentLayer is None:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr("Select a layer to prepare the environment!"),
                level=Qgis.Warning,
                duration=2,
            )
            return
        if self.visitedFieldComboBox.currentIndex() == 0:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr("Invalid attribute filter! Select a boolean field."),
                level=Qgis.Warning,
                duration=2,
            )
            return
        if not self.validateVisitedField(self.visitedFieldComboBox.currentIndex()):
            return
        if self.rankFieldComboBox.currentIndex() == 0:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr(
                    "Invalid rank field! Select an integer field with unique ordered items."
                ),
                level=Qgis.Warning,
                duration=2,
            )
            return
        if not self.validateRankField(self.rankFieldComboBox.currentIndex()):
            return

        overviewWidget = self.getOverviewWidget()
        if overviewWidget is not None:
            overviewWidget.show()
        currentLayerFromTreeRoot = (
            QgsProject.instance().layerTreeRoot().findLayer(currentLayer.id())
        )
        currentLayerFromTreeRoot.setCustomProperty("overview", 1)
        fieldList = [
            field
            for field in self.visitedFieldComboBox.fields()
            if field.name() == self.visitedFieldComboBox.currentField()
        ]
        if len(fieldList) == 0 or fieldList[0].type() != QVariant.Bool:
            self.iface.messageBar().pushMessage(
                title=self.tr("Warning!"),
                text=self.tr("Invalid attribute filter!"),
                level=Qgis.Warning,
                duration=2,
            )
            return
        currentField = fieldList[0]
        self.applyStyle(currentLayer, currentField.name())
        self.addCurrentLayerToGenericSelectionBlackList()
        currentLayer.setReadOnly(True)

    def getOverviewWidget(self) -> None:
        itemList = [
            i
            for i in self.iface.mainWindow().children()
            if i.objectName() == "Overview"
        ]
        return None if len(itemList) == 0 else itemList[0]

    def applyStyle(self, lyr: QgsVectorLayer, fieldName: str) -> None:
        stylePath = self.createTempStyle(fieldName)
        lyr.loadNamedStyle(stylePath, True)
        lyr.triggerRepaint()
        self.deleteTempStyle(stylePath)

    def createTempStyle(self, fieldName: str) -> None:
        currentPath = os.path.dirname(os.path.abspath(__file__))
        templatePath = os.path.join(currentPath, "grid_style.qml")
        tempOutputPath = os.path.join(currentPath, "grid_style_temp.qml")
        with open(templatePath) as f:
            templateFile = f.read()
        templateFile = templateFile.replace('attr="visited"', f'attr="{fieldName}"')
        with open(tempOutputPath, "w") as f:
            f.write(templateFile)
        return tempOutputPath

    def deleteTempStyle(self, tempStylePath: str) -> None:
        os.remove(tempStylePath)

    @pyqtSlot(bool, name="on_reviewPushButton_toggled")
    def toggleBar(self, toggled: Optional[bool] = None) -> None:
        """
        Shows/Hides the tool bar
        """
        toggled = self.reviewPushButton.isChecked() if toggled is None else toggled
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()

    @pyqtSlot(bool)
    def on_previousTileButton_clicked(self) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        rankField = self.rankFieldComboBox.currentField()
        if rankField is None:
            return
        visitedField = self.visitedFieldComboBox.currentField()
        if visitedField is None:
            return
        request = self.getFeatureRequest(
            rankField, expression=f"{visitedField} = False", ascending=True
        )
        featDict = {feat.id(): feat for feat in layer.getFeatures(request)}
        featIdList = sorted(featDict.keys(), reverse=False)
        nFeats = len(featDict)
        if nFeats == 0:
            self.iface.messageBar().pushMessage(
                title=self.tr("Info!"),
                text=self.tr("All tiles already visited!"),
                level=Qgis.Info,
                duration=2,
            )
            return
        currentIdx = (
            featIdList.index(self.currentTile) if self.currentTile in featIdList else 0
        )
        nextFeature = featDict[featIdList[(currentIdx - 1)]]
        if self.zoomComboBox.currentIndex() == CenterPointAndBoundariesToolbar.ZoomToNext:
            self.zoomToFeature(nextFeature)
        else:
            self.panToFeature(nextFeature)
        self.currentTile = nextFeature.id()

    @pyqtSlot(bool)
    def on_nextTileButton_clicked(self) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        rankField = self.rankFieldComboBox.currentField()
        if rankField is None:
            return
        visitedField = self.visitedFieldComboBox.currentField()
        if visitedField is None:
            return
        request = self.getFeatureRequest(
            rankField, expression=f"{visitedField} = False", ascending=True
        )
        featDict = {feat.id(): feat for feat in layer.getFeatures(request)}
        featIdList = sorted(featDict.keys(), reverse=False)
        nFeats = len(featDict)
        if nFeats == 0:
            self.iface.messageBar().pushMessage(
                title=self.tr("Info!"),
                text=self.tr("All tiles already visited!"),
                level=Qgis.Info,
                duration=2,
            )
            return
        currentIdx = (
            featIdList.index(self.currentTile) if self.currentTile in featIdList else -1
        )
        nextFeature = featDict[featIdList[(currentIdx + 1) % nFeats]]
        if self.zoomComboBox.currentIndex() == CenterPointAndBoundariesToolbar.ZoomToNext:
            self.zoomToFeature(nextFeature)
        else:
            self.panToFeature(nextFeature)
        self.currentTile = nextFeature.id()

    @pyqtSlot(bool)
    def on_resetPushButton_clicked(self) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        visitedField = self.visitedFieldComboBox.currentField()
        if visitedField is None:
            return
        if (
            not QMessageBox.question(
                self,
                self.tr("DSGTools Review Toolbar: Confirm action"),
                self.tr("Would you like to set all features from grid as unvisited?"),
                QMessageBox.Ok | QMessageBox.Cancel,
            )
            == QMessageBox.Ok
        ):
            return
        layer.setReadOnly(False)
        layer.startEditing()
        layer.beginEditCommand("DSGTools review tool")
        for feat in layer.getFeatures():
            feat[visitedField] = False
            layer.updateFeature(feat)
        layer.endEditCommand()
        layer.commitChanges()
        layer.setReadOnly(True)

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self) -> None:
        selectedFeatures = self.getSelectedFeatures()
        featList = (
            selectedFeatures
            if selectedFeatures != []
            else self.getFeaturesFromCursorBoundingBox()
        )
        if featList == []:
            return
        self.setFeaturesAsVisited(featList)
        nextFeat = self.getNextFeature(featList[0])
        if nextFeat is None:
            self.iface.messageBar().pushMessage(
                title=self.tr("Info!"),
                text=self.tr("All tiles already visited!"),
                level=Qgis.Info,
                duration=2,
            )
            return
        if self.zoomComboBox.currentIndex() == CenterPointAndBoundariesToolbar.ZoomToNext:
            self.zoomToFeature(nextFeat)
        elif self.zoomComboBox.currentIndex() == CenterPointAndBoundariesToolbar.PanToNext:
            self.panToFeature(nextFeat)
        else:
            self.iface.mapCanvas().refresh()
        currentField = self.rankFieldComboBox.currentField()
        if currentField is None:
            return
        self.currentTile = nextFeat.id()

    def getSelectedFeatures(self) -> List[QgsFeature]:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return []
        return [feat for feat in layer.selectedFeatures()]

    def getFeaturesFromCursorBoundingBox(self) -> List[QgsFeature]:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return []
        bbox = self.getBoundingBoxFromCursor(layer)
        return [feat for feat in layer.getFeatures(bbox)]

    def getBoundingBoxFromCursor(self, layer: QgsVectorLayer) -> QgsRectangle:
        rect = self.getCursorRect()
        bbRect = self.iface.mapCanvas().mapSettings().mapToLayerCoordinates(layer, rect)
        return bbRect

    def getCursorRect(self):
        p = QgsMapTool(self.iface.mapCanvas()).toMapCoordinates(
            self.iface.mapCanvas().mouseLastXY()
        )
        w = self.iface.mapCanvas().mapUnitsPerPixel() * 10
        return QgsRectangle(p.x() - w, p.y() - w, p.x() + w, p.y() + w)

    def setFeaturesAsVisited(self, featureList: List[QgsFeature]) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        visitedField = self.visitedFieldComboBox.currentField()
        layer.setReadOnly(False)
        layer.startEditing()
        layer.beginEditCommand("DSGTools review tool")
        for feat in featureList:
            feat[visitedField] = not feat[visitedField]
            layer.updateFeature(feat)
        layer.endEditCommand()
        layer.commitChanges()
        layer.setReadOnly(True)

    def getNextFeature(self, currentFeature, forward=True) -> QgsFeature:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        rankField = self.rankFieldComboBox.currentField()
        if rankField is None:
            return
        visitedField = self.visitedFieldComboBox.currentField()
        if visitedField is None:
            return
        # we first try to get the next local feature
        if currentFeature is not None:
            expression = (
                f"{visitedField} = False and {rankField} > {currentFeature[rankField]} "
                if forward
                else f"{visitedField} = False and {rankField} < {currentFeature[rankField]} "
            )
            request = self.getFeatureRequest(rankField, expression=expression, limit=1)
            nextFeat = next(layer.getFeatures(request), None)
            if nextFeat is not None:
                return nextFeat
        # if there is no next local feature, we search globally, but this search can also return None
        request = self.getFeatureRequest(
            rankField,
            expression=f"{visitedField} = False",
            ascending=True if forward else False,
            limit=1,
        )
        return next(layer.getFeatures(request), None)

    def getFeatureRequest(
        self,
        rankField: str,
        expression: str,
        ascending: bool = True,
        limit: Optional[int] = None,
    ):
        request = QgsFeatureRequest().setFilterExpression(expression)
        orderby = QgsFeatureRequest.OrderBy(
            [QgsFeatureRequest.OrderByClause(rankField, ascending=ascending)]
        )
        request.setOrderBy(orderby)
        if limit is not None:
            request.setLimit(limit)
        return request

    def zoomToFeature(self, feat: QgsFeature) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        bbox = feat.geometry().boundingBox()
        bbox.grow(min(bbox.width(), bbox.height()) * 0.4)
        epsg = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        crsDest = QgsCoordinateReferenceSystem(epsg)
        srid = layer.crs().authid()
        crsSrc = QgsCoordinateReferenceSystem(
            srid
        )  # here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(
            crsSrc, crsDest, QgsProject.instance()
        )
        newBox = coordinateTransformer.transform(bbox)
        self.iface.mapCanvas().setExtent(newBox)
        self.iface.mapCanvas().refresh()

    def panToFeature(self, feat: QgsFeature) -> None:
        layer = self.mMapLayerComboBox.currentLayer()
        if layer is None:
            return
        self.iface.mapCanvas().panToFeatureIds(layer, [feat.id()])

    def addCurrentLayerToGenericSelectionBlackList(self, layer=None):
        layer = self.mMapLayerComboBox.currentLayer() if layer is None else layer
        if layer is None:
            return
        self.addLayerNameToGenericSelectionBlackList(layer.name())

    @pyqtSlot(QgsVectorLayer, name="on_mMapLayerComboBox_layerChanged")
    def removeLayerFromGenericSelectionBlackList(self, layer=None):
        layer = self.mMapLayerComboBox.currentLayer() if layer is None else layer
        if layer is None:
            return
        if self.mMapLayerComboBox.currentIndex() == 0:
            return
        self.removeLayerNameToGenericSelectionBlackList(layer.name())

    def addLayerNameToGenericSelectionBlackList(self, layerName: str):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        valueList = [i for i in settings.value("valueList").split(";") if i != ""]
        if layerName in valueList:
            return
        valueList.append(layerName)
        settings.setValue("valueList", ";".join(valueList))
        settings.endGroup()

    def removeLayerNameToGenericSelectionBlackList(self, layerName):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        valueList = [i for i in settings.value("valueList").split(";") if i != ""]
        if valueList != [] and (
            layerName not in valueList or layerName in self.originalValueList
        ):
            return
        valueList.pop(layerName)
        settings.setValue("valueList", ";".join(valueList))
        settings.endGroup()

    def getValueListFromQsettings(self):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        valueList = [i for i in settings.value("valueList").split(";") if i != ""]
        settings.endGroup()
        return valueList

    def restoreOriginalValueList(self):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        valueList = self.originalValueList
        settings.setValue("valueList", ";".join(valueList))
        settings.endGroup()

    def unload(self) -> None:
        self.restoreOriginalValueList()
        self.iface.unregisterMainWindowAction(self.applyPushButtonAction)

    def setState(
        self,
        layer: QgsVectorLayer,
        rankFieldName: str,
        visitedFieldName: str,
        zoomType: int = 0,
    ):
        self.mMapLayerComboBox.setLayer(layer)
        self.rankFieldComboBox.setField(rankFieldName)
        self.visitedFieldComboBox.setField(visitedFieldName)
        self.zoomComboBox.setCurrentIndex(int(zoomType))
        self.preparePushButton.click()
