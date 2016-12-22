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
from DsgTools.CustomWidgets.CustomDbManagementWidgets.addAttributeWidget import AddAttributeWidget
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'newClassWidget.ui'))

class NewClassWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.geomUiDict = {self.tr('Point'):{'sufix':'p','type':'MULTIPOINT([epsg])'}, self.tr('Line'):{'sufix':'l','type':'MULTILINESTRING([epsg])'}, self.tr('Area'):{'sufix':'a','type':'MULTIPOLYGON([epsg])'}} 
        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
        regex = QtCore.QRegExp('[a-z][a-z\_]*')
        validator = QtGui.QRegExpValidator(regex, self.classNameLineEdit)
        self.classNameLineEdit.setValidator(validator)
        regex2 = QtCore.QRegExp('[a-z]*')
        validator2 = QtGui.QRegExpValidator(regex2, self.categoryLineEdit)
        self.categoryLineEdit.setValidator(validator2)
        self.abstractDb = abstractDb
        self.populateSchemaCombo()
        self.jsonBuilder = CustomJSONBuilder()
    
    def populateSchemaCombo(self):
        self.schemaComboBox.clear()
        schemaList = self.abstractDb.getGeometricSchemaList()
        for schema in schemaList:
            self.schemaComboBox.addItem(schema)
    
    @pyqtSlot()
    def on_classNameLineEdit_editingFinished(self):
        text = self.classNameLineEdit.text()
        while text[-1] == '_':
            self.classNameLineEdit.setText(text[0:-1])
            text = text[0:-1]
    
    @pyqtSlot(str)
    def on_classNameLineEdit_textEdited(self, newText):
        if len(newText) > 1:
            if newText[-1] == '_' and newText[-2] == '_':
                    self.classNameLineEdit.setText(newText[0:-1])
    
    @pyqtSlot(bool)
    def on_addAttributePushButton_clicked(self):
        index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(index)
        newAttribute = AddAttributeWidget(self.abstractDb)
        self.tableWidget.setCellWidget(index,0,newAttribute)
    
    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selected = self.tableWidget.selectedIndexes()
        rowList = [i.row() for i in selected]
        rowList.sort(reverse=True)
        for row in rowList:
            self.tableWidget.removeRow(row)
    
    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def getChildWidgetList(self):
        childWidgetList = []
        for i in range(self.tableWidget.rowCount()):
            childWidgetList.append(self.tableWidget.cellWidget(i,0))
        return childWidgetList
    
    def validate(self):
        if self.categoryLineEdit.text() == '':
            return False
        if self.classNameLineEdit.text() == '':
            return False
        if self.geomComboBox.currentIndex() == 0:
            return False 
        return True

    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.categoryLineEdit.text() == '':
            invalidatedReason += self.tr('Class must have a category.\n')
        if self.classNameLineEdit.text() == '':
            invalidatedReason += self.tr('Class must have a name.\n')
        if self.geomComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('Class must have a geometric primitive.\n')
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.tr('Error in class ')+ self.title + ' : ' + self.validateDiagnosis())
        schema = self.schemaComboBox.currentText()
        name = '_'.join([ self.categoryLineEdit.text(), self.classNameLineEdit.text(), self.geomUiDict[self.geomComboBox.currentText()]['sufix'] ])
        widgetList = self.getChildWidgetList()
        attrList = []
        #create pk attr
        pkItem = self.jsonBuilder.buildAttributeElement('id', 'serial', True, False)
        attrList.append(pkItem)
        #create geom attr
        geomItem = self.jsonBuilder.buildAttributeElement('geom', self.geomUiDict[self.geomComboBox.currentText()]['type'], False, False)
        attrList.append(geomItem)
        for widget in widgetList:
            attrList.append(widget.getJSONTag())
        return self.jsonBuilder.buildClassElement(schema,name,attrList)