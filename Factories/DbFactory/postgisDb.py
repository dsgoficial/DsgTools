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
from qgis.core import QgsCredentials
from osgeo import ogr
from uuid import uuid4

class PostgisDb(AbstractDb):
    
    def __init__(self):
        super(PostgisDb,self).__init__()
        self.db = QSqlDatabase('QPSQL')
        self.gen = SqlGeneratorFactory().createSqlGenerator(False)
        
    def getDatabaseName(self):
        return self.db.databaseName()
    
    def connectDatabase(self,conn=None):
        if conn.split(':')[0] == 'PG':
            connSplit = conn.split(' ')
            parDict = dict()
            for i in connSplit[1::]:
                par = i.split('=')
                parDict[par[0]]=par[1]
            self.connectDatabaseWithParameters(parDict['host'], parDict['port'], parDict['dbname'], parDict['user'], parDict['password'])
        else:
            self.connectDatabaseWithQSettings(conn)

    def connectDatabaseWithGui(self):
        return None

    def connectDatabaseWithParameters(self, host, port, database, user, password):
        self.db.setHostName(host)
        if type(port) != 'int':
            self.db.setPort(int(port))
        else:
            self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        if password == '':
            conInfo = 'host='+host+' port='+port+' dbname='+database
            check = False
            while not check:
                try:
                    (success, user, password) = QgsCredentials.instance().get(conInfo, user, None)
                    if not success:
                        return 
                    self.db.setPassword(password)
                    self.checkAndOpenDb()                    
                    check = True
                    QgsCredentials.instance().put(conInfo, user, password)
                except:
                    pass
        else:
            self.db.setPassword(password)

    def connectDatabaseWithQSettings(self, name):
        (host, port, database, user, password) = self.getConnectionFromQSettings(name)
        self.db.setHostName(host)
        if type(port) != 'int':
            self.db.setPort(int(port))
        else:
            self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        if password == '':
            conInfo = 'host='+host+' port='+port+' dbname='+database
            check = False
            while not check:
                try:
                    (success, user, password) = QgsCredentials.instance().get(conInfo, user, None)
                    if not success:
                        return 
                    self.db.setPassword(password)
                    self.checkAndOpenDb()       
                    check = True
                    QgsCredentials.instance().put(conInfo, user, password)
                except:
                    pass
        else:
            self.db.setPassword(password)

    def getDatabaseVersion(self):
        try:
            self.checkAndOpenDb()
        except:
            return '-1'
        sqlVersion = self.gen.getEDGVVersion()
        queryVersion = QSqlQuery(sqlVersion, self.db)
        while queryVersion.next():
            version = queryVersion.value(0)
        return version
    
    def listGeomClassesFromDatabase(self):
        try:
            self.checkAndOpenDb()
        except:
            return []    
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
        try:
            self.checkAndOpenDb()
        except:
            return []      
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableSchema = query.value(0)
            tableName = query.value(1)
            layerName = tableSchema+'.'+tableName
            if tableSchema == 'complexos':
                classList.append(layerName)
        classList.sort()
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
        try:
            self.checkAndOpenDb()
        except:
            return dict()
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
                if 'geom' in classDict[className].keys():
                    classDict[className]['geom'] = 'GEOMETRY'
                if str(query.value(0)) <> 'complexos' and 'id' in classDict[className].keys():
                    classDict[className]['id'] = 'OGC_FID'
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
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos']
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
                notNullDict[cl] = []
            notNullDict[cl].append(attName)
        return notNullDict

    def getDomainDict(self):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        if self.getDatabaseVersion() == '2.1.3':
            schemaList = ['cb', 'complexos', 'dominios']
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

    def translateAbstractDbLayerNameToOutputFormat(self,lyr,outputAbstractDb):
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return lyr

    def translateOGRLayerNameToOutputFormat(self,lyr,ogrOutput):
        if ogrOutput.GetDriver().name == 'SQLite':
            return str(lyr.split('.')[0]+'_'+'_'.join(lyr.split('.')[1::]))
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return lyr

    def getTableSchema(self,lyr):
        schema = lyr.split('.')[0]
        className = '_'.join(lyr.split('.')[1::])
        return (schema, className)

    def convertToPostgis(self, outputAbstractDb,type=None):
        return None
    
    def convertToSpatialite(self, outputAbstractDb,type=None):
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict) = self.prepareForConversion(outputAbstractDb)
        status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
        return status
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        try:
            self.checkAndOpenDb()
        except:
            return ''
        complexClass = complexClass.replace('complexos.', '')
        #query to obtain the link column between the complex and the feature layer
        sql = self.gen.getLinkColumn(complexClass, aggregatedClass)
        query = QSqlQuery(sql, self.db)
        column_name = ''
        while query.next():
            column_name = query.value(0)
        return column_name

    def loadAssociatedFeatures(self, complex):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        associatedDict = dict()
        complex = complex.replace('complexos.', '')
        #query to get the possible links to the selected complex in the combobox
        sql = self.gen.getComplexLinks(complex)
        query = QSqlQuery(sql, self.db)
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
            while complexQuery.next():
                complex_uuid = complexQuery.value(0)
                name = complexQuery.value(1)

                if not (complex_uuid and name):
                    continue
                
                associatedDict = self.utils.buildNestedDict(associatedDict, [name, complex_uuid, aggregated_class], [])
                
                #query to obtain the id of the associated feature
                sql = self.gen.getAssociatedFeaturesData(aggregated_schema, aggregated_class, column_name, complex_uuid)
                associatedQuery = QSqlQuery(sql, self.db)

                while associatedQuery.next():
                    ogc_fid = associatedQuery.value(0)
                    associatedDict = self.utils.buildNestedDict(associatedDict, [name, complex_uuid, aggregated_class], [ogc_fid])
        return associatedDict
    
    def isComplexClass(self, className):
        try:
            self.checkAndOpenDb()
        except:
            return False
        #getting all complex tables
        query = QSqlQuery(self.gen.getComplexTablesFromDatabase(), self.db)
        while query.next():
            if query.value(0) == className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        sql = self.gen.disassociateComplexFromComplex(aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())
    
    def getUsers(self):
        try:
            self.checkAndOpenDb()
        except:
            return []
        ret = []
        
        sql = self.gen.getUsers()
        query = QSqlQuery(sql, self.db)

        while query.next():
            ret.append(query.value(0))
            
        ret.sort()
        return ret

    def getUserRelatedRoles(self, username):
        try:
            self.checkAndOpenDb()
        except:
            return [], []
        installed = []
        assigned = []

        sql = self.gen.getUserRelatedRoles(username)
        query = QSqlQuery(sql, self.db)

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
        try:
            self.checkAndOpenDb()
        except:
            return []
        ret = []

        sql = self.gen.getRoles()
        query = QSqlQuery(sql, self.db)

        while query.next():
            ret.append(query.value(0))

        ret.sort()
        return ret

    def createRole(self, role, dict):
        try:
            self.checkAndOpenDb()
        except:
            return
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
        try:
            self.checkAndOpenDb()
        except:
            return
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
        try:
            self.checkAndOpenDb()
        except:
            return
        sql = self.gen.alterUserPass(user, newpassword)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem altering user\'s password: ') +user+'\n'+query.lastError().text())

    def createUser(self, user, password, isSuperUser):
        try:
            self.checkAndOpenDb()
        except:
            return
        sql = self.gen.createUser(user, password, isSuperUser)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem creating user: ') +user+'\n'+query.lastError().text())

    def removeUser(self, user):
        try:
            self.checkAndOpenDb()
        except:
            return
        sql = self.gen.removeUser(user)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem removing user: ') +user+'\n'+query.lastError().text())

    def grantRole(self, user, role):
        try:
            self.checkAndOpenDb()
        except:
            return        
        sql = self.gen.grantRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem granting profile: ') +role+'\n'+query.lastError().text())

    def revokeRole(self, user, role):
        try:
            self.checkAndOpenDb()
        except:
            return
        sql = self.gen.revokeRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem revoking profile: ') +role+'\n'+query.lastError().text())

    def getTablesFromDatabase(self):
        try:
            self.checkAndOpenDb()
        except:
            return []
        ret = []

        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)

        while query.next():
            #table name
            ret.append(query.value(0))

        return ret

    def getRolePrivileges(self, role, dbname):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        privilegesDict = dict()
        
        sql = self.gen.getRolePrivileges(role, dbname)
        query = QSqlQuery(sql, self.db)
        
        while query.next():
            schema = query.value(3)
            table = query.value(4)
            privilege = query.value(5)
            
            if schema in ['cb', 'public', 'complexos']:
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
        return 'public.aux_moldura_a'
    
    def getEDGVDbsFromServer(self):
        #Can only be used in postgres database.
        try:
            self.checkAndOpenDb()
        except:
            return []
        query = QSqlQuery(self.gen.getDatabasesFromServer(),self.db)
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
                QtGui.QMessageBox.critical(self, self.tr('Error!'), 'DB :'+database+'| msg: '+db.lastError().databaseText())

            query2 = QSqlQuery(db)
            if query2.exec_(self.gen.getEDGVVersion()):
                while query2.next():
                    version = query2.value(0)
                    if version:
                        edvgDbList.append((database,version))
        return edvgDbList
    
    def checkSuperUser(self):
        try:
            self.checkAndOpenDb()
        except:
            return False
        query = QSqlQuery(self.db)
        if query.exec_(self.gen.isSuperUser(self.db.userName())):
            query.next()
            value = query.value(0)
            return value
        return False
    
    def dropDatabase(self, candidateName):
        try:
            self.checkAndOpenDb()
        except:
            return
        if self.checkSuperUser():
            sql = self.gen.dropDatabase(candidateName)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                raise Exception(self.tr('Problem dropping database: ') + query.lastError().text())
