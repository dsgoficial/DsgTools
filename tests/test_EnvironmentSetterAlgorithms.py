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
import processing
from qgis.PyQt.QtCore import QSettings
from qgis.testing import unittest
from qgis.core import QgsProcessingFeedback, QgsProcessingContext

class EnvironmentSetterAlgorithmsTest(unittest.TestCase):

    def test_setfreehandtoolparametersalgorithm(self):
        parameters = {
                'FREE_HAND_TOLERANCE' : 10,
                'FREE_HAND_SMOOTH_ITERATIONS' : 20,
                'FREE_HAND_SMOOTH_OFFSET' : 30,
                'ALG_ITERATIONS' : 40,
                'UNDO_POINTS' : 50,
                'FREE_HAND_FINAL_SIMPLIFY_TOLERANCE' : 60
            }
        QSETTINGS_DICT = {
            'FREE_HAND_TOLERANCE' : 'freeHandTolerance',
            'FREE_HAND_SMOOTH_ITERATIONS' : 'freeHandSmoothIterations',
            'FREE_HAND_SMOOTH_OFFSET' : 'freeHandSmoothOffset',
            'ALG_ITERATIONS' : 'algIterations',
            'UNDO_POINTS' : 'undoPoints',
            'FREE_HAND_FINAL_SIMPLIFY_TOLERANCE' : 'freeHandFinalSimplifyTolerance'
        }
        processing.run(
            'dsgtools:setfreehandtoolparametersalgorithm',
            parameters,
            context = QgsProcessingContext(),
            feedback = QgsProcessingFeedback()
        )
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        for key, value in parameters.items():
            storedValue = settings.value(QSETTINGS_DICT[key])
            self.assertEqual(storedValue, value)

def run_all():
    """Default function that is called by the runner if nothing else is specified"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(EnvironmentSetterAlgorithmsTest, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)