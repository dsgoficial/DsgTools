# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from builtins import object
from ...dsgEnums import DsgEnums


class SqlGenerator(object):
    def getComplexLinks(self, complex):
        return None

    def getComplexTablesFromDatabase(self):
        return None

    def getComplexData(self, complex_schema, complex):
        return None

    def getAssociatedFeaturesData(
        self, aggregated_schema, aggregated_class, column_name, complex_uuid
    ):
        return None

    def getLinkColumn(self, complexClass, aggregatedClass):
        return None

    def getSrid(self):
        return None

    def getEDGVVersion(self):
        sql = "SELECT edgvversion FROM db_metadata LIMIT 1"
        return sql

    def getEDGVVersionAndImplementationVersion(self):
        sql = "SELECT edgvversion, dbimplversion FROM db_metadata LIMIT 1"
        return sql

    def getTablesFromDatabase(self):
        return None

    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        return None

    def getTemplates(self):
        return None

    def getCreateDatabase(self, name):
        return None

    def insertFrameIntoTable(self, wkb):
        return None

    def getDatabasesFromServer(self):
        return None

    def dropDatabase(self, name):
        return None

    def createRole(self, mydict):
        return None

    def dropRole(self, role):
        return None

    def grantRole(self, user, role):
        return None

    def revokeRole(self, user, role):
        return None

    def getRoles(self):
        return None

    def getUserRelatedRoles(self):
        return None

    def getUsers(self):
        return None

    def createUser(self):
        return None

    def removeUser(self):
        return None

    def alterUserPass(self):
        return None

    def validateWithDomain(self):
        return None

    def getNotNullFields(self):
        return None

    def getFeaturesWithSQL(self, layer, attrList):
        return None

    def getStructure(self, edgvVersion):
        return None

    def getAggregationColumn(self):
        return None

    def getAggregatorFromId(self, className, id):
        return None

    def getAggregatorFromComplexSchema(self, aggregated, aggregationColumn):
        return None

    def createCustomSort(self):
        return None

    def getRolePrivileges(self, role, dbname):
        return None

    def isSuperUser(self, user):
        return None

    def getInvalidGeom(self, tableSchema, tableName):
        return None

    def checkValidationStructure(self):
        return None

    def createValidationStructure(self, srid):
        return None

    def getTableExtent(self, tableSchema, tableName):
        return None

    def implementationVersion(self):
        """
        Query to retrieve database's implementation version, if available.
        :return: (str) database's implementation version (e.g. '5.2').
        """
        return None
