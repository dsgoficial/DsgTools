# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
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

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'networkDirectioningWidget.ui'))

class NetworkDirectioningWidget(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)
    def __init__(self, parent = None):
        """Constructor."""
        super(NetworkDirectioningWidget, self).__init__(parent)
        self.networkLayer = None
        self.referenceLayer = None
        self.selectedLayers = []
        self.setupUi(self)
    
    def setTitle(self, title):
        self.networkDirectioningWidget.setTitle(title)
    
    @pyqtSlot(int)
    def on_networkComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            if self.referenceLayer and self.unifiedList:
                self.networkDirectioningWidget.addItems([self.referenceLayer], unique=False)
                self.referenceLayer = None
            self.customSelectorWidget.setEnabled(False)
        else:
            if self.referenceLayer and self.unifiedList:
                addItem = [self.referenceLayer]
                self.networkDirectioningWidget.addItems(addItem, unique=False)
            self.customSelectorWidget.setEnabled(True)
            self.referenceLayer = self.referenceComboBox.currentText()
            if self.unifiedList:
                self.networkDirectioningWidget.removeItem(self.referenceLayer)

    @pyqtSlot(int)
    def on_referenceComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            if self.referenceLayer and self.unifiedList:
                self.networkDirectioningWidget.addItems([self.referenceLayer], unique=False)
                self.referenceLayer = None
            self.networkDirectioningWidget.setEnabled(False)
        else:
            if self.referenceLayer and self.unifiedList:
                addItem = [self.referenceLayer]
                self.networkDirectioningWidget.addItems(addItem, unique=False)
            self.networkDirectioningWidget.setEnabled(True)
            self.referenceLayer = self.referenceComboBox.currentText()
            if self.unifiedList:
                self.networkDirectioningWidget.removeItem(self.referenceLayer)
    
    def setInitialState(self, referenceList, originalList, unique=False):
        """
        Sets the initial state
        """
        self.originalList = originalList
        self.networkDirectioningWidget.addItems(originalList)
        self.networkComboBox.addItem(self.tr('Select a layer'))
        self.referenceComboBox.addItem(self.tr('Select a layer'))        
        originalList.sort()
        if len(referenceList) == 0:
            self.unifiedList = True
            self.referenceComboBox.addItems(originalList)
        else:
            self.unifiedList = False
            self.referenceComboBox.addItems(referenceList)
    
    def getParameters(self):
        """
        Gets parameters
        """
        return self.networkLayer, self.referenceLayer, self.networkDirectioningWidget.toLs