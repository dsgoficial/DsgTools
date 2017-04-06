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
    
    def __init__(self, permissionManager, abstractDb, parent = None):
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
        self.abstractDb = abstractDb
        self.abstractDbFactory = DbFactory()

        self.populateTreeDict()
        
    def __del__(self):
        """
        Destructor
        """
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None

    def populateTreeDict(self):
        """
        Makes a tree widget were the user can define profile properties
        """
        try:
            geomTypeDict = self.abstractDb.getGeomTypeDict()
            geomDict = self.abstractDb.getGeomDict(geomTypeDict, insertCategory = True)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return
        
        self.profile = dict()
        categories = dict()
        for layerName in geomDict.keys():
            schema = geomDict[layerName]['schema']
            category = geomDict[layerName]['category']
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
        """
        Creates the profile file
        """
        if not self.lineEdit.text():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profileName = self.lineEdit.text()
        permissionDict = self.permissionManager.getSettings()
        edgvVersion = self.versionCombo.currentText()
        if edgvVersion in permissionDict.keys():
            if profileName in permissionDict[edgvVersion]:
                QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile ') + profileName + self.tr(' for EDGV ') + edgvVersion + self.tr(' already exists!'))
                return
        jsonDict = json.dumps(self.profile, sort_keys=True, indent=4)
        self.permissionManager.createSetting(profileName, edgvVersion, jsonDict)
        self.profileCreated.emit(profileName, edgvVersion)

    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
        """
        Changes the edgv version and updates the tree widget
        """
        self.populateTreeDict()
