# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-01-10
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from DsgTools.Factories.DbCustomizationFactory.dbCustomization import DbCustomization

class NewDomainValueCustomization(DbCustomization):
    def __init__(self, customJson):
        super(NewDomainValueCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        {'domainName':domainName, 'code':code, 'code_name':code_name, 'filterToAlterList':filterToAlterList}
        filterToAlterList = [{'schema':schema, 'tableName':tableName, 'attrName':attrName, 'filterName':filterName,'originalFilterList':originalFilterList, 'newValue':newValue}]
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AddDomainValue']:
            sql += '''INSERT INTO dominios."{0}" (code, code_name) VALUES ({1}, '{2}');\n'''.format(modItem['domainName'], code, code_name)
            for filterToAlter in modItem['filterToAlterList']:
                filterList = filterToAlter['originalFilterList']
                if modItem['code'] not in filterList:
                    filterList.append(modItem['code'])
                sql += ''''ALTER TABLE "{0}"."{1}" DROP CONSTRAINT IF EXISTS {1};\n'''.format(filterToAlter['schema'], filterToAlter['tableName'], filterToAlter['filterName'])
                sql += '''ALTER TABLE "{0}"."{1}" ADD CONSTRAINT {2} CHECK ({3} = ANY(ARRAY[{4}]);\n'''.format(filterToAlter['schema'], filterToAlter['tableName'], filterToAlter['filterName'], filterToAlter['attrName'], '::SMALLINT,'.join(map(str,filterList))+'::SMALLINT')
        return sql
    
    def buildUndoSql(self):
        '''
        {'domainName':domainName, 'valueDict': valueDict}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AddDomainValue']:
            sql += '''DELETE FROM dominios."{0}" where code = {1};\n'''.format(modItem['domainName'], modItem['code'])
            for filterToAlter in modItem['filterToAlterList']:
                filterList = filterToAlter['originalFilterList']
                sql += '''ALTER TABLE "{0}"."{1}" DROP CONSTRAINT IF EXISTS "{1}";\n'''.format(filterToAlter['schema'], filterToAlter['tableName'], filterToAlter['filterName'])
                sql += '''ALTER TABLE "{0}"."{1}" ADD CONSTRAINT "{2}" CHECK ({3} = ANY(ARRAY[{4}]);\n'''.format(filterToAlter['schema'], filterToAlter['tableName'], filterToAlter['filterName'], filterToAlter['attrName'], '::SMALLINT,'.join(map(str,filterList))+'::SMALLINT')
        return sql