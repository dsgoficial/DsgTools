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
from .spatialiteSqlGenerator import SpatialiteSqlGenerator
from DsgTools.core.dsgEnums import DsgEnums

class GeopackageSqlGenerator(SpatialiteSqlGenerator):

    def getEDGVVersion(self):
        """
        Gets the version of the data model.
        """
        sql = "SELECT edgvversion FROM db_metadata LIMIT 1"
        return sql

    def getSrid(self, parameters = dict()):
        """
        Gets SRID for selected database (it is assumed all tables have the same SRID).
        """
        sql = "SELECT srs_id FROM gpkg_geometry_columns"
        return sql

    def getGeomTablesFromGeometryColumns(self, edgvVersion):
        """
        Gets a dict for tables and their geometry columns.
        """
        sql = 'select srs_id, column_name, geometry_type_name, table_name from gpkg_geometry_columns'
        return sql

    def getGeomByPrimitive(self, edgvVersion):
        sql = """select geometry_type_name, table_name from gpkg_geometry_columns"""
        return sql

    def getGeomColumnDict(self):
        sql = """select column_name, table_name from gpkg_geometry_columns"""
        return sql

    def getFullTablesName(self, name):
        sql = "SELECT table_name as name FROM gpkg_geometry_columns WHERE table_name LIKE '%{0}%' ORDER BY name".format(name)
        return sql

    def getGeomColumnTupleList(self, edgvVersion, showViews = False):
        if edgvVersion in ('2.1.3','FTer_2a_Ed'):
            sql = """select table_name, column_name, geometry_type_name from gpkg_geometry_columns"""
        else:
            sql = """select table_name, column_name, geometry_type_name from gpkg_geometry_columns"""
        return sql

    def getTablesFromDatabase(self):
        sql = "SELECT tbl_name as name, type FROM sqlite_master WHERE type='table' ORDER BY name"
        return sql

    def getStructure(self,edgvVersion):
        sql = ''
        if edgvVersion == '2.1.3':
            sql = 'select tbl_name as name, sql from sqlite_master where type = \'table\' and (name like \'cb_%\' or name like \'complexos_%\' or name like \'public_%\')'
        elif edgvVersion == 'FTer_2a_Ed':
            sql = 'select tbl_name as name, sql from sqlite_master where type = \'table\' and (name like \'ge_%\' or name like \'pe_%\' or name like \'complexos_%\' or name like \'public_%\')' 
        elif edgvVersion == '3.0':
            sql = sql = 'select tbl_name as name, sql from sqlite_master where type = \'table\' and (name like \'edgv_%\' or name like \'complexos_%\' or name like \'public_%\')'
        return sql

    def getComplexTablesFromDatabase(self):
        sql = "SELECT tbl_name as name FROM sqlite_master WHERE type='table' AND name LIKE 'complexos_%' ORDER BY name"
        return sql

    def databaseInfo(self):
        """
        Gets database information to be displayed.
        :return: (str) SQL to executed.
        """
        sql = """
            SELECT table_name, column_name, geometry_type_name, srs_id
                FROM gpkg_geometry_columns
                ORDER BY table_name ASC"""
        return sql
