# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from qgis.core import QgsMessageLog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_history.ui'))

class ValidationHistory(QtGui.QDialog, FORM_CLASS):
    def __init__(self, postgisDb, parent=None):
        """
        Constructor
        """
        super(ValidationHistory, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.postgisDb = postgisDb
        try:
            self.projectModel = QSqlTableModel(None,self.postgisDb.db)
            self.refreshViewTable()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details. (Did you select a database?)'))
            QgsMessageLog.logMessage(': (did you choose )'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
    
    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        """
        Closes the dialog
        """
        self.hide()

    def keyPressEvent(self, e):
        """
        Refreshes table if F5 is pressed.
        """
        if e.key() == Qt.Key_F5:
            self.refreshViewTable()
            self.getUserName()

    def refreshViewTable(self):
        """
        Refreshes the view table.
        """
        self.postgisDb.createValidationHistoryViewTable() # refreshes the view
        self.projectModel.setTable('validation.process_history_view')
        self.projectModel.select()
        self.tableView.setModel(self.projectModel)
        header = self.tableView.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
    
    def getUserName(self):
        log = self.postgisDb.getValidationLog()
        users = [self.tr("Select a username...")]
        for l in log:
            for line in l.split("\n"):
                if line == self.tr("Database username:"):
                    users.append(l)
        print len(users), list(set(users))
        