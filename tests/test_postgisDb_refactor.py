# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-01-01
        copyright            : (C) 2024 by Philipe Borba
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

"""
Tests para garantir que a refatoração de QSql → psycopg2 em PostgisDb
não introduza quebras de comportamento. Cada teste verifica o CONTRATO
do método (o que ele retorna e quando levanta exceção), de forma
independente da camada de execução de SQL.

Estratégia de mock
------------------
- self.postgis_db.db  → MagicMock com a interface do PsycopgDbAdapter
                        (pgConnectionAdapter.py), via patch() na classe
- self.postgis_db.gen → MagicMock que retorna strings SQL previsíveis
- self.mock_cursor    → o db.cursor() do adaptador; cada consulta do PostgisDb
                        (_execute, _fetch_one, _fetch_all) pede um cursor, e o
                        teste devolve um MockCursor com as linhas ou a falha

O mesmo conjunto de testes deve passar **antes** (QSql) e **depois**
(psycopg2) do refactor, pois testa comportamento, não implementação.
Os cenários são os mesmos da versão QSql: "consulta inativa" (isActive()
falso) e "exec() falhou" viram um cursor cujo execute() levanta
psycopg2.Error, que é como o psycopg2 sinaliza a mesma falha.
"""

import unittest
from unittest.mock import MagicMock, patch

import psycopg2

from qgis.testing import start_app

start_app()

# ---------------------------------------------------------------------------
# Importações do plugin (precisam de QGIS no path)
# ---------------------------------------------------------------------------
from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb  # noqa: E402
from DsgTools.core.Factories.DbFactory.pgConnectionAdapter import (  # noqa: E402
    PsycopgDbAdapter,
)


# ---------------------------------------------------------------------------
# Utilitários de mock
# ---------------------------------------------------------------------------


class MockCursor:
    """
    Simula o cursor psycopg2 que o PsycopgDbAdapter.cursor() devolve, para
    permitir testes sem banco real.

    Parâmetros
    ----------
    rows : list of tuple, opcional
        Linhas devolvidas por fetchall() / fetchone() depois do execute().
    is_active : bool
        Falso simula a consulta que o QSqlQuery deixava inativa: execute()
        levanta psycopg2.Error.
    exec_success : bool
        Falso simula o exec() que falhava: execute() levanta psycopg2.Error.
    exec_rows : list of tuple, opcional
        Linhas disponíveis após o execute() (equivale a rows; mantido para
        os cenários escritos na versão QSql).
    """

    def __init__(self, rows=None, is_active=True, exec_success=True, exec_rows=None):
        self._rows = list(exec_rows) if exec_rows else (list(rows) if rows else [])
        self._fails = not (is_active and exec_success)
        self.executed = []
        self.rowcount = -1

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        if self._fails:
            raise psycopg2.Error("Mock DB error")
        self.rowcount = len(self._rows)

    def fetchall(self):
        return list(self._rows)

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def close(self):
        pass


def make_mock_query(rows=None, is_active=True, exec_success=True, exec_rows=None):
    """Factory que retorna uma instância de MockCursor."""
    return MockCursor(
        rows=rows,
        is_active=is_active,
        exec_success=exec_success,
        exec_rows=exec_rows,
    )


# ---------------------------------------------------------------------------
# Classe base de teste
# ---------------------------------------------------------------------------


class PostgisDbTestBase(unittest.TestCase):
    """
    Configura um PostgisDb com todas as dependências de banco mockadas.

    Após setUp:
    - self.postgis_db.db  → MagicMock com a interface do PsycopgDbAdapter
    - self.postgis_db.gen → MagicMock (simula SqlGenerator)
    - self.mock_cursor    → self.postgis_db.db.cursor, que os testes alimentam
                            com MockCursor (return_value ou side_effect)
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        patcher_db = patch(
            "DsgTools.core.Factories.DbFactory.postgisDb.PsycopgDbAdapter"
        )
        patcher_gen = patch(
            "DsgTools.core.Factories.DbFactory.postgisDb.SqlGeneratorFactory"
        )

        self.mock_db_class = patcher_db.start()
        self.mock_gen_factory = patcher_gen.start()

        self.addCleanup(patcher_db.stop)
        self.addCleanup(patcher_gen.stop)

        # Instância retornada por PsycopgDbAdapter(); o spec faz o teste falhar
        # se o PostgisDb chamar no adaptador um método que ele não tem
        self.mock_db_instance = MagicMock(spec=PsycopgDbAdapter)
        self.mock_db_instance.isOpen.return_value = True
        self.mock_db_instance.open.return_value = True
        self.mock_db_class.return_value = self.mock_db_instance
        self.mock_cursor = self.mock_db_instance.cursor
        self.mock_cursor.return_value = make_mock_query()

        # Instância retornada por SqlGeneratorFactory().createSqlGenerator(...)
        self.mock_gen = MagicMock()
        self.mock_gen_factory.return_value.createSqlGenerator.return_value = (
            self.mock_gen
        )

        self.postgis_db = PostgisDb()


# ===========================================================================
# 1. Métodos de conexão / informação básica
# ===========================================================================


class TestConnectionMethods(PostgisDbTestBase):
    def test_getDatabaseName_delegates_to_db(self):
        self.postgis_db.db.databaseName.return_value = "test_db"
        self.assertEqual(self.postgis_db.getDatabaseName(), "test_db")

    def test_getHostName_returns_str(self):
        self.postgis_db.db.hostName.return_value = "localhost"
        self.assertEqual(self.postgis_db.getHostName(), "localhost")

    def test_getDatabaseParameters_returns_tuple(self):
        self.postgis_db.db.hostName.return_value = "host"
        self.postgis_db.db.port.return_value = 5432
        self.postgis_db.db.userName.return_value = "user"
        self.postgis_db.db.password.return_value = "pass"

        result = self.postgis_db.getDatabaseParameters()
        self.assertEqual(result, ("host", 5432, "user", "pass"))

    def test_checkAndOpenDb_opens_when_closed(self):
        self.postgis_db.db.isOpen.return_value = False
        self.postgis_db.db.open.return_value = True
        # Não deve levantar exceção
        self.postgis_db.checkAndOpenDb()
        self.postgis_db.db.open.assert_called_once()

    def test_checkAndOpenDb_raises_on_open_failure(self):
        self.postgis_db.db.isOpen.return_value = False
        self.postgis_db.db.open.return_value = False
        self.postgis_db.db.lastError.return_value.text.return_value = "conn refused"
        with self.assertRaises(Exception) as ctx:
            self.postgis_db.checkAndOpenDb()
        self.assertIn("conn refused", str(ctx.exception))

    def test_checkAndOpenDb_does_not_reopen_when_already_open(self):
        self.postgis_db.db.isOpen.return_value = True
        self.postgis_db.checkAndOpenDb()
        self.postgis_db.db.open.assert_not_called()


# ===========================================================================
# 2. getDatabaseVersion  (postgisDb)
# ===========================================================================


class TestGetDatabaseVersion(PostgisDbTestBase):
    def test_returns_version_string(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_cursor.return_value = make_mock_query(rows=[("3.0",)], is_active=True)

        result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "3.0")

    def test_returns_non_edgv_when_query_inactive(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "Non_EDGV")

    def test_returns_minus_one_when_no_rows(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=True)

        result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "-1")


# ===========================================================================
# 3. findEPSG  (abstractDb)
# ===========================================================================


class TestFindEPSG(PostgisDbTestBase):
    def test_returns_srid(self):
        self.mock_gen.getSrid.return_value = "SELECT srid()"
        self.mock_cursor.return_value = make_mock_query(rows=[(4674,)], is_active=True)

        result = self.postgis_db.findEPSG()
        self.assertEqual(result, 4674)

    def test_raises_on_inactive_query(self):
        self.mock_gen.getSrid.return_value = "SELECT srid()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.findEPSG()
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_returns_minus_one_when_no_rows(self):
        self.mock_gen.getSrid.return_value = "SELECT srid()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=True)

        result = self.postgis_db.findEPSG()
        self.assertEqual(result, -1)


# ===========================================================================
# 6. implementationVersion / getImplementationVersion  (abstractDb)
# ===========================================================================


class TestImplementationVersion(PostgisDbTestBase):
    def test_returns_version(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        self.mock_cursor.return_value = make_mock_query(rows=[("5.0",)], is_active=True)

        result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "5.0")

    def test_returns_empty_string_when_inactive(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "")

    def test_returns_empty_string_when_value_is_none(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        self.mock_cursor.return_value = make_mock_query(rows=[(None,)], is_active=True)

        result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "")

    def test_getImplementationVersion_returns_version(self):
        self.mock_gen.getImplementationVersion.return_value = "SELECT implv()"
        self.mock_cursor.return_value = make_mock_query(rows=[("5.1",)], is_active=True)

        result = self.postgis_db.getImplementationVersion()
        self.assertEqual(result, "5.1")

    def test_getImplementationVersion_raises_on_inactive(self):
        self.mock_gen.getImplementationVersion.return_value = "SELECT implv()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getImplementationVersion()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 7. getStructureDict  (postgisDb)
# ===========================================================================


class TestGetStructureDict(PostgisDbTestBase):
    def _setup_version(self, version, struct_rows):
        """Configura getDatabaseVersion e getStructure com um único side_effect."""
        call_count = [0]

        def query_factory(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # getDatabaseVersion call
                return make_mock_query(rows=[(version,)], is_active=True)
            else:
                # getStructure call
                return make_mock_query(rows=struct_rows, is_active=True)

        self.mock_cursor.side_effect = query_factory

    def test_returns_populated_dict(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_gen.getStructure.return_value = "SELECT struct()"

        self._setup_version(
            version="3.0",
            struct_rows=[
                ("cb", "infra_via_deslocamento_l", "id"),
                ("cb", "infra_via_deslocamento_l", "geom"),
            ],
        )

        result = self.postgis_db.getStructureDict()
        self.assertIn("cb.infra_via_deslocamento_l", result)

    def test_raises_on_inactive_struct_query(self):
        call_count = [0]

        def query_factory(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return make_mock_query(rows=[("3.0",)], is_active=True)
            return make_mock_query(rows=[], is_active=False)

        self.mock_cursor.side_effect = query_factory
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_gen.getStructure.return_value = "SELECT struct()"

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getStructureDict()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 8. listComplexClassesFromDatabase  (postgisDb)
# ===========================================================================


class TestListComplexClassesFromDatabase(PostgisDbTestBase):
    def test_returns_only_complexos_schema(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[
                ("cb", "infra_via_l"),
                ("complexos", "pto_ref_geod_topo_p"),
                ("complexos", "complexo_portuario_a"),
            ],
            is_active=True,
        )

        result = self.postgis_db.listComplexClassesFromDatabase()
        self.assertIn("complexos.pto_ref_geod_topo_p", result)
        self.assertIn("complexos.complexo_portuario_a", result)
        self.assertNotIn("cb.infra_via_l", result)

    def test_result_is_sorted(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[
                ("complexos", "z_ultimo"),
                ("complexos", "a_primeiro"),
            ],
            is_active=True,
        )

        result = self.postgis_db.listComplexClassesFromDatabase()
        self.assertEqual(result, sorted(result))

    def test_raises_on_inactive_query(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.listComplexClassesFromDatabase()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 9. getTablesFromDatabase  (postgisDb)
# ===========================================================================


class TestGetTablesFromDatabase(PostgisDbTestBase):
    def test_returns_schema_dot_table_list(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[
                ("cb", "infra_via_l"),
                ("complexos", "estrutura_a"),
            ],
            is_active=True,
        )

        result = self.postgis_db.getTablesFromDatabase()
        self.assertIn("cb.infra_via_l", result)
        self.assertIn("complexos.estrutura_a", result)

    def test_raises_on_inactive_query(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getTablesFromDatabase()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 10. getUsers / getUserRelatedRoles / getRoles  (postgisDb)
# ===========================================================================


class TestUserMethods(PostgisDbTestBase):
    def test_getUsers_returns_sorted_list(self):
        self.mock_gen.getUsers.return_value = "SELECT users()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("zebra",), ("alice",), ("bob",)], is_active=True
        )

        result = self.postgis_db.getUsers()
        self.assertEqual(result, ["alice", "bob", "zebra"])

    def test_getUsers_raises_on_inactive(self):
        self.mock_gen.getUsers.return_value = "SELECT users()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getUsers()
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_getUserRelatedRoles_separates_installed_and_assigned(self):
        """
        Regra: rolname com usename vazio → installed; com usename → assigned.
        """
        self.mock_gen.getUserRelatedRoles.return_value = "SELECT roles()"
        # (rolname, usename)
        self.mock_cursor.return_value = make_mock_query(
            rows=[
                ("role_leitura", None),
                ("role_edicao", None),
                ("role_admin", "alice"),
            ],
            is_active=True,
        )

        installed, assigned = self.postgis_db.getUserRelatedRoles("alice")
        self.assertIn("role_leitura", installed)
        self.assertIn("role_edicao", installed)
        self.assertIn("role_admin", assigned)
        self.assertEqual(installed, sorted(installed))
        self.assertEqual(assigned, sorted(assigned))

    def test_getRoles_returns_sorted_list(self):
        self.mock_gen.getRoles.return_value = "SELECT roles()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("role_z",), ("role_a",)], is_active=True
        )

        result = self.postgis_db.getRoles()
        self.assertEqual(result, ["role_a", "role_z"])

    def test_getRoles_raises_on_inactive(self):
        self.mock_gen.getRoles.return_value = "SELECT roles()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getRoles()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 11. createUser / removeUser / alterUserPass  (postgisDb)
# ===========================================================================


class TestUserDMLMethods(PostgisDbTestBase):
    def test_createUser_executes_sql(self):
        self.mock_gen.createUser.return_value = "CREATE USER alice"
        mock_query = make_mock_query(exec_success=True)
        self.mock_cursor.return_value = mock_query

        # Não deve levantar exceção
        self.postgis_db.createUser("alice", "senha123", False)
        self.mock_gen.createUser.assert_called_once_with("alice", "senha123", False)

    def test_createUser_raises_on_exec_failure(self):
        self.mock_gen.createUser.return_value = "CREATE USER alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.createUser("alice", "senha123", False)
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_removeUser_executes_sql(self):
        self.mock_gen.removeUser.return_value = "DROP USER alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.removeUser("alice")
        self.mock_gen.removeUser.assert_called_once_with("alice")

    def test_removeUser_raises_on_exec_failure(self):
        self.mock_gen.removeUser.return_value = "DROP USER alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.removeUser("alice")
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_alterUserPass_executes_sql(self):
        self.mock_gen.alterUserPass.return_value = "ALTER USER alice PASSWORD 'nova'"
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.alterUserPass("alice", "nova")
        self.mock_gen.alterUserPass.assert_called_once_with("alice", "nova")

    def test_alterUserPass_raises_on_failure(self):
        self.mock_gen.alterUserPass.return_value = "ALTER USER alice PASSWORD 'nova'"
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.alterUserPass("alice", "nova")
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 12. grantRole / revokeRole  (postgisDb)
# ===========================================================================


class TestRoleDMLMethods(PostgisDbTestBase):
    def test_grantRole_executes_sql(self):
        self.mock_gen.grantRole.return_value = "GRANT role_leitura TO alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.grantRole("alice", "role_leitura")
        self.mock_gen.grantRole.assert_called_once_with("alice", "role_leitura")

    def test_grantRole_raises_on_failure(self):
        self.mock_gen.grantRole.return_value = "GRANT ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.grantRole("alice", "role_leitura")
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_revokeRole_executes_sql(self):
        self.mock_gen.revokeRole.return_value = "REVOKE role_leitura FROM alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.revokeRole("alice", "role_leitura")
        self.mock_gen.revokeRole.assert_called_once_with("alice", "role_leitura")

    def test_revokeRole_raises_on_failure(self):
        self.mock_gen.revokeRole.return_value = "REVOKE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.revokeRole("alice", "role_leitura")
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 13. disassociateComplexFromComplex  (abstractDb)
# ===========================================================================


class TestDisassociateComplex(PostgisDbTestBase):
    def test_executes_sql_successfully(self):
        self.mock_gen.disassociateComplexFromComplex.return_value = "UPDATE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.disassociateComplexFromComplex(
            "complexos.estrutura_a", "id_estrutura", "uuid-123"
        )
        self.mock_gen.disassociateComplexFromComplex.assert_called_once()

    def test_raises_on_exec_failure(self):
        self.mock_gen.disassociateComplexFromComplex.return_value = "UPDATE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.disassociateComplexFromComplex(
                "complexos.estrutura_a", "id_estrutura", "uuid-123"
            )
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 14. obtainLinkColumn  (abstractDb)
# ===========================================================================


class TestObtainLinkColumn(PostgisDbTestBase):
    def test_returns_column_name(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("id_estrutura_a",)], is_active=True
        )

        result = self.postgis_db.obtainLinkColumn(
            "complexos.estrutura_a", "cb.infra_elemento_p"
        )
        self.assertEqual(result, "id_estrutura_a")

    def test_raises_on_inactive_query(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.obtainLinkColumn(
                "complexos.estrutura_a", "cb.infra_elemento_p"
            )
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_returns_empty_string_when_no_rows(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=True)

        result = self.postgis_db.obtainLinkColumn(
            "complexos.estrutura_a", "cb.infra_elemento_p"
        )
        self.assertEqual(result, "")


# ===========================================================================
# 15. isComplexClass  (abstractDb)
# ===========================================================================


class TestIsComplexClass(PostgisDbTestBase):
    def test_returns_true_when_class_found(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("estrutura_a",), ("complexo_portuario_a",)], is_active=True
        )

        result = self.postgis_db.isComplexClass("estrutura_a")
        self.assertTrue(result)

    def test_returns_false_when_class_not_found(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("estrutura_a",)], is_active=True
        )

        result = self.postgis_db.isComplexClass("inexistente_a")
        self.assertFalse(result)

    def test_raises_on_inactive_query(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.isComplexClass("estrutura_a")
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 16. getQmlRecordDict  (abstractDb)
# ===========================================================================


class TestGetQmlRecordDict(PostgisDbTestBase):
    def test_returns_dict_for_list_input(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("camada_a", "<qml_content_a/>"), ("camada_l", "<qml_content_l/>")],
            is_active=True,
        )

        result = self.postgis_db.getQmlRecordDict(["camada_a", "camada_l"])
        self.assertIsInstance(result, dict)
        self.assertIn("camada_a", result)
        self.assertEqual(result["camada_a"], "<qml_content_a/>")

    def test_returns_single_value_for_str_input(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("camada_a", "<qml_single/>")], is_active=True
        )

        result = self.postgis_db.getQmlRecordDict("camada_a")
        self.assertEqual(result, "<qml_single/>")

    def test_raises_on_inactive_query(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getQmlRecordDict(["camada_a"])
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 17. checkSuperUser  (postgisDb)
# ===========================================================================


class TestCheckSuperUser(PostgisDbTestBase):
    def test_returns_true_for_superuser(self):
        self.mock_gen.isSuperUser.return_value = "SELECT is_super()"
        self.postgis_db.db.userName.return_value = "postgres"

        mock_q = make_mock_query(exec_rows=[(True,)], exec_success=True)
        self.mock_cursor.return_value = mock_q

        result = self.postgis_db.checkSuperUser()
        self.assertTrue(result)

    def test_raises_on_exec_failure(self):
        self.mock_gen.isSuperUser.return_value = "SELECT is_super()"
        self.postgis_db.db.userName.return_value = "alice"
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.checkSuperUser()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 18. getDbsFromServer  (postgisDb)
# ===========================================================================


class TestGetDbsFromServer(PostgisDbTestBase):
    def test_returns_database_list(self):
        self.mock_gen.getDatabasesFromServer.return_value = "SELECT dbs()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[("postgres",), ("edgv_213_prod",), ("edgv_3_homol",)], is_active=True
        )

        result = self.postgis_db.getDbsFromServer()
        self.assertEqual(result, ["postgres", "edgv_213_prod", "edgv_3_homol"])

    def test_raises_on_inactive_query(self):
        self.mock_gen.getDatabasesFromServer.return_value = "SELECT dbs()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getDbsFromServer()
        self.assertIn("Mock DB error", str(ctx.exception))


# ===========================================================================
# 19. getInvalidGeomRecords  (postgisDb)
# ===========================================================================


class TestGetInvalidGeomRecords(PostgisDbTestBase):
    def test_returns_list_of_tuples(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"
        self.mock_cursor.return_value = make_mock_query(
            rows=[
                (1, "Self-intersection", "0101..."),
                (2, "Ring not closed", "0101..."),
            ],
            is_active=True,
        )

        result = self.postgis_db.getInvalidGeomRecords(
            "cb.infra_elemento_p", "geom", "id"
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (1, "Self-intersection", "0101..."))

    def test_raises_on_inactive_query(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=False)

        with self.assertRaises(Exception) as ctx:
            self.postgis_db.getInvalidGeomRecords("cb.infra_elemento_p", "geom", "id")
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_returns_empty_list_when_no_invalid_geoms(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=True)

        result = self.postgis_db.getInvalidGeomRecords(
            "cb.infra_elemento_p", "geom", "id"
        )
        self.assertEqual(result, [])


# ===========================================================================
# 20. removeFeatures com transação  (postgisDb)
# ===========================================================================


class TestRemoveFeatures(PostgisDbTestBase):
    def test_commits_on_success(self):
        self.mock_gen.deleteFeatures.return_value = "DELETE FROM t WHERE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        processList = [{"id": 1}, {"id": 2}]
        count = self.postgis_db.removeFeatures(
            "cb.infra_via_l", processList, "id", useTransaction=True
        )

        self.assertEqual(count, 2)
        self.postgis_db.db.transaction.assert_called_once()
        self.postgis_db.db.commit.assert_called_once()
        self.postgis_db.db.rollback.assert_not_called()

    def test_rollback_and_raises_on_failure(self):
        self.mock_gen.deleteFeatures.return_value = "DELETE FROM t WHERE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=False)

        processList = [{"id": 1}]
        with self.assertRaises(Exception) as ctx:
            self.postgis_db.removeFeatures(
                "cb.infra_via_l", processList, "id", useTransaction=True
            )

        # a transação é conferida antes da mensagem, para que uma falha na
        # mensagem não esconda o estado do rollback
        self.postgis_db.db.rollback.assert_called_once()
        self.postgis_db.db.commit.assert_not_called()
        self.assertIn("Mock DB error", str(ctx.exception))

    def test_no_transaction_when_flag_false(self):
        self.mock_gen.deleteFeatures.return_value = "DELETE FROM t WHERE ..."
        self.mock_cursor.return_value = make_mock_query(exec_success=True)

        self.postgis_db.removeFeatures(
            "cb.infra_via_l", [{"id": 1}], "id", useTransaction=False
        )
        self.postgis_db.db.transaction.assert_not_called()
        self.postgis_db.db.commit.assert_not_called()


# ===========================================================================
# 21. getLayersWithElementsV2  (abstractDb)
# ===========================================================================


class TestGetLayersWithElementsV2(PostgisDbTestBase):
    def test_returns_layers_with_elements(self):
        self.mock_gen.getElementCountFromLayerV2.return_value = "SELECT count()"

        call_count = [0]

        def query_factory(*args, **kwargs):
            call_count[0] += 1
            # camada_a → 5 elementos; camada_l → 0 elementos
            if call_count[0] % 2 == 1:
                return make_mock_query(rows=[(5,)], is_active=True)
            else:
                return make_mock_query(rows=[(0,)], is_active=True)

        self.mock_cursor.side_effect = query_factory

        result = self.postgis_db.getLayersWithElementsV2(["cb.camada_a", "cb.camada_l"])
        # Somente camada_a (count > 0) deve aparecer
        self.assertIn("camada_a", result)
        self.assertNotIn("camada_l", result)

    def test_skips_layer_when_query_returns_no_rows(self):
        """
        Quando next() retorna False (sem linhas), a camada deve ser ignorada
        silenciosamente (sem exception), conforme lógica original.
        """
        self.mock_gen.getElementCountFromLayerV2.return_value = "SELECT count()"
        self.mock_cursor.return_value = make_mock_query(rows=[], is_active=True)

        result = self.postgis_db.getLayersWithElementsV2(["cb.camada_a"])
        self.assertEqual(result, [])


# ===========================================================================
# Ponto de entrada
# ===========================================================================

if __name__ == "__main__":
    unittest.main()
