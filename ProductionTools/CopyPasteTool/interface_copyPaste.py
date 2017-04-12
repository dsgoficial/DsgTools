# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog
from PyQt4.QtCore import pyqtSlot, QSettings, QObject
import psycopg2
from time import sleep
from PyQt4 import QtGui, uic, QtCore
import sys, os

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'interface_copyPaste.ui'), resource_suffix='')

class CopyPaste(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, layer, parent=None):
        super(CopyPaste, self).__init__(parent)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.setupUi(self)
        self.SelectedLayers = None
        self.layerInitial = {}
        self.setDataLayer(layer)
        self.addItems()
        
    def setDataLayer(self, layer):
        for index in self.iface.activeLayer().pendingAllAttributesList():
            if not (index == 0):
                field = self.iface.activeLayer().pendingFields()[index].name()
                value = self.iface.activeLayer().selectedFeatures()[0].attribute(field)
                self.layerInitial[field] =  value
        self.removeSelecoes()   
        
    def addItems(self):
        fields = sorted(self.layerInitial.keys())
        self.listField.addItems(fields)
        for i in range(self.listField.count()):
            self.listField.item(i).setCheckState(QtCore.Qt.Checked)
            
    def getFieldsToCopy(self):
        fieldsInital = []
        for i in range(self.listField.count()):
            if self.listField.item(i).checkState():
                fieldsInital.append(self.listField.item(i).text())
        return fieldsInital
    
    def getSelectedLayers(self):
        return self.SelectedLayers
    
    def setSelectedLayers(self, layers):
        self.SelectedLayers = layers
        
    def startCopyPaste(self):
        selectedLayers = self.getSelectedLayers()
        if selectedLayers:
            layers = QgsMapLayerRegistry.instance().mapLayers()    
            grupo={}
            for x in range(len(layers)):
                if layers.keys()[x][:-17] in selectedLayers:
                    grupo[layers.keys()[x][:-17]]=layers.get(layers.keys()[x]) 
            for layer in grupo:
                self.iface.setActiveLayer(grupo[layer])
                ids = self.iface.activeLayer().selectedFeaturesIds()
                self.attributeLayer(ids)
            self.removeSelecoes()
        
    def attributeLayer(self, ids):
        fields = self.getFieldsToCopy()
        for id in ids:
            for field in fields:
                idx = self.iface.activeLayer().fieldNameIndex(field)
                if idx >=0 :
                    self.iface.activeLayer().changeAttributeValue(id , idx, self.layerInitial[field])
        
    @pyqtSlot(bool)    
    def on_pasteButton_clicked(self):
        self.startCopyPaste()
        
    @pyqtSlot(bool)    
    def on_removeButton_clicked(self):
        for i in range(self.listField.count()):
            self.listField.item(i).setCheckState(QtCore.Qt.Unchecked)
    
    @pyqtSlot(bool)    
    def on_selectButton_clicked(self):
        for i in range(self.listField.count()):
            self.listField.item(i).setCheckState(QtCore.Qt.Checked)
                
    def removeSelecoes(self):
        for i in range(len(self.canvas.layers())):
            try:
                self.canvas.layers()[i].removeSelection()
            except:
                pass
            
    def closeEvent(self, e):
        self.canvas.unsetCursor()
        self.removeSelecoes()
            
