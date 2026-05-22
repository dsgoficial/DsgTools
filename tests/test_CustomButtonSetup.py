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
import pytest
from qgis.testing import unittest

try:
    from DsgTools.gui.ProductionTools.Toolboxes.CustomFeatureToolBox.customButtonSetup import (
        CustomButtonSetup,
        CustomFeatureButton,
    )
except ImportError:
    pytest.skip(
        "customButtonSetup module not found — class was removed during QGIS 4 migration",
        allow_module_level=True,
    )


class ButtonTester(unittest.TestCase):
    def test_constructorNoArgs(self):
        """Runs class constructor checks when no args are provided."""
        b = CustomFeatureButton()
        self.assertEqual(b.name(), "New button")
        self.assertFalse(b.openForm())
        self.assertTrue(b.useColor())
        self.assertEqual(b.color(), (255, 255, 255, 255))
        self.assertEqual(b.toolTip(), "")
        self.assertEqual(b.category(), "")
        self.assertEqual(b.shortcut(), "")
        self.assertEqual(b.layer(), "")
        self.assertEqual(b.keywords(), set())
        self.assertEqual(b.attributeMap(), dict())
        self.assertEqual(b.digitizingTool(), "default")
        self.assertEqual(b.isCheckable(), False)
        self.assertEqual(b.isChecked(), False)
        self.assertEqual(b.isEnabled(), False)
        from qgis.PyQt.QtWidgets import QPushButton

        p = {
            "name": "New button",
            "openForm": False,
            "useColor": True,
            "color": (255, 255, 255, 255),
            "toolTip": "",
            "size": QPushButton().font().pointSize(),
            "category": "",
            "layer": "",
            "shortcut": "",
            "keywords": set(),
            "attributeMap": dict(),
            "digitizingTool": "default",
            "isCheckable": False,
            "isChecked": False,
            "isEnabled": False,
        }
        self.assertEqual(b.properties(), p)

    def test_supportedTools(self):
        """Tests if supported tools are correctly set"""
        b = CustomFeatureButton()
        # tests are run in a QGIS instance in English
        tools = {
            "default": "QGIS default feature extraction tool",
            "freeHandAcquisiton": "DSGTools: Free Hand Acquisition",
            "circle2points": "QGIS Circle extraction tool",
            "acquisition": "DSGTools: Right Degree Angle Digitizing",
        }
        self.assertEqual(b.supportedTools(), tools)

    def test_setDigitizingTool(self):
        """Tests digitizing tool setting method"""
        b = CustomFeatureButton()
        with self.assertRaises(TypeError):
            b.setDigitizingTool(1)
        with self.assertRaises(ValueError):
            b.setDigitizingTool("qgis")
        for tool in b.supportedTools():
            b.setDigitizingTool(tool)
            self.assertEqual(b.digitizingTool(), tool)

    def test_newWidget(self):
        """Tests if a new widget is correctly created and managed"""
        b = CustomFeatureButton({"size": 150})
        pb = b.newWidget()
        self.assertEqual(b.size(), 150)
        self.assertEqual(pb.font().pointSize(), 150)
        b.setSize(100)
        # asserts whether "old" widgets are updated.
        self.assertEqual(pb.font().pointSize(), 100)


class SetupTester(unittest.TestCase):
    def test_emptyConstructor(self):
        """Runs class constructor with no args passed to it"""
        s = CustomButtonSetup()
        self.assertEqual(s.name(), "Custom Button Setup")
        self.assertEqual(s.description(), "")
        self.assertFalse(s.dynamicShortcut())
        self.assertEqual(s.buttons(), list())

    def test_constructor(self):
        """Runs class constructor with all args"""
        b1 = CustomFeatureButton({"name": "Button 1", "category": "Cat 1"})
        b2 = CustomFeatureButton({"name": "Button 2", "isCheckable": True})
        b3 = CustomFeatureButton({"name": "Button 3", "color": (10, 2, 45, 5)})
        s = CustomButtonSetup(
            buttonsProps=[b.properties() for b in (b1, b2, b3)],
            displayName="My setup",
            description="...",
        )
        self.assertEqual(s.name(), "My setup")
        self.assertEqual(s.description(), "...")
        self.assertFalse(s.dynamicShortcut())
        self.assertEqual(s.buttonNames(), [b.name() for b in (b1, b2, b3)])

    def test_newButton(self):
        """Tests whether asking for a new button is working and manages name collision"""
        s = CustomButtonSetup()
        b = s.newButton()
        # make sure buttons are passed as reference
        self.assertEqual(s.buttons()[0], b)
        self.assertEqual(b.name(), "New button")
        # make sure new button's names are managed
        s.newButton()
        self.assertTrue(s.button("New button 1") is not None)

    def test_addButton(self):
        """Tests if adding a button from an existing one works"""
        b = CustomFeatureButton({"name": "My button", "toolTip": "..."})
        s = CustomButtonSetup()
        s.addButton(b.properties())
        newB = s.button("My button")
        self.assertTrue(newB is not None)
        self.assertEqual(newB.toolTip(), "...")

    def test_removeButton(self):
        """Tests if removing a button works, whether it actually exists or not"""
        b = CustomFeatureButton({"name": "My button"})
        s = CustomButtonSetup()
        s.addButton(b.properties())
        self.assertTrue(s.removeButton("My button"))
        newB = s.button("My button")
        self.assertTrue(newB is None)
        self.assertFalse(s.removeButton("adsad"))

    def test_groupButtons(self):
        """Tests if grouping buttons work"""
        from collections import defaultdict

        b1 = CustomFeatureButton({"name": "Button 1", "category": "Cat 1"})
        b2 = CustomFeatureButton({"name": "Button 2", "isCheckable": True})
        b3 = CustomFeatureButton({"name": "Button 3", "color": (10, 2, 45, 5)})
        s = CustomButtonSetup(buttonsProps=[b.properties() for b in (b1, b2, b3)])
        groups = defaultdict(set)
        for b in s.buttons():
            if b.name() == b1.name():
                groups["Cat 1"].add(b)
            else:
                groups[""].add(b)
        self.assertEqual(s.groupButtons(), groups)

    def test_setSize(self):
        """Tests if size modifications applies to all buttons"""
        b1 = CustomFeatureButton({"size": 5})
        b2 = CustomFeatureButton({"size": 5})
        b3 = CustomFeatureButton({"size": 5})
        s = CustomButtonSetup(buttonsProps=[b.properties() for b in (b1, b2, b3)])
        for b in s.buttons():
            self.assertEqual(b.size(), 5)
        s.setButtonsSize(10)
        for b in s.buttons():
            self.assertEqual(b.size(), 10)

    def test_checkKeyword(self):
        """Tests if matching buttons to keywords works"""
        b1 = CustomFeatureButton({"name": "B1", "keywords": set(["test"])})
        b2 = CustomFeatureButton({"name": "B2", "keywords": set(["test"])})
        b3 = CustomFeatureButton({"name": "B3"})
        s = CustomButtonSetup(buttonsProps=[b.properties() for b in (b1, b2, b3)])
        self.assertEqual(s.checkKeyword("test"), [b1, b2])

    def test_toggleButton(self):
        """Tests if only one button is toggled at once in a setup"""
        s = CustomButtonSetup()
        for i in range(3):
            s.newButton()
        s.setButtonsCheckable(True)
        s.toggleButton(s.button("New button 2"), True)
        self.assertEqual(
            {b.name(): b.isChecked() for b in s.buttons()},
            {"New button": False, "New button 1": False, "New button 2": True},
        )
        s.toggleButton(s.button("New button"), True)
        self.assertEqual(
            {b.name(): b.isChecked() for b in s.buttons()},
            {"New button": True, "New button 1": False, "New button 2": False},
        )
        s.toggleButton(s.button("New button 1"), True)
        self.assertEqual(
            {b.name(): b.isChecked() for b in s.buttons()},
            {"New button": False, "New button 1": True, "New button 2": False},
        )


def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ButtonTester, filterString))
    suite.addTests(unittest.makeSuite(SetupTester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
