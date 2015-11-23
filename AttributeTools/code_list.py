# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsField
from PyQt4.QtGui import QTableWidgetItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'code_list.ui'))

class CodeList(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        super(CodeList, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        self.iface.currentLayerChanged.connect(self.layerChanged)
        
        self.setState()
        
    def setState(self):
        self.comboBox.clear()
        self.currLayer = self.iface.activeLayer()
        if self.currLayer:
            for field in self.currLayer.fields():
                valueDict, keys = self.getCodeListDict(field.name())
                if len(keys) > 0:
                    self.comboBox.addItem(field.name())
        self.comboBox.setCurrentIndex(0)
        
        self.loadCodeList()
        
    def getCodeListDict(self, field):
        fieldIndex = self.currLayer.fieldNameIndex(field)
        valueDict = self.currLayer.editorWidgetV2Config(fieldIndex) 
        keys = [value for value in valueDict.keys() if not (value == 'UseHtml' or value == 'IsMultiline')]
        return  valueDict, keys 
        
    @pyqtSlot(QgsMapLayer)
    def layerChanged(self, layer):
        self.setState()
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        self.loadCodeList()        
        
    def loadCodeList(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Value'), self.tr('Code')])
        
        field = self.comboBox.currentText()
        valueDict, keys = self.getCodeListDict(field)
        
        self.tableWidget.setRowCount(len(keys))
        
        for row, value in enumerate(keys):
            code = valueDict[value]
            valueItem = QTableWidgetItem(str(value).decode('utf-8'))  
            codeItem = QTableWidgetItem(str(code))
            self.tableWidget.setItem(row, 0, valueItem)
            self.tableWidget.setItem(row, 1, codeItem)
        