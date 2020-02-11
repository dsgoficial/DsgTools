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

from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup

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
        self.orderedTableWidget.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.textEdit.setPlaceholderText(
            self.tr("Insert a short description for current button setup..."))
        self.setup = buttonSetup or CustomButtonSetup()

    def newButton(self):
        """
        Generates a new button, adds it to buttons manager object and retrieve
        its widget.
        :return: (QPushButton) widget associated with a new instance of button.
        """
        b = self.setup.newButton()
        self.buttonComboBox.addItem(b.name())
        self.setCurrentButton(b)
        return b.widget()

    def setCurrentButton(self, button):
        """
        Sets button properties to the GUI.
        :param button:  (CustomFeatureButton) button to be set to the GUI.
        """
        pass