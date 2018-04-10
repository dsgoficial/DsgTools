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
from qgis.core import QgsMapLayer, QgsVectorLayer, QgsMessageLog, QgsFeatureRequest, Qgis
from qgis.PyQt import QtCore, QtGui

from .....core.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

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
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
    
    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + '/flipLineTool.png'
        toolTip = self.tr("DSGTools: Flip Line Tool\nInsert tool tip for Flip Line Tool.")
        manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Flip Line Tool'),
            callback=callback,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar =parentMenu
        )

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

    def canvasReleaseEvent(self, e):
        """
        Selects all line features inside the rectangle created by dragging the mouse around 
        canvas whilst holding Shift key.
        :param e: mouse event on canvas.
        """
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = False
            r = self.rectangle()
            layers = self.canvas.layers()
            for layer in layers:
                #ignore layers on black list and features that are not vector layers and if layer not a line
                if (not isinstance(layer, QgsVectorLayer)) or layer.geometryType() != 1 or (self.layerHasPartInBlackList(layer.name())):
                    continue
                if r is not None:
                    #builds bbRect and select from layer, adding selection
                    bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                    layer.select(bbRect, True)
            self.rubberBand.hide()

    def getAllSelectedLines(self):
        """
        Gets all selected lines on canvas.
        """
        selection = []
        for layer in self.iface.mapCanvas().layers():
            if (not isinstance(layer, QgsVectorLayer)) or layer.geometryType() != 1:
                continue
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
            # QtGui.QMessageBox.critical(self, self.tr('Critical!'), logMsg)
            QgsMessageLog.logMessage(logMsg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
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

    # def flipLine(self, layer, line):
    #     """
    #     Flips the given line.
    #     :param layer: layer containing the target feature
    #     :param line: target feature to be flipped 
    #     """
    #     print "INVERTEU {} (id={})!".format(layer.name(), line.id())

    # def flipLineList(self, lineList):
    #     """
    #     Flips all lines in a given list.
    #     :param lineList: a list os items as of [layer, line_feature[, geometry_type]]
    #     """
    #     for item in lineList:
    #          self.flipLine(layer=item[0], line=item[1])
            
    # def createContextMenu(self, e):
    #     """
    #     Reimplementation of parent method. Context Menu created to support feature selection.
    #     :param e: mouse event caught from canvas
    #     """ 
    #     selected = (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
    #     # setting a list of features to iterate over
    #     layerList = self.getPrimitiveDict(e, hasControlModifyer=selected)
    #     # getting all features that are already selected on canvas
    #     t = self.getAllSelectedFeatures()
    #     # only line should be dealt with by this tool
    #     if 1 in layerList.keys():
    #         layers = layerList[1]
    #     elif not layers:
    #         return
    #     if layers:
    #         menu = QtGui.QMenu()
    #         rect = self.getCursorRect(e)
    #         for layer in layers:
    #             if not isinstance(layer, QgsVectorLayer):
    #                 continue
    #             # iterate over features inside the mouse bounding box 
    #             bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
    #             for feature in layer.getFeatures(QgsFeatureRequest(bbRect)):
    #                 geom = feature.geometry()
    #                 if geom:
    #                     if geom.intersects(rect):
    #                         t.append([layer, feature, layer.geometryType()])
    #         if len(t) > 1:
    #             pop = 0 # number of features 
    #             for i in range(0, len(t)):
    #                 [layer, feature, geom] = t[i-pop] # geom to avoid dimension issues
    #                 # layers from different dabases may have the same name
    #                 # hence the need of db_name
    #                 self.iface.setActiveLayer(layer) # a layer must be active in order to get db_name
    #                 dsUri = self.iface.activeLayer().dataProvider().dataSourceUri()
    #                 if '/' in dsUri:
    #                     db_name = dsUri
    #                 else:
    #                     db_name = self.iface.activeLayer().dataProvider().dataSourceUri().split("'")[1]
    #                 s = '{0}.{1} (feat_id = {2})'.format(db_name, layer.name(), feature.id())
    #                 action = menu.addAction(s)
    #                 # handling CTRL key and left/right click actions
    #                 if e.button() == QtCore.Qt.LeftButton: 
    #                         # line added to make sure the action is associated with current loop value,
    #                         # lambda function is used with standard parameter set to current loops value.
    #                         triggeredAction = lambda t=t[i] : self.setSelectionFeature(layer=t[0], feature=t[1], selectAll=selected)
    #                         hoveredAction = lambda t=t[i] : self.createRubberBand(feature=t[1], layer=t[0], geom=t[2])
    #                 self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
    #             # setting the action for the "All" options
    #             if e.button() == QtCore.Qt.LeftButton:
    #                 action = menu.addAction(self.tr('Select All Lines'))
    #                 triggeredAction = lambda t=t: self.setSelectionListFeature(listLayerFeature=t)
    #             # to trigger "Hover" signal on QMenu for the multiple options
    #             hoveredAction = lambda t=t : self.createMultipleRubberBand(featureList=t)
    #             self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
    #             menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
    #         elif t:
    #             t = t[0]
    #             if e.button() == QtCore.Qt.LeftButton:
    #                 self.selectFeatures(e, hasControlModifyer = selected)
