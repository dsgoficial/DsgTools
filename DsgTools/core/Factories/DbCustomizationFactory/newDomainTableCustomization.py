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
# DsgTools Imports
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import (
    DbCustomization,
)


class NewDomainTableCustomization(DbCustomization):
    def __init__(self, customJson):
        super(NewDomainTableCustomization, self).__init__(customJson)

    def buildSql(self):
        """
        {'domainName':domainName, 'valueDict': valueDict}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["AddDomainTable"]:
            sql += """CREATE TABLE IF NOT EXISTS dominios."{0}";\n""".format(
                modItem["domainName"]
            )
            for code in list(modItem["valueDict"].keys()):
                sql += """INSERT INTO dominios."{0}" (code, code_name) VALUES ({1}, '{2}');\n""".format(
                    modItem["domainName"], code, modItem["valueDict"][code]
                )
        return sql

    def buildUndoSql(self):
        """
        {'domainName':domainName, 'valueDict': valueDict}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["AddDomainTable"]:
            for code in list(modItem["valueDict"].keys()):
                sql += """DROP TABLE IF EXISTS dominios."{0}";""".format(
                    modItem["domainName"]
                )
        return sql
