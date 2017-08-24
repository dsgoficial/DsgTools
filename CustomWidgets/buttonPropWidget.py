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

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog, QMessageBox, QRadioButton


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonPropWidget.ui'))

class ButtonPropWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ButtonPropWidget, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(bool, name = 'on_colorCheckBox_stateChanged')
    @pyqtSlot(bool, name = 'on_tooltipCheckBox_stateChanged')
    @pyqtSlot(bool, name = 'on_customCategoryCheckBox_stateChanged')
    def setEnabled(self, state):
        """
        Enables or disables 
        """
        if self.sender.name() == 'colorCheckBox':
            self.mColorButton.setEnabled(state)
        if self.sender.name() == 'tooltipCheckBox':
            self.toolTipLineEdit.setEnabled(state)
        if self.sender.name() == 'customCategoryCheckBox':
            self.customCategoryComboBox.setEnabled(state)