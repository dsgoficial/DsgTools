# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-25
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

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore, QtGui
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'genericParameterSetter.ui'))

class GenericParameterSetter(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent = None, nameList = None, hideDbUi = False):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.nameList = nameList
        self.setupUi(self)
        self.isHidden = hideDbUi
        if hideDbUi:
            self.connectionWidget.hide()
        else:
            self.connectionWidget.tabWidget.removeTab(1)
        regex = QtCore.QRegExp('[a-z][a-z\_0-9]*')
        validator = QtGui.QRegExpValidator(regex, self.customNameLineEdit)
        self.customNameLineEdit.setValidator(validator)
    
    def validateUi(self):
        if self.customNameLineEdit.text() == '':
            return False
        if self.nameList:
            if self.customNameLineEdit.text() in self.nameList:
                return False
        if not self.isHidden:
            if self.connectionWidget.abstractDb == None:
                return False
        return True
    
    def validateUiReason(self):
        validateReason = ''
        if self.customNameLineEdit.text() == '':
            validateReason += self.tr('Enter a parameter name!\n')
        if self.nameList:
            if self.customNameLineEdit.text() in self.nameList:
                validateReason += self.tr('Parameter already exists! Choose another name!\n')
        if not self.isHidden:
            if self.connectionWidget.abstractDb == None:
                validateReason += self.tr('Select a template database!\n')
        return validateReason
    
    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        if not self.validateUi():
            reason = self.validateUiReason()
            QMessageBox.warning(self, self.tr('Warning!'), reason)
        else:
            self.done(1)
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):   
        self.done(0)

    def getParameters(self):
        if self.isHidden:
            return self.customNameLineEdit.text()
        else:
            return (self.connectionWidget.abstractDb , self.customNameLineEdit.text(), self.connectionWidget.abstractDb.getDatabaseVersion())
