# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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
from functools import partial

from qgis.core import (
    QgsGeometry,
    QgsRaster,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsWkbTypes,
    Qgis
)

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QTimer
from qgis.PyQt.QtWidgets import QWidget, QToolTip, QAction
from qgis.PyQt.QtGui import QIcon

from DsgTools.gui.ProductionTools.Toolbars.DsgRasterInfoTool.bandValueTool import (
    BandValueTool,
)
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.gui.ProductionTools.Toolbars.DsgRasterInfoTool.assignBandValueTool import (
    AssignBandValueTool,
)

# FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'dsgRasterInfoTool.ui'))
from .dsgRasterInfoTool_ui import Ui_DsgRasterInfoTool

class DsgRasterInfoTool(QWidget, Ui_DsgRasterInfoTool):
    """
    This class is supposed to help revision operators. It shows, on mouse hovering
    raster layer's band values. For a MDS product, altimetry is, then, given.
    Tool Behaviour:
    1- On hoverring a pixel: expose band value(s)
    2- On mouse click: create a new instance of desired layer (filled on config).
        * behaviour 2 is an extrapolation of first conception
    """

    def __init__(self, iface, parent=None):
        """
        Class constructor.
        """
        self.canvas = iface.mapCanvas()
        super(DsgRasterInfoTool, self).__init__(parent)
        self.setupUi(self)
        self.bandTooltipButton.setToolTip(self.tr("Show raster tooltip"))
        self.dynamicHistogramButton.setToolTip(self.tr("Dynamic histogram view"))
        self.valueSetterButton.setToolTip(
            self.tr(
                "Set raster value from mouse click\nShift + Left Click + Mouse Drag: Selects a set of points and assigns raster value for each point"
            )
        )
        self.assignBandValueTool = None
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        self.timerMapTips = QTimer(self.canvas)
        self.geometryHandler = GeometryHandler(iface)
        self.addShortcuts()
        self.valueSetterButton.setEnabled(False)
        self.iface.mapCanvas().currentLayerChanged.connect(self.enableAssignValue)
        self.iface.actionToggleEditing().triggered.connect(self.enableAssignValue)
        self.iface.mapCanvas().mapToolSet.connect(self.enableAssignValue)
        self.valueSetterButton.toggled.connect(self.activateValueSetter)
        # self.rasterComboBox.currentIndexChanged.connect(self.enableAssignValue)
        # start currentLayer selection
        self.currentLayer = None

    def resetEditingSignals(self, currentLayer):
        """
        Disconnects editing signal from previously selected layer and connects it to newly selected layer.
        Method is called whenever currentlLayerChanged signal is emitted.
        """
        # get previous selected layer
        prevLayer = self.currentLayer
        # update current selected layer
        if not currentLayer:
            self.currentLayer = currentLayer
        self.activateAlias = partial(self.activateValueSetter, True)
        self.deactivateAlias = partial(self.activateValueSetter, False)
        if prevLayer:
            try:
                # if there was a previous selection, signals must be disconnected from it before connecting to the new layer
                prevLayer.editingStarted.disconnect(self.activateAlias)
                prevLayer.editingStopped.disconnect(self.deactivateAlias)
            except:
                # in case signal is not yet connected, somehow
                pass
        # connecting signals to new layer
        if isinstance(self.currentLayer, QgsVectorLayer):
            if self.currentLayer.geometryType() == QgsWkbTypes.PointGeometry:
                self.currentLayer.editingStarted.connect(self.activateAlias)
                self.currentLayer.editingStopped.connect(self.deactivateAlias)

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def addShortcuts(self):
        icon_path = ":/plugins/DsgTools/icons/rasterToolTip.png"
        text = self.tr("DSGTools: Raster information tool")
        self.activateToolAction = self.add_action(
            icon_path, text, self.rasterInfoPushButton.toggle, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.activateToolAction, "")
        icon_path = ":/plugins/DsgTools/icons/band_tooltip.png"
        text = self.tr("DSGTools: Band tooltip")
        self.bandTooltipButtonAction = self.add_action(
            icon_path, text, self.bandTooltipButton.toggle, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.bandTooltipButtonAction, "")
        icon_path = ":/plugins/DsgTools/icons/dynamic_histogram_viewer.png"
        text = self.tr("DSGTools: Dynamic Histogram Viewer")
        self.dynamicHistogramButtonAction = self.add_action(
            icon_path, text, self.dynamicHistogramButton.toggle, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.dynamicHistogramButtonAction, "")
        icon_path = ":/plugins/DsgTools/icons/valueSetter.png"
        text = self.tr("DSGTools: Set Value From Point")
        self.valueSetterButtonAction = self.add_action(
            icon_path, text, self.valueSetterButton.toggle, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.valueSetterButtonAction, "")
        self.refreshPushButtonAction = self.add_action(
            icon_path, text, self.refreshPushButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.refreshPushButtonAction, "")
        self.refreshPushButton.setToolTip(
            self.tr("Set current layer as selected layer on inspect tool")
        )
        # self.timerMapTips.timeout.connect( self.showToolTip )

    def disconnectAllSignals(self):
        """
        Disconnects all signals connected/related to Set Value Checker tool.
        """
        try:
            self.valueSetterButton.toggled.disconnect(self.activateValueSetter)
            # self.valueSetterButton.blockSignals(True)
        except:
            pass
        # try:
        #     self.rasterComboBox.currentIndexChanged.disconnect(self.enableAssignValue)
        # except:
        #     pass
        try:
            self.iface.mapCanvas().currentLayerChanged.disconnect(
                self.enableAssignValue
            )
        except:
            pass
        try:
            self.iface.actionToggleEditing().triggered.disconnect(
                self.enableAssignValue
            )
        except:
            pass
        try:
            self.iface.mapCanvas().mapToolSet.disconnect(self.enableAssignValue)
        except:
            pass
        try:
            self.currentLayer.editingStarted.disconnect(self.activateAlias)
        except:
            pass
        try:
            self.currentLayer.editingStopped.disconnect(self.deactivateAlias)
        except:
            pass

    def connectAllSignals(self):
        """
        Connects all signals connected/related to Set Value Checker tool.
        """
        self.valueSetterButton.toggled.connect(self.activateValueSetter)
        # self.valueSetterButton.blockSignals(False)
        self.iface.mapCanvas().currentLayerChanged.connect(self.enableAssignValue)
        self.iface.actionToggleEditing().triggered.connect(self.enableAssignValue)
        self.iface.mapCanvas().mapToolSet.connect(self.enableAssignValue)
        # self.rasterComboBox.currentIndexChanged.connect(self.enableAssignValue)
        if self.currentLayer:
            self.currentLayer.editingStarted.connect(self.activateAlias)
            self.currentLayer.editingStopped.connect(self.deactivateAlias)

    def enableAssignValue(self, newTool=None, oldTool=None):
        self.disconnectAllSignals()
        layer = self.iface.mapCanvas().currentLayer()
        if layer and isinstance(layer, QgsVectorLayer):
            if (
                layer.geometryType() == QgsWkbTypes.PointGeometry
                and layer.isEditable()
                and not self.rasterComboBox.currentLayer() is None
            ):
                self.valueSetterButton.setEnabled(True)
                # reset editing signals
                self.resetEditingSignals(currentLayer=layer)
            else:
                self.valueSetterButton.setEnabled(False)
                if self.valueSetterButton.isChecked():
                    self.valueSetterButton.setChecked(False)
                    self.activateValueSetter(False)
        else:
            self.valueSetterButton.setEnabled(False)
            if self.valueSetterButton.isChecked():
                self.valueSetterButton.setChecked(False)
                self.activateValueSetter(False)
        self.connectAllSignals()

    def deactivate(self):
        self.activateBandValueTool(False)
        self.activateStretchTool(False)
        self.activateValueSetter(False)

    @pyqtSlot(bool, name="on_rasterInfoPushButton_toggled")
    def toggleBar(self, toggled=None):
        """
        Shows/Hides the tool bar
        """
        if toggled is None:
            toggled = self.rasterInfoPushButton.isChecked()
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()

    @pyqtSlot(bool, name="on_bandTooltipButton_toggled")
    def activateBandValueTool(self, state):
        if state:
            self.iface.mapCanvas().xyCoordinates.connect(self.showToolTip)
        else:
            self.iface.mapCanvas().xyCoordinates.disconnect(self.showToolTip)

    @pyqtSlot(bool, name="on_dynamicHistogramButton_toggled")
    def activateStretchTool(self, state):
        if state:
            self.iface.mapCanvas().extentsChanged.connect(self.stretch_raster)
        else:
            self.iface.mapCanvas().extentsChanged.disconnect(self.stretch_raster)

    def stretch_raster(self):
        try:
            formerLayer = self.iface.activeLayer()
            layer = self.rasterComboBox.currentLayer()
            # keep track of current tool status
            assignValueStatus = self.valueSetterButton.isChecked()
            self.iface.setActiveLayer(layer)
            self.iface.mainWindow().findChild(
                QAction, "mActionLocalCumulativeCutStretch"
            ).trigger()
            self.iface.setActiveLayer(formerLayer)
            # make sure it still be on, if necessary
            if assignValueStatus:
                self.valueSetterButton.setChecked(assignValueStatus)
        except AttributeError:
            pass

    # @pyqtSlot(bool, name = 'on_valueSetterButton_toggled')
    def activateValueSetter(self, state):
        if state:
            raster = self.rasterComboBox.currentLayer()
            self.loadTool(self.iface, raster)
        else:
            self.unloadTool()

    def loadTool(self, iface, raster):
        self.disconnectAllSignals()
        self.assignBandValueTool = AssignBandValueTool(self.iface, raster)
        self.assignBandValueTool.activate()
        self.iface.mapCanvas().setMapTool(self.assignBandValueTool)
        self.connectAllSignals()

    def unloadTool(self):
        self.disconnectAllSignals()
        if self.assignBandValueTool:
            self.assignBandValueTool.deactivate()
            self.iface.mapCanvas().unsetMapTool(self.assignBandValueTool)
        self.assignBandValueTool = None
        self.iface.mapCanvas().mapToolSet.connect(self.enableAssignValue)
        self.connectAllSignals()

    def getPixelValue(self, mousePos, rasterLayer):
        """ """
        rasterCrs = rasterLayer.crs()
        mousePosGeom = QgsGeometry.fromPointXY(mousePos)
        canvasCrs = self.canvas.mapSettings().destinationCrs()
        self.geometryHandler.reprojectFeature(mousePosGeom, rasterCrs, canvasCrs)
        mousePos = mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify(mousePos, QgsRaster.IdentifyFormatValue)
        if i.isValid():
            text = ", ".join(
                ["{0:g}".format(r) for r in list(i.results().values()) if r is not None]
            )
        else:
            text = ""
        return text

    def showToolTip(self, qgsPoint):
        """ """
        self.timerMapTips.stop()
        self.timerMapTips.start(6000)  # time in milliseconds
        if self.canvas.underMouse():
            raster = self.rasterComboBox.currentLayer()
            if raster:
                text = self.getPixelValue(qgsPoint, raster)
                p = self.canvas.mapToGlobal(self.canvas.mouseLastXY())
                QToolTip.showText(p, text, self.canvas)

    @pyqtSlot(bool)
    def on_refreshPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if isinstance(activeLayer, QgsRasterLayer):
            self.rasterComboBox.setLayer(activeLayer)
        else:
            self.iface.messageBar().pushMessage(
                self.tr("Warning!"),
                self.tr("Active layer is not valid to be used in this tool."),
                level=Qgis.Warning,
                duration=2,
            )

    def unload(self):
        self.disconnectAllSignals()
        try:
            self.iface.mapCanvas().extentsChanged.disconnect(self.stretch_raster)
        except:
            pass
        try:
            self.iface.mapCanvas().xyCoordinates.disconnect(self.showToolTip)
        except:
            pass
        self.iface.unregisterMainWindowAction(self.activateToolAction)
        self.iface.unregisterMainWindowAction(self.valueSetterButtonAction)
        self.iface.unregisterMainWindowAction(self.bandTooltipButtonAction)
        self.iface.unregisterMainWindowAction(self.dynamicHistogramButtonAction)
