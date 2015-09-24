# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-14
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.create_profile import CreateProfile

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'remove_profiles.ui'))

class RemoveProfiles(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(RemoveProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(0, False)
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(False)
        self.utils = Utils()
        
        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.getProfiles)
        
        self.getProfiles()
             
    def getProfiles(self):
        self.listWidget.clear()
        
        if not self.widget.db:
            return
        
        ret = []

        sql = self.gen.getRoles()
        query = QSqlQuery(sql, self.widget.db)

        while query.next():
            ret.append(query.value(0))

        ret.sort()
        self.listWidget.addItems(ret)

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        for item in self.listWidget.selectedItems():
            role = item.text()

            sql = self.gen.dropRole(role)
            split = sql.split('#')
            query = QSqlQuery(self.widget.db)

            for inner in split:
                if not query.exec_(inner):
                    QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem removing profile: ') +role+'\n'+query.lastError().text())
                    return
            
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profiles removed successfully!'))
                    