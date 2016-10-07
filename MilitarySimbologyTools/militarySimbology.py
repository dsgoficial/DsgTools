# -*- coding: utf-8 -*-

"""
/***************************************************************************
militarySymbology
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-10-05
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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

# Qt imports
from PyQt4.QtSql import QSqlDatabase
# QGIS imports
from qgis.core import QgsDataSourceURI, QgsMapLayerRegistry, QgsVectorLayer, QgsProject, QgsLayerTreeLayer
# lib python imports
import re
import os

class MilitarySymbology:
    def __init__(self, iface, sqlitePathDB, stylePath, nameLayer):
        """construtor"""
        self.iface = iface
        self.stylePath = stylePath
        uri = QgsDataSourceURI()
        uri.setDatabase(sqlitePathDB)
        listOfTables = self.readTablesSqlite(uri)
        listOfConf = self.loadTables(uri, listOfTables)
        self.loadLayer(listOfConf, uri, nameLayer)

    def readTablesSqlite(self, uri):
        """
        listo todas as tabelas de mapa de valores no Sqlite e as guardo em uma lista
        """
        db = QSqlDatabase.addDatabase("QSQLITE");
        db.setDatabaseName(uri.database())
        db.open()
        query = db.exec_("""SELECT name FROM sqlite_master WHERE type='table';""")
        listOfTables = []
        while query.next():
            m = re.search('^d', query.value(0))
            if m != None:
                listOfTables.append(m.string)
        return listOfTables
    
    def setConfStyleForm(self, tableId):
        """defino as configurações para cada campo do formulário de acordo com suas
            respectivas tabelas de mapa de valores
        """
        conf = dict()
        #conf[u'FilterExpression'] = u'code in (0,1,2,3)'
        conf[u'Layer'] = tableId
        conf[u'UseCompleter'] = False
        conf[u'AllowMulti'] =  True
        conf[u'AllowNull'] = True
        conf[u'OrderByValue'] =  False
        conf[u'Value'] = u'code_name'
        conf[u'Key'] = u'code'
        return conf        
    
    def loadTables(self, uri, listOfTables):
        """
        Carrego as tabelas de mapa de valores para o Qgis em seu grupo
        """
        listOfConfToFields = []
        root = QgsProject.instance().layerTreeRoot()
        if not root.findGroup(u"Mapa_de_valores"):
            legend = self.iface.legendInterface()
            groupMapvalue = legend.addGroup (u"Mapa_de_valores", True)
            
            for table in listOfTables:
                uri.setDataSource('', table,'','','id')
                table = QgsVectorLayer(uri.uri(), table[9:], 'spatialite')
                QgsMapLayerRegistry.instance().addMapLayer(table)
                tableId = self.iface.activeLayer().id()
                legend.moveLayer(legend.layers()[0], groupMapvalue)
                conf = self.setConfStyleForm(tableId)
                listOfConfToFields.append(conf)
            return listOfConfToFields
        else:
            group = root.findGroup(u"Mapa_de_valores")
            for table in group.children():
                conf = self.setConfStyleForm(table.layerId())
                listOfConfToFields.append(conf)
            return list(reversed(listOfConfToFields))
        
    def loadLayer(self, listOfConf, uri, nameLayer):
        """
        Carrego as camadas
        """
        root = QgsProject.instance().layerTreeRoot()
        mygroup = root.findGroup(u"Mapa_de_valores")
        parentGroup = mygroup.parent()
        groupIndex=-1
        for child in parentGroup.children():
            groupIndex+=1
            if mygroup == child:
                break
        uri.setDataSource('', nameLayer.lower(), 'geometria', '', 'id')
        layer = QgsVectorLayer(uri.uri(), nameLayer, 'spatialite')
        QgsMapLayerRegistry.instance().addMapLayer(layer, False)
        parentGroup.insertChildNode(groupIndex, QgsLayerTreeLayer(layer))
        self.loadStyle(layer, listOfConf)
     
    def loadStyle(self, layer, listOfConf):
        """
        Defino o estilo para a camada carregada
        """
        with open( self.stylePath, 'r') as template_style:
            style = template_style.read().replace('\n', '')
        styleReady = unicode(self.setPathStyle(style), 'utf-8')    
        layer.applyNamedStyle(styleReady)
        i = 2
        for index in range(len(listOfConf)) : 
            layer.setEditorWidgetV2Config(i, listOfConf[index] )
            i+=1

    def setPathStyle(self, style):
        """
        Defino a variável {path} no modelo de estilo (.qml) para apontar pro .SVG de acordo com sistema
        """
        currentPath = os.path.join(os.path.dirname(__file__), 'symbols')+os.sep
        styleReady = style.replace('{path}', currentPath)
        return styleReady
