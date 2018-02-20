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
        self.dbEncoding = 'utf-8'
        self.dictNoUser = { 'No User' : self.tr("Select a username...") } # text used as indicator of userName box contents
        self.idxManChgd = True # first execution should not raise currentIndexChange
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
            """
            F5 updates the table
            """
            username = self.userFilterComboBox.currentText()
            if username == self.dictNoUser['No User']:
                username=None
            self.refreshViewTable(username=username)
        elif e.key() == Qt.Key_Escape:
            """
            Esc closes the window.
            """
            self.hide()

    def refreshViewTable(self, idListString=None):
        print 1, self.idxManChgd
        """
        Refreshes the view table.
        """
        self.postgisDb.createValidationHistoryViewTable(idListString=idListString) # refreshes the view
        self.projectModel.setTable('validation.process_history_view')
        self.projectModel.select()
        self.tableView.setModel(self.projectModel)
        self.fillUsernameComboBox()
        header = self.tableView.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)

    def getUserProcessbyId(self):
        print 2, self.idxManChgd
        """
        Returns a string containing a list of process ID by username (format: (int)(id_1, id_2, ...)).
        """
        username = self.userFilterComboBox.currentText()
        if username == self.tr("Select a username..."):
            # case no user is specified, no filter should be applied
            return
        ids = "("
        logs, idL = self.postgisDb.getValidationLog(idList=True)
        users = []
        for idx, log in enumerate(logs):
            for line in log.split("\n"):
                # treating the log string as a list of strings (lines) 
                if self.tr("Database username: {0}").format(username).decode(self.dbEncoding) in line.decode(self.dbEncoding):
                    # buiding up the string
                    ids += "{0}, ".format(idL[idx])
        # fixing the string's ending
        ids = (ids + ")").replace(", )", ")")
        return ids

    def getUsernameList(self):
        print 3, self.idxManChgd
        """
        Get the usernames from the log and returns it as a list.
        "Select a username..." is always the first element of this list.
        """
        log = self.postgisDb.getValidationLog()
        log = list(set(log))
        users = []
        # there may be a better way, as the current code iterates over each line for every log
        # present in the database. 
        for l in log:
            for line in l.split("\n"):
                if self.tr("Database username:").decode(self.dbEncoding) in line.decode(self.dbEncoding):
                    # treating the log string as a list of strings (lines) 
                    users.append(line.split(": ")[1])
        # in order to "Select a username..." always be first and the list to only have unique names
        return [self.dictNoUser['No User']] + sorted(list(set(users)))
    
    def fillUsernameComboBox(self):
        print 4, self.idxManChgd
        """
        Loads the username list to the combobox.
        """
        username = self.userFilterComboBox.currentText()
        userList = self.getUsernameList()
        self.userFilterComboBox.clear()
        self.userFilterComboBox.addItems(userList)
        if username and username != self.dictNoUser['No User']:
            # if there's a user already selected it is expected
            # to keep that user selected upon table update.
            idx = max(0, self.userFilterComboBox.findText(username)) # case idx = -1
            self.userFilterComboBox.setCurrentIndex(idx)
            self.idxManChgd = True
        else:
            self.userFilterComboBox.setCurrentIndex(0)
            self.idxManChgd = True

    @pyqtSlot(int)
    def on_userFilterComboBox_currentIndexChanged(self):
        print 5, self.idxManChgd
        """
        Filters the view to only show the process ran by a given User.
        """
        if self.idxManChgd:
            # if the index has been manually changed, no action is required.
            self.idxManChgd = False
            return
        username = self.userFilterComboBox.currentText()
        if username != self.dictNoUser['No User']:
            idListString = self.getUserProcessbyId()
        else:
            idListString = None
        self.refreshViewTable(idListString=idListString)
