# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-08-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import os

from qgis.core import QgsMessageLog

from qgis.PyQt import uic
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox, QRadioButton

from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup, CustomFeatureButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonPropWidget.ui'))

class ButtonPropWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None, buttonSetup=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param buttonSetup: (CustomButtonSetup) object that handles all
                            buttons displayed and configured through this GUI.
        """
        super(ButtonPropWidget, self).__init__(parent)
        self.setupUi(self)
        # self._buttonSetup = buttonSetup or CustomButtonSetup()
        # self.refresh()

    # def setup(self):
    #     """
    #     Retrieves the object responsible for button management.
    #     :return: (CustomButtonSetup) button setup object.
    #     """
    #     return self._buttonSetup

    # def clear(self):
    #     """
    #     Clears all data from interface.
    #     """
    #     pass

    # def refresh(self):
    #     """
    #     Clears interface data and resets it to its default.
    #     """
    #     self.clear()
    #     self.buttonComboBox.addItem(self.tr("Select a button..."))
    #     self.buttonComboBox.addItems([
    #         b.name() for b in self.setup().buttons()
    #     ])

    # def readButton(self):
    #     """
    #     Reads data from the interface and sets it to a button object.
    #     :return: (CustomFeatureButton) button read from the interface.
    #     """
    #     b = CustomFeatureButton()
    #     b.setName(self.nameLineEdit.text().strip())
    #     b.setUseColor(self.colorCheckBox.isChecked())
    #     if self.colorCheckBox.isChecked():
    #         b.setColor(self.mColorButton.color().getRgb())
    #     if self.tooltipCheckBox.isChecked():
    #         b.setToolTip(self.toolTipLineEdit.text().strip())
    #     if self.categoryCheckBox.isChecked():
    #         b.setCategory(self.categoryLineEdit.text().strip())
    #     if self.shortcutCheckBox.isChecked():
    #         b.setShortcut(self.shortcutWidget.getShortcut().strip())
    #     b.setOpenForm(self.openFormCheckBox.isChecked())
    #     return b

    # def currentButtonName(self):
    #     """
    #     Retrieves currently selected button on button combo box.
    #     :return: (CustomFeatureButton) button read from the setup object.
    #     """
    #     text = self.buttonComboBox.currentText()
    #     return text if text != self.tr("Select a button...") else ""

    # def currentButton(self):
    #     """
    #     Retrieves currently selected button on button combo box.
    #     :return: (CustomFeatureButton) button read from the setup object.
    #     """
    #     if not self.currentButtonName():
    #         button = CustomFeatureButton()
    #         button.setName("")
    #         return button
    #     return self.setup().button(self.currentButtonName())

    # @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    # def setActiveButton(self, button):
    #     """
    #     Changes current active button.
    #     :button: (CustomFeatureButton) button to be set as active.
    #     """
    #     isButton = bool(self.currentButtonName())
    #     self.savePushButton.setEnabled(isButton)
    #     self.undoPushButton.setEnabled(isButton)
    #     self.removePushButton.setEnabled(isButton)
    #     if isinstance(button, int):
    #         # then this came from the signal input
    #         button = self.currentButton()
    #     self.buttonComboBox.setCurrentText(button.name())
    #     self.nameLineEdit.setText(button.name())
    #     self.colorCheckBox.setChecked(button.useColor())
    #     if button.useColor():
    #         col = button.color()
    #         col = QColor(col) if isinstance(col, str) else QColor(*col)
    #         self.mColorButton.setColor(col)
    #     self.tooltipCheckBox.setChecked(bool(button.toolTip()))
    #     self.toolTipLineEdit.setText(button.toolTip())
    #     self.categoryCheckBox.setChecked(bool(button.category()))
    #     self.categoryLineEdit.setText(button.category())
    #     self.shortcutCheckBox.setChecked(bool(button.shortcut()))
    #     self.shortcutWidget.setShortcut(button.shortcut())
    #     self.openFormCheckBox.setChecked(button.openForm())

    # def validateData(self, data=None, new=True):
    #     """
    #     Validates if a given set of button properties is valid accordingly to
    #     current button setup context.
    #     :param data: (dict) map of button properties to be validated.
    #     :param new: (bool) indicates if the property map is for a button that
    #                 is already saved into current setup, or if it is supposed
    #                 to be added to it.
    #     :return: (str) invalidation reason.
    #     """
    #     b = CustomFeatureButton(data or self.readButton().properties())
    #     s = self.setup()
    #     return ""

    # def isValid(self):
    #     """
    #     Identifies whether all input data is valid.
    #     :return: (bool) input data is validity status.
    #     """
    #     return self.validateData() == ""

    # @pyqtSlot(bool, name="on_savePushButton_clicked")
    # def updateCurrentButton(self, props):
    #     """
    #     Current data will be stored as current button's properties.
    #     :param props: (dict) a map to button's properties to be updated.
    #     """
    #     if isinstance(props, bool):
    #         # if button pressing was the triggering event, current data will be
    #         # store into current button
    #         props = self.readButton().properties()
    #     msg = self.validateData()
    #     if msg == "":
    #         button = self.currentButton()
    #         prevName = button.name()
    #         self.setup().updateButton(prevName, props)
    #         newName = button.name()
    #         if prevName != newName:
    #             self.buttonComboBox.removeItem(
    #                 self.buttonComboBox.findText(prevName)
    #             )
    #             self.buttonComboBox.addItem(newName)
    #             self.buttonComboBox.setCurrentText(newName)

    # @pyqtSlot(bool)
    # def on_undoPushButton_clicked(self):
    #     """
    #     Restores stored data from current button and sets it to GUI.
    #     """
    #     self.setActiveButton(self.currentButton())

    # @pyqtSlot(bool, name="on_addPushButton_clicked")
    # def addButton(self):
    #     """
    #     Adds a new button to the interface.
    #     """
    #     button = CustomFeatureButton()
    #     name = button.name()
    #     names = [b.name() for b in self.setup().buttons()]
    #     if name in names:
    #         i = 1
    #         name = "{0} {1}".format(name, i)
    #         while name in names:
    #             name = "{0} {1}".format(button.name(), i)
    #             i += 1
    #         button.setName(name)
    #     self.setup().addButton(button.properties())
    #     self.buttonComboBox.addItem(name)
    #     self.setActiveButton(button)

    # @pyqtSlot(bool)
    # def on_removePushButton_clicked(self):
    #     """
    #     Removes the current button from setup.
    #     """
    #     # ADD CONFIRMATION BOX
    #     name = self.currentButton().name()
    #     if name == "":
    #         # ignore the "Select a button..."
    #         return
    #     self.setup().removeButton(name)
    #     self.buttonComboBox.removeItem(self.buttonComboBox.findText(name))

    # def state(self):
    #     """
    #     Retrieves dialog's data display state.
    #     :return: (dict) a map to object's state.
    #     """
    #     return {
    #         "item": self.buttonComboBox.currentIndex(),
    #         "buttons": [b.properties() for b in self.setup().buttons()],
    #         "activeData": {} # this may be a modified button not yet saved
    #     }

    # def setState(self, state):
    #     """
    #     Restores a saved state to current dialog's instance.
    #     :param state: (dict) a map to object's state.
    #     """
    #     msg = self.validateData(state)
    #     if msg == "":
    #         self.setup()
        