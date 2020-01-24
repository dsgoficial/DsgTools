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
        self.buttonSetup = buttonSetup or CustomButtonSetup()
        self.refresh()

    def clear(self):
        """
        Clears all data from interface.
        """
        pass

    def refresh(self):
        """
        Clears interface data and resets it to its default.
        """
        self.clear()
        self.buttonComboBox.addItem(self.tr("Select a button..."))
        self.buttonComboBox.addItems([
            b.name() for b in self.buttonSetup.buttons()
        ])

    def readButton(self):
        """
        Reads data from the interface and sets it to a button object.
        :return: (CustomFeatureButton) button read from the interface.
        """
        b = CustomFeatureButton()
        b.setName(self.nameLineEdit.text())
        b.setUseColor(self.colorCheckBox.isChecked())
        if self.colorCheckBox.isChecked():
            b.setColor(self.mColorButton.color().getRgb())
        if self.tooltipCheckBox.isChecked():
            b.setToolTip(self.toolTipLineEdit.text())
        if self.categoryCheckBox.isChecked():
            b.setCategory(self.categoryLineEdit.text())
        if self.shortcutCheckBox.isChecked():
            b.setShortcut(self.shortcutWidget.getShortcut())
        b.setOpenForm(self.openFormCheckBox.isChecked())
        return b

    def currentButtonName(self):
        """
        Retrieves currently selected button on button combo box.
        :return: (CustomFeatureButton) button read from the setup object.
        """
        text = self.buttonComboBox.currentText()
        return text if text != self.tr("Select a button...") else ""

    def currentButton(self):
        """
        Retrieves currently selected button on button combo box.
        :return: (CustomFeatureButton) button read from the setup object.
        """
        if not self.currentButtonName():
            button = CustomFeatureButton()
            button.setName("")
            return button
        return self.buttonSetup.button(self.currentButtonName())

    @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    def setCurrentButton(self, button):
        """
        Changes current active button.
        :button: (CustomFeatureButton) button to be set as active.
        """
        isButton = bool(self.currentButtonName())
        self.savePushButton.setEnabled(isButton)
        self.undoPushButton.setEnabled(isButton)
        self.removePushButton.setEnabled(isButton)
        if isinstance(button, int):
            # then this came from the signal input
            button = self.currentButton()
        self.buttonComboBox.setCurrentText(button.name())
        self.nameLineEdit.setText(button.name())
        self.colorCheckBox.setChecked(button.useColor())
        if button.useColor():
            col = button.color()
            col = QColor(col) if isinstance(col, str) else QColor(*col)
            self.mColorButton.setColor(col)
        self.tooltipCheckBox.setChecked(bool(button.toolTip()))
        self.toolTipLineEdit.setText(button.toolTip())
        self.categoryCheckBox.setChecked(bool(button.category()))
        self.categoryLineEdit.setText(button.category())
        self.shortcutCheckBox.setChecked(bool(button.shortcut()))
        self.shortcutWidget.setShortcut(button.shortcut())
        self.openFormCheckBox.setChecked(button.openForm())

    @pyqtSlot(bool)
    def on_savePushButton_clicked(self, props):
        """
        Current data will be store as current buttons properties
        """
        pass

    @pyqtSlot(bool)
    def on_undoPushButton_clicked(self):
        """
        Current data will be store as current buttons properties
        """
        self.setCurrentButton(self.currentButton())

    @pyqtSlot(bool, name="on_addPushButton_clicked")
    def addButton(self):
        """
        Adds a new button to the interface.
        """
        button = CustomFeatureButton()
        name = button.name()
        names = [b.name() for b in self.buttonSetup.buttons()]
        if name in names:
            i = 1
            name = "{0} {1}".format(name, i)
            while name in names:
                name = "{0} {1}".format(button.name(), i)
                i += 1
            button.setName(name)
        self.buttonSetup.addButton(button.properties())
        self.buttonComboBox.addItem(name)
        self.setCurrentButton(button)

    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        """
        Current data will be store as current buttons properties
        """
        pass
