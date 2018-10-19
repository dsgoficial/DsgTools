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
        sql = "SELECT srid from geometry_columns"
        return sql

    def getGeomTablesFromGeometryColumns(self, edgvVersion):
        if edgvVersion in ('2.1.3','FTer_2a_Ed'):
            sql = 'select srid, f_geometry_column, type, f_table_name from geometry_columns'
        else:
            sql = 'select srid, f_geometry_column, geometry_type, f_table_name from geometry_columns'
        return sql

    def getGeomByPrimitive(self, edgvVersion):
        if edgvVersion in ('2.1.3','FTer_2a_Ed'):
            sql = """select type, f_table_name from geometry_columns"""
        else:
            sql = """select geometry_type, f_table_name from geometry_columns"""
        return sql

    def getGeomColumnDict(self):
        sql = """select f_geometry_column, f_table_name from geometry_columns"""
        return sql

    def getFullTablesName(self, name):
        sql = "SELECT f_table_name as name FROM geometry_columns WHERE f_table_name LIKE '%{0}%' ORDER BY name".format(name)
        return sql

    def getGeomColumnTupleList(self, edgvVersion, showViews = False):
        if edgvVersion in ('2.1.3','FTer_2a_Ed'):
            sql = """select f_table_name, f_geometry_column, type from geometry_columns"""
        else:
            sql = """select f_table_name, f_geometry_column, geometry_type from geometry_columns"""
        return sql
