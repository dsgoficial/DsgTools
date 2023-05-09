# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-09-27
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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QWizard
from fileinput import filename
from DsgTools.core.Utils.utils import Utils

from DsgTools.gui.DatabaseTools.UserTools.PermissionManagerWizard.permissionWizardProfile import (
    PermissionWizardProfile,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "permissionWizard.ui")
)


class PermissionWizard(QtWidgets.QWizard, FORM_CLASS):
    def __init__(self, serverAbstractDb, dbsDict, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.parent = parent
        self.setupUi(self)
        self.serverAbstractDb = serverAbstractDb
        self.userCustomSelector.setTitle(self.tr("Select users to be managed"))
        userList = [i[0] for i in self.serverAbstractDb.getUsersFromServer()]
        self.userCustomSelector.setInitialState(userList)
        self.sequenceDict = {"PermissionWizardProfile": 1}

        self.setPage(
            self.sequenceDict["PermissionWizardProfile"], PermissionWizardProfile()
        )
        # self.setPage(self.sequenceDict['CreateBatchIncrementing'],CreateBatchIncrementing())

    def nextId(self):
        if self.currentId() == 0:
            if len(self.userCustomSelector.toLs) != 0:
                return self.sequenceDict["PermissionWizardProfile"]
            else:
                return -1
        else:
            return self.currentId()
