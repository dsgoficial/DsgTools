# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attributeRulesEditor.ui'))

class AttributeRulesEditor(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, parameterDict = None, parent = None):
        """Constructor."""
        super(AttributeRulesEditor, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.attributeRulesWidget.setArgs([self.abstractDb.getLayerDict()])
        if parameterDict:
            if self.validateJson(parameterDict):
                self.attributeRulesWidget.populateInterface(parameterDict['orderedAttributeRulesWidget'])
                self.attributeRuleTypeWidget.populateInterface(parameterDict['attributeRuleTypeWidget'])

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        1. Validate widget
        2. Export jsonDict
        """
        if not self.validate():
            msg = self.invalidatedReason()
            QgsMessageLog.logMessage(msg, "DSGTools Plugin", Qgis.Critical)
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Errors on interface! Check log for details!'))
            return
        self.done(1)
    
    def validate(self):
        if not self.attributeRuleTypeWidget.validate():
            return False
        if not self.attributeRulesWidget.validate():
            return False
        return True
    
    def invalidatedReason(self):
        msg = ''
        msg += self.attributeRuleTypeWidget.invalidatedReason()
        msg += self.attributeRulesWidget.invalidatedReason()
        return msg
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()
    
    def validate(self, parameterDict):
        if 'orderedAttributeRulesWidget' not in list(parameterDict.keys()):
            return False
        return True
    
    def invalidatedJsonReason(self):
        msg = ''
        if ['attributeRuleTypeWidget', 'orderedAttributeRulesWidget'] != list(parameterDict.keys()):
            msg += self.tr('Invalid tags for attributeRulesEditor!\n')
        msg += self.attributeRulesWidget.invalidatedJsonReason()
        msg += self.attributeRuleTypeWidget.invalidatedJsonReason()
    
    def getParameterDict(self):
        return {'attributeRuleTypeWidget':self.attributeRuleTypeWidget.getParameterDict(),
        'orderedAttributeRulesWidget':self.attributeRulesWidget.getParameterDict()}
    
    def populateInterface(self, parameterDict):
        self.attributeRuleTypeWidget.populateInterface(parameterDict['attributeRuleTypeWidget'])
        self.attributeRulesWidget.populateInterface(parameterDict['orderedAttributeRulesWidget'])
    
    def validateJson(self, parameterDict):
        if ['attributeRuleTypeWidget', 'orderedAttributeRulesWidget'] != list(parameterDict.keys()):
            return False
        if not self.attributeRulesWidget.validateJson(parameterDict['orderedAttributeRulesWidget']):
            return False
        if not self.attributeRuleTypeWidget.validateJson(parameterDict['attributeRuleTypeWidget']):
            return False
        return True

