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
from collections import defaultdict
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QTableWidgetItem, QDockWidget
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.core import QgsVectorLayer, QgsProject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'code_list.ui'))

class CodeList(QDockWidget, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        super(CodeList, self).__init__()
        self.setupUi(self)
        self.iface = iface
        self.setInitialState()

    def blockAllSignals(self, status):
        """
        Blocks (or unblocks) signals emitted from all GUI components.
        :param status: (bool) whether should be blocked
        """
        self.comboBox.blockSignals(status)
        self.classComboBox.blockSignals(status)
        self.refreshButton.blockSignals(status)

    def readClassFieldMap(self, preferEdgvMapping=True):
        """
        Gets all layers with value maps.
        :param preferEdgvMapping: (bool) whether edgv mapping should be preferred, if exists.
        :return: (dict) a map from layer to list of fields with a value map. 
        """
        classFieldMap = defaultdict(dict)
        for layer in self.iface.mapCanvas().layers():
            if not isinstance(layer, QgsVectorLayer):
                continue
            layername = layer.name()
            if preferEdgvMapping:
                fMap = self.getAllEdgvDomainsFromTableName(layername)
                if fMap:
                    classFieldMap[layername] = fMap
                    continue
            for field in layer.fields():
                fieldName = field.name()
                fieldConfig = field.editorWidgetSetup().config()
                if 'map' not in fieldConfig or fieldName in ('UseHtml', 'IsMultiline'):
                    continue
                if isinstance(fieldConfig['map'], list):
                    for map_ in fieldConfig['map']:
                        if fieldName not in classFieldMap[layername]:
                            classFieldMap[layername][fieldName] = map_
                        else:
                            classFieldMap[layername][fieldName].update(map_)
                else:
                    def sortingMethod(item):
                        try:
                            return int(item[1])
                        except:
                            return item[1]
                    classFieldMap[layername][fieldName] = {
                        k: v for k, v in sorted(
                            fieldConfig['map'].items(), key=sortingMethod
                        )
                    }
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
        layers = []
        for layer in self._classFieldMap.keys():
            uriString = self.layerByName(layer).dataProvider().dataSourceUri()
            if "|" in uriString:
                db_name = os.path.basename(uriString.split("|")[0])
            elif "'" in uriString:
                db_name = os.path.basename(uriString.split("'")[1])
            else:
                db_name = uriString
            layers.append("{db}: {layer}".format(db=db_name, layer=layer))
        layers.sort()
        return layers

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
        self.blockAllSignals(True)
        self.updateClassFieldMap()
        self.resetClasses()
        self.blockAllSignals(False)
        self.resetFields()

    def getAllEdgvDomainsFromTableName(self, table):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        It checks for all attributes found.
        :param table: (str) layer to be checked for its EDGV mapping.
        :param table: (QgsVectorLayer) overloaded method - layer to be checked for its EDGV mapping.
        :param field: (str) field to be checked.
        :return: (dict) value map for all attributes that have one.
        """
        ret = defaultdict(dict)
        currentLayer = table if isinstance(table, QgsVectorLayer) else self.layerByName(table)
        if currentLayer.isValid():
            try:
                uri = currentLayer.dataProvider().uri()
                if uri.host() == '':
                    db = QSqlDatabase('QSQLITE')
                    db.setDatabaseName(
                        uri.uri().split("|")[0].strip() if uri.uri().split("|")[0].strip().endswith(".gpkg") \
                            else uri.database()
                    )
                    sql = 'select code, code_name from dominios_{field} order by code'
                else:
                    db = QSqlDatabase('QPSQL')
                    db.setHostName(uri.host())
                    db.setPort(int(uri.port()))
                    db.setDatabaseName(uri.database())
                    db.setUserName(uri.username())
                    db.setPassword(uri.password())
                    sql = 'select code, code_name from dominios.{field} order by code'   
                if not db.open():
                    db.close()
                    return ret
                for field in currentLayer.fields():
                    fieldName = field.name()
                    if fieldName in self.specialEdgvAttributes():
                        # EDGV "special" attributes that are have different domains depending on 
                        # which class it belongs to
                        category = (table if isinstance(table, str) else table.name()).split("_")[0]
                        fieldN = "{attribute}_{cat}".format(attribute=fieldName, cat=category)
                        query = QSqlQuery(sql.format(field=fieldN), db)
                    else:
                        query = QSqlQuery(sql.format(field=fieldName), db)
                    if not query.isActive():
                        continue
                    while query.next():
                        code = str(query.value(0))
                        code_name = query.value(1)
                        ret[fieldName][code_name] = code    
                db.close()
            except:
                pass
        return ret

    def specialEdgvAttributes(self):
        """
        Gets the list of attributes shared by many EDGV classes and have a different domain
        depending on which category the EDGV class belongs to.
        :return: (list-of-str) list of "special" EDGV classes. 
        """
        return ["finalidade", "relacionado", "coincidecomdentrode"]

    def getEdgvDomainsFromTableName(self, table, field=None):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        :param table: (str) layer to be checked for its EDGV mapping.
        :param table: (QgsVectorLayer) overloaded method - layer to be checked for its EDGV mapping.
        :param field: (str) field to be checked.
        :return: (dict) value map.
        """
        ret = dict()
        currentLayer = table if isinstance(table, QgsVectorLayer) else self.layerByName(table)
        if currentLayer.isValid():
            try:
                uri = currentLayer.dataProvider().uri()
                field = field or self.currentField()
                if field in self.specialEdgvAttributes():
                    # EDGV "special" attributes that are have different domains depending on 
                    # which class it belongs to
                    category = self.currentLayerName().split("_")[0]
                    field = "{attribute}_{cat}".format(attribute=field, cat=category)
                if uri.host() == '':
                    db = QSqlDatabase('QSQLITE')
                    db.setDatabaseName(
                        uri.uri().split("|")[0].strip() if uri.uri().split("|")[0].strip().endswith(".gpkg") \
                            else uri.database()
                    )
                    sql = 'select code, code_name from dominios_{field} order by code'.format(field=field)
                else:
                    db = QSqlDatabase('QPSQL')
                    db.setHostName(uri.host())
                    db.setPort(int(uri.port()))
                    db.setDatabaseName(uri.database())
                    db.setUserName(uri.username())
                    db.setPassword(uri.password())
                    sql = 'select code, code_name from dominios.{field} order by code'.format(field=field)    
                if not db.open():
                    db.close()
                    return ret
                query = QSqlQuery(sql, db)
                if not query.isActive():
                    return ret       
                while query.next():
                    code = str(query.value(0))
                    code_name = query.value(1)
                    ret[code_name] = code      
                db.close()
            except:
                pass
        return ret

    def getEdgvDomains(self):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        :return: (dict) value map.
        """
        return self.getEdgvDomainsFromTableName(self.currentLayerName())

    @pyqtSlot(int, name='on_comboBox_currentIndexChanged')
    def populateFieldsTable(self):
        """
        Populates field map to codelist table.
        """
        fieldMap = self.currentFieldMap()
        self.tableWidget.setRowCount(len(fieldMap))
        for row, (code, value) in enumerate(fieldMap.items()):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(value))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(code))
        # self.tableWidget.sortItems(1)
