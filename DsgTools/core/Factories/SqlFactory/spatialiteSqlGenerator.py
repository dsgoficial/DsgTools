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
from .sqlGenerator import SqlGenerator
from ...dsgEnums import DsgEnums


class SpatialiteSqlGenerator(SqlGenerator):
    def getComplexLinks(self, complex):
        sql = (
            "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from public_complex_schema where complex = '%s'"
            % self._el(complex)
        )
        return sql

    def getComplexTablesFromDatabase(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'complexos_%' ORDER BY name"
        return sql

    def getComplexData(self, complex_schema, complex):
        sql = "SELECT id, nome from %s" % self._qi(complex_schema + "_" + complex)
        return sql

    def getAssociatedFeaturesData(
        self, aggregated_schema, aggregated_class, column_name, complex_uuid
    ):
        table = self._qi(aggregated_schema + "_" + aggregated_class)
        col = self._qi(column_name)
        uuid_val = self._el(complex_uuid)
        if aggregated_schema == "complexos":
            sql = "SELECT id from %s where %s='%s'" % (table, col, uuid_val)
        else:
            sql = "SELECT OGC_FID from %s where %s='%s'" % (table, col, uuid_val)
        return sql

    def getLinkColumn(self, complexClass, aggregatedClass):
        if self.isComplexClass(aggregatedClass):
            sql = (
                "SELECT column_name from public_complex_schema where complex = '%s' and aggregated_class = '%s'"
                % (
                    self._el(complexClass),
                    self._el(aggregatedClass[10:]),
                )
            )
        else:
            sql = (
                "SELECT column_name from public_complex_schema where complex = '%s' and aggregated_class = '%s'"
                % (
                    self._el(complexClass),
                    self._el(aggregatedClass),
                )
            )
        return sql

    def getSrid(self, parameters=dict()):
        sql = "SELECT srid from geometry_columns"
        return sql

    def getTablesFromDatabase(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        return sql

    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        sql = "UPDATE %s SET %s=NULL WHERE id = '%s'" % (
            self._qi(aggregated_class),
            self._qi(link_column),
            self._el(uuid),
        )
        return sql

    def isComplexClass(self, aggregatedClass):
        size = len(aggregatedClass.split("_")[0])
        if size == 9:
            return True
        return False

    def getTemplates(self):
        return None

    def getCreateDatabase(self, name):
        return None

    def insertFrameIntoTable(self, wkt):
        sql = (
            "INSERT INTO public_aux_moldura_a(GEOMETRY) VALUES(GeomFromText('%s'))"
            % self._el(wkt)
        )
        return sql

    def getElementCountFromLayer(self, layer):
        sql = "SELECT count(*) FROM %s" % self._qi(layer)
        return sql

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
        ls = ",".join(self._qi(a) for a in attrList)
        sql = "SELECT %s FROM %s" % (ls, self._qi(layer))
        return sql

    def getStructure(self, edgvVersion):
        sql = ""
        if edgvVersion == "2.1.3":
            sql = "select name, sql from sqlite_master where type = 'table' and (name like 'cb_%' or name like 'complexos_%' or name like 'public_%')"
        elif edgvVersion == "FTer_2a_Ed":
            sql = "select name, sql from sqlite_master where type = 'table' and (name like 'ge_%' or name like 'pe_%' or name like 'complexos_%' or name like 'public_%')"
        elif edgvVersion == "3.0":
            sql = (
                sql
            ) = "select name, sql from sqlite_master where type = 'table' and (name like 'edgv_%' or name like 'complexos_%' or name like 'public_%')"
        return sql

    def getAggregationColumn(self):
        sql = "SELECT DISTINCT column_name FROM public_complex_schema"
        return sql

    def getAggregatorFromId(self, className, id):
        sql = "SELECT id from %s where id ='%s'" % (self._qi(className), self._el(id))
        return sql

    def getAggregatorFromComplexSchema(self, aggregated, aggregationColumn):
        sql = (
            "SELECT complex from public_complex_schema where aggregated_class = '%s' and aggregationColumn = '%s'"
            % (
                self._el(aggregated),
                self._el(aggregationColumn),
            )
        )
        return sql

    def createCustomSort(self):
        return None

    def getRolePrivileges(self, role, dbname):
        return None

    def isSuperUser(self, user):
        return None

    def getInvalidGeom(self, tableSchema, tableName):
        return None

    def makeRelationDict(self, table, in_clause):
        sql = "select code, code_name from %s where code in %s" % (
            self._qi("dominios_" + table),
            in_clause,
        )
        return sql

    def checkValidationStructure(self):
        return None

    def createValidationStructure(self, srid):
        return None

    def getEDGVVersion(self):
        sql = "SELECT edgvversion FROM public_db_metadata LIMIT 1"
        return sql

    def getEDGVVersionAndImplementationVersion(self):
        sql = "SELECT edgvversion, dbimplversion FROM public_db_metadata LIMIT 1"
        return sql

    def getStylesFromDb(self, dbVersion):
        return None

    def getGeomTablesFromGeometryColumns(self, edgvVersion):
        if edgvVersion in ("2.1.3", "FTer_2a_Ed"):
            sql = "select srid, f_geometry_column, type, f_table_name from geometry_columns"
        else:
            sql = "select srid, f_geometry_column, geometry_type, f_table_name from geometry_columns"
        return sql

    def getGeomByPrimitive(self, edgvVersion):
        if edgvVersion in ("2.1.3", "FTer_2a_Ed"):
            sql = """select type, f_table_name from geometry_columns"""
        else:
            sql = """select geometry_type, f_table_name from geometry_columns"""
        return sql

    def getGeomColumnDict(self):
        sql = """select f_geometry_column, f_table_name from geometry_columns"""
        return sql

    def insertFrame(self, scale, mi, inom, frame, srid, geoSrid, paramDict=dict()):
        sql = """INSERT INTO public_aux_moldura_a (mi,inom,escala,GEOMETRY) VALUES ('{0}','{1}','{2}',Transform(ST_GeomFromText('{3}',{4}), {5}))""".format(
            self._el(mi),
            self._el(inom),
            self._el(scale),
            self._el(frame),
            geoSrid,
            srid,
        )
        return sql

    def getElementCountFromLayerV2(self, schema, table, useInheritance):
        layer = "_".join([schema, table])
        return self.getElementCountFromLayer(layer)

    def getFullTablesName(self, name):
        sql = "SELECT f_table_name as name FROM geometry_columns WHERE f_table_name LIKE '%%{0}%%' ORDER BY name".format(
            self._el(name)
        )
        return sql

    def getGeomColumnTupleList(self, edgvVersion, showViews=False):
        if edgvVersion in ("2.1.3", "FTer_2a_Ed"):
            sql = (
                """select f_table_name, f_geometry_column, type from geometry_columns"""
            )
        else:
            sql = """select f_table_name, f_geometry_column, geometry_type from geometry_columns"""
        return sql

    def getQmlRecords(self, layerList):
        sql = """select layername, domainqml from public_domain_qml where layername in ('{0}')""".format(
            "','".join(self._el(l) for l in layerList)
        )
        return sql

    def databaseInfo(self):
        """
        Gets database information to be displayed.
        :return: (str) SQL to executed.
        """
        sql = """
            SELECT f_table_name, f_geometry_column, type, srid
                FROM geometry_columns
                ORDER BY f_table_name ASC"""
        return sql

    def implementationVersion(self):
        """
        Query to retrieve database's implementation version, if available.
        :return: (str) query to database's implementation version (e.g. '5.2').
        """
        return """SELECT dbimplversion FROM public_db_metadata;"""

    def tableFields(self, table):
        """
        Gets all attribute names for a table.
        :param table: (str) table name.
        :return: (list-of-str) list of attribute names.
        """
        return """PRAGMA table_info('{0}');""".format(self._el(table))

    def getImplementationVersion(self):
        sql = """select dbimplversion from public_db_metadata limit 1"""
        return sql
