# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-01-08
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

import sys
from qgis.testing import unittest

from DsgTools.core.DSGToolsProcessingAlgs.Models.dsgToolsProcessingModel import DsgToolsProcessingModel

class ModelTester(unittest.TestCase):

    def test_constructor(self):
        """Runs class constructor checks."""
        # name and set of parameters are mandatory, even if they're invalid
        self.assertRaises(Exception, DsgToolsProcessingModel)
        self.assertRaises(Exception, DsgToolsProcessingModel, parameters={})
        self.assertRaises(Exception, DsgToolsProcessingModel, name="")
        model = DsgToolsProcessingModel({}, "Invalid model")
        self.assertFalse(model.isValid())
        self.assertEquals(model.name(), "Invalid model")

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = 'test_' if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ModelTester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)