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
from collections import defaultdict
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceUri, QgsMessageLog,\
                      QgsVectorLayer, Qgis, QgsProject
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
        # self.currLayer = None
        # self.refreshClassesDictList() # creates and populates self.classesFieldDict
        self.setInitialState()
    
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

    def readClassFieldMap(self):
        """
        Gets all layers with value maps.
        :return: (dict) a map from layer to list of fields with a value map. 
        """
        classFieldMap = defaultdict(dict)
        for layer in self.iface.mapCanvas().layers():
            if not isinstance(layer, QgsVectorLayer):
                continue
            for field in layer.fields():
                fieldConfig = field.editorWidgetSetup().config()
                fieldName = field.name()
                if 'map' not in fieldConfig or fieldName in ('UseHtml', 'IsMultiline'):
                    continue
                if isinstance(fieldConfig['map'], list):
                    for map_ in fieldConfig['map']:
                        if fieldName not in classFieldMap[layer.name()]:
                            classFieldMap[layer.name()][fieldName] = map_
                        else:
                            classFieldMap[layer.name()][fieldName].update(map_)
                else:
                    classFieldMap[layer.name()][fieldName] = fieldConfig['map']
        return classFieldMap

    def updateClassFieldMap(self):
        """
        Updates current registry of layers and their value map.
        """
        self._classFieldMap = self.readClassFieldMap()

    def availableLayers(self):
        """
        Gets all layers that have attributes with a value map associated to it.
        :return: (list-of-str) sorted list of layers.
        """
        return sorted(self._classFieldMap.keys())

    def resetClasses(self):
        """
        Sets current class-fields map data to combo boxes.
        """
        self.classComboBox.clear()
        self.classComboBox.addItem(self.tr('Select a layer...'))
        self.classComboBox.addItems(self.availableLayers())

    @pyqtSlot(int, name='on_classComboBox_currentIndexChanged')
    def resetFields(self):
        """
        Resets current available fields
        """
        self.comboBox.clear()
        self.comboBox.addItem(self.tr('Select a field...'))
        self.comboBox.addItems(self.availableFields())

    def layerByName(self, layerName):
        """
        Gets vector layer from current selection.
        :param layerName: (str) layer name to have its layer object retrieved.
        :return: (QgsVectorLayer)
        """
        l = QgsProject.instance().mapLayersByName(layerName)
        return l[0] if l else QgsVectorLayer()

    def currentLayerName(self):
        """
        Gets current selected layer name.
        :return: (str) current layer's name.
        """
        return self.classComboBox.currentText().split(': ')[-1]

    def availableFieldsFromLayerName(self, layerName):
        """
        Gets all available fields that have value maps.
        :param layerName: (str) layer to have its layers checked.
        :return: (list-of-str) list of field names available. 
        """
        return [] if layerName not in self._classFieldMap else list(self._classFieldMap[layerName].keys())

    def availableFields(self):
        """
        Gets all available fields that have value maps from current layer selection.
        :return: (list-of-str) list of field names available. 
        """
        return self.availableFieldsFromLayerName(self.currentLayerName())

    def currentLayer(self):
        """
        Gets vector layer from current selection.
        :return: (QgsVectorLayer)
        """
        return self.layerByName(self.currentLayerName())

    def fieldMapFromFieldName(self, fieldName, layerName):
        """
        Gets a field map from an attribute name.
        :param layerName: (str) layer name to have its fielf map checked.
        :param layerName: (str) field name to have its map retrieved.
        :return: (dict) field map.
        """
        if layerName in self._classFieldMap and fieldName in self._classFieldMap[layerName]:
            return self._classFieldMap[layerName][fieldName]
        return dict()

    def currentField(self):
        """
        Gets current field selection.
        :return: (str) field name.
        """
        ct = self.comboBox.currentText()
        return '' if ct == self.tr('Select a field...') else ct

    def currentFieldMap(self):
        """
        Gets current selection's field map.
        :return: (dict) field map
        """
        return self.fieldMapFromFieldName(self.currentField(), self.currentLayerName())

    @pyqtSlot(bool, name='on_refreshButton_clicked')
    def setInitialState(self):
        """
        Sets interface components to its initial state.
        """
        self.updateClassFieldMap()
        self.resetClasses()
        self.resetFields()

    def getEdgvDomains(self):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        :param fieldConfig: (dict) field config.
        :return: (dict) value map.
        """
        ret = dict()
        currentLayer = self.currentLayer()
        if currentLayer.isValid():
            try:
                uri = QgsDataSourceUri(self.currentLayer().dataProvider().dataSourceUri())
                if uri.host() == '':
                    db = QSqlDatabase('QSQLITE')
                    db.setDatabaseName(uri.database())
                    sql = 'select code, code_name from dominios_{tablename} order by code'.format(tablename=self.currentField())
                else:
                    db = QSqlDatabase('QPSQL')
                    db.setHostName(uri.host())
                    db.setPort(int(uri.port()))
                    db.setDatabaseName(uri.database())
                    db.setUserName(uri.username())
                    db.setPassword(uri.password())
                    sql = 'select code, code_name from dominios.{tablename} order by code'.format(tablename=self.currentField())    
                if not db.open():
                    db.close()
                    return ret
                query = QSqlQuery(sql, db)
                if not query.isActive():
                    # QMessageBox.critical(self.iface.mainWindow(), self.tr("Error!"), self.tr("Problem obtaining domain values: ")+query.lastError().text())
                    return ret       
                while query.next():
                    code = str(query.value(0))
                    code_name = query.value(1)
                    ret[code_name] = code      
                db.close()
            except:
                pass
        return ret

    @pyqtSlot(int, name='on_comboBox_currentIndexChanged')
    def populateFieldsTable(self):
        """
        Populates field map to codelist table.
        """
        # always prefer EDGV domain tables, if available
        fieldMap = self.getEdgvDomains() or self.currentFieldMap()
        self.tableWidget.setRowCount(len(fieldMap))
        for row, (code, value) in enumerate(fieldMap.items()):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(value))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(code))
        self.tableWidget.sortItems(1)
