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

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validationWorkflowCreator.ui'))

class ValidationWorkflowCreator(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, validationManager, parameterDict = None, parent = None):
        """Constructor."""
        super(ValidationWorkflowCreator, self).__init__(parent)
        self.validationManager = validationManager
        self.setupUi(self)
        self.workflowOrderedWidget.parent = self

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
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()
    
    def validate(self, parameterDict):
        if 'orderedAttributeRulesWidget' not in list(parameterDict.keys()):
            return False
        return True
    
    def invalidatedReason(self):
        return self.tr('Invalid tag for attributeRulesEditor!')
    
    def getParameterDict(self):
        return {'orderedAttributeRulesWidget':self.attributeRulesWidget.getParameterDict()}
    
    def populateInterface(self, parameterDict):
        self.attributeRulesWidget.populateInterface(parameterDict['orderedAttributeRulesWidget'])
    
    def validateJson(self, parameterDict):
        if ['orderedAttributeRulesWidget'] != list(parameterDict.keys()):
            return False
        return self.attributeRulesWidget.validateJson(parameterDict['orderedAttributeRulesWidget'])

