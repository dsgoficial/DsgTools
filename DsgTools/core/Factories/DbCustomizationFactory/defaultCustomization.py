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
# DsgTools Imports
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import (
    DbCustomization,
)


class DefaultCustomization(DbCustomization):
    def __init__(self, customJson):
        super(DefaultCustomization, self).__init__(customJson)

    def buildSql(self, abstractDb):
        """
        {'schema': schema, 'table': table, 'attrName':attrName, 'oldValue':oldValue, 'newValue':newValue}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = """"""
        for modItem in self.customJson["ChangeDefault"]:
            sql += """ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN "{2}" SET DEFAULT {3};\n""".format(
                modItem["schema"],
                modItem["table"],
                modItem["attrName"],
                modItem["newValue"],
            )
        return sql

    def buildUndoSql(self):
        """
        {'schema': schema, 'table': table, 'attrName':attrName, 'oldValue':oldValue, 'newValue':newValue}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = """"""
        for modItem in self.customJson["ChangeDefault"]:
            sql += """ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN "{2}" SET DEFAULT {3};\n""".format(
                modItem["schema"],
                modItem["table"],
                modItem["attrName"],
                modItem["oldValue"],
            )
        return sql
