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
        email                : borba@dsg.eb.mil.br
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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attributeRuleWidget.ui'))

class AttributeRuleWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, layerDict, interfaceDict = {}, parent = None):
        """Constructor."""
        super(AttributeRuleWidget, self).__init__(parent = )
        self.setupUi(self)
        self.layerDict = layerDict
        self.layerComboBox.addItem(self.tr('Select a layer'))
        self.layerComboBox.addItems(layerDict.keys())
        self.attributeComboBox.setEnabled(False)
        self.mFieldExpressionWidget.setEnabled(False)
        self.descriptionLineEdit.setEnabled(False)
    
    def clearAll(self):
        self.attributeComboBox.clear()
        self.mFieldExpressionWidget.setRow(-1)
        self.descriptionLineEdit.clear()
    
    @pyqtSlot(int, name = 'on_layerComboBox_currentIndexChanged')
    def filterAttributeCombo(self, idx):
        self.clearAll()
        if idx > 0:
            key = self.layerComboBox.currentText()
            self.attributeComboBox.addItem(self.tr('Select attribute'))
            self.attributeComboBox.addItems(self.layerDict[key])


