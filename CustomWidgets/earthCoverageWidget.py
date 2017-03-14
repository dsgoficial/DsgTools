# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
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
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'earthCoverageWidget.ui'))

from DsgTools.ValidationTools.setupEarthCoverage import SetupEarthCoverage
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from qgis.core import QgsMessageLog
from DsgTools.ServerManagementTools.earthCoverageManager import EarthCoverageManager
from DsgTools.dsgEnums import DsgEnums

class EarthCoverageWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.earthCoverageDict = dict()
        self.abstractDb = None
        self.settingDict = dict()
        self.enableSetup(False)
    
    def checkSuperUser(self):
        try:
            if self.abstractDb.checkSuperUser():
                self.enableSetup(True)
                return True
            else:
                self.enableSetup(False)
                return False
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
    
    def enableSetup(self, enabled):
        self.defineEarthCoverageButton.setEnabled(enabled)
    
    def instantiateServerAbstractDb(self, abstractDb):
        (host, port, user, password) = abstractDb.getParamsFromConectedDb()
        serverAbstractDb = DbFactory().createDbFactory('QPSQL')
        serverAbstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
        return serverAbstractDb

    @pyqtSlot(AbstractDb)
    def setDatabase(self, db):
        """
        Sets the database and create validation structure
        """
        self.abstractDb = db
        if db:
            if self.checkSuperUser():
                serverAbstractDb = self.instantiateServerAbstractDb(self.abstractDb)
                edgvVersion = self.abstractDb.getDatabaseVersion()
                self.genericManager = EarthCoverageManager(serverAbstractDb, {self.abstractDb.db.databaseName():self.abstractDb}, edgvVersion)
                self.abstractDb.checkAndCreateValidationStructure()
            self.loadEarthCoverage()

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        """
        Closes the window
        """
        self.hide()

    @pyqtSlot(bool)
    def on_defineEarthCoverageButton_clicked(self):
        """
        Defines a earth coverage configuration
        """
        if not self.abstractDb:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to manage earth coverage'))
            return
        try:
            classList = self.abstractDb.getOrphanGeomTables()
            areas = self.abstractDb.getParentGeomTables(getFullName = True, primitiveFilter = ['a'])
            lines = self.abstractDb.getParentGeomTables(getFullName = True, primitiveFilter = ['l'])
            if self.earthCoverageDict == dict():
                self.getEarthCoverageDict()
            oldCoverage = None
            data = self.earthCoverageDict
            if data != dict():
                if QMessageBox.question(self, self.tr('Question'), self.tr('An earth coverage is already defined. Do you want to redefine it? All data will be lost.'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                    self.loadEarthCoverage()
                    return
                oldCoverage = data
            edgvVersion = self.abstractDb.getDatabaseVersion()
            settings = self.genericManager.getSettings()
            if edgvVersion in settings.keys():
                propertyList = settings
            else:
                propertyList = []
            dlg = SetupEarthCoverage(edgvVersion, areas, lines, oldCoverage, propertyList)
            dlg.exec_()
            configDict = dlg.configDict
            if configDict != dict():
                newDict = json.dumps(configDict)
                successList, errorDict = self.genericManager.createAndInstall(configDict['configName'], newDict, edgvVersion, dbList = [self.abstractDb.db.databaseName()])
                if errorDict != dict():
                    raise errorDict.values()[0]
                QtGui.QMessageBox.critical(self, self.tr('Success!'), self.tr('Earth Coverage created!'))
                self.loadEarthCoverage()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

    def clearTree(self):
        """
        Clear the configuration tree widget
        """
        self.earthCoverageTreeWidget.invisibleRootItem().takeChildren()

    def getEarthCoverageDict(self):
        propertyDict = self.genericManager.getPropertyPerspectiveDict(viewType = DsgEnums.Database)
        dbName = self.abstractDb.db.databaseName()
        if dbName not in propertyDict.keys():
            self.settingDict = dict()
            return
        else:
            propertyName = propertyDict[dbName][0]
            edgvVersion = self.abstractDb.getDatabaseVersion()
            self.settingDict = self.genericManager.getSetting(propertyName,edgvVersion)
            self.earthCoverageDict = self.settingDict['earthCoverageDict']

    def loadEarthCoverage(self):
        """
        Loads a previously saved earth coverage configuration
        """
        try:
            self.clearTree()
            if self.earthCoverageDict == dict():
                self.getEarthCoverageDict()
            rootItem = self.earthCoverageTreeWidget.invisibleRootItem()
            #database item
            for key in self.earthCoverageDict.keys():
                item = QTreeWidgetItem(rootItem)
                item.setText(0,key)
                item.setExpanded(True)
                for cl in self.earthCoverageDict[key]:
                    covItem = QTreeWidgetItem(item)
                    covItem.setText(1,cl)
                    covItem.setExpanded(True)
        except Exception as e:
            QgsMessageLog.logMessage(self.tr('Earth Coverage not loaded! Check log for details.')+str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)