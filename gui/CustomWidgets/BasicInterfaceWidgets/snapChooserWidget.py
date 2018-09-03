# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os, json
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'snapChooserWidget.ui'))

class SnapChooserWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, layerList, parameterDict = {}, parent = None):
        """Constructor."""
        super(SnapChooserWidget, self).__init__(parent = parent)
        self.setupUi(self)
        self.layerList = layerList
        self.layerList.sort()
        self.layerComboBox.addItem(self.tr('Select a layer'))
        self.layerComboBox.addItems(self.layerList)
        self.validKeys = ['layerName', 'snap']
        self.snapDoubleSpinBox.setDecimals(20)
        self.snapDoubleSpinBox.setMaximum(1000000)
        self.snapDoubleSpinBox.setMinimum(0.00000000000000001)
        if parameterDict != {}:
            self.populateInterface(parameterDict)
    
    def refresh(self, blackList):
        currentText = self.layerComboBox.currentText()
        refreshList = [i for i in self.layerList if i not in blackList]
        if currentText not in refreshList and self.layerComboBox.currentIndex() > 0:
            refreshList.append(currentText)
        refreshList.sort()
        self.layerComboBox.clear()
        self.layerComboBox.addItem(self.tr('Select a layer'))
        self.layerComboBox.addItems(refreshList)
        idx = self.layerComboBox.findText(currentText, flags = Qt.MatchExactly)
        self.layerComboBox.setCurrentIndex(idx)
    
    def getSelectedItem(self):
        if self.layerComboBox.currentIndex() > 0:
            return self.layerComboBox.currentText()
        else:
            return None
    
    def clearAll(self):
        """
        Clears all widget information
        """
        self.layerComboBox.clear()
        self.snapDoubleSpinBox.setValue(1.0)
    
    def getParameterDict(self):
        """
        Components:
        parameterDict = {'layerName':--name of the layer--,
                         'snap': --snap value--}
        """
        if not self.validate():
            raise Exception(self.invalidatedReason())
        parameterDict = dict()
        parameterDict['layerName'] = self.layerComboBox.currentText()
        parameterDict['snap'] = self.snapDoubleSpinBox.value()
        return parameterDict

    def populateInterface(self, parameterDict):
        """
        Populates interface with parameters from parameterDict.
        """
        if parameterDict:
            if not self.validateJson(parameterDict):
                raise Exception(self.tr('Invalid Snap Chooser Widget json config!'))
            #set layer combo
            idx = self.layerComboBox.findText(parameterDict['layerName'], flags = Qt.MatchExactly)
            self.layerComboBox.setCurrentIndex(idx)
            #set snap double spin box
            self.snapDoubleSpinBox.setValue(parameterDict['snap'])
            
    
    def validateJson(self, inputJson):
        """
        Validates input json
        """
        inputKeys = list(inputJson.keys())
        inputKeys.sort()
        if self.validKeys != inputKeys:
            return False
        else:
            return True

    def validate(self):
        """
        Validates fields. Returns True if all information are filled correctly.
        """
        if self.layerComboBox.currentIndex() < 1:
            return False
        if self.snapDoubleSpinBox.value() <= 0:
            return False
        return True
    
    def invalidatedReason(self):
        """
        Error reason
        """
        msg = ''
        if self.layerComboBox.currentIndex() < 1:
            msg += self.tr('Invalid layer!\n')
        if self.snapDoubleSpinBox.value() <= 0:
            msg += self.tr('Invalid snap value!\n')
        return msg