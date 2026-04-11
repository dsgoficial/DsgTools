# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-04
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
from collections import defaultdict
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal

from .....core.Utils.utils import Utils
from .....core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from .....core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.dsgEnums import DsgEnums


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "customServerConnectionWidget.ui")
)


class CustomServerConnectionWidget(QtWidgets.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal()
    resetAll = pyqtSignal()
    dbDictChanged = pyqtSignal(str, list)

    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.utils = Utils()
        self.dbFactory = DbFactory()
        self.factory = SqlGeneratorFactory()
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.populatePostgisSelector)
        self.comboDict = {
            self.tr("Load Database Model EDGV Version 2.1.3"): "2.1.3",
            self.tr("Load Database Model EDGV Version 2.1.3 Pro"): "2.1.3 Pro",
            self.tr("Load Database Model EDGV Version 3.0"): "3.0",
            self.tr("Load Database Model EDGV Version 3.0 Pro"): "3.0 Pro",
            self.tr("Load Database Model EDGV Version FTer_2a_Ed"): "FTer_2a_Ed",
            self.tr("Load Other Database Models"): "Non_EDGV",
        }
        self.dbNameDict = dict()
        self.selectedDbsDict = defaultdict()
        self.postgisCustomSelector.selectionChanged.connect(self.selectedDatabases)

    def selectedDatabases(self, dbList, type):
        """
        Selects databases from a name list and database type
        """
        if type == "added":
            (
                host,
                port,
                user,
                password,
            ) = self.serverWidget.abstractDb.getParamsFromConectedDb()
            for dbNameAlias in dbList:
                if dbNameAlias in list(self.selectedDbsDict.keys()):
                    continue
                if not host or not port or not user:
                    continue
                localDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
                localDb.connectDatabaseWithParameters(
                    host, port, self.dbNameDict[dbNameAlias], user, password
                )
                self.selectedDbsDict[dbNameAlias] = localDb
            self.dbDictChanged.emit("added", dbList)
        if type == "removed":
            for dbNameAlias in list(self.selectedDbsDict.keys()):
                if dbNameAlias in dbList:
                    self.selectedDbsDict.pop(dbNameAlias)
            self.dbDictChanged.emit("removed", dbList)

    def populatePostgisSelector(self):
        """
        Populates the postgis database list according to the database type
        """
        self.dbNameDict = dict()
        dbList = []
        try:
            if self.serverWidget.abstractDb:
                dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer(
                    parentWidget=self
                )
            else:
                self.clearPostgisTab()
                return
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
            self.clearPostgisTab()
        dbList.sort()
        for (dbName, dbversion, dbimplversion) in dbList:
            self.dbNameDict[
                self.getDisplayString(dbName, dbversion, dbimplversion)
            ] = dbName
        self.postgisCustomSelector.setInitialState(self.dbNameDict.keys())

    def getDisplayString(self, dbName, dbversion, dbimplversion):
        if dbversion in ["2.1.3", "3.0", "2.1.3 Pro", "3.0 Pro"]:
            dbversion = f"EDGV {dbversion}"
        if dbversion == "Non_EDGV":
            displayString = dbName + " (" + self.tr("Unknown model") + ")"
        elif dbimplversion == -1:
            displayString = f"{dbName} ({dbversion})"
        else:
            displayString = f"{dbName} ({dbversion} impl. {dbimplversion})"
        return displayString

    def clearPostgisTab(self):
        """
        Clears the postgis tab, returning it to the original state
        """
        self.postgisCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbNameDict = {}
        self.edgvType = None
        self.selectedDbsDict = dict()
        self.resetAll.emit()
