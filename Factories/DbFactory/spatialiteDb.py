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
from PyQt4.QtGui import QFileDialog
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from osgeo import ogr

class SpatialiteDb(AbstractDb):

    def __init__(self):
        super(SpatialiteDb,self).__init__()
        self.db = QSqlDatabase('QSQLITE')
        self.gen = SqlGeneratorFactory().createSqlGenerator(True)
    
    def getDatabaseName(self):
        return self.db.databaseName().split('.sqlite')[0].split('/')[-1]
    
    def connectDatabase(self, conn = None):
        if conn is None:
            self.connectDatabaseWithGui()
        else:
            self.db.setDatabaseName(conn)
    
    def connectDatabaseWithGui(self):
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a DSGTools Spatialite file'),filter=self.tr('Spatialite file databases (*.sqlite)'))
        self.db.setDatabaseName(filename)
    
    def connectDatabaseWithQSettings(self, name):
        return None

    def connectDatabaseWithParameters(self, host, port, database, user, password):
        return None
    
    def listGeomClassesFromDatabase(self):
        try:
            self.checkAndOpenDb()
        except:
            return []
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        while query.next():
            tableName = str(query.value(0))
            layerName = tableName
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
                tableName = str(query.value(0))
                layerName = tableName
                tableSchema = layerName.split('_')[0]
                if tableSchema == 'complexos': 
                    classList.append(layerName)
        return classList    

    def getConnectionFromQSettings(self, conName):
        return None

    def storeConnection(self, server):
        return None
        
    def getServerConfiguration(self, name):
        return None

    def getStructureDict(self):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        classDict = dict()
        sql = self.gen.getStructure(self.getDatabaseVersion())        
        query = QSqlQuery(sql, self.db)
        while query.next():
            className = str(query.value(0))
            classSql = str(query.value(1))
            if className.split('_')[0] == 'complexos' or className.split('_')[-1] in ['p','l','a']:
                if className not in classDict.keys():
                    classDict[className]=dict()
                classSql = classSql.split(className)[1]
                sqlList = classSql.replace('(','').replace(')','').replace('\"','').replace('\'','').split(',')
                for s in sqlList:
                     fieldName = str(s.strip().split(' ')[0])
                     classDict[className][fieldName]=fieldName

                if 'GEOMETRY' in classDict[className].keys():
                    classDict[className]['GEOMETRY'] = 'geom'
                if 'OGC_FID' in classDict[className].keys():
                    classDict[className]['OGC_FID'] = 'id'

        return classDict
    
    def makeOgrConn(self):
        constring = self.db.databaseName()
        return constring

    def getNotNullDict(self):
        return None

    def getDomainDict(self):
        return None 

    def validateWithOutputDatabaseSchema(self,outputAbstractDb):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        invalidated = self.buildInvalidatedDict()
        inputdbStructure = self.getStructureDict()
        outputdbStructure = outputAbstractDb.getStructureDict()
        domainDict = outputAbstractDb.getDomainDict()
        classes =  self.listClassesWithElementsFromDatabase()
        notNullDict = outputAbstractDb.getNotNullDict()
        
        for inputClass in classes.keys():
            outputClass = self.translateAbstractDbLayerNameToOutputFormat(inputClass,outputAbstractDb)
            (schema,className) = self.getTableSchema(inputClass)
            if outputClass in outputdbStructure.keys():
                outputAttrList = self.reorderTupleList(outputdbStructure[outputClass].keys())
                inputAttrList = self.reorderTupleList(inputdbStructure[inputClass].keys())
                            
                sql = self.gen.getFeaturesWithSQL(inputClass,inputAttrList) 
                query = QSqlQuery(sql, self.db)
                
                while query.next():
                    id = query.value(0)
                    #detects null lines
                    for i in range(len(inputAttrList)):
                        nullLine = True
                        value = query.value(i)
                        if value <> None:
                            nullLine = False
                            break
                    if nullLine:
                        if cl not in invalidated['nullLine'].keys():
                            invalidated['nullLine'][inputClass]=0
                        invalidated['nullLine'][inputClass]+=1
                    
                    #validates pks
                    if id == None and (not nullLine):
                        if cl not in invalidated['nullPk'].keys():
                            invalidated['nullPk'][inputClass]=0
                        invalidated['nullPk'][inputClass]+=1
                    
                    for i in range(len(inputAttrList)):
                        value = query.value(i)
                        #validates domain
                        if outputClass in domainDict.keys():    
                            if inputAttrList[i] in domainDict[outputClass].keys():
                                if value not in domainDict[outputClass][inputAttrList[i]] and (not nullLine):
                                    invalidated = self.utils.buildNestedDict(invalidated, ['notInDomain',inputClass,id,inputAttrList[i]], value)
                        #validates not nulls
                        if outputClass in notNullDict.keys():
                            if outputClass in domainDict.keys():
                                if inputAttrList[i] in notNullDict[outputClass] and inputAttrList[i] not in domainDict[outputClass].keys():
                                    if (value == None) and (not nullLine) and (inputAttrList[i] not in domainDict[outputClass].keys()):
                                        invalidated = self.utils.buildNestedDict(invalidated, ['nullAttribute',inputClass,id,inputAttrList[i]], value)             
                            else:
                                if inputAttrList[i] in notNullDict[outputClass]:
                                    if (value == None) and (not nullLine) and (inputAttrList[i] not in domainDict[outputClass].keys()):
                                        invalidated = self.utils.buildNestedDict(invalidated, ['nullAttribute',inputClass,id,inputAttrList[i]], value)
                        if outputClass in domainDict.keys():
                            if (inputAttrList[i] not in ['geom','GEOMETRY','id','OGC_FID'] and schema <> 'complexos') or (schema == 'complexos' and inputAttrList[i] <> 'id'):
                                if inputAttrList[i] not in outputdbStructure[outputClass].keys():
                                    invalidated = self.utils.buildNestedDict(invalidated, ['attributeNotFoundInOutput',inputClass], [inputAttrList[i]])
                            
            else:
                invalidated['classNotFoundInOutput'].append(inputAttrList)
        return invalidated
    
    def translateAbstractDbLayerNameToOutputFormat(self,lyr,outputAbstractDb):
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return lyr
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return str(lyr.split('_')[0]+'.'+'_'.join(lyr.split('_')[1::]))
    
    def translateOGRLayerNameToOutputFormat(self,lyr,ogrOutput):
        if ogrOutput.GetDriver().name == 'SQLite':
            return lyr
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return str(lyr.split('_')[0]+'.'+'_'.join(lyr.split('_')[1::]))
    
    def getTableSchema(self,lyr):
        schema = lyr.split('_')[0]
        className = '_'.join(lyr.split('_')[1::])
        return (schema, className)
    
    def convertToPostgis(self, outputAbstractDb,type=None):
        try:
            self.checkAndOpenDb()
        except:
            return False
        (inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict) = self.prepareForConversion(outputAbstractDb)
        invalidated = self.validateWithOutputDatabaseSchema(outputAbstractDb)
        hasErrors = self.makeValidationSummary(invalidated)
        if type == 'untouchedData':
            if hasErrors:
                self.signals.updateLog.emit('\n\n\n'+self.tr('Conversion not perfomed due to validation errors! Check log above for more information.'))
                return False
            else:
                status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
                return status
        if type == 'fixData':
            if hasErrors:
                status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict, invalidated)
                return status
            else:
                status = self.translateDS(inputOgrDb, outputOgrDb, fieldMap, inputLayerList, errorDict)
                return status
        return False
    
    def convertToSpatialite(self, outputAbstractDb,type=None):
        return None
    
    def getDatabaseVersion(self):
        try:
            self.checkAndOpenDb()
        except:
            return None
        version = '2.1.3'
        try:
            sqlVersion = self.gen.getEDGVVersion()
            queryVersion =  QSqlQuery(sqlVersion, self.db)
            while queryVersion.next():
                version = queryVersion.value(0)
        except:
            version = '2.1.3'
        return version
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        try:
            self.checkAndOpenDb()
        except:
            return ''
        #query to obtain the link column between the complex and the feature layer
        sql = self.gen.getLinkColumn(complexClass.replace('complexos_', ''), aggregatedClass)
        query = QSqlQuery(sql, self.db)
        column_name = ""
        while query.next():
            column_name = query.value(0)
        return column_name

    def loadAssociatedFeatures(self, complex):
        try:
            self.checkAndOpenDb()
        except:
            return dict()
        associatedDict = dict()
        #query to get the possible links to the selected complex in the combobox
        complexName = complex.replace('complexos_', '')
        sql = self.gen.getComplexLinks(complexName)
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
            if query.value(0) == 'complexos_'+className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        sql = self.gen.disassociateComplexFromComplex('complexos_'+aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())
    
    def getUsers(self):
        return None
    
    def getUserRelatedRoles(self, username):
        return None
    
    def getRoles(self):
        return None
    
    def createRole(self, role, dict):
        pass

    def dropRole(self, role):
        pass

    def alterUserPass(self, user, newpassword):
        pass

    def createUser(self, user, password, isSuperUser):
        pass

    def removeUser(self, user):
        pass

    def grantRole(self, user, role):
        pass

    def revokeRole(self, user, role):
        pass

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
        return None

    def getFrameLayerName(self):
        return 'public_aux_moldura_a'

    def getEDGVDbsFromServer(self,name):
        return None

    def getDbsFromServer(self):
        return None
    
    def checkSuperUser(self):
        return None

    def dropDatabase(self,abstractCandidate):
        return None
