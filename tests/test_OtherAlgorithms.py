# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-07-04
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

"""
Script designed to test each validation algorithm from DSGTools 4.X.
It is supposed to be run through QGIS with DSGTools installed.
* This is merely a prototype for our unit test suite. *
"""

import os
import sys
import warnings
import yaml
import shutil
from osgeo import ogr

import processing
from qgis.utils import iface
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProcessingFeedback,\
                      QgsProcessingContext, QgsLayerTreeLayer, QgsProject
from qgis.PyQt.QtSql import QSqlDatabase

from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from qgis.testing import unittest

from DsgTools.tests.algorithmsTestBase import AlgorithmsTest, GenericAlgorithmsTest

class Tester(GenericAlgorithmsTest, AlgorithmsTest):

    @classmethod
    def setUpClass(cls):
        start_app()
        cls.cleanup_paths = []

    @classmethod
    def tearDownClass(cls):
        for path in cls.cleanup_paths:
            shutil.rmtree(path)

    def get_definition_file(self):
        return 'otherAlgorithms.yaml'

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = 'test_' if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Tester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
