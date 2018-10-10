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
from builtins import str
from builtins import map
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceUri, QgsMessageLog, QgsVectorLayer
from qgis.PyQt.QtWidgets import QTableWidgetItem, QMessageBox
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'code_list.ui'))

class CodeList(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        super(CodeList, self).__init__()
        self.setupUi(self)
        self.iface = iface
        self.currLayer = None
        self.refreshClassesDictList() # creates and populates self.classesFieldDict
        self.setState()
    
    def addTool(self, manager, callback, parentMenu, iconBasePath, parentStackButton):
        icon_path = iconBasePath + 'codelist.png'
        text = self.tr('View Code List Codes and Values')
        action = manager.add_action(
            icon_path,
            text=text,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            parentMenu = parentMenu,
            parentButton = parentStackButton
            )
        
    @pyqtSlot()
    def setState(self):
        """
        Sets the code list viewer initial state.
        Populates the field comboBox.
        """
        self.comboBox.clear()
        # in case reload is used or index changed and comboBox is empty, for some reason
        try:
            # gets the layer to be "translated"
            for lyr in list(self.classesFieldDict.keys()):
                if lyr.name() == self.classComboBox.currentText().split(": ")[1]:
                    self.currLayer = lyr
                    break
        except: # leaves self.currLayer set as None
            pass
        if not self.currLayer:
            return        
        try:
            if QgsMapLayer is not None:
                if self.currLayer.type() != QgsMapLayer.VectorLayer:
                    return        
                for field in self.classesFieldDict[self.currLayer]:
                    # iterates over every field that has a value map on database
                    valueDict, keys = self.getCodeListDict(field.name())
                    if len(keys) > 0:
                        self.comboBox.addItem(field.name())
                self.comboBox.setCurrentIndex(0)            
                self.loadCodeList()
        except:
            pass
        
    def getCodeListDict(self, field):
        """
        Gets the code list dictionary
        """
        fieldList = self.currLayer.fields()
        fieldIndex = fieldList.lookupField(field)
        if fieldIndex == -1:
            return dict(), list()
        valueDict = fieldList[fieldIndex].editorWidgetSetup().config()
        if 'map' in valueDict:
            valueDict = valueDict['map']
        keys = [value for value in valueDict if not (value == 'UseHtml' or value == 'IsMultiline')]
        return valueDict, keys
    
    def makeValueRelationDict(self, valueDict):
        """
        Gets the value relation dictionary. This is necessary for multi valued attributes.
        """
        ret = dict()

        codes = valueDict['FilterExpression'].replace('code in (', '').replace(')','').split(',')
        in_clause = ','.join(map(str, codes))
        keyColumn = valueDict['Key']
        valueColumn = valueDict['Value']
        table = valueDict['Layer'][:-17]#removing the date-time characters
        
        uri = QgsDataSourceUri(self.currLayer.dataProvider().dataSourceUri())
        if uri.host() == '':
            db = QSqlDatabase('QSQLITE')
            db.setDatabaseName(uri.database())
            sql = 'select code, code_name from dominios_%s where code in (%s)' % (table, in_clause)
        else:
            db = QSqlDatabase('QPSQL')
            db.setHostName(uri.host())
            db.setPort(int(uri.port()))
            db.setDatabaseName(uri.database())
            db.setUserName(uri.username())
            db.setPassword(uri.password())
            sql = 'select code, code_name from dominios.%s where code in (%s)' % (table, in_clause)
        
        if not db.open():
            db.close()
            return ret

        query = QSqlQuery(sql, db)
        if not query.isActive():
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Error!"), self.tr("Problem obtaining domain values: ")+query.lastError().text())
            return ret
        
        while next(query):
            code = str(query.value(0))
            code_name = query.value(1)
            ret[code_name] = code
            
        db.close()
                
        return ret
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        """
        Slot that updates the code lists when the current active layers changes.
        """
        try:
            for lyr in list(self.classesFieldDict.keys()):
                if lyr.name() == self.classComboBox.currentText().split(": ")[1]:
                    self.currLayer = lyr
            self.loadCodeList()   
        except:
            pass
        
    def loadCodeList(self):
        """
        Loads the current code lists viewer for the active layer
        """
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Value'), self.tr('Code')])
        
        field = self.comboBox.currentText()
        valueDict, keys = self.getCodeListDict(field)
        
        if 'FilterExpression' in keys:
            valueDict = self.makeValueRelationDict(valueDict)
            keys = list(valueDict.keys())
        elif 'Relation' in keys:
            return

        self.tableWidget.setRowCount(len(keys))
        row = 0
        for code, value in valueDict.items():
            valueItem = QTableWidgetItem(value)
            codeItem = QTableWidgetItem(code)
            self.tableWidget.setItem(row, 0, valueItem)
            self.tableWidget.setItem(row, 1, codeItem)
            row += 1
        self.tableWidget.sortItems(1)

    def refreshClassesDictList(self):        
        """
        Refreshs the list of classes having Value Map set.
        Populates the classComboBox.
        Returns the dict of classes and their attributes that have the value map set (classesFieldDict)
        """
        # checks if the selected class has a value map and fills the field combobox if necessary
        self.classComboBox.clear()
        try:
            self.classesFieldDict.clear()
        except:
            # this dict is composed by [ QgsLayer obj : [ 'Every attribute (QgsField obj) that has a value map of this specific layer' ] ]
            self.classesFieldDict = dict()
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                for field in layer.fields():
                    # only classes that have value maps may be enlisted on the feature
                    if field.editorWidgetSetup().type() in ['ValueMap', 'ValueRelation']:
                        if layer not in self.classesFieldDict:
                            self.classesFieldDict[layer] = []
                            # in case more tha a db is loaded and they have the same layer
                            # name for some class. 
                            uriString = layer.dataProvider().dataSourceUri()
                            if "'" in uriString:
                                splitToken = "'" 
                                idx = 1
                            elif "|" in uriString:
                                splitToken = "|"
                                idx = 1
                            else:
                                splitToken = ""
                                idx = 0
                            db_name = uriString.split(splitToken)[idx] if splitToken != "" else uriString
                            self.classComboBox.addItem("{0}: {1}".format(db_name, layer.name()))
                        if field not in self.classesFieldDict[layer]:
                            self.classesFieldDict[layer].append(field)
        self.classComboBox.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_classComboBox_currentIndexChanged(self):
        """
        Slot that updates the code lists when the selected layer changes.
        """
        # if index is changed, no need to reset dict, just updates field list and attr table...
        self.setState()
        self.loadCodeList()

    @pyqtSlot(bool)
    def on_refreshButton_clicked(self):
        """
         Refreshs the list of classes having Value Map set when refresh button is clicked.
        """
        try:
            self.refreshClassesDictList()
            self.setState()
            self.loadCodeList()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details. (Do the layers have Value Maps?)'))
            QgsMessageLog.logMessage(self.tr('Error loading classes to Code List Viewer: ')+':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
