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
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog, QMessageBox, QRadioButton, QColor


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonPropWidget.ui'))

class ButtonPropWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ButtonPropWidget, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(bool, name = 'on_colorCheckBox_toggled')
    @pyqtSlot(bool, name = 'on_tooltipCheckBox_toggled')
    @pyqtSlot(bool, name = 'on_customCategoryCheckBox_toggled')
    def setEnabled(self, state):
        """
        Enables or disables 
        """
        if self.sender().objectName() == 'colorCheckBox':
            self.mColorButton.setEnabled(state)
        if self.sender().objectName() == 'tooltipCheckBox':
            self.toolTipLineEdit.setEnabled(state)
        if self.sender().objectName() == 'customCategoryCheckBox':
            self.customCategoryComboBox.setEnabled(state)
    
    def getParameterDict(self):
        """
        Returns a dict in the format:
        {'buttonColor':--color of the button--, 'buttonToolTip'--button toolTip--, 'buttonGroupTag':--group tag of the button--}
        """
        parameterDict = dict()
        if self.colorCheckBox.checkState() == Qt.Checked:
            parameterDict['buttonColor'] = ','.join(map(str,self.mColorButton.color().getRgb())) #must map to string
        if self.tooltipCheckBox.checkState() == Qt.Checked:
            parameterDict['buttonToolTip'] = self.toolTipLineEdit.text()
        if self.customCategoryCheckBox.checkState() == Qt.Checked:
            parameterDict['buttonGroupTag'] = self.customCategoryComboBox.currentText()
        return parameterDict
    
    def setInterface(self, parameterDict):
        """
        Sets the interface with a dict in the format:
        {'buttonColor':--color of the button--, 'buttonToolTip'--button toolTip--, 'buttonGroupTag':--group tag of the button--}
        """
        if 'buttonColor' in parameterDict.keys():
            self.colorCheckBox.setCheckState(Qt.Checked)
            R,G,B,A = map(int,parameterDict['buttonColor'].split(',')) #QColor only accepts int values
            self.mColorButton.setColor(QColor(R,G,B,A))
        else:
            self.colorCheckBox.setCheckState(Qt.Unchecked) #if 'buttonColor' isn't on dict keys, set colorCheckBox as unchecked
        if 'buttonToolTip' in parameterDict.keys():
            self.tooltipCheckBox.setCheckState(Qt.Checked)
            self.toolTipLineEdit.setText(parameterDict['buttonToolTip'])
        else:
            self.tooltipCheckBox.setCheckState(Qt.Unchecked) #if 'buttonToolTip' isn't on dict keys, set colorCheckBox as unchecked
        if 'buttonGroupTag' in parameterDict.keys():
            self.customCategoryCheckBox.setCheckState(Qt.Checked)
            itemList = [self.customCategoryComboBox.itemText(i) for i in range(self.customCategoryComboBox.count())]
            if parameterDict['buttonGroupTag'] not in itemList:
                self.customCategoryComboBox.addItem(parameterDict['buttonGroupTag'])
            idx = self.customCategoryComboBox.findData(parameterDict['buttonGroupTag'], Qt.MatchExactly)
            if idx != -1:
                self.customCategoryComboBox.setCurrentIndex(idx)
                
        else:
            self.customCategoryCheckBox.setCheckState(Qt.Unchecked) #if 'buttonGroupTag' isn't on dict keys, set colorCheckBox as unchecked
