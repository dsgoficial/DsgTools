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
# currentPath = 'C:/Users/luiz/.qgis2/python/plugins/DsgTools'
currentPath = '/home/dsgdev/.qgis2/python/plugins/DsgTools'
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

        size = len(layers)
        count = 1
        for layer in layers:
            layerName = layer.name()
            fileName = layerName+'.qml'

            qmlPath = os.path.join(qmlVersionPath, 'edgv_213', fileName)
            parser = QmlParser(qmlPath)
            domainDict = parser.getDomainDict()

            self.createFeatures(layer, domainDict)
            print str(count),'de',size,'Camada ',layer.name()
            count += 1

    def createFeatures(self, layer, domainDict):
        provider = layer.dataProvider()
        fields = provider.fields()

        #getting all attributes that are valueMaps
        combinationlist = []
        mapIndexes = []
        for field in fields:
            if field.name() in domainDict.keys():
                valueMap = domainDict[field.name()]
                #storing the valueMaps
                combinationlist.append(valueMap.values())
                #storing the indexes
                mapIndexes.append(field.name())

        #calculate all possible combinations between attributes that are valueMaps
        allcombinations = list(itertools.product(*combinationlist))
        #checking the combinations
#         print 'combinations',allcombinations

        #getting the normal attributes
        normalIndexes = dict()
        for field in fields:
#             print 'tipos geral: ',field.type(), field.typeName()
            if field.name() not in domainDict.keys():
                #defining a dummy value to store with the field index
                if field.name() != 'id' and field.type() == 2:
                    normalIndexes[field.name()] = 0
                elif field.typeName() != 'uuid' and field.type() == 10:
                    normalIndexes[field.name()] = '\'teste\''

        #just checking the normal indexes
#         print 'normal: ',normalIndexes

        for combination in allcombinations:
            geom = self.createGeom(layer)
            ewkt = '\''+geom.exportToWkt()+'\','+str(31983)
            sql = 'INSERT INTO cb.'+layer.name()
            columns = '(geom'
            values = ' VALUES(ST_GeomFromText('+ewkt+')'

            #inserting the dummy values in the feature
            for key in normalIndexes.keys():
                fieldName = key
                columns += ','+fieldName
                values += ','+normalIndexes[key]

            #inserting the combination values in the feature
            for i in range(len(combination)):
                fieldName = mapIndexes[i]
                columns += ','+fieldName
                values += ','+combination[i]
#                 print 'field ID = ',fieldName,'||field Value = ',combination[i]

            columns += ')'
            values += ')'

            sql += columns+values
#             print sql
            query = QSqlQuery(self.db)
            file = open('/home/dsgdev/.qgis2/python/plugins/DsgTools/LayerTools/'+layer.name()+'_relatorio_banco_2015_03_18.txt','w')
            filetext = ''
            if not query.exec_(sql):
                QgsMessageLog.logMessage('Deu merda: '+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                filetext += 'SQL rodada: '+sql+'\n'
                filetext += 'Erro obtido: '+query.lastError().text()+'\n'
            file.write(filetext)
            file.close()

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
