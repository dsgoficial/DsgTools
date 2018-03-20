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

from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QGis, QgsPoint, QgsRectangle, QgsMapLayer, QgsFeatureRequest, QgsDataSourceURI, QgsVectorLayer
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor, QMenu, QCursor

import numpy as np
from PyQt4.QtCore import Qt
from DsgTools.ProductionTools.CopyPasteTool.multiLayerSelect import MultiLayerSelection
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class FlipLine(MultiLayerSelection):
    def __init__(self, canvas, iface):
        super(FlipLine, self).__init__(canvas, iface)

    def selectFlipLine(self):
        self.iface.mapCanvas().setMapTool(FlipLine(self.iface.mapCanvas(), self.iface))

    def activate(self):
        """
        Activate tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)

    def checkSelectedLayers(self):
        """
        Reimplementation from parent class. Checks if there are any line type feature selected.
        """
        geom = None
        for layer in self.iface.legendInterface().layers():
            selection = layer.selectedFeatures()
            if isinstance(layer, QgsVectorLayer):
                if len(selection):
                    if layer.geometryType() == 1:
                        geom = layer.geometryType()
                        break
        return geom

    def canvasReleaseEvent(self, e):
        """
        Reimplementation of parent class. Selects all line features inside the rectangle created by dragging
        the mouse around canvas whilst holding Shift key.
        After the rectangle is built, here features are selected.
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

    def getAllSelectedFeatures(self):
        """
        Gets all selected lines on canvas.
        """
        selection = []
        for layer in self.iface.legendInterface().layers():
            if (not isinstance(layer, QgsVectorLayer)) or layer.geometryType() != 1:
                return
            selection += layer.selectedFeatures()
        return selection

    def createContextMenu(self, e):
        """
        Reimplementation of parent method.
        :param e: mouse event caught from canvas
        """ 
        selected = (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
        if selected:
            firstGeom = self.checkSelectedLayers()
        # setting a list of features to iterate over
        layerList = self.getPrimitiveDict(e, hasControlModifyer=selected)
        # getting all features that are already selected on canvas
        layers = self.getAllSelectedFeatures()
        # only line should be dealt with by this tool
        if 1 in layerList.keys():
            layers += layerList[1]
        else:
            return
        if layers:
            menu = QtGui.QMenu()
            rect = self.getCursorRect(e)
            t = []
            for layer in layers:
                # iterate over features inside the mouse bounding box 
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
                for feature in layer.getFeatures(QgsFeatureRequest(bbRect)):
                    geom = feature.geometry()
                    if geom:
                        if geom.intersects(rect):
                            t.append([layer, feature, layer.geometryType()])
            if len(t) > 1:
                pop = 0 # number of features 
                for i in range(0, len(t)):
                    [layer, feature, geom] = t[i-pop] # geom to avoid dimension issues
                    # layers from different dabases may have the same name
                    # hence the need of db_name
                    self.iface.setActiveLayer(layer) # a layer must be active in order to get db_name
                    dsUri = self.iface.activeLayer().dataProvider().dataSourceUri()
                    if '/' in dsUri:
                        db_name = dsUri
                    else:
                        db_name = self.iface.activeLayer().dataProvider().dataSourceUri().split("'")[1]
                    s = '{0}.{1} (feat_id = {2})'.format(db_name, layer.name(), feature.id())
                    action = menu.addAction(s) # , lambda feature=feature : self.setSelectionFeature(layer, feature))
                    # handling CTRL key and left/right click actions
                    if e.button() == QtCore.Qt.LeftButton: 
                            # line added to make sure the action is associated with current loop value,
                            # lambda function is used with standard parameter set to current loops value.
                            triggeredAction = lambda t=t[i] : self.setSelectionFeature(t[0], t[1])
                            hoveredAction = lambda t=t[i] : self.createRubberBand(feature=t[1], layer=t[0], geom=t[2])
                    elif e.button() == QtCore.Qt.RightButton:
                        if selected:                        
                            triggeredAction = lambda layer=layer : self.iface.setActiveLayer(layer)
                            hoveredAction = None
                            # remove feature from candidates of selection and set layer for selection
                            t.pop(i-pop)
                            pop += 1
                            continue
                        else:
                            triggeredAction = lambda t=t[i] : self.iface.openFeatureForm(t[0], t[1], showModal=False)
                            hoveredAction = lambda t=t[i] : self.createRubberBand(feature=t[1], layer=t[0], geom=t[2])
                    self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
                # setting the action for the "All" options
                action = menu.addAction(self.tr('Invert All Lines'))
                triggeredAction = lambda t=t: self.invertListFeature(t)
                # to trigger "Hover" signal on QMenu for the multiple options
                hoveredAction = lambda t=t : self.createMultipleRubberBand(featureList=t)
                self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
                menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
            elif t:
                t = t[0]
                selected =  (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
                if e.button() == QtCore.Qt.LeftButton:
                    self.selectFeatures(e, hasControlModifyer = selected)
                elif selected:
                    self.iface.setActiveLayer(t[0])
                else:
                    self.iface.openFeatureForm(t[0], t[1], showModal=False)