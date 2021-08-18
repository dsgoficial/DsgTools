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
    os.path.dirname(__file__), 'customSizeSetter.ui'))

class CustomSizeSetter(QtWidgets.QDialog, FORM_CLASS):
    sizeCreated = pyqtSignal(dict)
    def __init__(self, customDict, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.customDict = customDict
        self.setupUi(self)
        regex = QtCore.QRegExp('[0-9][0-9\.0-9]*')
        validator = QtGui.QRegExpValidator(regex, self.measureLineEdit)
        self.measureLineEdit.setValidator(validator)
    
    def validateUi(self):
        if self.comboTextLineEdit.text() == '':
            return False
        if self.measureLineEdit.text() == '':
            return False
        return True
    
    def validateUiReason(self):
        validateReason = ''
        if self.comboTextLineEdit.text() == '':
            validateReason += self.tr('Enter a combo box text!\n')
        if self.measureLineEdit.text() == '':
            validateReason += self.tr('Enter a measurement!\n')
        return validateReason
    
    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        if not self.validateUi():
            reason = self.validateUiReason()
            QtWidgets.QMessageBox.warning(self, self.tr('Warning!'), reason)
        else:
            self.done(1)
            newCustomDict = self.getCustomDictFromUi()
            self.sizeCreated.emit(newCustomDict)
    
    def getCustomDictFromUi(self):
        newValueDict = dict()
        if self.areaRadioButton.isChecked():
            newValueDict['shape'] = 'area'
        else:
            newValueDict['shape'] = 'distance'
        newValueDict['comboText'] = self.comboTextLineEdit.text()
        newValueDict['value'] = self.measureLineEdit.text()
        return newValueDict
    
    @pyqtSlot(bool, name = 'on_areaRadioButton_toggled')
    def turnButtonsOn(self, enabled):
        if enabled:
            self.measureLabel.setText(self.tr(u'Area in mm²'))
        else:
            self.measureLabel.setText(self.tr('Distance in mm'))

    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):   
        self.done(0)
