# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-14
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
from DsgTools.UserTools.create_profile import CreateProfile
from DsgTools.UserTools.profile_editor import ProfileEditor

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'assign_profiles.ui'))

class AssignProfiles(QtGui.QDialog, FORM_CLASS):
    def __init__(self, index = None, parent = None):
        """Constructor."""
        super(AssignProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(0, False)
        if index:
            self.widget.comboBoxPostgis.setCurrentIndex(index)
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(False)
        self.utils = Utils()        
        
        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')
        self.getModelProfiles()
        
        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.getInstalledProfiles)

    def parseJson(self, filename):       
        try:
            file = open(filename, 'r')
            data = file.read()
            profileDict = json.loads(data)
            file.close()
            return profileDict
        except:
            return None
        
    def getModelProfiles(self):
        self.possibleProfiles.clear()
        
        ret = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'json':
                    ret.append(file.split('.')[0])

        ret.sort()
        self.possibleProfiles.addItems(ret)
        
    def getInstalledProfiles(self):
        self.assignedProfiles.clear()
        
        if not self.widget.abstractDb:
            return
        
        ret = self.widget.abstractDb.getRoles()

        self.assignedProfiles.addItems(ret)

    @pyqtSlot(bool)
    def on_installButton_clicked(self):
        for item in self.possibleProfiles.selectedItems():
            role = item.text()
            profile = os.path.join(self.folder, role +'.json')
            dict = self.parseJson(profile)
            
            try:
                self.widget.abstractDb.createRole(role, dict)
            except Exception as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
                return
            
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profiles assigned successfully!'))    
        
        self.getInstalledProfiles()            
        
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.close()
        
    @pyqtSlot(bool)
    def on_openProfileEditor_clicked(self):
        dlg = ProfileEditor()
        dlg.exec_()
        self.getModelProfiles()
        
    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        problem = False
        for item in self.assignedProfiles.selectedItems():
            role = item.text()

            sql = self.gen.dropRole(role)
            split = sql.split('#')
            query = QSqlQuery(self.widget.db)

            for inner in split:
                if not query.exec_(inner):
                    QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem removing profile: ') +role+'\n'+query.lastError().text())
                    problem = True
            
        if not problem:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profiles removed successfully!'))
        
        self.getInstalledProfiles()

    @pyqtSlot(bool)
    def on_removeJson_clicked(self):
        if not QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to remove selected profile models?')):
            return
        
        for item in self.possibleProfiles.selectedItems():
            json = item.text()
            file = json+'.json'
            path = os.path.join(self.folder, file)
            try:
                os.remove(path)
            except OSError as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem removing profile model: ')+json+'\n'+e.strerror)
        
        self.getModelProfiles()
