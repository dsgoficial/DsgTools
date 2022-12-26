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
from builtins import map
from DsgTools.core.Factories.DbCustomizationFactory.dbCustomization import (
    DbCustomization,
)


class AttributeCustomization(DbCustomization):
    def __init__(self, customJson):
        super(AttributeCustomization, self).__init__(customJson)

    def buildSql(self):
        """
        self.customJson['AttributeToAdd'] = [{'schemaName':'schema', 'tableName':'nome', 'attrList':[-list of attrDef-], childrenToAlter:[-list of children-]}]
        attrDef = [{'attrName':'nome', 'attrType':'varchar(80)', 'isPk':False, 'isNullable':True, 'references':None, 'defaultValue':None, 'filter':[]}]
        """
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["AttributeToAdd"]:
            schema = modItem["schemaName"]
            table = modItem["tableName"]
            for attr in modItem["attrList"]:
                auxSql = 'ALTER TABLE "{0}"."{1}" ADD COLUMN {2} {3}'.format(
                    schema, table, attr["attrName"], attr["attrType"]
                )
                if not attr["isNullable"]:
                    auxSql += " NOT NULL "
                if "references" in list(attr.keys()):
                    if attr["references"]:
                        if attr["defaultValue"]:
                            auxSql += " REFERENCES {0} DEFAULT {1}".format(
                                attr["references"], attr["defaultValue"]
                            )
                        else:
                            auxSql += " REFERENCES {0}".format(attr["references"])
                auxSql += ";\n"
                sql += auxSql
                if len(attr["filter"]) > 0:
                    sql += """ALTER TABLE "{0}"."{1}" ADD CONSTRAINT "{1}_{2}_check CHECK ({2} = ANY(ARRAY[{3}]);\n""".format(
                        schema,
                        table,
                        attr["attrName"],
                        "::SMALLINT,".join(map(str, attr["filter"])) + "::SMALLINT",
                    )
                    for child in modItem["childrenToAlter"]:
                        sql += """ALTER TABLE "{0}"."{1}" ADD CONSTRAINT "{1}_{2}_check CHECK ({2} = ANY(ARRAY[{3}]);\n""".format(
                            child["schema"],
                            child["table"],
                            attr["attrName"],
                            "::SMALLINT,".join(map(str, attr["filter"])) + "::SMALLINT",
                        )
                if attr["references"]:
                    sql += """ALTER TABLE "{0}"."{1}"\n ADD CONSTRAINT "{1}_{2}_fk FOREIGN KEY({2}) \n  REFERENCES dominios."{3}" (code) MATCH FULL \n  ON UPDATE NO ACTION ON DELETE NO ACTION;\n""".format(
                        schema, table, attr["attrName"], attr["references"]
                    )
                    for child in modItem["childrenToAlter"]:
                        sql += """ALTER TABLE "{0}"."{1}"\n ADD CONSTRAINT "{1}_{2}_fk FOREIGN KEY({2}) \n  REFERENCES dominios."{3}" (code) MATCH FULL \n  ON UPDATE NO ACTION ON DELETE NO ACTION;\n""".format(
                            child["schema"],
                            child["table"],
                            attr["attrName"],
                            attr["references"],
                        )
                if attr["defaultValue"]:
                    sql += """ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN {2} SET DEFAULT {3};""".format(
                        schema, table, attr["attrName"], attr["defaultValue"]
                    )
                    for child in modItem["childrenToAlter"]:
                        sql += """ALTER TABLE ONLY "{0}"."{1}" ALTER COLUMN {2} SET DEFAULT {3};""".format(
                            child["schema"],
                            child["table"],
                            attr["attrName"],
                            attr["defaultValue"],
                        )
        return sql

    def buildUndoSql(self):
        # Abstract method. Must be reimplemented in each child.
        sql = ""
        for modItem in self.customJson["AttributeToAdd"]:
            schema = modItem["schemaName"]
            table = modItem["tableName"]
            for attr in modItem["attrList"]:
                sql += 'ALTER TABLE "{0}"."{1}" DROP COLUMN IF EXISTS "{2}" CASCADE;'.format(
                    schema, table, attr["attrName"]
                )
        return sql
