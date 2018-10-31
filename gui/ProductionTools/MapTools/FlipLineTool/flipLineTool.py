# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-03-19
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
from __future__ import absolute_import
from qgis.gui import QgsMapTool, QgsMessageBar
from qgis.core import QgsMapLayer, QgsVectorLayer, QgsMessageLog, QgsFeatureRequest, QgsWkbTypes, Qgis
from qgis.PyQt import QtCore, QtGui

from .....core.GeometricTools.geometryHandler import GeometryHandler

class FlipLine(QgsMapTool):
    """
    Tool expected behaviour:
    When (valid) line features are selected, it flips them upon tool activation.
    """
    def __init__(self, iface):
        self.iface = iface        
        self.canvas = self.iface.mapCanvas()
        self.toolAction = None
        QgsMapTool.__init__(self, self.canvas)
        self.DsgGeometryHandler = GeometryHandler(iface)
        self.currentLayer = None
    
    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + '/flipLineTool.png'
        toolTip = self.tr("DSGTools: Flip Line Tool\nInsert tool tip for Flip Line Tool.")
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Flip Line Tool'),
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar =parentMenu
        )
        self.setAction(action)

    def setToolEnabled(self, layer=None):
        """
        Checks if it is possible to use tool given layer editting conditions and type.
        :param layer: (QgsVectorLayer) layer that may have its lines flipped.
        :return: (bool) whether tool may be used.
        """
        if not isinstance(layer, QgsVectorLayer):
            layer = self.iface.mapCanvas().currentLayer()
        if not layer or not isinstance(layer, QgsVectorLayer) or layer.geometryType() != QgsWkbTypes.LineGeometry or not layer.isEditable():
            enabled = False
        else:
            enabled = True
        self.toolAction.setEnabled(enabled) if self.toolAction else None
        return enabled

    def activate(self):
        """
        Activates tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(False)
    
    def setAction(self, action):
        """
        Defines an action for tool.
        action: QAction to be set.
        """
        self.toolAction = action

    def getAllSelectedLines(self):
        """
        Gets all selected lines on canvas.
        """
        selection = []
        # for layer in self.iface.mapCanvas().layers():
        #     if (not isinstance(layer, QgsVectorLayer)) or layer.geometryType() != 1:
        #         continue
        # it is expected that Flip Line Tool only work on active layer features
        layer = self.iface.mapCanvas().currentLayer()
        for feat in layer.selectedFeatures():
            selection.append([layer, feat, layer.geometryType()])
        return selection

    def flipSelectedLines(self):
        """
        Method for flipping all selected lines. Used for button callback.
        """        
        # get all selected features and remove all features that are not lines
        selectedFeatures = self.getAllSelectedLines()
        pop = 0
        for idx, item in enumerate(selectedFeatures):
            if item[2] != 1:
                selectedFeatures.pop(idx-pop)
                pop += 1
        if not selectedFeatures:
            logMsg = self.getLogMessage(None, None)
            self.iface.messageBar().pushMessage(self.tr('Error'), logMsg, level=Qgis.Critical, duration=3)
            # QMessageBox.critical(self, self.tr('Critical!'), logMsg)
            QgsMessageLog.logMessage(logMsg, "DSG Tools Plugin", Qgis.Critical)
            return
        # call the method for flipping features from geometry module
        flippedLines, failedLines = self.DsgGeometryHandler.flipFeatureList(featureList=selectedFeatures, debugging=True)
        logMsg = self.getLogMessage(flippedLines, failedLines)
        self.iface.messageBar().pushMessage(self.tr('Success'), logMsg, level=Qgis.Info, duration=3)
        QgsMessageLog.logMessage(logMsg, "DSG Tools Plugin", Qgis.Info)
 
    def getLogMessage(self, flippedLines, failedLines):
        """
        Method for mounting log message to be exposed to user.
        :param flippedLines: list of lines that were selected and were successfully flipped.
        :param failedLines: list of lines that were selected and failed to be flipped.
        :param success: indicates whether the log is for a failed execution or 
        """
        nrFlipped = nrFailed = 0  
        if not flippedLines and not failedLines:
            return self.tr('There are no (valid) lines selected!')
        if flippedLines:
            nrFlipped = len(flippedLines)
            logMsg = self.tr("Feature(s) flipped: ")
            for item in flippedLines:
                logMsg += "{} (id={}), ".format(item[0].name(), item[1].id())
            logMsg = (logMsg + ")").replace(", )", "")
        elif failedLines:
            nrFailed = len(failedLines)
            logMsg += self.tr("\nFeature(s) that failed to be flipped: ")
            for item in failedLines:
                logMsg += "{} (id={}), ".format(item[0].name(), item[1].id())
            logMsg = (logMsg + ")").replace(", )", ".")
        return logMsg + self.tr("\n{} lines flipped. {} failed to be flipped.").format(nrFlipped, nrFailed)

    def startFlipLineTool(self):
        if self.canvas.currentLayer() in self.iface.editableLayers():
            self.flipSelectedLines()
        else:
            self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Start editing in current layer!'), level=Qgis.Info, duration=3)

    def deactivate(self):
        gui.QgsMapTool.deactivate(self)
        self.canvas.unsetMapTool(self)