# -*- coding: utf-8 -*-
"""@package docstring
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
from qgis.core import QgsCredentials, QgsMessageLog, QgsDataSourceURI, QgsFeature, QgsVectorLayer, QgsField
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii, re
import psycopg2
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class PostgisDb(AbstractDb):
    def __init__(self):
        """
        Constructor
        """
        super(PostgisDb, self).__init__()
        #setting database type to postgresql
        self.db = QSqlDatabase('QPSQL')
        #setting up a sql generator
        self.gen = SqlGeneratorFactory().createSqlGenerator(False)

    def getDatabaseParameters(self):
        """
        Gets (host, port, user, password)
        """
        return (self.db.hostName(), self.db.port(), self.db.userName(), self.db.password())

    def getDatabaseName(self):
        """
        Gets the database name
        """
        return self.db.databaseName()

    def getHostName(self):
        return str(self.db.hostName())

    def connectDatabase(self, conn=None):
        """
        Connects to database
        conn: connection parameters. It can be a OGR connection or a QSettings connection
        """
        if conn.split(':')[0] == 'PG':
            connSplit = conn.split(' ')
            parDict = dict()
            for i in connSplit[1::]:
                par = i.split('=')
                parDict[par[0]] = par[1]
            self.connectDatabaseWithParameters(parDict['host'], parDict['port'], parDict['dbname'], parDict['user'], parDict['password'])
        else:
            self.connectDatabaseWithQSettings(conn)

    def connectDatabaseWithParameters(self, host, port, database, user, password):
        """
        Connects to database with parameters
        host: host IP
        port: host port
        database: database name
        user: user name
        password: user password
        """
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
        """
        Connects to database with parameters
        name: QSettings connection name
        """
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
        """
        Gets the database version
        """
        self.checkAndOpenDb()
        sql = self.gen.getEDGVVersion()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            return 'Non_EDGV'
        version = '-1'
        while query.next():
            version = query.value(0)
        return version

    def listGeomClassesFromDatabase(self, primitiveFilter = [], withElements = False, excludeViews = True, getGeometryColumn = False):
        """
        Gets a list with geometry classes from database
        returns dict if getGeometryColumn = True
        return list if getGeometryColumn = False
        """
        self.checkAndOpenDb()
        classList = []
        schemaList = [i for i in self.getGeomSchemaList() if i not in ['validation', 'views']]
        #primitiveFilter building
        dbPrimitiveList = []
        if len(primitiveFilter) > 0:
            for primitive in primitiveFilter:
                if primitive == 'p':
                    dbPrimitiveList.append('POINT')
                    dbPrimitiveList.append('MULTIPOINT')
                if primitive == 'l':
                    dbPrimitiveList.append('LINESTRING')
                    dbPrimitiveList.append('MULTILINESTRING')
                if primitive == 'a':
                    dbPrimitiveList.append('POLYGON')
                    dbPrimitiveList.append('MULTIPOLYGON')
        sql = self.gen.getGeomTables(schemaList, dbPrimitiveList = dbPrimitiveList, excludeViews = excludeViews, geomColumn = getGeometryColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem listing geom classes: ")+query.lastError().text())
        localList = []
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
            layerName = tableSchema+'.'+tableName
            geometryColumn = ''
            if getGeometryColumn:
                geometryColumn = query.value(2)
            localList.append({'schema':tableSchema, 'tableName':tableName, 'layerName':layerName, 'geometryColumn':geometryColumn})
        #remove possible duplicates to filter layers with elements
        layerNameList = []
        for i in localList:
            if i['layerName'] not in layerNameList:
                layerNameList.append(i['layerName'])
        if withElements:
            listWithElements = self.getLayersWithElementsV2(layerNameList)
            partialTagList = [i for i in localList if i['tableName'] in listWithElements]
        else:
            partialTagList = localList
        if not getGeometryColumn:
            classList = [i['layerName'] for i in partialTagList]
        else:
            classList = partialTagList
        return classList

    def listComplexClassesFromDatabase(self):
        """
        Gets a list with complex classes from database
        """
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        Stores a connection into QSettings
        """
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
        """
        Gets a connection from QSettings
        conName: connection name stored
        """
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
        """
        Gets a server configuration from QSettings
        name: server name
        """
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)

    def getStructureDict(self):
        """
        Gets database structure according to the edgv version
        """
        self.checkAndOpenDb()
        classDict = dict()
        sql = self.gen.getStructure(self.getDatabaseVersion())        
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        Makes a OGR connection string
        """
        dbName = self.db.databaseName()
        dbUser = self.db.userName()
        dbHost = self.db.hostName()
        dbPass = self.db.password()
        dbPort = str(self.db.port())
        constring = 'PG: dbname=\''+dbName+'\' user=\''+dbUser+'\' host=\''+dbHost+'\' password=\''+dbPass+'\' port='+dbPort
        return constring

    def getNotNullDict(self):
        """
        Gets a dictionary with all not null fields for the edgv database used
        """
        self.checkAndOpenDb()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos']
        elif self.getDatabaseVersion() == '3.0':
            schemaList = ['edgv', 'complexos']
        elif self.getDatabaseVersion() == 'FTer_2a_Ed':
            schemaList = ['pe','ge', 'complexos']
        else:
            QgsMessageLog.logMessage(self.tr('Operation not defined for this database version!'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None
        
        sql = self.gen.getNotNullFields(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        SHOULD BE DEPRECATED OR IN FOR A MAJOR REFACTORY!!!!!
        Gets the domain dictionary for the edgv database used
        """
        self.checkAndOpenDb()        
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos', 'dominios']
        elif self.getDatabaseVersion() == '3.0':
            schemaList = ['edgv', 'complexos', 'dominios']
        elif self.getDatabaseVersion() == 'FTer_2a_Ed':
            schemaList = ['pe','ge', 'complexos']
        else:
            QgsMessageLog.logMessage(self.tr('Operation not defined for this database version!'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return
        
        sql = self.gen.validateWithDomain(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        Translates abstractdb layer name to output format
        lyr: layer name that will be translated
        outputAbstractDb: output database
        """
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return lyr

    def translateOGRLayerNameToOutputFormat(self, lyr, ogrOutput):
        """
        Translates ogr layer name to output format
        lyr: layer name that will be translated
        ogrOutput: ogr output
        """
        if ogrOutput.GetDriver().name == 'SQLite':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return lyr

    def getTableSchema(self,lyr):
        """
        DEPRECATED
        Gets the table schema
        lyr: layer name
        """
        schema = lyr.split('.')[0]
        className = '_'.join(lyr.split('.')[1::])
        return (schema, className)
    
    def convertToSpatialite(self, outputAbstractDb, type=None):
        """
        Converts this to a spatialite database
        outputAbstractDb: spatialite output
        type: conversion type
        """
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict) = self.prepareForConversion(outputAbstractDb)
        status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
        return status
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        """
        Obtains the link column between complex and aggregated class
        complexClass: complex class name
        aggregatedClass: aggregated class name
        """
        self.checkAndOpenDb()
        complexClass = complexClass.replace('complexos.', '')
        #query to obtain the link column between the complex and the feature layer
        sql = self.gen.getLinkColumn(complexClass, aggregatedClass)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem obtaining link column: ")+query.lastError().text())
        column_name = ''
        while query.next():
            column_name = query.value(0)
        return column_name

    def loadAssociatedFeatures(self, complex):
        """
        Loads all the features associated to the complex 
        complex: complex class name
        """
        self.checkAndOpenDb()
        associatedDict = dict()
        complex = complex.replace('complexos.', '')
        #query to get the possible links to the selected complex in the combobox
        sql = self.gen.getComplexLinks(complex)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
                    raise Exception(self.tr("Problem loading associated features: ")+associatedQuery.lastError().text())

                while associatedQuery.next():
                    ogc_fid = associatedQuery.value(0)
                    associatedDict = self.utils.buildNestedDict(associatedDict, [name, complex_uuid, aggregated_class], [ogc_fid])
        return associatedDict
    
    def isComplexClass(self, className):
        """
        Checks if a class is a complex class
        className: class name to be checked
        """
        self.checkAndOpenDb()
        #getting all complex tables
        query = QSqlQuery(self.gen.getComplexTablesFromDatabase(), self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem executing query: ")+query.lastError().text())

        while query.next():
            if query.value(0) == className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        """
        Disassociates a complex from another complex
        aggregated_class: aggregated class that will be disassociated
        link_column: link column between complex and its aggregated class
        id: complex id (uid) to be disassociated
        """
        sql = self.gen.disassociateComplexFromComplex(aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())
    
    def getUsers(self):
        """
        Gets 'this' database users
        """
        self.checkAndOpenDb()
        ret = []
        
        sql = self.gen.getUsers()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting users: ")+query.lastError().text())

        while query.next():
            ret.append(query.value(0))
            
        ret.sort()
        return ret

    def getUserRelatedRoles(self, username):
        """
        Gets user roles assigned to 'username'
        username: user name
        """
        self.checkAndOpenDb()
        installed = []
        assigned = []

        sql = self.gen.getUserRelatedRoles(username)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        Gets roles installed in 'this' database
        """
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getRoles()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting roles: ")+query.lastError().text())

        while query.next():
            ret.append(query.value(0))

        ret.sort()
        return ret

    def createRole(self, role, roleDict, permissionManager = False):
        """
        Creates a role into this database
        role: role name
        dict: role definitions
        """
        self.checkAndOpenDb()
        #making this so the instaciated permissions stay with different names
        uuid = str(uuid4()).replace('-', '_')
        role += '_'+uuid

        sql = self.gen.createRole(role, roleDict)
        split = sql.split(';')
        query = QSqlQuery(self.db)
        
        if permissionManager:
            if not query.exec_(sql):
                raise Exception(self.tr('Problem assigning profile: ') +role+'\n'+query.lastError().text())
            return role

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
        """
        Deletes a role from 'this' database
        role: role name
        """
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
        """
        Alters the user password
        user: user name
        newpassword: new password
        """
        self.checkAndOpenDb()
        sql = self.gen.alterUserPass(user, newpassword)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem altering user\'s password: ') +user+'\n'+query.lastError().text())

    def createUser(self, user, password, isSuperUser):
        """
        Creates a new user
        user: user name
        password: user password
        isSuperUser: bool to define is the newly created user is a super user (i.e a user like 'postgres')
        """
        self.checkAndOpenDb()
        sql = self.gen.createUser(user, password, isSuperUser)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem creating user: ') +user+'\n'+query.lastError().text())

    def removeUser(self, user):
        """
        Removes a user
        user: user name
        """
        self.checkAndOpenDb()
        sql = self.gen.removeUser(user)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem removing user: ') +user+'\n'+query.lastError().text())

    def grantRole(self, user, role):
        """
        Grants a role to a user
        user: user name
        role: role name
        """
        self.checkAndOpenDb()
        sql = self.gen.grantRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem granting profile: ') +role+'\n'+query.lastError().text())

    def revokeRole(self, user, role):
        """
        Revokes a role from the user
        user: user name
        role: role name
        """
        self.checkAndOpenDb()
        sql = self.gen.revokeRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem revoking profile: ') +role+'\n'+query.lastError().text())

    def getTablesFromDatabase(self):
        """
        Gets all tables from database
        """
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting tables from database: ")+query.lastError().text())

        while query.next():
            #table name
            ret.append(query.value(0))

        return ret

    def getRolePrivileges(self, role, dbname):
        """
        Gets role settings (e.g. what is possible to do with the role)
        role: role name
        dbname: database name
        """
        self.checkAndOpenDb()
        privilegesDict = dict()
        
        sql = self.gen.getRolePrivileges(role, dbname)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
        """
        Gets the frame layer name
        """
        return 'public.aux_moldura_a'
    
    def getEDGVDbsFromServer(self, parentWidget = None):
        """
        Gets edgv databases from 'this' server
        """
        #Can only be used in postgres database.
        self.checkAndOpenDb()
        query = QSqlQuery(self.gen.getDatabasesFromServer(),self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting EDGV databases: ")+query.lastError().text())

        dbList = []
        
        while query.next():
            dbList.append(query.value(0))
        
        edvgDbList = []
        if parentWidget:
            progress = ProgressWidget(1,len(dbList),self.tr('Reading selected databases... '), parent = parentWidget)
            progress.initBar()
        for database in dbList:
            db = None
            db = QSqlDatabase("QPSQL")
            db.setDatabaseName(database)
            db.setHostName(self.db.hostName())
            db.setPort(self.db.port())
            db.setUserName(self.db.userName())
            db.setPassword(self.db.password())
            if not db.open():
                raise Exception(self.tr("Problem opening databases: ")+db.lastError().databaseText())

            query2 = QSqlQuery(db)
            if query2.exec_(self.gen.getGeometryTablesCount()):
                while query2.next():
                    count = query2.value(0)
                    if count > 0:
                        query3 = QSqlQuery(db)
                        if query3.exec_(self.gen.getEDGVVersion()):
                            while query3.next():
                                version = query3.value(0)
                                if version:
                                    edvgDbList.append((database,version))
                                else:
                                    edvgDbList.append((database,'Non_EDGV'))
                        else:
                            edvgDbList.append((database,'Non_EDGV'))
            if parentWidget:
                progress.step()
        return edvgDbList
    
    def getDbsFromServer(self):
        """
        Gets databases from 'this' server
        """
        #Can only be used in postgres database.
        self.checkAndOpenDb()
        query = QSqlQuery(self.gen.getDatabasesFromServer(),self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting databases: ")+query.lastError().text())
        dbList = []
        
        while query.next():
            dbList.append(query.value(0))
        return dbList
    
    def checkSuperUser(self):
        """
        Checks if the user used to connect to this database is a super user
        """
        self.checkAndOpenDb()
        query = QSqlQuery(self.db)
        if query.exec_(self.gen.isSuperUser(self.db.userName())):
            query.next()
            value = query.value(0)
            return value
        else:
            raise Exception(self.tr("Problem checking user: ")+query.lastError().text())
        return False
    
    def checkTemplateImplementationVersion(self, edgvVersion = None):
        """
        Returns True if templateSql version is larger than installed template
        Works when abstractDb is connected to the template
        """
        if not edgvVersion:
            edgvVersion = self.getDatabaseVersion()
        templateName = self.getTemplateName(edgvVersion)
        fileImplementationVersion = self.getImplementationVersionFromFile(edgvVersion)
        templateImplementationVersion = self.getImplementationVersion()
        if templateImplementationVersion < fileImplementationVersion:
            return True
        else:
            return False
    
    def getImplementationVersion(self):
        """
        Returns implementation version
        """
        self.checkAndOpenDb()
        sql = self.gen.getImplementationVersion()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting implementation version: ') + query.lastError().text()) 
        while query.next():
            return query.value(0)
    
    def dropDatabase(self, candidateName, dropTemplate = False):
        """
        Drops a database from server
        candidataName: database name
        """
        self.checkAndOpenDb()
        if self.checkSuperUser():
            if dropTemplate:
                self.setDbAsTemplate(dbName = candidateName, setTemplate = False)
            self.dropAllConections(candidateName)
            sql = self.gen.dropDatabase(candidateName)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                raise Exception(self.tr('Problem dropping database: ') + query.lastError().text())
        else:
            raise Exception(self.tr('Problem dropping database: user must have permission for that.'))
    
    def createResolvedDomainViews(self, createViewClause, fromClause, useTransaction = True):
        """
        Creates a view with all domain values resolved
        createViewClause: sql query to create the view
        fromClause: from sql clause
        """
        self.checkAndOpenDb()
        if self.checkSuperUser():
            filename = self.getSqlViewFile()
            if filename <> None:
                file = codecs.open(filename, encoding='utf-8', mode="r")
                sql = file.read()
                sql = sql.replace('[VIEW]', createViewClause).replace('[FROM]', fromClause)
                file.close()
                commands = sql.split('#')
                commands = [i for i in sql.split('#') if i != '']
                if useTransaction:
                    self.db.transaction()
                query = QSqlQuery(self.db)
                for command in commands:
                    if not query.exec_(command):
                        if useTransaction:
                            self.db.rollback() 
                        raise Exception(self.tr('Problem creating views: ') + query.lastError().text())
                if useTransaction:
                    self.db.commit()
                
    def getSqlViewFile(self):
        """
        Gets the sql view file
        """
        self.checkAndOpenDb()
        currentPath = os.path.dirname(__file__)
        dbVersion = self.getDatabaseVersion()
        file = None
        if dbVersion == '2.1.3':
            file = os.path.join(currentPath,'..','..','DbTools','PostGISTool', 'sqls', '213', 'views_213.sql')
        if dbVersion == 'FTer_2a_Ed':
            file = os.path.join(currentPath,'..','..','DbTools','PostGISTool', 'sqls', 'FTer_2a_Ed', 'views_edgvFter_2a_Ed.sql')
        return file
    
    def getInvalidGeomRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets invalid geometry data from database
        """
        self.checkAndOpenDb()
        invalidRecordsList = []
        tableSchema, tableName = self.getTableSchema(cl)
        sql = self.gen.getInvalidGeom(tableSchema, tableName, geometryColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting invalid geometries: ")+query.lastError().text())
        while query.next():
            featId = query.value(0)
            reason = query.value(1)
            geom = query.value(2)
            invalidRecordsList.append( (featId, reason, geom) )
        return invalidRecordsList
    
    def insertFlags(self, flagTupleList, processName, useTransaction = True):
        """
        Inserts flags into database
        flagTupleList: flag tuple list
        processName: process name
        """
        self.checkAndOpenDb()
        if len(flagTupleList) > 0:
            if useTransaction:
                self.db.transaction()
            query = QSqlQuery(self.db)
            for record in flagTupleList:
                try:
                    dimension = self.getDimension(record[3]) # getting geometry dimension
                except Exception as e:
                    raise e
                # specific EPSG search
                flagSRID = self.findEPSG(parameters={'tableSchema':'validation', 'tableName':'aux_flags_validacao_p', 'geometryColumn':'geom'})
                try:
                    tableSchema, tableName = record[0].split('.')
                    parameters = {'tableSchema':tableSchema, 'tableName':tableName, 'geometryColumn':record[4]}
                    srid = self.findEPSG(parameters=parameters)
                except:
                    srid = flagSRID
                #actual flag insertion
                sql = self.gen.insertFlagIntoDb(record[0], record[1], record[2], record[3], srid, processName, dimension, record[4], flagSRID)
                if not query.exec_(sql):
                    if useTransaction:
                        self.db.rollback()
                    raise Exception(self.tr('Problem inserting flags: ') + query.lastError().text())
            if useTransaction:
                self.db.commit()
            return len(flagTupleList)
        else:
            return 0
    
    def deleteProcessFlags(self, processName=None, className=None, flagId=None):
        """
        Deletes flags from database
        processName: process name that will have all flags removed
        className: class name that will have all flags removed
        """
        self.checkAndOpenDb()
        sql = self.gen.deleteFlags(processName = processName, className = className, flagId = flagId)
        sqlList = sql.split('#')
        query = QSqlQuery(self.db)
        self.db.transaction()
        for inner in sqlList:
            if not query.exec_(inner):
                self.db.rollback()
                raise Exception(self.tr('Problem deleting flags: ') + query.lastError().text())
        self.db.commit()
            
    def checkAndCreateValidationStructure(self, useTransaction = True):
        """
        Checks if the validation structure is already created, if not it should be created now
        """
        self.checkAndOpenDb()
        sql = self.gen.checkValidationStructure()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem creating structure: ')+query.lastError().text())
        created = True
        while query.next():
            if query.value(0) == 0:
                created = False
        if not created:
            sqltext = self.gen.createValidationStructure(self.findEPSG())
            sqlList = sqltext.split('#')
            query2 = QSqlQuery(self.db)
            if useTransaction:
                self.db.transaction()
            for sql2 in sqlList:
                if not query2.exec_(sql2):
                    if useTransaction:
                        self.db.rollback()
                    raise Exception(self.tr('Problem creating structure: ') + query.lastError().text())
            if useTransaction:
                self.db.commit()
                
    def getValidationStatus(self, processName):
        """
        Gets the validation status for a specific process
        processName: process name
        """
        self.checkAndOpenDb()
        sql = self.gen.validationStatus(processName)
        query = QSqlQuery(sql,self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def getValidationStatusText(self, processName):
        """
        Gets the validation message text for a specific process
        processName: process name
        """
        self.checkAndOpenDb()
        sql = self.gen.validationStatusText(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def setValidationProcessStatus(self, processName, log, status):
        """
        Sets the validation status for a specific process
        processName: process name
        """
        self.checkAndOpenDb()
        sql = self.gen.setValidationStatusQuery(processName, log, status)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem setting status: ') + query.lastError().text())
    
    def getRunningProc(self):
        """
        Gets the active running process into database
        """
        self.checkAndOpenDb()
        sql = self.gen.getRunningProc()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting running process: ') + query.lastError().text())
        while query.next():
            processName = query.value(0)
            status = query.value(1)
            if status == 3:
                return processName
        return None
    
    def isLyrInDb(self, lyr):
        """
        Checks if a layer is in the database
        """
        candidateUri = QgsDataSourceURI(lyr.dataProvider().dataSourceUri())
        candidateHost = candidateUri.host()
        candidatePort = int(candidateUri.port())
        candidateDb = candidateUri.database()
        if self.db.hostName() == candidateHost and self.db.port() == candidatePort and self.db.databaseName() == candidateDb:
            return True
        else:
            return False
        
    def testSpatialRule(self, class_a, necessity, predicate_function, class_b, min_card, max_card, rule, aKeyColumn, bKeyColumn, aGeomColumn, bGeomColumn):
        """
        Tests spatial predicates to check whether a rule is broken
        """
        self.checkAndOpenDb()
        sql = self.gen.testSpatialRule(class_a, necessity, predicate_function, class_b, min_card, max_card, aKeyColumn, bKeyColumn, aGeomColumn, bGeomColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem testing spatial rule: ') + query.lastError().text()) 
        ret = []
        flagClass = class_a.replace('_temp', '')
        while query.next():
            feat_id = query.value(0)
            reason = self.tr('Feature id {} from {} violates rule {} {}').format(feat_id, class_a, rule.decode('utf-8'), class_b)
            geom = query.value(1)
            # storing flags for class_a
            ret.append((flagClass, feat_id, reason, geom, aGeomColumn))
        return ret

    def getDimension(self, geom):
        """
        Gets geometry's dimension
        geom: geometry tested
        """
        self.checkAndOpenDb()
        sql = self.gen.getDimension(geom)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting dimension: ') + query.lastError().text()) 
        dimension = 0
        while query.next():
            dimension = query.value(0)
        return dimension
    
    def getExplodeCandidates(self, cl):
        """
        Gets multi geometries (i.e number of parts > 1) that will be deaggregated later
        """
        self.checkAndOpenDb()
        sql= self.gen.getMulti(cl)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem exploding candidates: ') + query.lastError().text())
        idList = []
        while query.next():
            idList.append(query.value(0))
        return idList

    def getURI(self, table, useOnly = True, geomColumn = 'geom'):
        """
        Gets tabel URI
        table: table name
        useOnly: bool to determine if 'from only' should be used
        geomColumn: geometry column
        """
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
        id = self.getPrimaryKeyColumn(table)
        uri.setDataSource(schema, layer_name, geomColumn, sql, id)
        uri.disableSelectAtId(True)
        
        return uri
    
    def getDuplicatedGeomRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets duplicated records
        cl: class to be checked
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        tupleList = []
        tableSchema, tableName = self.getTableSchema(cl)
        sql = self.gen.getDuplicatedGeom(tableSchema, tableName, geometryColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting duplicated geometries: ') + query.lastError().text())
        while query.next():
            tupleList.append( (query.value(0),query.value(2)) )
        return tupleList

    def getSmallAreasRecords(self, cl, tol, geometryColumn, keyColumn):
        """
        Gets duplicated records
        cl: class to be checked
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        smallAreasTupleList = []
        tableSchema, tableName = self.getTableSchema(cl)
        sql = self.gen.getSmallAreas(tableSchema, tableName, tol, geometryColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting small areas: ') + query.lastError().text())
        while query.next():
            smallAreasTupleList.append( (query.value(0),query.value(1)) )
        return smallAreasTupleList

    def getSmallLinesRecords(self,classesWithGeom, tol, geometryColumn, keyColumn):
        """
        Gets small lines records 
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        smallLinesDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getSmallLines(tableSchema, tableName, tol, geometryColumn, keyColumn)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                raise Exception(self.tr('Problem getting small lines: ') + query.lastError().text())
            while query.next():
                smallLinesDict = self.utils.buildNestedDict(smallLinesDict, [cl,query.value(0)], query.value(1))
        return smallLinesDict

    def getVertexNearEdgesRecords(self, tableSchema, tableName, tol, geometryColumn, keyColumn, geomType, useTransaction = True):
        """
        Gets vertexes near edges. These vertexes are problematic and should be treated
        tableSchema: table schema
        tableName: table name
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        result = []
        sql = self.gen.prepareVertexNearEdgesStruct(tableSchema, tableName, geometryColumn, keyColumn, geomType)
        sqlList = sql.split('#')
        if useTransaction:
            self.db.transaction()
        for sql2 in sqlList:
            query = QSqlQuery(self.db)
            if not query.exec_(sql2):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem preparing auxiliary structure: ') + query.lastError().text())
        # specific EPSG search
        parameters = {'tableSchema': tableSchema, 'tableName': tableName, 'geometryColumn': geometryColumn}
        epsg = self.findEPSG(parameters=parameters)
        sql = self.gen.getVertexNearEdgesStruct(epsg, tol, geometryColumn, keyColumn)
        query = QSqlQuery(sql,self.db)
        if not query.isActive():
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem getting vertex near edges: ') + query.lastError().text())
        while query.next():
            id = query.value(0)
            geom = query.value(1)
            result.append((id,geom))
        if useTransaction:
            self.db.commit()
        return result

    def removeFeatures(self, cl, processList, keyColumn, useTransaction = True):
        """
        Removes features from class
        cl: class name
        processList: list of dictionaries (id and geometry column)
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        tableSchema, tableName = self.getTableSchema(cl)
        idList = [i['id'] for i in processList]
        sql = self.gen.deleteFeatures(tableSchema, tableName, idList, keyColumn)
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem deleting features from ')+cl+': '+ query.lastError().text())
        if useTransaction:
            self.db.commit()
        return len(idList)

    def getNotSimpleRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets not simple geometries records
        classesWithGeom: class list
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        tupleList = []
        tableSchema, tableName = self.getTableSchema(cl)
        sql = self.gen.getNotSimple(tableSchema, tableName, geometryColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting not simple geometries: ') + query.lastError().text())
        while query.next():
            tupleList.append( (query.value(0), query.value(1)) )
        return tupleList

    def getOutOfBoundsAnglesRecords(self, tableSchema, tableName, tol, geometryColumn, geomType, keyColumn):
        """
        Gets records with anchor points (points between segments) that are out of bounds (i.e outside a limit tolerance)
        tableSchema: table schema
        tableName: table name
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        result = []
        sql = self.gen.getOutofBoundsAngles(tableSchema, tableName, tol, geometryColumn, geomType, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting not out of bounds angles: ') + query.lastError().text())
        while query.next():
            id = query.value(0)
            geom = query.value(1)
            result.append((id, geom))
        return result

    def getFlagsDictByProcess(self, processName):
        """
        Gets flags data dictionary by process name
        processName: process name
        """
        self.checkAndOpenDb()
        flagsDict = dict()
        sql = self.gen.getFlagsByProcess(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting flags dict: ') + query.lastError().text())
        while query.next():
            cl = query.value(0)
            id = query.value(1)
            geometry_column = query.value(2) 
            if cl not in flagsDict.keys():
                flagsDict[cl] = []
            flagsDict[cl].append({'id':str(id), 'geometry_column':geometry_column})
        return flagsDict
    
    def forceValidity(self, cl, processList, keyColumn, useTransaction = True):
        """
        Forces geometry validity (i.e uses ST_MakeValid)
        cl: class
        processList: list of dictionaries (id and geometry column)
        keyColumn: pk column
        """
        self.checkAndOpenDb()
        tableSchema, tableName = self.getTableSchema(cl)
        idList = [i['id'] for i in processList]
        geometryColumn = processList[0]['geometry_column']
        # specific EPSG search
        parameters = {'tableSchema':tableSchema, 'tableName':tableName, 'geometryColumn':geometryColumn}
        srid = self.findEPSG(parameters=parameters)
        sql = self.gen.forceValidity(tableSchema, tableName, idList, srid, keyColumn, geometryColumn)
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem forcing validity of features from ')+cl+': '+ query.lastError().text())
        if useTransaction:
            self.db.commit()
        return len(idList)
    
    def getTableExtent(self, tableSchema, tableName):
        """
        Forces geometry validity (i.e uses ST_MakeValid)
        cl: class
        idList: feature ids to be processed
        """
        self.checkAndOpenDb()
        sql = self.gen.getTableExtent(tableSchema, tableName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting table extent: ') + query.lastError().text())
        
        extent = None
        while query.next():
            xmin = query.value(0)
            xmax = query.value(1)
            ymin = query.value(2)
            ymax = query.value(3)
            extent = (xmin, xmax, ymin, ymax)
        return extent

    def getOrphanGeomTables(self, loading = False):
        """
        Gets parent classes
        """
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements(loading)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting orphan tables: ') + query.lastError().text())
        result = []
        while query.next():
            result.append(query.value(0))
        return result

    def getOrphanGeomTablesWithElements(self, loading = False):
        """
        Gets populated parent classes
        """
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements(loading)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
    
    def updateGeometries(self, tableSchema, tableName, tuplas, epsg, useTransaction = True):
        """
        Updates geometries on database
        tableSchema: table schema
        tableName: table name
        tuplas: tuples used during the update
        epsg: geometry srid
        """
        self.checkAndOpenDb()
        sqls = self.gen.updateOriginalTable(tableSchema, tableName, tuplas, epsg)
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        for sql in sqls:
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem updating geometries: ') + query.lastError().text())
        sqlDel = self.gen.deleteFeaturesNotIn(tableSchema, tableName, tuplas.keys())
        query2 = QSqlQuery(self.db)
        if not query2.exec_(sqlDel):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem deleting geometries: ') + query.lastError().text())            
        if useTransaction:
            self.db.commit()
    
    def checkCentroidAuxStruct(self):
        """
        Checks the centroid structure
        """
        self.checkAndOpenDb()
        sql = self.gen.checkCentroidAuxStruct()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem checking structure: ')+query.lastError().text())
        while query.next():
            if query.value(0) == None:
                return False
        return True
    
    def createCentroidAuxStruct(self, earthCoverageClasses, useTransaction = True):
        """
        Creates the centroid structure
        earthCoverageClasses: earth coverage configuration diciotnary
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        for cl in earthCoverageClasses:
            # getting table schema
            if '.' in cl:
                tableSchema = cl.split('.')[0]
                tableName = cl.split('.')[-1]
            else:
                tableSchema = self.getTableSchemaFromDb(cl)
                tableName = cl
            # specific EPSG search
            parameters = {'tableSchema':tableSchema, 'tableName':tableName}
            srid = self.findEPSG(parameters=parameters)
            sqltext = self.gen.createCentroidColumn(tableSchema, tableName, srid)
            sqlList = sqltext.split('#')
            query = QSqlQuery(self.db)
            for sql2 in sqlList:
                if not query.exec_(sql2):
                    if useTransaction:
                        self.db.rollback()
                    raise Exception(self.tr('Problem creating centroid structure: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
            
    def checkAndCreateCentroidAuxStruct(self, earthCoverageClasses):
        """
        Checks the centroid structure. If not already created, it creates the centroid structure
        earthCoverageClasses: earth coverage configuration diciotnary
        """
        if not self.checkCentroidAuxStruct():
            self.createCentroidAuxStruct(earthCoverageClasses)
    
    def getEarthCoverageClasses(self):
        """
        Gets the earth coverage classes from earth coverage configuration dictionary.
        """
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting earth coverage tables: ') + query.lastError().text())
        result = []
        while query.next():
            result.append(query.value(0))
        return result

    def getEarthCoverageDict(self):
        """
        Gets the earth coverage configuration dictionary.
        """
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting earth coverage structure: ') + query.lastError().text())
        while query.next():
            return query.value(0)

    def setEarthCoverageDict(self, textDict, useTransaction = True):
        """
        Sets the earth coverage configuration dictionary.
        textDict: earth coverage configuration dictionary
        """
        self.checkAndOpenDb()
        sql = self.gen.setEarthCoverageDict(textDict)
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem setting earth coverage structure: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()

    def updateEarthCoverageDict(self, updateDict, oldDict, useTransaction = True):
        """
        Updates earthCoverage, creating new centroids and removing old unused ones.
        """
        creationList = []
        removalList = []
        updateList = updateDict.keys()
        oldList = oldDict.keys()
        for centroid in updateList:
            if centroid not in oldList:
                creationList.append(centroid)
        for centroid in oldList:
            if centroid not in updateList:
                removalList.append(centroid)
        self.createCentroidAuxStruct(creationList, useTransaction = useTransaction)
        self.dropCentroids(removalList, useTransaction = useTransaction)

        
    def dropCentroids(self, classList, useTransaction = True):
        """
        Drops the centroid structure
        classList: classes to be altered
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            # getting table schema
            if '.' not in cl:
                tableSchema = self.getTableSchemaFromDb(cl)
                fullTableName = tableSchema+'.'+cl
            else:
                fullTableName = cl
            # making the query using table schema and table name
            sql = self.gen.dropCentroid(fullTableName)
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem dropping centroids: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()

    def rollbackEarthCoverage(self, classList):
        """
        Rolls back the centroid structure
        classList: classes to be altered
        """
        try:
            self.dropCentroids(classList)
            self.setEarthCoverageDict(None)
        except Exception as e:
            raise e

    def getEarthCoverageCentroids(self):
        """
        Gets the earth coverage structure
        """
        self.checkAndOpenDb()
        sql = self.gen.getEarthCoverageCentroids()
        query = QSqlQuery(sql, self.db)
        centroidList = []
        if not query.isActive():
            raise Exception(self.tr('Problem getting earth coverage structure: ') + query.lastError().text())
        while query.next():
            table = query.value(0).split('_')
            table[-1] = 'c'
            layerName = '_'.join(table)
            centroidList.append(layerName)
        return centroidList

    def getWhoAmI(self, cl, id):
        """
        Gets relation name (relname) from pg_class
        cl: class with schema
        id: table oid
        """
        self.checkAndOpenDb()
        sql = self.gen.getWhoAmI(cl, id)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting class name: ') + query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getDbOID(self):
        self.checkAndOpenDb()
        sql = self.gen.getDbOID(self.db.databaseName())
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting db oid: ') + query.lastError().text())
        while query.next():
            return query.value(0)
    
    def snapToGrid(self, classList, tol, srid, geometryColumn, useTransaction = True):
        """
        Snaps tables to grid (i.e executes ST_SnapToGrid)
        classList: classes to be altered
        tol: tolerance
        geometryColumn: geometryColumn
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sql = self.gen.snapToGrid(cl, tol, srid, geometryColumn)
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem snapping to grid: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
        
    def snapLinesToFrame(self, classList, frameTable, tol, geometryColumn, keyColumn, frameGeometryColumn):
        """
        Snaps lines to frame. This means the lines are prolonged to the frame according to the specified tolerance
        classList: classes to be altered
        tol: tolerance
        geometryColumn: line geometry column
        keyColumn: line ok column
        frameGeometryColumn: frame geometry column
        """
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sqls = self.gen.snapLinesToFrame(cl, frameTable, tol, geometryColumn, keyColumn, frameGeometryColumn)
            for sql in sqls.split('#'):
                if not query.exec_(sql):
                    self.db.rollback()
                    raise Exception(self.tr('Problem snapping to frame: ') + query.lastError().text())
        self.db.commit()
            
    def densifyFrame(self, classList, frameTable, snapTolerance, geometryColumn, frameGeometryColumn, useTransaction = True):
        """
        Densifies the frame creating new vertexes where the lines were snapped
        classList: classes to be altered
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        for cl in classList:
            sql = self.gen.densifyFrame(cl, frameTable, snapTolerance, geometryColumn, frameGeometryColumn)
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem densifying frame: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
        
    def recursiveSnap(self, classList, tol, geometryColumn, keyColumn, useTransaction = True):
        """
        Executes a recursive snap within the class
        classList: classes to be snapped
        tol: tolerance
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.makeRecursiveSnapFunction(geometryColumn, keyColumn)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating recursive snap function: ') + query.lastError().text())
        for cl in classList:
            sql = self.gen.executeRecursiveSnap(cl, tol)
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem snapping class: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def runQuery(self, sql, errorMsg, params, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            if useTransaction:
                self.db.rollback()
            raise Exception(errorMsg + query.lastError().text())
        result = dict()
        key = ','.join(params)
        result[key] = []
        while query.next():
            newElement = []
            for i in range(len(params)):
                newElement.append(query.value(i))
            result[key].append(newElement)
        if useTransaction:
            self.db.commit()
        return result

    def createAndPopulateTempTableFromMap(self, tableName, featureMap, geomColumnName, keyColumn, srid, useTransaction=True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.createTempTable(tableName)
        sqls = sql.split('#')
        for s in sqls:
            if not query.exec_(s):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem creating temp table {}: '.format(tableName)) + query.lastError().text())
        attributes = None
        auxAttributes = None
        for feat in featureMap.values():
            if not attributes:
                # getting only provider fields (we ignore expression fields - type = 6)
                attributes = [field.name() for field in feat.fields() if field.type() != 6]
            # getting keyColumn idx
            keyIdx = feat.fieldNameIndex(keyColumn)
            # getting only the needed attribute values
            values = [feat.attribute(fieldname) for fieldname in attributes]
            # setting the feature id
            values[keyIdx] = feat.id()
            if not feat.geometry():
                continue
            geometry = binascii.hexlify(feat.geometry().asWkb())
            # adding the geometry column to attributes
            if not auxAttributes:
                auxAttributes = attributes[:] #this is done not to mess up original attributes list
                auxAttributes.append(geomColumnName)
            # adding the geometry value to values
            values.append(geometry)
            # preparing 
            prepareValues = []
            for attr in auxAttributes:
                if attr == geomColumnName:
                    prepareValues.append("""ST_SetSRID(ST_Multi(:{0}),{1})""".format(attr,str(srid)))
                else:
                    prepareValues.append(':'+attr)
            #getting sql
            insertSql = self.gen.populateTempTable(tableName, auxAttributes, prepareValues)
            query.prepare(insertSql)
            # binding my values to avoid injections
            for i in range(len(auxAttributes)):
                query.bindValue(prepareValues[i], values[i])
            # actual query execution
            if not query.exec_():
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem creating temp table {}: '.format(tableName)) + query.lastError().text())
        indexSql = self.gen.createSpatialIndex(tableName, geomColumnName)
        if not query.exec_(indexSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating spatial index on temp table {}: '.format(tableName)) + query.lastError().text())
        if useTransaction:
            self.db.commit()        
        
    def dropTempTable(self, tableName, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.dropTempTable(tableName)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem dropping temp table {}: '.format(tableName)) + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def createStyleTable(self, useTransaction = True):
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.createStyleTable()
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating style table: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()

    def checkAndCreateStyleTable(self, useTransaction = True):
        self.checkAndOpenDb()
        sql = self.gen.checkStyleTable()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting style table: ") + query.lastError().text())
        query.next()
        created = query.value(0)
        if not created:
            if useTransaction:
                self.db.transaction()
            createSql = self.gen.createStyleTable()
            query = QSqlQuery(self.db)
            if not query.exec_(createSql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem creating style table: ') + query.lastError().text())
            if useTransaction:
                self.db.commit()
        return created
    
    def getStylesFromDb(self,dbVersion):
        self.checkAndOpenDb()
        sql = self.gen.getStylesFromDb(dbVersion)
        if not sql:
            return []
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting styles from db: ") + query.lastError().text())
        styleList = []
        while query.next():
            styleList.append(query.value(0))
        return styleList
    
    def getStyle(self, styleName, table_name, parsing = True):
        self.checkAndOpenDb()
        sql = self.gen.getStyle(styleName, table_name)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting styles from db: ") + query.lastError().text())
        styleList = []
        query.next()
        qml = query.value(0)
        #TODO: post parse qml to remove possible attribute value type
        if parsing:
            if qml:
                qml = self.utils.parseStyle(qml)
        return qml
    
    def importStyle(self, styleName, table_name, qml, tableSchema, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        parsedQml = self.utils.parseStyle(qml)
        dbName = self.db.databaseName()
        sql = self.gen.importStyle(styleName, table_name, parsedQml, tableSchema,dbName)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem importing style')+ styleName+'/'+ table_name +':' + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def updateStyle(self, styleName, table_name, qml, tableSchema, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        parsedQml = self.utils.parseStyle(qml)
        sql = self.gen.updateStyle(styleName, table_name, parsedQml, tableSchema)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem importing style')+ styleName+'/'+ table_name +':' + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def deleteStyle(self, styleName, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.deleteStyle(styleName)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem importing style')+ styleName+':' + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def importStylesIntoDb(self, styleFolder, useTransaction = True):
        """
        path: path to folder
        styleFolder: folder with version. Example: edgv_213/example
        """
        if self.versionFolderDict[self.getDatabaseVersion()] not in styleFolder:
            raise Exception(self.tr('Style ')+styleFolder+self.tr(' does not match the version of database ') + self.db.databaseName())
        path = os.path.join(os.path.dirname(__file__),'..', '..','Styles')
        stylePath = os.path.join(path,styleFolder)
        availableStyles = os.walk(stylePath).next()[2]
        created = self.checkAndCreateStyleTable(useTransaction = useTransaction)
        for style in availableStyles:
            #filtering and checking file names for special characters
            if style[0] == '.':
                continue
            if not re.match("^[a-zA-Z0-9_.]*$", style):
                raise Exception(self.tr('Problem importing style ')+style)

            tableName = style.split('.')[0]
            localStyle = os.path.join(stylePath,style)
            tableSchema = self.getTableSchemaFromDb(tableName)
            #check if style already exists. If it does, update it.
            #if style does not exist, create one.
            if self.getStyle(styleFolder, tableName, parsing = False):
                self.updateStyle(styleFolder, tableName, localStyle, tableSchema, useTransaction = useTransaction)
            else:
                try:
                    self.importStyle(styleFolder, tableName, localStyle, tableSchema, useTransaction = useTransaction)
                except Exception as e:
                    raise Exception(self.tr('Problem importing style ')+style+':'+':'.join(e.args))

    def getTableSchemaFromDb(self,table):
        self.checkAndOpenDb()
        sql = self.gen.getTableSchemaFromDb(table)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting table schema from db: ") + query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getAllStylesDict(self, perspective = 'style'):
        """
        Returns a dict of styles in a form acording to perspective:
            if perspective = 'style'    : [styleName][dbName][tableName] = timestamp
            if perspective = 'database' : [dbName][styleName][tableName] = timestamp 
        """
        self.checkAndOpenDb()
        sql = self.gen.getAllStylesFromDb()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting styles from db: ") + query.lastError().text())
        styleDict = dict()
        while query.next():
            dbName = query.value(0)
            styleName = query.value(1)
            tableName = query.value(2)
            timestamp = query.value(3)
            if perspective == 'style':
                styleDict = self.utils.buildNestedDict(styleDict, [styleName, dbName, tableName], timestamp)
            elif perspective == 'database':
                styleDict = self.utils.buildNestedDict(styleDict, [dbName, styleName, tableName], timestamp)
        return styleDict
    
    def runSqlFromFile(self, sqlFilePath, useTransaction = True, encoding = 'utf-8'):
        self.checkAndOpenDb()
        file = codecs.open(sqlFilePath, encoding=encoding, mode='r')
        sql = file.read()
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem running sql ')+ sqlFilePath +':' + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def getStructureDict2(self):
        """
        Don't know the purpose of this method
        """
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
                code_name = query2.value(1)
                classDict = self.utils.buildNestedDict(classDict,[str(cl),str(attName)],[(value,code_name)])
        #TODO: get constraints
        return classDict
    
    def getGeomSchemaList(self):
        self.checkAndOpenDb()
        sql = self.gen.getGeometricSchemas()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        schemaList = []
        while query.next():
            schemaList.append(query.value(0))
        return schemaList
    
    def getGeomDict(self, geomTypeDict, insertCategory = False):
        """
        returns a dict like this:
        {'tablePerspective' : {
            'layerName' :
        """
        self.checkAndOpenDb()
        edgvVersion = self.getDatabaseVersion()
        sql = self.gen.getGeomTablesFromGeometryColumns()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom tables from db: ")+query.lastError().text())
        geomDict = dict()
        geomDict['primitivePerspective'] = geomTypeDict
        geomDict['tablePerspective'] = dict()
        while query.next():
            isCentroid = False
            srid = query.value(0)
            geometryType = query.value(2)
            tableSchema = query.value(3)
            tableName = query.value(4)
            geometryColumn = query.value(1)
            layerName = tableName
            if geometryColumn == 'centroid':
                table = layerName.split('_')
                table[-1] = 'c'
                layerName = '_'.join(table)
            if layerName not in geomDict['tablePerspective'].keys():
                geomDict['tablePerspective'][layerName] = dict()
                geomDict['tablePerspective'][layerName]['schema'] = tableSchema
                geomDict['tablePerspective'][layerName]['srid'] = str(srid)
                geomDict['tablePerspective'][layerName]['geometryColumn'] = geometryColumn
                geomDict['tablePerspective'][layerName]['geometryType'] = geometryType
                geomDict['tablePerspective'][layerName]['tableName'] = tableName
                if insertCategory:
                    if edgvVersion == 'Non_EDGV':
                        geomDict['tablePerspective'][layerName]['category'] = ''
                    else:
                        geomDict['tablePerspective'][layerName]['category'] = layerName.split('_')[0]
        return geomDict
    
    def getDbDomainDict(self, auxGeomDict, buildOtherInfo = False):
        """
        returns a dict like this:
        {'adm_posto_fiscal_a': {
            'columns':{
                'operacional': {'references':'dominios.operacional', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                'situacaofisica': {'references':'dominios.situacaofisica', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                'tipopostofisc': {'references':'dominios.tipopostofisc', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                }
            'schema': schemaName
            'geometryColum': geometryColumn
            'primaryKey': primaryKey
            }
        }
        """
        self.checkAndOpenDb()
        #gets only schemas of classes with geom, to speed up the process.
        checkConstraintDict = self.getCheckConstraintDict()
        notNullDict = self.getNotNullDictV2()
        multiDict = self.getMultiColumnsDict()
        sql = self.gen.getGeomTablesDomains()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            #parse done in parseFkQuery to make code cleaner.
            tableName, fkAttribute, domainTable, domainReferencedAttribute = self.parseFkQuery(query.value(0),query.value(1))
            if tableName not in geomDict.keys():
                geomDict[tableName] = dict()
            if 'columns' not in geomDict[tableName].keys():
                geomDict[tableName]['columns'] = dict()
            if fkAttribute not in geomDict[tableName]['columns'].keys():
                geomDict[tableName]['columns'][fkAttribute] = dict()
            geomDict[tableName]['columns'][fkAttribute]['references'] = domainTable
            geomDict[tableName]['columns'][fkAttribute]['refPk'] = domainReferencedAttribute
            values, otherKey = self.getLayerColumnDict(domainReferencedAttribute, domainTable)
            geomDict[tableName]['columns'][fkAttribute]['values'] = values
            geomDict[tableName]['columns'][fkAttribute]['otherKey'] = otherKey
            geomDict[tableName]['columns'][fkAttribute]['constraintList'] = []
            geomDict[tableName]['columns'][fkAttribute]['isMulti'] = False
            if tableName in checkConstraintDict.keys():
                if fkAttribute in checkConstraintDict[tableName].keys():
                    geomDict[tableName]['columns'][fkAttribute]['constraintList'] = checkConstraintDict[tableName][fkAttribute]
            geomDict[tableName]['columns'][fkAttribute]['nullable'] = True
            if tableName in notNullDict.keys():
                if fkAttribute in notNullDict[tableName]['attributes']:
                    geomDict[tableName]['columns'][fkAttribute]['nullable'] = False
            if tableName in multiDict.keys():
                if fkAttribute in multiDict[tableName]:
                    geomDict[tableName]['columns'][fkAttribute]['isMulti'] = True
        for tableName in multiDict.keys():
            if tableName in auxGeomDict['tablePerspective'].keys():
                for fkAttribute in multiDict[tableName]:
                    if tableName not in geomDict.keys():
                        geomDict[tableName] = dict()
                    if 'columns' not in geomDict[tableName].keys():
                        geomDict[tableName]['columns'] = dict()
                    if fkAttribute not in geomDict[tableName]['columns'].keys():
                        geomDict[tableName]['columns'][fkAttribute] = dict()
                    geomDict[tableName]['columns'][fkAttribute]['references'] = None
                    if fkAttribute in checkConstraintDict[tableName].keys():
                        geomDict[tableName]['columns'][fkAttribute]['constraintList'] = checkConstraintDict[tableName][fkAttribute]
                    geomDict[tableName]['columns'][fkAttribute]['nullable'] = True
                    if tableName in notNullDict.keys():
                            if fkAttribute in notNullDict[tableName]['attributes']:
                                geomDict[tableName]['columns'][fkAttribute]['nullable'] = False
                    if tableName in multiDict.keys():
                        if fkAttribute in multiDict[tableName]:
                            geomDict[tableName]['columns'][fkAttribute]['isMulti'] = True
                            geomDict[tableName]['columns'][fkAttribute]['refPk'] = 'code'
                            geomDict[tableName]['columns'][fkAttribute]['otherKey'] = 'code_name'
                            geomDict[tableName]['columns'][fkAttribute]['values'] = dict()
            
        return geomDict
    
    def getCheckConstraintDict(self):
        """
        returns a dict like this:
        {'asb_dep_abast_agua_a': {
                'finalidade': [2,3,4]
                'construcao': [1,2]
                'situacaofisica': [0,1,2,3,5]
            }
        }
        """
        self.checkAndOpenDb()
        #gets only schemas of classes with geom, to speed up the process.
        sql = self.gen.getGeomTableConstraints()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            #parse done in parseCheckConstraintQuery to make code cleaner.
            tableName, attribute, checkList = self.parseCheckConstraintQuery(query.value(0),query.value(1))
            if tableName not in geomDict.keys():
                geomDict[tableName] = dict()
            geomDict[tableName][attribute] = checkList
        return geomDict
    
    def parseFkQuery(self, queryValue0, queryValue1):
        if '.' in queryValue0:
            splitList = queryValue0.split('.')
            tableName = splitList[1]
        else:
            tableName = queryValue0
        fkText = queryValue1
        fkAttribute = fkText.split(')')[0].replace('FOREIGN KEY (','')
        subtextList = fkText.split(' REFERENCES ')[-1].replace(' MATCH FULL','').split('(')
        domainTable = subtextList[0]
        if '.' not in domainTable:
            auxDomain = domainTable.replace('"','')
            domainTable = '''"{0}"."{1}"'''.format(self.getTableSchemaFromDb(auxDomain), auxDomain)
        domainReferencedAttribute = subtextList[1].replace(')','') 
        return tableName.replace('"',''), fkAttribute.replace('"',''), domainTable, domainReferencedAttribute

    def parseCheckConstraintQuery(self, queryValue0, queryValue1):
        try:
            if 'ANY' in queryValue1 or '@' in queryValue1:
                return self.parseCheckConstraintWithAny(queryValue0, queryValue1)
            else:
                return self.parseCheckConstraintWithOr(queryValue0, queryValue1)
        except Exception as e:
            raise Exception(self.tr("Error parsing check constraint!\n"+':'.join(e.args)))
    
    def parseCheckConstraintWithOr(self, queryValue0, queryValue1):
        if '.' in queryValue0:
            query0Split = queryValue0.split('.')
            tableSchema = query0Split[0]
            tableName = query0Split[1]
        else:
            tableName = queryValue0
        query1Split = queryValue1.replace('CHECK ','').replace('(','').replace(')','').replace(' ','').replace('"','').split('OR')
        checkList = []
        for i in query1Split:
            attrSplit = i.split('=')
            attribute = attrSplit[0]
            checkList.append(int(attrSplit[1]))
        return tableName, attribute, checkList
    
    def parseCheckConstraintWithAny(self, queryValue0, queryValue1):
        if '.' in queryValue0:
            query0Split = queryValue0.split('.')
            tableSchema = query0Split[0]
            tableName = query0Split[1]
        else:
            tableName = queryValue0
        query1Split = queryValue1.replace('"','').replace('ANY','').replace('ARRAY','').replace('::smallint','').replace('(','').replace(')','').replace('CHECK','').replace('[','').replace(']','').replace(' ','')
        checkList = []
        splitToken = ''
        if '=' in query1Split:
            splitToken = '='
        elif '<@' in query1Split:
            splitToken = '<@'
        equalSplit = query1Split.split(splitToken)
        attribute = equalSplit[0]
        checkList = map(int,equalSplit[1].split(','))
        return tableName, attribute, checkList
    
    def getMultiColumnsDict(self):
        """
        { 'table_name':[-list of columns-] } 
        """
        self.checkAndOpenDb()
        #gets only schemas of classes with geom, to speed up the process.
        schemaList = self.getGeomSchemaList()
        sql = self.gen.getMultiColumns(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            #TODO: check if 2.1.3 raises problem, because of empty query
            aux = json.loads(query.value(0))
            geomDict[aux['table_name']]=aux['attributes']
        return geomDict
    
    def getTablesJsonList(self):
        self.checkAndOpenDb()
        sql = self.gen.getTablesJsonList()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting tables dict from db: ")+query.lastError().text())
        geomList = []
        while query.next():
            geomList.append(json.loads(query.value(0)))
        return geomList  
    
    def getGeomTypeDict(self, loadCentroids=False):
        self.checkAndOpenDb()
        sql = self.gen.getGeomByPrimitive()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom types from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            if loadCentroids and aux['geomtype'] == 'POINT':
                classlist = []
                for layerName in aux['classlist']:
                    table = layerName.split('_')
                    table[-1] = 'c'
                    classlist.append('_'.join(table))                  
                geomDict[aux['geomtype']] = classlist
            else:
                geomDict[aux['geomtype']] = aux['classlist']
        return geomDict
    
    def getGeomColumnDict(self):
        """
        Dict in the form 'geomName':[-list of table names-]
        """
        self.checkAndOpenDb()
        sql = self.gen.getGeomColumnDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom column dict: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            if aux['f2'] not in geomDict.keys():
                geomDict[aux['f2']] = []
            geomDict[aux['f2']].append(aux['f1'])
        return geomDict
    
    def getGeomColumnTupleList(self, showViews = False, hideCentroids = True, primitiveFilter = [], withElements = False):
        """
        list in the format [(table_schema, table_name, geometryColumn, geometryType, tableType)]
        centroids are hidden by default
        """
        self.checkAndOpenDb()
        centroidTableList = []
        try:
            edgvVersion = self.getDatabaseVersion()
            if hideCentroids:
                if self.checkIfExistsConfigTable('EarthCoverage'):
                    propertyDict = self.getAllSettingsFromAdminDb('EarthCoverage')
                    propertyName = propertyDict[edgvVersion][0]
                    dbName = self.db.databaseName()
                    settingDict = json.loads(self.getSettingFromAdminDb('EarthCoverage', propertyName, edgvVersion))
                    earthCoverageDict = settingDict['earthCoverageDict']
                    centroidTableList = [i.split('.')[-1] for i in earthCoverageDict.keys()]
        except:
            pass
        
        sql = self.gen.getGeomColumnTupleList(showViews = showViews)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom tuple list: ")+query.lastError().text())
        localList = []
        while query.next():
            if query.value(2) == 'centroid' and query.value(3) == 'POINT' and query.value(1) in centroidTableList:
                continue
            else:
                localList.append((query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)))
        if not withElements and primitiveFilter == []:
            return localList
        if withElements:
            listWithElements = self.getLayersWithElementsV2([{'tableSchema':i[0],'tableName':i[1]} for i in localList])
            geomList = [i for i in localList if i[1] in listWithElements]
        else:
            geomList = localList
        if primitiveFilter <> []:
            geomTypeFilter = []
            if 'p' in primitiveFilter: 
                geomTypeFilter.append('POINT')
                geomTypeFilter.append('MULTIPOINT')
            if 'l' in primitiveFilter: 
                geomTypeFilter.append('LINESTRING')
                geomTypeFilter.append('MULTILINESTRING')
            if 'a' in primitiveFilter:
                geomTypeFilter.append('POLYGON')
                geomTypeFilter.append('MULTIPOLYGON')
            geomList = [i for i in geomList if i[3] in geomTypeFilter]
        return geomList
    
    def getGeomColumnDictV2(self, showViews = False, hideCentroids = True, primitiveFilter = [], withElements = False, excludeValidation = False):
        geomList = self.getGeomColumnTupleList(showViews = showViews, hideCentroids = hideCentroids, primitiveFilter = primitiveFilter, withElements = withElements)
        edgvVersion = self.getDatabaseVersion()
        lyrDict = dict()
        for tableSchema, tableName, geom, geomType, tableType in geomList:
            if excludeValidation:
                if tableSchema == 'validation':
                    continue
            if edgvVersion == 'Non_EDGV':
                lyrName = tableName
                cat = tableSchema
            else:
                lyrName = '_'.join(tableName.split('_')[1::])
                cat = tableName.split('_')[0]
            key = ','.join([cat, lyrName, geom, geomType, tableType])
            lyrDict[key] = {'tableSchema':tableSchema, 'tableName':tableName, 'geom':geom, 'geomType':geomType, 'tableType':tableType, 'lyrName':lyrName, 'cat':cat}
        return lyrDict

    def getLayersFilterByInheritance(self, layerList):
        filter = [i.split('.')[-1] for i in self.getOrphanGeomTables(loading = True)]
        filtered = []
        for lyr in layerList:
            if lyr in filter:
                filtered.append(lyr)
        return filtered

    def getNotNullDictV2(self):
        """
        Dict in the form 'tableName': { 'schema':-name of the schema'
                                        'attributes':[-list of table names-]}
        """
        self.checkAndOpenDb()
        sql = self.gen.getNotNullDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting not null dict: ")+query.lastError().text())
        notNullDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            if aux['f1'] not in notNullDict.keys():
                notNullDict[aux['f1']] = dict()
            notNullDict[aux['f1']]['schema'] = aux['f2']
            if 'attributes' not in notNullDict[aux['f1']].keys():
                notNullDict[aux['f1']]['attributes'] = []
            notNullDict[aux['f1']]['attributes'] = aux['f3']
        return notNullDict
    
    def getDomainDictV2(self, domainTable):
        self.checkAndOpenDb()
        sql = self.gen.getDomainDict(domainTable)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting domain dict from table ")+domainTable+':'+query.lastError().text())
        domainDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            domainDict[aux['f2']] = aux['f1']
        return domainDict
    
    def getLayerColumnDict(self, refPk, domainTable):
        self.checkAndOpenDb()
        sql = self.gen.getDomainCodeDict(domainTable)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting layer column dict from table ")+domainTable+':'+query.lastError().text())
        domainDict = dict()
        otherKey = None
        while query.next():
            aux = json.loads(query.value(0))
            if not otherKey:
                otherKey = [key for key in aux.keys() if key <> refPk][0]
            domainDict[aux[refPk]] = aux[otherKey]
        return domainDict, otherKey
    
    def getGeomStructDict(self):
        """
        Returns dict in the following format:
        {'tableName': { 'attrName1':isNullable, 'attrName2':isNullable} }
        """
        self.checkAndOpenDb()
        sql = self.gen.getGeomStructDict()
        yesNoDict = {'YES':True, 'NO':False}
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom struct dict: ")+query.lastError().text())
        geomStructDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            tableName = aux['table_name']
            if tableName not in geomStructDict.keys():
                geomStructDict[tableName] = dict()
            for d in aux['array_agg']:
                geomStructDict[tableName][d['f1']] = yesNoDict[d['f2']]
        return geomStructDict
    
    def createDbFromTemplate(self, dbName, templateName, parentWidget = None):
        #check if created, if created prompt if drop is needed
        self.checkAndOpenDb()
        if parentWidget:
            progress = ProgressWidget(1,2,self.tr('Creating database {0} from template {1}... ').format(dbName, templateName), parent = parentWidget)
            progress.initBar()
        self.dropAllConections(templateName)
        if parentWidget:
            progress.step()
        sql = self.gen.createFromTemplate(dbName, templateName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem creating from template: ') + query.lastError().text())
        self.checkAndCreateStyleTable()
        #this close is to allow creation from template
        self.db.close()
        if parentWidget:
            progress.step()
    
    def getViewDefinition(self, viewName):
        self.checkAndOpenDb()
        sql = self.gen.getViewDefinition(viewName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting view definition: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def updateDbSRID(self, srid, useTransaction = True, closeAfterUse = True, parentWidget = None, threading = False):
        self.checkAndOpenDb()
        tableDictList = self.getParentGeomTables(getDictList = True, showViews = False, hideCentroids = False)
        viewList = ['''"{0}"."{1}"'''.format(i['tableSchema'],i['tableName']) for i in self.getGeomColumnDictV2(showViews = True, hideCentroids = False).values() if i['tableType'] == 'VIEW']
        viewDefinitionDict = {i:self.getViewDefinition(i) for i in viewList}

        if useTransaction:
            self.db.transaction()
        if parentWidget:
            progress = ProgressWidget(1, 2*len(viewList)+len(tableDictList), self.tr('Updating SRIDs from {0}... ').format(self.db.databaseName()), parent = parentWidget)
            progress.initBar()
        for view in viewList:
            viewSql = self.gen.dropView(view)
            query = QSqlQuery(self.db)
            if not query.exec_(viewSql):
                if useTransaction:
                    self.db.rollback()
                if threading:
                    return (viewSql, query)
                else:
                    raise Exception(self.tr('Problem dropping views: ') + query.lastError().text())
            if parentWidget:
                progress.step()

        for tableDict in tableDictList:
            sridSql = self.gen.updateDbSRID(tableDict, srid)
            query = QSqlQuery(self.db)
            if not query.exec_(sridSql):
                if useTransaction:
                    self.db.rollback()
                if threading:
                    return (sridSql, query)
                else:
                    raise Exception(self.tr('Problem dropping views: ') + query.lastError().text())
            if parentWidget:
                progress.step()
        for viewName in viewList:
            createViewSql = self.gen.createViewStatement(viewName, viewDefinitionDict[viewName])
            query = QSqlQuery(self.db)
            if not query.exec_(createViewSql):
                if useTransaction:
                    self.db.rollback()
                if threading:
                    return (createViewSql, query)
                else:
                    raise Exception(self.tr('Problem dropping views: ') + query.lastError().text())
            if parentWidget:
                progress.step()
        if useTransaction:
            self.db.commit()
        #this close is to allow creation from template
        if closeAfterUse:
            self.db.close()
    
    def checkTemplate(self, version = None):
        self.checkAndOpenDb()
        if not version:
            version = self.getDatabaseVersion()
        dbName = self.getTemplateName(version)
        sql = self.gen.checkTemplate()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem setting as template: ")+query.lastError().text())
        while query.next():
            if query.value(0) == dbName:
                return True
        return False
    
    def createTemplateDatabase(self, version):
        """
        version: edgv version
        creates an empty database with the name of a template
        """
        self.checkAndOpenDb()
        dbName = self.getTemplateName(version)
        try:
            self.dropDatabase(dbName)
        except:
            pass
        self.createDatabase(dbName)
    
    def createDatabase(self, dbName):
        """
        Creates a database with a given name
        """
        self.checkAndOpenDb()
        sql = self.gen.getCreateDatabase(dbName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem creating database: ")+query.lastError().text())
    
    def getTemplateName(self, version):
        if version == '2.1.3':
            return 'template_edgv_213'
        elif version == 'FTer_2a_Ed':
            return 'template_edgv_fter_2a_ed'
        elif version == '3.0':
            return 'template_edgv_3'
    
    def setDbAsTemplate(self, version = None, dbName = None, setTemplate = True, useTransaction = True):
        self.checkAndOpenDb()
        if not dbName:
            dbName = self.getTemplateName(version)
        sql = self.gen.setDbAsTemplate(dbName, setTemplate)
        query = QSqlQuery(self.db)
        if useTransaction:
            self.db.transaction()
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr("Problem setting database as template: ")+query.lastError().text())
        if useTransaction:
            self.db.commit()

    def checkIfTemplate(self, dbName):
        self.checkAndOpenDb()
        sql = self.gen.checkIfTemplate(dbName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem checking  template: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getCreationSqlPath(self, version):
        currentPath = os.path.dirname(__file__)
        currentPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool')
        edgvPath = ''
        if version == '2.1.3':
            edgvPath = os.path.join(currentPath, 'sqls', '213', 'edgv213.sql')
        elif version == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, 'sqls', 'FTer_2a_Ed', 'edgvFter_2a_Ed.sql')
        elif version == '3.0':
            edgvPath = os.path.join(currentPath, 'sqls', '3', 'edgv3.sql')
        elif version == 'admin':
            edgvPath = os.path.join(currentPath, 'sqls', 'admin', 'dsgtools_admindb.sql')
        return edgvPath
    
    def getCommandsFromFile(self, edgvPath, epsg = None):
        """
        Gets all sql commands from file
        """
        file = codecs.open(edgvPath, encoding='utf-8', mode="r")
        sql = file.read()
        if epsg:
            sql = sql.replace('[epsg]', str(epsg))
        file.close()
        commands = sql.split('#')
        return commands
    
    def getImplementationVersionFromFile(self, edgvVersion):
        edgvPath = self.getCreationSqlPath(edgvVersion)
        commands = self.getCommandsFromFile(edgvPath)
        searchString = 'INSERT INTO public.db_metadata (edgvversion,dbimplversion) VALUES ('
        for command in commands:
            if searchString in command:
                return command.split(searchString)[-1].split(',')[-1].replace(')','').replace("'","")

    def setStructureFromSql(self, version, epsg, useTransaction = True, closeAfterUsage = True):
        self.checkAndOpenDb()
        edgvPath = self.getCreationSqlPath(version)
        commands = [i for i in self.getCommandsFromFile(edgvPath, epsg = epsg) if i != '']
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        for command in commands:
            if not query.exec_(command):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Error on database creation! ')+query.lastError().text()+ self.tr(' Db will be dropped.'))
        if useTransaction:
            self.db.commit()
        self.alterSearchPath(version, useTransaction = useTransaction)
        self.setDbAsTemplate(version = version, useTransaction = useTransaction)
        self.createStyleTable(useTransaction = useTransaction)
        #this close is to allow creation from template
        if closeAfterUsage:
            self.db.close()
    
    def alterSearchPath(self, version, useTransaction = True):
        self.checkAndOpenDb()
        dbName = self.db.databaseName()
        sql = self.gen.alterSearchPath(dbName, version)
        self.db.transaction()
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            raise Exception(self.tr("Problem altering search path: ")+query.lastError().text())
        self.db.commit()

    def createFrame(self, type, scale, param, paramDict = dict()):
        mi, inom, frame = self.prepareCreateFrame(type, scale, param)
        self.insertFrame(scale, mi, inom, binascii.hexlify(frame.asWkb()), paramDict = paramDict)
        return frame
    
    def getUsersFromServer(self):
        self.checkAndOpenDb()
        ret = []
        sql = self.gen.getUsersFromServer()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting users: ")+query.lastError().text())
        while query.next():
            ret.append((query.value(0), query.value(1)))
        return ret
    
    def reassignAndDropUser(self, user):
        self.checkAndOpenDb()
        sql = self.gen.reasignAndDropUser(user)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem removing user: ') +user+'\n'+query.lastError().text())
        
    def removeFeatureFlags(self, layer, featureId, processName, useTransaction = True):
        """
        Removes flags for a specific layer, feature id and process name
        layer: layer name
        featureId: feature id
        processName: process name
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.deleteFeatureFlagsFromDb(layer, str(featureId), processName)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem deleting flag: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
        
    def removeEmptyGeometries(self, layer, geometryColumn, useTransaction = True):
        """
        Removes empty geometries from layer
        layer: layer name
        geometryColumn: geometryColumn
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.removeEmptyGeomtriesFromDb(layer, geometryColumn)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem removing empty geometries: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def getParamsFromConectedDb(self):
        self.checkAndOpenDb()
        host = self.db.hostName()
        port = self.db.port()
        user = self.db.userName()
        password = self.db.password()
        return (host, port, user, password)

    def createAdminDb(self):
        """
        Creates a database with a given name
        """
        self.checkAndOpenDb()
        sql = self.gen.getCreateDatabase('dsgtools_admindb')
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem creating database: ")+query.lastError().text())
    
    def hasAdminDb(self):
        """
        Checks if server has a dsgtools_admindb
        """
        self.checkAndOpenDb()
        sql = self.gen.hasAdminDb()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem looking for admindb: ")+query.lastError().text())
        while query.next():
            if query.value(0):
                return True
        return False
    
    def getRolesDict(self):
        """
        Gets a dict with the format: 'dbname':{[-list of roles-]}
        """
        self.checkAndOpenDb()
        sql = self.gen.getRolesDict()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting roles dict: ")+query.lastError().text())
        rolesDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            if aux['dbname'] not in rolesDict.keys():
                rolesDict[aux['dbname']] = []
            rolesDict[aux['dbname']].append(aux['rolename'])
        return rolesDict
    
    def insertIntoPermissionProfile(self, name, jsondict, edgvversion):
        """
        Inserts into public.permission_profile on dsgtools_admindb (name, jsondict, edgvversion)
        """
        self.checkAndOpenDb()
        if self.db.databaseName() <> 'dsgtools_admindb':
            raise Exception(self.tr('Error! Operation not defined for non dsgtools_admindb'))
        sql = self.gen.insertIntoPermissionProfile(name, jsondict, edgvversion)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem inserting into permission profile: ")+query.lastError().text())
    
    def dropRoleOnDatabase(self, roleName):
        """
        Drops role using drop owned by and drop role.
        This is like dropRole, but it does not uses a specific function, hence it is more generic.
        """
        self.checkAndOpenDb()
        sql = self.gen.dropRoleOnDatabase(roleName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem dropping profile: ")+ roleName + ' :' + query.lastError().text())
    
    def getRoleFromAdminDb(self, roleName, edgvVersion):
        """
        Gets role from public.permission_profile
        """
        self.checkAndOpenDb()
        sql = self.gen.getPermissionProfile(roleName, edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting roles from adminDb: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getAllRolesFromAdminDb(self):
        """
        Gets role from public.permission_profile and returns a dict with format {edgvVersion:[-list of roles-]}
        """
        self.checkAndOpenDb()
        sql = self.gen.getAllPermissionProfiles()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting all roles from adminDb: ")+query.lastError().text())
        allRolesDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            allRolesDict[aux['edgvversion']] = aux['profiles']
        return allRolesDict
    
    def deletePermissionProfile(self, name, edgvversion):
        """
        Deletes profile from from public.permission_profiles
        """
        self.checkAndOpenDb()
        sql = self.gen.deletePermissionProfile(name, edgvversion)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem deleting permission profile: ")+query.lastError().text())
    
    def getGrantedRolesDict(self):
        """
        Gets a dict in the format:
        { roleName : [-list of users-] } 
        """
        self.checkAndOpenDb()
        sql = self.gen.getRolesWithGrantedUsers()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting granted roles dict: ")+query.lastError().text())
        grantedRolesDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            if aux['profile'] not in grantedRolesDict.keys():
                grantedRolesDict[aux['profile']] = []
            for user in aux['users']:
                if user not in grantedRolesDict[aux['profile']]:
                    grantedRolesDict[aux['profile']].append(user)
        return grantedRolesDict
    
    def updatePermissionProfile(self, name, edgvVersion, newjsondict):
        """
        Updates public.permission_profile with new definition.
        """
        self.checkAndOpenDb()
        sql = self.gen.updateRecordFromPropertyTable('Permission', name, edgvVersion, newjsondict)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem updating permission profile: ")+query.lastError().text())
    
    def getDomainTables(self):
        """
        Lists all domain tables available.
        """
        self.checkAndOpenDb()
        sql = self.gen.getDomainTables()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting domain tables: ")+query.lastError().text())
        domainList = []
        while query.next():
            domainList.append(query.value(0))
        return domainList
    
    def getGeometricSchemaList(self):
        """
        Lists all schemas with geometries.
        """
        self.checkAndOpenDb()
        sql = self.gen.getGeometricSchemaList()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geometric schema list: ")+query.lastError().text())
        schemaList = []
        while query.next():
            schemaList.append(query.value(0))
        return schemaList
    
    def getGeometricTableListFromSchema(self, schema):
        """
        Lists all tables with geometries from schema
        """
        self.checkAndOpenDb()
        sql = self.gen.getGeometricTableListFromSchema(schema)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geometric table list: ")+query.lastError().text())
        tableList = []
        while query.next():
            tableList.append(query.value(1))
        return tableList
    
    def getParentGeomTables(self, getTuple = False, getFullName = False, primitiveFilter = [], showViews = False, hideCentroids = True, getDictList = False):
        """
        Lists all tables with geometries from schema that are parents.
        """
        self.checkAndOpenDb()
        layerDictList = self.getGeomColumnDictV2(showViews = showViews, hideCentroids = hideCentroids)
        geomTables = [i['tableName'] for i in layerDictList.values()]
        inhDict = self.getInheritanceDict()

        # final parent list
        parentGeomTables = []
        childList = []
        parentList = []
        for parent in inhDict.keys():
            # parents list
            if parent not in parentList:
                parentList.append(parent)
            # children list
            for child in inhDict[parent]:
                if child not in childList:
                    childList.append(child)

        # we must check tables orphan tables (no parent and no child)
        # if a table like this is a geometry table it should be stored
        for geomTable in geomTables:
            if geomTable not in childList and geomTable not in parentList and geomTable not in parentGeomTables:
                parentGeomTables.append(geomTable)
                
        # analyzing only the inheritance information
        for parent in inhDict.keys():
            if parent in geomTables:
                # if a parent is a geometry table but is also a child it should not be stored
                if parent not in childList and parent not in parentGeomTables:
                    parentGeomTables.append(parent)
            else:
                # if the parent is not a geometry table all its children should be stored
                for child in inhDict[parent]:
                    if child not in parentGeomTables:
                        parentGeomTables.append(child)                

        #filters in case of filter
        if primitiveFilter != []:
            filterList = [i['tableName'] for i in self.getGeomColumnDictV2(showViews = showViews, hideCentroids = hideCentroids, primitiveFilter = primitiveFilter).values()]
            aux = [i for i in parentGeomTables if i in filterList]
            parentGeomTables = aux
        parentGeomTables.sort()
        if getDictList:
            filteredDictList = [i for i in layerDictList.values() if i['tableName'] in parentGeomTables]
            return filteredDictList
        #output types
        if getFullName:
            parentFullList = []
            for parent in parentGeomTables:
                schema = self.getTableSchemaFromDb(parent)
                if schema not in ['views', 'validation'] and schema:
                    parentFullList.append( schema+'.'+parent )
            return parentFullList
        if not getTuple:
            return [i for i in parentGeomTables if self.getTableSchemaFromDb(i) not in ['views', 'validation'] ]
        else:
            parentTupleList = []
            for parent in parentGeomTables:
                schema = self.getTableSchemaFromDb(parent)
                if schema not in ['views', 'validation']:
                    parentTupleList.append( (schema, parent) )
            return parentTupleList
    
    def getInheritanceDict(self):
        self.checkAndOpenDb()
        sql = self.gen.getInheritanceDict()
        query = QSqlQuery(sql, self.db)
        inhDict = dict()
        if not query.isActive():
            raise Exception(self.tr("Problem getting inheritance: ")+query.lastError().text())
        while query.next():
            aux = json.loads(query.value(0))
            inhDict[aux['parentname']] = aux['childname']
        return inhDict
    
    def getInheritanceBloodLine(self, parent, inhDict = None):
        """
        Lists all tables that have parent as an ancestor.
        """
        if not inhDict:
            inhDict = self.getInheritanceDict()
        bloodLine = []
        self.utils.getRecursiveInheritance(parent, bloodLine, inhDict)
        return bloodLine
    
    def getFullBloodLineDict(self, candidate):
        pass
    
    def getAttributeListFromTable(self, schema, tableName):
        """
        Lists all attributes from table.
        """
        self.checkAndOpenDb()
        sql = self.gen.getAttributeListFromTable(schema, tableName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting attribute list: ")+query.lastError().text())
        attributeList = []
        while query.next():
            attributeList.append(query.value(0))
        return attributeList
    
    def getAttributeJsonFromDb(self):
        self.checkAndOpenDb()
        sql = self.gen.getAttributeDictFromDb()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting attribute list: ")+query.lastError().text())
        attributeJson = []
        while query.next():
            attributeJson.append(json.loads(query.value(0)))
        return attributeJson
    
    def getAllDomainValues(self, domainTableList = []):
        self.checkAndOpenDb()
        if domainTableList == []:
            domainTableList = self.getDomainTables()
        valueList = []
        for domainTable in domainTableList:
            sql = self.gen.getAllDomainValues(domainTable)
            query = QSqlQuery(sql, self.db)
            while query.next():
                value = query.value(0)
                if value not in valueList:
                    valueList.append(value)
        valueList.sort()
        return valueList
    
    def getInheritanceTreeDict(self):
        self.checkAndOpenDb()
        inhDict = self.getInheritanceDict()
        layerList = self.listGeomClassesFromDatabase()
        geomTables = [i.split('.')[-1] for i in layerList]
        inhTreeDict = dict()
        for parent in inhDict.keys():
            self.utils.getRecursiveInheritanceTreeDict(parent, inhTreeDict, inhDict)
        blackList = []
        for parent in inhTreeDict.keys():
            otherKeys = [i for i in inhTreeDict.keys() if i <> parent]
            for otherKey in otherKeys:
                if inhTreeDict[parent] in inhTreeDict[otherKey].values():
                    if parent not in blackList:
                        blackList.append(parent)
                        break
        for item in blackList:
            inhTreeDict.pop(item)
        childBlackList = []
        self.utils.getAllItemsInDict(inhTreeDict,childBlackList)
        for geomTable in geomTables:
            if geomTable not in childBlackList:
                schema = self.getTableSchemaFromDb(geomTable)
                if schema not in ['views', 'validation']:
                    inhTreeDict[geomTable] = dict()
        r = {'root':inhTreeDict}
        return r
    
    def getInheritanceConstraintDict(self):
        """
        Returns a dict in the form:
            {'tableName':{'attributeName': {'tableName','constraintName', 'filter'} 
                }
            }
        """
        self.checkAndOpenDb()
        schemaList = [i for i in self.getGeometricSchemaList() if i not in ['views', 'validation']]
        sql = self.gen.getConstraintDict(schemaList)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem constraint dict from db: ")+query.lastError().text())
        inhConstrDict = dict()
        while query.next():
            queryResult = json.loads(query.value(0))
            tableName = queryResult['tablename']
            if tableName not in inhConstrDict.keys():
                inhConstrDict[tableName] = dict()
            defList = queryResult['array_agg']
            for value in defList:
                constraintName = value['f1'] 
                constraintDef = value['f2']
                attrName = constraintName.split('_')[-2]
                currTableName = constraintName.split('_'+attrName)[0]
                if attrName not in inhConstrDict[tableName].keys():
                    inhConstrDict[tableName][attrName] = []
                filterDef = self.parseCheckConstraintQuery(constraintName,constraintDef)[-1]
                schema = self.getTableSchemaFromDb(currTableName)
                currTag = {'schema':schema, 'tableName':currTableName, 'constraintName':constraintName, 'filter':filterDef}
                if currTag not in inhConstrDict[tableName][attrName]:
                    inhConstrDict[tableName][attrName].append(currTag)
        return inhConstrDict
    
    def getDefaultFromDb(self, schema, tableName, attrName):
        """
        Gets default value from table
        """
        self.checkAndOpenDb()
        sql = self.gen.getDefaultFromDb(schema, tableName, attrName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting default from db: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def insertSettingIntoAdminDb(self, settingType, name, jsondict, edgvversion):
        """
        Inserts setting into dsgtools_admindb (name, jsondict, edgvversion),
        according to settingType
        """
        self.checkAndOpenDb()
        if self.db.databaseName() <> 'dsgtools_admindb':
            raise Exception(self.tr('Error! Operation not defined for non dsgtools_admindb'))
        sql = self.gen.insertSettingIntoAdminDb(settingType, name, jsondict, edgvversion)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem inserting property ")+settingType+self.tr(' into dsgtools_admindb: ')+query.lastError().text())
    
    def getSettingFromAdminDb(self, settingType, settingName, edgvVersion):
        """
        Gets role from public.permission_profile
        """
        self.checkAndOpenDb()
        sql = self.gen.getSettingFromAdminDb(settingType, settingName, edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting setting from adminDb: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getSettingVersion(self, settingType, settingName):
        self.checkAndOpenDb()
        sql = self.gen.getSettingVersion(settingType, settingName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting setting from adminDb: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getAllSettingsFromAdminDb(self, settingType):
        """
        Gets role from public.permission_profile and returns a dict with format {edgvVersion:[-list of roles-]}
        """
        self.checkAndOpenDb()
        if not self.checkIfExistsConfigTable(settingType):
            return dict()
        sql = self.gen.getAllSettingsFromAdminDb(settingType)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting settings from adminDb: ")+query.lastError().text())
        allRolesDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            allRolesDict[aux['edgvversion']] = aux['settings']
        return allRolesDict
    
    def deleteSettingFromAdminDb(self, settingType, name, edgvversion):
        """
        Deletes profile from from public.permission_profiles
        """
        self.checkAndOpenDb()
        sql = self.gen.deleteSettingFromAdminDb(settingType, name, edgvversion)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem deleting permission setting: ")+query.lastError().text())

    def upgradePostgis(self, useTransaction = True):
        self.checkAndOpenDb()
        updateDict = self.getPostgisVersion()
        if updateDict <> dict():
            if useTransaction:
                self.db.transaction()
            sql = self.gen.upgradePostgis(updateDict)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr("Problem upgrading postgis: ")+query.lastError().text())
            if useTransaction:
                self.db.commit()
    
    def getPostgisVersion(self):
        self.checkAndOpenDb()
        sql = self.gen.getPostgisVersion()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting postgis version: ")+query.lastError().text())
        updateDict = dict()
        while query.next():
            defaultVersion = query.value(1)
            installedVersion = query.value(2)
            if defaultVersion <> installedVersion and installedVersion not in ['', None]:                
                updateDict[query.value(0)] = {'defaultVersion':defaultVersion, 'installedVersion':installedVersion}
        return updateDict
    
    def getCustomizationPerspectiveDict(self, perspective):
        self.checkAndOpenDb()
        sql = self.gen.getCustomizationPerspectiveDict(perspective)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting applied customizations: ")+query.lastError().text())
        customDict = dict()
        while query.next():
            jsonDict = json.loads(query.value(0))
            customDict[jsonDict['name']] = jsonDict['array_agg']
        return customDict

    def getPropertyPerspectiveDict(self, settingType, perspective, versionFilter = None):
        self.checkAndOpenDb()
        sql = self.gen.getPropertyPerspectiveDict(settingType, perspective, versionFilter)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting applied customizations: ")+query.lastError().text())
        customDict = dict()
        while query.next():
            jsonDict = json.loads(query.value(0))
            customDict[jsonDict['name']] = jsonDict['array_agg']
        return customDict
    
    def createPropertyTable(self, settingType, useTransaction = True):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.createPropertyTable(settingType)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating Setting table: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def checkIfTableExists(self, schema, tableName):
        self.checkAndOpenDb()
        sql = self.gen.checkIfTableExists(schema, tableName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting checking if table exists: ")+query.lastError().text())
        while query.next():
            if query.value(0):
                return True
        return False

    def checkIfExistsConfigTable(self, settingType):
        settingTable = self.gen.getSettingTable(settingType)
        return self.checkIfTableExists('public', settingTable)
    
    def getRecordFromAdminDb(self, settingType, propertyName, edgvVersion):
        self.checkAndOpenDb()
        sql = self.gen.getRecordFromAdminDb(settingType, propertyName, edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting getting record from adminDb: ")+query.lastError().text())
        retDict = dict()
        while query.next():
            retDict['id'] = query.value(0)
            retDict['name'] = query.value(1)
            retDict['jsondict'] = query.value(2)
            retDict['edgvversion'] = query.value(3)
            #yes, this return is inside the while. Why? Because I said so!
            return retDict
    
    def insertRecordInsidePropertyTable(self, settingType, settingDict, edgvVersion, useTransaction = False):
        self.checkAndOpenDb()
        if edgvVersion != self.getDatabaseVersion():
            raise Exception(self.tr('Invalid property with database version.'))
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.insertRecordInsidePropertyTable(settingType, settingDict)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem inserting record inside property table: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def getPropertyDict(self, settingType):
        self.checkAndOpenDb()
        sql = self.gen.getAllPropertiesFromDb(settingType)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting getting property dict: ")+query.lastError().text())
        propertyDict = dict()
        while query.next():
            edgvVersion = query.value(0)
            name = query.value(1)
            jsonDict = json.loads(query.value(2))
            if edgvVersion not in propertyDict.keys():
                propertyDict[edgvVersion] = dict()
            propertyDict[edgvVersion][name] = jsonDict
        return propertyDict
    
    def insertInstalledRecordIntoAdminDb(self, settingType, recDict, dbOid, useTransaction = False):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.insertInstalledRecordIntoAdminDb(settingType, recDict, dbOid)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem inserting installed record into adminDb: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def removeRecordFromPropertyTable(self, settingType, configName, edgvVersion, useTransaction = False):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.removeRecordFromPropertyTable(settingType, configName, edgvVersion)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem removing installed record into db: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()

    def updateRecordFromPropertyTable(self, settingType, configName, edgvVersion, jsonDict, useTransaction = False):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        if isinstance(jsonDict,dict):
            jsonDict = json.dumps(jsonDict, sort_keys=True, indent=4)
        createSql = self.gen.updateRecordFromPropertyTable(settingType, configName, edgvVersion, jsonDict)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem removing installed record into db: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
    
    def uninstallPropertyOnAdminDb(self, settingType, configName, edgvVersion, useTransaction = False, dbName = None):
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        createSql = self.gen.uninstallPropertyOnAdminDb(settingType, configName, edgvVersion, dbName = dbName)
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem removing installed record into db: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()
            
    def getPrimaryKeyColumn(self, tableName):
        self.checkAndOpenDb()
        sql = self.gen.getPrimaryKeyColumn(tableName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting primary key column: ")+query.lastError().text())
        while query.next():
            return query.value(0)
    
    def dropAllConections(self, dbName):
        """
        Terminates all database conections
        """
        self.checkAndOpenDb()
        if self.checkSuperUser():
            sql = self.gen.dropAllConections(dbName)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                raise Exception(self.tr('Problem dropping database conections: ') + query.lastError().text())
    
    def getAttributesFromTable(self, tableSchema, tableName, typeFilter = [], returnType = 'list'):
        """
        Gets attributes from "tableSchema"."tableName" according to typeFilter
        """
        self.checkAndOpenDb()
        sql = self.gen.getAttributesFromTable(tableSchema, tableName, typeFilter = typeFilter)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting attributes from table {0}.{1}: {2}").format(tableSchema, tableName, query.lastError().text()))
        returnStruct = []
        while query.next():
            if returnType == 'list':
                returnStruct.append(query.value(0))
            else:
                returnStruct.append({'attrName':query.value(0), 'attrType':query.value(1)})
        return returnStruct

    def checkAndCreatePostGISAddonsFunctions(self, useTransaction = True):
        """
        Checks if PostGIS Add-ons functions are installed in the PostgreSQL choosed server.
        If not, it creates the functions based on our git submodule (ext_dep folder)
        """
        self.checkAndOpenDb()
        sql = self.gen.checkPostGISAddonsInstallation()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem creating structure: ')+query.lastError().text())
        created = True
        while query.next():
            if query.value(0) == 0:
                created = False
        if not created:
            current_dir = os.path.dirname(__file__)
            sql_file_path = os.path.join(current_dir, '..', '..', 'ext_dep', 'postgisaddon', 'postgis_addons.sql')
            self.runSqlFromFile(sql_file_path, useTransaction)

    def createAndPopulateCoverageTempTable(self, coverageLayer, useTransaction = True):
        """
        Creates and populates a postgis table with features that compose the coverage layer
        """
        self.checkAndOpenDb()
        if useTransaction:
            self.db.transaction()
        query = QSqlQuery(self.db)
        #getting srid from something like 'EPSG:31983'
        srid = coverageLayer.crs().authid().split(':')[-1]
        #complete table name
        tableName = 'validation.coverage'
        sql = self.gen.createCoverageTempTable(srid)
        if not query.exec_(sql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating coverage temp table: ') + query.lastError().text())
        for feat in coverageLayer.getFeatures():
            # getting only the needed attribute values
            featid = feat['featid']
            classname = feat['classname']
            if not feat.geometry():
                continue
            geometry = binascii.hexlify(feat.geometry().asWkb())
            # values list and attributes list
            values = [featid, classname, geometry]
            attributes = ['featid', 'classname', 'geom']
            # preparing 
            prepareValues = []
            for attr in attributes:
                if attr == 'geom':
                    prepareValues.append("""ST_SetSRID(ST_Multi(:{0}),{1})""".format(attr,str(srid)))
                else:
                    prepareValues.append(':'+attr)
            #getting sql
            insertSql = self.gen.populateTempTable(tableName, attributes, prepareValues)
            query.prepare(insertSql)
            # binding my values to avoid injections
            for i in range(len(attributes)):
                query.bindValue(prepareValues[i], values[i])
            # actual query execution
            if not query.exec_():
                if useTransaction:
                    self.db.rollback()
                raise Exception(self.tr('Problem populating coverage temp table: ') + query.lastError().text())
        indexSql = self.gen.createSpatialIndex(tableName, 'geom')
        if not query.exec_(indexSql):
            if useTransaction:
                self.db.rollback()
            raise Exception(self.tr('Problem creating spatial index on coverage temp table: ') + query.lastError().text())
        if useTransaction:
            self.db.commit()   

    def getGapsAndOverlapsRecords(self, frameTable, geomColumn, useTransaction = True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        self.checkAndOpenDb()
        # checking for gaps with frame
        invalidCoverageRecordsList = []
        sql = self.gen.checkCoverageForGapsWithFrame(frameTable, geomColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting gaps: ")+query.lastError().text())
        while query.next():
            reason = self.tr('Gap between the frame layer and coverage layer')
            geom = query.value(0)
            invalidCoverageRecordsList.append( (0, reason, geom) )
        # checking for overlaps in coverage
        invalidCoverageRecordsList += self.getOverlapsRecords('validation.coverage_temp','geom','id')
        # checking for inner gaps in coverage
        invalidCoverageRecordsList += self.getGapsRecords('validation.coverage_temp','geom','id')
        return invalidCoverageRecordsList

    def getOverlapsRecords(self, table, geomColumn, keyColumn, useTransaction = True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        self.checkAndOpenDb()
        # checking for gaps
        invalidRecordsList = []
        # checking for overlaps
        sql = self.gen.checkCoverageForOverlaps(table, geomColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting overlaps: ")+query.lastError().text())
        while query.next():
            reason = self.tr('Overlap between the features of the layer')
            geom = query.value(0)
            invalidRecordsList.append( (0, reason, geom) )
        return invalidRecordsList
    
    def fillComboBoxProcessOrClasses(self, filterType=None):
        """
        Returns a list of possible classes or processes
        based on existing flags.
        """
        self.checkAndOpenDb()
        sql = self.gen.getProcessOrClassFlags(filterType)
        # list of all filtered flags
        classesOrProcesses = []
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem filtering flags: ")+query.lastError().text())
        classesOrProcesses.append("")
        while query.next():
            classesOrProcesses.append(str(query.value(0)))
        return classesOrProcesses

    def getFilteredFlagsView(self, filterType=None,filteredElement=None):
        """
        Returns a list of flagged features accordingly to what
        was chosen to filter and which element was chosen as such
        (e.g. a process named 'identifyDuplicatedGeometries') 
        """        
        self.checkAndOpenDb()
        sql = self.gen.getFilteredFlagsQuery(filterType, filteredElement)
        outFiltered = []
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem filtering flags: ")+query.lastError().text())
        while query.next():
            outFiltered.append(str(query.value(0)))
        return outFiltered

    def createFilteredFlagsViewTable(self, filterType=None,filteredElement=None):
        """
        Cretas a View Table if it doesn't exist and populates it
        with data considering the users selection of filtering
        """
        self.checkAndOpenDb()
        sql = self.gen.createFilteredFlagsViewTableQuery(filterType, filteredElement)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem filtering flags: ")+query.lastError().text())
        return

    def getGapsRecords(self, table, geomColumn, keyColumn, useTransaction = True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        self.checkAndOpenDb()
        # checking for gaps
        invalidRecordsList = []
        # checking for overlaps
        sql = self.gen.checkCoverageForGaps(table, geomColumn, keyColumn)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting gaps: ")+query.lastError().text())
        while query.next():
            reason = self.tr('Gap between the features of the layer')
            geom = query.value(0)
            invalidRecordsList.append( (0, reason, geom) )
        return invalidRecordsList

    def getNumberOfFlagsByProcess(self, processName):
        """
        Returns the number of flags raised by a process.
        """
        self.checkAndOpenDb()
        sql = self.gen.getFlagsByProcess(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr('Problem getting flags dict: ') + query.lastError().text())
        nrFlags = 0
        while query.next():
            nrFlags += 1
        return nrFlags

    def createValidationHistoryViewTable(self):
        """
        Creates the view table for validation processes history. 
        """
        self.checkAndOpenDb()
        sql = self.gen.createValidationHistoryViewTableQuery()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting validation processes history table: ")+query.lastError().text())
        return
