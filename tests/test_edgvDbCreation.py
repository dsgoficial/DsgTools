# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-11-14
        copyright            : (C) 2026 by Brazilian Army - Geographic Service Bureau
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
Criação de banco EDGV direto do SQL embarcado, sem banco de template no
servidor (issue #857).

O template sobrevivia à versão do plugin que o criou: o servidor que guardava
um template_edgv_3 antigo seguia entregando o modelo antigo, com outra
numeração de domínios. Estes testes fixam o contrato novo:

- o banco EDGV nasce do SQL embarcado, já no SRID pedido;
- nada é marcado como template nem copiado de template;
- o modelo vai ao servidor em um único envio;
- banco que falhou na criação não fica para trás, vazio;
- a cópia de um banco existente (lote e banco escolhido pelo usuário) segue
  como estava.

Sem banco real: o adaptador e o gerador de SQL são mocks, no mesmo molde do
test_postgisDb_refactor.
"""

import glob
import os
import re
import unittest
from unittest.mock import MagicMock, patch

from qgis.testing import start_app

start_app()

from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb  # noqa: E402
from DsgTools.core.Factories.DbFactory.pgConnectionAdapter import (  # noqa: E402
    PsycopgDbAdapter,
)
from DsgTools.core.Factories.DbCreatorFactory.postgisDbCreator import (  # noqa: E402
    PostgisDbCreator,
)

MODELS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "DsgTools",
    "core",
    "DbModels",
    "PostGIS",
)
METADATA_INSERT = re.compile(
    r"INSERT INTO public\.db_metadata \(edgvversion, dbimplversion\) "
    r"VALUES \('([^']+)','([^']+)'\)"
)


class SetStructureFromSqlTest(unittest.TestCase):
    def setUp(self):
        patcherDb = patch(
            "DsgTools.core.Factories.DbFactory.postgisDb.PsycopgDbAdapter"
        )
        patcherGen = patch(
            "DsgTools.core.Factories.DbFactory.postgisDb.SqlGeneratorFactory"
        )
        dbClass = patcherDb.start()
        genFactory = patcherGen.start()
        self.addCleanup(patcherDb.stop)
        self.addCleanup(patcherGen.stop)
        self.db = MagicMock(spec=PsycopgDbAdapter)
        self.db.isOpen.return_value = True
        self.db.databaseName.return_value = "banco_novo"
        dbClass.return_value = self.db
        self.cursor = MagicMock()
        self.cursor.fetchone.return_value = (False,)  # no layer_styles yet
        self.db.cursor.return_value = self.cursor
        self.gen = MagicMock()
        self.gen.alterSearchPath.return_value = "ALTER SEARCH PATH"
        self.gen.checkStyleTable.return_value = "CHECK STYLE TABLE"
        self.gen.createStyleTable.return_value = "CREATE STYLE TABLE"
        genFactory.return_value.createSqlGenerator.return_value = self.gen
        self.postgisDb = PostgisDb()

    def executed(self):
        return [call.args[0] for call in self.cursor.execute.call_args_list]

    def test_model_goes_in_one_round_trip_at_the_requested_srid(self):
        self.postgisDb.setStructureFromSql("3.0", 31982)
        executed = self.executed()
        model = [sql for sql in executed if "CREATE SCHEMA edgv" in sql]
        self.assertEqual(len(model), 1)
        self.assertNotIn("[epsg]", model[0])
        self.assertNotIn("#", model[0])
        self.assertIn("geometry(MultiPolygon, 31982)", model[0])
        self.assertNotIn(", 4674)", model[0])
        # the whole model and nothing else but the search path and the styles
        self.assertEqual(
            executed,
            [model[0], "ALTER SEARCH PATH", "CHECK STYLE TABLE", "CREATE STYLE TABLE"],
        )

    def test_style_table_created_by_the_model_is_kept(self):
        # EDGV 2.1.3 Pro ships its own layer_styles: creating it again failed
        self.cursor.fetchone.return_value = (True,)
        self.postgisDb.setStructureFromSql("2.1.3 Pro", 4674)
        self.assertNotIn("CREATE STYLE TABLE", self.executed())

    def test_database_is_not_marked_as_template(self):
        self.postgisDb.setStructureFromSql("3.0", 4674)
        self.gen.setDbAsTemplate.assert_not_called()

    def test_failure_rolls_back_and_raises(self):
        self.cursor.execute.side_effect = Exception("permission denied")
        with self.assertRaises(Exception) as ctx:
            self.postgisDb.setStructureFromSql("3.0", 4674)
        self.assertIn("permission denied", str(ctx.exception))
        self.db.rollback.assert_called()
        self.db.commit.assert_not_called()

    def test_template_methods_are_gone(self):
        for name in (
            "checkTemplate",
            "createTemplateDatabase",
            "getTemplateName",
            "checkTemplateImplementationVersion",
            "getImplementationVersionFromFile",
        ):
            self.assertFalse(hasattr(self.postgisDb, name), name)


class PostgisDbCreatorTest(unittest.TestCase):
    def setUp(self):
        self.serverDb = MagicMock(spec=PostgisDb)
        self.serverDb.gen = MagicMock()
        self.serverDb.gen.dropDatabase.return_value = "DROP DATABASE"
        self.creator = PostgisDbCreator(self.serverDb)
        self.newDb = MagicMock(spec=PostgisDb)
        self.creator.instantiateNewDb = MagicMock(return_value=self.newDb)

    def test_edgv_database_comes_from_the_sql_not_from_a_template(self):
        result = self.creator.createDb(
            "banco_novo", "31982", {"isTemplateEdgv": True, "version": "3.0 Topo"}
        )
        self.assertIs(result, self.newDb)
        self.serverDb.createDatabase.assert_called_once_with("banco_novo")
        self.creator.instantiateNewDb.assert_called_once_with("banco_novo")
        self.newDb.setStructureFromSql.assert_called_once_with("3.0 Topo", 31982)
        self.serverDb.createDbFromTemplate.assert_not_called()
        self.newDb.updateDbSRID.assert_not_called()

    def test_failed_creation_does_not_leave_an_empty_database(self):
        self.newDb.setStructureFromSql.side_effect = Exception("boom")
        with self.assertRaises(Exception) as ctx:
            self.creator.createDb(
                "banco_novo", 4674, {"isTemplateEdgv": True, "version": "3.0"}
            )
        self.assertEqual(str(ctx.exception), "boom")
        self.newDb.closeDatabase.assert_called_once()
        self.serverDb.gen.dropDatabase.assert_called_once_with("banco_novo")
        self.serverDb._execute_autocommit.assert_called_once_with("DROP DATABASE")

    def test_srid_must_be_a_number(self):
        with self.assertRaises(ValueError):
            self.creator.createDb(
                "banco_novo",
                "4674); DROP TABLE x; --",
                {"isTemplateEdgv": True, "version": "3.0"},
            )
        self.newDb.setStructureFromSql.assert_not_called()

    def test_copy_of_a_user_database_is_unchanged(self):
        self.creator.createDb(
            "banco_novo", 31982, {"isTemplateEdgv": False, "templateName": "modelo"}
        )
        self.serverDb.createDbFromTemplate.assert_called_once_with(
            "banco_novo", templateName="modelo", parentWidget=None
        )
        self.newDb.updateDbSRID.assert_called_once_with(31982, parentWidget=None)
        self.newDb.checkAndCreateStyleTable.assert_called_once()
        self.serverDb.createDatabase.assert_not_called()

    def test_batch_copy_of_the_first_database_is_unchanged(self):
        self.creator.createDb(
            "banco_2",
            31982,
            {"isTemplateEdgv": True, "version": "3.0", "templateDb": "banco_1"},
        )
        self.serverDb.createDbFromTemplate.assert_called_once_with(
            "banco_2", templateName="banco_1", parentWidget=None
        )
        self.serverDb.createDatabase.assert_not_called()


class ShippedSqlTest(unittest.TestCase):
    def test_every_creation_sql_declares_its_version(self):
        sqlFiles = glob.glob(os.path.join(MODELS_DIR, "*", "edgv*.sql"))
        self.assertTrue(sqlFiles)
        for path in sqlFiles:
            with open(path, encoding="utf-8") as sqlFile:
                sql = sqlFile.read()
            self.assertEqual(len(METADATA_INSERT.findall(sql)), 1, path)
            # the DEFAULT of the column and the inserted row must agree
            version = METADATA_INSERT.search(sql).group(2)
            self.assertIn("DEFAULT '{0}'".format(version), sql, path)

    def test_edgv_3_sqls_have_no_fixed_srid(self):
        for model in ("3", "3_Topo", "3_Orto", "3_Pro"):
            path = glob.glob(os.path.join(MODELS_DIR, model, "edgv*.sql"))[0]
            with open(path, encoding="utf-8") as sqlFile:
                sql = sqlFile.read()
            self.assertIn("[epsg]", sql, path)
            self.assertIsNone(re.search(r"geometry\(\s*\w+\s*,\s*\d+\s*\)", sql), path)


if __name__ == "__main__":
    unittest.main()
