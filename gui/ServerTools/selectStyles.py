# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import PermissionProperties
from DsgTools.gui.ServerTools.createView import CreateView
from DsgTools.gui.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'selectStyles.ui'))

class SelectStyles(QtWidgets.QDialog, FORM_CLASS):
    
    def __init__(self, styleList, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.customSelector.setInitialState(styleList)
        self.customSelector.setTitle(self.tr('Select Styles'))

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.selectedStyles = self.customSelector.toLs
        if len(self.selectedStyles) == 0:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Select at least one style!'))