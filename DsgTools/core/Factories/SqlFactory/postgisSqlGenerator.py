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
from builtins import str
from builtins import map
from .sqlGenerator import SqlGenerator
from ...dsgEnums import DsgEnums

DB_ENCODING = "utf-8"


class PostGISSqlGenerator(SqlGenerator):
    def getComplexLinks(self, complex):
        sql = (
            "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = '"
            + complex
            + "'"
        )
        return sql

    def getComplexTablesFromDatabase(self):
        sql = "select distinct table_name from information_schema.columns where table_schema = 'complexos'  ORDER BY table_name"
        return sql

    def getComplexData(self, complex_schema, complex):
        sql = "SELECT id, nome from " + complex_schema + "." + complex
        return sql

    def getAssociatedFeaturesData(
        self, aggregated_schema, aggregated_class, column_name, complex_uuid
    ):
        sql = (
            "SELECT id from only "
            + aggregated_schema
            + "."
            + aggregated_class
            + " where "
            + column_name
            + "="
            + "'"
            + complex_uuid
            + "'"
        )
        return sql

    def getLinkColumn(self, complexClass, aggregatedClass):
        sql = (
            "SELECT column_name from complex_schema where complex = '"
            + complexClass
            + "'"
            + " and aggregated_class = "
            + "'"
            + aggregatedClass
            + "'"
        )
        return sql

    def getSrid(self, parameters=dict()):
        if parameters == dict():
            sql = "SELECT DISTINCT srid from geometry_columns WHERE f_table_schema <> 'tiger' and f_table_schema <> 'topology' LIMIT 1"
        else:
            whereClauseList = []
            if "tableSchema" in list(parameters.keys()):
                whereClauseList.append(
                    """f_table_schema = '{0}'""".format(parameters["tableSchema"])
                )
            if "tableName" in list(parameters.keys()):
                whereClauseList.append(
                    """f_table_name = '{0}'""".format(parameters["tableName"])
                )
            if "geometryColumn" in list(parameters.keys()):
                whereClauseList.append(
                    """f_geometry_column = '{0}'""".format(parameters["geometryColumn"])
                )
            whereClause = " AND ".join(whereClauseList)
            sql = """SELECT DISTINCT srid from geometry_columns WHERE {0} LIMIT 1""".format(
                whereClause
            )
        return sql

    def getTablesFromDatabase(self):
        sql = "select distinct table_schema, table_name from information_schema.columns where (table_schema <> 'dominios' and table_schema <> 'topology')"
        return sql

    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        sql = (
            "UPDATE complexos."
            + aggregated_class
            + " SET "
            + link_column
            + "=NULL WHERE id = "
            + "'"
            + uuid
            + "'"
        )
        return sql

    def getTemplates(self):
        sql = "SELECT datname FROM pg_database WHERE datistemplate = true;"
        return sql

    def allowConnections(self, name):
        sql = (
            "ALTER DATABASE "
            + name
            + " SET search_path = public, topology, cb, cc, complexos, ct;"
        )
        return sql

    def loadLayerFromDatabase(self, layer_name, pkColumn="id"):
        layer_name = '"."'.join(layer_name.replace('"', "").split("."))
        sql = """{1} in (SELECT {1} FROM ONLY "{0}")""".format(layer_name, pkColumn)
        return sql

    def loadLayerFromDatabaseUsingInh(self, layer_name, pkColumn="id"):
        layer_name = '"."'.join(layer_name.replace('"', "").split("."))
        sql = """{1} in (SELECT {1} FROM ONLY "{0}")""".format(layer_name, pkColumn)
        return sql

    def getCreateDatabase(self, name, dropIfExists=False):
        sql = ""
        if dropIfExists:
            sql += """DROP DATABASE IF EXISTS "{0}";""".format(name)
        sql += """CREATE DATABASE "{0}";""".format(name)
        return sql

    def insertFrameIntoTable(self, wkt):
        sql = "INSERT INTO aux_moldura_a(geom) VALUES(ST_GeomFromText(" + wkt + "))"
        return sql

    def getElementCountFromLayer(self, table):
        sql = "SELECT count(id) FROM ONLY {0} limit 1".format(table)
        return sql

    def getElementCountFromLayerV2(self, schema, table, useInheritance):
        if useInheritance == False:
            sql = """SELECT count(a) FROM ( SELECT * FROM ONLY "{0}"."{1}" ) as a""".format(
                schema, table
            )
        else:
            sql = """SELECT count(a) FROM ( SELECT * FROM "{0}"."{1}" ) as a""".format(
                schema, table
            )
        return sql

    def getElementCountFromLayerWithInh(self, layer):
        sql = "SELECT count(*) FROM " + layer
        return sql

    def getDatabasesFromServer(self):
        sql = "SELECT datname FROM pg_database where datname <> 'postgres' and datname <> 'template' and datname <> 'template0' and datname <> 'template_postgis' and datistemplate = 'f'"
        return sql

    def dropDatabase(self, name):
        sql = """DROP DATABASE "{0}" """.format(name)
        return sql

    def createRole(self, roleName, mydict):
        sql = """CREATE ROLE "{0}" with NOLOGIN REPLICATION;\n""".format(roleName)
        for db in list(mydict.keys()):
            for schema in list(mydict[db].keys()):
                for cat in list(mydict[db][schema].keys()):
                    for tableName in list(mydict[db][schema][cat].keys()):
                        table = '''"{0}"."{1}"'''.format(schema, tableName)
                        read = mydict[db][schema][cat][tableName]["read"]
                        write = mydict[db][schema][cat][tableName]["write"]
                        if write == "2":
                            sql += """GRANT ALL ON {0} TO "{1}";\n""".format(
                                table, roleName
                            )
                        elif read == "2":
                            sql += """GRANT SELECT ON {0} TO "{1}";\n""".format(
                                table, roleName
                            )
                sql += """GRANT ALL ON SCHEMA "{0}" TO "{1}";\n""".format(
                    schema, roleName
                )
                sql += """REVOKE CREATE ON SCHEMA "{0}" FROM "{1}";\n""".format(
                    schema, roleName
                )
                sql += """GRANT USAGE ON SCHEMA "{0}" TO "{1}";\n""".format(
                    schema, roleName
                )
                sql += """GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA "{0}" TO "{1}";\n""".format(
                    schema, roleName
                )
                sql += """GRANT USAGE ON ALL SEQUENCES IN SCHEMA "{0}" TO "{1}";\n""".format(
                    schema, roleName
                )

        # not needed anymore due to our generic approach
        # sql += """GRANT SELECT ON db_metadata TO "{0}";\n""".format(roleName)
        sql += """GRANT SELECT ON public.geometry_columns TO "{0}";\n""".format(
            roleName
        )
        sql += """GRANT ALL ON ALL TABLES IN SCHEMA information_schema TO "{0}";\n""".format(
            roleName
        )
        sql += """GRANT ALL ON ALL TABLES IN SCHEMA pg_catalog TO "{0}";\n""".format(
            roleName
        )
        sql += """GRANT ALL ON SCHEMA information_schema TO "{0}";\n""".format(roleName)
        sql += """GRANT ALL ON SCHEMA pg_catalog TO "{0}";\n""".format(roleName)
        sql += """REVOKE CREATE ON SCHEMA information_schema FROM "{0}";\n""".format(
            roleName
        )
        sql += """REVOKE CREATE ON SCHEMA pg_catalog FROM "{0}";\n""".format(roleName)
        sql += """GRANT USAGE ON SCHEMA information_schema TO "{0}";\n""".format(
            roleName
        )
        sql += """GRANT USAGE ON SCHEMA pg_catalog TO "{0}";\n""".format(roleName)
        sql += """GRANT USAGE ON ALL SEQUENCES IN SCHEMA information_schema TO "{0}";\n""".format(
            roleName
        )
        sql += """GRANT USAGE ON ALL SEQUENCES IN SCHEMA pg_catalog TO "{0}" """.format(
            roleName
        )
        return sql

    def dropRole(self, role):
        sql = """CREATE OR REPLACE FUNCTION droprole(name text) RETURNS void AS $BODY$
                    DECLARE
                        s text;
                    BEGIN
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL TABLES IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL SEQUENCES IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        EXECUTE 'REVOKE ALL ON db_metadata FROM '|| name;
                        RETURN;

                    END
                $BODY$ LANGUAGE plpgsql;#
            """
        sql += "SELECT droprole('" + role + "')#"
        sql += "DROP ROLE IF EXISTS " + role
        return sql

    def grantRole(self, user, role):
        sql = "GRANT " + role + " TO " + user
        return sql

    def revokeRole(self, user, role):
        sql = "REVOKE " + role + " FROM " + user
        return sql

    def getRoles(self):
        sql = "SELECT rolname FROM pg_roles WHERE rolname <> 'postgres' AND rolcanlogin = 'f' AND rolname in (select split_part(unnest(nspacl)::text, '=', 1) from pg_namespace where nspname = 'pg_catalog')"
        return sql

    def getUserRelatedRoles(self, username):
        sql = (
            """select rolname, usename from
                    (select * from pg_roles as r where r.rolcanlogin = \'f\' and r.rolname<>\'postgres\') as listaRoles left join
                    (select * from pg_auth_members as m join pg_user as u on m.member = u.usesysid and u.usename=\'%s\')
                    as euTenho on euTenho.roleid=listaRoles.oid  where rolname in (select split_part(unnest(nspacl)::text, \'=\', 1) from pg_namespace where nspname = \'pg_catalog\')
                """
            % username
        )
        return sql

    def getUsers(self):
        sql = "SELECT usename FROM pg_user WHERE usename <> 'postgres'"
        return sql

    def createUser(self, user, password, isSuperuser):
        if isSuperuser:
            sql = (
                "CREATE ROLE "
                + user
                + " WITH SUPERUSER CREATEDB CREATEROLE REPLICATION LOGIN PASSWORD '"
                + password
                + "';"
            )
        else:
            sql = "CREATE ROLE " + user + " WITH LOGIN PASSWORD '" + password + "';"
        return sql

    def removeUser(self, user):
        sql = "DROP ROLE " + user
        return sql

    def alterUserPass(self, user, newPass):
        sql = "ALTER ROLE " + user + " WITH PASSWORD '" + newPass + "'"
        return sql

    def validateWithDomain(self, schemaList):
        schemas = "'" + "','".join(schemaList) + "'"
        sql = (
            """SELECT
                tc.table_schema,tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || ccu.column_name || ' FROM dominios.' || ccu.table_name || ' ORDER BY ' || ccu.column_name || ' ASC'
                    FROM
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in (%s)"""
            % schemas
        )
        return sql

    def getTableDomains(self, tableList):
        schemas = "'" + "','".join(tableList) + "'"
        sql = (
            """SELECT
                tc.table_schema,tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || ccu.column_name || ' FROM dominios.' || ccu.table_name || ' ORDER BY ' || ccu.column_name || ' ASC'
                    FROM
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in (%s)"""
            % schemas
        )
        return sql

    def getNotNullFields(self, schemaList):
        schemas = "'" + "','".join(schemaList) + "'"
        sql = (
            "select table_schema, table_name, column_name from information_schema.columns where is_nullable = 'NO' and column_name not in ('id','geom') and table_schema in (%s)"
            % schemas
        )
        return sql

    def getFeaturesWithSQL(self, layer, attrList):
        ls = ",".join(attrList)
        sql = "SELECT %s FROM ONLY %s" % (ls, layer)
        return sql

    def getStructure(self, edgvVersion):
        sql = ""
        if edgvVersion == "2.1.3":
            sql = "SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_schema in ('cb','complexos','public')"
        elif edgvVersion == "FTer_2a_Ed":
            sql = "SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_schema in ('ge','pe','complexos','public')"
        elif edgvVersion == "3.0":
            sql = "SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_schema in ('edgv','complexos','public')"
        return sql

    def getAggregationColumn(self):
        sql = "SELECT DISTINCT column_name FROM public.complex_schema"
        return sql

    def getAggregatorFromId(self, className, id):
        sql = "SELECT id from %s where id ='%s'" % (className, id)
        return sql

    def getAggregatorFromComplexSchema(self, aggregated, aggregationColumn):
        sql = (
            "SELECT complex from public.complex_schema where aggregated_class = '%s' and aggregationColumn = '%s'"
            % (aggregated, aggregationColumn)
        )
        return sql

    def createCustomSort(self):
        sql = """CREATE OR REPLACE FUNCTION
                      array_sort_dsg(
                        array_vals_to_sort anyarray
                      )
                      RETURNS TABLE (
                        sorted_array anyarray
                      )
                      AS $BODY$
                        BEGIN
                          RETURN QUERY SELECT
                            ARRAY_AGG(val) AS sorted_array
                          FROM
                            (
                              SELECT
                                UNNEST(array_vals_to_sort) AS val
                              ORDER BY
                                val DESC NULLS FIRST
                            ) AS sorted_vals
                          ;
                        END;
                      $BODY$
                    LANGUAGE plpgsql;
                    """
        return sql

    def getRolePrivileges(self, role, dbname):
        sql = (
            "SELECT * FROM information_schema.role_table_grants where grantee = '%s' and table_catalog = '%s' ORDER BY table_name"
            % (role, dbname)
        )
        return sql

    def isSuperUser(self, user):
        sql = "SELECT rolsuper FROM pg_roles WHERE rolname = '%s'" % user
        return sql

    def getInvalidGeom(self, tableSchema, tableName, geometryColumn, keyColumn):
        return """select  distinct f."{3}" as "{3}",(reason(ST_IsValidDetail(f."{2}",0))), (location(ST_IsValidDetail(f."{2}",0))) as "{2}" from (select "{3}", "{2}" from only "{0}"."{1}"  where ST_IsValid("{2}") = 'f') as f""".format(
            tableSchema, tableName, geometryColumn, keyColumn
        )

    def getNonSimpleGeom(self, tableSchema, tableName):
        return """select  f.id as id,(reason(ST_IsValidDetail(f.geom,0))), (location(ST_IsValidDetail(f.geom,0))) as geom from (select id, geom from only "{0}"."{1}"  where ST_IsSimple(geom) = 'f') as f""".format(
            tableSchema, tableName
        )

    def checkValidationStructure(self):
        return "select count(*) from information_schema.columns where table_name = 'aux_flags_validacao'"

    def createValidationStructure(self, srid):
        sql = """CREATE SCHEMA IF NOT EXISTS validation#
        CREATE TABLE validation.aux_flags_validacao (
            id serial NOT NULL,
            process_name varchar(200) NOT NULL,
            layer varchar(200) NOT NULL,
            feat_id bigint NOT NULL,
            reason varchar(200) NOT NULL,
            user_fixed boolean NOT NULL DEFAULT FALSE,
            dimension smallint NOT NULL,
            geometry_column varchar(200) NOT NULL,
            CONSTRAINT aux_flags_validacao_pk PRIMARY KEY (id)
             WITH (FILLFACTOR = 100)
        )#

        CREATE TABLE validation.aux_flags_validacao_p (
            geom geometry(MULTIPOINT, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_p_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#

        CREATE TABLE validation.aux_flags_validacao_l (
            geom geometry(MULTILINESTRING, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_l_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#

        CREATE TABLE validation.aux_flags_validacao_a (
            geom geometry(MULTIPOLYGON, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_a_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#

        CREATE TABLE validation.status
        (
          id smallint NOT NULL,
          status character varying(200) NOT NULL,
          CONSTRAINT status_pk PRIMARY KEY (id)
        )#
        CREATE TABLE validation.process_history (
            id serial NOT NULL,
            process_name varchar(200) NOT NULL,
            log text NOT NULL,
            status int NOT NULL,
            finished timestamp NOT NULL default now(),
            CONSTRAINT process_history_pk PRIMARY KEY (id),
            CONSTRAINT process_history_status_fk FOREIGN KEY (status) REFERENCES validation.status (id) MATCH FULL ON UPDATE NO ACTION ON DELETE NO ACTION

        )#
        CREATE TABLE validation.settings(
            id serial NOT NULL,
            scale character varying(10),
            tolerance float,
            earthcoverage text,
            CONSTRAINT settings_pk PRIMARY KEY (id)
        )#
        INSERT INTO validation.settings(earthcoverage) VALUES (NULL)#
        INSERT INTO validation.status(id,status) VALUES (0,'Not yet ran'), (1,'Finished'), (2,'Failed'), (3,'Running'), (4,'Finished with flags')
        """ % (
            srid,
            srid,
            srid,
        )
        return sql

    def validationStatus(self, processName):
        sql = (
            "SELECT status FROM validation.process_history where process_name = '%s' ORDER BY finished DESC LIMIT 1; "
            % processName
        )
        return sql

    def validationStatusText(self, processName):
        sql = (
            "SELECT sta.status FROM validation.process_history as hist left join validation.status as sta on sta.id = hist.status where hist.process_name = '%s' ORDER BY hist.finished DESC LIMIT 1 "
            % processName
        )
        return sql

    def setValidationStatusQuery(self, processName, log, status):
        sql = (
            "INSERT INTO validation.process_history (process_name, log, status) values ('%s','%s',%s)"
            % (processName, log, status)
        )
        return sql

    def insertFlagIntoDb(
        self,
        layer,
        feat_id,
        reason,
        geom,
        srid,
        processName,
        dimension,
        geometryColumn,
        flagSRID,
    ):
        if dimension == 0:
            tableName = "aux_flags_validacao_p"
        elif dimension == 1:
            tableName = "aux_flags_validacao_l"
        elif dimension == 2:
            tableName = "aux_flags_validacao_a"
        sql = """INSERT INTO validation.{0} (process_name, layer, feat_id, reason, geom, dimension, geometry_column) values
        ('{1}','{2}',{3},'{4}',ST_Transform(ST_SetSRID(ST_Multi('{5}'),{6}),{7}), {8}, '{9}');""".format(
            tableName,
            processName,
            layer,
            str(feat_id),
            reason,
            geom,
            srid,
            flagSRID,
            dimension,
            geometryColumn,
        )
        return sql

    def getRunningProc(self):
        sql = "SELECT process_name, status FROM validation.process_history ORDER BY finished DESC LIMIT 1;"
        return sql

    def deleteFlags(self, processName=None, className=None, flagId=None):
        if not processName and not className and not flagId:
            whereClause = ""
        else:
            clauseList = []
            if processName:
                processClause = """process_name = '{0}'""".format(processName)
                clauseList.append(processClause)
            if className:
                classClause = """layer = '{0}'""".format(className)
                clauseList.append(classClause)
            if flagId:
                try:
                    for row in flagId:
                        flagClauseRow = """id = {0} """.format(row)
                        clauseList.append(flagClauseRow)
                except TypeError:
                    flagClause = """id = {0} """.format(flagId)
                    clauseList.append(flagClause)
            whereClause = """where {0}""".format(" AND ".join(clauseList))
        sql = """
        DELETE FROM validation.aux_flags_validacao_p
        WHERE id in
        (SELECT id FROM validation.aux_flags_validacao_p {0})#

        DELETE FROM validation.aux_flags_validacao_l
        WHERE id in
        (SELECT id FROM validation.aux_flags_validacao_l {0})#

        DELETE FROM validation.aux_flags_validacao_a
        WHERE id in
        (SELECT id FROM validation.aux_flags_validacao_a {0})
        """.format(
            whereClause
        )
        return sql

    def testSpatialRule(
        self,
        class_a,
        necessity,
        predicate_function,
        class_b,
        min_card,
        max_card,
        aKeyColumn,
        bKeyColumn,
        aGeomColumn,
        bGeomColumn,
    ):
        # TODO: Add SRIDS
        class_a = '"' + '"."'.join(class_a.replace('"', "").split(".")) + '"'
        class_b = '"' + '"."'.join(class_b.replace('"', "").split(".")) + '"'

        # checking if the rule checks the layer with itself
        if class_a != class_b:
            sameClassRestriction = ""
        else:
            sameClassRestriction = " WHERE a.{0} <> b.{1} ".format(
                aKeyColumn, bKeyColumn
            )

        if predicate_function == "ST_Disjoint":
            if necessity == "'f'":
                sql = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.{4} id, SUM(CASE WHEN {0}(a.{6},b.{7}) = 'f' THEN 1 ELSE 0 END) count, a.{6} geom
                    FROM {1} as a,{2} as b {3} GROUP BY a.{4}, a.{6}) as foo
                WHERE foo.count > 0
                """.format(
                    predicate_function,
                    class_a,
                    class_b,
                    sameClassRestriction,
                    aKeyColumn,
                    bKeyColumn,
                    aGeomColumn,
                    bGeomColumn,
                )
            elif necessity == "'t'":
                sql = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.{4} id, SUM(CASE WHEN {0}(a.{6},b.{7}) = 'f' THEN 1 ELSE 0 END) count, a.{6} geom
                    FROM {1} as a,{2} as b {3} GROUP BY a.{4}, a.{6}) as foo
                WHERE foo.count = 0
                """.format(
                    predicate_function,
                    class_a,
                    class_b,
                    sameClassRestriction,
                    aKeyColumn,
                    bKeyColumn,
                    aGeomColumn,
                    bGeomColumn,
                )
        else:
            if necessity == "'f'":  # must (be)
                if max_card == "*":
                    sql = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{4} id, SUM(CASE WHEN {0}(a.{6},b.{7}) THEN 1 ELSE 0 END) count, a.{6} geom
                        FROM {1} as a,{2} as b {3} GROUP BY a.{4}, a.{6}) as foo
                    WHERE foo.count < {8}
                    """.format(
                        predicate_function,
                        class_a,
                        class_b,
                        sameClassRestriction,
                        aKeyColumn,
                        bKeyColumn,
                        aGeomColumn,
                        bGeomColumn,
                        min_card,
                    )
                elif min_card is None and max_card is None:
                    sql = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{4} id, SUM(CASE WHEN {0}(a.{6},b.{7}) THEN 1 ELSE 0 END) count, a.{6} geom
                        FROM {1} as a,{2} as b {3} GROUP BY a.{4}, a.{6}) as foo
                    WHERE foo.count != 0;
                    """.format(
                        predicate_function,
                        class_a,
                        class_b,
                        sameClassRestriction,
                        aKeyColumn,
                        bKeyColumn,
                        aGeomColumn,
                        bGeomColumn,
                        min_card,
                    )
                else:
                    sql = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{4} id, SUM(CASE WHEN {0}(a.{6},b.{7}) THEN 1 ELSE 0 END) count, a.{6} geom
                        FROM {1} as a,{2} as b {3} GROUP BY a.{4}, a.{6}) as foo
                    WHERE foo.count < {8} OR foo.count > {9}
                    """.format(
                        predicate_function,
                        class_a,
                        class_b,
                        sameClassRestriction,
                        aKeyColumn,
                        bKeyColumn,
                        aGeomColumn,
                        bGeomColumn,
                        min_card,
                        max_card,
                    )
            elif necessity == "'t'":  # must not (be)
                if class_a != class_b:
                    sameClassRestriction = ""
                else:
                    sameClassRestriction = " AND a.{0} <> b.{1} ".format(
                        aKeyColumn, bKeyColumn
                    )

                sql = """SELECT DISTINCT a.{5} id, (ST_Dump(ST_Intersection(a.{7}, b.{8}))).geom as geom
                FROM {0} as a, {1} as b
                    WHERE {2}(a.{7},b.{8}) = {3} {4}
                """.format(
                    class_a,
                    class_b,
                    predicate_function,
                    necessity,
                    sameClassRestriction,
                    aKeyColumn,
                    bKeyColumn,
                    aGeomColumn,
                    bGeomColumn,
                )
        return sql

    def getDimension(self, geom):
        sql = "select ST_Dimension('%s')" % geom
        return sql

    def getMulti(self, cl):
        # TODO: get pk
        cl = '"' + '"."'.join(cl.replace('"', "").split(".")) + '"'
        sql = """select id from only {0} where ST_NumGeometries(geom) > 1""".format(cl)
        return sql

    def getDuplicatedGeom(self, schema, cl, geometryColumn, keyColumn):
        sql = """select * from (
        SELECT "{3}",
        ROW_NUMBER() OVER(PARTITION BY "{2}" ORDER BY "{3}" asc) AS Row,
        geom FROM ONLY "{0}"."{1}"
        ) dups
        where
        dups.Row > 1""".format(
            schema, cl, geometryColumn, keyColumn
        )
        return sql

    def getSmallAreas(self, schema, cl, areaTolerance, geometryColumn, keyColumn):
        sql = """select  foo2."{4}", foo2."{3}" from (
        select "{4}", "{3}", ST_Area("{3}") as area from "{0}"."{1}"
        ) as foo2 where foo2.area < {2} order by foo2."{4}" """.format(
            schema, cl, areaTolerance, geometryColumn, keyColumn
        )
        return sql

    def getSmallLines(self, schema, cl, areaTolerance, geometryColumn, keyColumn):
        sql = """select  foo2."{4}", foo2."{3}" from (
        select "{4}", "{3}", ST_Length("{3}") as len from "{0}"."{1}"
        ) as foo2 where len < {2} order by foo2."{4}" """.format(
            schema, cl, areaTolerance, geometryColumn, keyColumn
        )
        return sql

    def prepareVertexNearEdgesStruct(
        self, tableSchema, tableName, geometryColumn, keyColumn, geomType
    ):
        if "POLYGON" in geomType:
            sql = """drop table if exists seg#
            create temp table seg as (
            SELECT segments."{3}" as "{3}", ST_MakeLine(sp,ep) as "{2}"
            FROM
            (SELECT
                ST_PointN("{2}", generate_series(1, ST_NPoints("{2}")-1)) as sp,
                ST_PointN("{2}", generate_series(2, ST_NPoints("{2}")  )) as ep,
                linestrings."{3}" as "{3}"
                FROM
                (SELECT "{3}" as "{3}", (ST_Dump(ST_Boundary("{2}"))).geom
                FROM only "{0}"."{1}"
                ) AS linestrings
                ) AS segments)#
            drop table if exists pontos#
            create temp table pontos as select "{3}" as "{3}", (ST_DumpPoints("{2}")).geom as "{2}" from only "{0}"."{1}"#
            create index pontos_gist on pontos using gist ("{2}")#
            create index seg_gist on seg using gist ("{2}")""".format(
                tableSchema, tableName, geometryColumn, keyColumn
            )
        else:
            sql = """drop table if exists seg#
            create temp table seg as (
            SELECT segments."{3}" as "{3}", ST_MakeLine(sp,ep) as "{2}"
            FROM
            (SELECT
                ST_PointN("{2}", generate_series(1, ST_NPoints("{2}")-1)) as sp,
                ST_PointN("{2}", generate_series(2, ST_NPoints("{2}")  )) as ep,
                linestrings."{3}" as "{3}"
                FROM
                (SELECT "{3}" as "{3}", (ST_Dump("{2}")).geom
                FROM only "{0}"."{1}"
                ) AS linestrings
                ) AS segments)#
            drop table if exists pontos#
            create temp table pontos as select "{3}" as "{3}", (ST_DumpPoints("{2}")).geom as "{2}" from only "{0}"."{1}"#
            create index pontos_gist on pontos using gist ("{2}")#
            create index seg_gist on seg using gist ("{2}")""".format(
                tableSchema, tableName, geometryColumn, keyColumn
            )
        return sql

    def getVertexNearEdgesStruct(self, epsg, tol, geometryColumn, keyColumn):
        sql = """select pontos."{3}", ST_SetSRID(pontos."{2}",{0}) as "{2}" from pontos, seg where ST_DWithin(seg."{2}", pontos."{2}", {1}) and ST_Distance(seg."{2}", pontos."{2}") > 0""".format(
            epsg, tol, geometryColumn, keyColumn
        )
        return sql

    def deleteFeatures(self, schema, table, idList, keyColumn):
        sql = """DELETE FROM "{0}"."{1}"
        WHERE "{3}" in ({2})""".format(
            schema, table, ",".join(idList), keyColumn
        )
        return sql

    def deleteFeaturesNotIn(self, schema, table, idList):
        sql = """DELETE FROM "{0}"."{1}"
        WHERE id not in ({2})""".format(
            schema, table, ",".join(map(str, idList))
        )
        return sql

    def getNotSimple(self, tableSchema, tableName, geometryColumn, keyColumn):
        sql = """select foo."{3}" as "{3}", ST_MULTI(st_startpoint(foo."{2}")) as "{2}" from (
        select "{3}" as "{3}", (ST_Dump(ST_Node(ST_SetSRID(ST_MakeValid("{2}"),ST_SRID("{2}"))))).geom as "{2}" from "{0}"."{1}"
        where ST_IsSimple("{2}") = 'f') as foo where st_equals(st_startpoint(foo."{2}"),st_endpoint(foo."{2}"))""".format(
            tableSchema, tableName, geometryColumn, keyColumn
        )
        return sql

    def getOutofBoundsAngles(
        self, tableSchema, tableName, angle, geometryColumn, geomType, keyColumn
    ):
        if "LINESTRING" in geomType:
            sql = """
            WITH result AS (SELECT points."{4}", points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN("{3}", generate_series(1, ST_NPoints("{3}")-2)) as pt1,
                              ST_PointN("{3}", generate_series(2, ST_NPoints("{3}")-1)) as anchor,
                              ST_PointN("{3}", generate_series(3, ST_NPoints("{3}"))) as pt2,
                              linestrings."{4}" as "{4}"
                            FROM
                              (SELECT "{4}" as "{4}", (ST_Dump("{3}")).geom as "{3}"
                               FROM only "{0}"."{1}"
                               ) AS linestrings WHERE ST_NPoints(linestrings."{3}") > 2 ) as points)
            select distinct "{4}", anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))""".format(
                tableSchema, tableName, angle, geometryColumn, keyColumn
            )
        elif "POLYGON" in geomType:
            sql = """
            WITH result AS (SELECT points."{4}", points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN("{3}", generate_series(1, ST_NPoints("{3}")-1)) as pt1,
                              ST_PointN("{3}", generate_series(1, ST_NPoints("{3}")-1) %  (ST_NPoints("{3}")-1)+1) as anchor,
                              ST_PointN("{3}", generate_series(2, ST_NPoints("{3}")) %  (ST_NPoints("{3}")-1)+1) as pt2,
                              linestrings."{4}" as "{4}"
                            FROM
                              (SELECT "{4}" as "{4}", (ST_Dump(ST_Boundary(ST_ForceRHR((ST_Dump("{3}")).geom)))).geom as "{3}"
                               FROM only "{0}"."{1}"
                               ) AS linestrings WHERE ST_NPoints(linestrings."{3}") > 2 ) as points)
            select distinct "{4}", anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))""".format(
                tableSchema, tableName, angle, geometryColumn, keyColumn
            )
        return sql

    def getFlagsByProcess(self, processName):
        sql = (
            """select layer, feat_id, geometry_column from validation.aux_flags_validacao where process_name = '%s'"""
            % processName
        )
        return sql

    def forceValidity(
        self, tableSchema, tableName, idList, srid, keyColumn, geometryColumn
    ):
        sql = """update "{0}"."{1}" set "{5}" = ST_Multi(result."{5}") from (
        select distinct parts."{4}", ST_Union(parts."{5}") as "{5}" from "{0}"."{1}" as source,
                                        (select "{4}" as "{4}", ST_Multi(((ST_Dump(ST_SetSRID(ST_MakeValid("{5}"), {3}))).geom)) as "{5}" from
                                        "{0}"."{1}"  where "{4}" in ({2})) as parts where ST_GeometryType(parts."{5}") = ST_GeometryType(source."{5}") group by parts."{4}"
        ) as result where  result."{4}" = "{0}"."{1}"."{4}" """.format(
            tableSchema, tableName, ",".join(idList), srid, keyColumn, geometryColumn
        )
        return sql

    def getTableExtent(self, tableSchema, tableName):
        # TODO: put geometry column
        sql = """
        SELECT ST_XMin(ST_Extent(geom)), ST_XMax(ST_Extent(geom)), ST_YMin(ST_Extent(geom)), ST_YMax(ST_Extent(geom)) AS extent FROM "{0}"."{1}"
        """.format(
            tableSchema, tableName
        )
        return sql

    def getOrphanGeomTablesWithElements(self, loading=False):
        # TODO: Avaliate if deprecated
        if not loading:
            sql = """
            select pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid)
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ('ge','pe', 'cb') and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union
            select distinct p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and
                gc.f_table_schema in ('cb', 'pe', 'ge')

            order by tb
            """
        else:
            sql = """
            select pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid)
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ('ge','pe', 'cb', 'public') and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union
            select distinct p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and
                gc.f_table_schema in ('cb', 'pe', 'ge', 'public')

            order by tb
            """
        return sql

    def updateOriginalTable(self, tableSchema, tableName, result, epsg):
        # TODO: Put original id
        sqls = []
        for key in list(result.keys()):
            geoms = []
            for wkb in result[key]:
                geoms.append("ST_SetSRID(ST_Multi('{0}'), {1})".format(wkb, epsg))
            array = ",".join(geoms)
            union = "ST_Union(ARRAY[{}])".format(array)

            sql = """
            UPDATE "{0}"."{1}" SET geom = ST_Multi({2}) WHERE id = {3}
            """.format(
                tableSchema, tableName, union, key
            )
            sqls.append(sql)
        return sqls

    def getOrphanTableElementCount(self, orphan):
        orphan = '"' + '"."'.join(orphan.replace('"', "").split(".")) + '"'
        sql = "select id from %s limit 1" % orphan
        return sql

    def checkCentroidAuxStruct(self):
        sql = "select distinct count(column_name) from information_schema.columns where column_name = 'centroid' group by column_name"
        return sql

    def dropCentroid(self, table):
        table = '"' + '"."'.join(table.replace('"', "").split(".")) + '"'
        sql = "alter table %s drop column if exists centroid" % table
        return sql

    def createCentroidColumn(self, table_schema, table_name, srid):
        sql = """alter table "{1}"."{2}" add column centroid geometry('POINT',{0})#
        alter table "{1}"."{2}" alter column geom drop not null#
        CREATE INDEX {3} ON "{1}"."{2}" USING gist(centroid)""".format(
            srid, table_schema, table_name, table_name[:-2] + "_c_gist"
        )
        return sql

    def createCentroidGist(self, table_schema, table_name):
        gistName = table_name[:-2] + "_c_gist"
        sql = """CREATE INDEX {0} ON "{1}"."{2}" USING gist(centroid)""".format(
            gistName, table_schema, table_name
        )
        return sql

    def getEarthCoverageClasses(self):
        sql = "select distinct table_schema || '.' || table_name from information_schema.columns where column_name = 'centroid'"
        return sql

    def getEarthCoverageDict(self):
        sql = "select earthcoverage from validation.settings limit 1"
        return sql

    def setEarthCoverageDict(self, earthDict):
        if earthDict:
            sql = "update validation.settings set earthcoverage = '%s'" % earthDict
        else:
            sql = "update validation.settings set earthcoverage = NULL"
        return sql

    def makeRelationDict(self, table, codes):
        sql = """select code, code_name from dominios.%s where code in %s""" % (
            table,
            codes,
        )
        return sql

    def getEarthCoverageCentroids(self):
        sql = "select distinct table_name from information_schema.columns where column_name = 'centroid'"
        return sql

    def getWhoAmI(self, cl, id):
        sql = "select p.relname from {0} as c, pg_class as p where c.tableoid = p.oid and c.id = {1}".format(
            cl, id
        )
        return sql

    def snapLinesToFrame(
        self, cl, frameTable, tol, geometryColumn, keyColumn, frameGeometryColumn
    ):
        schema, table = cl.split(".")
        frameSchema, frameTable = frameTable.split(".")
        sql = """
        update "{0}"."{1}" as classe set "{5}" = ST_Multi(agrupado."{5}")
        from
            (
                select simplelines."{6}" as "{6}", ST_Union(simplelines.newline) as "{5}"
                from
                (
                    select short."{6}", St_SetPoint((ST_Dump(short."{5}")).geom, 0,
                    ST_EndPoint(from_start)) as newline
                    from
                    (   select a."{6}" as "{6}", a."{5}" as "{5}",
                        ST_ShortestLine(st_startpoint((ST_Dump(a."{5}")).geom),
                        ST_Boundary(m."{7}")) as from_start
                        from "{0}"."{1}" a, "{3}"."{4}" m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines."{6}"
            ) as agrupado
        where classe."{6}" = agrupado."{6}"#
        update "{0}"."{1}" as classe set "{5}" = ST_Multi(agrupado."{5}")
        from
            (
                select simplelines."{6}" as "{6}", ST_Union(simplelines.newline) as "{5}"
                from
                (
                    select short."{6}", St_SetPoint((ST_Dump(short."{5}")).geom,
                    short.index - 1, ST_EndPoint(from_start)) as newline
                    from
                    (   select a."{6}" as "{6}", a."{5}" as "{5}",
                        ST_ShortestLine(st_endpoint((ST_Dump(a."{5}")).geom),
                        ST_Boundary(m."{7}")) as from_start,
                        ST_NPoints((ST_Dump(a."{5}")).geom) as index
                        from "{0}"."{1}" a, "{3}"."{4}" m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines."{6}"
            ) as agrupado
        where classe."{6}" = agrupado."{6}"
        """.format(
            schema,
            table,
            str(tol),
            frameSchema,
            frameTable,
            geometryColumn,
            keyColumn,
            frameGeometryColumn,
        )
        return sql

    def densifyFrame(
        self, cl, frameTable, snapTolerance, geometryColumn, frameGeometryColumn
    ):
        cl = '"' + '"."'.join(cl.replace('"', "").split(".")) + '"'
        frameTable = '"' + '"."'.join(frameTable.replace('"', "").split(".")) + '"'
        sql = """
        update {2} m set {4} = st_multi(st_snap(m.{4},
        foo.vertices, {1}))
        from
        (
            select st_union(st_boundary(a.{3})) as vertices from
        {0} a
        ) as foo
        """.format(
            cl, snapTolerance, frameTable, geometryColumn, frameGeometryColumn
        )
        return sql

    def snapToGrid(self, cl, precision, srid, geometryColumn):
        schema, table = cl.split(".")
        sql = 'update "{0}"."{1}" set "{4}" = ST_SetSRID(ST_SnapToGrid("{4}",{2}),{3})'.format(
            schema, table, precision, srid, geometryColumn
        )
        return sql

    def makeRecursiveSnapFunction(self, geometryColumn, keyColumn):
        sql = """
        CREATE OR REPLACE FUNCTION dsgsnap(tabela text, snap float) RETURNS void AS
        $BODY$
            DECLARE
            id int;
            BEGIN
                FOR id in execute('select "{1}" from '||tabela)
                LOOP
                    EXECUTE
                'update '||tabela||' as classe set "{0}" = st_multi(res."{0}")
                from
                    (
                        select st_snap(a."{0}", st_collect(b."{0}"), '||snap||') as "{0}", a."{1}" as "{1}"
                        from '||tabela||' a, '||tabela||' b
                        where a."{1}" != b."{1}" and st_isempty(a."{0}") = FALSE and a."{1}" = '||id||'
                        group by a."{1}", a."{0}"
                    ) as res
                where res."{1}" = classe."{1}" ';
                END LOOP;
                RETURN;
            END
        $BODY$
        LANGUAGE plpgsql;
        """.format(
            geometryColumn, keyColumn
        )
        return sql

    def executeRecursiveSnap(self, cl, tol):
        sql = "SELECT dsgsnap('{0}', {1})".format(cl, str(tol))
        return sql

    def createTempTable(self, layerName):
        schema, tableName = layerName.split(".")
        sql = """
        DROP TABLE IF EXISTS "{0}"."{1}_temp"#
        CREATE TABLE "{0}"."{1}_temp" as (select * from "{0}"."{1}" where 1=2)
        """.format(
            schema, tableName
        )
        return sql

    def dropTempTable(self, tableName):
        tableName = '"' + '"."'.join(tableName.replace('"', "").split(".")) + '"'
        sql = """DROP TABLE IF EXISTS {0}""".format(tableName)
        return sql

    def populateTempTable(self, tableName, attributes, prepareValues):
        tableName = '"' + '"."'.join(tableName.split("."))
        columnTupleString = '"' + '","'.join(map(str, attributes)) + '"'
        valueTuppleString = ",".join(map(str, prepareValues))
        sql = """INSERT INTO {0}_temp"({1}) VALUES ({2})""".format(
            tableName, columnTupleString, valueTuppleString
        )
        return sql

    def createSpatialIndex(self, tableName, geomColumnName="geom"):
        tableName = '"' + '"."'.join(tableName.replace('"', "").split("."))
        sql = 'create index "{0}_temp_gist" on {1}_temp" using gist ({2})'.format(
            tableName.split(".")[-1].replace('"', ""), tableName, geomColumnName
        )
        return sql

    def getStoredStyles(self):
        sql = "select f_table_schema, f_table_name, f_geometry_column, stylename, styleqml from public.layer_styles where f_table_catalog = current_database()"
        return sql

    def getStyles(self):
        sql = "select description, f_table_schema, f_table_name, stylename from public.layer_styles where f_table_catalog = current_database()"
        return sql

    def checkStyleTable(self):
        sql = "select relname from pg_class where relname = 'layer_styles' limit 1"
        return sql

    def createStyleTable(self):
        sql = """
        CREATE TABLE public.layer_styles
        (
          id serial NOT NULL,
          f_table_catalog character varying,
          f_table_schema character varying,
          f_table_name character varying,
          f_geometry_column character varying,
          stylename text,
          styleqml text,
          stylesld text,
          useasdefault boolean,
          description text,
          owner character varying(30),
          ui xml,
          update_time timestamp without time zone DEFAULT now(),
          CONSTRAINT layer_styles_pkey PRIMARY KEY (id)
        )
        """
        return sql

    def listStylesFromDb(self, dbVersion):
        """
        Returns the stylenames of the database.
        The replace(stylename,'/' || f_table_name, '') is done due to compatibility issues
        with previous DSGTools behaviour.
        """
        sql = """
            select distinct replace(stylename,'/' || f_table_name, '')
                from public.layer_styles
                where f_table_catalog = current_database()
        """
        return sql

    def getStyle(self, styleName, table_name):
        sql = """SELECT styleqml from public.layer_styles where f_table_name = '{0}' and (stylename = '{1}' or stylename like '{1}/%')and f_table_catalog = current_database()""".format(
            table_name, styleName
        )
        return sql

    def updateStyle(self, styleName, table_name, parsedQml, tableSchema):
        sql = """UPDATE public.layer_styles SET styleqml = '{0}', update_time = now() where f_table_name = '{1}' and description = '{2}'""".format(
            parsedQml.replace("'", "''"), table_name, styleName
        )
        return sql

    def importStyle(self, styleName, table_name, parsedQml, tableSchema, dbName):
        # TODO:REDO it
        if table_name[-1] == "c":
            geomColumn = "centroid"
        else:
            geomColumn = "geom"
        sql = (
            """INSERT INTO  public.layer_styles (styleqml, f_table_name, description, f_geometry_column, stylename, f_table_schema, f_table_catalog, useasdefault) VALUES ('"""
            + parsedQml.replace("'", "''")
            + """','{0}','{1}','{2}','{3}','{4}','{5}',FALSE)""".format(
                table_name,
                styleName,
                geomColumn,
                styleName.split("/")[-1] + "/" + table_name,
                tableSchema,
                dbName,
            )
        )
        return sql

    def getTableSchemaFromDb(self, table):
        sql = """select distinct table_schema from information_schema.columns where table_name = '{0}' and table_schema not in ('validation','views')""".format(
            table
        )
        return sql

    def getAllStylesFromDb(self):
        sql = """SELECT DISTINCT f_table_catalog, description, f_table_name, update_time from public.layer_styles order by f_table_catalog, description, f_table_name asc """
        return sql

    def deleteStyle(self, styleName):
        sql = """delete from public.layer_styles where description = '{0}'""".format(
            styleName
        )
        return sql

    # Atentar que a coluna consrc foi descontinuada no pg 12+ (issue #521)
    # def getConstraints(self, schemaList):
    #     sql = """select sch.nspname, cl.relname, c.conname, c.consrc from
    #         (
    #             select * from pg_constraint where contype = 'c'
    #         ) as c join (
    #             select oid, nspname from pg_namespace where nspname in ({0})
    #         ) as sch on sch.oid = c.connamespace
    #         left join pg_class as cl on c.conrelid = cl.oid
    #         """.format(','.schemaList)
    #     return sql

    def getGeometricSchemas(self):
        sql = "select distinct f_table_schema from public.geometry_columns"
        return sql

    def getGeomTablesFromGeometryColumns(self):
        sql = "select srid, f_geometry_column, type, f_table_schema, f_table_name from public.geometry_columns"
        return sql

    def getGeomTablesDomains(self, layerFilter=None):
        inClause = (
            """'{text}'""".format(text='","'.join(layerFilter))
            if layerFilter
            else """select f_table_name from public.geometry_columns where f_table_schema <> 'views'"""
        )
        sql = """select distinct case
            when split_part(conrelid::regclass::text,'.',2) = '' then replace(split_part(conrelid::regclass::text,'.',1),'"','')
            else replace(split_part(conrelid::regclass::text,'.',2),'"','')
            end as cl, pg_get_constraintdef(oid) FROM
            pg_constraint WHERE contype = 'f' and case
            when replace(split_part(conrelid::regclass::text,'.',2),'"','') = '' then replace(split_part(conrelid::regclass::text,'.',1),'"','')
            else replace(split_part(conrelid::regclass::text,'.',2),'"','')
        end in ({in_clause})
        """.format(
            in_clause=inClause
        )
        return sql

    def getGeomTableConstraints(self, layerFilter=None):
        inClause = (
            """'{text}'""".format(text='","'.join(layerFilter))
            if layerFilter
            else """select f_table_name from public.geometry_columns where f_table_schema <> 'views'"""
        )
        sql = """select distinct case
            when split_part(conrelid::regclass::text,'.',2) = '' then split_part(conrelid::regclass::text,'.',1)
            else split_part(conrelid::regclass::text,'.',2)
            end as cl, pg_get_constraintdef(oid) FROM
             pg_constraint WHERE contype = 'c' and case
            when split_part(conrelid::regclass::text,'.',2) = '' then split_part(conrelid::regclass::text,'.',1)
            else split_part(conrelid::regclass::text,'.',2)
        end in ({in_clause})
        order by cl
        """.format(
            in_clause=inClause
        )
        return sql

    def getMultiColumns(self, schemaList):
        sql = """select row_to_json(a) from (
                select t.table_name, array_agg(t.column_name::text) as attributes from
                (select table_name, column_name from information_schema.columns
                where data_type = 'ARRAY' and table_schema in ({0})
                ) as t group by t.table_name
            ) as a
        """.format(
            "'" + "','".join(schemaList) + "'"
        )
        return sql

    def getMultiColumnsFromTableList(self, tableList):
        sql = """select row_to_json(a) from (
                select t.table_name, array_agg(t.column_name::text) as attributes from
                (select table_name, column_name from information_schema.columns
                where data_type = 'ARRAY' and table_name in ({0})
                ) as t group by t.table_name
            ) as a
        """.format(
            "'" + "','".join(tableList) + "'"
        )
        return sql

    def getGeomByPrimitive(self):
        sql = """select row_to_json(a) from (select type as geomtype, array_agg(f_table_name) as classlist from public.geometry_columns where f_table_schema not in ('views','topology') group by type) as a"""
        return sql

    def getTablesJsonList(self):
        sql = """select row_to_json(a) from (select table_schema::text, table_name::text from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') order by table_schema, table_name) as a"""
        return sql

    def getGeomColumnDict(self):
        sql = """select row_to_json(row(f_table_name, f_geometry_column)) from public.geometry_columns where f_table_schema not in ('views','topology')"""
        return sql

    def getGeomColumnTupleList(self, showViews=False, filterList=None):
        filterLayersClause = (
            " f_table_name in ({table_name_list})".format(
                table_name_list=",".join(filterList)
            )
            if filterList
            else """"""
        )
        showViewsClause = """ table_type = 'BASE TABLE'""" if not showViews else """"""
        whereStrList = list(
            filter(lambda x: x != "", [filterLayersClause, showViewsClause])
        )
        whereClause = (
            "" if whereStrList == [] else f"WHERE {' AND '.join(whereStrList)}"
        )

        sql = f"""select f_table_schema, f_table_name, f_geometry_column, type, table_type from (select distinct f_table_schema, f_table_name, f_geometry_column, type, f_table_schema || '.' || f_table_name as jc  from public.geometry_columns as gc) as inn
            left join (select table_schema || '.' || table_name as jc, table_type from information_schema.tables) as infs on inn.jc = infs.jc
            {whereClause}"""
        return sql

    def getNotNullDict(self, layerFilter=None):
        tableNameClause = (
            """'{text}'""".format(text='","'.join(layerFilter))
            if layerFilter
            else """select distinct f_table_name from public.geometry_columns """
        )
        sql = """select row_to_json(row(table_name, table_schema,  array_agg(column_name::text)))
                    from information_schema.columns
                    where table_name in ({table_name_clause})
                        and is_nullable = 'NO' and data_type = 'smallint'
                    group by table_name, table_schema
            """.format(
            table_name_clause=tableNameClause
        )
        return sql

    def getTableMetadataDict(self, layerFilter=None):
        sql = """select row_to_json(a) from (
	                select table_schema, table_name, column_name as attr_name, is_nullable::boolean as nullable, data_type as column_type, gc.f_geometry_column as geometry_column, gc.type as geometry_type
					    from information_schema.columns as c
					left join public.geometry_columns as gc
						on c.table_name = gc.f_table_name and c.table_schema = gc.f_table_schema ) as a
	            where a.table_name in ({filter})
        """.format(
            filter="""'{text}'""".format(text='","'.join(layerFilter))
            if layerFilter
            else """select f_table_name from public.geometry_columns where f_table_schema <> 'views'"""
        )
        return sql

    def getDomainDict(self, domainTable):
        sql = """select row_to_json(row(code, code_name)) from {0}""".format(
            domainTable
        )
        return sql

    def getDomainCodeDict(self, domainTable):
        sql = """select row_to_json(a) from (select * from {0}) as a""".format(
            domainTable
        )
        return sql

    def getDomainCodeDictWithColumns(self, domainTable, refPk, otherKey):
        sql = """select row_to_json(a) from (select {pk}, {fk} from {table}) as a""".format(
            table=domainTable, pk=refPk, fk=otherKey
        )
        return sql

    def getGeomStructDict(self):
        sql = """select row_to_json(a) from (
                    select table_name, array_agg(row_to_json(row(column_name::text, is_nullable))) from information_schema.columns where
                        table_name in (select f_table_name from public.geometry_columns)
                        and column_name not like 'id_%'
                        and column_name not in ('id','geom')
                        and table_schema not in ('validation','views')
                    group by table_name
                    ) as a
        """
        return sql

    def insertFrame(self, scale, mi, inom, frame, srid, geoSrid, paramDict=dict()):
        paramKeys = list(paramDict.keys())
        if "tableSchema" not in paramKeys:
            tableSchema = "public"
        else:
            tableSchema = paramDict["tableSchema"]
        if "tableName" not in paramKeys:
            tableName = "aux_moldura_a"
        else:
            tableName = paramDict["tableName"]
        if "miAttr" not in paramKeys:
            miAttr = "mi"
        else:
            miAttr = paramDict["miAttr"]
        if "inomAttr" not in paramKeys:
            inomAttr = "inom"
        else:
            inomAttr = paramDict["inomAttr"]
        if "geom" not in paramKeys:
            geometryColumn = "geom"
        else:
            geometryColumn = paramDict["geom"]
        if "geomType" not in paramKeys:
            geomType = "MULTIPOLYGON"
        else:
            geomType = paramDict["geomType"]

        if geomType == "MULTIPOLYGON":
            sql = """INSERT INTO "{5}"."{6}" ({7},{8},{9}) VALUES ('{0}','{1}',ST_Transform(ST_Multi(ST_GeomFromWKB({2},{3})), {4}))""".format(
                mi,
                inom,
                frame,
                geoSrid,
                srid,
                tableSchema,
                tableName,
                miAttr,
                inomAttr,
                geometryColumn,
            )
        else:
            sql = """INSERT INTO "{5}"."{6}" ({7},{8},{9}) VALUES ('{0}','{1}',ST_Transform((ST_SetSRID( (ST_Dump('{2}')).geom,{3})), {4}))""".format(
                mi,
                inom,
                frame,
                geoSrid,
                srid,
                tableSchema,
                tableName,
                miAttr,
                inomAttr,
                geometryColumn,
            )
        return sql

    def createFromTemplate(self, dbName, templateName):
        sql = """CREATE DATABASE "{0}" with template = "{1}";""".format(
            dbName, templateName
        )
        return sql

    def updateDbSRID(self, tableDict, srid):
        sql = """select UpdateGeometrySRID('{0}', '{1}', '{2}',{3})""".format(
            tableDict["tableSchema"], tableDict["tableName"], tableDict["geom"], srid
        )
        return sql

    def setDbAsTemplate(self, dbName, setTemplate=True):
        if setTemplate:
            sql = """UPDATE pg_database set datistemplate = 't' where datname = '{0}';""".format(
                dbName
            )
        else:
            sql = """UPDATE pg_database set datistemplate = 'f' where datname = '{0}';""".format(
                dbName
            )
        return sql

    def checkTemplate(self):
        sql = """select datname from pg_database where datistemplate = 't'"""
        return sql

    def checkIfTemplate(self, dbName):
        sql = """select datistemplate from pg_database where datname = '{0}'""".format(
            dbName
        )
        return sql

    def alterSearchPath(self, dbName, version):
        if version == "2.1.3":
            sql = "ALTER DATABASE \"{0}\" SET search_path = \"$user\", public, topology,'cb','complexos','dominios';".format(
                dbName
            )
        elif version == "2.1.3 Pro":
            sql = "ALTER DATABASE \"{0}\" SET search_path = \"$user\", public, topology,'edgv','dominios';".format(
                dbName
            )
        elif version in ("3.0", "3.0 Pro"):
            sql = "ALTER DATABASE \"{0}\" SET search_path = \"$user\", public, topology, pg_catalog, 'edgv' ,'dominios';".format(
                dbName
            )
        elif version == "FTer_2a_Ed":
            sql = "ALTER DATABASE \"{0}\" SET search_path = \"$user\", public, topology,'pe','ge','complexos','dominios';".format(
                dbName
            )
        return sql

    def getUsersFromServer(self):
        sql = """SELECT usename, usesuper FROM pg_user WHERE usename <> 'postgres' order by usename"""
        return sql

    def reasignAndDropUser(self, user):
        sql = """REASSIGN OWNED BY {0} to postgres; DROP USER {0};""".format(user)
        return sql

    def deleteFeatureFlagsFromDb(self, layer, feat_id, processName):
        sql = "DELETE FROM validation.aux_flags_validacao WHERE process_name = '{0}' AND layer = '{1}' AND feat_id = {2}".format(
            processName, layer, feat_id
        )
        return sql

    def removeEmptyGeomtriesFromDb(self, layer, geometryColumn):
        schema, table = layer.split(".")
        sql = """DELETE FROM "{0}"."{1}" WHERE st_isempty("{2}") = TRUE""".format(
            schema, table, geometryColumn
        )
        return sql

    def hasAdminDb(self):
        sql = """SELECT datname from pg_database where datname = 'dsgtools_admindb';"""
        return sql

    def getRolesDict(self):
        sql = """select row_to_json(a) from (select distinct  pgd.datname as dbname, pgr.rolname as rolename from pg_shdepend as shd join (
            select * from pg_roles where rolcanlogin = 'f'
            ) as pgr on shd.refobjid = pgr.oid join pg_database as pgd on shd.dbid = pgd.oid) as a
            """
        return sql

    def getSettingTable(self, settingType):
        if settingType == "Permission":
            tableName = "permission_profile"
        elif settingType == "Customization":
            tableName = "customization"
        elif settingType == "EarthCoverage":
            tableName = "earth_coverage"
        elif settingType == "Style":
            tableName = "style"
        elif settingType == "FieldToolBoxConfig":
            tableName = "field_toolbox_config"
        elif settingType == "ValidationConfig":
            tableName = "validation_config"
        elif settingType == "AttributeRules":
            tableName = "attribute_rules"
        elif settingType == "SpatialRules":
            tableName = "spatial_rules"
        elif settingType == "ValidationWorkflow":
            tableName = "validation_workflow"
        else:
            raise Exception("Setting type not defined!")
        return tableName

    def insertSettingIntoAdminDb(self, settingType, name, jsondict, edgvversion):
        tableName = self.getSettingTable(settingType)
        sql = """INSERT INTO "public"."{0}" (name, jsondict, edgvversion) VALUES ('{1}','{2}','{3}'); """.format(
            tableName, name, jsondict, edgvversion
        )
        return sql

    def getSettingFromAdminDb(self, settingType, name, edgvversion):
        tableName = self.getSettingTable(settingType)
        sql = """select jsondict as jsondict from "public"."{0}" where name = '{1}' and edgvversion = '{2}';""".format(
            tableName, name, edgvversion
        )
        return sql

    def deleteSettingFromAdminDb(self, settingType, name, edgvversion):
        tableName = self.getSettingTable(settingType)
        sql = """DELETE FROM "public"."{0}" where name = '{1}' and  edgvversion = '{2}';""".format(
            tableName, name, edgvversion
        )
        return sql

    def getAllSettingsFromAdminDb(self, settingType):
        tableName = self.getSettingTable(settingType)
        sql = """select row_to_json(a) from (
                    select edgvversion, array_agg(name) as settings from public.{0} group by edgvversion
                ) as a;""".format(
            tableName
        )
        return sql

    def dropRoleOnDatabase(self, roleName):
        sql = """drop owned by "{0}" cascade;
            drop role "{0}";""".format(
            roleName
        )
        return sql

    def getRolesWithGrantedUsers(self):
        sql = """select row_to_json(a) from (
                    select pgr.rolname as profile, array_agg(pgr2.rolname) as users  from pg_auth_members as pgam
                        left join pg_roles as pgr on pgam.roleid = pgr.oid
                        left join pg_roles as pgr2 on pgam.member = pgr2.oid
                    group by pgr.rolname
                ) as a;
        """
        return sql

    def getDomainTables(self):
        sql = """select distinct table_name from information_schema.columns where table_schema = 'dominios' order by table_name asc"""
        return sql

    def getGeometricSchemaList(self):
        sql = """select distinct f_table_schema from public.geometry_columns order by f_table_schema asc;"""
        return sql

    def getGeometricTableListFromSchema(self, schema):
        if isinstance(schema, list):
            sql = """select distinct f_table_schema, f_table_name from public.geometry_columns where f_table_schema in ('{0}') and f_table_name in (
                select distinct table_name from information_schema.tables where table_type <> 'VIEW'
                )
                 order by f_table_name asc;""".format(
                "','".join(schema)
            )
        else:
            sql = """select distinct f_table_schema, f_table_name from public.geometry_columns where f_table_schema = '{0}' and f_table_name in (
                select distinct table_name from information_schema.tables where table_type <> 'VIEW'
                )
                 order by f_table_name asc;""".format(
                schema
            )
        return sql

    def getParentGeomTables(self, schemaList):
        schemaList = [i for i in schemaList if i not in ["validation", "views"]]
        sql = """select pgnsp.nspname, pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid)
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ('{0}') and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union
            select distinct gc.f_table_schema,p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and
                gc.f_table_schema in ('{0}')

            order by tb""".format(
            "','".join(schemaList)
        )
        return sql

    def getInheritanceDict(self):
        sql = """select row_to_json(a) from (select pgc.relname parentname, array_agg(pgc1.relname) childname
                from pg_inherits as pginh
                    left join pg_class pgc on pginh.inhparent = pgc.oid
                    left join pg_class as pgc1 on pginh.inhrelid = pgc1.oid
                group by pgc.relname
                ) as a"""
        return sql

    def getGeomTables(
        self, schemaList, dbPrimitiveList=[], excludeViews=True, geomColumn=False
    ):
        primitiveClause = ""
        viewClause = ""
        if dbPrimitiveList != []:
            primitiveClause = """and type in ('{0}')""".format(
                "','".join(dbPrimitiveList)
            )
        if excludeViews:
            viewClause = """and f_table_name in (select table_name from information_schema.tables where table_type <> 'VIEW')"""
        selectClause = "f_table_schema, f_table_name"
        if geomColumn:
            selectClause += ",f_geometry_column"
        sql = """select distinct {0} from public.geometry_columns where f_table_schema in ('{1}') {2} {3} order by f_table_name""".format(
            selectClause, "','".join(schemaList), primitiveClause, viewClause
        )
        return sql

    def getAttributeListFromTable(self, schema, tableName):
        sql = """select distinct column_name from information_schema.columns where table_schema = '{0}' and table_name = '{1}' and column_name not in (
        select f_geometry_column from public.geometry_columns where f_table_schema = '{0}' and f_table_name = '{1}'
        )
        and column_name not like 'id%' order by column_name """.format(
            schema, tableName
        )
        return sql

    def getAttributeDictFromDb(self):
        sql = """select row_to_json(a) from (select distinct table_schema, table_name, array_agg(column_name::text) as attributelist from information_schema.columns where table_schema not in ('views','validation')
        and table_schema in (select distinct f_table_schema from public.geometry_columns)
        and table_name in (select distinct f_table_name from public.geometry_columns)

         and column_name not in (
            select f_geometry_column from public.geometry_columns where f_table_schema = table_schema and f_table_name = table_name
            )
        and column_name not like 'id%' group by table_schema, table_name order by table_schema, table_name) as a"""
        return sql

    def getAttributeInfoFromTable(self, schema, tableName):
        sql = """ select row_to_json(a) from (select distinct column_name, data_type, is_nullable, column_default from information_schema.columns
        where table_schema = '{0}' and table_name = '{1}' and column_name not in (
        select f_geometry_column from public.geometry_columns where f_table_schema = '{0}' and f_table_name = '{1}'
        )
        and column_name not like 'id%' order by column_name ) as a
        """.format(
            schema, tableName
        )
        return sql

    def getAttrTypeDictFromDb(self):
        sql = """ select row_to_json(a) from (
                    select udt_name, array_agg(row_to_json(row(table_schema::text, table_name::text, column_name::text))) from information_schema.columns where
                        table_name in (select f_table_name from public.geometry_columns)
                        and column_name not like 'id_%'
                        and column_name <> 'id'
                        and column_name not in (
            select f_geometry_column from public.geometry_columns where f_table_schema = table_schema and f_table_name = table_name
            )
                        and table_schema not in ('validation','views')
                    group by udt_name
                    ) as a
        """
        return sql

    def getAllDomainValues(self, domainTable):
        sql = """ select code from dominios.{0}""".format(domainTable)
        return sql

    # Atentar que a coluna consrc foi descontinuada no pg 12+ (issue #521)
    # def getConstraintDict(self, domainList):
    #     sql = """select row_to_json(result) from (
    #     select a.tn as tablename, array_agg(row_to_json(row(a.conname::text, a.consrc::text))) from (select sch.nspname as sch, cl.relname as tn, c.conname as conname, c.consrc as consrc from
    #             (
    #                 select * from pg_constraint where contype = 'c'
    #             ) as c join (
    #                 select oid, nspname from pg_namespace where nspname in ('{0}')
    #             ) as sch on sch.oid = c.connamespace
    #             left join pg_class as cl on c.conrelid = cl.oid) as a where a.tn in (select f_table_name from public.geometry_columns) group by a.tn order by a.tn
    #     ) as result
    #     """.format("""','""".join(domainList))
    #     return sql

    def getDefaultFromDb(self, schema, tableName, attrName):
        sql = """select column_default from information_schema.columns where table_schema = '{0}' and table_name = '{1}' and column_name = '{2}';""".format(
            schema, tableName, attrName
        )
        return sql

    def upgradePostgis(self, updateDict):
        sql = ""
        for key in updateDict:
            sql += """ALTER EXTENSION {0} UPDATE TO "{1}";""".format(
                key, updateDict[key]["defaultVersion"]
            )
        return sql

    def getPostgisVersion(self):
        sql = """SELECT name, default_version,installed_version FROM pg_available_extensions WHERE name in ('postgis', 'postgis_topology')"""
        return sql

    def getCustomizationPerspectiveDict(self, perspective):
        if perspective == DsgEnums.Property:
            sql = """select row_to_json(a) from (
                        select name, array_agg(datname) from customization as custom
                            left join applied_customization as appcust on custom.id = appcust.id_customization
                            left join pg_database as pgd on pgd.oid = appcust.dboid group by name
                    ) as a"""
        if perspective == DsgEnums.Database:
            sql = """select row_to_json(a) from (
                        select datname as name, array_agg(name) from customization as custom
                            left join applied_customization as appcust on custom.id = appcust.id_customization
                            left join pg_database as pgd on pgd.oid = appcust.dboid group by datname
                    ) as a"""
        return sql

    def getFieldToolBoxConfigPerspectiveDict(self, perspective):
        if perspective == DsgEnums.Property:
            sql = """select row_to_json(a) from (
                        select name, array_agg(datname) from field_toolbox_config as custom
                            left join applied_field_toolbox_config as appcust on custom.id = appcust.id_applied_field_toolbox_config
                            left join pg_database as pgd on pgd.oid = appcust.dboid group by name
                    ) as a"""
        if perspective == DsgEnums.Database:
            sql = """select row_to_json(a) from (
                        select datname as name, array_agg(name) from field_toolbox_config as custom
                            left join applied_field_toolbox_config as appcust on custom.id = appcust.id_applied_field_toolbox_config
                            left join pg_database as pgd on pgd.oid = appcust.dboid group by datname
                    ) as a"""
        return sql

    def createFieldToolBoxConfigTable(self):
        sql = """CREATE TABLE IF NOT EXISTS public.field_toolbox_config(
                id uuid NOT NULL DEFAULT uuid_generate_v4(),
                name text,
                jsondict text NOT NULL,
                edgvversion text,
                CONSTRAINT field_toolbox_config_pk PRIMARY KEY (id),
                CONSTRAINT field_toolbox_config_unique_name_and_version UNIQUE (name,edgvversion)

            );
        """
        return sql

    def checkIfTableExists(self, schema, tableName):
        sql = """select table_name from information_schema.tables where table_schema = '{0}' and table_name = '{1}' limit 1""".format(
            schema, tableName
        )
        return sql

    def getRecordFromAdminDb(self, settingType, propertyName, edgvVersion):
        tableName = self.getSettingTable(settingType)
        sql = """SELECT id, name, jsondict, edgvversion from public.{0} where name = '{1}' and edgvversion = '{2}' """.format(
            tableName, propertyName, edgvVersion
        )
        return sql

    def createPropertyTable(self, settingType, isAdminDb=False):
        tableName = self.getSettingTable(settingType)
        sql = """CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
        CREATE TABLE IF NOT EXISTS public.{0}(
                id uuid NOT NULL DEFAULT uuid_generate_v4(),
                name text,
                jsondict text NOT NULL,
                edgvversion text,
                CONSTRAINT {0}_pk PRIMARY KEY (id),
                CONSTRAINT {0}_unique_name_and_version UNIQUE (name,edgvversion)
                );
            """.format(
            tableName
        )
        if isAdminDb:
            sql += """CREATE TABLE public.applied_{0}(
                id uuid NOT NULL DEFAULT uuid_generate_v4(),
                id_{0} uuid NOT NULL,
                dboid oid NOT NULL,
                CONSTRAINT applied_{0}_pk PRIMARY KEY (id),
                CONSTRAINT applied_{0}_id_{0}_config_fk FOREIGN KEY (id_{0}) REFERENCES public.{0} (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
            );
            ALTER TABLE public.applied_{0} OWNER TO postgres;
            """.format(
                tableName
            )
        return sql

    def getPropertyPerspectiveDict(self, settingType, perspective, versionFilter=None):
        if versionFilter:
            versionFilter = """ where edgvversion = '{0}' """.format(versionFilter)
        else:
            versionFilter = ""
        tableName = self.getSettingTable(settingType)
        if perspective == DsgEnums.Property:
            sql = """select row_to_json(a) from (
                        select name, array_agg(datname) from public.{0} as custom
                            left join applied_{0} as appcust on custom.id = appcust.id_{0}
                            left join pg_database as pgd on pgd.oid = appcust.dboid
                            {1}
                            group by name
                    ) as a""".format(
                tableName, versionFilter
            )
        if perspective == DsgEnums.Database:
            sql = """select row_to_json(a) from (
                        select datname as name, array_agg(name) from public.{0} as custom
                            right join applied_{0} as appcust on custom.id = appcust.id_{0}
                            left join pg_database as pgd on pgd.oid = appcust.dboid
                            {1}
                            group by datname
                    ) as a""".format(
                tableName, versionFilter
            )
        return sql

    def insertRecordInsidePropertyTable(self, settingType, settingDict):
        tableName = self.getSettingTable(settingType)
        sql = """INSERT INTO public.{0} (name, jsondict, edgvversion) VALUES ('{1}','{2}','{3}')""".format(
            tableName,
            settingDict["name"],
            settingDict["jsondict"],
            settingDict["edgvversion"],
        )
        return sql

    def insertInstalledRecordIntoAdminDb(self, settingType, recDict, dbOid):
        settingTable = self.getSettingTable(settingType)
        tableName = "applied_" + settingTable
        idName = "id_" + settingTable
        sql = """INSERT INTO public.{0} ({1}, dboid) VALUES ('{2}',{3})""".format(
            tableName, idName, recDict["id"], dbOid
        )
        return sql

    def getDbOID(self, dbName):
        sql = """SELECT oid from pg_database where datname = '{0}' """.format(dbName)
        return sql

    def getAllPropertiesFromDb(self, settingType):
        tableName = self.getSettingTable(settingType)
        sql = """select edgvversion, name, jsondict from public.{0}""".format(tableName)
        return sql

    def removeRecordFromPropertyTable(self, settingType, configName, edgvVersion):
        tableName = self.getSettingTable(settingType)
        if not edgvVersion:
            sql = """DELETE FROM public.{0} where name = '{1}';""".format(
                tableName, configName
            )
        else:
            sql = """DELETE FROM public.{0} where name = '{1}' and edgvversion = '{2}';""".format(
                tableName, configName, edgvVersion
            )
        return sql

    def updateRecordFromPropertyTable(
        self, settingType, configName, edgvVersion, jsonDict
    ):
        tableName = self.getSettingTable(settingType)
        sql = """UPDATE public.{0} SET jsondict = '{1}' where name = '{2}' and edgvversion = '{3}';""".format(
            tableName, jsonDict, configName, edgvVersion
        )
        return sql

    def uninstallPropertyOnAdminDb(
        self, settingType, configName, edgvVersion, dbName=None
    ):
        tableName = self.getSettingTable(settingType)
        dbNameFilterClause = ""
        if dbName:
            dbNameFilterClause = """dboid in (select oid from pg_database where datname ='{0}') and """.format(
                dbName
            )
        sql = """DELETE FROM public.applied_{0} where {1} id_{0} in (select id from public.{0} where name = '{2}' and edgvversion = '{3}');""".format(
            tableName, dbNameFilterClause, configName, edgvVersion
        )
        return sql

    def getSettingVersion(self, settingType, settingName):
        tableName = self.getSettingTable(settingType)
        sql = """select edgvversion from public.{0} where name = '{1}' """.format(
            tableName, settingName
        )
        return sql

    def getPrimaryKeyColumn(self, tableName):
        if "." in tableName:
            tableSchema, tableName = (
                tableName.replace("'", "").replace('"', "").split(".")
            )
            tableName = '''"{0}"."{1}"'''.format(tableSchema, tableName)
        sql = """
        SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{}'::regclass
        AND    i.indisprimary;
        """.format(
            tableName
        )
        return sql

    def getGeometryTablesCount(self):
        sql = """select count(*) from public.geometry_columns"""
        return sql

    def dropAllConections(self, dbName):
        sql = """SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{0}'
                AND pid <> pg_backend_pid();""".format(
            dbName
        )
        return sql

    def getAttributesFromTable(self, tableSchema, tableName, typeFilter=None):
        whereClause = (
            """"""
            if not typeFilter
            else """ and data_type in ('{0}') """.format("','".join(typeFilter))
        )
        sql = """select column_name, data_type from information_schema.columns where
            table_schema = '{0}' and table_name = '{1}' {2} order by column_name """.format(
            tableSchema, tableName, whereClause
        )
        return sql

    def getViewDefinition(self, viewName):
        sql = """select pg_get_viewdef('{0}')""".format(viewName)
        return sql

    def dropView(self, viewName):
        if '"' in viewName:
            sql = """DROP VIEW {0} """.format(viewName)
        elif "." in viewName:
            schema, name = viewName.split(".")
            sql = """DROP VIEW "{0}"."{1}" """.format(schema, name)
        else:
            sql = """DROP VIEW "{0}" """.format(viewName)
        return sql

    def createViewStatement(self, viewName, viewDef):
        sql = """ CREATE OR REPLACE VIEW {0} AS {1}""".format(viewName, viewDef)
        return sql

    def checkPostGISAddonsInstallation(self):
        sql = """SELECT COUNT(*) FROM pg_proc WHERE proname = 'st_geotablesummary' """
        return sql

    def createCoverageTempTable(self, srid):
        sql = """
        DROP TABLE IF EXISTS validation.coverage_temp;
        CREATE TABLE validation.coverage_temp (
            id serial NOT NULL,
            featid bigint NOT NULL,
            classname varchar(200) NOT NULL,
            geom geometry(MULTIPOLYGON, {}) NOT NULL,
            CONSTRAINT coverage_pk PRIMARY KEY (id)
        )
        """.format(
            srid
        )
        return sql

    def checkCoverageForGapsWithFrame(self, frameTable, geomColumn):
        frameSchema, frameTable = frameTable.split(".")
        sql = """
        select (ST_Dump(ST_SymDifference(a.geom, b.geom))).geom from
        (select ST_Union({0}) as geom from "{1}"."{2}") as a,
        (select ST_Union(geom) as geom from validation.coverage_temp) as b
        """.format(
            geomColumn, frameSchema, frameTable
        )
        return sql

    def checkCoverageForOverlaps(
        self, table="validation.coverage_temp", geomColumn="geom", keyColumn="id"
    ):
        tableSchema, tableName = table.split(".")
        sql = """
        select (ST_Dump(foo.geom)).geom as geom from (
        select (ST_GeoTableSummary('{0}', '{1}', '{2}', '{3}', 10, 'S3')).geom
        ) as foo
        where ST_IsEmpty(foo.geom) = 'f'
        """.format(
            tableSchema, tableName, geomColumn, keyColumn
        )
        return sql

    def getProcessOrClassFlags(self, filterType=None):
        """
        Returns all process or classes that raised flags
        """
        # to allow changing cases as desired
        # filterType = filterType.lower()
        sql = ""
        # problemas com o Enum.
        if "process" in filterType.lower():
            filterType = 0
        elif filterType:
            filterType = 1
        if filterType == DsgEnums.ProcessName:
            sql = """
        SELECT DISTINCT process_name
            FROM validation.aux_flags_validacao;
            """
        elif filterType == DsgEnums.ClassName:
            sql = """
        SELECT DISTINCT layer
            FROM validation.aux_flags_validacao;
            """
        return sql

    def getFilteredFlagsQuery(self, filterType=None, filteredElement=None):
        """
        Returns process or classes that raised flags filtered by
        chosen element in comboBox
        """
        sql = ""
        # problemas com o Enum.
        if "process" in filterType.lower():
            filterTypeEnum = 0
        elif filterType:
            filterTypeEnum = 1
        sql = """
        SELECT * FROM validation.aux_flags_validacao;
            """
        whereClause = ""
        if filterTypeEnum == DsgEnums.ProcessName:
            whereClause = " WHERE process_name = '{0}';".format(filteredElement)
        elif filterType == DsgEnums.ClassName:
            whereClause = " WHERE layer = '{0}';".format(filteredElement)
        if filteredElement and filteredElement != "":
            sql = sql + whereClause
        return sql

    def createFilteredFlagsViewTableQuery(self, filterType=None, filteredElement=None):
        """
        Returns the query for creating and populating a view table of flags raised in
        validation processes based on users settings.
        """
        sql = """
        CREATE OR REPLACE VIEW validation.filtered_flags AS
        SELECT * FROM validation.aux_flags_validacao
        """
        whereClause = ""
        # problemas com o Enum.
        if "process" in filterType.lower():
            filterTypeEnum = 0
        elif filterType:
            filterTypeEnum = 1
        if filterTypeEnum == DsgEnums.ProcessName:
            whereClause = " WHERE process_name = '{0}';".format(filteredElement)
        elif filterTypeEnum == DsgEnums.ClassName:
            whereClause = " WHERE layer = '{0}';".format(filteredElement)
        if filteredElement and filteredElement != "":
            sql = sql + whereClause
        return sql

    def checkCoverageForGaps(
        self, table="validation.coverage_temp", geomColumn="geom", keyColumn="id"
    ):
        tableSchema, tableName = table.split(".")
        sql = """
        select (ST_Dump(foo.geom)).geom as geom from (
        select (ST_GeoTableSummary('{0}', '{1}', '{2}', '{3}', 10, 'S4')).geom
        ) as foo
        where ST_IsEmpty(foo.geom) = 'f'
        """.format(
            tableSchema, tableName, geomColumn, keyColumn
        )
        return sql

    def createValidationHistoryViewTableQuery(self, idListString=None):
        """
        Returns the query for creating and populating a view table.
        Shows the history of validation processes, ordered by execution.
        If the optional parameter idListString is given, the list will
        be filtered to a list of given IDs (format: "(int)(id_1, id_2, ...)").
        This method uses the data on compact_process_history.
        """
        sql = """
        CREATE OR REPLACE VIEW validation.process_history_view AS
        SELECT t.process_name, t.log, s.status, t.finished
        FROM validation.compact_process_history AS t
        JOIN validation.status AS s ON t.status = s.id
        ORDER BY t.finished DESC;
        """
        if idListString:
            sql = sql.replace(
                "ORDER BY t.finished DESC;",
                "WHERE t.id in {0} ORDER BY t.finished DESC;",
            ).format(idListString)
        return sql

    def getQmlRecords(self, layerList):
        sql = """select layername, domainqml from public.domain_qml where layername in ('{0}')""".format(
            "','".join(layerList)
        )
        return sql

    def getImplementationVersion(self):
        sql = """select dbimplversion from public.db_metadata limit 1"""
        return sql

    def getValidationLogQuery(self):
        """
        Returns the query for a list of all logs UNIQUE registered for each
        process executed.
        """
        sql = """SELECT DISTINCT log, id FROM validation.compact_process_history;"""
        # ALTERAR PARA FUNÇÃO DE UPDATE DA TABELA PARA QUE INCLUA OS NOMES DE USUÁRIOS
        return sql

    def getValidationHistoryQuery(self, idListString=None):
        """
        Returns the query of all validation processes available informations.
        :param idListString:
        """
        sql = """SELECT * FROM validation.process_history;"""
        if idListString:
            sql = sql.replace(";", " WHERE id IN {};".format(idListString))
        return sql

    def createCompactValidationHistoryQuery(self):
        """
        Returns the query for compact validation history table creation.
        """
        sql = """
            DROP TABLE IF EXISTS validation.compact_process_history CASCADE;
            CREATE TABLE validation.compact_process_history (
                id serial NOT NULL,
                process_name varchar(200) NOT NULL,
                log text NOT NULL,
                status int NOT NULL,
                finished timestamp NOT NULL,
                CONSTRAINT compact_process_history_pk PRIMARY KEY (id),
                CONSTRAINT compact_process_history_status_fk FOREIGN KEY (status) REFERENCES validation.status (id) MATCH FULL ON UPDATE NO ACTION ON DELETE NO ACTION
        ); """
        return sql

    def populateCompactValidationHistoryQuery(self, logList):
        """
        Returns the query for compact validation history table population.
        :param logList: either a list of logs or a log line [id, process_name, log_text, status, finished_timestamp]
        """
        sql = ""
        if isinstance(logList, list):
            for log in logList:
                sql += """INSERT INTO validation.compact_process_history (id, process_name, log, status, finished) VALUES ({0}, '{1}', '{2}', {3}, '{4}');\n""".format(
                    log[0],
                    log[1],
                    log[2].replace(r"\n", "\n"),
                    log[3],
                    log[4].toPyDateTime(),
                )
        elif logList:
            sql += """INSERT INTO validation.compact_process_history (id, process_name, log, status, finished) VALUES ({0}, '{1}', '{2}', {3}, '{4}');\n""".format(
                logList[0],
                logList[1],
                logList[2].replace(r"\n", "\n"),
                logList[3],
                logList[4].toPyDateTime(),
            )
        return sql

    def getAttrListWithFilter(self):
        sql = """select distinct table_name from information_schema.columns where table_schema = 'dominios' and column_name = 'filter'"""
        return sql

    def getFilterJsonList(self, domainName):
        sql = (
            """select row_to_json(a) from (select * from dominios.{0}) as a """.format(
                domainName
            )
        )
        return sql

    def databaseInfo(self):
        """
        Gets database information to be displayed.
        :return: (str) SQL to executed.
        """
        sql = """
            SELECT f_table_schema, f_table_name, f_geometry_column, type, srid
                FROM public.geometry_columns
                ORDER BY f_table_schema, f_table_name ASC"""
        return sql

    def implementationVersion(self):
        """
        Query to retrieve database's implementation version, if available.
        :return: (str) query to database's implementation version (e.g. '5.2').
        """
        return """SELECT dbimplversion FROM public.db_metadata;"""

    def getSchemasFromInformationSchema(self):
        return f"""SELECT schema_name FROM information_schema.schemata"""

    def getTablesFromInformationSchema(self, schemaName):
        return f"""SELECT DISTINCT table_name from information_schema.tables where table_schema = '{schemaName}' """

    def getColumnsFromInformationSchema(self, schemaName):
        return f"""SELECT * FROM information_schema.columns WHERE table_schema = '{schemaName}'"""

    def getPrimaryKeyFromInformationSchema(self, schemaName):
        return f"""
        SELECT kcu.table_schema,
               kcu.table_name,
               tco.constraint_name,
               kcu.ordinal_position AS POSITION,
               kcu.column_name AS key_column
        FROM information_schema.table_constraints tco
        JOIN information_schema.key_column_usage kcu
             ON kcu.constraint_name = tco.constraint_name
             AND kcu.constraint_schema = tco.constraint_schema
             AND kcu.constraint_name = tco.constraint_name
        WHERE tco.constraint_type = 'PRIMARY KEY' AND kcu.table_schema = '{schemaName}'
        ORDER BY kcu.table_schema,
                 kcu.table_name,
                 position
        """

    def getAllValuesFromTable(self, schemaName, tableName, columnNameList):
        return f"SELECT {', '.join(columnNameList)} from {schemaName}.{tableName}"

    def getIfCollumnIsNullable(self, schemaName):
        return f"SELECT * FROM information_schema.columns WHERE table_schema='{schemaName}'"

    def getConstraintMapValueFromSchema(self):
        return f"""
        SELECT
            tc.table_schema,
            tc.constraint_name,
            tc.table_name,
            kcu.column_name,
            ccu.table_schema AS foreign_table_schema,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        """

    def getNameColumnTableDataTypeFromSchema(self, schemaName):
        return f"""
        SELECT column_name, table_name, data_type
        FROM information_schema.columns
        WHERE table_schema = '{schemaName}'
        """

    def getMaxLengthVarcharFromSchema(self, schemaName):
        return f"""
        SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '{schemaName}'
        """
