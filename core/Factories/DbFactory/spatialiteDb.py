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
        email                : borba.philipe@eb.mil.br
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
from builtins import str
from builtins import range

from qgis.PyQt.QtSql import QSqlQuery, QSqlDatabase
from qgis.PyQt.QtWidgets import QFileDialog

from .abstractDb import AbstractDb
from ..SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from osgeo import ogr, osr
from qgis.core import QgsCoordinateReferenceSystem 

class SpatialiteDb(AbstractDb):

    def __init__(self):
        '''
        Constructor
        '''
        super(SpatialiteDb,self).__init__()
        self.db = QSqlDatabase('QSQLITE')
        self.gen = SqlGeneratorFactory().createSqlGenerator(True)
    
    def getDatabaseName(self):
        '''
        Gets the database name
        '''
        return self.db.databaseName().split('.sqlite')[0].split('/')[-1]
    
    def connectDatabase(self, conn = None):
        '''
        Connects to database
        conn: Database name
        '''
        if conn is None:
            self.connectDatabaseWithGui()
        else:
            self.db.setDatabaseName(conn)
    
    def connectDatabaseWithGui(self):
        '''
        Connects to database using user interface dialog
        '''
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a DSGTools Spatialite file'),filter=self.tr('Spatialite file databases (*.sqlite)'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        self.db.setDatabaseName(filename)
    
    def listGeomClassesFromDatabase(self, primitiveFilter = []):
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
            tableName = str(query.value(0))
            layerName = tableName
            if tableName[-2:] in ["_p", "_l", "_a"]:
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
                tableName = str(query.value(0))
                layerName = tableName
                tableSchema = layerName.split('_')[0]
                if tableSchema == 'complexos': 
                    classList.append(layerName)
        return classList    

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
            className = str(query.value(0))
            classSql = str(query.value(1))
            if className.split('_')[0] == 'complexos' or className.split('_')[-1] in ['p','l','a']:
                if className not in list(classDict.keys()):
                    classDict[className]=dict()
                classSql = classSql.split(className)[1]
                sqlList = classSql.replace('(','').replace(')','').replace('\"','').replace('\'','').split(',')
                for s in sqlList:
                     fieldName = str(s.strip().split(' ')[0])
                     classDict[className][fieldName]=fieldName

                if 'GEOMETRY' in list(classDict[className].keys()):
                    classDict[className]['GEOMETRY'] = 'geom'
                if 'geometry' in list(classDict[className].keys()):
                    classDict[className]['geometry'] = 'geom'
                if 'OGC_FID' in list(classDict[className].keys()):
                    classDict[className]['OGC_FID'] = 'id'

        return classDict
    
    def makeOgrConn(self):
        '''
        Makes a connection string for spatialite databases (e.g just the name)
        '''
        constring = self.db.databaseName()
        return constring

    def validateWithOutputDatabaseSchema(self, outputAbstractDb):
        '''
        Validates the conversion with the output database.
        It generates a dictionary (invalidated) that stores conversion problems
        '''
        self.checkAndOpenDb()
        invalidated = self.buildInvalidatedDict()
        inputdbStructure = self.getStructureDict()
        outputdbStructure = outputAbstractDb.getStructureDict()
        domainDict = outputAbstractDb.getDomainDict()
        classes =  self.listClassesWithElementsFromDatabase()
        notNullDict = outputAbstractDb.getNotNullDict()
        
        for inputClass in list(classes.keys()):
            outputClass = self.translateAbstractDbLayerNameToOutputFormat(inputClass,outputAbstractDb)
            (schema,className) = self.getTableSchema(inputClass)
            if outputClass in list(outputdbStructure.keys()):
                outputAttrList = self.reorderTupleList(list(outputdbStructure[outputClass].keys()))
                inputAttrList = self.reorderTupleList(list(inputdbStructure[inputClass].keys()))
                            
                sql = self.gen.getFeaturesWithSQL(inputClass,inputAttrList) 
                query = QSqlQuery(sql, self.db)
                if not query.isActive():
                    self.db.close()
                    raise Exception(self.tr("Problem executing query: ")+query.lastError().text())
                
                while query.next():
                    id = query.value(0)
                    #detects null lines
                    for i in range(len(inputAttrList)):
                        nullLine = True
                        value = query.value(i)
                        if value != None:
                            nullLine = False
                            break
                    if nullLine:
                        if cl not in list(invalidated['nullLine'].keys()):
                            invalidated['nullLine'][inputClass]=0
                        invalidated['nullLine'][inputClass]+=1
                    
                    #validates pks
                    if id == None and (not nullLine):
                        if cl not in list(invalidated['nullPk'].keys()):
                            invalidated['nullPk'][inputClass]=0
                        invalidated['nullPk'][inputClass]+=1
                    
                    for i in range(len(inputAttrList)):
                        value = query.value(i)
                        #validates domain
                        if outputClass in list(domainDict.keys()):    
                            if inputAttrList[i] in list(domainDict[outputClass].keys()):
                                if value not in domainDict[outputClass][inputAttrList[i]] and (not nullLine):
                                    invalidated = self.utils.buildNestedDict(invalidated, ['notInDomain',inputClass,id,inputAttrList[i]], value)
                        #validates not nulls
                        if outputClass in list(notNullDict.keys()):
                            if outputClass in list(domainDict.keys()):
                                if inputAttrList[i] in notNullDict[outputClass] and inputAttrList[i] not in list(domainDict[outputClass].keys()):
                                    if (value == None) and (not nullLine) and (inputAttrList[i] not in list(domainDict[outputClass].keys())):
                                        invalidated = self.utils.buildNestedDict(invalidated, ['nullAttribute',inputClass,id,inputAttrList[i]], value)             
                            else:
                                if inputAttrList[i] in notNullDict[outputClass]:
                                    try:
                                        if value.isNull():
                                            invalidated = self.utils.buildNestedDict(invalidated, ['nullAttribute',inputClass,id,inputAttrList[i]], value)
                                    except:
                                        if (value == None) and (not nullLine) and (inputAttrList[i] not in list(domainDict[outputClass].keys())):
                                            invalidated = self.utils.buildNestedDict(invalidated, ['nullAttribute',inputClass,id,inputAttrList[i]], value)
                        if outputClass in list(domainDict.keys()):
                            if (inputAttrList[i] not in ['geom','GEOMETRY','geometry','id','OGC_FID'] and schema != 'complexos') or (schema == 'complexos' and inputAttrList[i] != 'id'):
                                if inputAttrList[i] not in list(outputdbStructure[outputClass].keys()):
                                    invalidated = self.utils.buildNestedDict(invalidated, ['attributeNotFoundInOutput',inputClass], [inputAttrList[i]])
                        #validates fk field
                        if 'id_' == inputAttrList[0:3]:
                            if not self.validateUUID(value):
                                if inputAttrList[i] not in list(outputdbStructure[outputClass].keys()):
                                    invalidated = self.utils.buildNestedDict(invalidated, ['nullComplexFk',inputClass], [inputAttrList[i]])
            else:
                invalidated['classNotFoundInOutput'].append(inputAttrList)
        return invalidated
    
    def translateAbstractDbLayerNameToOutputFormat(self, lyr, outputAbstractDb):
        '''
        Translates abstractdb layer name to output format
        lyr: layer name that will be translated
        outputAbstractDb: output database
        '''
        if outputAbstractDb.db.driverName() == 'QSQLITE':
            return lyr
        if outputAbstractDb.db.driverName() == 'QPSQL':
            return str(lyr.split('_')[0]+'.'+'_'.join(lyr.split('_')[1::]))
    
    def translateOGRLayerNameToOutputFormat(self, lyr, ogrOutput):
        '''
        Translates ogr layer name to output format
        lyr: layer name that will be translated
        ogrOutput: ogr output
        '''
        if ogrOutput.GetDriver().name == 'SQLite':
            return lyr
        if ogrOutput.GetDriver().name == 'PostgreSQL':
            return str(lyr.split('_')[0]+'.'+'_'.join(lyr.split('_')[1::]))
    
    def getTableSchema(self,lyr):
        '''
        Gets the table schema
        lyr: layer name
        '''
        schema = lyr.split('_')[0]
        className = '_'.join(lyr.split('_')[1::])
        return (schema, className)
    
    def convertToPostgis(self, outputAbstractDb, type=None):
        '''
        Converts this to a postgis database
        outputAbstractDb: postgis output
        type: conversion type
        '''
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
    
    def getDatabaseVersion(self):
        '''
        Gets the database version
        '''
        self.checkAndOpenDb()
        version = '2.1.3'
        sql = self.gen.getEDGVVersion()
        query = QSqlQuery(sql, self.db)
        # if not query.isActive():
        #     raise Exception(self.tr("Problem getting database version: ")+query.lastError().text())
        while query.next():
            version = query.value(0)
        return version
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        '''
        Obtains the link column between complex and aggregated class
        complexClass: complex class name
        aggregatedClass: aggregated class name
        '''
        self.checkAndOpenDb()
        #query to obtain the link column between the complex and the feature layer
        sql = self.gen.getLinkColumn(complexClass.replace('complexos_', ''), aggregatedClass)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem obtaining link column: ")+query.lastError().text())
        column_name = ""
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
        #query to get the possible links to the selected complex in the combobox
        complexName = complex.replace('complexos_', '')
        sql = self.gen.getComplexLinks(complexName)
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
            
            if aggregated_class.split('_')[-1] not in ['p', 'l', 'a']:
                continue

            #query to obtain the created complexes
            sql = self.gen.getComplexData(complex_schema, complex)
            complexQuery = QSqlQuery(sql, self.db)
            if not complexQuery.isActive():
                self.db.close()
                raise Exception(self.tr("Problem executing query: ")+complexQuery.lastError().text())

            while next(complexQuery):
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
                    raise Exception(self.tr("Problem executing query: ")+associatedQuery.lastError().text())

                while next(associatedQuery):
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
            if query.value(0) == 'complexos_'+className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        '''
        Disassociates a complex from another complex
        aggregated_class: aggregated class that will be disassociated
        link_column: link column between complex and its aggregated class
        id: complex id (uid) to be disassociated
        '''
        sql = self.gen.disassociateComplexFromComplex('complexos_'+aggregated_class, link_column, id)
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            self.db.close()
            raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())

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

    def getFrameLayerName(self):
        '''
        Gets the frame layer name
        '''
        return 'public_aux_moldura_a'

    def getOrphanGeomTablesWithElements(self, loading = False):
        return []
    
    def getOrphanGeomTables(self):
        return []
    
    def checkAndCreateStyleTable(self):
        return None

    def getStylesFromDb(self,dbVersion):
        return None

    def getGeomTypeDict(self, loadCentroids=False):
        self.checkAndOpenDb()
        edgvVersion = self.getDatabaseVersion()
        sql = self.gen.getGeomByPrimitive(edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom types from db: ")+query.lastError().text())
        geomDict = dict()
        while query.next():
            if edgvVersion in ('2.1.3','FTer_2a_Ed'):
                type = query.value(0)
            else:
                type = self.getResolvedGeomType(query.value(0))
            tableName = query.value(1)
            layerName = '_'.join(tableName.split('_')[1::])
            if type not in list(geomDict.keys()):
                geomDict[type] = []
            if layerName not in geomDict[type]:
                geomDict[type].append(layerName)
        return geomDict
    
    def getGeomDict(self, getCentroids = False):
        '''
        returns a dict like this:
        {'tablePerspective' : {
            'layerName' :
        '''
        self.checkAndOpenDb()
        edgvVersion = self.getDatabaseVersion()
        sql = self.gen.getGeomTablesFromGeometryColumns(edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom tables from db: ")+query.lastError().text())
        geomDict = dict()
        geomDict['primitivePerspective'] = self.getGeomTypeDict()
        geomDict['tablePerspective'] = dict()
        while query.next():
            isCentroid = False
            srid = query.value(0)
            if edgvVersion in ('2.1.3','FTer_2a_Ed'):
                geometryType = query.value(2)
            else:
                geometryType = self.getResolvedGeomType(query.value(2))
            tableName = query.value(3)
            tableSchema = tableName.split('_')[0]
            geometryColumn = query.value(1)
            layerName = '_'.join(tableName.split('_')[1::])
            if layerName not in list(geomDict['tablePerspective'].keys()):
                geomDict['tablePerspective'][layerName] = dict()
                geomDict['tablePerspective'][layerName]['schema'] = tableSchema
                geomDict['tablePerspective'][layerName]['srid'] = str(srid)
                geomDict['tablePerspective'][layerName]['geometryColumn'] = geometryColumn
                geomDict['tablePerspective'][layerName]['geometryType'] = geometryType
                geomDict['tablePerspective'][layerName]['tableName'] = tableName
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
            geomColumn = query.value(0)
            tableName = query.value(1)
            lyrName = '_'.join(tableName.split('_')[1::])
            if geomColumn not in list(geomDict.keys()):
                geomDict[geomColumn] = []
            geomDict[geomColumn].append(lyrName)
        return geomDict

    def createFrame(self, type, scale, param, paramDict = dict()):
        mi, inom, frame = self.prepareCreateFrame(type, scale, param)
        self.insertFrame(scale, mi, inom, frame.asWkb())
        return frame
    
    def insertFrame(self, scale, mi, inom, frame):
        self.checkAndOpenDb()
        srid = self.findEPSG()
        geoSrid = QgsCoordinateReferenceSystem(int(srid)).geographicCRSAuthId().split(':')[-1]
        ogr.UseExceptions()
        outputDS = self.buildOgrDatabase()
        outputLayer=outputDS.GetLayerByName('public_aux_moldura_a')
        newFeat=ogr.Feature(outputLayer.GetLayerDefn())
        auxGeom = ogr.CreateGeometryFromWkb(frame)
        #set geographic srid from frame
        geoSrs = ogr.osr.SpatialReference()
        geoSrs.ImportFromEPSG(int(geoSrid))
        auxGeom.AssignSpatialReference(geoSrs)
        #reproject geom
        outSpatialRef = outputLayer.GetSpatialRef()
        coordTrans = osr.CoordinateTransformation(geoSrs, outSpatialRef)
        auxGeom.Transform(coordTrans)
        newFeat.SetGeometry(auxGeom)
        newFeat.SetField('mi', mi)
        newFeat.SetField('inom', inom)
        newFeat.SetField('escala', str(scale))
        out=outputLayer.CreateFeature(newFeat)
        outputDS.Destroy()
    
    def getTableSchemaFromDb(self, table):
        self.checkAndOpenDb()
        sql = self.gen.getFullTablesName(table)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting full table name: ")+query.lastError().text())
        while query.next():
            return query.value(0).split('_')[0]
    
    def getGeomColumnTupleList(self, showViews = False):
        """
        list in the format [(table_schema, table_name, geometryColumn, geometryType, tableType)]
        centroids are hidden by default
        """
        self.checkAndOpenDb()
        edgvVersion = self.getDatabaseVersion()
        sql = self.gen.getGeomColumnTupleList(edgvVersion)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom tuple list: ")+query.lastError().text())
        geomList = []
        while query.next():
            if edgvVersion in ['2.1.3','FTer_2a_Ed']:
                geomList.append((query.value(0).split('_')[0], '_'.join(query.value(0).split('_')[1::]), query.value(1), query.value(2), 'BASE TABLE'))
            else:
                geomList.append((query.value(0).split('_')[0], '_'.join(query.value(0).split('_')[1::]), query.value(1), self.getResolvedGeomType(int(query.value(2))), 'BASE TABLE'))
        return geomList
    
    def getResolvedGeomType(self, geometryType):
        geomDict = {0:'GEOMETRY',
                    1:'POINT',
                    2:'LINESTRING',
                    3:'POLYGON',
                    4:'MULTIPOINT',
                    5:'MULTILINESTRING',
                    6:'MULTIPOLYGON',
                    7:'GEOMETRYCOLLECTION',
                    8:'CIRCULARSTRING',
                    9:'COMPOUNDCURVE',
                    10:'CURVEPOLYGON',
                    11:'MULTICURVE',
                    12:'MULTISURFACE',
                    13:'CURVE',
                    14:'SURFACE'}
        return geomDict[geometryType]