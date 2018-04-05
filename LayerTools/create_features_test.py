# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadByClass
                                 A QGIS plugin
 Load database classes.
                             -------------------
        begin                : 2015-03-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : lcoandrade@dsg.eb.mil.br
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
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

from qgis.core import QgsDataSourceURI, QgsMessageLog, QgsGeometry

import sys, os
from uuid import uuid4
# currentPath = 'C:/Users/luiz/.qgis2/python/plugins/DsgTools'
currentPath = '/home/luiz/.qgis2/python/plugins/DsgTools'
sys.path.append(os.path.join(currentPath, 'QmlTools'))
sys.path.append(os.path.join(currentPath, 'Utils'))
from qmlParser import QmlParser
from utils import Utils

import unittest, itertools

# class CreateFeatureTest(unittest.TestCase):
class CreateFeatureTest(): 
    def __init__(self, layers, geomClass = True):
        '''
        Constructor
        '''
        self.geomClass = geomClass

        #Connecting to the database that will be tested
        self.db = QSqlDatabase("QPSQL")
        self.db.setDatabaseName('fter')
        self.db.setHostName('localhost')
        self.db.setPort(5432)
        self.db.setUserName('postgres')
        self.db.setPassword('postgres')
        if not self.db.open():
            print self.db.lastError().text()

        #obtaining the qml file path
        qmlVersionPath = os.path.join(currentPath, 'Qmls', 'qgis_26')

        #Going through all loaded layers
        size = len(layers)
        count = 1
        for layer in layers:
            layerName = layer.name()
            fileName = layerName+'.qml'

#             qmlPath = os.path.join(qmlVersionPath, 'edgv_213', fileName)
            qmlPath = os.path.join(qmlVersionPath, 'FTer_2a_Ed', fileName)
            parser = QmlParser(qmlPath)
            domainDict = parser.getDomainDict()

            self.createFeatures(layer, domainDict)
            print str(count),'de',size,'Camada ',layer.name()
            count += 1

    def createFeatures(self, layer, domainDict):
        '''
        Creates dummy features to test the database structure
        layer: table used
        domainDict: domain dict made from the QML files
        '''
        #Getting the layer provider
        provider = layer.dataProvider()
        #Getting all fields
        fields = provider.fields()
        #Getting layer schema
        schema = str(QgsDataSourceURI(layer.dataProvider().dataSourceUri()).schema())

        #Creating the log file
        file = open(os.path.join(currentPath, 'LayerTools', 'Problemas', layer.name()+'_relatorio_banco_2016_03_29.txt'), 'w')
        filetext = ''
        #Iterate on every field
        for field in fields:
            #Check if the field name is inside the qml dict
            if field.name() in domainDict.keys():
                #Getting a obj for the field in analysis
                obj = domainDict[field.name()]
                #Test if the field is a dict
                if isinstance(obj, dict):
                    valueMap = obj
                    #Make a sql for each value in the dict
                    for value in valueMap.values():
                        sql = ''
                        if self.geomClass:
                            # if the class is a geometric class we must create a dummy geometry
                            geom = self.createGeom(layer)
                            #Exporting the geometry to wkt
                            ewkt = '\''+geom.exportToWkt()+'\','+str(31982)
                            #Start the query
                            sql += 'INSERT INTO %s.%s' % (schema, layer.name())
                            columns = '(geom,'+field.name()+')'
                            values = ' VALUES(ST_GeomFromText('+ewkt+'),'+value+')'
                            sql += columns+values
                        else:
                            sql += 'INSERT INTO complexos.'+layer.name()
                            columns = '(nome,'+field.name()+')'
                            values = ' VALUES(\'teste\','+value+')'
                            sql += columns+values
                        query = QSqlQuery(self.db)
                        filetext += self.executeSql(query, sql)
                elif isinstance(obj, list):
                    filter_keys = obj
                    for key in filter_keys:
                        sql = ''
                        if self.geomClass:
                            # if the class is a geometric class we must create a dummy geometry
                            geom = self.createGeom(layer)
                            #Exporting the geometry to wkt
                            ewkt = '\''+geom.exportToWkt()+'\','+str(31982)
                            #Start the query
                            sql += 'INSERT INTO %s.%s' % (schema, layer.name())
                            columns = '(geom,'+field.name()+')'
                            values = ' VALUES(ST_GeomFromText('+ewkt+'),ARRAY['+key+'])'
                            sql += columns+values
                        else:
                            sql += 'INSERT INTO complexos.'+layer.name()
                            columns = '(nome,'+field.name()+')'
                            values = ' VALUES(\'teste\',ARRAY['+key+'])'
                            sql += columns+values
                        query = QSqlQuery(self.db)
                        filetext += self.executeSql(query, sql)
        file.write(filetext)
        file.close()
        
    def executeSql(self, query, sql):
        '''
        Executes the sql query that creates the dummy features
        query: QSqlQuery object
        sql: actual query
        '''
        # try to execute the query
        text = ''
        if not query.exec_(sql):
            #Make error message
            text += 'SQL rodada: '+sql+'\n'
            text += 'Erro obtido: '+query.lastError().text()+'\n'
            #Write log on QGIS
            QgsMessageLog.logMessage('Deu merda: '+text, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            #Finish error message
            text += '-------------------------------------------\n'
        return text

    def createGeom(self, layer):
        '''
        Creates the dummy geometry according to the layer type
        layer: layer used to create the dummy geometries
        '''
        #Creating dummy geometries
        geom = None
        if layer.name().split('_')[-1] == 'p':
            geom = QgsGeometry.fromMultiPoint([QgsPoint(50,50)])
        if layer.name().split('_')[-1] == 'l':
            polyline = []

            point = QgsPoint(0, 0)
            polyline.append(point)
            point = QgsPoint(50, 50)
            polyline.append(point)

            geom = QgsGeometry.fromMultiPolyline([polyline])
        if layer.name().split('_')[-1] == 'a':
            polyline = []

            point = QgsPoint(0, 0)
            polyline.append(point)
            point = QgsPoint(50, 0)
            polyline.append(point)
            point = QgsPoint(50, 50)
            polyline.append(point)
            point = QgsPoint(0, 0)
            polyline.append(point)

            geom = QgsGeometry.fromMultiPolygon([[polyline]])

        return geom
    
    def testComplexAggregation(self):
        '''
        Tests complex aggregation. If a problem occurs a log file is made with information about it.
        '''
        #Creating the log file
        file = open(os.path.join(currentPath, 'LayerTools', 'Problemas', 'complexos_relatorio_banco_2016_03_29.txt'), 'w')
        
        sql = 'SELECT * from public.complex_schema order by complex asc'
        query = QSqlQuery(sql, self.db)
        while query.next():
            complex_schema = query.value(0)
            complex = query.value(1)
            aggregated_schema = query.value(2)
            aggregated_class = query.value(3)
            column_name = query.value(4)
            
            if aggregated_schema == 'complexos':
                continue
            
            sql = 'SELECT id from '+complex_schema+'.'+complex+' order by nome asc LIMIT 1'
            query1 = QSqlQuery(sql, self.db)
            while query1.next():
                uuid = str(query1.value(0))
    
            sql = 'SELECT id from '+aggregated_schema+'.'+aggregated_class+' order by id asc LIMIT 1'
            query2 = QSqlQuery(sql, self.db)
            while query2.next():
                id = str(query2.value(0))
    
            sql = 'UPDATE '+aggregated_schema+'.'+aggregated_class+' SET '+column_name+'='+'\''+uuid+'\''+' WHERE id='+id
            query3 = QSqlQuery(self.db)
            if not query3.exec_(sql):
                filetext = 'SQL rodada: '+sql+'\n'
                filetext += 'Erro obtido: '+query3.lastError().text()+'\n'
                filetext += '-------------------------------------------\n'
                QgsMessageLog.logMessage(filetext, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                file.write(filetext)
        file.close()

layers = iface.mapCanvas().layers()
#creator = CreateFeatureTest(layers, False)
creator.testComplexAggregation() #to run this method QGIS TOC (layers tree) must be empty