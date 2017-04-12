# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence

class MultiLayerSelection(QgsMapTool):
	finished = QtCore.pyqtSignal(list)
	def __init__(self, canvas, iface):
		self.iface=iface        
		self.canvas = canvas
		self.free = False
		self.selecaoMulti=[]
		QgsMapTool.__init__(self, self.canvas)
		
	def getSelectionsLayers(self):
		self.selecaoVariada =  list(set( self.selecaoVariada ))
		return self.selecaoVariada
	
	def setSelectionsLayers(self, name):
		self.selecaoVariada.append(name)
	
	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Control:
		    self.free = False

	def keyPressEvent(self, event):
	    if event.key() == Qt.Key_Control:
	        self.free = True
	   
	def canvasPressEvent(self, e):
		if not self.free:
			self.removerSelecoes()
		layers = self.canvas.layers()	
		layer2 = QgsMapLayerRegistry.instance().mapLayers()	
		grupo={}
		for x in range(len(layer2)):
			grupo[layer2.keys()[x][:-17]]=layer2.get(layer2.keys()[x])    		
		p = self.toMapCoordinates(e.pos())
		w = self.canvas.mapUnitsPerPixel() * 10
		rect = QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
		for layer in layers:
			if (layer.type() == QgsMapLayer.RasterLayer) or (layer.name() == 'moldura'):
				continue
			else:
				lRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)			   
				layer.select(lRect, False)
				if (self.free) and (layer.selectedFeatureCount() >= 1):
					self.setSelectionsLayers(layer.name())
					self.iface.setActiveLayer(grupo.get(layer.name()))
					self.iface.activeLayer().startEditing()
				elif layer.selectedFeatureCount() == 1:
					self.setSelectionsLayers(layer.name())
					
				else:
					layer.removeSelection()					
		selectionsLayers = self.getSelectionsLayers()
		if not self.free:
			self.setOnlyOneSelection()
		self.finished.emit(selectionsLayers)
			
					
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
		self.iface.activeLayer().startEditing()
	                   
	def deactivate(self):
		if self is not None:
			QgsMapTool.deactivate(self)

	def activate(self):
		QgsMapTool.activate(self)
	
	def removerSelecoes(self):
		for i in range(len(self.iface.mapCanvas().layers())):
			try:
				self.iface.mapCanvas().layers()[i].removeSelection()
			except:
				pass
		self.selecaoVariada=[]
	
		






