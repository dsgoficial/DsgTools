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
from qgis.core import QgsCredentials, QgsMessageLog, QgsDataSourceURI
from osgeo import ogr
from uuid import uuid4
import codecs, os, json

class PostgisDb(AbstractDb):
    def __init__(self):
        '''
        Constructor
        '''
        super(PostgisDb,self).__init__()
        #setting database type to postgresql
        self.db = QSqlDatabase('QPSQL')
        #setting up a sql generator
        self.gen = SqlGeneratorFactory().createSqlGenerator(False)
        
    def getDatabaseName(self):
        '''
        Gets the database name
        '''
        return self.db.databaseName()
    
    def connectDatabase(self,conn=None):
        '''
        Connects to database
        conn: connection parameters. It can be a OGR connection or a QSettings connection
        '''
        if conn.split(':')[0] == 'PG':
            connSplit = conn.split(' ')
            parDict = dict()
            for i in connSplit[1::]:
                par = i.split('=')
                parDict[par[0]]=par[1]
            self.connectDatabaseWithParameters(parDict['host'], parDict['port'], parDict['dbname'], parDict['user'], parDict['password'])
        else:
            self.connectDatabaseWithQSettings(conn)

    def connectDatabaseWithParameters(self, host, port, database, user, password):
        '''
        Connects to database with parameters
        host: host IP
        port: host port
        database: database name
        user: user name
        password: user password
        '''
        self.db.setHostName(host)
        if type(port) != 'int':
            self.db.setPort(int(port))
        else:
            self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        if not password or password == '':
            conInfo = 'host='+host+' port='+port+' dbname='+database
            check = False
            while not check:
                try:
                    (success, user, password) = QgsCredentials.instance().get(conInfo, user, None)
                    if not success:
                        return 
                    self.db.setPassword(password)
                    check = True
                    self.checkAndOpenDb()
                    QgsCredentials.instance().put(conInfo, user, password)
                except:
                    pass
        else:
            self.db.setPassword(password)

    def connectDatabaseWithQSettings(self, name):
        '''
        Connects to database with parameters
        name: QSettings connection name
        '''
        #getting connection parameters from qsettings
        (host, port, database, user, password) = self.getConnectionFromQSettings(name)
        self.db.setHostName(host)
        if type(port) != 'int':
            self.db.setPort(int(port))
        else:
            self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        if not password or password == '':
            conInfo = 'host='+host+' port='+port+' dbname='+database
            check = False
            while not check:
                try:
                    (success, user, password) = QgsCredentials.instance().get(conInfo, user, None)
                    if not success:
                        return 
                    self.db.setPassword(password)
                    check = True
                    self.checkAndOpenDb()
                    QgsCredentials.instance().put(conInfo, user, password)
                except:
                    pass
        else:
            self.db.setPassword(password)

    def getDatabaseVersion(self):
        '''
        Gets the database version
        '''
        self.checkAndOpenDb()
        sql = self.gen.getEDGVVersion()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting database version: ")+query.lastError().text())
        version = '-1'
        while query.next():
            version = query.value(0)
        return version
    
    def listGeomClassesFromDatabase(self):
        '''
        Gets a list with geometry classes from database
        '''
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem listing geom classes: ")+query.lastError().text())
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
            layerName = tableSchema+'.'+tableName
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" \
                or tableName.split("_")[-1] == "a":
                if tableSchema not in ['validation', 'views']:
                    classList.append(layerName)
        return classList
    
    def listComplexClassesFromDatabase(self):
        '''
        Gets a list with complex classes from database
        '''
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem listing complex classes: ")+query.lastError().text())
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
            layerName = tableSchema+'.'+tableName
            if tableSchema == 'complexos':
                classList.append(layerName)
        classList.sort()
        return classList

    def storeConnection(self, server):
        '''
        Stores a connection into QSettings
        '''
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
        '''
        Gets a connection from QSettings
        conName: connection name stored
        '''
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
        '''
        Gets a server configuration from QSettings
        name: server name
        '''
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)

    def getStructureDict(self):
        '''
        Gets database structure according to the edgv version
        '''
        self.checkAndOpenDb()
        classDict = dict()
        sql = self.gen.getStructure(self.getDatabaseVersion())        
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting database structure: ")+query.lastError().text())
        while query.next():
            className = str(query.value(0))+'.'+str(query.value(1))
            fieldName = str(query.value(2))
            if str(query.value(0)) == 'complexos' or className.split('_')[-1] in ['p','l','a']:
                if className not in classDict.keys():
                    classDict[className]=dict()
                classDict[className][fieldName]=fieldName
                if 'geom' in classDict[className].keys():
                    classDict[className]['geom'] = 'GEOMETRY'
                if str(query.value(0)) <> 'complexos' and 'id' in classDict[className].keys():
                    classDict[className]['id'] = 'OGC_FID'
        return classDict
    
    def makeOgrConn(self):
        '''
        Makes a OGR connection string
        '''
        dbName = self.db.databaseName()
        dbUser = self.db.userName()
        dbHost = self.db.hostName()
        dbPass = self.db.password()
        dbPort = str(self.db.port())
        constring = 'PG: dbname=\''+dbName+'\' user=\''+dbUser+'\' host=\''+dbHost+'\' password=\''+dbPass+'\' port='+dbPort
        return constring

    def getNotNullDict(self):
        '''
        Gets a dictionary with all not null fields for the edgv database used
        '''
        self.checkAndOpenDb()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos']
        elif self.getDatabaseVersion() == 'FTer_2a_Ed':
            schemaList = ['pe','ge', 'complexos']
        else:
            QgsMessageLog.logMessage(self.tr('Operation not defined for this database version!'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None
        
        sql = self.gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem executing query: ")+query.lastError().text())
        notNullDict = dict()
        while query.next():
            schemaName = str(query.value(0))
            className = str(query.value(1))
            attName = str(query.value(2))
            cl = schemaName+'.'+className
            if cl not in notNullDict.keys():
                notNullDict[cl] = []
            notNullDict[cl].append(attName)
        return notNullDict

    def getDomainDict(self):
        '''
        Gets the domain dictionary for the edgv database used
        '''
        self.checkAndOpenDb()        
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos', 'dominios']
        elif self.getDatabaseVersion() == 'FTer_2a_Ed':
            schemaList = ['pe','ge', 'complexos']
        else:
            QgsMessageLog.logMessage(self.tr('Operation not defined for this database version!'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return
        
        sql = self.gen.validateWithDomain(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem executing query: ")+query.lastError().text())

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

    def translateAbstractDbLayerNameToOutputFormat(self, lyr, outputAbstractDb):
        '''
        Translates abstractdb layer name to output format
        lyr: layer name that will be translated
        outputAbstractDb: output database
        '''
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return lyr

    def translateOGRLayerNameToOutputFormat(self, lyr, ogrOutput):
        '''
        Translates ogr layer name to output format
        lyr: layer name that will be translated
        ogrOutput: ogr output
        '''
        if ogrOutput.GetDriver().name == 'SQLite':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return lyr

    def getTableSchema(self,lyr):
        '''
        Gets the table schema
        lyr: layer name
        '''
        schema = lyr.split('.')[0]
        className = '_'.join(lyr.split('.')[1::])
        return (schema, className)
    
    def convertToSpatialite(self, outputAbstractDb, type=None):
        '''
        Converts this to a spatialite database
        outputAbstractDb: spatialite output
        type: conversion type
        '''
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict) = self.prepareForConversion(outputAbstractDb)
        status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
        return status
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        '''
        Obtains the link column between complex and aggregated class
        complexClass: complex class name
        aggregatedClass: aggregated class name
        '''
        self.checkAndOpenDb()
        complexClass = complexClass.replace('complexos.', '')
        #query to obtain the link column between the complex and the feature layer
        sql = self.gen.getLinkColumn(complexClass, aggregatedClass)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem obtaining link column: ")+query.lastError().text())
        column_name = ''
        while query.next():
            column_name = query.value(0)
        return column_name

    def loadAssociatedFeatures(self, complex):
        '''
        Loads all the features associated to the complex 
        complex: complex class name
        '''
        self.checkAndOpenDb()
        associatedDict = dict()
        complex = complex.replace('complexos.', '')
        #query to get the possible links to the selected complex in the combobox
        sql = self.gen.getComplexLinks(complex)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem loading associated features: ")+query.lastError().text())

        while query.next():
            #setting the variables
            complex_schema = query.value(0)
            complex = query.value(1)
            aggregated_schema = query.value(2)
            aggregated_class = query.value(3)
            column_name = query.value(4)

            #query to obtain the created complexes
            sql = self.gen.getComplexData(complex_schema, complex)
            complexQuery = QSqlQuery(sql, self.db)
            if not complexQuery.isActive():
                self.db.close()
                raise Exception(self.tr("Problem loading associated features: ")+complexQuery.lastError().text())

            while complexQuery.next():
                complex_uuid = complexQuery.value(0)
                name = complexQuery.value(1)

                if not (complex_uuid and name):
                    continue
                
                associatedDict = self.utils.buildNestedDict(associatedDict, [name, complex_uuid, aggregated_class], [])
                
                #query to obtain the id of the associated feature
                sql = self.gen.getAssociatedFeaturesData(aggregated_schema, aggregated_class, column_name, complex_uuid)
                associatedQuery = QSqlQuery(sql, self.db)
                if not associatedQuery.isActive():
                    self.db.close()
                    raise Exception(self.tr("Problem loading associated features: ")+associatedQuery.lastError().text())

                while associatedQuery.next():
                    ogc_fid = associatedQuery.value(0)
                    associatedDict = self.utils.buildNestedDict(associatedDict, [name, complex_uuid, aggregated_class], [ogc_fid])
        return associatedDict
    
    def isComplexClass(self, className):
        '''
        Checks if a class is a complex class
        className: class name to be checked
        '''
        self.checkAndOpenDb()
        #getting all complex tables
        query = QSqlQuery(self.gen.getComplexTablesFromDatabase(), self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem executing query: ")+query.lastError().text())

        while query.next():
            if query.value(0) == className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        '''
        Disassociates a complex from another complex
        aggregated_class: aggregated class that will be disassociated
        link_column: link column between complex and its aggregated class
        id: complex id (uid) to be disassociated
        '''
        sql = self.gen.disassociateComplexFromComplex(aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())
    
    def getUsers(self):
        '''
        Gets 'this' database users
        '''
        self.checkAndOpenDb()
        ret = []
        
        sql = self.gen.getUsers()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting users: ")+query.lastError().text())

        while query.next():
            ret.append(query.value(0))
            
        ret.sort()
        return ret

    def getUserRelatedRoles(self, username):
        '''
        Gets user roles assigned to 'username'
        username: user name
        '''
        self.checkAndOpenDb()
        installed = []
        assigned = []

        sql = self.gen.getUserRelatedRoles(username)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting user roles: ")+query.lastError().text())

        while query.next():
            rolname = query.value(0)
            usename = query.value(1)
            if not usename:
                installed.append(rolname)
            else:
                assigned.append(rolname)

        installed.sort()
        assigned.sort()
        return installed, assigned
    
    def getRoles(self):
        '''
        Gets roles installed in 'this' database
        '''
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getRoles()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting roles: ")+query.lastError().text())

        while query.next():
            ret.append(query.value(0))

        ret.sort()
        return ret

    def createRole(self, role, dict):
        '''
        Creates a role into this database
        role: role name
        dict: role definitions
        '''
        self.checkAndOpenDb()
        #making this so the instaciated permissions stay with different names
        uuid = str(uuid4()).replace('-', '_')
        role += '_'+uuid

        sql = self.gen.createRole(role, dict)
        split = sql.split(';')
        query = QSqlQuery(self.db)
        
        #try to revoke the permissions
        try:
            self.dropRole(role)
        except:
            pass

        for inner in split:
            if not query.exec_(inner):
                if '42710' in query.lastError().text():
                    #In this case the role is already created (duplicate object error). We just need to proceed executing the grants.
                    continue
                else:
                    raise Exception(self.tr('Problem assigning profile: ') +role+'\n'+query.lastError().text())
    
    def dropRole(self, role):
        '''
        Deletes a role from 'this' database
        role: role name
        '''
        self.checkAndOpenDb()
        sql = self.gen.dropRole(role)
        split = sql.split('#')
        query = QSqlQuery(self.db)

        for inner in split:
            if not query.exec_(inner):
                if '2BP01' in query.lastError().text():
                    #In this case the role is still used by other databases, therefore it shouldn't be dropped.
                    continue
                else:
                    raise Exception(self.tr('Problem removing profile: ') +role+'\n'+query.lastError().text())

    def alterUserPass(self, user, newpassword):
        '''
        Alters the user password
        user: user name
        newpassword: new password
        '''
        self.checkAndOpenDb()
        sql = self.gen.alterUserPass(user, newpassword)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem altering user\'s password: ') +user+'\n'+query.lastError().text())

    def createUser(self, user, password, isSuperUser):
        '''
        Creates a new user
        user: user name
        password: user password
        isSuperUser: bool to define is the newly created user is a super user (i.e a user like 'postgres')
        '''
        self.checkAndOpenDb()
        sql = self.gen.createUser(user, password, isSuperUser)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem creating user: ') +user+'\n'+query.lastError().text())

    def removeUser(self, user):
        '''
        Removes a user
        user: user name
        '''
        self.checkAndOpenDb()
        sql = self.gen.removeUser(user)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem removing user: ') +user+'\n'+query.lastError().text())

    def grantRole(self, user, role):
        '''
        Grants a role to a user
        user: user name
        role: role name
        '''
        self.checkAndOpenDb()
        sql = self.gen.grantRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem granting profile: ') +role+'\n'+query.lastError().text())

    def revokeRole(self, user, role):
        '''
        Revokes a role from the user
        user: user name
        role: role name
        '''
        self.checkAndOpenDb()
        sql = self.gen.revokeRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem revoking profile: ') +role+'\n'+query.lastError().text())

    def getTablesFromDatabase(self):
        '''
        Gets all tables from database
        '''
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting tables from database: ")+query.lastError().text())

        while query.next():
            #table name
            ret.append(query.value(0))

        return ret

    def getRolePrivileges(self, role, dbname):
        '''
        Gets role settings (e.g. what is possible to do with the role)
        role: role name
        dbname: database name
        '''
        self.checkAndOpenDb()
        privilegesDict = dict()
        
        sql = self.gen.getRolePrivileges(role, dbname)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting role privileges: ")+query.lastError().text())
        
        while query.next():
            schema = query.value(3)
            table = query.value(4)
            privilege = query.value(5)
            
            if schema in ['cb', 'public', 'complexos', 'dominios', 'pe', 'ge']:
                privilegesDict = self.utils.buildNestedDict(privilegesDict, [schema, table], [privilege])
            
        permissionsDict = dict()
        for schema in privilegesDict.keys():
            for table in privilegesDict[schema].keys():
                split = table.split('_')
                category = split[0]
                layerName = schema+'.'+table
                
                if schema not in permissionsDict.keys():
                    permissionsDict[schema] = dict()
                    
                if category not in permissionsDict[schema].keys():
                    permissionsDict[schema][category] = dict()

                privileges = privilegesDict[schema][table]
                write = ['DELETE', 'INSERT', 'SELECT', 'UPDATE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']
                if all((permission in privileges for permission in write)):
                    if layerName not in permissionsDict[schema][category]:
                        permissionsDict[schema][category][layerName] = dict()
                        permissionsDict[schema][category][layerName]['read'] = '2'#read yes
                        permissionsDict[schema][category][layerName]['write'] = '2'#write yes
                else:
                    if layerName not in permissionsDict[schema][category]:
                        permissionsDict[schema][category][layerName] = dict()
                        permissionsDict[schema][category][layerName]['read'] = '2'#read yes
                        permissionsDict[schema][category][layerName]['write'] = '0'#write no
                        
        return permissionsDict    

    def getFrameLayerName(self):
        '''
        Gets the frame layer name
        '''
        return 'public.aux_moldura_a'
    
    def getEDGVDbsFromServer(self):
        '''
        Gets edgv databases from 'this' server
        '''
        #Can only be used in postgres database.
        self.checkAndOpenDb()
        query = QSqlQuery(self.gen.getDatabasesFromServer(),self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting EDGV databases: ")+query.lastError().text())

        dbList = []
        
        while query.next():
            dbList.append(query.value(0))
        
        edvgDbList = []
        for database in dbList:
            db = None
            db = QSqlDatabase("QPSQL")
            db.setDatabaseName(database)
            db.setHostName(self.db.hostName())
            db.setPort(self.db.port())
            db.setUserName(self.db.userName())
            db.setPassword(self.db.password())
            if not db.open():
                raise Exception(self.tr("Problem opening EDGV databases: ")+db.lastError().databaseText())

            query2 = QSqlQuery(db)
            if query2.exec_(self.gen.getEDGVVersion()):
                while query2.next():
                    version = query2.value(0)
                    if version:
                        edvgDbList.append((database,version))
        return edvgDbList
    
    def getDbsFromServer(self):
        '''
        Gets databases from 'this' server
        '''
        #Can only be used in postgres database.
        self.checkAndOpenDb()
        query = QSqlQuery(self.gen.getDatabasesFromServer(),self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting databases: ")+query.lastError().text())
        dbList = []
        
        while query.next():
            dbList.append(query.value(0))
        return dbList
    
    def checkSuperUser(self):
        '''
        Checks if the user used to connect to this database is a super user
        '''
        self.checkAndOpenDb()
        query = QSqlQuery(self.db)
        if query.exec_(self.gen.isSuperUser(self.db.userName())):
            query.next()
            value = query.value(0)
            return value
        else:
            self.db.close()
            raise Exception(self.tr("Problem checking user: ")+query.lastError().text())
        return False
    
    def dropDatabase(self, candidateName):
        '''
        Drops a database from server
        candidataName: database name
        '''
        self.checkAndOpenDb()
        if self.checkSuperUser():
            sql = self.gen.dropDatabase(candidateName)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                self.db.close()
                raise Exception(self.tr('Problem dropping database: ') + query.lastError().text())
    
    def createResolvedDomainViews(self, createViewClause, fromClause):
        '''
        Creates a view with all domain values resolved
        createViewClause: sql query to create the view
        fromClause: from sql clause
        '''
        self.checkAndOpenDb()
        if self.checkSuperUser():
            filename = self.getSqlViewFile()
            if filename <> None:
                file = codecs.open(filename, encoding='utf-8', mode="r")
                sql = file.read()
                sql = sql.replace('[VIEW]', createViewClause).replace('[FROM]', fromClause)
                file.close()
                commands = sql.split('#')
                self.db.transaction()
                query = QSqlQuery(self.db)
                for command in commands:
                    if not query.exec_(command):
                        self.db.rollback()
                        self.db.close()
                        raise Exception(self.tr('Problem creating views: ') + query.lastError().text())
                self.db.commit()
                self.db.close()

    def getSqlViewFile(self):
        '''
        Gets the sql view file
        '''
        self.checkAndOpenDb()
        currentPath = os.path.dirname(__file__)
        dbVersion = self.getDatabaseVersion()
        file = None
        if dbVersion == '2.1.3':
            file = os.path.join(currentPath,'..','..','DbTools','PostGISTool', 'sqls', '213', 'views_213.sql')
        if dbVersion == 'FTer_2a_Ed':
            file = os.path.join(currentPath,'..','..','DbTools','PostGISTool', 'sqls', 'FTer_2a_Ed', 'views_edgvFter_2a_Ed.sql')
        return file
    
    def getInvalidGeomRecords(self):
        '''
        Gets invalid geometry data from database
        '''
        self.checkAndOpenDb()
        geomList = self.listClassesWithElementsFromDatabase()
        invalidRecordsList = []
        for lyr in geomList:
            tableSchema, tableName = self.getTableSchema(lyr)
            sql = self.gen.getInvalidGeom(tableSchema, tableName)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.close()
                raise Exception(self.tr("Problem getting invalid geometries: ")+query.lastError().text())
            while query.next():
                featId = query.value(0)
                reason = query.value(1)
                geom = query.value(2)
                invalidRecordsList.append( (tableSchema+'.'+tableName,featId,reason,geom) )
        return invalidRecordsList
    
    def insertFlags(self, flagTupleList, processName):
        '''
        Inserts flags into database
        flagTupleList: flag tuple list
        processName: process name
        '''
        self.checkAndOpenDb()
        srid = self.findEPSG()
        if len(flagTupleList) > 0:
            self.db.transaction()
            query = QSqlQuery(self.db)
            for record in flagTupleList:
                try:
                    dimension = self.getDimension(record[3]) # getting geometry dimension
                except Exception as e:
                    raise e
                sql = self.gen.insertFlagIntoDb(record[0], str(record[1]), record[2], record[3], srid, processName, dimension)
                if not query.exec_(sql):
                    self.db.rollback()
                    self.db.close()
                    raise Exception(self.tr('Problem inserting flags: ') + query.lastError().text())
                self.db.commit()
                self.db.close()
            return len(flagTupleList)
        else:
            return 0
    
    def deleteProcessFlags(self, processName):
        '''
        Deletes flags from database
        processName: process name that will have all flags removed
        '''
        self.checkAndOpenDb()
        sql = self.gen.deleteFlags(processName)
        sqlList = sql.split('#')
        query = QSqlQuery(self.db)
        self.db.transaction()
        for inner in sqlList:
            if not query.exec_(inner):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem deleting flags: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def checkAndCreateValidationStructure(self):
        '''
        Checks if the validation structure is already created, if not it should be created now
        '''
        self.checkAndOpenDb()
        sql = self.gen.checkValidationStructure()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem creating structure: ')+query.lastError().text())
        created = True
        while query.next():
            if query.value(0) == 0:
                created = False
        if not created:
            sqltext = self.gen.createValidationStructure(self.findEPSG())
            sqlList = sqltext.split('#')
            query2 = QSqlQuery(self.db)
            self.db.transaction()
            for sql2 in sqlList:
                if not query2.exec_(sql2):
                    self.db.rollback()
                    self.db.close()
                    raise Exception(self.tr('Problem creating structure: ') + query.lastError().text())
            self.db.commit()
            self.db.close()
    
    def getValidationStatus(self, processName):
        '''
        Gets the validation status for a specific process
        processName: process name
        '''
        self.checkAndOpenDb()
        sql = self.gen.validationStatus(processName)
        query = QSqlQuery(sql,self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def getValidationStatusText(self, processName):
        '''
        Gets the validation message text for a specific process
        processName: process name
        '''
        self.checkAndOpenDb()
        sql = self.gen.validationStatusText(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def setValidationProcessStatus(self, processName, log, status):
        '''
        Sets the validation status for a specific process
        processName: process name
        '''
        self.checkAndOpenDb()
        sql = self.gen.setValidationStatusQuery(processName, log, status)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem setting status: ') + query.lastError().text())
    
    def getRunningProc(self):
        '''
        Gets the active running process into database
        '''
        self.checkAndOpenDb()
        sql = self.gen.getRunningProc()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem getting running process: ') + query.lastError().text()) 
        while query.next():
            processName = query.value(0)
            status = query.value(1)
            if status == 3:
                return processName
        return None
    
    def isLyrInDb(self, lyr):
        '''
        Checks if a layer is in the database
        '''
        candidateUri = QgsDataSourceURI(lyr.dataProvider().dataSourceUri())
        candidateHost = candidateUri.host()
        candidatePort = int(candidateUri.port())
        candidateDb = candidateUri.database()
        if self.db.hostName() == candidateHost and self.db.port() == candidatePort and self.db.databaseName() == candidateDb:
            return True
        else:
            return False
        
    def testSpatialRule(self, class_a, necessity, predicate_function, class_b, min_card, max_card, rule):
        '''
        Tests spatial predicates to check whether a rule is broken
        '''
        self.checkAndOpenDb()
        sql = self.gen.testSpatialRule(class_a, necessity, predicate_function, class_b, min_card, max_card)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem testing spatial rule: ') + query.lastError().text()) 
        ret = []
        while query.next():
            feat_id = query.value(0)
            reason = 'Feature id %s from %s violates rule %s %s' % (feat_id, class_a, rule, class_b)
            geom = query.value(1)
            ret.append((class_a, feat_id, reason, geom))
        return ret

    def getDimension(self, geom):
        '''
        Gets geometry's dimension
        geom: geometry tested
        '''
        self.checkAndOpenDb()
        sql = self.gen.getDimension(geom)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr('Problem getting dimension: ') + query.lastError().text()) 
        dimension = 0
        while query.next():
            dimension = query.value(0)
        return dimension
    
    def getExplodeCandidates(self):
        '''
        Gets multi geometries (i.e number of parts > 1) that will be deaggregated later
        '''
        self.checkAndOpenDb()
        explodeDict = dict()
        classesWithElem = self.listClassesWithElementsFromDatabase()
        for cl in classesWithElem:
            sql= self.gen.getMulti(cl)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.close()
                raise Exception(self.tr('Problem exploding geometries: ') + query.lastError().text())
            idList = []
            while query.next():
                idList.append(query.value(0))
            if len(idList) > 0:
                explodeDict = self.utils.buildNestedDict(explodeDict, [cl], idList)
        return explodeDict

    def getURI(self, table, useOnly = True, geomColumn = 'geom'):
        '''
        Gets tabel URI
        table: table name
        useOnly: bool to determine if 'from only' should be used
        geomColumn: geometry column
        '''
        schema, layer_name = self.getTableSchema(table)

        host = self.db.hostName()
        port = self.db.port()
        database = self.db.databaseName()
        user = self.db.userName()
        password = self.db.password()
        
        if useOnly:
            sql = self.gen.loadLayerFromDatabase(table)
        else:
            sql = self.gen.loadLayerFromDatabaseUsingInh(table)
        
        uri = QgsDataSourceURI()
        uri.setConnection(str(host),str(port), str(database), str(user), str(password))
        uri.setDataSource(schema, layer_name, geomColumn, sql, 'id')
        uri.disableSelectAtId(True)
        
        return uri
    
    def getDuplicatedGeomRecords(self, classesWithGeom):
        '''
        Gets duplicated records
        classesWithGeom: list of classes with geomtries
        '''
        self.checkAndOpenDb()
        duplicatedDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            if tableSchema not in ('validation'):
                sql = self.gen.getDuplicatedGeom(tableSchema, tableName)
                query = QSqlQuery(sql, self.db)
                if not query.isActive():
                    self.db.close()
                    raise Exception(self.tr('Problem getting duplicated geometries: ') + query.lastError().text())
                while query.next():
                    duplicatedDict = self.utils.buildNestedDict(duplicatedDict, [cl,query.value(0)], query.value(2))
        return duplicatedDict

    def getSmallAreasRecords(self,classesWithGeom, tol):
        '''
        Gets duplicated records
        classesWithGeom: list of classes with geometries
        '''
        self.checkAndOpenDb()
        smallAreasDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getSmallAreas(tableSchema, tableName, tol)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem getting small areas: ') + query.lastError().text())
            while query.next():
                smallAreasDict = self.utils.buildNestedDict(smallAreasDict, [cl,query.value(0)], query.value(1))
        return smallAreasDict

    def getSmallLinesRecords(self,classesWithGeom, tol):
        '''
        Gets small lines records 
        tol: tolerance
        '''
        self.checkAndOpenDb()
        smallLinesDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getSmallLines(tableSchema, tableName, tol)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.close()
                raise Exception(self.tr('Problem getting small lines: ') + query.lastError().text())
            while query.next():
                smallLinesDict = self.utils.buildNestedDict(smallLinesDict, [cl,query.value(0)], query.value(1))
        return smallLinesDict

    def getVertexNearEdgesRecords(self, tableSchema, tableName, tol):
        '''
        Gets vertexes near edges. These vertexes are problematic and should be treated
        tableSchema: table schema
        tableName: table name
        tol: tolerance
        '''
        self.checkAndOpenDb()
        result = []
        sql = self.gen.prepareVertexNearEdgesStruct(tableSchema, tableName)
        sqlList = sql.split('#')
        self.db.transaction()
        for sql2 in sqlList:
            query = QSqlQuery(self.db)
            if not query.exec_(sql2):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem preparing auxiliary structure: ') + query.lastError().text())

        epsg = self.findEPSG()
        sql = self.gen.getVertexNearEdgesStruct(epsg, tol)
        query = QSqlQuery(sql,self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting vertex near edges: ') + query.lastError().text())
        while query.next():
            id = query.value(0)
            geom = query.value(1)
            result.append((id,geom))
        self.db.commit()
        self.db.close()
        return result

    def removeFeatures(self, cl, idList):
        '''
        Removes features from class
        cl: class name
        idList: id list to be removes
        '''
        self.checkAndOpenDb()
        tableSchema, tableName = self.getTableSchema(cl)
        sql = self.gen.deleteFeatures(tableSchema, tableName, idList)
        query = QSqlQuery(self.db)
        self.db.transaction()
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem deleting features from ')+cl+': '+ query.lastError().text())
        self.db.commit()
        self.db.close()
        return len(idList)

    def getNotSimpleRecords(self,classesWithGeom):
        self.checkAndOpenDb()
        notSimpleDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getNotSimple(tableSchema, tableName)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem getting not simple geometries: ') + query.lastError().text())
            while query.next():
                notSimpleDict = self.utils.buildNestedDict(notSimpleDict, [cl,query.value(0)], query.value(1))
        return notSimpleDict

    def getOutOfBoundsAnglesRecords(self, tableSchema, tableName, tol):
        self.checkAndOpenDb()
        result = []
        sql = self.gen.getOutofBoundsAngles(tableSchema, tableName, tol)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting not out of bounds angles: ') + query.lastError().text())
        while query.next():
            id = query.value(0)
            geom = query.value(1)
            result.append((id, geom))
        return result

    def getFlagsDictByProcess(self, processName):
        self.checkAndOpenDb()
        flagsDict = dict()
        sql = self.gen.getFlagsByProcess(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting flags dict: ') + query.lastError().text())
        while query.next():
            cl = query.value(0)
            id = query.value(1)
            flagsDict = self.utils.buildNestedDict(flagsDict, [cl], [str(id)])
        return flagsDict
    
    def forceValidity(self, cl, idList):
        self.checkAndOpenDb()
        tableSchema, tableName = self.getTableSchema(cl)
        srid = self.findEPSG()
        sql = self.gen.forceValidity(tableSchema, tableName, idList, srid)
        query = QSqlQuery(self.db)
        self.db.transaction()
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem forcing validity of features from ')+cl+': '+ query.lastError().text())
        self.db.commit()
        self.db.close()        
        return len(idList)
    
    def getTableExtent(self, tableSchema, tableName):
        self.checkAndOpenDb()
        sql = self.gen.getTableExtent(tableSchema, tableName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting table extent: ') + query.lastError().text())
        
        extent = None
        while query.next():
            xmin = query.value(0)
            xmax = query.value(1)
            ymin = query.value(2)
            ymax = query.value(3)
            extent = (xmin, xmax, ymin, ymax)
        return extent

    def getOrphanGeomTables(self):
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting orphan tables: ') + query.lastError().text())
        result = []
        while query.next():
            result.append(query.value(0))
        return result

    def getOrphanGeomTablesWithElements(self):
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting orphan tables: ') + query.lastError().text())
        result = []
        while query.next():
            orphanCandidate = query.value(0)
            sql2 = self.gen.getOrphanTableElementCount(orphanCandidate)
            query2 = QSqlQuery(sql2, self.db)
            if not query2.isActive():
                raise Exception(self.tr('Problem counting orphan table: ') + query2.lastError().text())
            while query2.next():
                if query2.value(0):
                    result.append(query.value(0))
        return result
    
    def updateGeometries(self, tableSchema, tableName, tuplas, epsg):
        self.checkAndOpenDb()
        sqls = self.gen.updateOriginalTable(tableSchema, tableName, tuplas, epsg)
        query = QSqlQuery(self.db)
        self.db.transaction()
        sqlDel = self.gen.deleteFeaturesNotIn(tableSchema, tableName, tuplas.keys())
        for sql in sqls:
            if not query.exec_(sql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem updating geometries: ') + query.lastError().text())
        query2 = QSqlQuery(self.db)
        if not query2.exec_(sqlDel):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem deleting geometries: ') + query.lastError().text())            
        self.db.commit()
        self.db.close()    
    
    def checkCentroidAuxStruct(self):
        self.checkAndOpenDb()
        sql = self.gen.checkCentroidAuxStruct()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem checking structure: ')+query.lastError().text())
        while query.next():
            if query.value(0) == None:
                return False
        return True
    
    def createCentroidAuxStruct(self,earthCoverageClasses):
        self.checkAndOpenDb()
        srid = self.findEPSG()
        self.db.transaction()
        for cl in earthCoverageClasses:
            table_schema, table_name = self.getTableSchema(cl)
            sqltext = self.gen.createCentroidColumn(table_schema, table_name, srid)
            sqlList = sqltext.split('#')
            query = QSqlQuery(self.db)
            for sql2 in sqlList:
                if not query.exec_(sql2):
                    self.db.rollback()
                    self.db.close()
                    raise Exception(self.tr('Problem creating centroid structure: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def checkAndCreateCentroidAuxStruct(self,earthCoverageClasses):
        created = self.checkCentroidAuxStruct()
    
    def getEarthCoverageClasses(self):
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting earth coverage tables: ') + query.lastError().text())
        result = []
        while query.next():
            result.append(query.value(0))
        return result

    def getEarthCoverageDict(self):
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting earth coverage structure: ') + query.lastError().text())
        while query.next():
            return query.value(0)

    def setEarthCoverageDict(self,textDict):
        self.checkAndOpenDb()
        sql = self.gen.setEarthCoverageDict(textDict)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem setting earth coverage structure: ') + query.lastError().text())
        self.db.commit()
        self.db.close()

    def dropCentroids(self, classList):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sql = self.gen.dropCentroid(cl)
            if not query.exec_(sql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem dropping centroids: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def rollbackEarthCoverage(self, classList):
        try:
            self.dropCentroids(classList)
            self.setEarthCoverageDict(None)
        except Exception as e:
            raise e

    def getEarthCoverageCentroids(self):
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageCentroids()
        query = QSqlQuery(sql, self.db)
        centroidList = []
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting earth coverage structure: ') + query.lastError().text())
        while query.next():
            centroidList.append(query.value(0))
        return centroidList

    def getWhoAmI(self, cl, id):
        """
        cl: class with schema
        """
        self.checkAndOpenDb()
        sql = self.gen.getWhoAmI(cl, id)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting class name: ') + query.lastError().text())
        while query.next():
            return query.value(0)
    
    def snapToGrid(self, classList, tol):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sql = self.gen.snapToGrid(cl, tol)
            if not query.exec_(sql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem snapping to grid: ') + query.lastError().text())
        self.db.commit()
        self.db.close()

    def snapLinesToFrame(self, classList, tol):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sqls = self.gen.snapLinesToFrame(cl, tol)
            for sql in sqls.split('#'):
                if not query.exec_(sql):
                    self.db.rollback()
                    self.db.close()
                    raise Exception(self.tr('Problem snapping to frame: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def densifyFrame(self, classList):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sql = self.gen.densifyFrame(cl)
            if not query.exec_(sql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem densifying frame: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
        
    def recursiveSnap(self, classList, tol):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.makeRecursiveSnapFunction()
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem creating recursive snap function: ') + query.lastError().text())
        for cl in classList:
            sql = self.gen.executeRecursiveSnap(cl, tol)
            if not query.exec_(sql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem snapping class: ') + query.lastError().text())
        self.db.commit()
        self.db.close()

    def removeFeatureFlags(self, layer, featureId, processName):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.deleteFeatureFlagsFromDb(layer, str(featureId), processName)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem deleting flag: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
        
    def removeEmptyGeometries(self, layer):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.removeEmptyGeomtriesFromDb(layer)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem removing empty geometries: ') + query.lastError().text())
        self.db.commit()
        self.db.close()