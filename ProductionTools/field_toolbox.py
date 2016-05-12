# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry, QgsProject, QgsLayerTreeLayer

#DsgTools imports
from DsgTools.ProductionTools.field_setup import FieldSetup
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_toolbox.ui'))

class FieldToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
    
    @pyqtSlot(bool)
    def on_setupButton_clicked(self):
        dlg = FieldSetup()
        dlg.exec_()
        
        self.reclassificationDict = dlg.makeReclassificationDict()
        self.createButtons(self.reclassificationDict)
        
    def createWidget(self, formLayout):
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtGui.QFrame.Shape(0))  # no frame
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(scrollArea)
        return scrollArea
        
    def createButtons(self, reclassificationDict):
        self.tabWidget.clear()
        
        for category in reclassificationDict.keys():
            if category == 'version':
                continue
            formLayout = QtGui.QFormLayout()
            scrollArea = self.createWidget(formLayout)
            self.tabWidget.addTab(scrollArea, category)
            for edgvClass in reclassificationDict[category].keys():
                for button in reclassificationDict[category][edgvClass].keys():
                    pushButton = QtGui.QPushButton(button)
                    pushButton.clicked.connect(self.reclassify)
                    formLayout.addRow(pushButton)
                    
    @pyqtSlot()
    def reclassify(self):
        #checking for current layer
        currLayer = self.iface.activeLayer()
        if not currLayer:
            return
        
        if currLayer.type() != QgsMapLayer.VectorLayer:
            return

        #button that sent the signal
        button = self.sender().text()
        #edgvClass found in the dictionary
        edgvClass = self.findReclassificationClass(button)
        #reclassification layer name
        reclassificationClass = '_'.join(edgvClass.split('_')[1::])
            
        #searching the QgsVectorLayer to perform the reclassification
        root = QgsProject.instance().layerTreeRoot()
        reclassificationLayer = self.searchLayer(root, reclassificationClass)

        #iterating over selected features
        for feature in currLayer.selectedFeatures():
            geom = feature.geometry()
            
    
    def findReclassificationClass(self, button):
        for category in self.reclassificationDict.keys():
            if category == 'version':
                continue
            for edgvClass in self.reclassificationDict[category].keys():
                for buttonName in self.reclassificationDict[category][edgvClass].keys():
                    if button == buttonName:
                        #returning the desired edgvClass
                        return edgvClass
        return ''
                    
    def searchLayer(self, group, name):
        for child in group.children():
            if isinstance(child, QgsLayerTreeLayer) and child.layerName() == name:
                #QgsVectorLayer found, return it
                return child.layer()
            else:
                self.searchLayer(child, name)