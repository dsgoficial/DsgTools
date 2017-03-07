# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog

#DsgTools imports
from DsgTools.ServerManagementTools.earthCoverageManager import EarthCoverageManager
from DsgTools.PostgisCustomization.createDatabaseCustomization import CreateDatabaseCustomization
from DsgTools.CustomWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.Utils.utils import Utils

from qgis.core import QgsMessageLog
import json

class EarthCoverageManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = EarthCoverageManager(serverAbstractDb, {})
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = CreateDatabaseCustomization(self.serverAbstractDb, self.genericDbManager)
        dlg.exec_()
    
    @pyqtSlot(bool)
    def on_deleteCustomizationPushButton_clicked(self):
        #TODO: Reimplement
        customizationName = self.customizationListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete customization ')+customizationName+'?', QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.deleteCustomization(customizationName, edgvVersion)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customization ') + customizationName + self.tr(' successfully deleted.'))
            self.refreshProfileList()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem deleting customization: ') + e.args[0])

    def populateConfigInterface(self, templateDb, jsonDict = None):
        '''
        Must be reimplemented in each child
        '''
        fieldDlg = FieldSetup(templateDb,returnDict = True)
        if jsonDict:
            fieldDlg.loadReclassificationConf(jsonDict)
        if fieldDlg.exec_():
            return fieldDlg.makeReclassificationDict()
        else:
            return None
    
    def getUpdateSelectedSettingHeader(self):
        header = self.tr('Update Earth Coverage configuration complete. \n')
        operation = self.tr('earth coverage configuration')
        return header, operation

    def getUninstallSelectedSettingHeader(self):
        header = self.tr('Uninstall Earth Coverage configuration complete. \n')
        operation = self.tr('earth coverage configuration')
        return header, operation

    def getApplyHeader(self):
        header = self.tr('Install Earth Coverage configuration complete. \n')
        operation = self.tr('earth coverage configurations')
        return header, operation
    
    def getDeleteHeader(self):
        header = self.tr('Delete Earth Coverage configuration complete. \n')
        operation = self.tr('earth coverage configurations')
        return header, operation
    
    def getUninstallFromSelected(self):
        header = self.tr('Uninstall Earth Coverage configuration complete. \n')
        operation = self.tr('earth coverage configurations')
        return header, operation