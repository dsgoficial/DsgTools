# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-01
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'newAttributeWidget.ui'))

class NewAttributeWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.jsonBuilder = CustomJSONBuilder()
        self.populateSchemaCombo()
    
    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def populateSchemaCombo(self):
        self.schemaComboBox.clear()
        schemaList = self.abstractDb.getGeometricSchemaList()
        for schema in schemaList:
            if schema <> 'views':
                self.schemaComboBox.addItem(schema)
    
    @pyqtSlot(int)
    def on_schemaComboBox_currentIndexChanged(self, idx):
        schema = self.schemaComboBox.currentText()
        self.tableComboBox.setEnabled(True)
        self.tableComboBox.clear()
        tableList = self.abstractDb.getGeometricTableListFromSchema(schema)
        for table in tableList:
            self.tableComboBox.addItem(table)
    
    @pyqtSlot(int)
    def on_allTablesCheckBox_stateChanged(self,idx):
        if idx == 2:
            self.tableComboBox.clear()
            self.tableComboBox.setEnabled(False)
            self.schemaComboBox.clear()
            self.schemaComboBox.setEnabled(False)
        else:
            self.schemaComboBox.setEnabled(True)
            self.populateSchemaCombo()
    
    def validate(self):
        if not self.allTablesCheckBox.isChecked():
            if self.tableComboBox.currentText() == '':
                return False
            if self.schemaComboBox.currentText() == '':
                return False
        return self.addAttributeWidget.validate()

    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.tableComboBox.currentText() == '':
            invalidatedReason += self.tr('A table name must be chosen.\n')
        if self.schemaComboBox.currentText() == '':
            invalidatedReason += self.tr('A schema must be chosen.\n')
        invalidatedReason += self.addAttributeWidget.validateDiagnosis()
        return invalidatedReason
    
    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.tr('Error in attribute ')+ self.title + ' : ' + self.validateDiagnosis())
        schema = self.schemaComboBox.currentText()
        tableName = self.tableComboBox.currentText()
        if not self.allTablesCheckBox.isChecked():
            attrList = [self.addAttributeWidget.getJSONTag()]
            return self.jsonBuilder.buildNewAttributeElement(schema, tableName, attrList)
        else:
            #TODO
            pass
            