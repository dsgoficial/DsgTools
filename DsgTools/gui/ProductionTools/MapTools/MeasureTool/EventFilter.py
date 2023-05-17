# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2023-05-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


from qgis.PyQt.QtCore import QObject, QEvent, Qt, QCoreApplication, QPoint
from qgis.PyQt.QtGui import QMouseEvent
from PyQt5.QtWidgets import QToolTip

from qgis.core import QgsWkbTypes, QgsGeometry

import math


class EventFilter(QObject):
   
    def __init__(self, iface, pointList, enableAction):
        QObject.__init__(self)
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        self.pointList = pointList
        self.enableAction = enableAction
        self.active = False

    def close(self):
        pass

    def eventFilter(self, obj, event):
        if not event.spontaneous():
            return QObject.eventFilter(self, obj, event)

        if ( (  (event.type() == QEvent.MouseMove and event.button() != Qt.MidButton) or
                (event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton) or
                (event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton) )
                and self.active == True ):
            curPoint = self.iface.mapCanvas().getCoordinateTransform().toMapCoordinates( event.pos() )
            self.updateMeasure(curPoint)
            self.pointList.updateCurrentPoint(curPoint)
            modifiedEvent = QMouseEvent(event.type(), self.toPixels(curPoint), event.button(), event.buttons(), event.modifiers())
            QCoreApplication.sendEvent(obj, modifiedEvent)
                
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.pointList.newPoint()   
            return True

        elif event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
                self.pointList.removeLastPoint()
                return False
            return event.isAccepted()
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.RightButton:
            self.pointList.empty()
            QCoreApplication.sendEvent(obj,event)
            return True
        else:
            return QObject.eventFilter(self, obj, event)

    def updateMeasure(self, point): 
        previousPoint = self.pointList.previousPoint()
        dist, distAcum = None, None
        area = None
    
        if self.iface.mapCanvas().currentLayer().geometryType() == QgsWkbTypes.LineGeometry:
            if len(self.pointList)>1:
                dist = math.sqrt(point.sqrDist(previousPoint))
    
            line = QgsGeometry.fromPolylineXY(self.pointList)
            distAcum = line.length()
            
            if dist != None and self.enableAction.isChecked():
                    color = 'darkred'
                    color2 = 'yellow'
                    txt = "<p style='background-color:{color};color:{color2}'><b>Parcial: {distance} m</b><br/>".format(color=color, color2=color2, distance="%.3f" % dist)    
                    txt += "<b>Total: {distance} m</b></p>".format(distance="%.3f" % distAcum)
                    QToolTip.showText(self.mapCanvas.mapToGlobal(self.mapCanvas.mouseLastXY()), txt, self.mapCanvas)
            else:
                QToolTip.hideText()
                
        
        elif self.iface.mapCanvas().currentLayer().geometryType() == QgsWkbTypes.PolygonGeometry:
            # Restrição de distância
            tempPointList = []
            
            if len(self.pointList)>2:
                tempPointList = self.pointList[:]
                tempPointList.append(self.pointList[0])
                polygon = QgsGeometry.fromPolygonXY([tempPointList])
                area = polygon.area()

            if area != None and self.enableAction.isChecked():
                    color = 'darkred'
                    color2 = 'yellow'
                    txt = "<p style='background-color:{color};color:{color2}'><b>Área: {area}</b></p>".format(color=color, color2=color2, area="%.3f" % area)    
                    QToolTip.showText(self.mapCanvas.mapToGlobal(self.mapCanvas.mouseLastXY()), txt, self.mapCanvas)
            else:
                QToolTip.hideText()

    def toPixels(self, qgspoint):
        """
        Dado um ponto nas coordenadas do projeto, retorna um ponto nas coordenadas de tela (pixel)
        """
        try:
            p = self.iface.mapCanvas().getCoordinateTransform().transform( qgspoint )
            return QPoint( int(p.x()), int(p.y()) )
        except ValueError:
            return QPoint()


