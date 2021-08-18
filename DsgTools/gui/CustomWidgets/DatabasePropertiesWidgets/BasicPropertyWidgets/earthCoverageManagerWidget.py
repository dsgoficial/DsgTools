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
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor

#DsgTools imports
from DsgTools.core.ServerManagementTools.earthCoverageManager import EarthCoverageManager
from DsgTools.gui.Misc.PostgisCustomization.createDatabaseCustomization import CreateDatabaseCustomization
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.setupEarthCoverage import SetupEarthCoverage
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class EarthCoverageManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb, edgvVersion, dbsDict = {}):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = EarthCoverageManager(serverAbstractDb, dbsDict, edgvVersion)
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = GenericParameterSetter()
        if not dlg.exec_():
            return
        templateDb, propertyName, edgvVersion = dlg.getParameters()
        if edgvVersion == self.tr('Select EDGV Version'):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Enter a EDGV Version'))
            return
        if propertyName == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Enter an Earth Coverage Name!'))
            return
        if propertyName in list(self.genericDbManager.getPropertyPerspectiveDict(viewType = DsgEnums.Property).keys()):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Earth Coverage Name already exists!'))
            return
        fieldSetupDict = self.populateConfigInterface(templateDb, propertyName = propertyName)
        if fieldSetupDict:
            self.genericDbManager.createSetting(propertyName, edgvVersion, fieldSetupDict)
            self.refresh()
            QMessageBox.information(self, self.tr('Success!'), self.tr('Field Toolbox Configuration ') + propertyName + self.tr(' created successfuly!'))   


    def populateConfigInterface(self, templateDb, jsonDict = None, propertyName = None):
        '''
        Must be reimplemented in each child
        '''
        areas = templateDb.getParentGeomTables(getFullName = True, primitiveFilter = ['a'])
        lines = templateDb.getParentGeomTables(getFullName = True, primitiveFilter = ['l'])
        edgvVersion = templateDb.getDatabaseVersion()
        settings = self.genericDbManager.getSettings()
        if edgvVersion in list(settings.keys()):
            propertyList = settings
        else:
            propertyList = []
        dlg = SetupEarthCoverage(edgvVersion, areas, lines, jsonDict, propertyList, propertyName = propertyName)
        if dlg.exec_():
            return dlg.configDict
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