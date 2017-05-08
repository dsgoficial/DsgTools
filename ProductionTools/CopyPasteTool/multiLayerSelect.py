# -*- coding: utf-8 -*-
"""
/***************************************************************************
multiLayerSelect
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
                               (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
                               borba.philipe@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin MultipleLayerSelection
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
from qgis.core import QGis, QgsPoint, QgsRectangle, QgsMapLayer, QgsFeatureRequest
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor

class MultiLayerSelection(QgsMapTool):
    finished = QtCore.pyqtSignal(list)
    def __init__(self, canvas, iface):
        self.iface=iface        
        self.canvas = canvas
        self.selecaoMulti=[]
        self.initSelectedIds()
        self.toolAction = None
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        mFillColor = QColor( 254, 178, 76, 63 )
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
        self.reset()
        self.blackList = ['moldura']
    
    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates( e.pos() )
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QGis.Polygon)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPoint(startPoint.x(), startPoint.y())
        point2 = QgsPoint(startPoint.x(), endPoint.y())
        point3 = QgsPoint(endPoint.x(), endPoint.y())
        point4 = QgsPoint(endPoint.x(), startPoint.y())
    
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)    # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None
    
        return QgsRectangle(self.startPoint, self.endPoint)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)

    def initSelectedIds(self):
        self.ids={}
        for l in self.canvas.layers():
            self.ids[l.name()] = []

    
    def canvasReleaseEvent(self, e):
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = False
            r = self.rectangle()
            layers = self.canvas.layers()
            for layer in layers:
                if layer.type() == QgsMapLayer.RasterLayer or (self.layerHasPartInBlackList(layer.name())):
                    continue
                if r is not None:
                    selectedIds = [feat.id for feat in layer.selectedFeatures()]
                    bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                    layer.select(bbRect, True)
            self.rubberBand.hide()

    def canvasPressEvent(self, e):
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = True
            self.startPoint = self.toMapCoordinates(e.pos())
            self.endPoint = self.startPoint
            self.isEmittingPoint = True
            self.showRect(self.startPoint, self.endPoint)
        else:
            self.isEmittingPoint = False
            selected =  (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
            self.selectFeatures(e, keepSelected = selected)
    
    def getCursorRect(self, e):
        p = self.toMapCoordinates(e.pos())
        w = self.canvas.mapUnitsPerPixel() * 10
        return QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
    
    def layerHasPartInBlackList(self, lyrName):
        for item in self.blackList:
            if item.lower() in lyrName.lower():
                return True
        return False
    
    def getPrimitiveDict(self, keepSelected = False):
        #these layers are ordered by view order
        primitiveDict = dict()
        for lyr in self.iface.legendInterface().layers():
            if (lyr.type() <> QgsMapLayer.VectorLayer) or (self.layerHasPartInBlackList(lyr.name())) or not self.iface.legendInterface().isLayerVisible(lyr):
                continue
            geomType = lyr.geometryType()
            if geomType not in primitiveDict.keys():
                primitiveDict[geomType] = []
            #removes selection
            if not keepSelected:
                lyr.removeSelection()
            primitiveDict[geomType].append(lyr)
        return primitiveDict
    
    def clearSelection(self):
        pass

    def selectFeatures(self, e, bbRect = None, keepSelected = False):
        if not bbRect:   
            rect = self.getCursorRect(e)
        if not keepSelected:
            self.clearSelection()
        primitiveDict = self.getPrimitiveDict(keepSelected = keepSelected)
        primitives = primitiveDict.keys()
        primitives.sort()
        for primitive in primitives:
            for lyr in primitiveDict[primitive]:
                if not bbRect:
                    bbRect = self.canvas.mapSettings().mapToLayerCoordinates(lyr, rect)
                for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                    if feat.geometry().intersects(bbRect):
                        lyr.startEditing()
                        if e.button() == QtCore.Qt.RightButton:
                            #set target, start edit and stop
                            if not keepSelected:
                                self.iface.setActiveLayer(lyr)
                                return
                            else:
                                self.iface.openFeatureForm(lyr,feat, showModal=False)
                                return
                        lyr.modifySelection([feat.id()],[])
                        if not keepSelected:
                            self.iface.setActiveLayer(lyr)
                            return
                       
    def deactivate(self):
        self.ids = {}
        if self.toolAction:
            self.toolAction.setChecked(False)
        if self is not None:
            QgsMapTool.deactivate(self)

    def activate(self):
        if self.toolAction:
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)
    
        






