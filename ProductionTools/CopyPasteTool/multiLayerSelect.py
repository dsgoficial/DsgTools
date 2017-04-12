# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence

class MultiLayerSelection(QgsMapTool):
    def __init__(self, canvas, iface):
        self.iface=iface        
        self.canvas = canvas
        self.selecaoMulti=[]
        self.initSelectedIds()
        QgsMapTool.__init__(self, self.canvas)
       
    def getSelectionsLayers(self):
        if self.selecaoVariada:
            self.selecaoVariada =  list(set( self.selecaoVariada ))
            return self.selecaoVariada
        else:
            return []
    
    def setSelectionsLayers(self, name):
        self.selecaoVariada.append(name)
        
    def initSelectedIds(self):
        self.ids={}
        for l in self.canvas.layers():
            self.ids[l.name()] = []
  
    def canvasPressEvent(self, e):
        if not (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier):
            self.removerSelecoes()
            self.initSelectedIds()
        else:
            self.setBkpLayersNames()
            self.setBkpIds()
            self.removerSelecoes(False)
        layers = self.canvas.layers()    
        layer2 = QgsMapLayerRegistry.instance().mapLayers()    
        self.grupo={}
        for x in range(len(layer2)):
            self.grupo[layer2.keys()[x][:-17]]=layer2.get(layer2.keys()[x])            
        p = self.toMapCoordinates(e.pos())
        w = self.canvas.mapUnitsPerPixel() * 10
        rect = QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
        for layer in layers:
            if (layer.type() == QgsMapLayer.RasterLayer) or ('moldura' in layer.name().lower()):
                continue
            else:
                lRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
                layer.select(lRect, False)
                if (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier) and (layer.selectedFeatureCount() >= 1):
                    self.setSelectionsLayers(layer.name())
                    self.iface.setActiveLayer(self.grupo.get(layer.name()))
                    self.iface.activeLayer().startEditing()
                elif layer.selectedFeatureCount() == 1:
                    self.setSelectionsLayers(layer.name())
                else:
                    layer.removeSelection()                    
        if not (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier):
            self.setOnlyOneSelection()
        else:
            for name in self.getSelectionsLayers():
                newIds = self.grupo[name].selectedFeaturesIds()
                for i in newIds:
                    if i in self.getBkpIds()[name]:
                        self.getBkpIds()[name].remove(i)
                    elif not(i in self.getBkpIds()[name]):
                        self.getBkpIds()[name].append(i)
            self.setBkpLayersNames(self.getBkpLayerNames())
            self.removerSelecoes(False)
            self.restoreAllLayerNames()
            self.selectLayers()                
                
    def restoreAllLayerNames(self):
        for name in self.getBkpLayerNames():
            self.setSelectionsLayers(name)
            
    def selectLayers(self):
        for name in self.getSelectionsLayers():
            for Id in self.getBkpIds()[name]:
                self.grupo[name].select(Id)                         
    
    def setBkpIds(self):
        self.initSelectedIds()
        for l in self.getSelectionsLayers():
            if not l in self.ids:
                self.ids[l] = []
            self.ids[l]+=self.grupo[l].selectedFeaturesIds()
            self.ids[l] = list(set(self.ids[l]))
                           
    def getBkpIds(self):
    	return self.ids
 
    def setBkpLayersNames(self, add=None):
        if add:
            self.layersName = self.getSelectionsLayers() + add
        else:
            self.layersName = self.getSelectionsLayers()
        
    def getBkpLayerNames(self):
        return self.layersName
                         
    def setOnlyOneSelection(self):
        selections = self.getSelectionsLayers()
        layers = QgsMapLayerRegistry.instance().mapLayers()    
        table = []
        for x in range(len(layers)):
            if layers.keys()[x][:-17] in selections:
                table.append([layers.get(layers.keys()[x]).geometryType(), layers.get(layers.keys()[x])])
        table.sort()
        geom = None
        for line in table:
            if line[0] == 0:
                geom = line[1]
                break
            elif line[0] == 1:
                geom = line[1]
                break
            else: 
                geom = line[1]
                break
        for line in table:
            if not (line[1] == geom):
                line[1].removeSelection()
        self.iface.setActiveLayer(geom)
        if self.iface.activeLayer():
            self.iface.activeLayer().startEditing()
                       
    def deactivate(self):
        self.ids = {}
        if self is not None:
            QgsMapTool.deactivate(self)

    def activate(self):
        QgsMapTool.activate(self)
    
    def removerSelecoes(self, all=True):
        if all:
            for i in range(len(self.iface.mapCanvas().layers())):
                try:
                    self.iface.mapCanvas().layers()[i].removeSelection()
                except:
                    pass
            self.selecaoVariada=[]
        else:
            for name in self.getBkpLayerNames():
                self.grupo[name].removeSelection()
            self.selecaoVariada=[]