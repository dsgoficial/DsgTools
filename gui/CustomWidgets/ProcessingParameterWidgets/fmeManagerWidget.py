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
import os, json, requests

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings

from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fmeManagerWidget.ui'))

class FMEManagerWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(FMEManagerWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.workspaceList = []
        self.interfaceDict = {}
        self.server = ''
        self.proxy_dict, self.auth = Utils().get_proxy_config()

    def getCurrentWorkspace(self):
        idx = self.workspaceComboBox.currentIndex()
        return self.workspaceList[idx]
    
    @pyqtSlot(int)
    def on_workspaceComboBox_currentIndexChanged(self):
        self.clearLayout()
        workspace = self.getCurrentWorkspace()
        for parameter in [x for x in workspace['parametros'] if x != 'LOG_FILE']:
            newLabel = QtWidgets.QLabel(parameter)
            self.verticalLayout_2.addWidget(newLabel)
            newLineEdit = QtWidgets.QLineEdit()
            self.interfaceDict[parameter] = newLineEdit
            self.verticalLayout_2.addWidget(newLineEdit)
    
    def clearLayout(self):
        for i in reversed(range(self.verticalLayout_2.count())):
            self.verticalLayout_2.itemAt(i).widget().setParent(None)
    
    @pyqtSlot(bool)
    def on_loadPushButton_clicked(self):
        self.server = self.serverLineEdit.text()
        self.workspaceComboBox.clear()
        url = '{server}/api/rotinas'.format(server=self.server)
        try:
            self.workspaceList = requests.get(
                url,
                proxies=self.proxy_dict,
                auth=self.auth,
                timeout=8
                ).json()['dados']
        except:
            pass
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
        workspace = self.getCurrentWorkspace()
        workspace_id = workspace['id']
        parameters = {'parametros':{key:value.text() for key, value in self.interfaceDict.items()}}
        returnDict = {
            'server':self.server,
            'workspace_id':workspace_id,
            'parameters':parameters,
            'auth' : self.auth,
            'proxy_dict' : self.proxy_dict
        }
        return returnDict