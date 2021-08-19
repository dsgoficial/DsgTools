# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-23
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

from .spatialiteDb import SpatialiteDb
from ..SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.dsgEnums import DsgEnums

from osgeo import ogr, osr
import os

class GeopackageDb(SpatialiteDb):
    """
    Geopackage is an OGC format base on SpatiLite, hence, it
    should inherit methods from SpatiaLite driver.
    """
    def __init__(self):
        """
        Constructor.
        """
        super(GeopackageDb, self).__init__()
        self.gen = SqlGeneratorFactory().createSqlGenerator(driver=DsgEnums.DriverGeopackage)
    
    def getDatabaseName(self):
        """
        Gets the database name.
        :return: (str) database name.
        """
        # reimplementation
        return os.path.basename(self.db.databaseName()).split('.gpkg')[0]
    
    def connectDatabaseWithGui(self):
        """
        Connects to database using user interface dialog
        """
        # reimplementation
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a DSGTools Geopackage file'),filter=self.tr('Geopackage file databases (*.gpkg)'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        self.db.setDatabaseName(filename)

    def listClassesFromDatabase(self):
        """
        Gets a list with all classes from database.
        :return: (str) list of all classes in the database.
        """
        self.checkAndOpenDb()
        classList = []
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem listing geom classes: ")+query.lastError().text())
        while query.next():
            classList.append(str(query.value(0)))
        return classList
        
    def getTablesFromDatabase(self):
        """
        Gets all tables from database except for configuration tables.
        """
        # reimplementation
        self.checkAndOpenDb()
        ret = []

        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            self.db.close()
            raise Exception(self.tr("Problem getting tables from database: ")+query.lastError().text())

        while query.next():
            #table name
            table = query.value(0)
            if 'gpkg_' not in table.lower() and 'rtree_' not in table.lower() and table.lower() != 'sqlite_sequence':
                ret.append(table)
        return ret
    
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
    
    def getTableSchemaFromDb(self, table):
        self.checkAndOpenDb()
        sql = self.gen.getFullTablesName(table)
        query = QSqlQuery(sql, self.db)
        if not query.isActive():
            raise Exception(self.tr("Problem getting full table name: ")+query.lastError().text())
        while query.next():
            return query.value(0).split('_')[0]

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
                type_ = query.value(0)
            else:
                type_ = self.getResolvedGeomType(query.value(0))
            tableName = query.value(1)
            layerName = '_'.join(tableName.split('_')[1::])
            if type_ not in list(geomDict.keys()):
                geomDict[type_] = []
            if layerName not in geomDict[type_]:
                geomDict[type_].append(layerName)
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
            geomList.append(
                (
                    query.value(0).split('_')[0],
                    '_'.join(query.value(0).split('_')[1::]),
                    query.value(1),
                    self.getResolvedGeomType(query.value(2)),
                    'BASE TABLE'
                )
            )

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
        return geometryType if geometryType in geomDict.values() else geomDict[int(geometryType)]

    def getType(self):
        """
        Gets the driver name.
        :return: (str) driver name.
        """
        return 'GPKG'
