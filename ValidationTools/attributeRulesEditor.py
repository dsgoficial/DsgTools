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
        email                : borba@dsg.eb.mil.br
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attributeRulesEditor.ui'))

class AttributeRulesEditor(QtGui.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, parameterDict = {}, parent = None):
        """Constructor."""
        super(AttributeRulesEditor, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.attributeRulesWidget.setArgs([self.abstractDb.getLayerDict()])
        if parameterDict != {}:
            self.attributeRulesWidget.populateInterface(parameterDict)

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        1. Validate widget
        2. Export jsonDict
        """
        if not self.attributeRulesWidget.validate():
            msg = self.attributeRulesWidget.invalidatedReason()
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Errors on interface! Check log for details!'))
            self.done(0)
            return
        self.done(1)
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()
    
    def getParameterDict(self):
        return self.attributeRulesWidget.getParameterDict()
