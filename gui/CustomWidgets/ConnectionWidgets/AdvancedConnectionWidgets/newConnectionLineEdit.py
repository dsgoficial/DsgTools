# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-10-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt.QtWidgets import QWidget, QFileDialog
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt import uic
# from qgis.utils import iface
from qgis.core import Qgis, QgsMessageLog

from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.dsgEnums import DsgEnums

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'newConnectionLineEdit.ui'))

class NewConnectionLineEdit(QWidget, FORM_CLASS):
    """
    Class designed to control generic behaviors of a widget able to
    retrieve parameters for a PostGIS database creation.
    """
    # signals to keep 
    connectionChanged = pyqtSignal()
    dbChanged = pyqtSignal(AbstractDb)
    problemOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Class contructor.
        """
        super(NewConnectionLineEdit, self).__init__()
        self.setupUi(self)
        self.viewServers = ViewServers()
        self.fillEdgvVersions()
        self.reset()

    def connectSignals(self):
        """
        Connects all signals.
        """
        self.dsLineEdit.textChanged.connect(self.loadDatabase)
        dsChangedAlias = lambda : self.dbChanged.emit(None)
        self.edgvComboBox.currentIndexChanged.connect(dsChangedAlias)
        self.mQgsProjectionSelectionWidget.crsChanged.connect(dsChangedAlias)

    def fillEdgvVersions(self):
        """
        Populates EDGV combo box with available versions. 
        """
        versions = [
            self.tr("EDGV Version..."),
            "EDGV 2.1.3",
            "EDGV 2.1.3 F Ter",
            "EDGV 2.1.3 Pro",
            "EDGV 3.0",
            "EDGV 3.0 Pro"
        ]
        self.edgvComboBox.addItems(versions)

    def currentDb(self):
        """
        Returns current selected datasource path.
        :return: (str) datasource path.
        """
        ds = self.dsLineEdit.text()
        return ds if not ds is None and ds != self.tr("New Database") else ''

    def edgvVersion(self):
        """
        Returns current selected EDGV version.
        :return: (str) EDGV version.
        """
        edgv = self.edgvComboBox.currentText()
        return edgv if not edgv is None and edgv != self.tr("EDGV Version...") else ''

    def authId(self):
        """
        Returns current selected EDGV version.
        :return: (str) EDGV version.
        """
        crs = self.crs()
        return crs.authid() if not crs is None and crs.isValid() else ''

    def crs(self):
        """
        Returns current selected EDGV version.
        :return: (QgsCoordinateReferenceSystem) current selected CRS.
        """
        crs = self.mQgsProjectionSelectionWidget.crs()
        return crs if not crs is None and crs.isValid() else None

    def reset(self):
        """
        Clears all GUI selections. 
        """
        self.dsLineEdit.setText(self.tr("New Database"))
        self.edgvComboBox.setCurrentIndex(0)
        # self.mQgsProjectionSelectionWidget.setCrs(0)
        self.connectSignals()

    def setAbstractDb(self):
        """
        Updates abstractDb attribute.
        """
        # to be reimplemented into children classes
        self.abstractDb = None

    def serverIsValid(self):
        """
        Checks if connection to server is valid.
        """
        # for files, server check is not necessary
        h = self.viewServers.getDefaultConnectionParameters()[1]
        return self.viewServers.testServer(h)

    def databaseExists(self):
        """
        Checks if database exists.
        """
        _, host, port, user, password = self.viewServers.getDefaultConnectionParameters()
        database = self.currentDb()
        # get a PostGIS database instance to check if database exists
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        return abstractDb.testCredentials(host, port, database, user, password)

    def loadDatabase(self, currentText):
        """
        Loads the selected database
        """
        try:
            if not self.currentDb():
                # in case no datasource was selected
                return
            self.setAbstractDb()
            msg = self.validate()
            self.dbChanged.emit(self.abstractDb)
            self.connectionChanged.emit()
            if msg:
                raise Exception(msg)
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)

    def validate(self):
        """
        Validates current widget. To be validated, it is necessary:
        - a valid datasource selection;
        - a NEW database name;
        - a valid EDGV selection; and
        - a valid CRS selection.
        :return: (str) invalidation reason.
        """
        # check a valid server name
        # check if datasource is a valid name and if it already exists into selected server
        if not self.currentDb() or " " in self.currentDb():
            return self.tr('Invalid datasource (is there a blank space on it?).')
        else:
            # check if the connection is a valid connection
            if not self.serverIsValid():
                return self.tr('Invalid connection to server.')
            # check if it exists
            if self.databaseExists():
                return self.tr('Database {0} already exists into selected server.').format(self.currentDb())
        # check if a valid EDGV version was selected
        if not self.edgvVersion():
            return self.tr('Invalid EDGV version.')
        # check if a valid projection was selected
        if not self.crs() or 'EPSG' not in self.authId():
            return self.tr('Invalid CRS.')
        # if all tests were positive, widget has a valid selection
        return ''

    def isValid(self):
        """
        Validates selection.
        :return: (bool) validation status.
        """
        # return self.validate() == ''
        msg = self.validate()
        # if msg:
        #     # if an invalidation reason was given, warn user and nothing else.
        #     iface.messageBar().pushMessage(self.tr('Warning!'), msg, level=Qgis.Warning, duration=5)
        return msg == ''

    def selectDatasource(self):
        """
        Opens dialog for file/directory selection.
        """
        # model of implementation for reimplementation
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.AnyFile)
        filename, __ = fd.getSaveFileName(caption=self.caption, filter=self.filter)
        if filename:
            self.dsLineEdit.setText(filename)
            print(self.isValid())
        self.loadDatabase(currentText=filename)

    @pyqtSlot(bool)
    def on_serverPushButton_clicked(self):
        self.viewServers.exec_()
