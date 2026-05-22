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
não introduza quebras de comportamento.

Estratégia de mock (pós-refactor)
----------------------------------
PostgisDb.__init__ usa PsycopgDbAdapter (não QSqlDatabase).
Todos os métodos que antes usavam QSqlQuery agora usam _fetch_all,
_fetch_one ou _execute.

- patch("...postgisDb.PsycopgDbAdapter") → self.postgis_db.db = MagicMock
- patch.object(self.postgis_db, '_fetch_all'/'_fetch_one'/'_execute')
"""

import unittest
from unittest.mock import MagicMock, patch, call

from qgis.testing import start_app

start_app()

from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb


# ---------------------------------------------------------------------------
# Classe base de teste
# ---------------------------------------------------------------------------


class PostgisDbTestBase(unittest.TestCase):
    """
    Configura um PostgisDb com todas as dependências de banco mockadas.

    PostgisDb.__init__ cria self.db = PsycopgDbAdapter(), então patchamos
    PsycopgDbAdapter para que self.postgis_db.db seja um MagicMock.
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

        self.mock_db_instance = MagicMock()
        self.mock_db_instance.isOpen.return_value = True
        self.mock_db_instance.open.return_value = True
        self.mock_db_class.return_value = self.mock_db_instance

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
# 2. getDatabaseVersion  (usa _fetch_all)
# ===========================================================================


class TestGetDatabaseVersion(PostgisDbTestBase):
    def test_returns_version_string(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        with patch.object(self.postgis_db, "_fetch_all", return_value=[("3.0",)]):
            result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "3.0")

    def test_returns_non_edgv_when_fetch_raises(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "Non_EDGV")

    def test_returns_minus_one_when_no_rows(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        with patch.object(self.postgis_db, "_fetch_all", return_value=[]):
            result = self.postgis_db.getDatabaseVersion()
        self.assertEqual(result, "-1")


# ===========================================================================
# 3. findEPSG  (usa _fetch_one)
# ===========================================================================


class TestFindEPSG(PostgisDbTestBase):
    def test_returns_srid(self):
        self.mock_gen.getSrid.return_value = "SELECT srid()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=(4674,)):
            result = self.postgis_db.findEPSG()
        self.assertEqual(result, 4674)

    def test_returns_minus_one_when_no_rows(self):
        self.mock_gen.getSrid.return_value = "SELECT srid()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=None):
            result = self.postgis_db.findEPSG()
        self.assertEqual(result, -1)


# ===========================================================================
# 4. implementationVersion / getImplementationVersion  (usa _fetch_one)
# ===========================================================================


class TestImplementationVersion(PostgisDbTestBase):
    def test_returns_version(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=("5.0",)):
            result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "5.0")

    def test_returns_empty_string_when_fetch_raises(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        with patch.object(
            self.postgis_db, "_fetch_one", side_effect=Exception("db error")
        ):
            result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "")

    def test_returns_empty_string_when_value_is_none(self):
        self.mock_gen.implementationVersion.return_value = "SELECT impl()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=(None,)):
            result = self.postgis_db.implementationVersion()
        self.assertEqual(result, "")

    def test_getImplementationVersion_returns_version(self):
        self.mock_gen.getImplementationVersion.return_value = "SELECT implv()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=("5.1",)):
            result = self.postgis_db.getImplementationVersion()
        self.assertEqual(result, "5.1")

    def test_getImplementationVersion_raises_when_row_is_none(self):
        self.mock_gen.getImplementationVersion.return_value = "SELECT implv()"
        with patch.object(self.postgis_db, "_fetch_one", return_value=None):
            with self.assertRaises(Exception) as ctx:
                self.postgis_db.getImplementationVersion()
        self.assertIn("Problem getting implementation version", str(ctx.exception))


# ===========================================================================
# 5. getStructureDict  (usa _fetch_all)
# ===========================================================================


class TestGetStructureDict(PostgisDbTestBase):
    def test_returns_populated_dict(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_gen.getStructure.return_value = "SELECT struct()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            side_effect=[
                [("3.0",)],  # getDatabaseVersion
                [
                    ("cb", "infra_via_deslocamento_l", "id"),
                    ("cb", "infra_via_deslocamento_l", "geom"),
                ],  # getStructure
            ],
        ):
            result = self.postgis_db.getStructureDict()
        self.assertIn("cb.infra_via_deslocamento_l", result)

    def test_raises_on_failed_struct_fetch(self):
        self.mock_gen.getEDGVVersion.return_value = "SELECT version()"
        self.mock_gen.getStructure.return_value = "SELECT struct()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            side_effect=[
                [("3.0",)],  # getDatabaseVersion succeeds
                Exception("db error"),  # getStructure fails
            ],
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getStructureDict()


# ===========================================================================
# 6. listComplexClassesFromDatabase  (usa _fetch_all)
# ===========================================================================


class TestListComplexClassesFromDatabase(PostgisDbTestBase):
    def test_returns_only_complexos_schema(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                ("cb", "infra_via_l"),
                ("complexos", "pto_ref_geod_topo_p"),
                ("complexos", "complexo_portuario_a"),
            ],
        ):
            result = self.postgis_db.listComplexClassesFromDatabase()

        self.assertIn("complexos.pto_ref_geod_topo_p", result)
        self.assertIn("complexos.complexo_portuario_a", result)
        self.assertNotIn("cb.infra_via_l", result)

    def test_result_is_sorted(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                ("complexos", "z_ultimo"),
                ("complexos", "a_primeiro"),
            ],
        ):
            result = self.postgis_db.listComplexClassesFromDatabase()

        self.assertEqual(result, sorted(result))

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.listComplexClassesFromDatabase()


# ===========================================================================
# 7. getTablesFromDatabase  (usa _fetch_all)
# ===========================================================================


class TestGetTablesFromDatabase(PostgisDbTestBase):
    def test_returns_schema_dot_table_list(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                ("cb", "infra_via_l"),
                ("complexos", "estrutura_a"),
            ],
        ):
            result = self.postgis_db.getTablesFromDatabase()

        self.assertIn("cb.infra_via_l", result)
        self.assertIn("complexos.estrutura_a", result)

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getTablesFromDatabase.return_value = "SELECT tables()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getTablesFromDatabase()


# ===========================================================================
# 8. getUsers / getUserRelatedRoles / getRoles  (usa _fetch_all)
# ===========================================================================


class TestUserMethods(PostgisDbTestBase):
    def test_getUsers_returns_sorted_list(self):
        self.mock_gen.getUsers.return_value = "SELECT users()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("zebra",), ("alice",), ("bob",)],
        ):
            result = self.postgis_db.getUsers()

        self.assertEqual(result, ["alice", "bob", "zebra"])

    def test_getUsers_raises_on_fetch_failure(self):
        self.mock_gen.getUsers.return_value = "SELECT users()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getUsers()

    def test_getUserRelatedRoles_separates_installed_and_assigned(self):
        self.mock_gen.getUserRelatedRoles.return_value = "SELECT roles()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                ("role_leitura", None),
                ("role_edicao", None),
                ("role_admin", "alice"),
            ],
        ):
            installed, assigned = self.postgis_db.getUserRelatedRoles("alice")

        self.assertIn("role_leitura", installed)
        self.assertIn("role_edicao", installed)
        self.assertIn("role_admin", assigned)
        self.assertEqual(installed, sorted(installed))
        self.assertEqual(assigned, sorted(assigned))

    def test_getRoles_returns_sorted_list(self):
        self.mock_gen.getRoles.return_value = "SELECT roles()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("role_z",), ("role_a",)],
        ):
            result = self.postgis_db.getRoles()

        self.assertEqual(result, ["role_a", "role_z"])

    def test_getRoles_raises_on_fetch_failure(self):
        self.mock_gen.getRoles.return_value = "SELECT roles()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getRoles()


# ===========================================================================
# 9. createUser / removeUser / alterUserPass  (usa _execute)
# ===========================================================================


class TestUserDMLMethods(PostgisDbTestBase):
    def test_createUser_executes_sql(self):
        self.mock_gen.createUser.return_value = "CREATE USER alice"

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.createUser("alice", "senha123", False)

        self.mock_gen.createUser.assert_called_once_with("alice", "senha123", False)
        mock_exec.assert_called_once()

    def test_createUser_raises_on_exec_failure(self):
        self.mock_gen.createUser.return_value = "CREATE USER alice"

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.createUser("alice", "senha123", False)

    def test_removeUser_executes_sql(self):
        self.mock_gen.removeUser.return_value = "DROP USER alice"

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.removeUser("alice")

        self.mock_gen.removeUser.assert_called_once_with("alice")
        mock_exec.assert_called_once()

    def test_removeUser_raises_on_exec_failure(self):
        self.mock_gen.removeUser.return_value = "DROP USER alice"

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.removeUser("alice")

    def test_alterUserPass_executes_sql(self):
        self.mock_gen.alterUserPass.return_value = "ALTER USER alice PASSWORD 'nova'"

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.alterUserPass("alice", "nova")

        self.mock_gen.alterUserPass.assert_called_once_with("alice", "nova")
        mock_exec.assert_called_once()

    def test_alterUserPass_raises_on_failure(self):
        self.mock_gen.alterUserPass.return_value = "ALTER USER alice PASSWORD 'nova'"

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.alterUserPass("alice", "nova")


# ===========================================================================
# 10. grantRole / revokeRole  (usa _execute)
# ===========================================================================


class TestRoleDMLMethods(PostgisDbTestBase):
    def test_grantRole_executes_sql(self):
        self.mock_gen.grantRole.return_value = "GRANT role_leitura TO alice"

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.grantRole("alice", "role_leitura")

        self.mock_gen.grantRole.assert_called_once_with("alice", "role_leitura")
        mock_exec.assert_called_once()

    def test_grantRole_raises_on_failure(self):
        self.mock_gen.grantRole.return_value = "GRANT ..."

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.grantRole("alice", "role_leitura")

    def test_revokeRole_executes_sql(self):
        self.mock_gen.revokeRole.return_value = "REVOKE role_leitura FROM alice"

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.revokeRole("alice", "role_leitura")

        self.mock_gen.revokeRole.assert_called_once_with("alice", "role_leitura")
        mock_exec.assert_called_once()

    def test_revokeRole_raises_on_failure(self):
        self.mock_gen.revokeRole.return_value = "REVOKE ..."

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.revokeRole("alice", "role_leitura")


# ===========================================================================
# 11. disassociateComplexFromComplex  (usa _execute)
# ===========================================================================


class TestDisassociateComplex(PostgisDbTestBase):
    def test_executes_sql_successfully(self):
        self.mock_gen.disassociateComplexFromComplex.return_value = "UPDATE ..."

        with patch.object(self.postgis_db, "_execute") as mock_exec:
            self.postgis_db.disassociateComplexFromComplex(
                "complexos.estrutura_a", "id_estrutura", "uuid-123"
            )

        self.mock_gen.disassociateComplexFromComplex.assert_called_once()
        mock_exec.assert_called_once()

    def test_raises_on_exec_failure(self):
        self.mock_gen.disassociateComplexFromComplex.return_value = "UPDATE ..."

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.disassociateComplexFromComplex(
                    "complexos.estrutura_a", "id_estrutura", "uuid-123"
                )


# ===========================================================================
# 12. obtainLinkColumn  (usa _fetch_all)
# ===========================================================================


class TestObtainLinkColumn(PostgisDbTestBase):
    def test_returns_column_name(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("id_estrutura_a",)],
        ):
            result = self.postgis_db.obtainLinkColumn(
                "complexos.estrutura_a", "cb.infra_elemento_p"
            )

        self.assertEqual(result, "id_estrutura_a")

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.obtainLinkColumn(
                    "complexos.estrutura_a", "cb.infra_elemento_p"
                )

    def test_returns_empty_string_when_no_rows(self):
        self.mock_gen.getLinkColumn.return_value = "SELECT link_col()"

        with patch.object(self.postgis_db, "_fetch_all", return_value=[]):
            result = self.postgis_db.obtainLinkColumn(
                "complexos.estrutura_a", "cb.infra_elemento_p"
            )

        self.assertEqual(result, "")


# ===========================================================================
# 13. isComplexClass  (usa _fetch_all)
# ===========================================================================


class TestIsComplexClass(PostgisDbTestBase):
    def test_returns_true_when_class_found(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("estrutura_a",), ("complexo_portuario_a",)],
        ):
            result = self.postgis_db.isComplexClass("estrutura_a")

        self.assertTrue(result)

    def test_returns_false_when_class_not_found(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("estrutura_a",)],
        ):
            result = self.postgis_db.isComplexClass("inexistente_a")

        self.assertFalse(result)

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getComplexTablesFromDatabase.return_value = "SELECT complex()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.isComplexClass("estrutura_a")


# ===========================================================================
# 14. getQmlRecordDict  (usa _fetch_all)
# ===========================================================================


class TestGetQmlRecordDict(PostgisDbTestBase):
    def test_returns_dict_for_list_input(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                ("camada_a", "<qml_content_a/>"),
                ("camada_l", "<qml_content_l/>"),
            ],
        ):
            result = self.postgis_db.getQmlRecordDict(["camada_a", "camada_l"])

        self.assertIsInstance(result, dict)
        self.assertIn("camada_a", result)
        self.assertEqual(result["camada_a"], "<qml_content_a/>")

    def test_returns_single_value_for_str_input(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("camada_a", "<qml_single/>")],
        ):
            result = self.postgis_db.getQmlRecordDict("camada_a")

        self.assertEqual(result, "<qml_single/>")

    def test_raises_when_rows_empty(self):
        self.mock_gen.getQmlRecords.return_value = "SELECT qml()"

        with patch.object(self.postgis_db, "_fetch_all", return_value=[]):
            with self.assertRaises(Exception) as ctx:
                self.postgis_db.getQmlRecordDict(["camada_a"])

        self.assertIn("Problem getting qmlRecordDict", str(ctx.exception))


# ===========================================================================
# 15. checkSuperUser  (usa _fetch_one)
# ===========================================================================


class TestCheckSuperUser(PostgisDbTestBase):
    def test_returns_true_for_superuser(self):
        self.mock_gen.isSuperUser.return_value = "SELECT is_super()"
        self.postgis_db.db.userName.return_value = "postgres"

        with patch.object(self.postgis_db, "_fetch_one", return_value=(True,)):
            result = self.postgis_db.checkSuperUser()

        self.assertTrue(result)

    def test_raises_on_fetch_failure(self):
        self.mock_gen.isSuperUser.return_value = "SELECT is_super()"
        self.postgis_db.db.userName.return_value = "alice"

        with patch.object(
            self.postgis_db, "_fetch_one", side_effect=Exception("permission denied")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.checkSuperUser()


# ===========================================================================
# 16. getDbsFromServer  (usa _fetch_all)
# ===========================================================================


class TestGetDbsFromServer(PostgisDbTestBase):
    def test_returns_database_list(self):
        self.mock_gen.getDatabasesFromServer.return_value = "SELECT dbs()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[("postgres",), ("edgv_213_prod",), ("edgv_3_homol",)],
        ):
            result = self.postgis_db.getDbsFromServer()

        self.assertEqual(result, ["postgres", "edgv_213_prod", "edgv_3_homol"])

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getDatabasesFromServer.return_value = "SELECT dbs()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getDbsFromServer()


# ===========================================================================
# 17. getInvalidGeomRecords  (usa _fetch_all)
# ===========================================================================


class TestGetInvalidGeomRecords(PostgisDbTestBase):
    def test_returns_list_of_tuples(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"

        with patch.object(
            self.postgis_db,
            "_fetch_all",
            return_value=[
                (1, "Self-intersection", "0101..."),
                (2, "Ring not closed", "0101..."),
            ],
        ):
            result = self.postgis_db.getInvalidGeomRecords(
                "cb.infra_elemento_p", "geom", "id"
            )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (1, "Self-intersection", "0101..."))

    def test_raises_on_fetch_failure(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"

        with patch.object(
            self.postgis_db, "_fetch_all", side_effect=Exception("db error")
        ):
            with self.assertRaises(Exception):
                self.postgis_db.getInvalidGeomRecords(
                    "cb.infra_elemento_p", "geom", "id"
                )

    def test_returns_empty_list_when_no_invalid_geoms(self):
        self.mock_gen.getInvalidGeom.return_value = "SELECT invalid()"

        with patch.object(self.postgis_db, "_fetch_all", return_value=[]):
            result = self.postgis_db.getInvalidGeomRecords(
                "cb.infra_elemento_p", "geom", "id"
            )

        self.assertEqual(result, [])


# ===========================================================================
# 18. removeFeatures  (usa _execute + @transactional)
# ===========================================================================


class TestRemoveFeatures(PostgisDbTestBase):
    def test_commits_on_success(self):
        self.mock_gen.deleteFeatures.return_value = "DELETE FROM t WHERE ..."

        with patch.object(self.postgis_db, "_execute"):
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

        with patch.object(
            self.postgis_db, "_execute", side_effect=Exception("delete failed")
        ):
            processList = [{"id": 1}]
            with self.assertRaises(Exception):
                self.postgis_db.removeFeatures(
                    "cb.infra_via_l", processList, "id", useTransaction=True
                )

        self.postgis_db.db.rollback.assert_called_once()
        self.postgis_db.db.commit.assert_not_called()

    def test_no_transaction_when_flag_false(self):
        self.mock_gen.deleteFeatures.return_value = "DELETE FROM t WHERE ..."

        with patch.object(self.postgis_db, "_execute"):
            self.postgis_db.removeFeatures(
                "cb.infra_via_l", [{"id": 1}], "id", useTransaction=False
            )

        self.postgis_db.db.transaction.assert_not_called()
        self.postgis_db.db.commit.assert_not_called()


# ===========================================================================
# 19. getLayersWithElementsV2  (usa _fetch_one)
# ===========================================================================


class TestGetLayersWithElementsV2(PostgisDbTestBase):
    def test_returns_layers_with_elements(self):
        self.mock_gen.getElementCountFromLayerV2.return_value = "SELECT count()"

        with patch.object(
            self.postgis_db,
            "_fetch_one",
            side_effect=[(5,), (0,)],  # camada_a=5, camada_l=0
        ):
            result = self.postgis_db.getLayersWithElementsV2(
                ["cb.camada_a", "cb.camada_l"]
            )

        self.assertIn("camada_a", result)
        self.assertNotIn("camada_l", result)

    def test_skips_layer_when_fetch_returns_none(self):
        self.mock_gen.getElementCountFromLayerV2.return_value = "SELECT count()"

        with patch.object(self.postgis_db, "_fetch_one", return_value=None):
            result = self.postgis_db.getLayersWithElementsV2(["cb.camada_a"])

        self.assertEqual(result, [])


# ===========================================================================
# Ponto de entrada
# ===========================================================================

if __name__ == "__main__":
    unittest.main()
