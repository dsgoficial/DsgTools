# -*- coding: utf-8 -*-
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL, Qt
from qgis.gui import QgsMapTool, QgsRubberBand, QgsAttributeDialog
from qgis.utils import iface
from qgis.core import QgsPoint, QgsFeature
import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence, QCursor, QPixmap, QColor
from PyQt4.QtCore import QSettings

class GeometricaAcquisition(QgsMapTool):
    def __init__(self, canvas, iface, action):
        super(GeometricaAcquisition, self).__init__(canvas)
        self.iface=iface        
        self.canvas = canvas
        self.rubberBand = None
        self.initVariable()
        self.setAction(action)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
                
    def canvasPressEvent(self, e):
        pass
    
    def deactivate(self):
        self.canvas.setMapTool(self)
        if self.toolAction:
            self.toolAction.setChecked(False)
    
    def activate(self):
        if self.toolAction:
            self.toolAction.setChecked(True)
        self.free = False
        self.cur = QCursor(QPixmap(["18 13 4 1",
                                    "           c None",
                                    "#          c #FF0000",
                                    ".          c #FF0000",
                                    "+          c #1210f3",
                                    "    +++++++++    ", 
                                    "   +++++++++++   ",
                                    "  ++    #    ++  ",
                                    " ++    .#.    ++ ",
                                    "++    ..#..    ++",
                                    "++......#......++",
                                    "++#############++", 
                                    "++......#......++",
                                    "++    ..#..    ++",
                                    " ++    .#.    ++",
                                    "  ++    #    ++  ",
                                    "   +++++++++++   ",
                                    "    +++++++++    ",]))
        self.canvas.setCursor(self.cur)
   
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.initVariable()
        if event.key() == Qt.Key_Control:
            self.free = False
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.free = True
        if event.key() == Qt.Key_Delete:
            if self.geometry:
                self.geometry.pop()
                geom = QgsGeometry.fromPolygon([self.geometry])
                self.qntPoint -= 1
                self.rubberBand.setToGeometry(geom, None)      
    
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(True)
            self.rubberBand = None
        self.qntPoint = 0
        if self.geometry:
            self.geometry = []
    
    def lineIntersection(self, p1, p2, p3, p4):        
        m1 = (p1.y() - p2.y())/(p1.x() - p2.x())
        a1 = p2.y() + p2.x()/m1
        m2 = (p3.y() - p4.y())/(p3.x() - p4.x())
        #Reta perpendicular P3 P4 que passa por P4
        a2 = p4.y() + p4.x()/m2
        if abs(m1 - m2) > 0.01:
            #intersecao
            x = (a2 - a1)/(1/m2 - 1/m1) 
            y = -x/m1 + a1
            return QgsPoint(x,y)
        return False
    
    def projectPoint(self, p1, p2, p3):        
        #reta P1 P2
        try:
            a = (p2.y()-p1.y())/(p2.x()-p1.x())
            #reta perpendicular a P1P2 que passa por P2
            a2 = -1/a
            b2 =  p2.y() - a2*p2.x()
            #reta paralela a P1P2 que passa por P3
            b3 = p3.y() - a*p3.x()
            #intersecao entre retas
            x = (b3 - b2)/(a2 - a)
            y = a*x + b3
        except:
            return None

        return QgsPoint(x, y)
    
    def getRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, True)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        return rubberBand
    
    def createGeometry(self, geom):
        if geom :
            layer = self.canvas.currentLayer() 
            feature = QgsFeature()
            fields = layer.pendingFields()
            feature.setGeometry(geom)
            feature.initAttributes(fields.count())            
            provider = layer.dataProvider()              
            for i in range(fields.count()):
                feature.setAttribute(i, provider.defaultValue(i))                
            form = QgsAttributeDialog(layer, feature, False)
            form.setIsAddDialog(True)
            if not form.dialog().exec_():
                ok = False
            else:
                ok = True
            if ok:
                feature.setAttributes(form.feature().attributes())
                layer.endEditCommand()
                self.initVariable()    
            else:
                self.initVariable()    
 
