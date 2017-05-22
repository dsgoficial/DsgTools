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
from PyQt4.QtGui import QMessageBox, QSpinBox
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject, Qt
from PyQt4 import QtGui, uic, QtCore
from PyQt4.Qt import QWidget, QObject

from qgis.core import QgsMapLayer, QGis, QgsVectorLayer
from qgis.gui import QgsMessageBar

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'inspectFeatures.ui'))

class InspectFeatures(QWidget,FORM_CLASS):
    idxChanged = pyqtSignal(int)
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(InspectFeatures, self).__init__(parent)
        self.setupUi(self)
        self.splitter.hide()
        self.iface = iface
        self.iface.currentLayerChanged.connect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.connect(self.enableScale)
        if not self.iface.activeLayer() and self.activeLayerCheckBox.isChecked():
            self.enableTool(False)
        self.iface.currentLayerChanged.connect(self.enableTool)
        self.mMapLayerComboBox.layerChanged.connect(self.enableTool)
        self.mScaleWidget.setScaleString('1:40000')
        self.mScaleWidget.setEnabled(False)
        self.enableScale()
        self.canvas = self.iface.mapCanvas()
        self.allLayers={}
        self.idxChanged.connect(self.setNewId)
        self.setToolTip('')
    
    def getIterateLayer(self):
        if self.activeLayerCheckBox.isChecked():
            return self.iface.activeLayer()
        else:
            return self.mMapLayerComboBox.currentLayer()
    
    @pyqtSlot(int)
    def on_activeLayerCheckBox_stateChanged(self, state):   
        if state == Qt.Checked:
            self.mMapLayerComboBox.setEnabled(False)
        else:
            self.mMapLayerComboBox.setEnabled(True)

    def enableTool(self, enabled = True):
        from qgis.core import QgsVectorLayer
        if enabled == None or not isinstance(enabled, QgsVectorLayer):
            enabled = False
        else:
            enabled = True
        self.backInspectButton.setEnabled(enabled)
        self.nextInspectButton.setEnabled(enabled)
        self.idSpinBox.setEnabled(enabled)
        self.onlySelectedRadioButton.setEnabled(enabled)
        
    def enableScale(self):
        """
        The scale combo should only be enabled for point layers
        """
        currentLayer = self.getIterateLayer()
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
    
    @pyqtSlot(int, name = 'on_idSpinBox_valueChanged')
    def setNewId(self, newId):
        if not isinstance(self.sender(), QSpinBox):
            self.idSpinBox.setValue(newId)
        else:
            currentLayer = self.getIterateLayer()
            lyrName = currentLayer.name()

            oldIndex = self.allLayers[lyrName]
            if oldIndex == 0:
                return
            featIdList = self.getFeatIdList(currentLayer)
            oldId = featIdList[oldIndex]
            zoom = self.mScaleWidget.scale()
            if oldId == newId:
                self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=QgsMessageBar.WARNING, duration=2)
                return
            try:
                index = featIdList.index(newId)
                self.allLayers[lyrName] = index
                self.makeZoom(zoom, currentLayer, newId)
            except:
                self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=QgsMessageBar.WARNING, duration=2)
                self.idSpinBox.setValue(oldId)
                self.makeZoom(zoom, currentLayer, oldId)




    def getFeatIdList(self, currentLayer):
        #getting all features ids
        if self.onlySelectedRadioButton.isChecked():
            featIdList = currentLayer.selectedFeaturesIds()
        else:
            featIdList = currentLayer.allFeatureIds()
        #sort is faster than sorted (but sort is just available for lists)
        featIdList.sort()
        return featIdList
    
    def iterateFeature(self, method):
        """
        Iterates over the features selecting and zooming to the desired one
        method: method used to determine the desired feature index
        """
        currentLayer = self.getIterateLayer()
        lyrName = currentLayer.name()
        
        zoom = self.mScaleWidget.scale()
        
        featIdList = self.getFeatIdList(currentLayer)
        
        if currentLayer and len(featIdList) > 0:
            #checking if this is the first time for this layer (currentLayer)
            if lyrName not in self.allLayers.keys():
                self.allLayers[lyrName] = 0

            #getting the current index
            index = self.allLayers[lyrName]

            #getting the current feature id
            id = featIdList[index]

            #getting max and min ids
            #this was made because the list is already sorted, there's no need to calculate max and min
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
            self.idxChanged.emit(id)

            self.makeZoom(zoom, currentLayer, id)
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
    
    def zoomToLayer(self, layer):
        box = layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def zoomFeature(self, zoom, idDict = {}):
        """
        Zooms to current layer selected features according to a specific zoom
        zoom: zoom to be applied
        """
        currentLayer = self.getIterateLayer()
        if idDict == {}:
            self.zoomToLayer(currentLayer)
        else:
            id = idDict['id']
            lyr = idDict['lyr']
            selectIdList = lyr.selectedFeaturesIds()
            lyr.removeSelection()
            lyr.setSelectedFeatures([id])
            self.zoomToLayer(layer = lyr)
            lyr.setSelectedFeatures(selectIdList)

        if self.getIterateLayer().geometryType() == QGis.Point:
            self.iface.mapCanvas().zoomScale(float(1/zoom))
        
    @pyqtSlot(bool)
    def on_inspectPushButton_toggled(self, toggled):
        """
        Shows/Hides the tool bar
        """
        if toggled:
            self.splitter.show()
            self.setToolTip(self.tr('Select a vector layer to enable tool'))
        else:
            self.splitter.hide()

    def setValues(self, featIdList, currentLayer):
        lyrName = currentLayer.name()
        featIdList.sort()
        self.allLayers[lyrName] = 0

        maxIndex = len(featIdList) - 1
        minIndex = 0
        
        self.idSpinBox.setMaximum(featIdList[maxIndex])
        self.idSpinBox.setMinimum(featIdList[minIndex])

        #getting the new feature id
        id = featIdList[0]

        #adjustin the spin box value
        self.idxChanged.emit(id)
        #self.idSpinBox.setValue(id)

        zoom = self.mScaleWidget.scale()
        self.makeZoom(zoom, currentLayer, id)

    def makeZoom(self, zoom, currentLayer, id):
        #selecting and zooming to the feature
        if not self.onlySelectedRadioButton.isChecked():
            self.selectLayer(id, currentLayer)
            self.zoomFeature(zoom)
        else:
            self.zoomFeature(zoom, idDict = {'id':id, 'lyr':currentLayer})        

    @pyqtSlot(bool)
    def on_onlySelectedRadioButton_toggled(self, toggled):
        currentLayer = self.getIterateLayer()
        if toggled:
            featIdList = currentLayer.selectedFeaturesIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(False)
        else:
            featIdList = currentLayer.allFeatureIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(True)
            