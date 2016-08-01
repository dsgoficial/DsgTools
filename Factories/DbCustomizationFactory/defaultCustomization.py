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

class DefaultCustomization(DbCustomization):
    def __init__(self, customJson):
        super(DefaultCustomization, self).__init__(customJson)
    
    def buildSql(self, abstractDb):
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        if self.jsonDict['default'].keys() == ['all']:
            classList = abstractDb.getTablesFromDatabase()
            for cl in classList:
                if self.jsonDict['default']['all'].keys() == ['all']:
                    attrList = abstractDb.getColumnsFromTable(cl)
                    value = self.jsonDict['default']['all']['all']
                    for attribute in attrList:
                        sql += """ALTER TABLE ONLY '{0}' ALTER COLUMN {1} SET DEFAULT {2};\n""".format(cl,attribute,str(value))
                else:
                    for attribute in self.jsonDict['default']['all'].keys():
                         value = self.jsonDict['default']['all'][attribute]
                         sql += """ALTER TABLE ONLY '{0}' ALTER COLUMN {1} SET DEFAULT {2};\n""".format(cl,attribute,str(value))
        else:
            for cl in self.jsonDict['default'].keys():
                if self.jsonDict['default'][cl].keys() == ['all']:
                    attrList = abstractDb.getColumnsFromTable(cl)
                    value = self.jsonDict['default'][cl]['all']
                    for attribute in attrList:
                        sql += """ALTER TABLE ONLY '{0}' ALTER COLUMN {1} SET DEFAULT {2};\n""".format(cl,attribute,str(value))
                else:
                    for attribute in self.jsonDict['default'][cl].keys():
                        value = self.jsonDict['default'][cl][attribute]
                        sql += """ALTER TABLE ONLY '{0}' ALTER COLUMN {1} SET DEFAULT {2};\n""".format(cl,attribute,str(value))
        return sql
    
    def buildUndoSql(self):
        #Abstract method. Must be reimplemented in each child.
        pass