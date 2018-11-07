# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-31
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
#DsgTools Imports
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import DbCustomization

class NullityCustomization(DbCustomization):
    def __init__(self, customJson):
        super(NullityCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        {'schema':schema, 'table':table, 'attrName':attrName, 'notNull':notNull}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''''''
        for modItem in self.customJson['ChangeNullity']:
            if modItem['notNull']:
                nullClause = 'SET'
            else:
                nullClause = 'DROP'
            sql += '''ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN "{2}" {3} NOT NULL;\n'''.format(modItem['schema'], modItem['table'], modItem['attrName'], nullClause)
        return sql
    
    def buildUndoSql(self):
        '''
        {'schema':schema, 'table':table, 'attrName':attrName, 'notNull':notNull}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''''''
        for modItem in self.customJson['ChangeNullity']:
            if not modItem['notNull']:
                nullClause = 'SET'
            else:
                nullClause = 'DROP'
            sql += '''ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN "{2}" {3} NOT NULL;\n'''.format(modItem['schema'], modItem['table'], modItem['attrName'], nullClause)
        return sql