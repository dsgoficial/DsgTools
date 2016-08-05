# -*- coding: utf-8 -*-
"""
/***************************************************************************
InspectFeatures
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
import os
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject
from PyQt4 import QtGui, uic, QtCore
from PyQt4.Qt import QWidget, QObject

from qgis.core import QgsMapLayer

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'inspectFeatures.ui'))


class InspectFeatures(QWidget,FORM_CLASS): 
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(InspectFeatures, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.iface.currentLayerChanged.connect(self.enableScale)
        self.mScaleWidget.setScaleString('1:40000')
        self.mScaleWidget.setEnabled(False)
        self.canvas = self.iface.mapCanvas()
        self.AllLayers={}
        
    def enableScale(self):
        currentLayer = self.iface.activeLayer()
        if QgsMapLayer is not None and currentLayer:
                if currentLayer.type() == QgsMapLayer.VectorLayer:
                    if currentLayer.geometryType() == 0:
                        self.mScaleWidget.setEnabled(True)
                    else:
                        self.mScaleWidget.setEnabled(False)
 
    @pyqtSlot(bool)
    def on_nextInspectButton_clicked(self):
        currentLayer = self.iface.activeLayer()
        lyrName = currentLayer.name()
        id = self.idSpinBox.value() 
        zoom = self.mScaleWidget.scale()
        if (currentLayer) and (currentLayer.allFeatureIds() <> []) :
            featIdList = sorted(currentLayer.allFeatureIds())
            maxId = max(featIdList)
            minId = min(featIdList)
            self.idSpinBox.setMaximum(maxId)
            self.idSpinBox.setMinimum(minId)
            initialIndex=self.AllLayers.get(lyrName)
            index = self.testIndexFoward(initialIndex, id, featIdList)
            self.AllLayers[lyrName]=index
            self.idSpinBox.setValue(index)
            self.selectLayer(index, currentLayer, featIdList)        
            self.zoomFeature(zoom)        
        else:
            self.errorMessage()
    
    def testIndexFoward(self, Index, id, AllIds):
        if Index == None:
            if id == '':
                Index = 0
            else:
                Index = int(id)
        elif Index >= (len(AllIds)-1):
            Index=0 
        else:
            Index+=1
        return Index
    
    def testIndexBackwards(self, Index, id, AllIds):
        if Index == None:
            if id == '':
                Index = (len(AllIds)-1)
            else:
                Index = int(id)
        elif Index <= 0:
            Index=(len(AllIds)-1)
        else:
            Index-=1 
        return Index
            
    @pyqtSlot(bool)
    def on_backInspectButton_clicked(self):
        currentLayer = self.iface.activeLayer()
        lyrName = currentLayer.name()
        id = self.idSpinBox.value() 
        zoom = self.mScaleWidget.scale()
        if (currentLayer) and (currentLayer.allFeatureIds() <> []) :
            featIdList = sorted(currentLayer.allFeatureIds())
            maxId = max(featIdList)
            minId = min(featIdList)
            self.idSpinBox.setMaximum(maxId)
            self.idSpinBox.setMinimum(minId)
            initialIndex = self.AllLayers.get(lyrName)
            index = self.testIndexBackwards(initialIndex, id, featIdList)
            self.AllLayers[lyrName]=index          
            self.idSpinBox.setValue(index)
            self.selectLayer(index, currentLayer,featIdList)
            self.zoomFeature(zoom)
        else:
            self.errorMessage()
            
    def errorMessage(self):
        QMessageBox.warning(self.iface.mainWindow(), self.tr(u"ERRO:"), self.tr(u"<font color=red>There are no features in current layer:<br></font><font color=blue>Add features and try again!</font>"), QMessageBox.Close)


    def removeSelections(self, currentLayer):
        try:
            currentLayer.removeSelection()
        except:
            pass
            
    def selectLayer(self, index, currentLayer, featIdList):
        self.removeSelections(currentLayer)      
        self.iface.activeLayer().select(featIdList[index])
        

    def zoomFeature(self, zoom):
        self.iface.actionZoomToSelected().trigger()
        if self.canvas.currentLayer().geometryType() == 0 :
            self.iface.mapCanvas().zoomScale(float(1/zoom))
        
        