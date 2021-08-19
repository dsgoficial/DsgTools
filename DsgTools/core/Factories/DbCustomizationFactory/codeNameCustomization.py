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

class CodeNameCustomization(DbCustomization):
    def __init__(self, customJson):
        super(CodeNameCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        {'domainTable':domainTable, 'codeValue':codeValue, 'oldCodeName':oldCodeName, 'newCodeName':newCodeName}
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['CodeNameToChange']:
            sql += '''UPDATE dominios."{0}" SET code_name = '{1}' where code = {2};\n'''.format(modItem['domainTable'], modItem['newCodeName'], modItem['codeValue'])
        return sql
    
    def buildUndoSql(self):
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['CodeNameToChange']:
            sql += '''UPDATE dominios."{0}" SET code_name = '{1}' where code = {2};\n'''.format(modItem['domainTable'], modItem['oldCodeName'], modItem['codeValue'])
        return sql