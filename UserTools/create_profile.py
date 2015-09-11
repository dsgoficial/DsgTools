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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'create_profile.ui'))

class CreateProfile(QtGui.QDialog, FORM_CLASS):
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
        self.db = None

        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(True)
        self.utils = Utils()
        
        self.populateTreeDict()
        
    def __del__(self):
        if self.db:
            self.db.close()
            self.db = None
        
    def getDbInfo(self):
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        else:
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '30', 'seed_edgv30.sqlite')

        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(edgvPath)
        if not self.db.open():
            #QgsMessageLog.logMessage(self.db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            print self.db.lastError().text()
        
    def populateTreeDict(self):
        self.getDbInfo()
        
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        
        self.profile = dict()
        
        categories = dict()
        while query.next():
            #table name
            tableName = query.value(0)
            
            #proceed only for edgv tables
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" or tableName.split("_")[-1] == "a":
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
                    categories[schema][category][layerName]['create'] = '0'
                    categories[schema][category][layerName]['drop'] = '0'
                    categories[schema][category][layerName]['super'] = '0'
                    
        self.profile['database'+'_'+self.versionCombo.currentText()] = categories

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        if not self.lineEdit.text():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profile = self.lineEdit.text()
            
        path = os.path.join(self.folder, profile+'.json')
        
        with open(path, 'w') as outfile:
            json.dump(self.profile, outfile, sort_keys=True, indent=4)

    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
         self.populateTreeDict()
                 