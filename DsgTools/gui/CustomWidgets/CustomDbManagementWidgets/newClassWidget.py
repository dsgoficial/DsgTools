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
from builtins import range
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.addAttributeWidget import AddAttributeWidget
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'newClassWidget.ui'))

class NewClassWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
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
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)
    
    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        populates ui from  uiParameterJsonDict with the following keys:
        {
            'schemaComboBox': --text of selected item on schemaComboBox --
            'categoryLineEdit': --text of categoryLineEdit --
            'classNameLineEdit' : --text of classNameLineEdit --
            'geomComboBoxIdx' : --index of selected item on schemaComboBox --
            'attrWidgetList' : [--list of uiParameterJsonDict from each attributeWidget--]
        }
        """
        if uiParameterJsonDict:
            idx = self.schemaComboBox.findText(uiParameterJsonDict['schemaComboBox'], flags = Qt.MatchExactly)
            self.schemaComboBox.setCurrentIndex(idx)
            self.categoryLineEdit.setText(uiParameterJsonDict['categoryLineEdit'])
            self.classNameLineEdit.setText(uiParameterJsonDict['classNameLineEdit'])
            self.geomComboBox.setCurrentIndex(int(uiParameterJsonDict['geomComboBoxIdx']))
            for attr in uiParameterJsonDict['attrWidgetList']:
                self.addCellWidget(uiParameterJsonDict=attr)
    
    def populateSchemaCombo(self):
        self.schemaComboBox.clear()
        schemaList = self.abstractDb.getGeometricSchemaList()
        for schema in schemaList:
            if schema not in ['views', 'validation']:
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
    
    @pyqtSlot(bool, name='on_addAttributePushButton_clicked')
    def addCellWidget(self, uiParameterJsonDict = None):
        index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(index)
        newAttribute = AddAttributeWidget(self.abstractDb, uiParameterJsonDict = uiParameterJsonDict)
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
        #TODO: validate attributes
        return True

    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.categoryLineEdit.text() == '':
            invalidatedReason += self.tr('Class must have a category.\n')
        if self.classNameLineEdit.text() == '':
            invalidatedReason += self.tr('Class must have a name.\n')
        if self.geomComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('Class must have a geometric primitive.\n')
        #TODO: validate attributes
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
            newAttrJson = widget.getJSONTag()
            if isinstance(newAttrJson,list):
                for i in newAttrJson:
                    attrList.append(i)
            else:
                attrList.append(newAttrJson)
        return [self.jsonBuilder.buildClassElement(schema,name,attrList)]

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'schemaComboBox': --text of selected item on schemaComboBox --
            'categoryLineEdit': --text of categoryLineEdit --
            'classNameLineEdit' : --text of classNameLineEdit --
            'geomComboBoxIdx' : --index of selected item on schemaComboBox --
            'attrWidgetList' : [--list of uiParameterJsonDict from each attributeWidget--]
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict['schemaComboBox'] = self.schemaComboBox.currentText()
        uiParameterJsonDict['categoryLineEdit'] = self.categoryLineEdit.text()
        uiParameterJsonDict['classNameLineEdit'] = self.classNameLineEdit.text()
        uiParameterJsonDict['geomComboBoxIdx'] = self.geomComboBox.currentIndex()
        uiParameterJsonDict['attrWidgetList'] = []
        widgetList = self.getChildWidgetList()
        for widget in widgetList:
            uiParameterJsonDict['attrWidgetList'].append(widget.getUiParameterJsonDict())
        return uiParameterJsonDict

            