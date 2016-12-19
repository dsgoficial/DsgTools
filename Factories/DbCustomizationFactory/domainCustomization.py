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
        email                : borba@dsg.eb.mil.br
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

class DomainCustomization(DbCustomization):
    def __init__(self, customJson):
        super(DomainCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        {'domainName':domainName, 'valueDict': valueDict}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AttributeValueToAdd']:
            for code in modItem['valueDict'].keys():
                sql += '''INSERT INTO dominios."{0}" (code, code_name) VALUES ({1}, '{2}');\n'''.format(modItem['domainName'],code, modItem['valueDict'][code])
        return sql
    
    def buildUndoSql(self):
        '''
        {'domainName':domainName, 'valueDict': valueDict}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AttributeValueToAdd']:
            for code in modItem['valueDict'].keys():
                sql += '''DELETE FROM dominios."{0}" where code = {1};\n'''.format(modItem['domainName'],code)
        return sql