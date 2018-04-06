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
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customReferenceAndLayersParameterSelector.ui'))

class CustomReferenceAndLayersParameterSelector(QtWidgets.QWidget, FORM_CLASS):

    def __init__(self, parent = None):
        """Constructor."""
        super(CustomReferenceAndLayersParameterSelector, self).__init__(parent)
        self.referenceLayerKey = None
        self.selectedLayersItems = []
        self.setupUi(self)
    
    def setTitle(self, title):
        self.customTableSelectorWidget.setTitle(title)
    
    @pyqtSlot(int)
    def on_referenceComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            if self.referenceLayerKey and self.unifiedList:
                self.customTableSelectorWidget.addItemsToWidget([self.layersTextDict[self.referenceLayerKey]], unique = True)
                self.referenceLayerKey = None
            self.customTableSelectorWidget.setEnabled(False)
        else:
            if self.referenceLayerKey:
                if self.unifiedList:
                    self.customTableSelectorWidget.addItemsToWidget([self.layersTextDict[self.referenceLayerKey]], unique = True)
                else:
                    self.customTableSelectorWidget.addItemsToWidget([self.referenceTextDict[self.referenceLayerKey]], unique = True)
            self.customTableSelectorWidget.setEnabled(True)
            self.referenceLayerKey = self.referenceComboBox.currentText()
            if self.unifiedList:
                self.customTableSelectorWidget.removeItemsFromWidget([self.layersTextDict[self.referenceLayerKey]])
            else:
                self.customTableSelectorWidget.removeItemsFromWidget([self.referenceTextDict[self.referenceLayerKey]])
    
    def setInitialState(self, inputOrderedDict, unique=True):
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
        self.referenceDictList = inputOrderedDict['referenceDictList']
        self.layersDictList = inputOrderedDict['layersDictList']
 
        #makes referenceTextDict
        self.referenceTextDict = OrderedDict()
        self.referenceTextDict[self.tr('Select a layer')] = None
        sortedRefKeys = list(self.referenceDictList.keys())
        sortedRefKeys.sort()
        for key in sortedRefKeys:
            cat, lyrName, geom, geomType, tableType = key.split(',')
            textItem = """{0}.{1} ({2}, {3}, {4})""".format(cat, lyrName, geom, geomType, tableType)
            self.referenceTextDict[textItem] = self.referenceDictList[key]
        #makes referenceTextDict
        self.layersTextDict = OrderedDict()
        self.layersTextDict[self.tr('Select a layer')] = None
        sortedLyrsKeys = list(self.layersDictList.keys())
        sortedLyrsKeys.sort()
        for key in sortedLyrsKeys:
            cat, lyrName, geom, geomType, tableType = key.split(',')
            textItem = """{0}.{1} ({2}, {3}, {4})""".format(cat, lyrName, geom, geomType, tableType)
            self.layersTextDict[textItem] = self.layersDictList[key]
        if len(list(self.referenceTextDict.keys())) == 1:
            self.unifiedList = True
            self.referenceComboBox.addItems(list(self.layersTextDict.keys())) #uses all layers to populate ref combo
        else:
            self.unifiedList = False
            self.referenceComboBox.addItems(list(self.referenceTextDict.keys())) #uses only some layers to populate ref combo
        self.customTableSelectorWidget.setInitialState(list(self.layersDictList.values()))
    
    def getParameters(self):
        """
        Gets parameters
        """
        if self.unifiedList:
            refItem = self.layersTextDict[self.referenceLayerKey]
            originalRefDict = self.layersDictList
        else:
            refItem = self.referenceTextDict[self.referenceLayerKey]
            originalRefDict = self.referenceDictList
        try:
            referenceKey = [k for (k,v) in originalRefDict.items() if v == refItem][0]
        except:
            referenceKey = None
        return referenceKey, self.customTableSelectorWidget.getSelectedNodes()