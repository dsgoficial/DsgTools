# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-02-10
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

import os

from qgis.core import QgsMessageLog

from qgis.PyQt import uic
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox, QRadioButton, QHeaderView

from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup, CustomFeatureButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonSetupWidget.ui'))

class ButtonSetupWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None, buttonSetup=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param buttonSetup: (CustomButtonSetup) object that handles all
                            buttons displayed and configured through this GUI.
        """
        super(ButtonSetupWidget, self).__init__(parent)
        self.setupUi(self)
        self.orderedTableWidget.setHeaders({
            0: {
                "header" : self.tr("Buttons"),
                "type" : "widget",
                "widget" : self.newButton,
                "setter" : "setProperties",
                "getter" : "properties"
            }
        })
        self.orderedTableWidget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch)
        self.textEdit.setPlaceholderText(
            self.tr("Insert a short description for current button setup..."))
        self.setup = buttonSetup or CustomButtonSetup()

    def buttonGetter(self, button):
        """
        A method to be passed to all new buttons in order to 
        """

    def newButton(self):
        """
        Generates a new button, adds it to buttons manager object and retrieve
        its widget.
        :return: (QPushButton) widget associated with a new instance of button.
        """
        b = self.addButton()
        b.widget().properties = b.properties
        b.widget().setProperties = b.setProperties
        self.setCurrentButton(b)
        return b.widget()

    def setButtonName(self, name):
        """
        Sets button name to GUI.
        :param name: (str) name to be set to GUI.
        """
        self.buttonPropWidget.setButtonName(name)

    def setAcquisitionTool(self, tool):
        """
        Sets button's acquisition tool to GUI.
        :param tool: (str) a supported acquisition tool to be set.
        """
        self.buttonPropWidget.setAcquisitionTool(tool)

    def setUseColor(self, useColor):
        """
        Sets button's acquisition tool to GUI.
        :param useColor: (bool) whether button should use a custom color
                         palette.
        """
        self.buttonPropWidget.setUseColor(useColor)

    def setColor(self, color):
        """
        Sets custom color to the color widget.
        :param color: (str/tuple) color to be set.
        """
        self.buttonPropWidget.setColor(color)

    def setUseToolTip(self, useToolTip):
        """
        Sets button's acquisition tool to GUI.
        :param useToolTip: (bool) whether button will have a tool tip assigned.
        """
        self.buttonPropWidget.setUseToolTip(useToolTip)

    def setToolTip(self, tooltip):
        """
        Sets a tool tip for the active button widget.
        :param tooltip: (str) tool tip to be set.
        """
        self.buttonPropWidget.setToolTip(tooltip)

    def setUseCategory(self, useCat):
        """
        Sets button's acquisition tool to GUI.
        :param useCat: (bool) whether button will have a category assigned.
        """
        self.buttonPropWidget.setUseCategory(useCat)

    def setCategory(self, cat):
        """
        Assigns a group to the active button.
        :param cat: (str) category to be set.
        """
        self.buttonPropWidget.setCategory(cat)

    def setUseKeywords(self, useKw):
        """
        Sets whether active button should have keywords for button searching.
        :param useKw: (bool) whether button will have keywords assigned to it.
        """
        self.buttonPropWidget.setUseKeywords(useKw)

    def setKeywords(self, kws):
        """
        Sets button's keywords for button searching.
        :param kws: (set-of-str) set of keywords to be assigned to the button.
        """
        self.buttonPropWidget.setKeywords(kws)

    def setUseShortcut(self, useShortcut):
        """
        Sets whether active button should have a shortcut assigned to it.
        :param useShortcut: (bool) whether button will have a shortcut assigned.
        """
        self.buttonPropWidget.setUseShortcut(useShortcut)

    def setShortcurt(self, s):
        """
        Assigns a shortcut to trigger active button's action.
        :param s: (str) new shortcut to be set.
        """
        self.buttonPropWidget.setShortcurt(s)

    def setOpenForm(self, openForm):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :param openForm: (bool) whether feature form should be opened.
        """
        self.buttonPropWidget.setOpenForm(openForm)

    def setAttributeMap(self, attrMap):
        """
        Sets the attribute value map for current button to GUI.
        :param attrMap: (dict) a map from each field and its value to be set. 
        """
        self.buttonPropWidget.setAttributeMap(attrMap)

    def currentButton(self):
        """
        Retrives button active on GUI that has a saved state (on its last saved
        state).
        :return: (CustomFeatureButton) current button.
        """
        return self.buttonPropWidget.currentButton()

    @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    def setCurrentButton(self, button):
        """
        Sets button properties to the GUI.
        :param button:  (CustomFeatureButton) button to be set to the GUI.
        """
        if isinstance(button, int):
            button = self.setup.button(self.buttonComboBox.itemText(button))
        if button.name() not in self.setup.buttonNames():
            # create a new one with that button?
            pass
        self.buttonComboBox.setCurrentText(button.name())
        self.buttonPropWidget.setButton(button)

    def addButton(self, button=None):
        """
        Adds a button to the setup.
        :button: (CustomFeatureButton) a pre-existent button to be set. 
        """
        if button is not None:
            if button.name() in self.setup.buttonNames():
                # raise a warning and ask if data should be replaced.
                pass
        else:
            button = self.setup.newButton()
        self.buttonComboBox.addItem(button.name())
        self.setCurrentButton(button)
        return button
