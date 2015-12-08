# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# DSGTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'create_profile.ui'))

class CreateProfile(QtGui.QDialog, FORM_CLASS):
    profileCreated = pyqtSignal(str)
    
    def __init__(self, parent = None):
        """Constructor."""
        super(CreateProfile, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')

        self.abstractDb = None
        self.abstractDbFactory = DbFactory()

        self.populateTreeDict()
        
    def __del__(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
        
    def getDbInfo(self):
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        else:
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '30', 'seed_edgv30.sqlite')

        self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
        self.abstractDb.connectDatabase(edgvPath)

        try:
            self.abstractDb.checkAndOpenDb()
        except Exception as e:
            print e.args[0]

    def populateTreeDict(self):
        self.getDbInfo()

        tables = self.abstractDb.getTablesFromDatabase()
        
        self.profile = dict()
        categories = dict()
        for tableName in tables:
            #proceed only for edgv tables
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" or tableName.split("_")[-1] == "a" or tableName.split("_")[0] == 'complexos':
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
        if not self.lineEdit.text():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profileName = self.lineEdit.text()
            
        path = os.path.join(self.folder, profileName+'.json')
        
        with open(path, 'w') as outfile:
            json.dump(self.profile, outfile, sort_keys=True, indent=4)
            self.profileCreated.emit(profileName)

    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
         self.populateTreeDict()
