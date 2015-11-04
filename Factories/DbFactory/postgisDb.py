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
from PyQt4.QtCore import QSettings
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from osgeo import ogr

class PostgisDb(AbstractDb):
    
    def __init__(self):
        super(PostgisDb,self).__init__()
        self.db = QSqlDatabase('QPSQL')
        self.gen = SqlGeneratorFactory().createSqlGenerator(False)
        
    def connectDatabase(self,conn=None):
        if conn.split(':')[0] == 'PG':
            connSplit = conn.split(' ')
            parDict = dict()
            for i in connSplit[1::]:
                par = i.split('=')
                parDict[par[0]]=par[1]
            self.connectDatabaseWithParameters(parDict['host'], parDict['port'], parDict['database'], parDict['user'], parDict['password'])
        else:
            self.connectDatabaseWithQSettings(conn)

    def connectDatabaseWithGui(self):
        return None

    def connectDatabaseWithParameters(self,host,port,database,user,password):
        self.db.setHostName(host)
        self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        self.db.setPassword(password)

    def connectDatabaseWithQSettings(self,name):
        (host, port, database, user, password) = self.getConnectionFromQSettings(name)
        self.db.setHostName(host)
        self.db.setPort(int(port))
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        self.db.setPassword(password)

    def getDatabaseVersion(self):
        self.checkAndOpenDb()
        sqlVersion = self.gen.getEDGVVersion()
        queryVersion =  QSqlQuery(sqlVersion, self.db)
        while queryVersion.next():
            version = queryVersion.value(0)
        return version
    
    def listGeomClassesFromDatabase(self):
        self.checkAndOpenDb()      
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
            layerName = tableSchema+'.'+tableName
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a":
                classList.append(layerName)
        return classList
    
    def listComplexClassesFromDatabase(self):
        self.checkAndOpenDb()        
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
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

    def getConnectionFromQSettings(self, conName):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+conName)
        host = settings.value('host')
        port = settings.value('port')
        database = settings.value('database')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, database, user, password)       

    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)        


    def getStructureDict(self):
        self.checkAndOpenDb()
        classDict = dict()
        sql = self.gen.getStructure(self.getDatabaseVersion())        
        query = QSqlQuery(sql, self.db)
        while query.next():
            className = str(query.value(0))+'.'+str(query.value(1))
            fieldName = str(query.value(2))
            if str(query.value(0)) == 'complexos' or className.split('_')[-1] in ['p','l','a']:
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


    def getNotNullDict(self):
        self.checkAndOpenDb()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb','complexos']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return None
        sql = self.gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, self.db)
        notNullDict = dict()
        while query.next():
            schemaName = str(query.value(0))
            className = str(query.value(1))
            attName = str(query.value(2))
            cl = schemaName+'.'+className
            if cl not in notNullDict.keys():
                notNullDict[cl]=[]
            notNullDict[cl].append(attName)
        return notNullDict

    def getDomainDict(self):
        self.checkAndOpenDb()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb','complexos','dominios']
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Operation not defined for this database version!'))
            return
        sql = self.gen.validateWithDomain(schemaList)
        query = QSqlQuery(sql, self.db)
        classDict = dict()
        domainDict = dict()
        while query.next():
            schemaName = str(query.value(0))
            className = str(query.value(1))
            attName = str(query.value(2))
            domainName = str(query.value(3))
            domainTable = str(query.value(4))
            domainQuery = str(query.value(5))
            cl = schemaName+'.'+className
            query2 = QSqlQuery(domainQuery,self.db)
            while query2.next():
                value = int(query2.value(0))
                classDict = self.utils.buildNestedDict(classDict,[str(cl),str(attName)],[value])
        return classDict
    
    def validateWithOutputDatabaseSchema(self,outputAbstractDb):
        return None

    def translateOGRLayerNameToOutputFormat(self,lyr,ogrOutput):
        if ogrOutput.GetDriver().name == 'SQLite':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return lyr

    def getTableSchema(self,lyr):
        schema = lyr.split('.')[0]
        className = lyr.split('.')[1::]
        return (schema,className)

    #TODO: treat each case (hammer time and don't touch my data)
    def convertToPostgis(self, outputAbstractDb,type=None):
        return None
    
    def convertToSpatialite(self, outputAbstractDb,type=None):
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList) = self.prepareForConversion(outputAbstractDb)
        status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList)
        return status
    
    def translateDSWithDataFix(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, invalidated):
        return None
