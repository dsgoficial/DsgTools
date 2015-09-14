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

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'assign_profiles.ui'))

class AssignProfiles(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(AssignProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
#         self.widget.tabWidget.removeTab(0)
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(False)
        self.utils = Utils()        
        
        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')
        self.getProfiles()

    def parseJson(self, filename):       
        try:
            file = open(filename, 'r')
            data = file.read()
            profileDict = json.loads(data)
            file.close()
            return profileDict
        except:
            return None
        
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        for i in range(self.assignedProfiles.__len__()):
            role = self.assignedProfiles.item(i).text()
            profile = os.path.join(self.folder, role +'.json')
            dict = self.parseJson(profile)

            sql = self.gen.createRole(role, dict)
            print sql
            split = sql.split(';')
            query = QSqlQuery(self.widget.db)

            for inner in split:
                if not query.exec_(inner):
                    print 'deu merda'
                    print self.widget.db.lastError().text()
        
    def getProfiles(self):
        self.possibleProfiles.clear()
        
        ret = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'json':
                    ret.append(file.split('.')[0])

        ret.sort()
        self.possibleProfiles.addItems(ret)
        
    @pyqtSlot(bool)
    def on_insertAllButton_clicked(self):
        tam = self.possibleProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.possibleProfiles.takeItem(i-2)
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

    @pyqtSlot(bool)
    def on_removeAllButton_clicked(self):
        tam = self.assignedProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.assignedProfiles.takeItem(i-2)
            self.possibleProfiles.addItem(item)
        self.possibleProfiles.sortItems()

    @pyqtSlot(bool)
    def on_insertButton_clicked(self):
        listedItems = self.possibleProfiles.selectedItems()
        for i in listedItems:
            item = self.possibleProfiles.takeItem(self.possibleProfiles.row(i))
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        listedItems = self.assignedProfiles.selectedItems()
        for i in listedItems:
            item = self.assignedProfiles.takeItem(self.assignedProfiles.row(i))
            self.possibleProfiles.addItem(item)
        self.possibleProfiles.sortItems()
        