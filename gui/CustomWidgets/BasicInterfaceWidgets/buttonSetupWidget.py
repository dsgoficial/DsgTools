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
        self.buttonComboBox.addItem(self.tr("No button selected"))
        bEnabled = self.buttonComboBox.currentIndex() > 0
        for w in ("savePushButton", "undoPushButton", "removePushButton",
                  "buttonPropWidget"):
            getattr(self, w).setEnabled(bEnabled)

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

    def getButtonByName(self, name):
        """
        Retrieves a registered button from its name.
        :param name: (str) name for the requested button.
        """
        return self.setup.button(name)

    def setButtonName(self, name):
        """
        Sets button name to GUI.
        :param name: (str) name to be set to GUI.
        """
        self.buttonPropWidget.setButtonName(name)

    def buttonName(self):
        """
        Reads button name from GUI.
        :return: (str) button name read from GUI.
        """
        return self.buttonPropWidget.buttonName()

    def registeredButtonNames(self):
        """
        All names for registered buttons on current profile.
        :return: (list-of-str) list of button names.
        """
        return self.setup.buttonNames()

    def setAcquisitionTool(self, tool):
        """
        Sets button's acquisition tool to GUI.
        :param tool: (str) a supported acquisition tool to be set.
        """
        self.buttonPropWidget.setAcquisitionTool(tool)

    def acquisitionTool(self):
        """
        Reads current acquisition tool from GUI.
        :return: (str) current acquisition tool.
        """
        return self.buttonPropWidget.acquisitionTool()

    def setUseColor(self, useColor):
        """
        Sets button's acquisition tool to GUI.
        :param useColor: (bool) whether button should use a custom color
                         palette.
        """
        self.buttonPropWidget.setUseColor(useColor)

    def useColor(self):
        """
        Reads whether button will have a custom color from GUI.
        :return: (bool) whether button should use a custom color
                        palette.
        """
        return self.buttonPropWidget.useColor()

    def setColor(self, color):
        """
        Sets custom color to the color widget.
        :param color: (str/tuple) color to be set.
        """
        self.buttonPropWidget.setColor(color)

    def color(self):
        """
        Reads custom color to be set to widget as read from GUI.
        :return: (tuple) color to be used.
        """
        return self.buttonPropWidget.color()

    def setUseToolTip(self, useToolTip):
        """
        Sets button's acquisition tool to GUI.
        :param useToolTip: (bool) whether button will have a tool tip assigned.
        """
        self.buttonPropWidget.setUseToolTip(useToolTip)

    def useToolTip(self):
        """
        Reads if the button will have a tool tip assigned to it from GUI.
        :return: (bool) whether the button will have a tool tip assigned.
        """
        return self.buttonPropWidget.useToolTip()

    def setToolTip(self, tooltip):
        """
        Sets a tool tip for the active button widget.
        :param tooltip: (str) tool tip to be set.
        """
        self.buttonPropWidget.setToolTip(tooltip)

    def toolTip(self):
        """
        Reads the tool tip for the button from GUI.
        :param tooltip: (str) tool tip to be used.
        """
        return self.buttonPropWidget.toolTip()

    def setUseCategory(self, useCat):
        """
        Sets button's acquisition tool to GUI.
        :param useCat: (bool) whether button will have a category assigned.
        """
        self.buttonPropWidget.setUseCategory(useCat)

    def useCategory(self):
        """
        Reads button's category/group from GUI.
        :return: (bool) whether button will have a category assigned.
        """
        return self.buttonPropWidget.useCategory()

    def setCategory(self, cat):
        """
        Assigns a group to the active button.
        :param cat: (str) category to be set.
        """
        self.buttonPropWidget.setCategory(cat)

    def category(self):
        """
        Reads the assigned category/group to the active button from GUI.
        :return: (str) category to be used.
        """
        return self.buttonPropWidget.category()

    def setUseKeywords(self, useKw):
        """
        Sets whether active button should have keywords for button searching.
        :param useKw: (bool) whether button will have keywords assigned to it.
        """
        self.buttonPropWidget.setUseKeywords(useKw)

    def useKeywords(self):
        """
        Reads whether active button should have keywords for button searching
        from GUI.
        :return: (bool) whether button will have keywords assigned to it.
        """
        return self.buttonPropWidget.useKeywords()

    def setKeywords(self, kws):
        """
        Sets button's keywords for button searching.
        :param kws: (set-of-str) set of keywords to be assigned to the button.
        """
        self.buttonPropWidget.setKeywords(kws)

    def keywords(self):
        """
        Reads button's keywords for button searching from GUI.
        :return: (set-of-str) set of keywords to be assigned to the button.
        """
        return self.buttonPropWidget.keywords()

    def setUseShortcut(self, useShortcut):
        """
        Sets whether active button should have a shortcut assigned to it.
        :param useShortcut: (bool) whether button will have a shortcut assigned.
        """
        self.buttonPropWidget.setUseShortcut(useShortcut)

    def useShortcut(self):
        """
        Reads whether active button should have a shortcut assigned to it from GUI.
        :return: (bool) whether button will have a shortcut assigned.
        """
        return self.buttonPropWidget.useShortcut()

    def setShortcurt(self, s, autoReplace):
        """
        Assigns a shortcut to trigger active button's action.
        :param s: (str) new shortcut to be set.
        :param autoReplace: (bool) whether a confirmation from the user is
                            necessary in order to replace existing shortcuts.
        """
        self.buttonPropWidget.setShortcurt(s, autoReplace)

    def shorcut(self):
        """
        Assigned shortcut read from GUI.
        :return: (str) shortcut to be used.
        """
        return self.buttonPropWidget.shorcut()

    def setOpenForm(self, openForm):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :param openForm: (bool) whether feature form should be opened.
        """
        self.buttonPropWidget.setOpenForm(openForm)

    def openForm(self):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :return: (bool) whether feature form should be opened.
        """
        return self.buttonPropWidget.openForm()

    def setAttributeMap(self, attrMap):
        """
        Sets the attribute value map for current button to GUI.
        :param attrMap: (dict) a map from each field and its value to be set. 
        """
        self.buttonPropWidget.setAttributeMap(attrMap)

    def attributeMap(self):
        """
        Reads the field map data and set it to a button attribute map format.
        :return: (dict) read attribute map. 
        """
        return self.buttonPropWidget.attributeMap()

    def setLayer(self, layer):
        """
        Sets current layer selection on GUI.
        :param layer: (str) name for the layer to be set.
        """
        self.buttonPropWidget.setLayer(layer)

    def layer(self):
        """
        Reads current layer selection from GUI.
        :return: (str) name for the selected layer.
        """
        self.buttonPropWidget.layer() 

    def currentButton(self):
        """
        Retrives button active on GUI that has a saved state (on its last saved
        state).
        :return: (CustomFeatureButton) current button.
        """
        return self.buttonPropWidget.currentButton()

    def readButton(self):
        """
        Reads current data on GUI and gets a button with those properties.
        :return: (CustomFeatureButton) current button as from GUI.
        """
        return self.buttonPropWidget.readButton()

    def buttonIsModified(self):
        """
        Checks whether current button is modified.
        :return: (bool) whether button is modified.
        """
        return self.currentButton() != self.readButton()

    def updateButton(self, buttonName, newProps):
        """
        Updates a registered button with a new set of properties.
        :param button: (str) name for the button to be updated.
        :param newProps: (dict) new set of properties.
        """
        self.setup.updateButton(buttonName, newProps)

    def confirmAction(self, msg, title=None, showNo=True):
        """
        Raises a message box that asks for user confirmation.
        :param msg: (str) message requesting for confirmation to be shown.
        :param showNo: (bool) whether No button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        self.buttonPropWidget.confirmAction(msg, title, showNo)

    @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    def setCurrentButton(self, button):
        """
        Sets button properties to the GUI.
        :param button:  (CustomFeatureButton) button to be set to the GUI.
        """
        if isinstance(button, int):
            if button == 0:
                button = CustomFeatureButton()
                button.setName("")
            else:
                button = self.getButtonByName(
                    self.buttonComboBox.itemText(button))
        if button.name() not in self.setup.buttonNames():
            # create a new one with that button?
            pass
        self.buttonComboBox.setCurrentText(button.name())
        self.buttonPropWidget.setButton(button)
        bEnabled = self.buttonComboBox.currentIndex() > 0
        for w in ("savePushButton", "undoPushButton", "removePushButton",
                  "buttonPropWidget"):
            getattr(self, w).setEnabled(bEnabled)

    def addButton(self, button=None, newButton=True):
        """
        Adds a button to the setup.
        :param button: (CustomFeatureButton) a pre-existent button to be set.
        :param newButton: (bool) indicates if added button is new to the setup.
        :return: (CustomFeatureButton) added button.
        """
        if button is not None and not newButton:
            if button in self.registeredButtons():
                msg = self.tr("Button {b} already exists. Would you like to "
                              "replace it?").format(b=button.name())
                cnf = self.confirmAction(msg,
                    self.tr("Replace existing button"))
                if not conf:
                    return self.getButtonByName(button.name())
        button = button or self.setup.newButton()
        self.buttonComboBox.addItem(button.name())
        self.setCurrentButton(button)
        return button

    @pyqtSlot(bool, name="on_savePushButton_clicked")
    def updateCurrentButton(self, props):
        """
        Current data will be stored as current button's properties.
        :param props: (dict) a map to button's properties to be updated.
        """
        if isinstance(props, bool):
            # if button pressing was the triggering event, current data will be
            # store into current button
            props = self.readButton().properties()
        # msg = self.validateData()
        msg = ""
        if msg == "":
            prevName = self.currentButton().name()
            button = self.getButtonByName(prevName)
            self.updateButton(prevName, props)
            newName = button.name()
            self.buttonPropWidget.button = button
            if prevName != newName:
                self.buttonComboBox.removeItem(
                    self.buttonComboBox.findText(prevName)
                )
                self.buttonComboBox.addItem(newName)
                self.buttonComboBox.setCurrentText(newName)

    @pyqtSlot(bool, name="on_undoPushButton_clicked")
    def undoButtonModifications(self):
        """
        Restores stored data from current button and sets it to GUI.
        """
        self.buttonPropWidget.setButton(self.currentButton())

    @pyqtSlot(bool, name="on_removePushButton_clicked")
    def removeButton(self):
        """
        Removes the current button from setup.
        """
        name = self.buttonName()
        txt = self.tr("Confirm button '{b}' removeal?").format(name)
        if name == "":
            # ignore the "Select a button..."
            return
        self.setup().removeButton(name)
        self.buttonComboBox.removeItem(self.buttonComboBox.findText(name))
