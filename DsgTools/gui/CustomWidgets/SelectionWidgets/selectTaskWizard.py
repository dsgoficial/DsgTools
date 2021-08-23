# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
                             -------------------
        begin                : 2017-03-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
        mod history          : 
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
import os, json

#PyQt imports
from qgis.PyQt import QtWidgets, QtCore, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor

#DsgTools imports
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'selectTaskWizard.ui'))

class SelectTaskWizard(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, settingList, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.hideSettings(True)
        self.settingList = settingList
    
    def hideSettings(self, hide):
        self.settingComboBox.hide(hide)
        self.label.hide(hide)
    
    def populateSettingCombo(self, settingList):
        self.settingComboBox.clear()
        self.settingComboBox.addItem(self.tr('Select one setting'))
        for setting in settingList:
            self.settingComboBox.addItem(setting)
    
    @pyqtSlot(name='on_importRadioButton_toggled')
    @pyqtSlot(name='on_createNewRadioButton_toggled')
    @pyqtSlot(name='on_installRadioButton_toggled')
    def manageCombos(self):
        if self.installRadioButton.checkState() == Qt.Checked:
            self.hideSettings(False)
            self.populateSettingCombo(self.settingList)
        else:
            self.hideSettings(True)
            self.populateSettnigCombo.clear()

    def validateCurrentPage(self):
        if self.currentId() == 0:
            if self.importRadioButton.checkState() == Qt.Unchecked() and self.createNewRadioButton.checkState() == Qt.Unchecked() and self.installRadioButton.checkState() == Qt.Unchecked():
                errorMsg = self.tr('An option must be chosen!\n')
                QMessageBox.warning(self, self.tr('Error!'), errorMsg)
                return False
            if self.installRadioButton.checkState() == Qt.Checked():
                if self.settingComboBox.currentIndex() == 0:
                    errorMsg = self.tr('A setting must be chosen!\n')
                    QMessageBox.warning(self, self.tr('Error!'), errorMsg)
                    return False
                else:
                    return True
            return True
        else:
            return True