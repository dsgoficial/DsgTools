# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-08
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# DSGTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createProfileWithProfileManager.ui'))

class CreateProfileWithProfileManager(QtGui.QDialog, FORM_CLASS):
    profileCreated = pyqtSignal(str, str)
    
    def __init__(self, permissionManager, parent = None):
        """
        Constructor
        """
        super(CreateProfileWithProfileManager, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.permissionManager = permissionManager
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()

        self.populateTreeDict()
        
    def __del__(self):
        '''
        Destructor
        '''
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
        
    def getDbInfo(self):
        '''
        Gets database info. This info is used to create a profile model that will be adjusted by the user
        '''
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        elif self.versionCombo.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')

        self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
        if not self.abstractDb:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('A problem occurred! Check log for details.'))
            return
        self.abstractDb.connectDatabase(edgvPath)

        try:
            self.abstractDb.checkAndOpenDb()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)

    def populateTreeDict(self):
        '''
        Makes a tree widget were the user can define profile properties
        '''
        self.getDbInfo()

        tables = []
        try:
            tables = self.abstractDb.getTablesFromDatabase()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        
        self.profile = dict()
        categories = dict()
        for tableName in tables:
            #proceed only for edgv tables
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" or tableName.split("_")[-1] == "a" or tableName.split("_")[0] == 'complexos' or tableName.split("_")[0] == 'dominios':
                layerName = tableName.split('_')[0]+'.'+'_'.join(tableName.split('_')[1::])
                split = tableName.split('_')
                
                if len(split) < 2:
                    continue
                
                schema = split[0]
                category = split[1]
                if schema not in categories.keys():
                    categories[schema] = dict()
                    
                if category not in categories[schema].keys():
                    categories[schema][category] = dict()

                if layerName not in categories[schema][category]:
                    categories[schema][category][layerName] = dict()
                    categories[schema][category][layerName]['read'] = '0'
                    categories[schema][category][layerName]['write'] = '0'
                    
        self.profile['database'+'_'+self.versionCombo.currentText()] = categories

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        '''
        Creates the profile file
        '''
        if not self.lineEdit.text():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profileName = self.lineEdit.text()
        permissionDict = self.permissionManager.getProfiles()
        edgvVersion = self.versionCombo.currentText()
        if profileName in permissionDict[edgvVersion]:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile ') + profileName + self.tr(' for EDGV ') + edgvVersion + self.tr(' already exists!'))
            return
        jsonDict = json.dumps(self.profile, sort_keys=True, indent=4)
        self.permissionManager.createPermissionProfile(profileName, edgvVersion, jsonDict)
        self.profileCreated.emit(profileName, edgvVersion)

    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
        '''
        Changes the edgv version and updates the tree widget
        '''
        self.populateTreeDict()
