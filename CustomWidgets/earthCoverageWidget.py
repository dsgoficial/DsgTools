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
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'earthCoverageWidget.ui'))

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

    @pyqtSlot(AbstractDb)
    def setDatabase(self, db):
        """
        Sets the database and create validation structure
        """
        self.abstractDb = db
        if db:
            self.loadEarthCoverage()

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        """
        Closes the window
        """
        self.hide()

    def clearTree(self):
        """
        Clear the configuration tree widget
        """
        self.earthCoverageTreeWidget.invisibleRootItem().takeChildren()

    def getEarthCoverageDict(self):
        if self.abstractDb.checkIfExistsConfigTable('EarthCoverage'):
            edgvVersion = self.abstractDb.getDatabaseVersion()
            propertyDict = self.abstractDb.getAllSettingsFromAdminDb('EarthCoverage')
            propertyName = propertyDict[edgvVersion][0]
            dbName = self.abstractDb.db.databaseName()
            self.settingDict = json.loads(self.abstractDb.getSettingFromAdminDb('EarthCoverage', propertyName, edgvVersion))
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
            QgsMessageLog.logMessage(self.tr('Earth Coverage not loaded! Check log for details.')+':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)