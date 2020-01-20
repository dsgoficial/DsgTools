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
from builtins import map
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox, QRadioButton
from qgis.PyQt.QtGui import QColor


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonPropWidget.ui'))

class ButtonPropWidget(QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ButtonPropWidget, self).__init__(parent)
        self.setupUi(self)
    #     self.customCategoryCheckBox.hide()
    #     self.customCategoryLineEdit.hide()
    
    # @pyqtSlot(bool, name = 'on_colorCheckBox_toggled')
    # @pyqtSlot(bool, name = 'on_tooltipCheckBox_toggled')
    # @pyqtSlot(bool, name = 'on_customCategoryCheckBox_toggled')
    # @pyqtSlot(bool, name = 'on_shortcutCheckBox_toggled')
    # def setEnabled(self, state):
    #     """
    #     Enables or disables 
    #     """
    #     if self.sender().objectName() == 'colorCheckBox':
    #         self.mColorButton.setEnabled(state)
    #     if self.sender().objectName() == 'tooltipCheckBox':
    #         self.toolTipLineEdit.setEnabled(state)
    #     if self.sender().objectName() == 'customCategoryCheckBox':
    #         self.customCategoryLineEdit.setEnabled(state)
    #     if self.sender().objectName() == 'shortcutCheckBox':
    #         self.shortcutWidget.setEnabled(state)
    
    # def getParameterDict(self):
    #     """
    #     Returns a dict in the format:
    #     {
    #         'buttonColor':--color of the button--, 
    #         'buttonToolTip':--button toolTip--, 
    #         'buttonGroupTag':--group tag of the button--,
    #         'buttonShortcut':--shortcut--
    #     }
    #     """
    #     parameterDict = dict()
    #     if self.colorCheckBox.checkState() == Qt.Checked:
    #         parameterDict['buttonColor'] = ','.join(map(str,self.mColorButton.color().getRgb())) #must map to string
    #     if self.tooltipCheckBox.checkState() == Qt.Checked:
    #         parameterDict['buttonToolTip'] = self.toolTipLineEdit.text()
    #     if self.customCategoryCheckBox.checkState() == Qt.Checked:
    #         parameterDict['buttonGroupTag'] = self.customCategoryLineEdit.text()
    #     if self.shortcutCheckBox.checkState() == Qt.Checked:
    #         parameterDict['buttonShortcut'] = self.shortcutWidget.getShortcut()
    #     if self.openFormCheckBox.checkState() == Qt.Checked:
    #         parameterDict['openForm'] = True
    #     return parameterDict
    
    # def setInterface(self, parameterDict):
    #     """
    #     Sets the interface with a dict in the format:
    #     {
    #         'buttonColor':--color of the button--, 
    #         'buttonToolTip'--button toolTip--, 
    #         'buttonGroupTag':--group tag of the button--,
    #         'buttonShortcut':--shortcut for the button--,
    #         'openForm':--open feature form when digitizing--
    #     }
    #     """
    #     if 'buttonColor' in list(parameterDict.keys()):
    #         self.colorCheckBox.setCheckState(Qt.Checked)
    #         R,G,B,A = list(map(int,parameterDict['buttonColor'].split(','))) #QColor only accepts int values
    #         self.mColorButton.setColor(QColor(R,G,B,A))
    #     else:
    #         self.colorCheckBox.setCheckState(Qt.Unchecked) #if 'buttonColor' isn't on dict keys, set colorCheckBox as unchecked
    #     if 'buttonToolTip' in list(parameterDict.keys()):
    #         self.tooltipCheckBox.setCheckState(Qt.Checked)
    #         self.toolTipLineEdit.setText(parameterDict['buttonToolTip'])
    #     else:
    #         self.tooltipCheckBox.setCheckState(Qt.Unchecked) #if 'buttonToolTip' isn't on dict keys, set tooltipCheckBox as unchecked
    #         self.toolTipLineEdit.setText('')
    #     if 'buttonGroupTag' in list(parameterDict.keys()):
    #         self.customCategoryCheckBox.setCheckState(Qt.Checked)
    #         self.customCategoryLineEdit.setText(parameterDict['buttonGroupTag'])
    #     else:
    #         self.customCategoryCheckBox.setCheckState(Qt.Unchecked) #if 'buttonGroupTag' isn't on dict keys, set customCategoryCheckBox as unchecked
    #         self.customCategoryLineEdit.setText('')
    #     if 'buttonShortcut' in list(parameterDict.keys()):
    #         self.shortcutCheckBox.setCheckState(Qt.Checked)
    #         self.shortcutWidget.setShortcut(parameterDict['buttonShortcut'])
    #     else:
    #         self.shortcutCheckBox.setCheckState(Qt.Unchecked) #if 'buttonShortcut' isn't on dict keys, set shortcutCheckBox as unchecked
    #         self.shortcutWidget.clearAll()
    #     if 'openForm' in list(parameterDict.keys()):
    #         self.openFormCheckBox.setCheckState(Qt.Checked)
    #     else:
    #         self.openFormCheckBox.setCheckState(Qt.Unchecked) #if 'openForm' isn't on dict keys, set openFormCheckBox as unchecked