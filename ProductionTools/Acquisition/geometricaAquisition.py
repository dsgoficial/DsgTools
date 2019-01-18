# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL, Qt, QSettings
from qgis.gui import QgsMapTool, QgsRubberBand, QgsAttributeDialog, QgsMapToolAdvancedDigitizing, QgsAttributeForm
from qgis.utils import iface
from qgis.core import QgsPoint, QgsFeature, QgsGeometry, QGis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsEditFormConfig
from qgis.gui import QgsMapMouseEvent
import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence, QCursor, QPixmap, QColor
from PyQt4.QtCore import QSettings
from distanceToolTip import DistanceToolTip
import math

class GeometricaAcquisition(QgsMapToolAdvancedDigitizing):
    def __init__(self, canvas, iface, action):
        super(GeometricaAcquisition, self).__init__(canvas, None)
        self.iface=iface        
        self.canvas = canvas
        self.rubberBand = None
        self.snapCursorRubberBand = None
        self.initVariable()
        self.setAction(action)        
        self.minSegmentDistance = self.getMinSegmentDistance()
        self.distanceToolTip = DistanceToolTip(self.iface, self.minSegmentDistance)


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

    def getParametersFromConfig(self):
        #Método para obter as configurações da tool do QSettings
        #Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        parameters = {
            u'minSegmentDistance' : settings.value('minSegmentDistance'),
        }
        settings.endGroup()
        return parameters

    def getMinSegmentDistance(self):
        parameters = self.getParametersFromConfig()
        return int(parameters[u'minSegmentDistance'])

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
            self.canvas.unsetMapTool(self)

   
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
                geom = QgsGeometry.fromPolygon([self.geometry])
                self.qntPoint -= 1
                self.rubberBand.setToGeometry(geom, None)      
    
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(True)
            self.rubberBand = None
            self.rubberBand = self.createRubberBand()
        self.qntPoint = 0
        self.geometry = []
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None

    def completePolygon(self,geom, p4):                
        if (len(geom)>=2) and (len(geom) % 2 == 0):
            p1      = geom[1]
            p2      = geom[0]
            p3      = geom[-1]
            pf = self.lineIntersection(p1, p2, p3, p4)
            new_geom = QgsGeometry.fromPolygon([self.geometry+[p4, pf]])                            
        else:
            new_geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(p4.x(), p4.y())]])            
            pf = p4            
        return new_geom, pf
            
    def lineIntersection(self, p1, p2, p3, p4):    
        p3Projected = p4       
        if((p1.y() == p2.y()) or (p3.x()==p4.x())):                                     
            y = p3Projected.y()
            x = p2.x() 
            return QgsPoint(x,y)
        if((p1.x() == p2.x()) or (p3.y() == p4.y())):    
            y = p2.y()
            x = p3Projected.x() 
            return QgsPoint(x,y)
        else:        
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


    def distanceBetweenLinesTest(self, geom, p):             
        teste_answer = True
        for i in range(len(geom)-1):
            p1 = geom[i]
            p2 = geom[i+1]   
            projected_point = self.projectPoint(p1,p2,p)
            distance = self.distanceToolTip.calculateDistance(projected_point,p2)            
            if distance > self.minSegmentDistance:
                continue
            else:
                teste_answer = False
                break
        return teste_answer

    def projectPoint(self, p1, p2, p3):        
        #reta P1 P2
        try:
            # p1 e p2 na vertical
            if (p1.x() == p2.x()):
                x = p3.x()
                y = p2.y()
            # p1 e p2 na horizontal
            elif (p1.y()== p2.y()):
                x = p2.x()
                y = p3.y()
            else:
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
        geomType = self.iface.activeLayer().geometryType()
        if geomType == QGis.Polygon:
            rubberBand = QgsRubberBand(self.canvas, True)
            rubberBand.setFillColor(QColor(255, 0, 0, 40))
        elif geomType == QGis.Line:
            rubberBand = QgsRubberBand(self.canvas, False)
        rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        return rubberBand
    
    def getSnapRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, geometryType = QGis.Point)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        rubberBand.setIcon(QgsRubberBand.ICON_X)
        return rubberBand        

    def setAllowedStyleSnapRubberBand(self):
        self.rubberBand.setLineStyle(Qt.PenStyle(Qt.SolidLine))
        self.rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        self.rubberBand.setFillColor(QColor(255, 0, 0, 40))

    def setAvoidStyleSnapRubberBand(self):
        self.rubberBand.setLineStyle(Qt.PenStyle(Qt.DashDotLine))
        self.rubberBand.setBorderColor(QColor(255, 255, 0, 200))
        self.rubberBand.setFillColor(QColor(255, 0, 0, 40))

    def createGeometry(self, geom):
        geom = self.reprojectRubberBand(geom)
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
            form.setMode(QgsAttributeForm.AddFeatureMode)
            formSuppress = layer.editFormConfig().suppress()
            if formSuppress == QgsEditFormConfig.SuppressDefault:
                if self.getSuppressOptions(): #this is calculated every time because user can switch options while using tool
                    layer.addFeature(feature, True)
                else:
                    if not form.dialog().exec_():
                        feature.setAttributes(form.feature().attributes())
            elif formSuppress == QgsEditFormConfig.SuppressOff:
                if not form.dialog().exec_():
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
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        lyrType = self.iface.activeLayer().geometryType()
        # Transforming the points
        if lyrType == QGis.Line:
            geomList = geom.asPolyline()
        elif lyrType == QGis.Polygon:
            geomList = geom.asPolygon()
        newGeom = []
        for j in xrange(len(geomList)):
            if lyrType == QGis.Line:
                newGeom.append(coordinateTransformer.transform(geomList[j]))
            elif lyrType == QGis.Polygon:
                line = geomList[j]
                for i in xrange(len(line)):
                    point = line[i]
                    newGeom.append(coordinateTransformer.transform(point))
        if lyrType == QGis.Line:
            return QgsGeometry.fromPolyline(newGeom + [newGeom[0]])
        elif lyrType == QGis.Polygon:
            return QgsGeometry.fromPolygon([newGeom])                   
