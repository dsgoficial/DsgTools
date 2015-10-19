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

import os, ogr
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

class Utils:
    def __init__(self):
        self.factory = SqlGeneratorFactory()

    def __del__(self):
        pass

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

    def findEPSG(self, db):
        gen = self.factory.createSqlGenerator(self.isSpatialiteDB(db))
        sql = gen.getSrid()
        query = QSqlQuery(sql, db)
        srids = []
        while query.next():
            srids.append(query.value(0))
        return srids[0]

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

    def getSpatialiteDatabase(self):
        db = None
        fd = QFileDialog()
        filename = fd.getOpenFileName(filter='*.sqlite')
        if filename:
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(filename)
        return (filename, db)

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

    def getDatabaseVersion(self, db):
        gen = self.factory.createSqlGenerator(self.isSpatialiteDB(db))
        sqlVersion = gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, db)
        version = '2.1.3'
        while queryVersion.next():
            version = queryVersion.value(0)
        return version

    def isSpatialiteDB(self, db):
        if db.driverName() == 'QPSQL':
            isSpatialite = False
        elif db.driverName() == 'QSQLITE':
            isSpatialite = True
        return isSpatialite
    
    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)
    
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
    
    def storeConnection(self, server, database):
        (host, port, user, password) = self.getServerConfiguration(server)
        
        connection = server+'_'+database
        settings = QSettings()
        if not settings.contains('PostgreSQL/connections/'+connection+'/database'):
            settings.beginGroup('PostgreSQL/connections/'+connection)
            settings.setValue('database', database)
            settings.setValue('host', host)
            settings.setValue('port', port)
            settings.setValue('username', user)
            settings.setValue('password', password)
            settings.endGroup()
            return True
        return False
    
    def listGeomClassesFromDatabase(self, db, isSpatialite):
        classList = []
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = gen.getTablesFromDatabase()
        query = QSqlQuery(sql, db)
        while query.next():
            if isSpatialite:
                tableName = query.value(0).encode('utf-8')
                layerName = tableName
            else:
                tableSchema = query.value(0).encode('utf-8')
                tableName = query.value(1).encode('utf-8')
                layerName = tableSchema+'.'+tableName
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a":

                classList.append(layerName)
        
        return classList

    def listComplexClassesFromDatabase(self, db, isSpatialite):
        classList = []
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = gen.getTablesFromDatabase()
        query = QSqlQuery(sql, db)
        while query.next():
            if isSpatialite:
                tableName = query.value(0).encode('utf-8')
                layerName = tableName
                tableSchema = layerName.split('_')[0]
            else:
                tableSchema = query.value(0).encode('utf-8')
                tableName = query.value(1).encode('utf-8')
                layerName = tableSchema+'.'+tableName
            if tableSchema == 'complexos':
                classList.append(layerName)
        
        return classList
    
    def countElements(self, layers, db, isSpatialite):
        listaQuantidades = []
        for layer in layers:
            gen = self.factory.createSqlGenerator(isSpatialite)
            sql = gen.getElementCountFromLayer(layer)
            query = QSqlQuery(sql,db)
            query.next()
            number = query.value(0)
            if not query.exec_(sql):
                QgsMessageLog.logMessage(self.tr("Problem counting elements: ")+query.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            listaQuantidades.append([layer, number])
        return listaQuantidades

    def listWithElementsFromDatabase(self, classList, db, isSpatialite):
        classListWithNumber = self.countElements(classList, db, isSpatialite)
        classesWithElements = dict()
        for cl in classListWithNumber:
            if cl[1]>0:
                classesWithElements[cl[0]]=cl[1]   
        return classesWithElements
    
    def listClassesWithElementsFromDatabase(self, db, isSpatialite):
        geomClassList = self.listGeomClassesFromDatabase(db, isSpatialite)
        complexClassList = self.listComplexClassesFromDatabase(db, isSpatialite)
        classList = []
        for g in geomClassList:
            classList.append(g)
        for c in complexClassList:
            classList.append(c)
        classList.sort()
        return self.listWithElementsFromDatabase(classList,db,isSpatialite)
    
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
    
    def getPostgisNotNullDict(self, edgvVersion, db):
        gen = self.factory.createSqlGenerator(False)
        if edgvVersion == '2.1.3':
            schemaList = ['cb','complexos']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return
        sql = gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, db)
        notNullDict = dict()
        while query.next():
            schemaName = query.value(0).encode('utf-8')
            className = query.value(1).encode('utf-8')
            attName = query.value(2).encode('utf-8')
            cl = schemaName+'.'+className
            if cl not in notNullDict.keys():
                notNullDict[cl]=[]
            notNullDict[cl].append(attName)
        return notNullDict

    def getPostgisDomainDict(self, edgvVersion, db):
        gen = self.factory.createSqlGenerator(False)
        if edgvVersion == '2.1.3':
            schemaList = ['cb','complexos','dominios']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return
        sql = gen.validateWithDomain(schemaList)

        query = QSqlQuery(sql, db)
        classDict = dict()
        domainDict = dict()
        
        while query.next():
            schemaName = query.value(0).encode('utf-8')
            className = query.value(1).encode('utf-8')
            attName = query.value(2).encode('utf-8')
            domainName = query.value(3).encode('utf-8')
            domainTable = query.value(4).encode('utf-8')
            domainQuery = query.value(5).encode('utf-8')
            cl = schemaName+'.'+className
            if cl not in classDict.keys():
                classDict[cl]=dict()
            if attName not in classDict[cl].keys():
                classDict[cl][attName]=[]
                query2 = QSqlQuery(domainQuery,db)
                while query2.next():
                    value = query2.value(0)
                    classDict[cl][attName].append(value)

        return classDict
    
    def getStructureDict(self, db, edgvVersion, isSpatialite):
        gen = self.factory.createSqlGenerator(isSpatialite)
        classDict = dict()
        sql = gen.getStructure(edgvVersion)        
        query = QSqlQuery(sql, db)
        
        if isSpatialite:
            while query.next():
                className = query.value(0).encode('utf-8')
                classSql = query.value(1).encode('utf-8')
                
                if className not in classDict.keys():
                    classDict[className]=dict()
                classSql = classSql.split(className)[1]
                sqlList = classSql.replace('(','').replace(')','').replace('\"','').replace('\'','').split(',')
                for s in sqlList:
                     fieldName = str(s.strip().split(' ')[0])
                     classDict[className][fieldName]=fieldName
                     
        if not isSpatialite:
            while query.next():
                className = query.value(0).encode('utf-8')+'.'+query.value(1).encode('utf-8')
                fieldName = query.value(2).encode('utf-8')
                if className not in classDict.keys():
                    classDict[className]=dict()

                classDict[className][fieldName]=fieldName

        return classDict

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
    
    def translateLayer(self, inputLayer, inputLayerName, outputLayer, layerPanMap, defaults={}, translateValues={},invalidatedDataDict=None):
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

    def translateDS(self, inputDS, outputDS, fieldMap, inputLayerList, inputIsSpatialite,invalidatedDataDict=None):
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
            self.translateLayer(inputLayer, filename, outputLayer, layerPanMap,invalidatedDataDict)
        outputDS.Destroy()
        return True
    
    def getAggregationAttributes(self,db,isSpatialite):
        columns = []
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = gen.getAggregationColumn()
        query = QSqlQuery(sql, db)
        
        while query.next():
            value = query.value(0)
            columns.append(value)
        return columns