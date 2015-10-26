# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from PyQt4.QtSql import QSqlQuery, QSqlDatabase

class PostgisDb(AbstractDb):
    
    def __init__(self):
        super(PostgisDb,self).__init__()
        self.db = QSqlDatabase('QPSQL')

    def connectDatabaseWithServerName(self,name):
        (host, port, user, password) = self.getServerConfiguration(name)
        self.db.setHostName(host)
        self.db.setPort(port)
        self.db.setUserName(user)
        self.db.setPassword(password)

    
    def listGeomClassesFromDatabase(self):
        self.checkAndOpenDb()      
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableSchema = query.value(0).toString()
            tableName = query.value(1).toString()
            layerName = tableSchema+'.'+tableName
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a":
                classList.append(layerName)
        return classList
    
    def listComplexClassesFromDatabase(self):
        self.checkAndOpenDb()        
        classList = []
        gen = self.factory.createSqlGenerator(isSpatialite)
        sql = gen.getTablesFromDatabase()
        query = QSqlQuery(sql, db)
        while query.next():
            tableSchema = query.value(0).toString()
            tableName = query.value(1).toString()
            layerName = tableSchema+'.'+tableName
            if tableSchema == 'complexos':
                classList.append(layerName)
        return classList

    def storeConnection(self, server):
        (host, port, user, password) = self.getServerConfiguration(server)
        database = self.db.databaseName()
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

    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)        

    def storeConnection(self, server):
        (host, port, user, password) = self.getServerConfiguration(server)
        connection = server+'_'+self.db.databaseName()
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

    def getStructureDict(self):
        self.checkAndOpenDb()
        classDict = dict()
        sql = gen.getStructure(self.dbVersion)        
        query = QSqlQuery(sql, db)
        while query.next():
            className = query.value(0).toString()+'.'+query.value(1).toString()
            fieldName = query.value(2).toString()
            if className not in classDict.keys():
                classDict[className]=dict()
            classDict[className][fieldName]=fieldName
        return classDict
    
    def makeOgrConn(self):
        dbName = self.db.databaseName()
        dbUser = self.db.userName()
        dbHost = self.db.hostName()
        dbPass = self.db.password()
        dbPort = str(self.db.port())
        constring = 'PG: dbname=\''+dbName+'\' user=\''+dbUser+'\' host=\''+dbHost+'\' password=\''+dbPass+'\' port='+dbPort
        return constring
    
    def buildOgrDatabase(self):
        con = self.makeOgrConn()
        self.ogrDb = ogr.Open(con)

    def getNotNullDict(self):
        self.checkAndOpenDb()
        if self.dbVersion == '2.1.3':
            schemaList = ['cb','complexos']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return None
        sql = self.gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, self.db)
        notNullDict = dict()
        while query.next():
            schemaName = query.value(0).toString()
            className = query.value(1).toString()
            attName = query.value(2).toString()
            cl = schemaName+'.'+className
            if cl not in notNullDict.keys():
                notNullDict[cl]=[]
            notNullDict[cl].append(attName)
        return notNullDict

    def getDomainDict(self):
        self.checkAndOpenDb()
        if self.dbVersion == '2.1.3':
            schemaList = ['cb','complexos','dominios']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return
        sql = self.gen.validateWithDomain(schemaList)
        query = QSqlQuery(sql, self.db)
        classDict = dict()
        domainDict = dict()
        while query.next():
            schemaName = query.value(0).toString()
            className = query.value(1).toString()
            attName = query.value(2).toString()
            domainName = query.value(3).toString()
            domainTable = query.value(4).toString()
            domainQuery = query.value(5).toString()
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
    
    #TODO: treat each case (hammer time and don't touch my data)
    def convertToPostgis(self, outputDb,type):
        return None
    
    def convertToSpatialite(self, outputDb,type):
        
        return None    
    
    def makeValidationSummary(self):
        return None
    
    def buildInvalidatedDict(self):
        invalidated = dict()
        notNullDict = self.utils.getPostgisNotNullDict(edgvVersion, postgisDB)
        spatialiteDbStructure = self.utils.getStructureDict(spatialiteDB, edgvVersion, True)
        aggregationColumns = self.utils.getAggregationAttributes(postgisDB,False)
 
        invalidated['nullLine'] = dict()       
        invalidated['nullPk'] = dict()
        invalidated['notInDomain'] = dict()
        invalidated['nullAttribute'] = dict()
        return invalidated
    
    def validateWithOutputDatabaseSchema(self,outputdb):
        invalidated = self.buildInvalidatedDict()
        outputdbStructure = outputdb.getStructureDict()
        domainDict = self.getDomainDict()
        classes = self.listClassesWithElementsFromDatabase()
        notNullDict = self.getNotNullDict()
        
        for cl in classes:
            if cl in outputdbStructure.keys():
                schema = cl.split('_')[0]
                table = '_'.join(cl.split('_')[1::])
                pgClass = schema + '.' + table
                allAttrList = outputdbStructure[cl].keys()
                if schema == 'complexos':
                    attrList = ['id']
                else:
                    attrList = ['OGC_FID']
                for att in allAttrList:
                    if att not in attrList:
                        attrList.append(att)
                sql = self.gen.getFeaturesWithSQL(cl,attrList) 
                query = QSqlQuery(sql, spatialiteDB)
                
                while query.next():
                    id = query.value(0)
                    #detects null lines
                    for i in range(len(attrList)):
                        nullLine = True
                        value = query.value(i)
                        if value <> None:
                            nullLine = False
                            break
                    if nullLine:
                        if cl not in invalidated['nullLine'].keys():
                            invalidated['nullLine'][cl]=0
                        invalidated['nullLine'][cl]+=1
                    
                    #validates pks
                    if id == None and (not nullLine):
                        if cl not in invalidated['nullPk'].keys():
                            invalidated['nullPk'][cl]=0
                        invalidated['nullPk'][cl]+=1
                    
                    for i in range(len(attrList)):
                        value = query.value(i)
                        #validates domain
                        if pgClass in domainDict.keys():    
                            if attrList[i] in domainDict[pgClass].keys():
                                if value not in domainDict[pgClass][attrList[i]] and (not nullLine):
                                    if cl not in invalidated['notInDomain'].keys():
                                        invalidated['notInDomain'][cl] = dict()
                                    if id not in invalidated['notInDomain'][cl].keys():
                                        invalidated['notInDomain'][cl][id] = dict()
                                    if att not in invalidated['notInDomain'][cl][id].keys():
                                        invalidated['notInDomain'][cl][id][attrList[i]] = dict()
                                    invalidated['notInDomain'][cl][id][attrList[i]] = value
                        #validates not nulls
                        if pgClass in notNullDict.keys():
                            if pgClass in domainDict.keys():
                                if attrList[i] in notNullDict[pgClass] and attrList[i] not in domainDict[pgClass].keys():
                                    if (value == None) and (not nullLine) and (attrList[i] not in domainDict[pgClass].keys()):
                                        if cl not in invalidated['nullAttribute'].keys():
                                            invalidated['nullAttribute'][cl] = dict()
                                        if id not in invalidated['nullAttribute'][cl].keys():
                                            invalidated['nullAttribute'][cl][id] = dict()
                                        if attrList[i] not in invalidated['nullAttribute'][cl][id].keys():
                                            invalidated['nullAttribute'][cl][id][attrList[i]] = dict()
                                        invalidated['nullAttribute'][cl][id][attrList[i]] = value                                    
                            else:
                                if attrList[i] in notNullDict[pgClass]:
                                    if (value == None) and (not nullLine) and (attrList[i] not in domainDict[pgClass].keys()):
                                        if cl not in invalidated['nullAttribute'].keys():
                                            invalidated['nullAttribute'][cl] = dict()
                                        if id not in invalidated['nullAttribute'][cl].keys():
                                            invalidated['nullAttribute'][cl][id] = dict()
                                        if attrList[i] not in invalidated['nullAttribute'][cl][id].keys():
                                            invalidated['nullAttribute'][cl][id][attrList[i]] = dict()
                                        invalidated['nullAttribute'][cl][id][attrList[i]] = value
        return invalidated
    