# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from .sqlGenerator import SqlGenerator
from ...dsgEnums import DsgEnums

class GeopackageSqlGenerator(SqlGenerator):

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
            sql = """select table_name, column_name, type from gpkg_geometry_columns"""
        else:
            sql = """select table_name, column_name, geometry_type_name from gpkg_geometry_columns"""
        return sql

    def getTablesFromDatabase(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        return sql
