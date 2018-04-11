# -*- coding: utf-8 -*-
from builtins import range
from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, Qt
from qgis.gui import QgsMapTool, QgsRubberBand, QgsAttributeDialog, QgsMapToolAdvancedDigitizing, QgsAttributeForm
from qgis.utils import iface
from qgis.core import QgsPointXY, QgsFeature, QgsGeometry, Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsEditFormConfig, QgsWkbTypes, QgsProject
from qgis.gui import QgsMapMouseEvent
import math
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QShortcut
from qgis.PyQt.QtGui import QKeySequence, QCursor, QPixmap, QColor
from qgis.PyQt.QtCore import QSettings

class GeometricaAcquisition(QgsMapToolAdvancedDigitizing):
    def __init__(self, canvas, iface, action):
        super(GeometricaAcquisition, self).__init__(canvas, None)
        self.iface=iface        
        self.canvas = canvas
        self.rubberBand = None
        self.snapCursorRubberBand = None
        self.initVariable()
        self.setAction(action)

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

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
                
    def canvasPressEvent(self, e):
        pass
    
    def activate(self):
        if self.toolAction:
            self.toolAction.setChecked(True)
        self.free = False
        self.cur = QCursor(QPixmap(["18 13 4 1",
                                    "           c None",
                                    "#          c #FF0000",
                                    ".          c #FF0000",
                                    "+          c #1210f3",
                                    "                 ", 
                                    "   +++++++++++   ",
                                    "  +     #     +  ",
                                    " +      #      + ",
                                    "+       #       +",
                                    "+       #       +",
                                    "++#############++", 
                                    "+       #       +",
                                    "+       #       +",
                                    " +      #      +",
                                    "  +     #     +  ",
                                    "   +++++++++++   ",
                                    "                 ",]))
        self.canvas.setCursor(self.cur)

    def deactivate(self):
        self.initVariable()
        if self.toolAction:
            self.toolAction.setChecked(False)
        if self is not None:
            QgsMapTool.deactivate(self)

   
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.initVariable()
        if event.key() == Qt.Key_Control:
            self.free = False
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.free = True
        if event.key() == Qt.Key_Backspace:
            if self.geometry:
                self.geometry.pop()
                geom = QgsGeometry.fromPolygonXY([self.geometry])
                self.qntPoint -= 1
                self.rubberBand.setToGeometry(geom, None)      
    
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(geometryType = self.iface.activeLayer().geometryType())
            self.rubberBand = None
        self.qntPoint = 0
        self.geometry = []
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QgsWkbTypes.PointGeometry)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
    
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
            return QgsPointXY(x,y)
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

        return QgsPointXY(x, y)
    
    def getRubberBand(self):
        geomType = self.iface.activeLayer().geometryType()
        if geomType == QgsWkbTypes.PolygonGeometry:
            rubberBand = QgsRubberBand(self.canvas, True)
            rubberBand.setFillColor(QColor(255, 0, 0, 40))
        elif geomType == QgsWkbTypes.LineGeometry:
            rubberBand = QgsRubberBand(self.canvas, False)
        rubberBand.setSecondaryStrokeColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        return rubberBand
    
    def getSnapRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, geometryType = QgsWkbTypes.PointGeometry)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setSecondaryStrokeColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        rubberBand.setIcon(QgsRubberBand.ICON_X)
        return rubberBand        
    
    def createGeometry(self, geom):
        geom = self.reprojectRubberBand(geom)
        if geom :
            layer = self.canvas.currentLayer()
            feature = QgsFeature()
            fields = layer.fields()
            feature.setGeometry(geom)
            feature.initAttributes(fields.count())            
            provider = layer.dataProvider()              
            for i in range(fields.count()):
                defaultClauseCandidate = provider.defaultValueClause(i)
                if defaultClauseCandidate:
                    feature.setAttribute(i, defaultClauseCandidate)                
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
            layer.endEditCommand()
            self.canvas.refresh()
            self.initVariable()   

    def createSnapCursor(self, point):
        self.snapCursorRubberBand = self.getSnapRubberBand()
        self.snapCursorRubberBand.addPoint(point) 
 
    def reprojectRubberBand(self, geom):
        """
        Reprojects the geometry
        geom: QgsGeometry
        """
        # Defining the crs from src and destiny
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        #getting srid from something like 'EPSG:31983'
        layer = self.canvas.currentLayer()
        srid = layer.crs().authid()
        crsDest = QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
        lyrType = self.iface.activeLayer().geometryType()
        # Transforming the points
        if lyrType == QgsWkbTypes.LineGeometry:
            geomList = geom.asPolyline()
        elif lyrType == QgsWkbTypes.PolygonGeometry:
            geomList = geom.asPolygon()
        newGeom = []
        for j in range(len(geomList)):
            if lyrType == QgsWkbTypes.LineGeometry:
                newGeom.append(coordinateTransformer.transform(geomList[j]))
            elif lyrType == QgsWkbTypes.PolygonGeometry:
                line = geomList[j]
                for i in range(len(line)):
                    point = line[i]
                    newGeom.append(coordinateTransformer.transform(point))
        if lyrType == QgsWkbTypes.LineGeometry:
            return QgsGeometry.fromPolylineXY(newGeom + [newGeom[0]])
        elif lyrType == QgsWkbTypes.PolygonGeometry:
            return QgsGeometry.fromPolygonXY([newGeom])                   