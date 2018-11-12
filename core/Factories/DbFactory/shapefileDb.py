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
from qgis.utils import iface

from .abstractDb import AbstractDb
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

from osgeo import ogr, osr
import os, json

class ShapefileDb(AbstractDb):

    def __init__(self, path=''):
        """
        Constructor
        """
        super(ShapefileDb, self).__init__()
        self.fullpath = path

    def getLayerLoader(self):
        """
        Gets the shapefile layer loader as designed in DSGTools plugin.
        LAYER LOADERS SHOULD NOT be imported in abstract db. (Shapefile AbstractDb)s are
        a concept extrapolation, and this is specific for this case.
        :return: (ShapefileLayerLoader) shapefile layer loader object. 
        """
        # DIAMOND PROBLEM ALERT: this method requires care to be used; similar methods should be avoided!
        return LayerLoaderFactory().makeLoader(iface, self)

    def __del__(self):
        """
        Destructor
        """
        if self.isOpen():
            self.fullpath = None

    def isOpen(self):
        """
        Checks if there is a loaded shapefile dataset (directory).
        :return: (bool) whether there is a valid dataset open. 
        """
        dn = self.databaseName()
        return dn is None or dn == ''

    def checkAndOpenDb(self):
        """
        Checks and opens the database (in this case, simply checks whether a valid path was chosen).
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
        :return: (str) fullpath as selected.
        """
        return self.fullpath if self.fullpath is not None else ''

    def getDatabaseName(self):
        """
        Gets the database name (the inner directory from dataset fullpath).
        :return: (str) dataset name.
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
        :return: (list-of-str) a list with all spatial SHP found, according to EDGV filing name standards.
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

    def getAttributesFromDbf(self, layer, layerLoader):
        """
        Gets all layer's attributes.
        :param layer: (str) layer name to have its fields retrieved.
        :param layerLoader: (ShapefileLayerLoader) shapefile layer loader.
        :return: (list-of-str) list of field names found.
        """
        # it is considered that layer name is its basename stripped from its extension (e.g. '.shp')
        vl = layerLoader.getLayerByName(layer=layer)
        return [f.name() for f in vl.fields()]

    def getStructureDict(self):
        """
        Gets database structure according to the edgv version.
        :return: (dict) attribute map for each available layer.
        """
        self.checkAndOpenDb()
        classDict = dict()
        # get layer loader - this might be re-thought as it is not a great idea to have a loader here...
        layerLoader = self.getLayerLoader()
        for shpLayer in self.getTablesFromDatabase():
            schema, className = self.getTableSchema(lyr=shpLayer)
            if schema == 'complexos' or className[-2:].lower() in ['_p','_l','_a']:
                if shpLayer not in list(classDict.keys()):
                    classDict[shpLayer] = dict()
                # read attributes from .dbf file
                attributes = []
                for att in self.getAttributesFromDbf(layer=shpLayer, layerLoader=layerLoader):
                    classDict[shpLayer][att]=att
                if 'GEOMETRY' in list(classDict[shpLayer].keys()):
                    classDict[shpLayer]['GEOMETRY'] = 'geom'
                elif 'geometry' in list(classDict[shpLayer].keys()):
                    classDict[shpLayer]['geometry'] = 'geom'
                if 'OGC_FID' in list(classDict[shpLayer].keys()):
                    classDict[shpLayer]['OGC_FID'] = 'id'
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
            with open(os.path.join(self.databaseName(), 'DSGTools.edgv'), 'r') as cf:
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
        geomDict = dict()
        for shpLayer in self.getTablesFromDatabase():
            lastChars = shpLayer[-2:].lower()
            # this is not elegant and it only work for EDGV names... but that's what it is for now
            g = 0 if lastChars == '_p' else 1 if lastChars == '_l' else 2 if lastChars == '_a' else -1
            geomType = self.getQgisResolvideGeomType(geometryType=g)
            schema, layer = self.getTableSchema(lyr=shpLayer)
            if geomType not in geomDict:
                geomDict[geomType] = []
            geomDict[geomType].append(layer)
        return geomDict
    
    def getGeomDict(self, getCentroids = False):
        pass
        # """
        # returns a dict like this:
        # {'tablePerspective' : {
        #     'layerName' :
        # """
        # self.checkAndOpenDb()
        # edgvVersion = self.getDatabaseVersion()
        # sql = self.gen.getGeomTablesFromGeometryColumns(edgvVersion)
        # query = QSqlQuery(sql, self.db)
        # if not query.isActive():
        #     raise Exception(self.tr("Problem getting geom tables from db: ")+query.lastError().text())
        # geomDict = dict()
        # geomDict['primitivePerspective'] = self.getGeomTypeDict()
        # geomDict['tablePerspective'] = dict()
        # while query.next():
        #     isCentroid = False
        #     srid = query.value(0)
        #     if edgvVersion in ('2.1.3','FTer_2a_Ed'):
        #         geometryType = query.value(2)
        #     else:
        #         geometryType = self.getResolvedGeomType(query.value(2))
        #     tableName = query.value(3)
        #     tableSchema = tableName.split('_')[0]
        #     geometryColumn = query.value(1)
        #     layerName = '_'.join(tableName.split('_')[1::])
        #     if layerName not in list(geomDict['tablePerspective'].keys()):
        #         geomDict['tablePerspective'][layerName] = dict()
        #         geomDict['tablePerspective'][layerName]['schema'] = tableSchema
        #         geomDict['tablePerspective'][layerName]['srid'] = str(srid)
        #         geomDict['tablePerspective'][layerName]['geometryColumn'] = geometryColumn
        #         geomDict['tablePerspective'][layerName]['geometryType'] = geometryType
        #         geomDict['tablePerspective'][layerName]['tableName'] = tableName
        # return geomDict
    
    def getGeomColumnDict(self):
        pass
        # """
        # Dict in the form 'geomName':[-list of table names-]
        # """
        # self.checkAndOpenDb()
        # sql = self.gen.getGeomColumnDict()
        # query = QSqlQuery(sql, self.db)
        # if not query.isActive():
        #     raise Exception(self.tr("Problem getting geom column dict: ")+query.lastError().text())
        # geomDict = dict()
        # while query.next():
        #     geomColumn = query.value(0)
        #     tableName = query.value(1)
        #     lyrName = '_'.join(tableName.split('_')[1::])
        #     if geomColumn not in list(geomDict.keys()):
        #         geomDict[geomColumn] = []
        #     geomDict[geomColumn].append(lyrName)
        # return geomDict

    def createFrame(self, type_, scale, param, paramDict = dict()):
        mi, inom, frame = self.prepareCreateFrame(type_, scale, param)
        self.insertFrame(scale, mi, inom, frame.asWkb())
        return frame
    
    def insertFrame(self, scale, mi, inom, frame):
        self.checkAndOpenDb()
        srid = self.findEPSG()
        geoSrid = QgsCoordinateReferenceSystem(int(srid)).geographicCRSAuthId().split(':')[-1]
        ogr.UseExceptions()
        # outputDS = self.buildOgrDatabase()
        outputLayer=outputDS.GetLayerByName(self.getFrameLayerName())
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
        for shpLayer in self.getTablesFromDatabase():
            schema, layer = self.getTableSchema(lyr=shpLayer)
            if table.lower() == layer.lower():
                return schema
        raise Exception(self.tr("Unable to locate file '[SCHEMA]_{}.shp'.").format(table))
    
    def getGeomColumnTupleList(self, showViews = False):
        pass
        # """
        # list in the format [(table_schema, table_name, geometryColumn, geometryType, tableType)]
        # centroids are hidden by default
        # """
        # self.checkAndOpenDb()
        # edgvVersion = self.getDatabaseVersion()
        # sql = self.gen.getGeomColumnTupleList(edgvVersion)
        # query = QSqlQuery(sql, self.db)
        # if not query.isActive():
        #     raise Exception(self.tr("Problem getting geom tuple list: ")+query.lastError().text())
        # geomList = []
        # while query.next():
        #     if edgvVersion in ['2.1.3','FTer_2a_Ed']:
        #         geomList.append((query.value(0).split('_')[0], '_'.join(query.value(0).split('_')[1::]), query.value(1), query.value(2), 'BASE TABLE'))
        #     else:
        #         geomList.append((query.value(0).split('_')[0], '_'.join(query.value(0).split('_')[1::]), query.value(1), self.getResolvedGeomType(int(query.value(2))), 'BASE TABLE'))
        # return geomList

    def getQgisResolvideGeomType(self, geometryType):
        """
        Gets the geometry type name of a given geometry type code, considering
        geometry type as given by QgsVectorLayer().geometryType().
        :param geometryType: (int) geometry type code.
        :return: (str) geometry type name.
        """
        geomDict = {
            0 : 'POINT',
            1 : 'LINESTRING',
            2 : 'POLYGON'
        }
        return geomDict[geometryType] if geometryType in geomDict else ''

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
        out = []
        layerByNameAlias = lambda l : self.getLayerLoader().getLayerByName(layer=l)
        for shpLayer in self.getTablesFromDatabase():
            # run through all .SHP files found (to include complexes and others non-EDGV filenames)
            schema, table = self.getTableSchema(lyr=shpLayer)
            vl = layerByNameAlias(l=shpLayer)
            rowDict = dict()
            rowDict['schema'] = schema
            rowDict['layer'] = table
            rowDict['geomCol'] = 'N/A' # shape doesn't have geom column
            # TODO: check geometry type for shapefile - such as in getResolvedGeomType, for SpatiaLite, for instance
            rowDict['geomType'] = self.getQgisResolvideGeomType(geometryType=vl.geometryType())
            rowDict['srid'] = vl.crs().authid().split(':')[-1]
            out.append(rowDict)
        return out

    def getType(self):
        """
        Gets the driver name.
        :return: (str) driver name.
        """
        return 'SHP'
