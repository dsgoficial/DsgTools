# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-10-01
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from collections import OrderedDict

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customReferenceAndLayersParameterSelector.ui'))

class CustomReferenceAndLayersParameterSelector(QtGui.QWidget, FORM_CLASS):

    def __init__(self, parent = None):
        """Constructor."""
        super(CustomReferenceAndLayersParameterSelector, self).__init__(parent)
        self.referenceLayerItem = None
        self.selectedLayersItems = []
        self.setupUi(self)
    
    def setTitle(self, title):
        self.customSelectorWidget.setTitle(title)
    
    @pyqtSlot(int)
    def on_referenceComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            if self.referenceLayer and self.unifiedList:
                self.customSelectorWidget.addItems([self.referenceLayer])
                self.referenceLayer = None
            self.customSelectorWidget.setEnabled(False)
        else:
            if self.referenceLayer and self.unifiedList:
                addItem = [self.referenceLayer]
                self.customSelectorWidget.addItems(addItem)
            self.customSelectorWidget.setEnabled(True)
            self.referenceLayer = self.referenceComboBox.currentText()
            if self.unifiedList:
                self.customSelectorWidget.removeItem(self.referenceLayer)
    
    def setInitialState(self, referenceDictList, layersDictList, unique=True, excludent = True):
        """
        Sets the initial state
        referenceDict: {'cat,lyrName,geom,geomType,tableType':{'tableSchema':tableSchema, 'tableName':tableName, 'geom':geom, 'geomType':geomType, 'tableType':tableType, 'lyrName':lyrName, 'cat':cat}}
        referenceDictList: interface ready dict like 
        {
            self.tr('Category'):cat, 
            self.tr('Layer Name'):lyrName, 
            self.tr('Geometry\nColumn'):geom, 
            self.tr('Geometry\nType'):geomType, 
            self.tr('Layer\nType'):tableType
        }
        """
        self.excludent = excludent
        self.referenceDictList = referenceDictList
        self.layersDictList = layersDictList

        #makes referenceTextDict
        self.referenceTextDict = OrderedDict()
        self.referenceTextDict[self.tr('Select a layer')] = None
        sortedRefKeys = self.referenceDictList.keys()
        sortedRefKeys.sort()
        for key in sortedRefKeys:
            cat, lyrName, geom, geomType, tableType = key.split(',')
            textItem = """"{0}.{1} ({2}, {3}, {4})""".format(cat, lyrName, geom, geomType, tableType)
            self.referenceTextDict[textItem] = self.referenceDictList[key]
        #makes referenceTextDict
        self.layersTextDict = OrderedDict()
        self.layersTextDict[self.tr('Select a layer')] = None
        sortedLyrsKeys = self.layersDictList.keys()
        sortedLyrsKeys.sort()
        for key in sortedLyrsKeys:
            cat, lyrName, geom, geomType, tableType = key.split(',')
            textItem = """"{0}.{1} ({2}, {3}, {4})""".format(cat, lyrName, geom, geomType, tableType)
            self.layersTextDict[textItem] = self.layersDictList[key]
        if len(self.referenceTextDict.keys()) == 1:
            self.unifiedList = True
            self.referenceComboBox.addItems(self.layersDictList.keys())
        else:
            self.unifiedList = False
            self.referenceComboBox.addItems(self.referenceTextDict.keys())
    
    def getParameters(self):
        """
        Gets parameters
        """
        return self.referenceLayer, self.customSelectorWidget.toLs