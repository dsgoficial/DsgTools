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

class EarthCoverageWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.earthCoverageDict = dict()
        self.abstractDb = None
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
                self.genericManager = EarthCoverageManager(serverAbstractDb, {self.abstractDb.db.databaseName():self.abstractDb})
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
            oldCoverage = None
            data = self.abstractDb.getEarthCoverageDict()
            if data:
                if QMessageBox.question(self, self.tr('Question'), self.tr('An earth coverage is already defined. Do you want to redefine it? All data will be lost.'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                    return
                oldCoverage = json.loads(data)
            dlg = SetupEarthCoverage(self.abstractDb, areas, lines, oldCoverage)
            dlg.coverageChanged.connect(self.loadEarthCoverage) #continue here tomorrow
            dlg.exec_()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

    def clearTree(self):
        """
        Clear the configuration tree widget
        """
        self.earthCoverageTreeWidget.invisibleRootItem().takeChildren()

    def loadEarthCoverage(self):
        """
        Loads a previously saved earth coverage configuration
        """
        try:
            self.clearTree()
            data = self.abstractDb.getEarthCoverageDict()
            if not data:
                return
            earthCoverageDict = json.loads(data)
            rootItem = self.earthCoverageTreeWidget.invisibleRootItem()
            #database item
            for key in earthCoverageDict.keys():
                item = QTreeWidgetItem(rootItem)
                item.setText(0,key)
                item.setExpanded(True)
                for cl in earthCoverageDict[key]:
                    covItem = QTreeWidgetItem(item)
                    covItem.setText(1,cl)
                    covItem.setExpanded(True)
        except Exception as e:
            QgsMessageLog.logMessage(self.tr('Earth Coverage not loaded! Check log for details.')+str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)