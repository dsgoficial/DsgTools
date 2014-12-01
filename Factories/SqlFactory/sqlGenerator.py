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
class SqlGenerator:
    def getComplexLinks(self, complex):
        sql = "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = "+complex
        return sql
    
    def getComplexTablesFromDatabase(self):
        return None
    
    def getComplexData(self, complex_schema, complex):
        return None

    def getAssociatedFeaturesData(self, aggregated_schema, aggregated_class, column_name, complex_uuid):
        return None
    
    def getLinkColumn(self, complexClass, aggregatedClass):
        return None
    
    def getSrid(self):
        return None
    
    def getElementCountFromLayer(self, layerItem):
        sql = "SELECT count() FROM "+layerItem[0]+";"
        return sql
    
    def getTablesFromDatabase(self):
        return None
