# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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


class GeopackageSqlGenerator(SqlGenerator):
    # ------------------------------------------------------------------ #
    # Methods copied from SpatialiteSqlGenerator (complex / frame / misc) #
    # ------------------------------------------------------------------ #

    def getComplexLinks(self, complex):
        sql = (
            "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from public_complex_schema where complex = '%s'"
            % self._el(complex)
        )
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

    def insertFrameIntoTable(self, wkt):
        sql = (
            "INSERT INTO public_aux_moldura_a(GEOMETRY) VALUES(GeomFromText('%s'))"
            % self._el(wkt)
        )
        return sql

    def getElementCountFromLayer(self, layer):
        sql = "SELECT count(*) FROM %s" % self._qi(layer)
        return sql

    def getFeaturesWithSQL(self, layer, attrList):
        ls = ",".join(self._qi(a) for a in attrList)
        sql = "SELECT %s FROM %s" % (ls, self._qi(layer))
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

    def makeRelationDict(self, table, in_clause):
        sql = "select code, code_name from %s where code in %s" % (
            self._qi("dominios_" + table),
            in_clause,
        )
        return sql

    def getQmlRecords(self, layerList):
        sql = """select layername, domainqml from public_domain_qml where layername in ('{0}')""".format(
            "','".join(self._el(l) for l in layerList)
        )
        return sql

    def implementationVersion(self):
        return """SELECT dbimplversion FROM public_db_metadata;"""

    def tableFields(self, table):
        return """PRAGMA table_info('{0}');""".format(self._el(table))

    def getImplementationVersion(self):
        sql = """select dbimplversion from public_db_metadata limit 1"""
        return sql

    # ------------------------------------------------------------------ #
    # GeoPackage-specific overrides                                        #
    # ------------------------------------------------------------------ #

    def getEDGVVersion(self):
        sql = "SELECT edgvversion FROM db_metadata LIMIT 1"
        return sql

    def getSrid(self, parameters=dict()):
        sql = "SELECT srs_id FROM gpkg_geometry_columns"
        return sql

    def getGeomTablesFromGeometryColumns(self, edgvVersion):
        sql = "select srs_id, column_name, geometry_type_name, table_name from gpkg_geometry_columns"
        return sql

    def getGeomByPrimitive(self, edgvVersion):
        sql = """select geometry_type_name, table_name from gpkg_geometry_columns"""
        return sql

    def getGeomColumnDict(self):
        sql = """select column_name, table_name from gpkg_geometry_columns"""
        return sql

    def getFullTablesName(self, name):
        sql = "SELECT table_name as name FROM gpkg_geometry_columns WHERE table_name LIKE '%%{0}%%' ORDER BY name".format(
            self._el(name)
        )
        return sql

    def getGeomColumnTupleList(self, edgvVersion, showViews=False):
        sql = """select table_name, column_name, geometry_type_name from gpkg_geometry_columns"""
        return sql

    def getTablesFromDatabase(self):
        sql = "SELECT tbl_name as name, type FROM sqlite_master WHERE type='table' ORDER BY name"
        return sql

    def getStructure(self, edgvVersion):
        sql = ""
        if edgvVersion == "2.1.3":
            sql = "select tbl_name as name, sql from sqlite_master where type = 'table' and (name like 'cb_%' or name like 'complexos_%' or name like 'public_%')"
        elif edgvVersion == "FTer_2a_Ed":
            sql = "select tbl_name as name, sql from sqlite_master where type = 'table' and (name like 'ge_%' or name like 'pe_%' or name like 'complexos_%' or name like 'public_%')"
        elif edgvVersion == "3.0":
            sql = "select tbl_name as name, sql from sqlite_master where type = 'table' and (name like 'edgv_%' or name like 'complexos_%' or name like 'public_%')"
        return sql

    def getComplexTablesFromDatabase(self):
        sql = "SELECT tbl_name as name FROM sqlite_master WHERE type='table' AND name LIKE 'complexos_%' ORDER BY name"
        return sql

    def databaseInfo(self):
        sql = """
            SELECT table_name, column_name, geometry_type_name, srs_id
                FROM gpkg_geometry_columns
                ORDER BY table_name ASC"""
        return sql
