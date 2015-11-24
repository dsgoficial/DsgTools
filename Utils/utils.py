# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

import qgis as qgis
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog

import os
from osgeo import ogr
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class Utils:
    def __init__(self):
        self.factory = SqlGeneratorFactory()

    def __del__(self):
        pass
    
    def mergeDict(self,dictionary1, dictionary2):
        output = dict()
        if type(dictionary1) <> dict or type(dictionary2) <> dict:
            return dictionary2
        for item, value in dictionary1.iteritems():
            if dictionary2.has_key(item):
                if isinstance(dictionary2[item], dict):
                    output[item] = self.mergeDict(value, dictionary2.pop(item))
                else:
                    if type(value) == list:
                        if item not in output.keys():
                            output[item] = []
                        for i in value:
                            if i not in output[item]:
                                output[item].append(i)
                        output[item].extend(self.mergeDict(value, dictionary2.pop(item)))
                    else:
                        output[item] = self.mergeDict(value, dictionary2.pop(item))
            else:
                if type(value) == list:
                    if item not in output.keys():
                        output[item]=[]
                    for i in value:
                        if i not in output[item]:
                            output[item].append(i)
                else:
                    output[item] = value
        for item, value in dictionary2.iteritems():
            if type(value) == list:
                if item not in output.keys():
                    output[item]=[]
                for i in value:
                    if i not in output[item]:
                        output[item].append(i)
            else:
                output[item] = value
        return output
    
    def buildOneNestedDict(self,inputDict,keyList,value):
        if len(keyList) == 1:
            if keyList[0] not in inputDict.keys():
                inputDict[keyList[0]] = dict()
            if type(value) == list:
                inputDict[keyList[0]]=[]
                for i in value:
                    if i not in inputDict[keyList[0]]:
                        inputDict[keyList[0]].append(i)
            else:
                inputDict[keyList[0]]=value
            return inputDict
        else:
            if keyList[0] not in inputDict.keys():
                if len(inputDict.values()) == 0:
                    inputDict[keyList[0]] = dict()
            inputDict[keyList[0]] = self.buildOneNestedDict(inputDict[keyList[0]],keyList[1::],value)
            return inputDict
    
    def buildNestedDict(self,inputDict,keyList,value):
        if len(inputDict.keys())>0:
            tempDict = self.buildOneNestedDict(dict(),keyList,value)
            return self.mergeDict(inputDict, tempDict)
        else:
            return self.buildOneNestedDict(inputDict,keyList,value)

    def getQmlDir(self, db):
        currentPath = os.path.dirname(__file__)
        if qgis.core.QGis.QGIS_VERSION_INT >= 20600:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_26')
        else:
            qmlVersionPath = os.path.join(currentPath, '..', 'Qmls', 'qgis_22')

        version = self.getDatabaseVersion(db)
        if version == '3.0':
            qmlPath = os.path.join(qmlVersionPath, 'edgv_30')
        elif version == '2.1.3':
            qmlPath = os.path.join(qmlVersionPath, 'edgv_213')
        return qmlPath

    def getPostGISConnectionParameters(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        database = settings.value('database')
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (database, host, port, user, password)

    def getPostGISConnections(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    def getPostGISDatabase(self, postGISConnection):
        (database, host, port, user, password) = self.getPostGISConnectionParameters(postGISConnection)
        return self.getPostGISDatabaseWithParams(database, host, port, user, password)
    
    def getPostGISDatabaseWithParams(self, database, host, port, user, password):
        db = None
        db = QSqlDatabase("QPSQL")
        db.setDatabaseName(database)
        db.setHostName(host)
        db.setPort(int(port))
        db.setUserName(user)
        db.setPassword(password)
        return db

    def isSpatialiteDB(self, db):
        if db.driverName() == 'QPSQL':
            isSpatialite = False
        elif db.driverName() == 'QSQLITE':
            isSpatialite = True
        return isSpatialite
    
    #TODO: Reimplement in server_tools
    def browseServer(self,dbList,host,port,user,password):
        gen = self.factory.createSqlGenerator(False)
        edvgDbList = []
        for database in dbList:
            db = self.getPostGISDatabaseWithParams(database,host,port,user,password)
            if not db.open():
                qgis.utils.iface.messageBar().pushMessage('DB :'+database+'| msg: '+db.lastError().databaseText(), level=QgsMessageBar.CRITICAL)

            query = QSqlQuery(db)
            if query.exec_(gen.getEDGVVersion()):
                while query.next():
                    version = query.value(0)
                    if version:
                        edvgDbList.append((database,version))
        return edvgDbList
    
    #TODO: Reimplement in server_tools    
    def getDbsFromServer(self,name):
        gen = self.factory.createSqlGenerator(False)
        
        (host, port, user, password) = self.getServerConfiguration(name)
        database = 'postgres'
        
        db = self.getPostGISDatabaseWithParams(database,host,port,user,password)
        if not db.open():
            QgsMessageLog.logMessage(db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        
        query = QSqlQuery(gen.getDatabasesFromServer(),db)
        dbList = []
        while query.next():
            dbList.append(query.value(0))
        return self.browseServer(dbList,host,port,user,password)
    
    def listComplexClassesWithElementsFromDatabase(self, db, isSpatialite):
        classList = self.listComplexClassesFromDatabase(db, isSpatialite)
        return self.listWithElementsFromDatabase(classList,db,isSpatialite)
    
    def makeOgrPostGISConn(self, db):
        dbName = db.databaseName()
        dbUser = db.userName()
        dbHost = db.hostName()
        dbPass = db.password()
        dbPort = str(db.port())
        constring = 'PG: dbname=\''+dbName+'\' user=\''+dbUser+'\' host=\''+dbHost+'\' password=\''+dbPass+'\' port='+dbPort
        return constring

    def makeTranslationMap(self, layerName, layer, outLayer, fieldMapper):
        layerFieldMapper=fieldMapper[layerName]
        layerDef = layer.GetLayerDefn()
        outLayerDef = outLayer.GetLayerDefn()
        panMap = []        
        for i in range(layerDef.GetFieldCount()):
            featureDef = layerDef.GetFieldDefn(i)
            fieldName = featureDef.GetName()
            if fieldName in layerFieldMapper.keys():
                name = layerFieldMapper[fieldName]
                fieldId = outLayerDef.GetFieldIndex(name)
                panMap.append(fieldId) 
            else:
                panMap.append(-1)
        return panMap
    
    def translateLayer(self, inputLayer, inputLayerName, outputLayer, layerPanMap, defaults={}, translateValues={}):
        inputLayer.ResetReading()
                    
        for feat in inputLayer:
            newFeat=ogr.Feature(outputLayer.GetLayerDefn())
            newFeat.SetFromWithMap(feat,True,layerPanMap)
            outputLayer.CreateFeature(newFeat)

    def translateLayerWithDataFix(self, inputLayer, inputLayerName, outputLayer, layerPanMap, defaults={}, translateValues={}):
        inputLayer.ResetReading()
        attrBlackList = dict()
        if invalidatedDataDict is not None:
            invId = []
            for errorType in invalidatedDataDict.keys():
                if errorType == 'nullComplexPk':
                    if className in invalidatedDataDict[errorType].keys():
                        invId.append(invalidatedDataDict[errorType][inputLayerName])
                if errorType == 'notInDomain' or errorType == 'nullAttribute':
                    if className in invalidatedDataDict[errorType].keys():
                        for id in invalidatedDataDict[errorType][inputLayerName].keys():
                            if id not in attrBlackList.keys():
                                attrBlackList[id]=[]
                            for a in invalidatedDataDict[errorType][inputLayerName][id].keys():
                                if a not in attrBlackList[id]:
                                    attrBlackList[id].append(a)
                    
        for feat in inputLayer:
            if invalidatedDataDict is not None:
                outputLyrDef = outputLayer.GetLayerDefn()
                newFeat=ogr.Feature(outputLayer.GetLayerDefn())
                featOriginalId = inputLayer.GetField('OGC_FID')
                newFeat.SetFromWithMap(feat,True,layerPanMap)
                outputLayer.CreateFeature(newFeat)
            else:
                newFeat=ogr.Feature(outputLayer.GetLayerDefn())
                newFeat.SetFromWithMap(feat,True,layerPanMap)
                outputLayer.CreateFeature(newFeat)

    def translateDS(self, inputDS, outputDS, fieldMap, inputLayerList, inputIsSpatialite):
        gen = self.factory.createSqlGenerator(inputIsSpatialite)
        for filename in inputLayerList:
            if inputIsSpatialite:
                schema = filename.split('_')[0]
            else:
                schema = filename.split('.')[0]
            attr = fieldMap[filename].keys()
            attrList = []
            for a in attr:
                if schema == 'complexos':
                    attrList.append(a)
                elif a not in ['id']:
                    attrList.append(a)
            
            sql = gen.getFeaturesWithSQL(filename,attrList) #order elements here
            inputLayer = inputDS.ExecuteSQL(sql.encode('utf-8'))
            if inputIsSpatialite:
                outFileName = filename.split('_')[0]+'.'+'_'.join(filename.split('_')[1::])
            else:
                outFileName = filename.replace('.','_')

            outputLayer=outputDS.GetLayerByName(outFileName)
            #order conversion here
            layerPanMap=self.makeTranslationMap(filename, inputLayer,outputLayer, fieldMap)
            self.translateLayer(inputLayer, filename, outputLayer, layerPanMap)
        outputDS.Destroy()
        return True

    def translateDSWithDataFix(self, inputDS, outputDS, fieldMap, inputLayerList, inputIsSpatialite,invalidatedDataDict):
        gen = self.factory.createSqlGenerator(inputIsSpatialite)
        for filename in inputLayerList:
            if inputIsSpatialite:
                schema = filename.split('_')[0]
            else:
                schema = filename.split('.')[0]
            attr = fieldMap[filename].keys()
            attrList = []
            for a in attr:
                if schema == 'complexos':
                    attrList.append(a)
                elif a not in ['id']:
                    attrList.append(a)
            
            sql = gen.getFeaturesWithSQL(filename,attrList) #order elements here
            inputLayer = inputDS.ExecuteSQL(sql.encode('utf-8'))
            if inputIsSpatialite:
                outFileName = filename.split('_')[0]+'.'+'_'.join(filename.split('_')[1::])
            else:
                outFileName = filename.replace('.','_')

            outputLayer=outputDS.GetLayerByName(outFileName)
            #order conversion here
            layerPanMap=self.makeTranslationMap(filename, inputLayer,outputLayer, fieldMap)
            self.translateLayerWithDataFix(inputLayer, filename, outputLayer, layerPanMap,invalidatedDataDict)
        outputDS.Destroy()
        return True