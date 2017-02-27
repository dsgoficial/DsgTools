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
from DsgTools.ServerManagementTools.fieldToolBoxConfigManager import FieldToolBoxConfigManager
from DsgTools.CustomWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.CustomWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.ProductionTools.FieldToolBox.field_setup import FieldSetup
from DsgTools.Utils.utils import Utils

from qgis.core import QgsMessageLog
import json

class FieldToolBoxConfigManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb, dbsDict = {}):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = FieldToolBoxConfigManager(serverAbstractDb, dbsDict)
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = GenericParameterSetter()
        dlg.exec_()
        edgvVersion, propertyName = dlg.getParameters()
        if edgvVersion == self.tr('Select EDGV Version'):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Enter a EDGV Version'))
            return
        if propertyName == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Enter a Field Toolbox Configuration Name!'))
            return
        if propertyName in self.genericDbManager.getPropertyPerspectiveDict('property').keys():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Field Toolbox Configuration Name already exists!'))
            return
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        fieldDlg = FieldSetup(templateDb,returnDict = True)
        ret = fieldDlg.exec_()
        if ret == 1:
            fieldSetupDict = fieldDlg.makeReclassificationDict()
            self.genericDbManager.createSetting(propertyName,edgvVersion,fieldSetupDict)
            self.refresh()

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        dbList = self.genericDbManager.dbDict.keys()
        successDict, exceptionDict = self.manageSettings('install', dbList)
        header = self.tr('Install Field Toolbox configuration complete. \n')
        operation = self.tr('field toolbox configurations')
        self.outputMessage(operation, header, successDict, exceptionDict)

    @pyqtSlot(bool)
    def on_deletePushButton_clicked(self):
        dbList = []
        successDict, exceptionDict = self.manageSettings('delete', dbList)
        header = self.tr('Delete Field Toolbox configuration complete. \n')
        operation = self.tr('field toolbox configurations')
        self.outputMessage(operation, header, successDict, exceptionDict)