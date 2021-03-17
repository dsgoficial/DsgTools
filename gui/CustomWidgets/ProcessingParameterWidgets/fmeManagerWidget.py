# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import requests

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings, QSize
from qgis.gui import QgsMessageBar

from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fmeManagerWidget.ui'))


class FMEManagerWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(FMEManagerWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.workspaceList = []
        self.interfaceDict = {}
        self.server = ''
        self.proxy_dict, self.auth = Utils().get_proxy_config()
        self.version = 'v1'
        self.versionComboBox.addItems(['v1', 'v2'])
        self.messabe_bar = QgsMessageBar(self)

    def getCurrentWorkspace(self):
        idx = self.workspaceComboBox.currentIndex()
        try:
            return self.workspaceList[idx]
        except IndexError:
            return None

    @pyqtSlot(int)
    def on_workspaceComboBox_currentIndexChanged(self):
        """
        Fetch necessary parameters from selected workspace and
        insert a QLineEdit for each parameter
        """
        self.clearLayout()
        workspace = self.getCurrentWorkspace()
        try:
            _parameters =  workspace['parameters'] if self.version == 'v1' else workspace['parametros']
            parameters = list(filter(lambda x: x != 'LOG_FILE', _parameters))
        except KeyError:
            parameters = []
        for parameter in parameters:
            newLabel = QtWidgets.QLabel(parameter)
            self.verticalLayout_2.addWidget(newLabel)
            newLineEdit = QtWidgets.QLineEdit()
            self.interfaceDict[parameter] = newLineEdit
            self.verticalLayout_2.addWidget(newLineEdit)

    def clearLayout(self):
        for i in reversed(range(self.verticalLayout_2.count())):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)

    def resizeEvent(self, e):
        """
        Resize QgsMessageBar to widget's width
        """
        self.messabe_bar.resize(
            QSize(
                self.geometry().size().width(),
                30
            )
        )

    @pyqtSlot(bool)
    def on_loadPushButton_clicked(self):
        """
        Sync available workspaces from server and display
        these workspaces on workspaceComboBox
        """
        self.server = self.serverLineEdit.text()
        self.version = self.versionComboBox.currentText()
        self.workspaceComboBox.clear()
        self.workspaceList = []
        if self.version == 'v1':
            url = '{server}/versions?last=true'.format(server=self.server)
            try:
                self.workspaceList = requests.get(
                    url,
                    proxies=self.proxy_dict,
                    auth=self.auth,
                    timeout=8
                ).json()['data']
            except:
                self.messabe_bar.pushMessage(self.tr('Workspaces not found'))
            for workspace in self.workspaceList:
                self.workspaceComboBox.addItem(
                    "{name} ({description})".format(
                        name=workspace['workspace_name'],
                        description=workspace['workspace_description']
                    )
                )
        elif self.version == 'v2':
            url = '{server}/api/rotinas'.format(server=self.server)
            try:
                self.workspaceList = requests.get(
                    url,
                    proxies=self.proxy_dict,
                    auth=self.auth,
                    timeout=8,
                    verify=False
                ).json()['dados']
            except:
                self.messabe_bar.pushMessage(self.tr('Workspaces not found'))
            for workspace in self.workspaceList:
                self.workspaceComboBox.addItem(
                    "{name} ({description})".format(
                        name=workspace['rotina'],
                        description=workspace['descricao']
                    )
                )

    def validate(self):
        """
        Validates fields. Returns True if all information are filled correctly.
        """
        if self.server == '':
            return False
        return True

    def getParameters(self):
        """
        Returns necessary parameters for running the algorithm
        """
        workspace = self.getCurrentWorkspace()
        workspace_id = workspace['id'] if workspace is not None else None
        if self.version == 'v1':
            parameters = {'parameters': {
                key: value.text() for key, value in self.interfaceDict.items()
                }}
        elif self.version == 'v2':
            parameters = {'parametros': {
                key: value.text() for key, value in self.interfaceDict.items()
                }}   
        returnDict = {
            'version': self.version,
            'server': self.server,
            'workspace_id': workspace_id,
            'parameters': parameters,
            'auth': self.auth,
            'proxy_dict': self.proxy_dict
        }
        return returnDict
