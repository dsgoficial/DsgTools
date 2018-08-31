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
    os.path.dirname(__file__), 'attributeRuleWidget.ui'))

class AttributeRuleWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, layerDict, parameterDict = {}, parent = None):
        """Constructor."""
        super(AttributeRuleWidget, self).__init__(parent = parent)
        self.setupUi(self)
        self.layerDict = layerDict
        self.layerComboBox.addItem(self.tr('Select a layer'))
        layerNames = list(layerDict.keys())
        layerNames.sort()
        self.layerComboBox.addItems(layerNames)
        self.setComponentsEnabled(False)
        self.validKeys = ['attributeName', 'attributeRule', 'description', 'layerName']
        if parameterDict != {}:
            self.populateInterface(parameterDict)
    
    def clearAll(self):
        """
        Clears all widget information
        """
        self.attributeComboBox.clear()
        self.mFieldExpressionWidget.setRow(-1)
        self.descriptionLineEdit.clear()
    
    def setComponentsEnabled(self, enabled):
        """
        Sets all components enabled.
        """
        self.attributeComboBox.setEnabled(enabled)
        self.mFieldExpressionWidget.setEnabled(enabled)
        self.descriptionLineEdit.setEnabled(enabled)
    
    @pyqtSlot(int, name = 'on_layerComboBox_currentIndexChanged')
    def filterAttributeCombo(self, idx):
        self.clearAll()
        if idx > 0:
            key = self.layerComboBox.currentText()
            self.attributeComboBox.addItem(self.tr('Select attribute'))
            #get attribute names
            attrNames = [i.name() for i in self.layerDict[key].fields()]
            #add items to combo box
            self.attributeComboBox.addItems(attrNames)
            #after everything is ok, set components enabled
            self.setComponentsEnabled(True)
            #set layer on mFieldExpressionWidget
            self.mFieldExpressionWidget.setLayer(self.layerDict[key])
        else:
            self.setComponentsEnabled(False)
    
    def getParameterDict(self):
        """
        Components:
        parameterDict = {'layerName':--name of the layer--,
                         'attributeName': --name of the attribute,
                         'attributeRule': --expression--,
                         'description': --description--}
        """
        if not self.validate():
            raise Exception(self.invalidatedReason())
        parameterDict = dict()
        parameterDict['layerName'] = self.layerComboBox.currentText()
        parameterDict['attributeName'] = self.attributeComboBox.currentText()
        parameterDict['attributeRule'] = self.mFieldExpressionWidget.currentText()
        parameterDict['description'] = self.descriptionLineEdit.text()
        return parameterDict

    def populateInterface(self, parameterDict):
        """
        Populates interface with parameters from parameterDict.
        """
        if parameterDict:
            if not self.validateJson(parameterDict):
                raise Exception(self.tr('Invalid Attribute Rule Widget json config!'))
            #set layer combo
            idx = self.layerComboBox.findText(parameterDict['layerName'], flags = Qt.MatchExactly)
            self.layerComboBox.setCurrentIndex(idx)
            #set attr combo
            idx = self.attributeComboBox.findText(parameterDict['attributeName'], flags = Qt.MatchExactly)
            self.attributeComboBox.setCurrentIndex(idx)
            #set rule
            self.mFieldExpressionWidget.setExpression(parameterDict['attributeRule'])
            #set description
            if parameterDict['description'] != '':
                self.descriptionLineEdit.setText(parameterDict['description'])
    
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
        if self.attributeComboBox.currentIndex() < 1:
            return False
        if self.mFieldExpressionWidget.currentText() == '' or \
            not self.mFieldExpressionWidget.isValidExpression(self.mFieldExpressionWidget.currentText()):
            return False
        return True
    
    def invalidatedReason(self):
        """
        Error reason
        """
        msg = ''
        if self.layerComboBox.currentIndex() < 1:
            msg += self.tr('Invalid layer!\n')
        if self.attributeComboBox.currentIndex() < 1:
            msg += self.tr('Invalid attribute!\n')
        if self.mFieldExpressionWidget.currentText() == '' or \
            not self.mFieldExpressionWidget.isValidExpression(self.mFieldExpressionWidget.currentText()):
            msg += self.tr('Invalid rule!\n')
        return msg