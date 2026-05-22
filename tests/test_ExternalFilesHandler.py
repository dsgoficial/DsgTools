# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-19
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import sys
import os

import pytest
from qgis.testing import unittest

pytestmark = pytest.mark.skip(
    reason="Legacy test from qgis_testrunner era; class was renamed to ExternalFileHandlerConfig/ExternalFileDownloadProcessor"
)

from DsgTools.core.NetworkTools.ExternalFilesHandler import (
    ExternalFileHandlerConfig,
    ExternalFileDownloadProcessor,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.spellChecker.datasets.ptBR import (
    WordDatasetPtBRFileConfig as WordDatasetPtBRFileHandler,
    PalavrasFileConfig as PalavrasFileHandler,
)


class ExternalFilesHandlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handlerList = [
            WordDatasetPtBRFileHandler(
                output_folder=os.path.abspath(os.path.dirname(__file__))
            ),
            PalavrasFileHandler(
                output_folder=os.path.abspath(os.path.dirname(__file__))
            ),
        ]

    @classmethod
    def tearDownClass(cls):
        for handler in cls.handlerList:
            os.unlink(handler.getFullPath())

    def test_downloadfilesalgorithm(self):
        filesHandler = ExternalFilesHandler()
        output = filesHandler.downloadFilesAlgorithm(self.handlerList)
        self.assertTrue(output)
        for handler in self.handlerList:
            self.assertTrue(os.path.exists(handler.getFullPath()))


def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ExternalFilesHandlerTest, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
