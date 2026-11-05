# -*- coding: utf-8 -*-
"""
Testes da revisão do gerador SQL PostGIS (avaliação de segurança do CDCiber,
2026, achado 4.1, parte "revisar todo o gerador").

Duas camadas, como em test_sqlInjectionCount.py:

1. Gerador (sempre roda): para cada método corrigido, uma entrada com aspas
   duplas, aspa simples, ponto e vírgula e comentário vira UM identificador
   (psycopg2.sql.Identifier) ou UM literal (psycopg2.sql.Literal) inteiro, e
   nenhum pedaço dela aparece como SQL cru. Onde o consumidor ainda recebe
   texto (comandos partidos por '#', DROP DATABASE por QSqlQuery, filtro de
   URI), o nome sai pelo escape de identificador e o separador é recusado.
   Valor que deveria ser número, função espacial ou lista de ids e chega com
   SQL levanta ValueError.

2. Banco (só com um PostgreSQL descartável configurado): os comandos críticos
   passam pelos consumidores reais do PostgisDb com uma conta administrativa,
   que tem privilégio para o comando injetado executar. O marcador é um
   papel (ou banco) que não pode passar a existir. Cobre: criar usuário com
   nome e senha maliciosos, alterar senha, grant e revoke de papel com nome
   malicioso, drop e create database com nome malicioso, e dois casos de
   segunda ordem (schema e tabela com nome malicioso no próprio banco, lidos
   pelo plugin e reaproveitados em outra consulta). A senha também é provada
   com standard_conforming_strings desligado, caso em que o escape antigo por
   aspas simples dobradas deixa o comando injetado executar.

   Variáveis de ambiente (os objetos são criados e destruídos pelo teste):
     DSGTOOLS_TEST_PG_HOST, DSGTOOLS_TEST_PG_PORT, DSGTOOLS_TEST_PG_DB,
     DSGTOOLS_TEST_PG_USER, DSGTOOLS_TEST_PG_PASSWORD (conta de superusuário
     do banco descartável).
"""
import datetime
import os
import secrets
import unittest

import psycopg2
from psycopg2 import sql as pgsql

from qgis.testing import start_app

start_app()

from DsgTools.core.Factories.SqlFactory.postgisSqlGenerator import (  # noqa: E402
    PostGISSqlGenerator,
)
from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb  # noqa: E402

# Aspas duplas, aspa simples, ponto e vírgula e comentário numa entrada só.
# Sem ponto e sem '#', para não ser partida nos métodos que recebem
# 'schema.tabela' nem nos que o PostgisDb divide por '#'.
P = "a\"b'c; DROP TABLE t; -- /*"
TRECHO = "DROP TABLE t"


def _qi(nome):
    return '"' + str(nome).replace('"', '""') + '"'


def _partes(x):
    if isinstance(x, (list, tuple)):
        for item in x:
            yield from _partes(item)
    elif isinstance(x, pgsql.Composed):
        for parte in x.seq:
            yield from _partes(parte)
    else:
        yield x


class _Data:
    def toPyDateTime(self):
        return datetime.datetime(2026, 11, 5, 10, 0, 0)


PERFIL_P = {"db": {P: {"cat": {P: {"read": "2", "write": "2"}}}}}

# (nome do teste, chamada, tipo, valor esperado)
#   ident: o valor esperado é exatamente um dos Identifier
#   lit:   o valor esperado é exatamente um dos Literal
#   erro:  levanta ValueError
#   texto: devolve texto que contém o valor esperado (escape de identificador)
CASOS = [
    # usuários e papéis
    ("createUser_nome", lambda g: g.createUser(P, "s", False), "ident", P),
    ("createUser_senha", lambda g: g.createUser("u", P, False), "lit", P),
    ("createUser_super_senha", lambda g: g.createUser("u", P, True), "lit", P),
    ("alterUserPass_nome", lambda g: g.alterUserPass(P, "s"), "ident", P),
    ("alterUserPass_senha", lambda g: g.alterUserPass("u", P), "lit", P),
    ("removeUser", lambda g: g.removeUser(P), "ident", P),
    ("grantRole_usuario", lambda g: g.grantRole(P, "r"), "ident", P),
    ("grantRole_papel", lambda g: g.grantRole("u", P), "ident", P),
    ("revokeRole_usuario", lambda g: g.revokeRole(P, "r"), "ident", P),
    ("revokeRole_papel", lambda g: g.revokeRole("u", P), "ident", P),
    ("reasignAndDropUser", lambda g: g.reasignAndDropUser(P), "ident", P),
    ("getUserRelatedRoles", lambda g: g.getUserRelatedRoles(P), "lit", P),
    ("isSuperUser", lambda g: g.isSuperUser(P), "lit", P),
    ("getRolePrivileges", lambda g: g.getRolePrivileges(P, P), "lit", P),
    ("createRoleStatements_papel", lambda g: g.createRoleStatements(P, {}), "ident", P),
    ("createRoleStatements_perfil", lambda g: g.createRoleStatements("r", PERFIL_P), "ident", P),
    ("createRole_inteiro", lambda g: g.createRole(P, PERFIL_P), "ident", P),
    ("dropRole_literal", lambda g: g.dropRole(P), "lit", P),
    ("dropRole_identificador", lambda g: g.dropRole(P), "ident", P),
    # bancos
    ("getCreateDatabase", lambda g: g.getCreateDatabase(P, True), "ident", P),
    ("createFromTemplate_banco", lambda g: g.createFromTemplate(P, "t"), "ident", P),
    ("createFromTemplate_modelo", lambda g: g.createFromTemplate("b", P), "ident", P),
    ("allowConnections", lambda g: g.allowConnections(P), "ident", P),
    ("alterSearchPath", lambda g: g.alterSearchPath(P, "3.0"), "ident", P),
    ("dropAllConections", lambda g: g.dropAllConections(P), "lit", P),
    ("setDbAsTemplate", lambda g: g.setDbAsTemplate(P), "lit", P),
    ("checkIfTemplate", lambda g: g.checkIfTemplate(P), "lit", P),
    ("upgradePostgis_versao", lambda g: g.upgradePostgis({"postgis": {"defaultVersion": P}}), "ident", P),
    ("upgradePostgis_extensao", lambda g: g.upgradePostgis({P: {"defaultVersion": "1"}}), "erro", None),
    ("dropDatabase_texto", lambda g: g.dropDatabase(P), "texto", "DROP DATABASE " + _qi(P) + " "),
    # catálogo, estilo e domínio
    ("getSrid", lambda g: g.getSrid({"tableSchema": P, "tableName": P, "geometryColumn": P}), "lit", P),
    ("getTableSchemaFromDb", lambda g: g.getTableSchemaFromDb(P), "lit", P),
    ("getGeomTables_schema", lambda g: g.getGeomTables([P]), "lit", P),
    ("getGeomTables_primitiva", lambda g: g.getGeomTables(["cb"], [P]), "lit", P),
    ("getGeometricTableListFromSchema_lista", lambda g: g.getGeometricTableListFromSchema([P]), "lit", P),
    ("getGeometricTableListFromSchema_texto", lambda g: g.getGeometricTableListFromSchema(P), "lit", P),
    ("getParentGeomTables", lambda g: g.getParentGeomTables([P]), "lit", P),
    ("getMultiColumns", lambda g: g.getMultiColumns([P]), "lit", P),
    ("getMultiColumnsFromTableList", lambda g: g.getMultiColumnsFromTableList([P]), "lit", P),
    ("getNotNullFields", lambda g: g.getNotNullFields([P]), "lit", P),
    ("validateWithDomain", lambda g: g.validateWithDomain([P]), "lit", P),
    ("getTableDomains", lambda g: g.getTableDomains([P]), "lit", P),
    ("getQmlRecords", lambda g: g.getQmlRecords([P]), "lit", P),
    ("getAttributesFromTable", lambda g: g.getAttributesFromTable(P, P, [P]), "lit", P),
    ("getAttributeListFromTable", lambda g: g.getAttributeListFromTable(P, P), "lit", P),
    ("getAttributeInfoFromTable", lambda g: g.getAttributeInfoFromTable(P, P), "lit", P),
    ("getDefaultFromDb", lambda g: g.getDefaultFromDb(P, P, P), "lit", P),
    ("checkIfTableExists", lambda g: g.checkIfTableExists(P, P), "lit", P),
    ("getStyle_nome", lambda g: g.getStyle(P, "t"), "lit", P),
    ("getStyle_padrao", lambda g: g.getStyle(P, "t"), "lit", P + "/%"),
    ("getStyle_tabela", lambda g: g.getStyle("e", P), "lit", P),
    ("updateStyle", lambda g: g.updateStyle(P, P, P, P), "lit", P),
    ("deleteStyle", lambda g: g.deleteStyle(P), "lit", P),
    ("updateDbSRID", lambda g: g.updateDbSRID({"tableSchema": P, "tableName": P, "geom": P}, 1), "lit", P),
    ("updateDbSRID_srid", lambda g: g.updateDbSRID({"tableSchema": "a", "tableName": "b", "geom": "c"}, "1); " + TRECHO), "erro", None),
    ("getViewDefinition", lambda g: g.getViewDefinition(P), "lit", P),
    ("getPrimaryKeyColumn", lambda g: g.getPrimaryKeyColumn(P), "lit", P),
    ("getGeomTablesDomains", lambda g: g.getGeomTablesDomains([P]), "lit", P),
    ("getGeomTableConstraints", lambda g: g.getGeomTableConstraints([P]), "lit", P),
    ("getNotNullDict", lambda g: g.getNotNullDict([P]), "lit", P),
    ("getTableMetadataDict", lambda g: g.getTableMetadataDict([P]), "lit", P),
    ("getGeomColumnTupleList", lambda g: g.getGeomColumnTupleList(False, [P]), "lit", P),
    ("getDomainDict_nome_sql", lambda g: g.getDomainDict("dominios." + _qi(P)), "ident", P),
    ("getDomainDict_texto_solto", lambda g: g.getDomainDict(P), "erro", None),
    ("getDomainCodeDict_nome_sql", lambda g: g.getDomainCodeDict(_qi(P)), "ident", P),
    ("getDomainCodeDict_texto_solto", lambda g: g.getDomainCodeDict("dominios.x; " + TRECHO), "erro", None),
    ("getDomainCodeDictWithColumns_coluna", lambda g: g.getDomainCodeDictWithColumns("dominios.x", "code", P), "ident", P),
    ("getDomainCodeDictWithColumns_pk", lambda g: g.getDomainCodeDictWithColumns("dominios.x", "code, (" + TRECHO + ")", "n"), "erro", None),
    ("dropView_nome_sql", lambda g: g.dropView(_qi("views") + "." + _qi(P)), "ident", P),
    ("dropView_texto_solto", lambda g: g.dropView(P), "erro", None),
    ("dropView_schema_ponto", lambda g: g.dropView("views.v'x;"), "ident", "v'x;"),
    ("createViewStatement_nome", lambda g: g.createViewStatement(_qi(P), "SELECT 1"), "ident", P),
    ("createViewStatement_texto_solto", lambda g: g.createViewStatement(P, "SELECT 1"), "erro", None),
    ("getAllDomainValues", lambda g: g.getAllDomainValues(P), "ident", P),
    ("getFilterJsonList", lambda g: g.getFilterJsonList(P), "ident", P),
    ("makeRelationDict_tabela", lambda g: g.makeRelationDict(P, [1, 2]), "ident", P),
    ("makeRelationDict_codigos", lambda g: g.makeRelationDict("t", "(1); " + TRECHO), "erro", None),
    ("getComplexLinks", lambda g: g.getComplexLinks(P), "lit", P),
    ("getComplexData", lambda g: g.getComplexData(P, P), "ident", P),
    ("getAssociatedFeaturesData_nome", lambda g: g.getAssociatedFeaturesData(P, P, P, "u"), "ident", P),
    ("getAssociatedFeaturesData_valor", lambda g: g.getAssociatedFeaturesData("s", "t", "c", P), "lit", P),
    ("getLinkColumn", lambda g: g.getLinkColumn(P, P), "lit", P),
    ("disassociateComplexFromComplex_nome", lambda g: g.disassociateComplexFromComplex(P, P, "u"), "ident", P),
    ("disassociateComplexFromComplex_valor", lambda g: g.disassociateComplexFromComplex("t", "c", P), "lit", P),
    ("getAggregatorFromId", lambda g: g.getAggregatorFromId("cb." + P, P), "ident", P),
    ("getAggregatorFromComplexSchema", lambda g: g.getAggregatorFromComplexSchema(P, P), "lit", P),
    ("getElementCountFromLayerWithInh", lambda g: g.getElementCountFromLayerWithInh("cb." + P), "ident", P),
    ("getFeaturesWithSQL", lambda g: g.getFeaturesWithSQL("cb." + P, [P]), "ident", P),
    ("getOrphanTableElementCount", lambda g: g.getOrphanTableElementCount("cb." + P), "ident", P.replace('"', "")),
    ("insertFrameIntoTable", lambda g: g.insertFrameIntoTable(P), "lit", P),
    ("insertFrame_nomes", lambda g: g.insertFrame("25k", "mi", "inom", "0103", 4674, 4674, {"tableSchema": P, "tableName": P, "miAttr": P, "inomAttr": P, "geom": P}), "ident", P),
    ("insertFrame_mi", lambda g: g.insertFrame("25k", P, "inom", "0103", 4674, 4674), "lit", P),
    ("insertFrame_srid", lambda g: g.insertFrame("25k", "mi", "inom", "0103", "4674); " + TRECHO, 4674), "erro", None),
    # validação, flags e edição de geometria
    ("getInvalidGeom", lambda g: g.getInvalidGeom(P, P, P, P), "ident", P),
    ("getNonSimpleGeom", lambda g: g.getNonSimpleGeom(P, P), "ident", P),
    ("validationStatus", lambda g: g.validationStatus(P), "lit", P),
    ("validationStatusText", lambda g: g.validationStatusText(P), "lit", P),
    ("setValidationStatusQuery", lambda g: g.setValidationStatusQuery(P, P, 1), "lit", P),
    ("setValidationStatusQuery_status", lambda g: g.setValidationStatusQuery("p", "l", "1); " + TRECHO), "erro", None),
    ("insertFlagIntoDb", lambda g: g.insertFlagIntoDb(P, 1, P, P, 4674, P, 0, P, 4674), "lit", P),
    ("insertFlagIntoDb_feicao", lambda g: g.insertFlagIntoDb("l", "1); " + TRECHO, "r", "g", 1, "p", 0, "c", 1), "erro", None),
    ("testSpatialRule_nomes", lambda g: g.testSpatialRule("cb." + P, "'f'", "ST_Intersects", "cb.x", 1, 2, P, P, P, P), "ident", P),
    ("testSpatialRule_funcao", lambda g: g.testSpatialRule("cb.a", "'f'", "ST_Intersects(1,1); " + TRECHO + "; --", "cb.b", 1, 2, "id", "id", "geom", "geom"), "erro", None),
    ("testSpatialRule_necessidade", lambda g: g.testSpatialRule("cb.a", "'t'; " + TRECHO, "ST_Intersects", "cb.b", 1, 2, "id", "id", "geom", "geom"), "erro", None),
    ("getDimension", lambda g: g.getDimension(P), "lit", P),
    ("getMulti", lambda g: g.getMulti("cb." + P), "ident", P.replace('"', "")),
    ("getDuplicatedGeom", lambda g: g.getDuplicatedGeom(P, P, P, P), "ident", P),
    ("getSmallAreas", lambda g: g.getSmallAreas(P, P, 1, P, P), "ident", P),
    ("getSmallAreas_tolerancia", lambda g: g.getSmallAreas("a", "b", "1 order by 1; " + TRECHO, "g", "k"), "erro", None),
    ("getSmallLines", lambda g: g.getSmallLines(P, P, 1, P, P), "ident", P),
    ("getVertexNearEdgesStruct", lambda g: g.getVertexNearEdgesStruct(4674, 1, P, P), "ident", P),
    ("getVertexNearEdgesStruct_epsg", lambda g: g.getVertexNearEdgesStruct("4674); " + TRECHO, 1, "g", "k"), "erro", None),
    ("deleteFeatures_nomes", lambda g: g.deleteFeatures(P, P, ["1"], P), "ident", P),
    ("deleteFeatures_id", lambda g: g.deleteFeatures("a", "b", ["1) or (1=1"], "id"), "lit", "1) or (1=1"),
    ("deleteFeaturesNotIn", lambda g: g.deleteFeaturesNotIn(P, P, [P]), "lit", P),
    ("getNotSimple", lambda g: g.getNotSimple(P, P, P, P), "ident", P),
    ("getOutofBoundsAngles", lambda g: g.getOutofBoundsAngles(P, P, 10, P, "LINESTRING", P), "ident", P),
    ("getFlagsByProcess", lambda g: g.getFlagsByProcess(P), "lit", P),
    ("forceValidity", lambda g: g.forceValidity(P, P, [P], 4674, P, P), "ident", P),
    ("getTableExtent", lambda g: g.getTableExtent(P, P), "ident", P),
    ("updateOriginalTable", lambda g: g.updateOriginalTable(P, P, {P: [P]}, 4674), "lit", P),
    ("getWhoAmI", lambda g: g.getWhoAmI("cb.x; " + TRECHO, 1), "erro", None),
    ("densifyFrame", lambda g: g.densifyFrame("cb." + P, "cb.m", 1, P, P), "ident", P),
    ("snapToGrid", lambda g: g.snapToGrid("cb." + P, 1, 4674, P), "ident", P),
    ("executeRecursiveSnap", lambda g: g.executeRecursiveSnap(P, 1), "lit", P),
    ("dropTempTable", lambda g: g.dropTempTable("cb." + P), "ident", P.replace('"', "")),
    ("createSpatialIndex", lambda g: g.createSpatialIndex("cb.t", P), "ident", P),
    ("deleteFeatureFlagsFromDb", lambda g: g.deleteFeatureFlagsFromDb(P, 1, P), "lit", P),
    ("removeEmptyGeomtriesFromDb", lambda g: g.removeEmptyGeomtriesFromDb("cb." + P, P), "ident", P),
    ("createCoverageTempTable", lambda g: g.createCoverageTempTable("4674) NOT NULL); " + TRECHO), "erro", None),
    ("checkCoverageForGapsWithFrame", lambda g: g.checkCoverageForGapsWithFrame("cb." + P, P), "ident", P),
    ("checkCoverageForOverlaps", lambda g: g.checkCoverageForOverlaps("cb." + P, P, P), "lit", P),
    ("checkCoverageForGaps", lambda g: g.checkCoverageForGaps("cb." + P, P, P), "lit", P),
    ("getFilteredFlagsQuery", lambda g: g.getFilteredFlagsQuery("process", P), "lit", P),
    ("createFilteredFlagsViewTableQuery", lambda g: g.createFilteredFlagsViewTableQuery("process", P), "lit", P),
    ("createValidationHistoryViewTableQuery", lambda g: g.createValidationHistoryViewTableQuery("(1); " + TRECHO), "erro", None),
    ("getValidationHistoryQuery", lambda g: g.getValidationHistoryQuery("(1); " + TRECHO), "erro", None),
    ("populateCompactValidationHistoryQuery", lambda g: g.populateCompactValidationHistoryQuery([[1, P, P, 1, _Data()]]), "lit", P),
    # texto que o consumidor parte por '#' ou não leva ao cursor
    ("deleteFlags_texto", lambda g: g.deleteFlags(P, P, [1]), "texto", "'" + P.replace("'", "''") + "'"),
    ("deleteFlags_separador", lambda g: g.deleteFlags("p#" + TRECHO), "erro", None),
    ("deleteFlags_id", lambda g: g.deleteFlags(flagId=["1 or 1=1"]), "erro", None),
    ("createTempTable_texto", lambda g: g.createTempTable("cb." + P), "texto", _qi(P + "_temp")),
    ("createTempTable_separador", lambda g: g.createTempTable("cb.t#" + TRECHO), "erro", None),
    ("prepareVertexNearEdgesStruct_texto", lambda g: g.prepareVertexNearEdgesStruct(P, P, P, P, "POLYGON"), "texto", "from only " + _qi(P) + "." + _qi(P)),
    ("prepareVertexNearEdgesStruct_separador", lambda g: g.prepareVertexNearEdgesStruct("s", "t#" + TRECHO, "g", "k", "POLYGON"), "erro", None),
    ("snapLinesToFrame_texto", lambda g: g.snapLinesToFrame("cb." + P, "cb.m", 1, P, P, P), "texto", "update " + _qi("cb") + "." + _qi(P)),
    ("snapLinesToFrame_separador", lambda g: g.snapLinesToFrame("cb.t#x", "cb.m", 1, "g", "k", "g"), "erro", None),
    ("snapLinesToFrame_tolerancia", lambda g: g.snapLinesToFrame("cb.t", "cb.m", "1#" + TRECHO, "g", "k", "g"), "erro", None),
    ("createValidationStructure_srid", lambda g: g.createValidationStructure("4674) NOT NULL)#" + TRECHO), "erro", None),
    ("makeRecursiveSnapFunction_coluna", lambda g: g.makeRecursiveSnapFunction(P, "id"), "texto", _qi(P).replace("'", "''")),
    ("makeRecursiveSnapFunction_tabela", lambda g: g.makeRecursiveSnapFunction("geom", "id"), "texto", "tabela::regclass::text"),
    ("loadLayerFromDatabase_coluna", lambda g: g.loadLayerFromDatabase("cb.t", P), "texto", _qi(P) + " in (SELECT " + _qi(P)),
]


def _fazerTeste(chamada, tipo, esperado):
    def teste(self):
        gen = PostGISSqlGenerator()
        if tipo == "erro":
            with self.assertRaises(ValueError):
                chamada(gen)
            return
        resultado = chamada(gen)
        if tipo == "texto":
            self.assertIsInstance(resultado, str)
            self.assertIn(esperado, resultado)
            return
        partes = list(_partes(resultado))
        for parte in partes:
            self.assertIsInstance(parte, pgsql.Composable, "o gerador devolveu texto")
        idents = [s for p in partes if isinstance(p, pgsql.Identifier) for s in p.strings]
        lits = [p.wrapped for p in partes if isinstance(p, pgsql.Literal)]
        sqls = [p.string for p in partes if isinstance(p, pgsql.SQL)]
        alvo = idents if tipo == "ident" else lits
        self.assertIn(esperado, alvo)
        for texto in sqls:
            self.assertNotIn(TRECHO, texto, "pedaço da entrada ficou como SQL cru")

    return teste


class TestGeradorSeguro(unittest.TestCase):
    """Um teste por método (e por parâmetro) corrigido."""

    def test_dropRole_funcao_usa_quote_ident(self):
        funcao = PostGISSqlGenerator().dropRole("r")[0]
        texto = "".join(p.string for p in _partes(funcao) if isinstance(p, pgsql.SQL))
        self.assertNotIn("' FROM ' || name", texto)
        self.assertEqual(texto.count("quote_ident(name)"), 5)

    def test_validateWithDomain_segunda_ordem_usa_quote_ident(self):
        consulta = PostGISSqlGenerator().validateWithDomain(["cb"])
        texto = "".join(p.string for p in _partes(consulta) if isinstance(p, pgsql.SQL))
        self.assertIn("quote_ident(ccu.column_name)", texto)
        self.assertIn("quote_ident(ccu.table_name)", texto)

    def test_parseSqlName_le_nome_escrito_em_sql(self):
        gen = PostGISSqlGenerator()
        ids = lambda c: [s for p in _partes(c) if isinstance(p, pgsql.Identifier) for s in p.strings]
        self.assertEqual(ids(gen._parseSqlName("dominios.Tipo")), ["dominios", "tipo"])
        self.assertEqual(ids(gen._parseSqlName('"Dom"."a""b"')), ["Dom", 'a"b'])
        for ruim in ("a.b; DROP TABLE t", 'a"."b', "a..b", "", "a.b.c.d", "(select 1)"):
            with self.assertRaises(ValueError, msg=ruim):
                gen._parseSqlName(ruim)


for _nome, _chamada, _tipo, _esperado in CASOS:
    setattr(TestGeradorSeguro, "test_" + _nome, _fazerTeste(_chamada, _tipo, _esperado))


def _config():
    chaves = ["HOST", "PORT", "DB", "USER", "PASSWORD"]
    valores = {c: os.environ.get("DSGTOOLS_TEST_PG_" + c) for c in chaves}
    return valores if all(valores.values()) else None


# Marcadores: papéis que o comando injetado criaria.
MARCADORES = [
    "marcador_injecao_" + s
    for s in ("nome", "senha", "senha_scs", "altera", "papel", "schema", "tabela")
]
USUARIO_MAL = 'usr_gerador"; CREATE ROLE marcador_injecao_nome; --'
PAPEL_MAL = 'pap_gerador"; CREATE ROLE marcador_injecao_papel; --'
SENHA_MAL = "x'; CREATE ROLE marcador_injecao_senha; --"
# Com standard_conforming_strings desligado a barra escapa a aspa que o _el
# dobrou, a aspa seguinte fecha o literal e o resto vira comando.
SENHA_MAL_SCS = "x\\'; CREATE ROLE marcador_injecao_senha_scs; --"
SENHA_MAL_ALTERA = "y\\'; CREATE ROLE marcador_injecao_altera; --"
BANCO_VITIMA = "alvo_gerador"
BANCO_MAL = 'alvo_gerador"--'
BANCO_NOVO_MAL = 'novo_gerador" OWNER "intruso_gerador'
INTRUSO = "intruso_gerador"
SCHEMA_MAL = "s_gerador'); CREATE ROLE marcador_injecao_schema; --"
TABELA_MAL = "t_gerador'; CREATE ROLE marcador_injecao_tabela; --"
ADMIN_SCS = "admin_scs_gerador"


@unittest.skipIf(_config() is None, "sem PostgreSQL descartável (DSGTOOLS_TEST_PG_*)")
class TestConsumidoresNoBanco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = _config()
        cls.senha_scs = secrets.token_hex(16)
        cls.admin = cls._conectar(cls.cfg["USER"], cls.cfg["PASSWORD"])
        cls.admin.autocommit = True
        cls._limpar()
        with cls.admin.cursor() as cur:
            cur.execute(
                pgsql.SQL("CREATE ROLE {} SUPERUSER LOGIN PASSWORD %s").format(
                    pgsql.Identifier(ADMIN_SCS)
                ),
                (cls.senha_scs,),
            )
            cur.execute(
                pgsql.SQL("ALTER ROLE {} SET standard_conforming_strings = off").format(
                    pgsql.Identifier(ADMIN_SCS)
                )
            )
            cur.execute(pgsql.SQL("CREATE ROLE {}").format(pgsql.Identifier(INTRUSO)))
            cur.execute(pgsql.SQL("CREATE ROLE {}").format(pgsql.Identifier(PAPEL_MAL)))

    @classmethod
    def tearDownClass(cls):
        cls._limpar()
        cls.admin.close()

    @classmethod
    def _conectar(cls, user, password, dbname=None):
        return psycopg2.connect(
            host=cls.cfg["HOST"], port=cls.cfg["PORT"], dbname=dbname or cls.cfg["DB"],
            user=user, password=password,
        )

    @classmethod
    def _limpar(cls):
        with cls.admin.cursor() as cur:
            for banco in (BANCO_VITIMA, BANCO_MAL, BANCO_NOVO_MAL, "novo_gerador"):
                cur.execute(
                    pgsql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                        pgsql.Identifier(banco)
                    )
                )
            cur.execute(pgsql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(pgsql.Identifier(SCHEMA_MAL)))
            cur.execute("DROP SCHEMA IF EXISTS s_gerador CASCADE")
            for papel in MARCADORES + [
                USUARIO_MAL, "usr_gerador", "usr_senha_gerador", ADMIN_SCS, INTRUSO,
                PAPEL_MAL, "pap_gerador", "membro_gerador",
            ]:
                cur.execute(pgsql.SQL("DROP ROLE IF EXISTS {}").format(pgsql.Identifier(papel)))

    def _postgisDb(self, user=None, password=None):
        db = PostgisDb()
        ok = db.testCredentials(
            self.cfg["HOST"], self.cfg["PORT"], self.cfg["DB"],
            user or self.cfg["USER"], password or self.cfg["PASSWORD"],
        )
        self.assertTrue(ok, "a conta não conectou")
        self.addCleanup(db.closeDatabase)
        return db

    def _existe_papel(self, db, nome):
        # Mesma conexão do consumidor: o papel criado por injeção e ainda não
        # confirmado aparece aqui.
        sql = "SELECT count(*) FROM pg_roles WHERE rolname = %s"
        try:
            return db._fetch_one(sql, (nome,))[0] > 0
        except Exception:
            db.db.rollback()
            return db._fetch_one(sql, (nome,))[0] > 0

    def _existe_banco(self, nome):
        with self.admin.cursor() as cur:
            cur.execute("SELECT count(*) FROM pg_database WHERE datname = %s", (nome,))
            return cur.fetchone()[0] > 0

    def _login(self, user, password):
        try:
            self._conectar(user, password).close()
            return True
        except psycopg2.OperationalError:
            return False

    # -- usuário e senha --------------------------------------------------

    def test_createUser_nome_e_senha_maliciosos(self):
        db = self._postgisDb()
        db.createUser(USUARIO_MAL, SENHA_MAL, False)
        self.assertFalse(self._existe_papel(db, "marcador_injecao_nome"))
        self.assertFalse(self._existe_papel(db, "marcador_injecao_senha"))
        self.assertTrue(self._existe_papel(db, USUARIO_MAL))
        db.db.commit()
        self.assertTrue(self._login(USUARIO_MAL, SENHA_MAL), "a senha não ficou gravada inteira")

    def test_createUser_senha_com_scs_desligado(self):
        db = self._postgisDb(ADMIN_SCS, self.senha_scs)
        db.createUser("usr_senha_gerador", SENHA_MAL_SCS, False)
        self.assertFalse(self._existe_papel(db, "marcador_injecao_senha_scs"))
        db.db.commit()
        self.assertTrue(self._login("usr_senha_gerador", SENHA_MAL_SCS))

    def test_alterUserPass_senha_com_scs_desligado(self):
        with self.admin.cursor() as cur:
            cur.execute("DROP ROLE IF EXISTS usr_gerador")
            cur.execute("CREATE ROLE usr_gerador LOGIN PASSWORD 'inicial'")
        db = self._postgisDb(ADMIN_SCS, self.senha_scs)
        db.alterUserPass("usr_gerador", SENHA_MAL_ALTERA)
        self.assertFalse(self._existe_papel(db, "marcador_injecao_altera"))
        db.db.commit()
        self.assertTrue(self._login("usr_gerador", SENHA_MAL_ALTERA))
        self.assertFalse(self._login("usr_gerador", "inicial"))

    # -- grant e revoke ---------------------------------------------------

    def _membro(self, papel, membro):
        with self.admin.cursor() as cur:
            cur.execute(
                """SELECT count(*) FROM pg_auth_members m
                   JOIN pg_roles r ON r.oid = m.roleid
                   JOIN pg_roles u ON u.oid = m.member
                   WHERE r.rolname = %s AND u.rolname = %s""",
                (papel, membro),
            )
            return cur.fetchone()[0] > 0

    def test_grant_e_revoke_de_papel_com_nome_malicioso(self):
        with self.admin.cursor() as cur:
            cur.execute("DROP ROLE IF EXISTS membro_gerador")
            cur.execute("CREATE ROLE membro_gerador")
        db = self._postgisDb()
        db.grantRole("membro_gerador", PAPEL_MAL)
        self.assertFalse(self._existe_papel(db, "marcador_injecao_papel"))
        db.db.commit()
        self.assertTrue(self._membro(PAPEL_MAL, "membro_gerador"))
        db.revokeRole("membro_gerador", PAPEL_MAL)
        self.assertFalse(self._existe_papel(db, "marcador_injecao_papel"))
        db.db.commit()
        self.assertFalse(self._membro(PAPEL_MAL, "membro_gerador"))

    # -- drop e create database ------------------------------------------

    def test_dropDatabase_nao_derruba_outro_banco(self):
        with self.admin.cursor() as cur:
            cur.execute(pgsql.SQL("CREATE DATABASE {}").format(pgsql.Identifier(BANCO_VITIMA)))
            cur.execute(pgsql.SQL("CREATE DATABASE {}").format(pgsql.Identifier(BANCO_MAL)))
        db = self._postgisDb()
        try:
            db.dropDatabase(BANCO_MAL)
        except Exception:
            pass
        self.assertTrue(self._existe_banco(BANCO_VITIMA), "o comando derrubou o banco vizinho")
        self.assertFalse(self._existe_banco(BANCO_MAL), "o banco pedido não foi apagado")

    def test_createDatabase_nome_malicioso_vira_um_nome(self):
        db = self._postgisDb()
        try:
            db.createDatabase(BANCO_NOVO_MAL)
        except Exception:
            pass
        self.assertFalse(self._existe_banco("novo_gerador"), "o OWNER injetado executou")
        self.assertTrue(self._existe_banco(BANCO_NOVO_MAL))
        with self.admin.cursor() as cur:
            cur.execute(
                "SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname = %s",
                (BANCO_NOVO_MAL,),
            )
            self.assertEqual(cur.fetchone()[0], self.cfg["USER"])

    # -- segunda ordem: nome malicioso gravado no próprio banco -----------

    def test_schema_malicioso_no_banco_nao_executa_na_listagem(self):
        with self.admin.cursor() as cur:
            cur.execute(pgsql.SQL("CREATE SCHEMA {}").format(pgsql.Identifier(SCHEMA_MAL)))
            cur.execute(
                pgsql.SQL("CREATE TABLE {}.veg_a (id serial PRIMARY KEY, geom geometry(Point, 4674))").format(
                    pgsql.Identifier(SCHEMA_MAL)
                )
            )
        db = self._postgisDb()
        try:
            camadas = db.listGeomClassesFromDatabase()
        except Exception:
            camadas = None
        self.assertFalse(self._existe_papel(db, "marcador_injecao_schema"))
        self.assertIn(SCHEMA_MAL + ".veg_a", camadas or [])

    def test_tabela_maliciosa_no_banco_nao_executa_na_busca_de_schema(self):
        with self.admin.cursor() as cur:
            cur.execute("CREATE SCHEMA s_gerador")
            cur.execute(
                pgsql.SQL("CREATE TABLE s_gerador.{} (id serial PRIMARY KEY)").format(
                    pgsql.Identifier(TABELA_MAL)
                )
            )
        db = self._postgisDb()
        try:
            schema = db.getTableSchemaFromDb(TABELA_MAL)
        except Exception:
            schema = None
        self.assertFalse(self._existe_papel(db, "marcador_injecao_tabela"))
        self.assertEqual(schema, "s_gerador")


if __name__ == "__main__":
    unittest.main()
