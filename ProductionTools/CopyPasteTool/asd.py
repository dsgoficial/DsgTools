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
from builtins import range
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QGis, QgsPoint, QgsRectangle, QgsMapLayer, QgsFeatureRequest, QgsDataSourceUri, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsGeometry
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QMenu

import numpy as np
from qgis.PyQt.QtCore import Qt

class MultiLayerSelection(QgsMapTool):
    finished = QtCore.pyqtSignal(list)
    def __init__(self, canvas, iface):
        """
        Tool Behaviours: (all behaviours start edition, except for rectangle one)
        1- Left Click: Clears previous selection, selects feature, sets feature layer as active layer. 
        The selection is done with the following priority: Point, Line then Polygon. 
        Selection is only done in visible layer.
        2- Control + Left Click: Adds to selection selected feature. This selection follows the priority in item 1.
        3- Right Click: Opens feature form
        4- Control + Right Click: clears selection and set feature's layer as activeLayer. activeLayer's definition
        follows priority of item 1;
        5- Shift + drag and drop: draws a rectangle, then features that intersect this rectangle are added to selection
        """
        self.iface = iface        
        self.canvas = canvas
        self.toolAction = None
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        mFillColor = QColor( 254, 178, 76, 63 )
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
        self.reset()
        self.blackList = ['moldura']
        self.cursorChanged = False
        self.cursorChangingHotkey = QtCore.Qt.Key_Alt
        #self.iface.mapCanvas().setContextMenuPolicy(Qt.CustomContextMenu)
        #self.iface.mapCanvas().customContextMenuRequested.connect(self.createContextMenu)
    
    def reset(self):
        """
        Resets rubber band.
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)
    
    def keyPressEvent(self, e):
        """
        Reimplemetation of keyPressEvent() in order to handle cursor changing hotkey (F2).
        """
        if e.key() == self.cursorChangingHotkey and not self.cursorChanged:
            self.cursorChanged = True
            QtGui.QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.cursorChanged = False
            QtGui.QApplication.restoreOverrideCursor()         

    def canvasMoveEvent(self, e):
        """
        Used only on rectangle select.
        """
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates( e.pos() )
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        """
        Builds rubberband rect.
        """
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
        """
        Builds rectangle from self.startPoint and self.endPoint
        """
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None
        return QgsRectangle(self.startPoint, self.endPoint)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
    
    def canvasReleaseEvent(self, e):
        """
        After the rectangle is built, here features are selected.
        """
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = False
            r = self.rectangle()
            layers = self.canvas.layers()
            for layer in layers:
                #ignore layers on black list and features that are not vector layers
                if layer.type() != QgsMapLayer.VectorLayer or (self.layerHasPartInBlackList(layer.name())):
                    continue
                if r is not None:
                    #builds bbRect and select from layer, adding selection
                    bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                    layer.select(bbRect, True)
            self.rubberBand.hide()

    def canvasPressEvent(self, e):
        """
        Method used to build rectangle if shift is held, otherwise, feature select/deselect and identify is done.
        """
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = True
            self.startPoint = self.toMapCoordinates(e.pos())
            self.endPoint = self.startPoint
            self.isEmittingPoint = True
            self.showRect(self.startPoint, self.endPoint)
        else:
            self.isEmittingPoint = False
            # selected =  (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
            self.createContextMenu(e)
            # self.selectFeatures(e, hasControlModifyer = selected)
    
    def getCursorRect(self, e):
        """
        Calculates small cursor rectangle around mouse position. Used to facilitate operations
        """
        p = self.toMapCoordinates(e.pos())
        w = self.canvas.mapUnitsPerPixel() * 10
        return QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
    
    def layerHasPartInBlackList(self, lyrName):
        """
        Verifies if terms in black list appear on lyrName
        """
        for item in self.blackList:
            if item.lower() in lyrName.lower():
                return True
        return False
    
    def getPrimitiveDict(self, e, hasControlModifyer=False):
        """
        Builds a dict with keys as geometryTypes of layer, which are QGis.Point (value 0), QGis.Line (value 1) or QGis.Polygon (value 2),
        and values as layers from self.iface.legendInterface().layers(). When self.iface.legendInterface().layers() is called, a list of
        layers ordered according to lyr order in TOC is returned.
        """
        #these layers are ordered by view order
        primitiveDict = dict()
        for lyr in self.iface.legendInterface().layers(): #ordered layers
            #layer types other than VectorLayer are ignored, as well as layers in black list and layers that are not visible
            if (lyr.type() != QgsMapLayer.VectorLayer) or (self.layerHasPartInBlackList(lyr.name())) or not self.iface.legendInterface().isLayerVisible(lyr):
                continue
            geomType = lyr.geometryType()
            if geomType not in list(primitiveDict.keys()):
                primitiveDict[geomType] = []
            #removes selection
            if (not hasControlModifyer and e.button() == QtCore.Qt.LeftButton) or (hasControlModifyer and e.button() == QtCore.Qt.RightButton):
                lyr.removeSelection()
            primitiveDict[geomType].append(lyr)
        else:
            return primitiveDict

    def selectFeatures(self, e, bbRect=None, hasControlModifyer=False):
        """
        Method to select features acoording to mouse event e.
        Optional parameters:
        bbRect: if supplied, other rectangle is used
        hasControlModifyer: used to add to selection or not.
        """
        rect = self.getCursorRect(e)
        primitiveDict = self.getPrimitiveDict(e, hasControlModifyer = hasControlModifyer)
        primitives = list(primitiveDict.keys())
        primitives.sort() #this sort enables search to be done in the order of Point (value 0), Line (value 1) and Polygon (value 2)
        for primitive in primitives:
            for lyr in primitiveDict[primitive]:
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(lyr, rect)
                # bbRect = self.reprojectSearchArea(lyr, bbRect)
                for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                    selectedIds = lyr.selectedFeaturesIds() #list of selected ids
                    featGeom = feat.geometry()
                    if not featGeom:
                        continue
                    if featGeom.intersects(bbRect): #tests if feature intersects tool bounding box, otherwise skip it
                        lyr.startEditing() #starts layer editting
                        if e.button() == QtCore.Qt.RightButton:
                            #set target, start edit and stop
                            if hasControlModifyer:
                                #sets active layer. Since hasControlModifyer indicates to this method to clear selection, this part of
                                #the code completes the  control + right click behaviour.
                                self.iface.setActiveLayer(lyr)
                                return
                            else:
                                #opens feature form. The tag showModal is to lock qgis window or not. 
                                #Current procedure is to imitate qgis way of doing things, so showModal = False
                                self.iface.setActiveLayer(lyr)
                                self.iface.openFeatureForm(lyr,feat, showModal=False)
                                return
                        #if code reaches here, it means that it is an incremental selection.
                        if feat.id() in selectedIds:
                            lyr.modifySelection([],[feat.id()])
                        else:
                            lyr.modifySelection([feat.id()],[])
                        if not hasControlModifyer:
                            self.iface.setActiveLayer(lyr)
                            return
                       
    def deactivate(self):
        """
        Deactivate tool.
        """
        QtGui.QApplication.restoreOverrideCursor()
        try:
            if self.toolAction:
                self.toolAction.setChecked(False)
            if self is not None:
                QgsMapTool.deactivate(self)
        except:
            pass

    def activate(self):
        """
        Activate tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)

    def openFeatureForm(self, layer, feature):
        self.iface.setActiveLayer(layer)
        self.iface.openFeatureForm(layer, feature, showModal=False)

    def setSelectionFeature(self, layer, feature):
        """
        Selects a given feature on canvas.
        """
        idList = layer.selectedFeaturesIds()
        self.iface.setActiveLayer(layer)
        layer.startEditing()
        featId = feature.id()
        if featId not in idList:
            idList.append(featId)
        layer.setSelectedFeatures(idList)
        return 

    def setSelectionListFeature(self, listLayerFeature):
        """
        Selects all features in a given list on canvas.
        
        arg listLayerFeature: a list os items as of [layer, feature[, geometry_type]]
        """
        for item in listLayerFeature:
            self.setSelectionFeature(item[0], item[1])
        return

    def openMultipleFeatureForm(self, listLayerFeature):
        """
        Opens all features Attribute Tables of a given list.
        
        arg listLayerFeature: a list os items as of [layer, feature[, geometry_type]]
        """
        for item in listLayerFeature:
            self.iface.openFeatureForm(item[0], item[1], showModal=False)

    def filterStrongestGeometry(self, listLayerFeature):
        """
        Filter a given list of features for its strongest geometry

        arg listLayerFeature: a list os items as of [layer, feature, geometry_type]
        returns a list [layer, feature]
        """
        if listLayerFeature:
            strongest_geometry = np.array(np.array(listLayerFeature)[:,2], 'int').min()
        else:
            return []
        l = []
        for i in listLayerFeature:
            if i[2] == strongest_geometry:
                l.append(i)
        return l

    def createContextMenu(self, e):
        """
        Creates the context menu for overlapping layers
        """  
        selected =  (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
        # setting a list of features to iterate over
        layerList = self.getPrimitiveDict(e, hasControlModifyer = selected)
        layers = []
        for key in list(layerList.keys()):
            layers += layerList[key]
        if layers:
            menu = QtGui.QMenu()
            rect = self.getCursorRect(e)
            t = []
            for layer in layers:
                # iterate over features inside the mouse bounding box 
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect) #this maps cursor rect to lyr coordinates
                for feature in layer.getFeatures(QgsFeatureRequest(bbRect)):
                    geom = feature.geometry()
                    if geom:
                        searchRect = self.reprojectSearchArea(layer, rect)
                        if geom.intersects(searchRect):
                            t.append([layer, feature, layer.geometryType()])
            t = self.filterStrongestGeometry(t)
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
                    if selected:
                        if e.button() == QtCore.Qt.LeftButton: 
                            # line added to make sure the action is associated with
                            # current loop value.
                            action.triggered[()].connect(lambda t=[e, selected] : self.selectFeatures(t[0], hasControlModifyer=t[1]))
                        elif e.button() == QtCore.Qt.RightButton:
                            # remove feature from candidates of selection and set layer for selection
                            action.triggered[()].connect(lambda layer=layer : self.iface.setActiveLayer(layer))
                            t.pop(i-pop)
                            pop += 1
                            continue
                    else:
                        if e.button() == QtCore.Qt.LeftButton:
                            action.triggered[()].connect(lambda t=t[i] : self.setSelectionFeature(t[0], t[1]))
                        elif e.button() == QtCore.Qt.RightButton:
                            action.triggered[()].connect(lambda t=t[i] : self.openFeatureForm(t[0], t[1]))
                # "Select All" always selects all features
                # Sugestion: Open all atribute tables? 
                if e.button() == QtCore.Qt.LeftButton:
                    menu.addAction(self.tr('Select All'), lambda t=t: self.setSelectionListFeature(t))
                else:
                    menu.addAction(self.tr('Open All Attribute Tables'), lambda t=t: self.openMultipleFeatureForm(t))    
                menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
            elif t:                
                t = t[0]
                selected =  (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
                if e.button() == QtCore.Qt.LeftButton:
                    self.selectFeatures(e, hasControlModifyer = selected)
                elif selected:
                    self.iface.setActiveLayer(t[0])
                else:
                    self.openFeatureForm(t[0], t[1])

    def reprojectSearchArea(self, layer, geom):
        #geom always have canvas coordinates
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        #getting srid from something like 'EPSG:31983'
        srid = layer.crs().authid()
        if epsg == srid:
            return geom
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        crsDest = QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        auxGeom = QgsGeometry.fromRect(geom)
        auxGeom.transform(coordinateTransformer)
        return auxGeom.boundingBox()