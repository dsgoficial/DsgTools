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

class ClassCustomization(DbCustomization):
    def __init__(self, customJson):
        super(ClassCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        Parses customJson and builds sqls to create class
        {'name':name, 'attrs':attrList,'schema':schema}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''''''
        pkClause = ''''''
        for table in self.customJson['ClassToAdd']:
            sql += '''CREATE TABLE "{0}"."{1}" (\n'''.format(table['schema'],table['name'])
            pkClause = None
            paramsSqlList = []
            for params in table['attrs']:
                paramSql = '''    "{0}" {1}'''.format(params['attrName'], params['attrType'])
                if not params['isNullable']:
                    paramSql += ''' NOT NULL'''
                if params['isPk']:
                    pkClause = '''    CONSTRAINT {0}_pk PRIMARY KEY ({1})'''.format(table['name'],params['attrName'])
                paramsSqlList.append(paramSql)
            if pkClause:
                paramsSqlList.append(pkClause)
            sql += ''',\n'''.join(paramsSqlList)
            sql += '''\n);\n'''
        return sql
    
    def buildUndoSql(self):
        '''
        Parses customJson and builds undo sql.
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for table in self.customJson['ClassToAdd']:
            sql += '''DROP TABLE  "{0}"."{1}";\n'''.format(table['schema'],table['name'])
        return sql