# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgManagementToolsDialog
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-08-12
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'batchDbManager.ui'))

class BatchDbManager(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.checkSuperUser)
        self.dbsCustomSelector.setTitle(self.tr('Server Databases'))
        self.dbsCustomSelector.selectionChanged.connect(self.instantiateAbstractDbs)

    def populateListWithDatabasesFromServer(self):
        dbList = []
        try:
            dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])

        dbList.sort()
        dbTextList = []
        for (dbname, dbversion) in dbList:
            dbTextList.append(dbname+' (EDGV v. '+dbversion+')')
        return dbTextList

    def checkSuperUser(self):
        try:
            if self.serverWidget.abstractDb.checkSuperUser():
                dbList = self.populateListWithDatabasesFromServer()
                self.dbsCustomSelector.setInitialState(dbList)
            else:
                QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection refused. Connect with a super user to inspect server.'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])

    def instantiateAbstractDbs(self):
        pass
