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
from qgis.core import QgsCredentials, QgsMessageLog, QgsDataSourceURI, QgsFeature, QgsVectorLayer
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii
import psycopg2
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

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

    def connectDatabaseWithParameters(self, host, port, database, user, password):
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
        self.checkAndOpenDb()
        sql = self.gen.getEDGVVersion()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting database version: ")+query.lastError().text())
        version = '-1'
        while query.next():
            version = query.value(0)
        return version
    
    def listGeomClassesFromDatabase(self):
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
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
            schemaList = ['cb', 'complexos']
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
                classDict = self.utils.buildNestedDict(classDict,[str(cl),str(attName)],[value])
        return classDict

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
    
    def convertToSpatialite(self, outputAbstractDb,type=None):
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict) = self.prepareForConversion(outputAbstractDb)
        status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
        return status
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
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
        sql = self.gen.disassociateComplexFromComplex(aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())
    
    def getUsers(self):
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

    def createRole(self, role, dict):
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
        self.checkAndOpenDb()
        sql = self.gen.alterUserPass(user, newpassword)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem altering user\'s password: ') +user+'\n'+query.lastError().text())

    def createUser(self, user, password, isSuperUser):
        self.checkAndOpenDb()
        sql = self.gen.createUser(user, password, isSuperUser)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem creating user: ') +user+'\n'+query.lastError().text())

    def removeUser(self, user):
        self.checkAndOpenDb()
        sql = self.gen.removeUser(user)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem removing user: ') +user+'\n'+query.lastError().text())

    def grantRole(self, user, role):
        self.checkAndOpenDb()
        sql = self.gen.grantRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem granting profile: ') +role+'\n'+query.lastError().text())

    def revokeRole(self, user, role):
        self.checkAndOpenDb()
        sql = self.gen.revokeRole(user, role)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            raise Exception(self.tr('Problem revoking profile: ') +role+'\n'+query.lastError().text())

    def getTablesFromDatabase(self):
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)

        while query.next():
            #table name
            ret.append(query.value(0))

        return ret

    def getRolePrivileges(self, role, dbname):
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
        return 'public.aux_moldura_a'
    
    def getEDGVDbsFromServer(self, parentWidget = None):
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
                raise Exception(self.tr("Problem opening EDGV databases: ")+db.lastError().databaseText())

            query2 = QSqlQuery(db)
            if query2.exec_(self.gen.getEDGVVersion()):
                while query2.next():
                    version = query2.value(0)
                    if version:
                        edvgDbList.append((database,version))
            if parentWidget:
                progress.step()
        return edvgDbList
    
    def getDbsFromServer(self):
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
        self.checkAndOpenDb()
        query = QSqlQuery(self.db)
        if query.exec_(self.gen.isSuperUser(self.db.userName())):
            query.next()
            value = query.value(0)
            return value
        else:
            raise Exception(self.tr("Problem checking user: ")+query.lastError().text())
        return False
    
    def dropDatabase(self, candidateName):
        self.checkAndOpenDb()
        if self.checkSuperUser():
            sql = self.gen.dropDatabase(candidateName)
            query = QSqlQuery(self.db)
            if not query.exec_(sql):
                raise Exception(self.tr('Problem dropping database: ') + query.lastError().text())
    
    def createResolvedDomainViews(self, createViewClause, fromClause):
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
        self.checkAndOpenDb()
        geomList = self.listClassesWithElementsFromDatabase()
        invalidRecordsList = []
        for lyr in geomList:
            tableSchema, tableName = self.getTableSchema(lyr)
            sql = self.gen.getInvalidGeom(tableSchema, tableName)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                raise Exception(self.tr("Problem getting invalid geometries: ")+query.lastError().text())
            while query.next():
                featId = query.value(0)
                reason = query.value(1)
                geom = query.value(2)
                invalidRecordsList.append( (tableSchema+'.'+tableName,featId,reason,geom) )
        return invalidRecordsList
    
    def insertFlags(self, flagTupleList, processName):
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
            return len(flagTupleList)
        else:
            return 0
    
    def deleteProcessFlags(self, processName):
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
        self.checkAndOpenDb()
        sql = self.gen.checkValidationStructure()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
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
        self.checkAndOpenDb()
        sql = self.gen.validationStatus(processName)
        query = QSqlQuery(sql,self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def getValidationStatusText(self, processName):
        self.checkAndOpenDb()
        sql = self.gen.validationStatusText(processName)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem acquiring status: ') + query.lastError().text()) 
        ret = None
        while query.next():
            ret = query.value(0)
        return ret

    def setValidationProcessStatus(self,processName,log,status):
        self.checkAndOpenDb()
        sql = self.gen.setValidationStatusQuery(processName,log,status)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem setting status: ') + query.lastError().text())
    
    def getRunningProc(self):
        self.checkAndOpenDb()
        sql = self.gen.getRunningProc()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting running process: ') + query.lastError().text()) 
        while query.next():
            processName = query.value(0)
            status = query.value(1)
            if status == 3:
                return processName
        return None
    
    def isLyrInDb(self,lyr):
        candidateUri = QgsDataSourceURI(lyr.dataProvider().dataSourceUri())
        candidateHost = candidateUri.host()
        candidatePort = int(candidateUri.port())
        candidateDb = candidateUri.database()
        if self.db.hostName() == candidateHost and self.db.port() == candidatePort and self.db.databaseName() == candidateDb:
            return True
        else:
            return False
        
    def testSpatialRule(self, class_a, necessity, predicate_function, class_b, min_card, max_card, rule):
        self.checkAndOpenDb()
        sql = self.gen.testSpatialRule(class_a, necessity, predicate_function, class_b, min_card, max_card)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
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
        self.checkAndOpenDb()
        sql = self.gen.getDimension(geom)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting dimension: ') + query.lastError().text()) 
        dimension = 0
        while query.next():
            dimension = query.value(0)
        return dimension
    
    def getExplodeCandidates(self):
        self.checkAndOpenDb()
        explodeDict = dict()
        classesWithElem = self.listClassesWithElementsFromDatabase()
        for cl in classesWithElem:
            sql= self.gen.getMulti(cl)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem exploding geometries: ') + query.lastError().text())
            idList = []
            while query.next():
                idList.append(query.value(0))
            if len(idList) > 0:
                explodeDict = self.utils.buildNestedDict(explodeDict, [cl], idList)
        return explodeDict

    def getURI(self, table, useOnly = True, geomColumn = 'geom'):
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
    
    def getDuplicatedGeomRecords(self,classesWithGeom):
        self.checkAndOpenDb()
        duplicatedDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            if tableSchema not in ('validation'):
                sql = self.gen.getDuplicatedGeom(tableSchema, tableName)
                query = QSqlQuery(sql, self.db)
                if not query.isActive():
                    self.db.rollback()
                    self.db.close()
                    raise Exception(self.tr('Problem getting duplicated geometries: ') + query.lastError().text())
                while query.next():
                    duplicatedDict = self.utils.buildNestedDict(duplicatedDict, [cl,query.value(0)], query.value(2))
        return duplicatedDict

    def getSmallAreasRecords(self,classesWithGeom, tol):
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
        self.checkAndOpenDb()
        smallLinesDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getSmallLines(tableSchema, tableName, tol)
            query = QSqlQuery(sql, self.db)
            if not query.isActive():
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem getting small lines: ') + query.lastError().text())
            while query.next():
                smallLinesDict = self.utils.buildNestedDict(smallLinesDict, [cl,query.value(0)], query.value(1))
        return smallLinesDict

    def getVertexNearEdgesRecords(self, tableSchema, tableName, tol):
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
        self.db.transaction()
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

    def removeFeatures(self,cl,idList):
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

    def getOrphanGeomTables(self, loading = False):
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements(loading)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem getting orphan tables: ') + query.lastError().text())
        result = []
        while query.next():
            result.append(query.value(0))
        return result

    def getOrphanGeomTablesWithElements(self, loading = False):
        self.checkAndOpenDb()
        sql = self.gen.getOrphanGeomTablesWithElements(loading)
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
    
    def runQuery(self, sql, errorMsg, params):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(errorMsg + query.lastError().text())
        result = dict()
        key = ','.join(params)
        result[key] = []
        while query.next():
            newElement = []
            for i in range(len(params)):
                newElement.append(query.value(i))
            result[key].append(newElement)
        self.db.commit()
        self.db.close()
        return result

    def snapToGrid(self, cl, tol, srid):
        sql = self.gen.snapToGrid(cl, tol, srid)
        errorMsg = self.tr('Problem snapping to grid: ')
        params = ['id','geom']
        result = self.runQuery(sql, errorMsg, params)
        return result

    def createAndPopulateTempTableFromMap(self, tableName, featureMap):
        srid = self.findEPSG()
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.createTempTable(tableName)
        sqls = sql.split('#')
        for s in sqls:
            if not query.exec_(s):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem creating temp table: ') + query.lastError().text())
        attributes = None
        for feat in featureMap.values():
            if not attributes:
                attributes = [field.name() for field in feat.fields()]
            values = feat.attributes()
            geometry = binascii.hexlify(feat.geometry().asWkb())
            insertSql = self.gen.populateTempTable(tableName, attributes, values, geometry, srid)
            if not query.exec_(insertSql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem populating temp table: ') + query.lastError().text())
        indexSql = self.gen.createSpatialIndex(tableName)
        if not query.exec_(indexSql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem creating spatial index on temp table: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
        
    def dropTempTable(self, tableName):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.dropTempTable(tableName)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem dropping temp table: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def createStyleTable(self):
        self.db.transaction()
        createSql = self.gen.createStyleTable()
        query = QSqlQuery(self.db)
        if not query.exec_(createSql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem creating style table: ') + query.lastError().text())
        self.db.commit()
        self.db.close()

    def checkAndCreateStyleTable(self):
        self.checkAndOpenDb()
        sql = self.gen.checkStyleTable()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr("Problem getting style table: ") + query.lastError().text())
        query.next()
        created = query.value(0)
        if not created:
            self.db.transaction()
            createSql = self.gen.createStyleTable()
            query = QSqlQuery(self.db)
            if not query.exec_(createSql):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Problem creating style table: ') + query.lastError().text())
            self.db.commit()
        self.db.close()
        return created
    
    def getStylesFromDb(self,dbVersion):
        self.checkAndOpenDb()
        sql = self.gen.getStylesFromDb(dbVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
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
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr("Problem getting styles from db: ") + query.lastError().text())
        styleList = []
        query.next()
        qml = query.value(0)
        #TODO: post parse qml to remove possible attribute value type
        if parsing:
            if qml:
                qml = self.utils.parseStyle(qml)
        return qml
    
    def importStyle(self, styleName, table_name, qml, tableSchema):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        parsedQml = self.utils.parseStyle(qml)
        dbName = self.db.databaseName()
        sql = self.gen.importStyle(styleName, table_name, parsedQml, tableSchema,dbName)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem importing style')+ styleName+'/'+ table_name +':' + query.lastError().text())
        self.db.commit()
    
    def updateStyle(self, styleName, table_name, qml, tableSchema):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        parsedQml = self.utils.parseStyle(qml)
        sql = self.gen.updateStyle(styleName, table_name, parsedQml, tableSchema)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem importing style')+ styleName+'/'+ table_name +':' + query.lastError().text())
        self.db.commit()
    
    def deleteStyle(self, styleName):
        self.checkAndOpenDb()
        self.db.transaction()
        query = QSqlQuery(self.db)
        sql = self.gen.deleteStyle(styleName)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem importing style')+ styleName+'/'+ table_name +':' + query.lastError().text())
        self.db.commit()
    
    def importStylesIntoDb(self, styleFolder):
        '''
        path: path to folder
        styleFolder: folder with version. Example: edgv_213/example
        '''
        if self.versionFolderDict[self.getDatabaseVersion()] not in styleFolder:
            raise Exception(self.tr('Style ')+styleFolder+self.tr(' does not match the version of database ') + self.db.databaseName())
        path = os.path.join(os.path.dirname(__file__),'..', '..','Styles')
        stylePath = os.path.join(path,styleFolder)
        availableStyles = os.walk(stylePath).next()[2]
        created = self.checkAndCreateStyleTable()
        for style in availableStyles:
            tableName = style.split('.')[0]
            localStyle = os.path.join(stylePath,style)
            tableSchema = self.getTableSchemaFromDb(tableName)
            #check if style already exists. If it does, update it.
            #if style does not exist, create one.
            if self.getStyle(styleFolder, tableName, parsing = False):
                self.updateStyle(styleFolder, tableName, localStyle, tableSchema)
            else:
                try:
                    self.importStyle(styleFolder, tableName, localStyle, tableSchema)
                except Exception as e:
                    raise Exception(self.tr('Problem importing style ')+style+':'+str(e.args[0]))

    def getTableSchemaFromDb(self,table):
        self.checkAndOpenDb()
        sql = self.gen.getTableSchemaFromDb(table)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr("Problem getting styles from db: ") + query.lastError().text())
        while query.next():
            return query.value(0)
    
    def getAllStylesDict(self, perspective = 'style'):
        '''
        Returns a dict of styles in a form acording to perspective:
            if perspective = 'style'    : [styleName][dbName][tableName] = timestamp
            if perspective = 'database' : [dbName][styleName][tableName] = timestamp 
        '''
        self.checkAndOpenDb()
        sql = self.gen.getAllStylesFromDb()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.rollback()
            self.db.close()
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
    
    def runSqlFromFile(self, sqlFilePath):
        self.checkAndOpenDb()
        file = codecs.open(sqlFilePath, encoding='utf-8', mode='r')
        #file = open(sqlFilePath,'r')
        sql = file.read()
        #sql = sql.replace('\xef\xbb\xbf','')
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem running sql ')+ sqlFilePath +':' + query.lastError().text())
        self.db.commit()
    
    def getStructureDict(self):
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
    
    def getGeomDict(self, getCentroids = False):
        '''
        returns a dict like this:
        {'tablePerspective' : {
            'layerName' :
        '''
        self.checkAndOpenDb()
        sql = self.gen.getGeomTablesFromGeometryColumns()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom tables from db: ")+query.lastError().text())
        geomDict = dict()
        geomDict['primitivePerspective'] = self.getGeomTypeDict()
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
                layerName = table[:-1]+table[-1].replace('c','a')
            if layerName not in geomDict['tablePerspective'].keys():
                geomDict['tablePerspective'][layerName] = dict()
                geomDict['tablePerspective'][layerName]['schema'] = tableSchema
                geomDict['tablePerspective'][layerName]['srid'] = str(srid)
                geomDict['tablePerspective'][layerName]['geometryColumn'] = geometryColumn
                geomDict['tablePerspective'][layerName]['geometryType'] = geometryType
                geomDict['tablePerspective'][layerName]['tableName'] = tableName
        return geomDict
    
    def getDbDomainDict(self):
        '''
        returns a dict like this:
        {'adm_posto_fiscal_a': {
            'columns':{
                'operacional': {'references':'dominios.operacional', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                'situacaofisica': {'references':'dominios.situacaofisica', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                'tipopostofisc': {'references':'dominios.tipopostofisc', 'refPk':'code', 'otherKey':'code_name', 'values':{-dict of code_name:value -}, 'nullable':False, 'constraintList':[1,2,3], 'isMulti':False}
                }
            }
        }
        '''
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
        auxGeomDict = self.getGeomDict()
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
        '''
        returns a dict like this:
        {'asb_dep_abast_agua_a': {
                'finalidade': [2,3,4]
                'construcao': [1,2]
                'situacaofisica': [0,1,2,3,5]
            }
        }
        '''
        self.checkAndOpenDb()
        edgvVersion = self.getDatabaseVersion()
        #gets only schemas of classes with geom, to speed up the process.
        sql = self.gen.getGeomTableConstraints()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            #parse done in parseFkQuery to make code cleaner.
            tableName, attribute, checkList = self.parseCheckConstraintQuery(edgvVersion, query.value(0),query.value(1))
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
        domainReferencedAttribute = subtextList[1].replace(')','') 
        return tableName, fkAttribute, domainTable, domainReferencedAttribute

    def parseCheckConstraintQuery(self, edgvVersion, queryValue0, queryValue1):
        if edgvVersion == '2.1.3':
            return self.parseCheckConstraint213(queryValue0, queryValue1)
        elif edgvVersion == 'FTer_2a_Ed':
            return self.parseCheckConstraintFTer(queryValue0, queryValue1)
        else:
            raise Exception(self.tr("EDGV Version not recognized!"))
    
    def parseCheckConstraint213(self, queryValue0, queryValue1):
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
    
    def parseCheckConstraintFTer(self, queryValue0, queryValue1):
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
        '''
        { 'table_name':[-list of columns-] } 
        '''
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
    
    def getGeomTypeDict(self):
        self.checkAndOpenDb()
        sql = self.gen.getGeomByPrimitive()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom types from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            aux = json.loads(query.value(0))
            geomDict[aux['geomtype']]=aux['classlist']
        return geomDict
    
    def getGeomColumnDict(self):
        '''
        Dict in the form 'geomName':[-list of table names-]
        '''
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
    
    def getLayersFilterByInheritance(self, layerList):
        filter = [i.split('.')[-1] for i in self.getOrphanGeomTables(loading = True)]
        filtered = []
        for lyr in layerList:
            if lyr in filter:
                filtered.append(lyr)
        return filtered

    def getNotNullDictV2(self):
        '''
        Dict in the form 'tableName': { 'schema':-name of the schema'
                                        'attributes':[-list of table names-]}
        '''
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
                otherKey = [key for key in aux.keys() if key <> 'code'][0]
            domainDict[aux[refPk]] = aux[otherKey]
        return domainDict, otherKey
    
    def getGeomStructDict(self):
        '''
        Returns dict in the following format:
        {'tableName': { 'attrName1':isNullable, 'attrName2':isNullable} }
        '''
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
    
    def createDbFromTemplate(self,dbName,version,templateName = 'edgv'):
        #check if created, if created prompt if drop is needed
        self.checkAndOpenDb()
        if templateName == 'edgv':
            templateName = self.getTemplateName(version)
        sql = self.gen.createFromTemplate(dbName,version,templateName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem creating from template: ') + query.lastError().text())
        self.db.close()
    
    def updateDbSRID(self, srid):
        self.checkAndOpenDb()
        self.db.transaction()
        sridSql = self.gen.updateDbSRID(srid)
        query = QSqlQuery(self.db)
        if not query.exec_(sridSql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr('Problem setting srid: ') + query.lastError().text())
        self.db.commit()
        self.db.close()
    
    def checkTemplate(self, version):
        self.checkAndOpenDb()
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
        '''
        version: edgv version
        creates an empty database with the name of a template
        '''
        self.checkAndOpenDb()
        dbName = self.getTemplateName(version)
        try:
            self.dropDatabase(dbName)
        except:
            pass
        self.createDatabase(dbName)
    
    def createDatabase(self, dbName):
        self.checkAndOpenDb()
        sql = self.gen.getCreateDatabase(dbName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr("Problem creating database: ")+query.lastError().text())
        self.db.close()
    
    def getTemplateName(self, version):
        if version == '2.1.3':
            return 'template_213'
        elif version == 'FTer_2a_Ed':
            return 'template_fter_2a_ed'
    
    def setDbAsTemplate(self, version):
        self.checkAndOpenDb()
        dbName = self.getTemplateName(version)
        sql = self.gen.setDbAsTemplate(dbName)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr("Problem setting database as template: ")+query.lastError().text())
        self.db.close()
    
    def getCreationSqlPath(self, version):
        currentPath = os.path.dirname(__file__)
        currentPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool')
        edgvPath = ''
        if version == '2.1.3':
            edgvPath = os.path.join(currentPath, 'sqls', '213', 'edgv213.sql')
        elif version == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, 'sqls', 'FTer_2a_Ed', 'edgvFter_2a_Ed.sql')
        return edgvPath
    
    def setStructureFromSql(self, version, epsg):
        self.checkAndOpenDb()
        edgvPath = self.getCreationSqlPath(version)
        file = codecs.open(edgvPath, encoding='utf-8', mode="r")
        sql = file.read()
        sql = sql.replace('[epsg]', str(epsg))
        file.close()
        commands = sql.split('#')
        self.db.transaction()
        query = QSqlQuery(self.db)
        for command in commands:
            if not query.exec_(command):
                self.db.rollback()
                self.db.close()
                raise Exception(self.tr('Error on database creation! ')+query.lastError().text()+ self.tr(' Db will be dropped.'))
        self.db.commit()
        self.alterSearchPath(version)
        self.setDbAsTemplate(version)
        self.createStyleTable()
    
    def alterSearchPath(self, version):
        self.checkAndOpenDb()
        dbName = self.db.databaseName()
        sql = self.gen.alterSearchPath(dbName, version)
        self.db.transaction()
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.rollback()
            self.db.close()
            raise Exception(self.tr("Problem altering search path: ")+query.lastError().text())
        self.db.commit()
        self.db.close()

    def createFrame(self, type, scale, param):
        if type == 'mi':
            mi = str(param)
            if scale == '250k':
                inom = self.utmGrid.getINomenFromMIR(str(param))
            else:
                inom = self.utmGrid.getINomenFromMI(str(param))
        elif type == 'inom':
            inom = str(param)
            if scale == '250k':
                mi = self.utmGrid.getMIR(inom)
            else:
                mi = self.utmGrid.getMI(inom)
        frame = self.createFrameFromInom(inom)
        self.insertFrame(scale,mi,inom,binascii.hexlify(frame.asWkb()))
    
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