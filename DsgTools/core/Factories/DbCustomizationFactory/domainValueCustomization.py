# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-06
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
# DsgTools Imports
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import (
    DbCustomization,
)


class DomainValueCustomization(DbCustomization):
    def __init__(self, customJson):
        super(DomainValueCustomization, self).__init__(customJson)

    def buildSql(self):
        """
        {'domainName':domainName, 'code':code, 'codeName':codeName}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["domainValue"]:
            sql += """INSERT INTO dominios."{0}" (code, code_name) VALUES ({1}, '{2}');\n""".format(
                modItem["domainName"], modItem["code"], modItem["codeName"]
            )
        return sql

    def buildUndoSql(self):
        """
        {'domainName':domainName, 'valueDict': valueDict}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["domainValue"]:
            sql += """DELETE FROM dominios."{0}" where code = {1};""".format(
                modItem["domainName"], modItem["code"]
            )
        return sql
