# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2020-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor, QPalette
from qgis.PyQt.QtWidgets import QDockWidget, QPushButton

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonSetupWidget import ButtonSetupWidget
from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None, profiles=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param profiles: (list-of-dict) a list of states for CustomButtonSetup
                         objects to be set to the GUI.
        """
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self._setups = dict()
        if profiles:
            self.setButtonProfiles(profiles)

    def setButtonProfiles(self, profiles):
        """
        Replaces/defines current setup associated to this GUI.
        :param profiles: (list-of-dict) a list of states for CustomButtonSetup
                         objects to be set to the GUI.
        """
        self.setupComboBox.clear()
        self.setupComboBox.addItem(self.tr("Select a button profile..."))
        for s in self._setup:
            del self._setups[s]
        for p in profiles:
            s = CustomButtonSetup()
            s.setState(p)
            self._setups[s.name()] = s
        self.setupComboBox.addItems(self.buttonProfiles("asc"))

    def buttonProfiles(self, order=None):
        """
        Retrieves current available button profiles (setups) names. 
        :return: (list-of-str) available profiles names.
        """
        return {
            "asc": lambda: sorted(self._setups.keys()),
            "desc": lambda: sorted(self._setups.keys(), reverse=True),
            None: lambda: list(self._setup.keys())
        }[order]()

    def buttonProfile(self, profile):
        """
        Retrieves a button profile object from its name. 
        :param profile: (str) profile to be retrieved.
        :return: (CustomButtonSetup) requested profile.
        """
        return self._setups[profile] if profile in self._setups else None

    def currentButtonProfileName(self):
        """
        Retrieves current active button profile name.
        :return: (str) current profile's name.
        """
        if self.setupComboBox.currentIndex() == 0:
            return ""
        return self.setupComboBox.currentText()

    def currentButtonProfile(self):
        """
        Retrieves current active button profile.
        :return: (CustomButtonSetup) requested profile.
        """
        return self.buttonProfile(self.currentButtonProfileName())

    def clearTabs(self):
        """
        Clears all tabs created for the buttons.
        """
        pass

    def createTabs(self):
        """
        Creates and populates all tabs for current button profile.
        """
        pass

    def createResearchTab(self):
        """
        Creates a tab for researched buttons.
        """
        pass

    @pyqtSlot(int, name="on_setupComboBox_currentIndexChanged")
    def setCurrentButtonProfile(self, profile=None):
        """
        Sets GUI to a new profile.
        """
        if isinstance(profile, str) and profile in self.buttonProfiles():
            self.setupComboBox.setCurrentText(self.currentButtonProfileName())
        self.clearTabs()
        if self.currentButtonProfile() is None:
            # raise a message and do nothing
            return
        self.createTabs()
        # test later if remove research tab is necessary - but it should, at
        # least be cleared

    @pyqtSlot(bool, name="on_editSetupPushButton_clicked")
    def setupCurrentButton(self):
        """
        Opens setup form.
        """
        dlg = ButtonSetupWidget()
        ret = dlg.exec_()
        if ret:
            pass
