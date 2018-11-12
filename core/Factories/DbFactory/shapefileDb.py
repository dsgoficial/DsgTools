# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt.QtSql import QSqlQuery, QSqlDatabase
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import QgsCoordinateReferenceSystem 

from .abstractDb import AbstractDb
from DsgTools.core.dsgEnums import DsgEnums

from osgeo import ogr, osr
import os, json

class ShapefileDb(AbstractDb):

    def __init__(self, path=''):
        """
        Constructor
        """
        super(ShapefileDb, self).__init__()
        self.fullpath = path

    def __del__(self):
        """
        Destructor
        """
        if self.isOpen():
            self.fullpath = None

    def isOpen(self):
        """
        Checks if there is a loaded shapefile dataset (directory).
        """
        dn = self.databaseName()
        return dn is None or dn == ''

    def checkAndOpenDb(self):
        """
        Check and open the database
        """
        fullpath = self.databaseName()
        if fullpath is None or fullpath == '':
            raise Exception(self.tr('Error opening database: a (valid) shapefiles path was not given.'))
        # MUDAR AQUI QUANDO HOUVER MÉTODO DE LEITURA DE CAMADAS
        # if :
        #     raise Exception(self.tr('Error opening database: ')+self.db.lastError().text())

    def databaseName(self):
        """
        Gets full path for selected dataset.
        """
        return self.fullpath if self.fullpath is not None else ''

    def getDatabaseName(self):
        """
        Gets the database name
        """
        fullpath = self.databaseName()
        splitChar = '/' if '/' in fullpath else '\\'
        return fullpath.split(splitChar)[-1] if fullpath else ''
    
    def connectDatabase(self, path=None):
        """
        Connects to database.
        :para path: (str) path to directory containing shapefiles.
        """
        if path is None:
            self.connectDatabaseWithGui()
        else:
            self.setDatabaseName(path)
    
    def connectDatabaseWithGui(self):
        """
        Connects to database using user interface dialog.
        """
        fd = QFileDialog()
        filename = fd.getExistingDirectory(caption=self.tr('Select a Path to Shapefiles'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        self.setDatabaseName(filename)

    def setDatabaseName(self, path):
        """
        Connects to database using a string (full path to dir containg .SHP).
        :para path: (str) path to directory containing shapefiles.
        """
        self.fullpath = path
        # MUDAR AQUI O QUE FAZER QUANDO ALTERAR O NOME DA BASE DE DADOS

    def listGeomClassesFromDatabase(self, primitiveFilter = []):
        """
        Gets a list with geometry classes from database.
        """
        self.checkAndOpenDb()
        classList = []
        fileList = next(os.walk(self.databaseName()))[2]
        # if fileList == []:
        #     self.db.close()
        #     raise Exception(self.tr("Problem listing geom classes: ")+query.lastError().text())
        for f in fileList:
            layerName, ext = os.path.splitext(f)
            if ext.lower() != '.shp':
                continue
            if layerName.lower()[-2:] in ["_p", "_l", "_a"]:
                classList.append(layerName)
        return classList

    def getTablesFromDatabase(self):
        """
        Gets all available shapefiles from selected directory.
        """
        self.checkAndOpenDb()
        classList = []
        fileList = next(os.walk(self.databaseName()))[2]
        for f in fileList:
            layerName, ext = os.path.splitext(f)
            if ext.lower() != '.shp':
                continue
            classList.append(layerName)
        return classList

    def listComplexClassesFromDatabase(self):
        """
        Gets a list with complex classes from database
        """
        self.checkAndOpenDb()
        classList = []
        # if not query.isActive():
        #     self.db.close()
        #     raise Exception(self.tr("Problem listing complex classes: ")+query.lastError().text())
        for layerName in self.getTablesFromDatabase():
                tableSchema = layerName.split('_')[0]
                if tableSchema.lower() == 'complexos': 
                    classList.append(layerName)
        return classList   

    def getStructureDict(self):
        """
        Gets database structure according to the edgv version
        """
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
    
    def getTableSchema(self,lyr):
        """
        Gets the table schema.
        :param lyr: (str) layer name.
        :return: (tuple-of-str) layer schema and name, in that order.
        """
        schema = lyr.split('_')[0]
        className = lyr[len(schema) + 1:]
        return (schema, className)
    
    def getDatabaseVersion(self):
        """
        Gets the database EDGV version.
        """
        edgvDict = {'213' : '2.1.3', '213pro' : '2.1.3 Pro', '213fter' : '2.1.3 FTer', '30' : '3.0', '30pro' : '3.0 Pro'}
        self.checkAndOpenDb()
        edgvVersion = 'Non EDGV'
        if 'DSGTools.edgv' in next(os.walk(self.databaseName()))[2]:
            with open(os.path.join(self.databaseName(), 'dsgtools.info'), 'r') as cf:
                config = json.loads(cf.read())
                edgvVersion = config['edgv']
        return edgvDict[edgvVersion] if edgvVersion in edgvDict else 'Non EDGV'

        # if not query.isActive():
        #     raise Exception(self.tr("Problem getting database version: ")+query.lastError().text())
        while query.next():
            version = query.value(0)
        return version
    
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        """
        Obtains the link column between complex and aggregated class
        complexClass: complex class name
        aggregatedClass: aggregated class name
        """
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
        """
        Loads all the features associated to the complex 
        complex: complex class name
        """
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
    
    def isComplexClass(self, layer):
        """
        Checks if a class is a complex class.
        :param layer: (str) class/layer name to be checked.
        :return: (bool) whether class is complex.
        """
        self.checkAndOpenDb()
        return layer in self.listComplexClassesFromDatabase()

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        """
        Disassociates a complex from another complex
        aggregated_class: aggregated class that will be disassociated
        link_column: link column between complex and its aggregated class
        id: complex id (uid) to be disassociated
        """
        pass
        # sql = self.gen.disassociateComplexFromComplex('complexos_'+aggregated_class, link_column, id)
        # query = QSqlQuery(self.db)
        # if not query.exec_(sql):
        #     self.db.close()
        #     raise Exception(self.tr('Problem disassociating complex from complex: ') + '\n' + query.lastError().text())

        # while query.next():
        #     #table name
        #     ret.append(query.value(0))
        # return ret

    def getFrameLayerName(self):
        """
        Gets the frame layer name
        """
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
        """
        returns a dict like this:
        {'tablePerspective' : {
            'layerName' :
        """
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

    def databaseInfo(self):
        """
        Gives information about all tables present in the database. Output is composed by
        schema, layer, geometry column, geometry type and srid, in that order.
        :return: (list-of-dict) database information.
        """
        self.checkAndOpenDb()
        sql = self.gen.databaseInfo()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting geom schemas from db: ")+query.lastError().text())
        out = []
        while query.next():
            rowDict = dict()
            rowDict['schema'] = query.value(0).split('_')[0]
            rowDict['layer'] = query.value(0)[len(rowDict['schema']) + 1 :]
            rowDict['geomCol'] = query.value(1)
            rowDict['geomType'] = query.value(2)
            rowDict['srid'] = str(query.value(3))
            out.append(rowDict)
        return out

    def getType(self):
        """
        Gets the driver name.
        :return: (str) driver name.
        """
        return 'SHP'