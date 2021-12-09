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
from requests.exceptions import ReadTimeout, InvalidSchema, ConnectTimeout

from qgis.core import Qgis
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QLabel, QLineEdit
from qgis.PyQt.QtCore import pyqtSlot, QSize
from qgis.gui import QgsMessageBar

from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), "fmeManagerWidget.ui"))


class FMEManagerWidget(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(FMEManagerWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self._workspaceList = list()
        self.paramWidgetMap = dict()
        self.versionComboBox.addItems(["v1", "v2"])
        self.messageBar = QgsMessageBar(self)

    def clearLayout(self):
        """
        Removes all inserted widgets from workspace's parameters from GUI.
        """
        for i in range(self.verticalLayout_2.count()-1, -1, -1):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)

    @pyqtSlot(int)
    def on_workspaceComboBox_currentIndexChanged(self):
        """
        Fetch necessary parameters from selected workspace and insert a
        QLineEdit for each parameter.
        """
        self.clearLayout()
        workspace = self.getCurrentWorkspace()
        key = "parameters" if self.version() == "v1" else "parametros"
        _parameters =  workspace.get(key, list())
        parameters = filter(lambda x: x != "LOG_FILE", _parameters)
        for parameter in parameters:
            newLabel = QLabel(parameter)
            self.verticalLayout_2.addWidget(newLabel)
            newLineEdit = QLineEdit()
            self.paramWidgetMap[parameter] = newLineEdit
            self.verticalLayout_2.addWidget(newLineEdit)

    def resizeEvent(self, e):
        """
        Resize QgsMessageBar to widget's width
        """
        self.messageBar.resize(
            QSize(
                self.geometry().size().width(),
                30
            )
        )

    def getProxyInfo(self):
        """
        Reads Proxy settings as registered on QGIS settings.
        :return: (tuple) the QGIS proxy mapping per schema and its
                 authentication object.
        """
        if self.useProxy():
            return Utils().get_proxy_config()
        else:
            return (None, None)

    def version(self):
        """
        Identifies the selected FME Manager from GUI.
        :return: (str) FME Manager selected version.
        """
        return self.versionComboBox.currentText()

    def server(self):
        """
        Identifies server provided by user from GUI.
        :return: (str) server from which FME routines are read from.
        """
        return self.serverLineEdit.text()

    def useSsl(self):
        """
        Identifies whether user intends to use SSL to request routines from FME
        Manager server.
        :return: (bool) whether SSL is going to be used as from GUI.
        """
        return self.sslCheckBox.isChecked()

    def useProxy(self):
        """
        Identifies whether user intends to connect to FME Manager server behind
        a proxy.
        :return: (bool) whether Proxy is set. Proxy setup is read from
                 QSettings (QGIS settings).
        """
        return self.proxyCheckBox.isChecked()

    def getWorkspacesFromServer(self):
        """
        Reads all available workspaces from a filled server.
        :return: (list-of-dict) list of available workspaces and its metadata.
        """
        useSsl = self.useSsl()
        if self.version() == "v1":
            url = "{server}/versions?last=true".format(server=self.server())
            jsonKey = "data"
        else:
            url = "{server}/api/rotinas".format(server=self.server())
            jsonKey = "dados"
        try:
            if not self.useProxy():
                workspaceList = requests.get(
                    url,
                    verify=useSsl,
                    timeout=15
                ).json()[jsonKey]
            else:
                proxyInfo, proxyAuth = self.getProxyInfo()
                workspaceList = requests.get(
                    url,
                    proxies=proxyInfo,
                    auth=proxyAuth,
                    verify=useSsl,
                    timeout=15
                ).json()[jsonKey]
        except ReadTimeout:
            self.messageBar.pushMessage(
                self.tr("Connection timed out."), level=Qgis.Warning)
            workspaceList = list()
        except ConnectTimeout:
            self.messageBar.pushMessage(
                self.tr("Connection timed out (max attempts)."),
                level=Qgis.Warning
            )
            workspaceList = list()
        except InvalidSchema:
            self.messageBar.pushMessage(
                self.tr("Missing connection schema (e.g.'http', etc)."),
                level=Qgis.Warning
            )
            workspaceList = list()
        except BaseException as e:
            self.messageBar.pushMessage(
                self.tr("Unexpected error while trying to reach server. "
                        "Check your parameters. Error message: {}".format(e)),
                level=Qgis.Warning
            )
            workspaceList = list()
        return workspaceList

    def setWorkspaces(self, workspaces):
        """
        Sets a list of workspaces to the GUI.
        :param workspaces: (list-of-str) 
        """
        self.workspaceComboBox.clear()
        if workspaces:
            self.workspaceComboBox.addItems(workspaces)

    def getCurrentWorkspace(self):
        """
        Reads currently selected workspace from GUI.
        :return: (dict) selected workspace's metadata map.
        """
        idx = self.workspaceComboBox.currentIndex()
        try:
            return self._workspaceList[idx]
        except IndexError:
            return dict()

    @pyqtSlot(bool)
    def on_loadPushButton_clicked(self):
        """
        Sync available workspaces from server and display
        these workspaces on workspaceComboBox
        """
        self.workspaceComboBox.clear()
        self._workspaceList = self.getWorkspacesFromServer()
        if self.version() == "v1":
            workspaceNameKey = "workspace_name"
            workspaceDescKey = "workspace_description"
        else:
            workspaceNameKey = "rotina"
            workspaceDescKey = "descricao"
        for workspace in self._workspaceList:
            self.workspaceComboBox.addItem(
                "{name} ({description})".format(
                    name=workspace[workspaceNameKey],
                    description=workspace[workspaceDescKey]
                )
            )

    def validate(self, pushAlert=False):
        """
        Validates fields. Returns True if all information are filled correctly.
        :param pushAlert: (bool) whether invalidation reason should be
                          displayed on the widget.
        :return: (bool) whether set of filled parameters if valid.
        """
        proxyInfo, _ = self.getProxyInfo()
        if self.useProxy() and not proxyInfo:
            if pushAlert:
                self.messageBar.pushMessage(
                    self.tr("Proxy usage is set but no QGIS proxy settings "
                            "was found."),
                    level=Qgis.Warning
                )
            return False
        if self.server() == "":
            if pushAlert:
                self.messageBar.pushMessage(
                    self.tr("URL to FME Manager server was not provided."),
                    level=Qgis.Warning
                )
            return False
        return True

    def getParameters(self):
        """
        Returns necessary parameters for running the algorithm
        """
        workspace = self.getCurrentWorkspace()
        workspaceId = workspace.get("id", None)
        version = self.version()
        parameters = {
            "parameters" if version == "v1" else "parametros": {
                key: value.text() for key, value in self.paramWidgetMap.items()
            }
        }
        proxyInfo, proxyAuth = self.getProxyInfo()
        return {
            "version": version,
            "server": self.server(),
            "workspace_id": workspaceId,
            "parameters": parameters,
            "auth": proxyAuth,
            "proxy_dict": proxyInfo,
            "use_ssl": self.useSsl(),
            "use_proxy": self.useProxy()
        }
