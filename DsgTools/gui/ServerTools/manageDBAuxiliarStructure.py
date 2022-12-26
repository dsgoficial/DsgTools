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

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import (
    PermissionProperties,
)
from DsgTools.gui.ServerTools.createView import CreateView

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "manageDBAuxiliarStructure.ui")
)


class ManageDBAuxiliarStructure(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDb = abstractDb

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        self.done(0)
