 
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-26
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QWidget, QCheckBox, QDialog

from .abstractMultiDsSelectorWidget import AbstractMultiDsSelectorWidget
from DsgTools.gui.CustomWidgets.ConnectionWidgets.ServerConnectionWidgets.exploreServerWidget import ExploreServerWidget
from DsgTools.core.dsgEnums import DsgEnums

import os
from operator import itemgetter

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'multiPostgisSelectorWidget.ui'))

class MultiPostgisSelector(QDialog, FORM_CLASS):
    """
    Class designed to manipulate just the driver selection behavior. Handles reading and inserting data into GUI.
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        """
        super(MultiPostgisSelector, self).__init__(parent)
        self.setupUi(self)
        self.serverName = ''
        self.dbList = []
        self.exploreServerWidget.serversCombo.currentIndexChanged.connect(self.serverUpdated)
        self.updateDbList()
        self.groupBox.setTitle(self.tr('Available Databases'))

    def clearGridLayout(self):
        """
        Clears every added widget to layout.
        """
        for row in range(self.gridLayout.rowCount()):
            for col in range(self.gridLayout.columnCount()):
                item = self.gridLayout.itemAtPosition(row, col)
                if not item is None:
                    widget = item.widget()
                    self.gridLayout.removeWidget(widget)
                    widget.setParent(None)
                    del widget

    def getDbsFromServer(self, name):
        """
        Alias to ExploreServerWidget() synonym method.
        :param name: (str) server name.
        """
        return self.exploreServerWidget.getDbsFromServer(name=name)

    def updateDbList(self):
        """
        Fills 
        """
        # remove all present widgets
        self.clearGridLayout()
        # get selected server
        serverName = self.exploreServerWidget.serversCombo.currentText()
        serverName = serverName.split(' ')[0] if self.exploreServerWidget.serversCombo.currentIndex() != 0 else ''
        # get available databases
        if serverName:
            dbList = self.getDbsFromServer(name=serverName)
        else:
            dbList = []
        if dbList:
            # to order db lists
            dbList.sort(key=itemgetter(0))
            for row, (db, edgvVersion) in enumerate(dbList):
                checkbox = QCheckBox()
                checkbox.setText("{0} (EDGV {1})".format(db, edgvVersion))
                self.gridLayout.addWidget(checkbox, row, 0)

    @pyqtSlot(int)
    def serverUpdated(self):
        """
        Sets GUI behavior when server is selected.
        """
        # clear previous database selection
        self.dbList = []
        # update database list
        self.updateDbList()

    @pyqtSlot(bool)
    def on_clearPushButton_clicked(self):
        """
        Clears all selected databases.
        """
        for row in range(self.gridLayout.rowCount()):
            # get checkbox
            checkbox = self.gridLayout.itemAtPosition(row, 0).widget()
            checkbox.setChecked(False)

    @pyqtSlot(bool)
    def on_selectAllPushButton_clicked(self):
        """
        Selects all databases.
        """
        for row in range(self.gridLayout.rowCount()):
            # get checkbox
            checkbox = self.gridLayout.itemAtPosition(row, 0).widget()
            checkbox.setChecked(True)

    @pyqtSlot(bool)
    def on_togglePushButton_clicked(self):
        """
        Inverts databases database selection.
        """
        for row in range(self.gridLayout.rowCount()):
            # get checkbox
            checkbox = self.gridLayout.itemAtPosition(row, 0).widget()
            checkbox.setChecked(not checkbox.isChecked())

    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        """
        Closes dialog.
        """
        self.close()

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        When ok is clicked, database list should be set.
        """
        # update server name attribute
        self.serverName = self.exploreServerWidget.serversCombo.currentText()
        self.serverName = self.serverName.split(' ')[0] if self.serverName != self.tr('Select Server') else ''
        for row in range(self.gridLayout.rowCount()):
            # get checkbox
            item = self.gridLayout.itemAtPosition(row, 0)
            if item:
                checkbox = self.gridLayout.itemAtPosition(row, 0).widget()
                # update dbList
                if checkbox.isChecked():
                    self.dbList.append(checkbox.text().split(' ')[0].replace('&', '')) # again, no idea why an '&' got in there...
        self.close()

class MultiPostgisSelectorWidget(AbstractMultiDsSelectorWidget):
    """
    Class designed to integrate the datasource selector widget to the abstract multi datasource selector widget.
    Handles data manipulation to be delivered to the next conversion step.
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to new instance.
        """
        super(MultiPostgisSelectorWidget, self).__init__()
        self.source = DsgEnums.PostGIS
        self.selector = self.getWidget(parent=parent)
        self.exploreServerWidget = ExploreServerWidget()

    def getWidget(self, parent=None):
        """
        Parents class reimplementation to retrieve widget.
        :param parent: (QWidget) widget parent to new multi datasource widget.
        """
        return MultiPostgisSelector(parent=parent)

    def getAvailableDb(self, serverName):
        """
        Gets all available DB from a given server.
        :param serverName: (str) server name to be scanned.
        :return: (list-of-str) databases found into selected server.
        """
        return self.exploreServerWidget.getDbsFromServer(name=serverName)

    def getDbServerInfo(self, serverName):
        """
        Gets access information from a selected dabatase.
        :param serverName: (str) server name to have its credentials retrieved.
        :return: (tuple-of-str) host, port, username and password.
        """
        return self.exploreServerWidget.getServerConfiguration(name=serverName)

    def getDbListServerInfo(self, dbList):
        """
        Gets server access information for all database listed in dbList
        :dbList: (list-of-str) database names that server info is required for.
        """
        if not dbList:
            dbList = self.getAvailableDb(serverName=self.selector.serverName)
        serverInfo = self.getDbServerInfo(serverName=self.selector.serverName)
        return { dbname : serverInfo for dbname in dbList }

    def exec_(self):
        """
        Executes selector dialog and updates selected databases, if any database is selected.
        :return: (int) execution code.
        """
        # datasources are cleared once dialog is re-opened
        self.datasources = {}
        # execute selector dialog
        result = self.selector.exec_()
        if not result:
            # if ok was selected on multiselector, check for database selection
            if self.selector.dbList:
                self.datasources = self.getDbListServerInfo(dbList=self.selector.dbList)
            if self.datasources:
                # there was a selection (operation was successful)
                return 0
        # no db was selected
        return 1
