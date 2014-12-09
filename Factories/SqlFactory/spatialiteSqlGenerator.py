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
from sqlGenerator import SqlGenerator

class SpatialiteSqlGenerator(SqlGenerator):
    def getComplexTablesFromDatabase(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'complexos_%' ORDER BY name"
        return sql
    
    def getComplexData(self, complex_schema, complex):
        sql = "SELECT id, nome from "+complex_schema+"_"+complex
        return sql

    def getAssociatedFeaturesData(self, aggregated_schema, aggregated_class, column_name, complex_uuid):
        if aggregated_schema == 'complexos':
            sql = "SELECT id from "+aggregated_schema+"_"+aggregated_class+" where "+column_name+"="+'\''+complex_uuid+'\''
        else:
            sql = "SELECT OGC_FID from "+aggregated_schema+"_"+aggregated_class+" where "+column_name+"="+'\''+complex_uuid+'\''
        return sql
    
    def getLinkColumn(self, complexClass, aggregatedClass):
        if self.isComplexClass(aggregatedClass):
            sql = "SELECT column_name from complex_schema where complex = "+complexClass+" and aggregated_class = "+'\''+aggregatedClass[10:]+'\''
        else:
            sql = "SELECT column_name from complex_schema where complex = "+complexClass+" and aggregated_class = "+'\''+aggregatedClass[3:]+'\''
        return sql

    def getSrid(self):
        sql = "SELECT srid from geometry_columns"
        return sql

    def getTablesFromDatabase(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        return sql
    
    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        sql = "UPDATE "+aggregated_class+" SET "+link_column+"=NULL WHERE id = "+'\''+uuid+'\''
        return sql
    
    def isComplexClass(self, aggregatedClass):
        size = len(aggregatedClass.split('_')[0])
        if size == 9:
            return True
        return False