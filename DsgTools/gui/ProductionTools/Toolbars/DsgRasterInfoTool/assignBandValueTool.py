# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2018-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

from functools import partial

from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolEmitPoint, \
                     QgsAttributeDialog, QgsAttributeForm, QgsMessageBar
from qgis import core
from qgis.core import QgsPointXY, QgsRectangle, QgsVectorLayer, QgsGeometry, \
                      QgsEditFormConfig, QgsRaster, QgsFeature, QgsWkbTypes, \
                      QgsProject, QgsVectorLayerUtils, Qgis
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QMenu, QApplication

from qgis.PyQt.QtCore import Qt
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

class AssignBandValueTool(QgsMapTool):
    def __init__(self, iface, rasterLayer):
        """
        Tool Behaviours: (all behaviours start edition, except for rectangle one)
        1- Left Click: Creates a new point feature with the value from raster, according to selected attribute. 
        5- Shift + drag and drop: draws a rectangle, then features that intersect this rectangle are selected 
        and their value is set according to raster value and selected attribute.
        """
        self.iface = iface        
        self.canvas = self.iface.mapCanvas()
        QgsMapTool.__init__(self, self.canvas)
        self.toolAction = None
        self.qgsMapToolEmitPoint = QgsMapToolEmitPoint(self.canvas)
        self.geometryHandler = GeometryHandler(iface)
        self.rasterLayer = rasterLayer
        self.setRubberbandParameters()
        self.reset()
        self.auxList = []
        self.decimals = self.getDecimals()

    def getDecimals(self):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        decimals = settings.value('decimals')
        if decimals:
            return int(decimals)
        else:
            return 0
    
    def getSuppressOptions(self):
        qgisSettings = QSettings()
        qgisSettings.beginGroup('qgis/digitizing')
        setting = qgisSettings.value('disable_enter_attribute_values_dialog')
        qgisSettings.endGroup()
        return setting

    def setRubberbandParameters(self):
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.hoverRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
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
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)

    def canvasPressEvent(self, e):
        """
        Method used to build rectangle if shift is held, otherwise, feature select/deselect and identify is done.
        :param e: (QgsMouseEvent) mouse event.
        """
        if e.button() == QtCore.Qt.LeftButton:
            self.auxList = []
            if QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
                self.isEmittingPoint = True
                self.startPoint = self.toMapCoordinates(e.pos())
                self.endPoint = self.startPoint
                self.isEmittingPoint = True
                self.showRect(self.startPoint, self.endPoint)

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
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())
    
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
        # tool was planned to work on left click 
        if e.button() == QtCore.Qt.LeftButton:
            layer = self.iface.mapCanvas().currentLayer()
            if QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
                self.isEmittingPoint = False
                r = self.rectangle()
                if r is None:
                    return
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                self.rubberBand.hide()
                #select all stuff
                layer.selectByIds([]) #portar para o feature handler
                layer.selectByRect(bbRect)
                #mudar depois para o dsgmothafucka
                featDict = dict()
                pointDict = dict()
                for feat in layer.selectedFeatures():
                    featDict[feat.id()] = feat
                    pointDict[feat.id()] = feat.geometry()
                pixelValueDict = self.getPixelValueFromPointDict(pointDict, self.rasterLayer)
                for idx in pointDict:
                    value = pixelValueDict[idx]
                    if value:
                        self.auxList.append({'featId':idx, 'feat':featDict[idx], 'value':value})
            else:
                value, pointGeom = self.getPixelValue(self.rasterLayer)
                if value:
                    self.auxList.append({'geom':pointGeom, 'value':value})
            #create context menu to select attribute
            if self.auxList:
                self.createContextMenuOnPosition(e, layer)
            self.iface.mapCanvas().currentLayer().triggerRepaint()

    def createContextMenuOnPosition(self, e, layer):
        menu = QMenu()
        callbackDict = dict()
        fieldList = [field.name() for field in layer.fields() if field.isNumeric()]
        for field in fieldList:
            action = menu.addAction(field)
            callback = partial(self.handleFeatures, field, layer)
            action.triggered.connect(callback)
        menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
    
    def handleFeatures(self, selectedField, layer):
        layer.startEditing()
        for item in self.auxList:
            if 'featId' in item:
                feat = item['feat']
                idx = feat.fieldNameIndex(selectedField)
                feat.setAttribute(idx, item['value'])
                layer.updateFeature(feat)
            else:
                self.geometryHandler.reprojectFeature(item['geom'], layer.crs())
                feature = QgsVectorLayerUtils.createFeature(layer, item['geom'])
                self.addFeature(feature, layer, selectedField, item['value'])
        self.auxList = []
        self.canvas.refresh()
    
    def addFeature(self, feature, layer, field, pointValue):
        fields = layer.fields()          
        provider = layer.dataProvider()             
        for i in range(fields.count()):
            value = provider.defaultValue(i) if fields[i].name() != field else pointValue
            if value is not None:
                feature.setAttribute(i, value)                
        form = QgsAttributeDialog(layer, feature, False)
        form.setMode(int(QgsAttributeForm.AddFeatureMode))
        formSuppress = layer.editFormConfig().suppress()
        if formSuppress == QgsEditFormConfig.SuppressDefault:
            if self.getSuppressOptions(): #this is calculated every time because user can switch options while using tool
                layer.addFeature(feature)
            else:
                if not form.exec_():
                    feature.setAttributes(form.feature().attributes())
        elif formSuppress == QgsEditFormConfig.SuppressOff:
            if not form.exec_():
                feature.setAttributes(form.feature().attributes())
        else:
            layer.addFeature(feature)

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
        QApplication.restoreOverrideCursor()
        self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        try:
            if self.toolAction:
                self.toolAction.setChecked(False)
            if self is not None:
                QgsMapTool.deactivate(self)
                # self.canvas.unsetMapTool(self)
        except:
            pass

    def activate(self):
        """
        Activate tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)
        # self.iface.mapCanvas().setMapTool(self)
        layer = self.iface.mapCanvas().currentLayer()
        if not layer or not isinstance(layer, QgsVectorLayer):
            self.iface.messageBar().pushMessage(self.tr("Warning"), self.tr("Select a point vector layer as the active layer"), level=Qgis.Warning, duration=5)
            self.deactivate()

    def getPixelValue(self, rasterLayer):
        mousePos = self.qgsMapToolEmitPoint.toMapCoordinates(self.canvas.mouseLastXY())
        mousePosGeom = QgsGeometry.fromPointXY(mousePos)
        return self.getPixelValueFromPoint(mousePosGeom, rasterLayer), mousePosGeom

    def getPixelValueFromPoint(self, mousePosGeom, rasterLayer, fromCanvas=True):
        """
        
        """
        rasterCrs = rasterLayer.crs()
        # if fromCanvas:
        #     self.geometryHandler.reprojectFeature(mousePosGeom, rasterCrs, QgsProject.instance().crs())
        # else:
        mousePosGeom = QgsGeometry(mousePosGeom)
        self.geometryHandler.reprojectFeature(mousePosGeom, rasterCrs, self.canvas.currentLayer().crs())
        mousePos = mousePosGeom.asMultiPoint()[0] if mousePosGeom.isMultipart() else mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify( mousePos, QgsRaster.IdentifyFormatValue )
        if i.isValid():
            value = list(i.results().values())[0]
            if value:
                value = int(value) if self.decimals == 0 else round(value, self.decimals)
            return value
        else:
            return None
    
    def getPixelValueFromPointDict(self, pointDict, rasterLayer):
        """
        pointDict = {'pointId':QgsGeometry}

        returns {'pointId': value}
        """
        return {key : self.getPixelValueFromPoint(value, rasterLayer, fromCanvas=False) for key, value in pointDict.items()} #no python3 eh items()
