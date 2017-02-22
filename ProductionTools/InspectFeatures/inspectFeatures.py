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

from qgis.core import QgsMapLayer, QGis

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'inspectFeatures.ui'))

class InspectFeatures(QWidget,FORM_CLASS): 
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(InspectFeatures, self).__init__(parent)
        self.setupUi(self)
        self.splitter.hide()
        self.iface = iface
        self.iface.currentLayerChanged.connect(self.enableScale)
        self.mScaleWidget.setScaleString('1:40000')
        self.mScaleWidget.setEnabled(False)
        self.canvas = self.iface.mapCanvas()
        self.allLayers={}
        
    def enableScale(self):
        """
        The scale combo should only be enabled for point layers
        """
        currentLayer = self.iface.activeLayer()
        if QgsMapLayer is not None and currentLayer:
                if currentLayer.type() == QgsMapLayer.VectorLayer:
                    if currentLayer.geometryType() == QGis.Point:
                        self.mScaleWidget.setEnabled(True)
                    else:
                        self.mScaleWidget.setEnabled(False)
 
    @pyqtSlot(bool)
    def on_nextInspectButton_clicked(self):
        """
        Inspects the next feature
        """
        method = getattr(self, 'testIndexFoward')
        self.iterateFeature(method)
    
    def testIndexFoward(self, index, maxIndex, minIndex):
        """
        Gets the next index
        """
        index += 1
        if index > maxIndex:
            index = minIndex
        return index
    
    def testIndexBackwards(self, index, maxIndex, minIndex):
        """
        gets the previous index
        """
        index -= 1
        if index < minIndex:
            index = maxIndex
        return index
            
    @pyqtSlot(bool)
    def on_backInspectButton_clicked(self):
        """
        Inspects the previous feature
        """
        method = getattr(self, 'testIndexBackwards')
        self.iterateFeature(method)
            
    def iterateFeature(self, method):
        """
        Iterates over the features selecting and zooming to the desired one
        method: method used to determine the desired feature index
        """
        currentLayer = self.iface.activeLayer()
        lyrName = currentLayer.name()
        
        zoom = self.mScaleWidget.scale()
        
        #getting all features ids
        featIdList = currentLayer.allFeatureIds()
        #sort is faster than sorted (but sort is just available for lists)
        featIdList.sort()
        
        if currentLayer and len(featIdList) > 0:
            #checking if this is the first time for this layer (currentLayer)
            if lyrName not in self.allLayers.keys():
                self.allLayers[lyrName] = 0

            #getting the current index
            index = self.allLayers[lyrName]

            #getting the current feature id
            id = featIdList[index]

            #getting max and min ids
            maxIndex = len(featIdList) - 1
            minIndex = 0
            
            self.idSpinBox.setMaximum(featIdList[maxIndex])
            self.idSpinBox.setMinimum(featIdList[minIndex])

            #getting the new index
            index = method(index, maxIndex, minIndex)

            self.allLayers[lyrName] = index

            #getting the new feature id
            id = featIdList[index]

            #adjustin the spin box value
            self.idSpinBox.setValue(id)

            #selecting and zooming to the feature
            self.selectLayer(id, currentLayer)
            self.zoomFeature(zoom)
        else:
            self.errorMessage()
            
    def errorMessage(self):
        """
        Shows am error message
        """
        QMessageBox.warning(self.iface.mainWindow(), self.tr(u"ERROR:"), self.tr(u"<font color=red>There are no features in the current layer:<br></font><font color=blue>Add features and try again!</font>"), QMessageBox.Close)

    def selectLayer(self, index, currentLayer):
        """
        Remove current layer feature selection
        currentLayer: layer that will have the feature selection removed
        """
        if currentLayer:
            currentLayer.removeSelection()
            currentLayer.select(index)

    def zoomFeature(self, zoom):
        """
        Zooms to current layer selected features according to a specific zoom
        zoom: zoom to be applied
        """
        self.iface.actionZoomToSelected().trigger()
        if self.canvas.currentLayer().geometryType() == QGis.Point:
            self.iface.mapCanvas().zoomScale(float(1/zoom))
        
    @pyqtSlot(bool)
    def on_inspectPushButton_toggled(self, toggled):
        """
        Shows/Hides the tool bar
        """
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()