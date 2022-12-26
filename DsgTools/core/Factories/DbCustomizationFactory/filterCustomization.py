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
from builtins import map
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import (
    DbCustomization,
)


class FilterCustomization(DbCustomization):
    def __init__(self, customJson):
        super(FilterCustomization, self).__init__(customJson)

    def buildSql(self):
        """
        {'schema':schema, 'tableName':tableName, 'attrName':attrName, 'filterName':filterName,'originalFilterList':originalFilterList, 'valueList':valueList, 'operation':operation, 'isMulti':isMulti}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["FilterValue"]:
            filterList = modItem["originalFilterList"]
            if modItem["code"] not in filterList:
                filterList.append(modItem["code"])
            sql += (
                """'ALTER TABLE "{0}"."{1}" DROP CONSTRAINT IF EXISTS {2};\n""".format(
                    modItem["schema"], modItem["tableName"], modItem["filterName"]
                )
            )
            sql += """ALTER TABLE "{0}"."{1}" ADD CONSTRAINT {2} CHECK ({3} = ANY(ARRAY[{4}]);\n""".format(
                modItem["schema"],
                modItem["tableName"],
                modItem["filterName"],
                modItem["attrName"],
                "::SMALLINT,".join(map(str, filterList)) + "::SMALLINT",
            )
        return sql

    def buildUndoSql(self):
        """
        {'domainName':domainName, 'valueDict': valueDict}
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["FilterValue"]:
            filterList = modItem["originalFilterList"]
            sql += (
                """ALTER TABLE "{0}"."{1}" DROP CONSTRAINT IF EXISTS "{2}";\n""".format(
                    modItem["schema"], modItem["tableName"], modItem["filterName"]
                )
            )
            sql += """ALTER TABLE "{0}"."{1}" ADD CONSTRAINT "{2}" CHECK ({3} = ANY(ARRAY[{4}]);\n""".format(
                modItem["schema"],
                modItem["tableName"],
                modItem["filterName"],
                modItem["attrName"],
                "::SMALLINT,".join(map(str, filterList)) + "::SMALLINT",
            )
        return sql
