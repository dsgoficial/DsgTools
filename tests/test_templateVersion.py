# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-11-14
        git sha              : $Format:%H$
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

Tests of the rule that decides when an installed EDGV template is rebuilt
(issue #857). The module under test is pure Python and is loaded by path, so
this file runs with a plain `python -m unittest`, without QGIS.
"""

import glob
import importlib.util
import os
import unittest

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DsgTools")
_spec = importlib.util.spec_from_file_location(
    "templateVersion", os.path.join(_ROOT, "core", "Utils", "templateVersion.py")
)
templateVersion = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(templateVersion)

isTemplateOutdated = templateVersion.isTemplateOutdated
parseMetadataFromSql = templateVersion.parseMetadataFromSql


class TemplateVersionTest(unittest.TestCase):
    def test_issue_857_old_lineage_is_rebuilt(self):
        # '4' is not smaller than '1.1.6': the old rule kept this template
        self.assertFalse("4" < "1.1.6")
        self.assertTrue(isTemplateOutdated("3.0", "4", "EDGV 3.0", "1.1.6"))

    def test_same_template_is_kept(self):
        self.assertFalse(isTemplateOutdated("EDGV 3.0", "1.1.6", "EDGV 3.0", "1.1.6"))

    def test_older_implementation_is_rebuilt(self):
        self.assertTrue(isTemplateOutdated("EDGV 3.0", "1.1.3", "EDGV 3.0", "1.1.6"))

    def test_newer_template_is_kept(self):
        # a newer plugin already updated the server: an older one must not undo it
        self.assertFalse(isTemplateOutdated("EDGV 3.0", "1.1.7", "EDGV 3.0", "1.1.6"))

    def test_versions_compare_as_numbers_not_text(self):
        self.assertTrue("1.4.10" < "1.4.4")  # what a text comparison answers
        self.assertTrue(
            isTemplateOutdated("EDGV 3.0 Topo", "1.4.4", "EDGV 3.0 Topo", "1.4.10")
        )
        self.assertFalse(
            isTemplateOutdated("EDGV 3.0 Topo", "1.4.10", "EDGV 3.0 Topo", "1.4.4")
        )

    def test_missing_parts_count_as_zero(self):
        self.assertFalse(isTemplateOutdated("EDGV 3.0", "1.1", "EDGV 3.0", "1.1.0"))
        self.assertFalse(isTemplateOutdated("2.1.3", "3.00", "2.1.3", "3.0"))
        self.assertTrue(isTemplateOutdated("EDGV 3.0", "1.1", "EDGV 3.0", "1.1.6"))

    def test_non_numeric_version_falls_back_to_difference(self):
        self.assertTrue(isTemplateOutdated("X", "beta", "X", "1.0"))
        self.assertFalse(isTemplateOutdated("X", "beta", "X", "beta"))

    def test_file_without_metadata_never_drops_the_template(self):
        self.assertFalse(isTemplateOutdated("3.0", "4", None, None))

    def test_parse_metadata(self):
        sql = (
            "CREATE TABLE public.db_metadata(x int)#\n"
            "INSERT INTO public.db_metadata (edgvversion, dbimplversion) "
            "VALUES ('EDGV 3.0','1.1.6')#\n"
        )
        self.assertEqual(parseMetadataFromSql(sql), ("EDGV 3.0", "1.1.6"))
        self.assertEqual(parseMetadataFromSql("CREATE SCHEMA edgv#"), (None, None))

    def test_every_shipped_creation_sql_declares_its_version(self):
        pattern = os.path.join(_ROOT, "core", "DbModels", "PostGIS", "*", "edgv*.sql")
        sqlFiles = glob.glob(pattern)
        self.assertTrue(sqlFiles)
        for path in sqlFiles:
            with open(path, encoding="utf-8") as sqlFile:
                edgvVersion, implVersion = parseMetadataFromSql(sqlFile.read())
            self.assertTrue(edgvVersion, path)
            self.assertIsNotNone(
                templateVersion.parseImplementationVersion(implVersion), path
            )


if __name__ == "__main__":
    unittest.main()
