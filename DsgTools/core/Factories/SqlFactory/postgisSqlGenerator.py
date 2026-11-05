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
import re
from psycopg2 import sql as pgsql
from .sqlGenerator import SqlGenerator
from ...dsgEnums import DsgEnums

DB_ENCODING = "utf-8"

# Um elemento de nome qualificado como o PostgreSQL o escreve: entre aspas
# duplas (aspas internas dobradas) ou sem aspas, no formato de identificador.
_NOME_SQL = re.compile(
    r'\s*(?:"((?:[^"]|"")+)"|([A-Za-z_\u0080-￿][A-Za-z0-9_$\u0080-￿]*))\s*'
)
_FUNCAO_ST = re.compile(r"^ST_[A-Za-z0-9_]+$")
_LISTA_DE_IDS = re.compile(r"^\(\s*-?\d+(\s*,\s*-?\d+)*\s*\)$")


class PostGISSqlGenerator(SqlGenerator):
    """
    Gerador de SQL do PostGIS.

    Regra de composição (avaliação do CDCiber, 2026, achado 4.1): nome de
    schema, tabela, coluna, papel, usuário ou banco entra como
    psycopg2.sql.Identifier, e valor entra como psycopg2.sql.Literal ou como
    número convertido. Os métodos devolvem psycopg2.sql.Composed, que o
    PostgisDb executa pelo cursor; o psycopg2 faz o escape com a conexão viva
    (inclusive com standard_conforming_strings desligado, caso em que o
    escape manual por aspas simples dobradas não basta).

    Ficam em texto, com _qi/_el, só os métodos cujo consumidor manipula o
    texto: os que o PostgisDb parte em comandos por '#', o filtro de URI do
    QGIS e o DROP DATABASE executado por QSqlQuery no postgisDbThread.
    """

    # ------------------------------------------------------------------
    # Composição segura
    # ------------------------------------------------------------------

    @staticmethod
    def _ident(name):
        """Um nome cru (como está no catálogo) vira UM identificador."""
        return pgsql.Identifier(str(name))

    @staticmethod
    def _lit(value):
        """Um valor vira UM literal de texto, escapado pelo driver."""
        return pgsql.Literal(str(value))

    @staticmethod
    def _num(value):
        """
        Número para o SQL. Aceita int, float ou texto numérico; o resto
        levanta ValueError, em vez de entrar no comando.
        """
        if isinstance(value, bool):
            raise ValueError("valor numérico inválido: {0!r}".format(value))
        if isinstance(value, (int, float)):
            return pgsql.Literal(value)
        texto = str(value).strip()
        try:
            return pgsql.Literal(int(texto))
        except ValueError:
            pass
        try:
            numero = float(texto)
        except ValueError:
            raise ValueError("valor numérico inválido: {0!r}".format(value))
        if numero != numero or numero in (float("inf"), float("-inf")):
            raise ValueError("valor numérico inválido: {0!r}".format(value))
        return pgsql.Literal(numero)

    @classmethod
    def _val(cls, value):
        """Chave de feição: número quando é número, senão literal de texto."""
        try:
            return cls._num(value)
        except ValueError:
            return cls._lit(value)

    @classmethod
    def _literalList(cls, values):
        """
        Conteúdo de um IN (...): um literal por valor. Lista vazia vira ''
        como no texto antigo ("','".join([]) entre aspas).
        """
        values = list(values)
        if not values:
            return pgsql.Literal("")
        return pgsql.SQL(", ").join([cls._lit(v) for v in values])

    @classmethod
    def _qualified(cls, name):
        """
        'schema.tabela' como o código antigo tratava: tira as aspas, parte
        no ponto e põe cada parte entre aspas, agora pelo driver.
        """
        partes = str(name).replace('"', "").split(".")
        return pgsql.SQL(".").join([cls._ident(p) for p in partes])

    @staticmethod
    def _parseSqlName(text, maxParts=3):
        """
        Lê um nome já escrito em SQL (como o devolvido por
        pg_get_constraintdef: dominios.tabela, "Esquema"."Tabela") e o
        recompõe por Identifier. Parte sem aspas é dobrada para minúsculas,
        como o PostgreSQL faz; qualquer outra coisa além do nome levanta
        ValueError, em vez de seguir como SQL.
        """
        texto = str(text)
        pos = 0
        partes = []
        while True:
            m = _NOME_SQL.match(texto, pos)
            if not m:
                raise ValueError("nome SQL inválido: {0!r}".format(texto))
            if m.group(1) is not None:
                partes.append(m.group(1).replace('""', '"'))
            else:
                partes.append(
                    "".join(c.lower() if "A" <= c <= "Z" else c for c in m.group(2))
                )
            pos = m.end()
            if pos == len(texto):
                break
            if texto[pos] != ".":
                raise ValueError("nome SQL inválido: {0!r}".format(texto))
            pos += 1
        if len(partes) > maxParts:
            raise ValueError("nome SQL inválido: {0!r}".format(texto))
        return pgsql.SQL(".").join([pgsql.Identifier(p) for p in partes])

    @staticmethod
    def _semSeparador(*values):
        """
        Para os comandos que o PostgisDb parte por '#': um valor com '#'
        quebraria o comando no meio, então é recusado.
        """
        for value in values:
            if "#" in str(value):
                raise ValueError(
                    "nome ou valor com '#' não pode entrar neste comando: {0!r}".format(
                        value
                    )
                )

    def getComplexLinks(self, complex):
        return pgsql.SQL(
            "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = {0}"
        ).format(self._lit(complex))

    def getComplexTablesFromDatabase(self):
        sql = "select distinct table_name from information_schema.columns where table_schema = 'complexos'  ORDER BY table_name"
        return sql

    def getComplexData(self, complex_schema, complex):
        return pgsql.SQL("SELECT id, nome from {0}.{1}").format(
            self._ident(complex_schema), self._ident(complex)
        )

    def getAssociatedFeaturesData(
        self, aggregated_schema, aggregated_class, column_name, complex_uuid
    ):
        return pgsql.SQL("SELECT id from only {0}.{1} where {2}={3}").format(
            self._ident(aggregated_schema),
            self._ident(aggregated_class),
            self._ident(column_name),
            self._lit(complex_uuid),
        )

    def getLinkColumn(self, complexClass, aggregatedClass):
        return pgsql.SQL(
            "SELECT column_name from complex_schema where complex = {0} and aggregated_class = {1}"
        ).format(self._lit(complexClass), self._lit(aggregatedClass))

    def getSrid(self, parameters=dict()):
        if parameters == dict():
            return "SELECT DISTINCT srid from geometry_columns WHERE f_table_schema <> 'tiger' and f_table_schema <> 'topology' LIMIT 1"
        whereClauseList = []
        if "tableSchema" in list(parameters.keys()):
            whereClauseList.append(
                pgsql.SQL("f_table_schema = {0}").format(
                    self._lit(parameters["tableSchema"])
                )
            )
        if "tableName" in list(parameters.keys()):
            whereClauseList.append(
                pgsql.SQL("f_table_name = {0}").format(self._lit(parameters["tableName"]))
            )
        if "geometryColumn" in list(parameters.keys()):
            whereClauseList.append(
                pgsql.SQL("f_geometry_column = {0}").format(
                    self._lit(parameters["geometryColumn"])
                )
            )
        whereClause = pgsql.SQL(" AND ").join(whereClauseList)
        return pgsql.SQL(
            "SELECT DISTINCT srid from geometry_columns WHERE {0} LIMIT 1"
        ).format(whereClause)

    def getTablesFromDatabase(self):
        sql = "select distinct table_schema, table_name from information_schema.columns where (table_schema <> 'dominios' and table_schema <> 'topology')"
        return sql

    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        return pgsql.SQL("UPDATE complexos.{0} SET {1}=NULL WHERE id = {2}").format(
            self._ident(aggregated_class), self._ident(link_column), self._lit(uuid)
        )

    def getTemplates(self):
        sql = "SELECT datname FROM pg_database WHERE datistemplate = true;"
        return sql

    def allowConnections(self, name):
        return pgsql.SQL(
            "ALTER DATABASE {0} SET search_path = public, topology, cb, cc, complexos, ct;"
        ).format(self._ident(name))

    def loadLayerFromDatabase(self, layer_name, pkColumn="id"):
        """
        Fica em texto: é o filtro do QgsDataSourceUri, não vai ao cursor. A
        tabela já perdia as aspas antes de ser citada; a coluna passa por _qi.
        """
        layer_name = '"."'.join(layer_name.replace('"', "").split("."))
        pk = self._qi(pkColumn)
        sql = """{1} in (SELECT {1} FROM ONLY "{0}")""".format(layer_name, pk)
        return sql

    def loadLayerFromDatabaseUsingInh(self, layer_name, pkColumn="id"):
        layer_name = '"."'.join(layer_name.replace('"', "").split("."))
        pk = self._qi(pkColumn)
        sql = """{1} in (SELECT {1} FROM ONLY "{0}")""".format(layer_name, pk)
        return sql

    def getCreateDatabase(self, name, dropIfExists=False):
        db = self._ident(name)
        sql = pgsql.SQL("CREATE DATABASE {0};").format(db)
        if dropIfExists:
            sql = pgsql.SQL("DROP DATABASE IF EXISTS {0};").format(db) + sql
        return sql

    def insertFrameIntoTable(self, wkt):
        return pgsql.SQL(
            "INSERT INTO aux_moldura_a(geom) VALUES(ST_GeomFromText({0}))"
        ).format(self._lit(wkt))

    @staticmethod
    def _qualifiedIdentifier(schema, table):
        """
        Compõe schema.tabela pelo driver (psycopg2.sql.Identifier), que escapa
        aspas e mantém o nome inteiro como UM identificador. Aspas externas por
        format() não bastam: um nome com aspa dupla fechava o identificador e o
        resto virava SQL (avaliação do CDCiber, 2026, achado 4.1).
        """
        if schema:
            return pgsql.SQL("{}.{}").format(
                pgsql.Identifier(str(schema)), pgsql.Identifier(str(table))
            )
        return pgsql.Identifier(str(table))

    def getElementCountFromLayer(self, table):
        """
        Conta as feições de uma tabela, sem herança.
        table: 'schema.tabela' (o formato de getTableSchema) ou só 'tabela'.
        Devolve um psycopg2.sql.Composed, que o PostgisDb executa pelo cursor.
        """
        parts = str(table).split(".", 1)
        schema, name = (parts[0], parts[1]) if len(parts) == 2 else (None, parts[0])
        return pgsql.SQL("SELECT count(*) FROM ONLY {}").format(
            self._qualifiedIdentifier(schema, name)
        )

    def getElementCountFromLayerV2(self, schema, table, useInheritance):
        """
        Conta as feições de schema.tabela, com ou sem as tabelas filhas.
        Devolve um psycopg2.sql.Composed, que o PostgisDb executa pelo cursor.
        """
        only = pgsql.SQL("") if useInheritance else pgsql.SQL("ONLY ")
        return pgsql.SQL("SELECT count(*) FROM {}{}").format(
            only, self._qualifiedIdentifier(schema, table)
        )

    def getElementCountFromLayerWithInh(self, layer):
        parts = str(layer).split(".")
        if len(parts) == 2:
            quoted = pgsql.SQL("{0}.{1}").format(
                self._ident(parts[0]), self._ident(parts[1])
            )
        else:
            quoted = self._ident(layer)
        return pgsql.SQL("SELECT count(*) FROM {0}").format(quoted)

    def getDatabasesFromServer(self):
        sql = "SELECT datname FROM pg_database where datname <> 'postgres' and datname <> 'template' and datname <> 'template0' and datname <> 'template_postgis' and datistemplate = 'f'"
        return sql

    def dropDatabase(self, name):
        """
        Fica em texto porque o postgisDbThread executa por QSqlQuery, que não
        aceita Composed. O _qi dobra a aspa dupla: um banco chamado
        'alvo"--' derrubava o banco 'alvo' com aspas fixas no format().
        """
        return "DROP DATABASE %s " % self._qi(name)

    def createRoleStatements(self, roleName, mydict):
        """
        Comandos do perfil, um Composed por comando, na ordem do texto
        antigo. O PostgisDb executa um a um: antes ele partia o texto por ';',
        e um nome de schema ou tabela com ';' (vindo do JSON do perfil)
        virava outro comando mesmo entre aspas.
        """
        role = self._ident(roleName)
        stmts = [pgsql.SQL("CREATE ROLE {0} with NOLOGIN REPLICATION").format(role)]
        for db in list(mydict.keys()):
            for schema in list(mydict[db].keys()):
                sch = self._ident(schema)
                for cat in list(mydict[db][schema].keys()):
                    for tableName in list(mydict[db][schema][cat].keys()):
                        table = pgsql.SQL("{0}.{1}").format(sch, self._ident(tableName))
                        read = mydict[db][schema][cat][tableName]["read"]
                        write = mydict[db][schema][cat][tableName]["write"]
                        if write == "2":
                            stmts.append(
                                pgsql.SQL("GRANT ALL ON {0} TO {1}").format(table, role)
                            )
                        elif read == "2":
                            stmts.append(
                                pgsql.SQL("GRANT SELECT ON {0} TO {1}").format(
                                    table, role
                                )
                            )
                for tpl in (
                    "GRANT ALL ON SCHEMA {0} TO {1}",
                    "REVOKE CREATE ON SCHEMA {0} FROM {1}",
                    "GRANT USAGE ON SCHEMA {0} TO {1}",
                    "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA {0} TO {1}",
                    "GRANT USAGE ON ALL SEQUENCES IN SCHEMA {0} TO {1}",
                ):
                    stmts.append(pgsql.SQL(tpl).format(sch, role))

        # not needed anymore due to our generic approach
        # GRANT SELECT ON db_metadata TO <role>
        for tpl in (
            "GRANT SELECT ON public.geometry_columns TO {0}",
            "GRANT ALL ON ALL TABLES IN SCHEMA information_schema TO {0}",
            "GRANT ALL ON ALL TABLES IN SCHEMA pg_catalog TO {0}",
            "GRANT ALL ON SCHEMA information_schema TO {0}",
            "GRANT ALL ON SCHEMA pg_catalog TO {0}",
            "REVOKE CREATE ON SCHEMA information_schema FROM {0}",
            "REVOKE CREATE ON SCHEMA pg_catalog FROM {0}",
            "GRANT USAGE ON SCHEMA information_schema TO {0}",
            "GRANT USAGE ON SCHEMA pg_catalog TO {0}",
            "GRANT USAGE ON ALL SEQUENCES IN SCHEMA information_schema TO {0}",
            "GRANT USAGE ON ALL SEQUENCES IN SCHEMA pg_catalog TO {0}",
        ):
            stmts.append(pgsql.SQL(tpl).format(role))
        return stmts

    def createRole(self, roleName, mydict):
        """O perfil inteiro num Composed só, comandos separados por ';'."""
        return pgsql.SQL(";\n").join(self.createRoleStatements(roleName, mydict))

    def dropRole(self, role):
        """
        Lista de comandos, que o PostgisDb executa um a um (antes ele partia
        um texto por '#'). Dentro da função droprole o nome do papel e o do
        schema entram por quote_ident: concatenados crus no EXECUTE, um nome
        de papel com ';' virava comando dentro da função.
        """
        funcao = pgsql.SQL(
            """CREATE OR REPLACE FUNCTION droprole(name text) RETURNS void AS $BODY$
                    DECLARE
                        s text;
                    BEGIN
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL TABLES IN SCHEMA ' || quote_ident(table_schema) || ' FROM ' || quote_ident(name) from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ' || quote_ident(table_schema) || ' FROM ' || quote_ident(name) from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL SEQUENCES IN SCHEMA ' || quote_ident(table_schema) || ' FROM ' || quote_ident(name) from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON SCHEMA ' || quote_ident(table_schema) || ' FROM ' || quote_ident(name) from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        EXECUTE 'REVOKE ALL ON db_metadata FROM '|| quote_ident(name);
                        RETURN;

                    END
                $BODY$ LANGUAGE plpgsql;
            """
        )
        return [
            funcao,
            pgsql.SQL("SELECT droprole({0})").format(self._lit(role)),
            pgsql.SQL("DROP ROLE IF EXISTS {0}").format(self._ident(role)),
        ]

    def grantRole(self, user, role):
        return pgsql.SQL("GRANT {0} TO {1}").format(self._ident(role), self._ident(user))

    def revokeRole(self, user, role):
        return pgsql.SQL("REVOKE {0} FROM {1}").format(
            self._ident(role), self._ident(user)
        )

    def getRoles(self):
        sql = "SELECT rolname FROM pg_roles WHERE rolname <> 'postgres' AND rolcanlogin = 'f' AND rolname in (select split_part(unnest(nspacl)::text, '=', 1) from pg_namespace where nspname = 'pg_catalog')"
        return sql

    def getUserRelatedRoles(self, username):
        return pgsql.SQL(
            """select rolname, usename from
                    (select * from pg_roles as r where r.rolcanlogin = 'f' and r.rolname<>'postgres') as listaRoles left join
                    (select * from pg_auth_members as m join pg_user as u on m.member = u.usesysid and u.usename={0})
                    as euTenho on euTenho.roleid=listaRoles.oid  where rolname in (select split_part(unnest(nspacl)::text, '=', 1) from pg_namespace where nspname = 'pg_catalog')
                """
        ).format(self._lit(username))

    def getUsers(self):
        sql = "SELECT usename FROM pg_user WHERE usename <> 'postgres'"
        return sql

    def createUser(self, user, password, isSuperuser):
        """
        A senha entra como literal composto pelo driver, o mesmo escape do
        parâmetro %s do psycopg2 (CREATE ROLE não aceita parâmetro do
        servidor). O escape manual por aspas simples dobradas falha com
        standard_conforming_strings desligado.
        """
        if isSuperuser:
            tpl = "CREATE ROLE {0} WITH SUPERUSER CREATEDB CREATEROLE REPLICATION LOGIN PASSWORD {1};"
        else:
            tpl = "CREATE ROLE {0} WITH LOGIN PASSWORD {1};"
        return pgsql.SQL(tpl).format(self._ident(user), self._lit(password))

    def removeUser(self, user):
        return pgsql.SQL("DROP ROLE {0}").format(self._ident(user))

    def alterUserPass(self, user, newPass):
        return pgsql.SQL("ALTER ROLE {0} WITH PASSWORD {1}").format(
            self._ident(user), self._lit(newPass)
        )

    def validateWithDomain(self, schemaList):
        """
        A consulta devolve, na 6ª coluna, um SELECT que o PostgisDb executa.
        Coluna e tabela de domínio entram nele por quote_ident: concatenadas
        cruas, um nome de coluna no banco virava SQL na segunda execução.
        """
        return pgsql.SQL(
            """SELECT
                tc.table_schema,tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || quote_ident(ccu.column_name) || ' FROM dominios.' || quote_ident(ccu.table_name) || ' ORDER BY ' || quote_ident(ccu.column_name) || ' ASC'
                    FROM
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in ({0})"""
        ).format(self._literalList(schemaList))

    def getTableDomains(self, tableList):
        return pgsql.SQL(
            """SELECT
                tc.table_schema,tc.table_name, kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || quote_ident(ccu.column_name) || ' FROM dominios.' || quote_ident(ccu.table_name) || ' ORDER BY ' || quote_ident(ccu.column_name) || ' ASC'
                    FROM
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in ({0})"""
        ).format(self._literalList(tableList))

    def getNotNullFields(self, schemaList):
        return pgsql.SQL(
            "select table_schema, table_name, column_name from information_schema.columns where is_nullable = 'NO' and column_name not in ('id','geom') and table_schema in ({0})"
        ).format(self._literalList(schemaList))

    def getFeaturesWithSQL(self, layer, attrList):
        ls = pgsql.SQL(",").join([self._ident(a) for a in attrList])
        parts = str(layer).split(".")
        if len(parts) == 2:
            quoted_layer = pgsql.SQL("{0}.{1}").format(
                self._ident(parts[0]), self._ident(parts[1])
            )
        else:
            quoted_layer = self._ident(layer)
        return pgsql.SQL("SELECT {0} FROM ONLY {1}").format(ls, quoted_layer)

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
        parts = str(className).split(".")
        if len(parts) == 2:
            quoted_class = pgsql.SQL("{0}.{1}").format(
                self._ident(parts[0]), self._ident(parts[1])
            )
        else:
            quoted_class = self._ident(className)
        return pgsql.SQL("SELECT id from {0} where id ={1}").format(
            quoted_class, self._lit(id)
        )

    def getAggregatorFromComplexSchema(self, aggregated, aggregationColumn):
        return pgsql.SQL(
            "SELECT complex from public.complex_schema where aggregated_class = {0} and aggregationColumn = {1}"
        ).format(self._lit(aggregated), self._lit(aggregationColumn))

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
        return pgsql.SQL(
            "SELECT * FROM information_schema.role_table_grants where grantee = {0} and table_catalog = {1} ORDER BY table_name"
        ).format(self._lit(role), self._lit(dbname))

    def isSuperUser(self, user):
        return pgsql.SQL("SELECT rolsuper FROM pg_roles WHERE rolname = {0}").format(
            self._lit(user)
        )

    def getInvalidGeom(self, tableSchema, tableName, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select  distinct f.{3} as {3},(reason(ST_IsValidDetail(f.{2},0))), (location(ST_IsValidDetail(f.{2},0))) as {2} from (select {3}, {2} from only {0}.{1}  where ST_IsValid({2}) = 'f') as f"""
        ).format(
            self._ident(tableSchema),
            self._ident(tableName),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def getNonSimpleGeom(self, tableSchema, tableName):
        return pgsql.SQL(
            """select  f.id as id,(reason(ST_IsValidDetail(f.geom,0))), (location(ST_IsValidDetail(f.geom,0))) as geom from (select id, geom from only {0}.{1}  where ST_IsSimple(geom) = 'f') as f"""
        ).format(self._ident(tableSchema), self._ident(tableName))

    def checkValidationStructure(self):
        return "select count(*) from information_schema.columns where table_name = 'aux_flags_validacao'"

    def createValidationStructure(self, srid):
        # Texto partido por '#' no PostgisDb: o srid entra só como número.
        srid = str(self._num(srid).wrapped)
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
            CONSTRAINT settings_pk PRIMARY KEY (id)
        )#
        INSERT INTO validation.settings DEFAULT VALUES#
        INSERT INTO validation.status(id,status) VALUES (0,'Not yet ran'), (1,'Finished'), (2,'Failed'), (3,'Running'), (4,'Finished with flags')
        """ % (
            srid,
            srid,
            srid,
        )
        return sql

    def validationStatus(self, processName):
        return pgsql.SQL(
            "SELECT status FROM validation.process_history where process_name = {0} ORDER BY finished DESC LIMIT 1; "
        ).format(self._lit(processName))

    def validationStatusText(self, processName):
        return pgsql.SQL(
            "SELECT sta.status FROM validation.process_history as hist left join validation.status as sta on sta.id = hist.status where hist.process_name = {0} ORDER BY hist.finished DESC LIMIT 1 "
        ).format(self._lit(processName))

    def setValidationStatusQuery(self, processName, log, status):
        return pgsql.SQL(
            "INSERT INTO validation.process_history (process_name, log, status) values ({0},{1},{2})"
        ).format(self._lit(processName), self._lit(log), self._num(status))

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
        return pgsql.SQL(
            """INSERT INTO validation.{0} (process_name, layer, feat_id, reason, geom, dimension, geometry_column) values
        ({1},{2},{3},{4},ST_Transform(ST_SetSRID(ST_Multi({5}),{6}),{7}), {8}, {9});"""
        ).format(
            pgsql.Identifier(tableName),
            self._lit(processName),
            self._lit(layer),
            self._num(feat_id),
            self._lit(reason),
            self._lit(geom),
            self._num(srid),
            self._num(flagSRID),
            self._num(dimension),
            self._lit(geometryColumn),
        )

    def getRunningProc(self):
        sql = "SELECT process_name, status FROM validation.process_history ORDER BY finished DESC LIMIT 1;"
        return sql

    def deleteFlags(self, processName=None, className=None, flagId=None):
        # Texto partido por '#' no PostgisDb: valores por _el, sem '#'.
        if not processName and not className and not flagId:
            whereClause = ""
        else:
            clauseList = []
            if processName:
                self._semSeparador(processName)
                processClause = """process_name = '%s'""" % self._el(processName)
                clauseList.append(processClause)
            if className:
                self._semSeparador(className)
                classClause = """layer = '%s'""" % self._el(className)
                clauseList.append(classClause)
            if flagId:
                try:
                    for row in flagId:
                        flagClauseRow = """id = {0} """.format(self._num(row).wrapped)
                        clauseList.append(flagClauseRow)
                except TypeError:
                    flagClause = """id = {0} """.format(self._num(flagId).wrapped)
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
        # A função espacial e a necessidade eram SQL colado: só passam os
        # valores que a regra pode ter (ST_<nome> e 't' ou 'f').
        if not _FUNCAO_ST.match(str(predicate_function)):
            raise ValueError(
                "função espacial inválida: {0!r}".format(predicate_function)
            )
        if necessity not in ("'f'", "'t'"):
            raise ValueError("necessidade inválida: {0!r}".format(necessity))
        args = dict(
            pred=pgsql.SQL(predicate_function),
            nec=pgsql.SQL(necessity),
            ca=self._qualified(class_a),
            cb=self._qualified(class_b),
            ak=self._ident(aKeyColumn),
            bk=self._ident(bKeyColumn),
            ag=self._ident(aGeomColumn),
            bg=self._ident(bGeomColumn),
        )
        if min_card is not None:
            args["minc"] = self._num(min_card)
        if max_card is not None and max_card != "*":
            args["maxc"] = self._num(max_card)
        sameClass = class_a.replace('"', "") == class_b.replace('"', "")

        # checking if the rule checks the layer with itself
        if not sameClass:
            args["same"] = pgsql.SQL("")
        else:
            args["same"] = pgsql.SQL(" WHERE a.{ak} <> b.{bk} ").format(**args)

        if predicate_function == "ST_Disjoint":
            if necessity == "'f'":
                tpl = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.{ak} id, SUM(CASE WHEN {pred}(a.{ag},b.{bg}) = 'f' THEN 1 ELSE 0 END) count, a.{ag} geom
                    FROM {ca} as a,{cb} as b {same} GROUP BY a.{ak}, a.{ag}) as foo
                WHERE foo.count > 0
                """
            elif necessity == "'t'":
                tpl = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.{ak} id, SUM(CASE WHEN {pred}(a.{ag},b.{bg}) = 'f' THEN 1 ELSE 0 END) count, a.{ag} geom
                    FROM {ca} as a,{cb} as b {same} GROUP BY a.{ak}, a.{ag}) as foo
                WHERE foo.count = 0
                """
        else:
            if necessity == "'f'":  # must (be)
                if max_card == "*":
                    tpl = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{ak} id, SUM(CASE WHEN {pred}(a.{ag},b.{bg}) THEN 1 ELSE 0 END) count, a.{ag} geom
                        FROM {ca} as a,{cb} as b {same} GROUP BY a.{ak}, a.{ag}) as foo
                    WHERE foo.count < {minc}
                    """
                elif min_card is None and max_card is None:
                    tpl = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{ak} id, SUM(CASE WHEN {pred}(a.{ag},b.{bg}) THEN 1 ELSE 0 END) count, a.{ag} geom
                        FROM {ca} as a,{cb} as b {same} GROUP BY a.{ak}, a.{ag}) as foo
                    WHERE foo.count != 0;
                    """
                else:
                    tpl = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.{ak} id, SUM(CASE WHEN {pred}(a.{ag},b.{bg}) THEN 1 ELSE 0 END) count, a.{ag} geom
                        FROM {ca} as a,{cb} as b {same} GROUP BY a.{ak}, a.{ag}) as foo
                    WHERE foo.count < {minc} OR foo.count > {maxc}
                    """
            elif necessity == "'t'":  # must not (be)
                if not sameClass:
                    args["same"] = pgsql.SQL("")
                else:
                    args["same"] = pgsql.SQL(" AND a.{ak} <> b.{bk} ").format(**args)

                tpl = """SELECT DISTINCT a.{ak} id, (ST_Dump(ST_Intersection(a.{ag}, b.{bg}))).geom as geom
                FROM {ca} as a, {cb} as b
                    WHERE {pred}(a.{ag},b.{bg}) = {nec} {same}
                """
        return pgsql.SQL(tpl).format(**args)

    def getDimension(self, geom):
        return pgsql.SQL("select ST_Dimension({0})").format(self._lit(geom))

    def getMulti(self, cl):
        # TODO: get pk
        return pgsql.SQL(
            "select id from only {0} where ST_NumGeometries(geom) > 1"
        ).format(self._qualified(cl))

    def getDuplicatedGeom(self, schema, cl, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select * from (
        SELECT {3},
        ROW_NUMBER() OVER(PARTITION BY {2} ORDER BY {3} asc) AS Row,
        geom FROM ONLY {0}.{1}
        ) dups
        where
        dups.Row > 1"""
        ).format(
            self._ident(schema),
            self._ident(cl),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def getSmallAreas(self, schema, cl, areaTolerance, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select  foo2.{4}, foo2.{3} from (
        select {4}, {3}, ST_Area({3}) as area from {0}.{1}
        ) as foo2 where foo2.area < {2} order by foo2.{4} """
        ).format(
            self._ident(schema),
            self._ident(cl),
            self._num(areaTolerance),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def getSmallLines(self, schema, cl, areaTolerance, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select  foo2.{4}, foo2.{3} from (
        select {4}, {3}, ST_Length({3}) as len from {0}.{1}
        ) as foo2 where len < {2} order by foo2.{4} """
        ).format(
            self._ident(schema),
            self._ident(cl),
            self._num(areaTolerance),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def prepareVertexNearEdgesStruct(
        self, tableSchema, tableName, geometryColumn, keyColumn, geomType
    ):
        # Texto partido por '#' no PostgisDb: nomes por _qi, sem '#'.
        self._semSeparador(tableSchema, tableName, geometryColumn, keyColumn)
        q = [self._qi(v) for v in (tableSchema, tableName, geometryColumn, keyColumn)]
        if "POLYGON" in geomType:
            sql = """drop table if exists seg#
            create temp table seg as (
            SELECT segments.{3} as {3}, ST_MakeLine(sp,ep) as {2}
            FROM
            (SELECT
                ST_PointN({2}, generate_series(1, ST_NPoints({2})-1)) as sp,
                ST_PointN({2}, generate_series(2, ST_NPoints({2})  )) as ep,
                linestrings.{3} as {3}
                FROM
                (SELECT {3} as {3}, (ST_Dump(ST_Boundary({2}))).geom
                FROM only {0}.{1}
                ) AS linestrings
                ) AS segments)#
            drop table if exists pontos#
            create temp table pontos as select {3} as {3}, (ST_DumpPoints({2})).geom as {2} from only {0}.{1}#
            create index pontos_gist on pontos using gist ({2})#
            create index seg_gist on seg using gist ({2})""".format(*q)
        else:
            sql = """drop table if exists seg#
            create temp table seg as (
            SELECT segments.{3} as {3}, ST_MakeLine(sp,ep) as {2}
            FROM
            (SELECT
                ST_PointN({2}, generate_series(1, ST_NPoints({2})-1)) as sp,
                ST_PointN({2}, generate_series(2, ST_NPoints({2})  )) as ep,
                linestrings.{3} as {3}
                FROM
                (SELECT {3} as {3}, (ST_Dump({2})).geom
                FROM only {0}.{1}
                ) AS linestrings
                ) AS segments)#
            drop table if exists pontos#
            create temp table pontos as select {3} as {3}, (ST_DumpPoints({2})).geom as {2} from only {0}.{1}#
            create index pontos_gist on pontos using gist ({2})#
            create index seg_gist on seg using gist ({2})""".format(*q)
        return sql

    def getVertexNearEdgesStruct(self, epsg, tol, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select pontos.{3}, ST_SetSRID(pontos.{2},{0}) as {2} from pontos, seg where ST_DWithin(seg.{2}, pontos.{2}, {1}) and ST_Distance(seg.{2}, pontos.{2}) > 0"""
        ).format(
            self._num(epsg),
            self._num(tol),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def deleteFeatures(self, schema, table, idList, keyColumn):
        return pgsql.SQL(
            """DELETE FROM {0}.{1}
        WHERE {3} in ({2})"""
        ).format(
            self._ident(schema),
            self._ident(table),
            pgsql.SQL(",").join([self._val(i) for i in idList]),
            self._ident(keyColumn),
        )

    def deleteFeaturesNotIn(self, schema, table, idList):
        return pgsql.SQL(
            """DELETE FROM {0}.{1}
        WHERE id not in ({2})"""
        ).format(
            self._ident(schema),
            self._ident(table),
            pgsql.SQL(",").join([self._val(i) for i in idList]),
        )

    def getNotSimple(self, tableSchema, tableName, geometryColumn, keyColumn):
        return pgsql.SQL(
            """select foo.{3} as {3}, ST_MULTI(st_startpoint(foo.{2})) as {2} from (
        select {3} as {3}, (ST_Dump(ST_Node(ST_SetSRID(ST_MakeValid({2}),ST_SRID({2}))))).geom as {2} from {0}.{1}
        where ST_IsSimple({2}) = 'f') as foo where st_equals(st_startpoint(foo.{2}),st_endpoint(foo.{2}))"""
        ).format(
            self._ident(tableSchema),
            self._ident(tableName),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )

    def getOutofBoundsAngles(
        self, tableSchema, tableName, angle, geometryColumn, geomType, keyColumn
    ):
        args = (
            self._ident(tableSchema),
            self._ident(tableName),
            self._num(angle),
            self._ident(geometryColumn),
            self._ident(keyColumn),
        )
        if "LINESTRING" in geomType:
            tpl = """
            WITH result AS (SELECT points.{4}, points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN({3}, generate_series(1, ST_NPoints({3})-2)) as pt1,
                              ST_PointN({3}, generate_series(2, ST_NPoints({3})-1)) as anchor,
                              ST_PointN({3}, generate_series(3, ST_NPoints({3}))) as pt2,
                              linestrings.{4} as {4}
                            FROM
                              (SELECT {4} as {4}, (ST_Dump({3})).geom as {3}
                               FROM only {0}.{1}
                               ) AS linestrings WHERE ST_NPoints(linestrings.{3}) > 2 ) as points)
            select distinct {4}, anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))"""
        elif "POLYGON" in geomType:
            tpl = """
            WITH result AS (SELECT points.{4}, points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN({3}, generate_series(1, ST_NPoints({3})-1)) as pt1,
                              ST_PointN({3}, generate_series(1, ST_NPoints({3})-1) %  (ST_NPoints({3})-1)+1) as anchor,
                              ST_PointN({3}, generate_series(2, ST_NPoints({3})) %  (ST_NPoints({3})-1)+1) as pt2,
                              linestrings.{4} as {4}
                            FROM
                              (SELECT {4} as {4}, (ST_Dump(ST_Boundary(ST_ForceRHR((ST_Dump({3})).geom)))).geom as {3}
                               FROM only {0}.{1}
                               ) AS linestrings WHERE ST_NPoints(linestrings.{3}) > 2 ) as points)
            select distinct {4}, anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))"""
        return pgsql.SQL(tpl).format(*args)

    def getFlagsByProcess(self, processName):
        return pgsql.SQL(
            """select layer, feat_id, geometry_column from validation.aux_flags_validacao where process_name = {0}"""
        ).format(self._lit(processName))

    def forceValidity(
        self, tableSchema, tableName, idList, srid, keyColumn, geometryColumn
    ):
        return pgsql.SQL(
            """update {0}.{1} set {5} = ST_Multi(result.{5}) from (
        select distinct parts.{4}, ST_Union(parts.{5}) as {5} from {0}.{1} as source,
                                        (select {4} as {4}, ST_Multi(((ST_Dump(ST_SetSRID(ST_MakeValid({5}), {3}))).geom)) as {5} from
                                        {0}.{1}  where {4} in ({2})) as parts where ST_GeometryType(parts.{5}) = ST_GeometryType(source.{5}) group by parts.{4}
        ) as result where  result.{4} = {0}.{1}.{4} """
        ).format(
            self._ident(tableSchema),
            self._ident(tableName),
            pgsql.SQL(",").join([self._val(i) for i in idList]),
            self._num(srid),
            self._ident(keyColumn),
            self._ident(geometryColumn),
        )

    def getTableExtent(self, tableSchema, tableName):
        # TODO: put geometry column
        return pgsql.SQL(
            """
        SELECT ST_XMin(ST_Extent(geom)), ST_XMax(ST_Extent(geom)), ST_YMin(ST_Extent(geom)), ST_YMax(ST_Extent(geom)) AS extent FROM {0}.{1}
        """
        ).format(self._ident(tableSchema), self._ident(tableName))

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
        srid = self._num(epsg)
        for key in list(result.keys()):
            geoms = [
                pgsql.SQL("ST_SetSRID(ST_Multi({0}), {1})").format(self._lit(wkb), srid)
                for wkb in result[key]
            ]
            union = pgsql.SQL("ST_Union(ARRAY[{0}])").format(pgsql.SQL(",").join(geoms))
            sqls.append(
                pgsql.SQL(
                    """
            UPDATE {0}.{1} SET geom = ST_Multi({2}) WHERE id = {3}
            """
                ).format(
                    self._ident(tableSchema),
                    self._ident(tableName),
                    union,
                    self._val(key),
                )
            )
        return sqls

    def getOrphanTableElementCount(self, orphan):
        return pgsql.SQL("select id from {0} limit 1").format(self._qualified(orphan))

    def makeRelationDict(self, table, codes):
        """
        codes: lista de códigos, ou o texto '(1,2,3)' que o código antigo
        recebia. Outro texto levanta ValueError em vez de seguir como SQL.
        """
        if isinstance(codes, (list, tuple, set)):
            inClause = pgsql.SQL("({0})").format(
                pgsql.SQL(", ").join([self._val(c) for c in codes])
            )
        elif _LISTA_DE_IDS.match(str(codes)):
            inClause = pgsql.SQL(str(codes))
        else:
            raise ValueError("lista de códigos inválida: {0!r}".format(codes))
        return pgsql.SQL(
            "select code, code_name from dominios.{0} where code in {1}"
        ).format(self._ident(table), inClause)

    def getWhoAmI(self, cl, id):
        return pgsql.SQL(
            "select p.relname from {0} as c, pg_class as p where c.tableoid = p.oid and c.id = {1}"
        ).format(self._parseSqlName(cl), self._val(id))

    def snapLinesToFrame(
        self, cl, frameTable, tol, geometryColumn, keyColumn, frameGeometryColumn
    ):
        # Texto partido por '#' no PostgisDb: nomes por _qi, sem '#'.
        schema, table = cl.split(".")
        frameSchema, frameTable = frameTable.split(".")
        self._semSeparador(
            schema, table, frameSchema, frameTable, geometryColumn, keyColumn,
            frameGeometryColumn,
        )
        sql = """
        update {0}.{1} as classe set {5} = ST_Multi(agrupado.{5})
        from
            (
                select simplelines.{6} as {6}, ST_Union(simplelines.newline) as {5}
                from
                (
                    select short.{6}, St_SetPoint((ST_Dump(short.{5})).geom, 0,
                    ST_EndPoint(from_start)) as newline
                    from
                    (   select a.{6} as {6}, a.{5} as {5},
                        ST_ShortestLine(st_startpoint((ST_Dump(a.{5})).geom),
                        ST_Boundary(m.{7})) as from_start
                        from {0}.{1} a, {3}.{4} m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines.{6}
            ) as agrupado
        where classe.{6} = agrupado.{6}#
        update {0}.{1} as classe set {5} = ST_Multi(agrupado.{5})
        from
            (
                select simplelines.{6} as {6}, ST_Union(simplelines.newline) as {5}
                from
                (
                    select short.{6}, St_SetPoint((ST_Dump(short.{5})).geom,
                    short.index - 1, ST_EndPoint(from_start)) as newline
                    from
                    (   select a.{6} as {6}, a.{5} as {5},
                        ST_ShortestLine(st_endpoint((ST_Dump(a.{5})).geom),
                        ST_Boundary(m.{7})) as from_start,
                        ST_NPoints((ST_Dump(a.{5})).geom) as index
                        from {0}.{1} a, {3}.{4} m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines.{6}
            ) as agrupado
        where classe.{6} = agrupado.{6}
        """.format(
            self._qi(schema),
            self._qi(table),
            str(self._num(tol).wrapped),
            self._qi(frameSchema),
            self._qi(frameTable),
            self._qi(geometryColumn),
            self._qi(keyColumn),
            self._qi(frameGeometryColumn),
        )
        return sql

    def densifyFrame(
        self, cl, frameTable, snapTolerance, geometryColumn, frameGeometryColumn
    ):
        return pgsql.SQL(
            """
        update {2} m set {4} = st_multi(st_snap(m.{4},
        foo.vertices, {1}))
        from
        (
            select st_union(st_boundary(a.{3})) as vertices from
        {0} a
        ) as foo
        """
        ).format(
            self._qualified(cl),
            self._num(snapTolerance),
            self._qualified(frameTable),
            self._ident(geometryColumn),
            self._ident(frameGeometryColumn),
        )

    def snapToGrid(self, cl, precision, srid, geometryColumn):
        schema, table = cl.split(".")
        return pgsql.SQL(
            "update {0}.{1} set {4} = ST_SetSRID(ST_SnapToGrid({4},{2}),{3})"
        ).format(
            self._ident(schema),
            self._ident(table),
            self._num(precision),
            self._num(srid),
            self._ident(geometryColumn),
        )

    def makeRecursiveSnapFunction(self, geometryColumn, keyColumn):
        """
        As colunas ficam dentro de literais do corpo plpgsql: entram por _qi e
        com a aspa simples dobrada. A tabela, que chega em tempo de execução,
        passa por ::regclass, que só aceita um nome de tabela existente (antes
        era concatenada crua no EXECUTE).
        """
        for nome in (geometryColumn, keyColumn):
            if "$BODY$" in str(nome):
                raise ValueError("nome de coluna inválido: {0!r}".format(nome))
        geom = self._el(self._qi(geometryColumn))
        key = self._el(self._qi(keyColumn))
        sql = """
        CREATE OR REPLACE FUNCTION dsgsnap(tabela text, snap float) RETURNS void AS
        $BODY$
            DECLARE
            id int;
            BEGIN
                FOR id in execute('select {1} from '||tabela::regclass::text)
                LOOP
                    EXECUTE
                'update '||tabela::regclass::text||' as classe set {0} = st_multi(res.{0})
                from
                    (
                        select st_snap(a.{0}, st_collect(b.{0}), '||snap||') as {0}, a.{1} as {1}
                        from '||tabela::regclass::text||' a, '||tabela::regclass::text||' b
                        where a.{1} != b.{1} and st_isempty(a.{0}) = FALSE and a.{1} = '||id||'
                        group by a.{1}, a.{0}
                    ) as res
                where res.{1} = classe.{1} ';
                END LOOP;
                RETURN;
            END
        $BODY$
        LANGUAGE plpgsql;
        """.format(
            geom, key
        )
        return sql

    def executeRecursiveSnap(self, cl, tol):
        return pgsql.SQL("SELECT dsgsnap({0}, {1})").format(
            self._lit(cl), self._num(tol)
        )

    def createTempTable(self, layerName):
        # Texto partido por '#' no PostgisDb: nomes por _qi, sem '#'.
        schema, tableName = layerName.split(".")
        self._semSeparador(schema, tableName)
        sql = """
        DROP TABLE IF EXISTS {0}.{1}#
        CREATE TABLE {0}.{1} as (select * from {0}.{2} where 1=2)
        """.format(
            self._qi(schema), self._qi(tableName + "_temp"), self._qi(tableName)
        )
        return sql

    def dropTempTable(self, tableName):
        return pgsql.SQL("DROP TABLE IF EXISTS {0}").format(self._qualified(tableName))

    def populateTempTable(self, tableName, attributes, prepareValues):
        tableName = '"' + '"."'.join(tableName.split("."))
        columnTupleString = '"' + '","'.join(map(str, attributes)) + '"'
        valueTuppleString = ",".join(map(str, prepareValues))
        sql = """INSERT INTO {0}_temp"({1}) VALUES ({2})""".format(
            tableName, columnTupleString, valueTuppleString
        )
        return sql

    def createSpatialIndex(self, tableName, geomColumnName="geom"):
        partes = tableName.replace('"', "").split(".")
        tabela = partes[:-1] + [partes[-1] + "_temp"]
        return pgsql.SQL("create index {0} on {1} using gist ({2})").format(
            self._ident(partes[-1] + "_temp_gist"),
            pgsql.SQL(".").join([self._ident(p) for p in tabela]),
            self._ident(geomColumnName),
        )

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

    def getStylesFromDb(self, dbVersion):
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
        return pgsql.SQL(
            "SELECT styleqml from public.layer_styles where f_table_name = {0} and (stylename = {1} or stylename like {2})and f_table_catalog = current_database()"
        ).format(
            self._lit(table_name),
            self._lit(styleName),
            self._lit("{0}/%".format(styleName)),
        )

    def updateStyle(self, styleName, table_name, parsedQml, tableSchema):
        return pgsql.SQL(
            "UPDATE public.layer_styles SET styleqml = {0}, update_time = now() where f_table_name = {1} and description = {2}"
        ).format(self._lit(parsedQml), self._lit(table_name), self._lit(styleName))

    def getTableSchemaFromDb(self, table):
        return pgsql.SQL(
            "select distinct table_schema from information_schema.columns where table_name = {0} and table_schema not in ('validation','views')"
        ).format(self._lit(table))

    def getAllStylesFromDb(self):
        sql = """SELECT DISTINCT f_table_catalog, description, f_table_name, update_time from public.layer_styles order by f_table_catalog, description, f_table_name asc """
        return sql

    def deleteStyle(self, styleName):
        return pgsql.SQL("delete from public.layer_styles where description = {0}").format(
            self._lit(styleName)
        )

    def getGeometricSchemas(self):
        sql = "select distinct f_table_schema from public.geometry_columns"
        return sql

    def getGeomTablesFromGeometryColumns(self):
        sql = "select srid, f_geometry_column, type, f_table_schema, f_table_name from public.geometry_columns"
        return sql

    def _layerFilterClause(self, layerFilter, subquery):
        """
        O texto antigo montava '{text}' com '","'.join(layerFilter): um
        literal só, que com mais de uma camada não casa com nenhuma. A
        semântica é mantida (o literal único), agora escapado pelo driver.
        """
        if layerFilter:
            return self._lit('","'.join(layerFilter))
        return pgsql.SQL(subquery)

    def getGeomTablesDomains(self, layerFilter=None):
        inClause = self._layerFilterClause(
            layerFilter,
            "select f_table_name from public.geometry_columns where f_table_schema <> 'views'",
        )
        return pgsql.SQL(
            """select distinct case
            when split_part(conrelid::regclass::text,'.',2) = '' then replace(split_part(conrelid::regclass::text,'.',1),'"','')
            else replace(split_part(conrelid::regclass::text,'.',2),'"','')
            end as cl, pg_get_constraintdef(oid) FROM
            pg_constraint WHERE contype = 'f' and case
            when replace(split_part(conrelid::regclass::text,'.',2),'"','') = '' then replace(split_part(conrelid::regclass::text,'.',1),'"','')
            else replace(split_part(conrelid::regclass::text,'.',2),'"','')
        end in ({in_clause})
        """
        ).format(in_clause=inClause)

    def getGeomTableConstraints(self, layerFilter=None):
        inClause = self._layerFilterClause(
            layerFilter,
            "select f_table_name from public.geometry_columns where f_table_schema <> 'views'",
        )
        return pgsql.SQL(
            """select distinct case
            when split_part(conrelid::regclass::text,'.',2) = '' then split_part(conrelid::regclass::text,'.',1)
            else split_part(conrelid::regclass::text,'.',2)
            end as cl, pg_get_constraintdef(oid) FROM
             pg_constraint WHERE contype = 'c' and case
            when split_part(conrelid::regclass::text,'.',2) = '' then split_part(conrelid::regclass::text,'.',1)
            else split_part(conrelid::regclass::text,'.',2)
        end in ({in_clause})
        order by cl
        """
        ).format(in_clause=inClause)

    def getMultiColumns(self, schemaList):
        return pgsql.SQL(
            """select row_to_json(a) from (
                select t.table_name, array_agg(t.column_name::text) as attributes from
                (select table_name, column_name from information_schema.columns
                where data_type = 'ARRAY' and table_schema in ({0})
                ) as t group by t.table_name
            ) as a
        """
        ).format(self._literalList(schemaList))

    def getMultiColumnsFromTableList(self, tableList):
        return pgsql.SQL(
            """select row_to_json(a) from (
                select t.table_name, array_agg(t.column_name::text) as attributes from
                (select table_name, column_name from information_schema.columns
                where data_type = 'ARRAY' and table_name in ({0})
                ) as t group by t.table_name
            ) as a
        """
        ).format(self._literalList(tableList))

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
        whereStrList = []
        if filterList:
            whereStrList.append(
                pgsql.SQL(" f_table_name in ({0})").format(self._literalList(filterList))
            )
        if not showViews:
            whereStrList.append(pgsql.SQL(" table_type = 'BASE TABLE'"))
        whereClause = (
            pgsql.SQL("")
            if whereStrList == []
            else pgsql.SQL("WHERE ") + pgsql.SQL(" AND ").join(whereStrList)
        )
        return pgsql.SQL(
            """select f_table_schema, f_table_name, f_geometry_column, type, table_type from (select distinct f_table_schema, f_table_name, f_geometry_column, type, f_table_schema || '.' || f_table_name as jc  from public.geometry_columns as gc) as inn
            left join (select table_schema || '.' || table_name as jc, table_type from information_schema.tables) as infs on inn.jc = infs.jc
            {0}"""
        ).format(whereClause)

    def getNotNullDict(self, layerFilter=None):
        tableNameClause = self._layerFilterClause(
            layerFilter, "select distinct f_table_name from public.geometry_columns "
        )
        return pgsql.SQL(
            """select row_to_json(row(table_name, table_schema,  array_agg(column_name::text)))
                    from information_schema.columns
                    where table_name in ({table_name_clause})
                        and is_nullable = 'NO' and data_type = 'smallint'
                    group by table_name, table_schema
            """
        ).format(table_name_clause=tableNameClause)

    def getTableMetadataDict(self, layerFilter=None):
        filterClause = self._layerFilterClause(
            layerFilter,
            "select f_table_name from public.geometry_columns where f_table_schema <> 'views'",
        )
        return pgsql.SQL(
            """select row_to_json(a) from (
	                select table_schema, table_name, column_name as attr_name, is_nullable::boolean as nullable, data_type as column_type, gc.f_geometry_column as geometry_column, gc.type as geometry_type
					    from information_schema.columns as c
					left join public.geometry_columns as gc
						on c.table_name = gc.f_table_name and c.table_schema = gc.f_table_schema ) as a
	            where a.table_name in ({filter})
        """
        ).format(filter=filterClause)

    def getDomainDict(self, domainTable):
        """domainTable: nome já escrito em SQL (vem de pg_get_constraintdef)."""
        return pgsql.SQL("select row_to_json(row(code, code_name)) from {0}").format(
            self._parseSqlName(domainTable)
        )

    def getDomainCodeDict(self, domainTable):
        """domainTable: nome já escrito em SQL (vem de pg_get_constraintdef)."""
        return pgsql.SQL("select row_to_json(a) from (select * from {0}) as a").format(
            self._parseSqlName(domainTable)
        )

    def getDomainCodeDictWithColumns(self, domainTable, refPk, otherKey):
        """
        domainTable e refPk vêm de pg_get_constraintdef (já escritos em SQL);
        otherKey é o nome cru de uma coluna.
        """
        return pgsql.SQL(
            "select row_to_json(a) from (select {pk}, {fk} from {table}) as a"
        ).format(
            table=self._parseSqlName(domainTable),
            pk=self._parseSqlName(refPk, maxParts=1),
            fk=self._ident(otherKey),
        )

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

        campos = dict(
            schema=self._ident(tableSchema),
            table=self._ident(tableName),
            mi_col=self._ident(miAttr),
            inom_col=self._ident(inomAttr),
            geom_col=self._ident(geometryColumn),
            mi=self._lit(mi),
            inom=self._lit(inom),
            geo_srid=self._num(geoSrid),
            srid=self._num(srid),
        )
        if geomType == "MULTIPOLYGON":
            # frame é a geometria que o próprio código gera (QgsGeometry.asWkb),
            # não texto de usuário nem do banco; entra como antes.
            campos["frame"] = pgsql.SQL(str(frame))
            tpl = "INSERT INTO {schema}.{table} ({mi_col},{inom_col},{geom_col}) VALUES ({mi},{inom},ST_Transform(ST_Multi(ST_GeomFromWKB({frame},{geo_srid})), {srid}))"
        else:
            campos["frame"] = self._lit(frame)
            tpl = "INSERT INTO {schema}.{table} ({mi_col},{inom_col},{geom_col}) VALUES ({mi},{inom},ST_Transform((ST_SetSRID( (ST_Dump({frame})).geom,{geo_srid})), {srid}))"
        return pgsql.SQL(tpl).format(**campos)

    def createFromTemplate(self, dbName, templateName):
        return pgsql.SQL("CREATE DATABASE {0} with template = {1};").format(
            self._ident(dbName), self._ident(templateName)
        )

    def updateDbSRID(self, tableDict, srid):
        return pgsql.SQL("select UpdateGeometrySRID({0}, {1}, {2},{3})").format(
            self._lit(tableDict["tableSchema"]),
            self._lit(tableDict["tableName"]),
            self._lit(tableDict["geom"]),
            self._num(srid),
        )

    def setDbAsTemplate(self, dbName, setTemplate=True):
        flag = "t" if setTemplate else "f"
        return pgsql.SQL(
            "UPDATE pg_database set datistemplate = {0} where datname = {1};"
        ).format(pgsql.Literal(flag), self._lit(dbName))

    def checkTemplate(self):
        sql = """select datname from pg_database where datistemplate = 't'"""
        return sql

    def checkIfTemplate(self, dbName):
        return pgsql.SQL(
            "select datistemplate from pg_database where datname = {0}"
        ).format(self._lit(dbName))

    def alterSearchPath(self, dbName, version):
        if version == "2.1.3":
            tpl = "ALTER DATABASE {0} SET search_path = \"$user\", public, topology,'cb','complexos','dominios';"
        elif version == "2.1.3 Pro":
            tpl = "ALTER DATABASE {0} SET search_path = \"$user\", public, topology,'edgv','dominios';"
        elif version in ("3.0", "3.0 Pro", "3.0 Orto", "3.0 Topo"):
            tpl = "ALTER DATABASE {0} SET search_path = \"$user\", public, topology, pg_catalog, 'edgv' ,'dominios';"
        elif version == "FTer_2a_Ed":
            tpl = "ALTER DATABASE {0} SET search_path = \"$user\", public, topology,'pe','ge','complexos','dominios';"
        return pgsql.SQL(tpl).format(self._ident(dbName))

    def getUsersFromServer(self):
        sql = """SELECT usename, usesuper FROM pg_user WHERE usename <> 'postgres' order by usename"""
        return sql

    def reasignAndDropUser(self, user):
        """
        O nome ia cru e sem aspas: além da injeção, um usuário com maiúsculas
        caía em outro papel, o do nome dobrado para minúsculas.
        """
        return pgsql.SQL("REASSIGN OWNED BY {0} to postgres; DROP USER {0};").format(
            self._ident(user)
        )

    def deleteFeatureFlagsFromDb(self, layer, feat_id, processName):
        return pgsql.SQL(
            "DELETE FROM validation.aux_flags_validacao WHERE process_name = {0} AND layer = {1} AND feat_id = {2}"
        ).format(self._lit(processName), self._lit(layer), self._num(feat_id))

    def removeEmptyGeomtriesFromDb(self, layer, geometryColumn):
        schema, table = layer.split(".")
        return pgsql.SQL("DELETE FROM {0}.{1} WHERE st_isempty({2}) = TRUE").format(
            self._ident(schema), self._ident(table), self._ident(geometryColumn)
        )

    def getDomainTables(self):
        sql = """select distinct table_name from information_schema.columns where table_schema = 'dominios' order by table_name asc"""
        return sql

    def getGeometricSchemaList(self):
        sql = """select distinct f_table_schema from public.geometry_columns order by f_table_schema asc;"""
        return sql

    def getGeometricTableListFromSchema(self, schema):
        if isinstance(schema, list):
            schemaClause = pgsql.SQL("in ({0})").format(self._literalList(schema))
        else:
            schemaClause = pgsql.SQL("= {0}").format(self._lit(schema))
        return pgsql.SQL(
            """select distinct f_table_schema, f_table_name from public.geometry_columns where f_table_schema {0} and f_table_name in (
                select distinct table_name from information_schema.tables where table_type <> 'VIEW'
                )
                 order by f_table_name asc;"""
        ).format(schemaClause)

    def getParentGeomTables(self, schemaList):
        schemaList = [i for i in schemaList if i not in ["validation", "views"]]
        return pgsql.SQL(
            """select pgnsp.nspname, pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid)
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ({0}) and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union
            select distinct gc.f_table_schema,p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and
                gc.f_table_schema in ({0})

            order by tb"""
        ).format(self._literalList(schemaList))

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
        primitiveClause = pgsql.SQL("")
        viewClause = pgsql.SQL("")
        if dbPrimitiveList != []:
            primitiveClause = pgsql.SQL("and type in ({0})").format(
                self._literalList(dbPrimitiveList)
            )
        if excludeViews:
            viewClause = pgsql.SQL(
                "and f_table_name in (select table_name from information_schema.tables where table_type <> 'VIEW')"
            )
        selectClause = "f_table_schema, f_table_name"
        if geomColumn:
            selectClause += ",f_geometry_column"
        return pgsql.SQL(
            "select distinct {0} from public.geometry_columns where f_table_schema in ({1}) {2} {3} order by f_table_name"
        ).format(
            pgsql.SQL(selectClause),
            self._literalList(schemaList),
            primitiveClause,
            viewClause,
        )

    def getAttributeListFromTable(self, schema, tableName):
        return pgsql.SQL(
            """select distinct column_name from information_schema.columns where table_schema = {0} and table_name = {1} and column_name not in (
        select f_geometry_column from public.geometry_columns where f_table_schema = {0} and f_table_name = {1}
        )
        and column_name not like 'id%' order by column_name """
        ).format(self._lit(schema), self._lit(tableName))

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
        return pgsql.SQL(
            """ select row_to_json(a) from (select distinct column_name, data_type, is_nullable, column_default from information_schema.columns
        where table_schema = {0} and table_name = {1} and column_name not in (
        select f_geometry_column from public.geometry_columns where f_table_schema = {0} and f_table_name = {1}
        )
        and column_name not like 'id%' order by column_name ) as a
        """
        ).format(self._lit(schema), self._lit(tableName))

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
        """domainTable: nome cru da tabela em dominios (vem do catálogo)."""
        return pgsql.SQL(" select code from dominios.{0}").format(
            self._ident(domainTable)
        )

    def getDefaultFromDb(self, schema, tableName, attrName):
        return pgsql.SQL(
            "select column_default from information_schema.columns where table_schema = {0} and table_name = {1} and column_name = {2};"
        ).format(self._lit(schema), self._lit(tableName), self._lit(attrName))

    def upgradePostgis(self, updateDict):
        """
        updateDict vem de pg_available_extensions (nome e versão da
        extensão). O nome ia cru e a versão entre aspas fixas.
        """
        partes = [
            pgsql.SQL("ALTER EXTENSION {0} UPDATE TO {1};").format(
                self._parseSqlName(key, maxParts=1),
                self._ident(updateDict[key]["defaultVersion"]),
            )
            for key in updateDict
        ]
        return pgsql.SQL("").join(partes)

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
        return pgsql.SQL(
            "select table_name from information_schema.tables where table_schema = {0} and table_name = {1} limit 1"
        ).format(self._lit(schema), self._lit(tableName))

    def getPrimaryKeyColumn(self, tableName):
        """
        O nome vai como texto para o cast ::regclass, que só lê um nome. A
        montagem do texto é a de antes; muda só o literal, agora escapado.
        """
        if "." in tableName:
            tableSchema, tableName = (
                tableName.replace("'", "").replace('"', "").split(".")
            )
            tableName = '''"{0}"."{1}"'''.format(tableSchema, tableName)
        return pgsql.SQL(
            """
        SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = {0}::regclass
        AND    i.indisprimary;
        """
        ).format(self._lit(tableName))

    def getGeometryTablesCount(self):
        sql = """select count(*) from public.geometry_columns"""
        return sql

    def dropAllConections(self, dbName):
        return pgsql.SQL(
            """SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = {0}
                AND pid <> pg_backend_pid();"""
        ).format(self._lit(dbName))

    def getAttributesFromTable(self, tableSchema, tableName, typeFilter=None):
        whereClause = (
            pgsql.SQL("")
            if not typeFilter
            else pgsql.SQL(" and data_type in ({0}) ").format(
                self._literalList(typeFilter)
            )
        )
        return pgsql.SQL(
            """select column_name, data_type from information_schema.columns where
            table_schema = {0} and table_name = {1} {2} order by column_name """
        ).format(self._lit(tableSchema), self._lit(tableName), whereClause)

    def getViewDefinition(self, viewName):
        return pgsql.SQL("select pg_get_viewdef({0})").format(self._lit(viewName))

    def dropView(self, viewName):
        if '"' in viewName:
            # já escrito em SQL: lido como nome, nunca colado como texto
            view = self._parseSqlName(viewName)
        elif "." in viewName:
            schema, name = viewName.split(".")
            view = pgsql.SQL("{0}.{1}").format(self._ident(schema), self._ident(name))
        else:
            view = self._ident(viewName)
        return pgsql.SQL("DROP VIEW {0} ").format(view)

    def createViewStatement(self, viewName, viewDef):
        """
        viewName é lido como nome SQL. viewDef é SQL por contrato: a
        definição que o próprio PostgreSQL devolve em pg_get_viewdef.
        """
        return pgsql.SQL(" CREATE OR REPLACE VIEW {0} AS {1}").format(
            self._parseSqlName(viewName), pgsql.SQL(viewDef)
        )

    def checkPostGISAddonsInstallation(self):
        sql = """SELECT COUNT(*) FROM pg_proc WHERE proname = 'st_geotablesummary' """
        return sql

    def createCoverageTempTable(self, srid):
        return pgsql.SQL(
            """
        DROP TABLE IF EXISTS validation.coverage_temp;
        CREATE TABLE validation.coverage_temp (
            id serial NOT NULL,
            featid bigint NOT NULL,
            classname varchar(200) NOT NULL,
            geom geometry(MULTIPOLYGON, {0}) NOT NULL,
            CONSTRAINT coverage_pk PRIMARY KEY (id)
        )
        """
        ).format(self._num(srid))

    def checkCoverageForGapsWithFrame(self, frameTable, geomColumn):
        frameSchema, frameTable = frameTable.split(".")
        return pgsql.SQL(
            """
        select (ST_Dump(ST_SymDifference(a.geom, b.geom))).geom from
        (select ST_Union({0}) as geom from {1}.{2}) as a,
        (select ST_Union(geom) as geom from validation.coverage_temp) as b
        """
        ).format(
            self._ident(geomColumn), self._ident(frameSchema), self._ident(frameTable)
        )

    def checkCoverageForOverlaps(
        self, table="validation.coverage_temp", geomColumn="geom", keyColumn="id"
    ):
        tableSchema, tableName = table.split(".")
        return pgsql.SQL(
            """
        select (ST_Dump(foo.geom)).geom as geom from (
        select (ST_GeoTableSummary({0}, {1}, {2}, {3}, 10, 'S3')).geom
        ) as foo
        where ST_IsEmpty(foo.geom) = 'f'
        """
        ).format(
            self._lit(tableSchema),
            self._lit(tableName),
            self._lit(geomColumn),
            self._lit(keyColumn),
        )

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
        # problemas com o Enum.
        if "process" in filterType.lower():
            filterTypeEnum = 0
        elif filterType:
            filterTypeEnum = 1
        sql = pgsql.SQL(
            """
        SELECT * FROM validation.aux_flags_validacao;
            """
        )
        whereClause = pgsql.SQL("")
        if filterTypeEnum == DsgEnums.ProcessName:
            whereClause = pgsql.SQL(" WHERE process_name = {0};").format(
                self._lit(filteredElement)
            )
        elif filterType == DsgEnums.ClassName:
            whereClause = pgsql.SQL(" WHERE layer = {0};").format(
                self._lit(filteredElement)
            )
        if filteredElement and filteredElement != "":
            sql = sql + whereClause
        return sql

    def createFilteredFlagsViewTableQuery(self, filterType=None, filteredElement=None):
        """
        Returns the query for creating and populating a view table of flags raised in
        validation processes based on users settings.
        """
        sql = pgsql.SQL(
            """
        CREATE OR REPLACE VIEW validation.filtered_flags AS
        SELECT * FROM validation.aux_flags_validacao
        """
        )
        whereClause = pgsql.SQL("")
        # problemas com o Enum.
        if "process" in filterType.lower():
            filterTypeEnum = 0
        elif filterType:
            filterTypeEnum = 1
        if filterTypeEnum == DsgEnums.ProcessName:
            whereClause = pgsql.SQL(" WHERE process_name = {0};").format(
                self._lit(filteredElement)
            )
        elif filterTypeEnum == DsgEnums.ClassName:
            whereClause = pgsql.SQL(" WHERE layer = {0};").format(
                self._lit(filteredElement)
            )
        if filteredElement and filteredElement != "":
            sql = sql + whereClause
        return sql

    def checkCoverageForGaps(
        self, table="validation.coverage_temp", geomColumn="geom", keyColumn="id"
    ):
        tableSchema, tableName = table.split(".")
        return pgsql.SQL(
            """
        select (ST_Dump(foo.geom)).geom as geom from (
        select (ST_GeoTableSummary({0}, {1}, {2}, {3}, 10, 'S4')).geom
        ) as foo
        where ST_IsEmpty(foo.geom) = 'f'
        """
        ).format(
            self._lit(tableSchema),
            self._lit(tableName),
            self._lit(geomColumn),
            self._lit(keyColumn),
        )

    def createValidationHistoryViewTableQuery(self, idListString=None):
        """
        Returns the query for creating and populating a view table.
        Shows the history of validation processes, ordered by execution.
        If the optional parameter idListString is given, the list will
        be filtered to a list of given IDs (format: "(int)(id_1, id_2, ...)").
        This method uses the data on compact_process_history.
        O idListString só passa no formato (1, 2, 3); outro texto levanta
        ValueError em vez de seguir como SQL.
        """
        sql = """
        CREATE OR REPLACE VIEW validation.process_history_view AS
        SELECT t.process_name, t.log, s.status, t.finished
        FROM validation.compact_process_history AS t
        JOIN validation.status AS s ON t.status = s.id
        ORDER BY t.finished DESC;
        """
        if idListString:
            if not _LISTA_DE_IDS.match(str(idListString)):
                raise ValueError("lista de ids inválida: {0!r}".format(idListString))
            sql = sql.replace(
                "ORDER BY t.finished DESC;",
                "WHERE t.id in {0} ORDER BY t.finished DESC;",
            ).format(idListString)
        return sql

    def getQmlRecords(self, layerList):
        return pgsql.SQL(
            "select layername, domainqml from public.domain_qml where layername in ({0})"
        ).format(self._literalList(layerList))

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
        :param idListString: só no formato (1, 2, 3).
        """
        sql = """SELECT * FROM validation.process_history;"""
        if idListString:
            if not _LISTA_DE_IDS.match(str(idListString)):
                raise ValueError("lista de ids inválida: {0!r}".format(idListString))
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
        tpl = pgsql.SQL(
            "INSERT INTO validation.compact_process_history (id, process_name, log, status, finished) VALUES ({0}, {1}, {2}, {3}, {4});\n"
        )

        def linha(log):
            return tpl.format(
                self._num(log[0]),
                self._lit(log[1]),
                self._lit(log[2].replace(r"\n", "\n")),
                self._num(log[3]),
                self._lit(log[4].toPyDateTime()),
            )

        if isinstance(logList, list):
            return pgsql.SQL("").join([linha(log) for log in logList])
        elif logList:
            return linha(logList)
        return ""

    def getAttrListWithFilter(self):
        sql = """select distinct table_name from information_schema.columns where table_schema = 'dominios' and column_name = 'filter'"""
        return sql

    def getFilterJsonList(self, domainName):
        """domainName: nome cru da tabela em dominios (vem do catálogo)."""
        return pgsql.SQL("select row_to_json(a) from (select * from dominios.{0}) as a ").format(
            self._ident(domainName)
        )

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
