# -*- coding: utf-8 -*-
"""
/***************************************************************************
multiLayerSelect
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2018-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QGis, QgsPoint, QgsRectangle, QgsMapLayer, QgsFeatureRequest, \
                      QgsVectorLayer, QgsDataSourceURI, QgsCoordinateReferenceSystem, \
                      QgsCoordinateTransform, QgsGeometry, QgsEditFormConfig
from PyQt4.QtCore import QSettings
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor, QMenu, QCursor

import numpy as np
from PyQt4.QtCore import Qt

class AssignBandValueTool(QgsMapTool):
    def __init__(self, canvas, iface, rasterLayer):
        """
        Tool Behaviours: (all behaviours start edition, except for rectangle one)
        1- Left Click: Creates a new point feature with the value from raster, according to selected attribute. 
        5- Shift + drag and drop: draws a rectangle, then features that intersect this rectangle are selected 
        and their value is set according to raster value and selected attribute.
        """
        QgsMapTool.__init__(self, self.canvas)
        self.iface = iface        
        self.canvas = canvas
        self.toolAction = None
        self.raster = rasterLayer
        self.setRubberbandParameters()
        self.reset()
        self.auxList = []

    def getSuppressOptions(self):
        qgisSettigns = QSettings()
        qgisSettigns.beginGroup('Qgis/digitizing')
        setting = qgisSettigns.value('disable_enter_attribute_values_dialog')
        qgisSettigns.endGroup()
        if not setting:
            return False
        if setting.lower() == u'false':
            return False
        else:
            return True

    def setRubberbandParameters(self):
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.hoverRubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        mFillColor = QColor( 254, 178, 76, 63 )
        self.rubberBand.setColor(mFillColor)
        self.hoverRubberBand.setColor(QColor( 255, 0, 0, 90 ))
        self.rubberBand.setWidth(1)
    
    def reset(self):
        """
        Resets rubber band.
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)

    def canvasMoveEvent(self, e):
        """
        Used only on rectangle select.
        """
        if self.menuHovered:
            # deactivates rubberband when the context menu is "destroyed" 
            self.hoverRubberBand.reset(QGis.Polygon)
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
        layer = self.iface.currentLayer()
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            self.isEmittingPoint = False
            r = self.rectangle()
            if r is None:
                return
            bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
            self.rubberBand.hide()
            #select all stuff
            layer.setSelectedFeatures([]) #portar para o feature handler
            layer.select(bbRect, True)
            #mudar depois para o dsgmothafucka
            featDict = dict()
            pointDict = dict()
            for feat in layer.selectedFeatures():
                featDict[feat.id()] = feat
                pointDict [feat.id()] = feat.geometry()
            pixelValueDict = self.getPixelValueFromPointDict(pointDict, self.rasterLayer)
            for idx in pointDict:
                self.auxList.append({'featId':idx, 'feat':featDict[idx], 'value':pixelValueDict[idx]})
        else:
            value, pointGeom = self.getPixelValue(self.rasterLayer)
            self.auxList.append({'geom':pointGeom, 'value':value})
        #create context menu to select attribute
        self.createContextMenuOnPosition(self, e, layer)

    def createContextMenuOnPosition(self, e, layer):
        menu = QMenu()
        callbackDict = dict()
        fieldList = [field.name() for field in layer.fields() if field.isNumeric()]
        for field in fieldList:
            action = menu.addAction(field)
            callback = lambda t = [field, layer] : self.handleFeatures(t[0], t[1])
            action.triggered[()].connect(callback)
        menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
    
    def handleFeatures(self, selectedField, layer):
        updateList = []
        addList = []
        layer.startEditing()
        for item in self.auxList:
            if 'featId' in item:
                feat = item['feat']
                feat[selectedField] = item['value']
                updateList.append(feat)
            else:
                feature = QgsFeature(layer.fields())
                feature.setGeometry(item['geom'])
                self.addFeature(feature, layer, selectedField, item['value'])
        if updateList:
            layer.updateFeatures(updateList)
    
    def addFeature(self, feature, layer, field, value):
        fields = layer.fields()
        feature.initAttributes(fields.count())            
        provider = layer.dataProvider()              
        for i in range(fields.count()):
            if fields[i].name() != field:
                value = provider.defaultValueClause(i)
            if value:
                feature.setAttribute(i, value)                
        form = QgsAttributeDialog(layer, feature, False)
        form.setMode(QgsAttributeForm.AddFeatureMode)
        formSuppress = layer.editFormConfig().suppress()
        if formSuppress == QgsEditFormConfig.SuppressDefault:
            if self.getSuppressOptions(): #this is calculated every time because user can switch options while using tool
                layer.addFeature(feature, True)
            else:
                if not form.exec_():
                    feature.setAttributes(form.feature().attributes())
        elif formSuppress == QgsEditFormConfig.SuppressOff:
            if not form.exec_():
                feature.setAttributes(form.feature().attributes())
        else:
            layer.addFeature(feature, True)


        


    
    def getCursorRect(self, e):
        """
        Calculates small cursor rectangle around mouse position. Used to facilitate operations
        """
        p = self.toMapCoordinates(e.pos())
        w = self.canvas.mapUnitsPerPixel() * 10
        return QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
    
    def deactivate(self):
        """
        Deactivate tool.
        """
        QtGui.QApplication.restoreOverrideCursor()
        self.hoverRubberBand.reset(QGis.Polygon)
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


    def reprojectSearchArea(self, layer, geom):
        """
        Reprojects search area if necessary, according to what is being searched.
        :param layer: (QgsVectorLayer) layer which target rectangle has to have same SRC.
        :param geom: (QgsRectangle) rectangle representing search area.
        """
        #geom always have canvas coordinates
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        #getting srid from something like 'EPSG:31983'
        srid = layer.crs().authid()
        if epsg == srid:
            return geom
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        crsDest = QgsCoordinateReferenceSystem(srid)
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest) # here we have to put authid, not srid
        auxGeom = QgsGeometry.fromRect(geom)
        auxGeom.transform(coordinateTransformer)
        return auxGeom.boundingBox()

    def getPixelValue(self, rasterLayer):
        mousePos = self.QgsMapToolEmitPoint.toMapCoordinates(self.canvas.mouseLastXY())
        mousePosGeom = QgsGeometry.fromPoint(mousePos)
        return self.getPixelValueFromPoint(mousePosGeom, rasterLayer), mousePosGeom
    
    def getPixelValueFromPoint(self, mousePosGeom, rasterLayer):
        """
        
        """
        rasterCrs = rasterLayer.crs()
        self.DsgGeometryHandler.reprojectFeature(mousePosGeom, rasterCrs, self.canvasCrs)
        mousePos = mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify( mousePos, QgsRaster.IdentifyFormatValue )
        if i.isValid():
            return i.results().values()[0]
        else:
            return None
    
    def getPixelValueFromPointDict(self, pointDict, rasterLayer):
        """
        pointDict = {'pointId':QgsGeometry}

        returns {'pointId': value}
        """
        return {key:self.getPixelValueFromPoint(value, rasterLayer) for key, value in pointDict.iteritems()} #no python3 eh items()
