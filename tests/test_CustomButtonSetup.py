# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-02-07
        git sha              : $Format:%H$
        copyright            : (C) 2020 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import (CustomButtonSetup,
                                                                                   CustomFeatureButton)

class ButtonTester(unittest.TestCase):

    def test_constructorNoArgs(self):
        """Runs class constructor checks when no args are provided."""
        b = CustomFeatureButton()
        self.assertEquals(b.name(), "New button")
        self.assertFalse(b.openForm())
        self.assertTrue(b.useColor())
        self.assertEquals(b.color(), "#ffffff")
        self.assertEquals(b.toolTip(), "")
        self.assertEquals(b.category(), "")
        self.assertEquals(b.shortcut(), "")
        self.assertEquals(b.layer(), "")
        self.assertEquals(b.keywords(), set())
        self.assertEquals(b.attributeMap(), dict())
        self.assertEquals(b.acquisitionTool(), "default")
        p = {
            "name": "New button",
            "openForm": False,
            "useColor": True,
            "color": "#ffffff",
            "tooltip": "",
            "category": "",
            "layer": "",
            "shortcut": "",
            "keywords": set(),
            "attributeMap": dict(),
            "acquisitionTool": "default"
        }
        self.assertEquals(b.properties(), p)

    def test_supportedTools(self):
        """Tests if supported tools are correctly set"""
        b = CustomFeatureButton()
        tools = {
            "default": "QGIS default feature extraction tool",
            "freeHand": "DSGTools: Free Hand",
            "circle": "QGIS Circle extraction tool",
            "rightAngle": "DSGTools: Right Degree Angle Digitizing"
        }
        self.assertEquals(b.supportedTools(), tools)

    def test_setAcquisitionTool(self):
        """Tests acquisition tool setting method"""
        b = CustomFeatureButton()
        with self.assertRaises(TypeError):
            b.setAcquisitionTool(1)
        with self.assertRaises(ValueError):
            b.setAcquisitionTool("qgis")
        self.assertEquals(b.acquisitionTool(), "default")
        for tool in b.supportedTools():
            b.setAcquisitionTool(tool)
        self.assertEquals(b.acquisitionTool(), tool)

class SetupTester(unittest.TestCase):

    def test_constructor(self):
        """Runs class constructor checks."""
        s = CustomButtonSetup()

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = 'test_' if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ButtonTester, filterString))
    suite.addTests(unittest.makeSuite(SetupTester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)