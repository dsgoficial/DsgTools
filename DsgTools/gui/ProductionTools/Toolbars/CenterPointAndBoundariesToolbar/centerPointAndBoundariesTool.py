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
from DsgTools.gui.ProductionTools.Toolboxes.ContourTool.dsg_line_tool import DsgPolygonTool
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

from processing.gui.MultipleInputDialog import MultipleInputDialog

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
    QgsGeometry,
    QgsProcessingContext,
)
from qgis.gui import QgsMapTool, QgsMessageBar, QgisInterface
from qgis.PyQt import QtCore, QtGui, uic
from qgis.PyQt.Qt import QObject, QVariant
from qgis.PyQt.QtCore import QObject, QSettings, Qt, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QSpinBox, QWidget
from qgis.PyQt.QtXml import QDomDocument
from qgis.core.additions.edit import edit
import processing

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "centerPointAndBoundaries.ui")
)


class CenterPointAndBoundariesToolbar(QWidget, FORM_CLASS):
    def __init__(self, iface: QgisInterface, parent: Optional[QWidget] = None):
        """
        Constructor
        """
        super(CenterPointAndBoundariesToolbar, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface

        self.canvas = self.iface.mapCanvas()

        icon_path = ":/plugins/DsgTools/icons/centroid.png"
        text = self.tr("DSGTools: Run add centroids")
        self.runPushButtonAction = self.add_action(
            icon_path, text, self.runPushButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.runPushButtonAction, "")

        self.lineLayerDict = dict()

        self.tool = DsgPolygonTool(self.canvas)
        self.tool.lineCreated.connect(self.runBuildPolygons)
        self.tool.deactivated.connect(self.deactivateButton)
        self.iface.newProjectCreated.connect(self.resetTool)
        QgsProject.instance().layersWillBeRemoved.connect(self.syncLayers)
        self.enableTool(enabled=False)
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()

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
    
    def deactivateButton(self):
        self.runPushButton.setChecked(False)

    def enableTool(self, enabled: bool = True) -> None:
        self.runPushButton.setEnabled(enabled)
    
    def runBuildPolygons(self, geom: QgsGeometry, merge = None):
        layer_list = QgsProject.instance().mapLayersByName('Centroides')
        outputLyr = None if len(layer_list) == 0 else layer_list[0]
        lyr = self.layerHandler.createMemoryLayerFromGeometry(geom, crs=QgsProject.instance().crs())
        outputCenterPointsLyr, _ = self.algRunner.runUnbuildPolygons(
            inputPolygonList=[lyr],
            lineConstraintLayerList=list(self.lineLayerDict.values()),
            context=QgsProcessingContext(),
        )
        outputCenterPointsLyr = self.runMerge(outputLyr, outputCenterPointsLyr) if outputLyr is not None else outputCenterPointsLyr
        outputCenterPointsLyr.setName('Centroides')
        node = self.findNode()
        QgsProject.instance().addMapLayer(outputCenterPointsLyr, addToLegend=False)
        node.addLayer(outputCenterPointsLyr)
        if outputLyr is not None:
            QgsProject.instance().removeMapLayer(outputLyr.id())
    
    def findNode(self):
        rootNode = QgsProject.instance().layerTreeRoot()
        groupName = "DSGTools_Output"
        groupNode = rootNode.findGroup(groupName)
        groupNode = groupNode if groupNode else rootNode.insertGroup(0, groupName)
        return groupNode
    
    def runMerge(self, existente, novo):
        merge = processing.run(
            'native:mergevectorlayers',
            {
                'LAYERS': [existente, novo],
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
        )
        return merge['OUTPUT']

    @pyqtSlot(bool, name="on_centerPointPushButton_toggled")
    def toggleBar(self, toggled: Optional[bool] = None) -> None:
        """
        Shows/Hides the tool bar
        """
        toggled = self.centerPointPushButton.isChecked() if toggled is None else toggled
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()

    def resetTool(self):
        self.lineLayerDict = dict()
        self.tool.deactivate()

    def syncLayers(self, layerids):
        for lyrid in layerids:
            if lyrid not in self.lineLayerDict:
                continue
            self.lineLayerDict.pop(lyrid)

    @pyqtSlot(bool)
    def on_runPushButton_clicked(self) -> None:
        if self.runPushButton.isChecked():
            self.iface.mapCanvas().setMapTool(self.tool)
        else:
            self.tool.deactivate()

    @pyqtSlot(bool)
    def on_configPushButton_clicked(self) -> None:
        lineLyrs = sorted(
            [
                i
                for i in QgsProject.instance().mapLayers().values()
                if isinstance(i, QgsVectorLayer)
                and i.geometryType() == QgsWkbTypes.LineGeometry
            ],
            key=lambda x: x.id(),
        )
        dlg = MultipleInputDialog(
            [i.name() for i in lineLyrs if i.id()],
            [
                idx
                for idx, lyrName in enumerate(lineLyrs)
                if lyrName in self.lineLayerDict.values()
            ],
        )
        dlg.exec()
        if dlg.selectedoptions is None:
            self.enableTool(enabled=self.lineLayerDict != dict())
            return
        selectedDict = {lineLyrs[i].id(): lineLyrs[i] for i in dlg.selectedoptions}
        self.lineLayerDict.update(selectedDict)

        keysToRemove = [k for k in self.lineLayerDict.keys() if k not in selectedDict]
        for key in keysToRemove:
            self.lineLayerDict.pop(key)
        self.enableTool(enabled=self.lineLayerDict != dict())

    def unload(self) -> None:
        self.iface.unregisterMainWindowAction(self.runPushButtonAction)
        self.iface.newProjectCreated.disconnect(self.resetTool)
        QgsProject.instance().layersWillBeRemoved.disconnect(self.syncLayers)
        self.iface.mapCanvas().unsetMapTool(self.tool)
