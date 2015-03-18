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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from qgis.core import *

import sys, os
currentPath = 'C:/Users/luiz/.qgis2/python/plugins/DsgTools'
sys.path.append(os.path.join(currentPath, 'QmlTools'))
sys.path.append(os.path.join(currentPath, 'Utils'))
from qmlParser import QmlParser
from utils import Utils

import unittest, itertools

# class CreateFeatureTest(unittest.TestCase):
class CreateFeatureTest():
    def __init__(self, layers):
        self.db = QSqlDatabase("QPSQL")
        self.db.setDatabaseName('edgv213')
        self.db.setHostName('localhost')
        self.db.setPort(5432)
        self.db.setUserName('postgres')
        self.db.setPassword('postgres')
        if not self.db.open():
            print self.db.lastError().text()


        #obtaining the qml file path
        qmlVersionPath = os.path.join(currentPath, 'Qmls', 'qgis_26')

        for layer in layers:
            layerName = layer.name()
            fileName = layerName+'.qml'

            qmlPath = os.path.join(qmlVersionPath, 'edgv_213', fileName)
            parser = QmlParser(qmlPath)
            domainDict = parser.getDomainDict()
            
            self.createFeatures(layer, domainDict)
            
    def createFeatures(self, layer, domainDict):
        provider = layer.dataProvider()
        fields = provider.fields()
        
        #getting all attributes that are valueMaps
        combinationlist = []
        mapIndexes = []
        for field in fields:
            if field.name() in domainDict.keys():
                print layer.fieldNameIndex(field.name()),field.name()
                valueMap = domainDict[field.name()]
                #storing the valueMaps
                combinationlist.append(valueMap.values())
                #storing the indexes
                mapIndexes.append(layer.fieldNameIndex(field.name()))
        
        #calculate all possible combinations between attributes that are valueMaps
        allcombinations = list(itertools.product(*combinationlist))
        #checking the combinations
        print 'combinations',allcombinations
              
        #getting the normal attributes
        normalIndexes = dict()        
        for field in fields:
            print 'tipos geral: ',field.type(), field.typeName()
            if field.name() not in domainDict.keys():
                #defining a dummy value to store with the field index
                if field.name() != 'id' and field.type() == 2:
                    normalIndexes[layer.fieldNameIndex(field.name())] = 0
                elif field.typeName() != 'uuid' and field.type() == 10:
                    normalIndexes[layer.fieldNameIndex(field.name())] = 'teste'
                    
        #just checking the normal indexes
        print 'normal: ',normalIndexes
                    
        for combination in allcombinations:
            feat = QgsFeature()            
            geom = self.createGeom(layer)
            feat.setGeometry(geom)

            #getting the nextval for the layer
            sql = 'select nextval(\'cb.'+layer.name()+'_id_seq\'::regclass)'
            query = QSqlQuery(sql, self.db)
            print 'query: ',sql
            while query.next():
                nextval = query.value(0)
                print 'nextval: ',nextval
                feat.setFeatureId(nextval)
                feat.setAttributes([0,nextval])
            
            #inserting the dummy values in the feature
            for key in normalIndexes.keys():
                feat.setAttributes([key, normalIndexes[key]])

            #inserting the combination values in the feature
            for i in range(len(combination)):
                idx = mapIndexes[i]
                print 'field ID = ',idx,'||field Value = ',combination[i]
                feat.setAttributes([idx, combination[i]])
            
            print 'feature ID: ',feat.id(),'feature with combination: ', combination
        
            #actual layer editing
            print layer.dataProvider().addFeatures([feat])
            for error in layer.dataProvider().errors():
                QgsMessageLog.logMessage(error, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            
    def createGeom(self, layer):
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
    
layers = iface.mapCanvas().layers()
creator = CreateFeatureTest(layers)
