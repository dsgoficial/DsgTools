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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.core import QgsMessageLog, Qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_history.ui'))

class ValidationHistory(QtWidgets.QDialog, FORM_CLASS):
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
        self.dictNoUser = {
                            'No User' : self.tr("Select a username..."), # no user name is selected
                            'Error' : self.tr("Processes with no user set"), # "username" for processes unable to retrieve db user
                            'User Name Error' : self.tr("Unable to get database username.") # log message raised on username retrieving error
                          } # text used as indicator of userName box contents
        try:
            self.projectModel = QSqlTableModel(None,self.postgisDb.db)
            self.refreshViewTable(createTable=True)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details. (Did you select a database?)'))
            QgsMessageLog.logMessage(': (did you choose )'.join(e.args), "DSGTools Plugin", Qgis.Critical)        
    
    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        """
        Closes the dialog
        """
        self.hide()

    def keyPressEvent(self, e):
        """
        Reimplementation of keyPressEvent() in order to set some Keys behaviour when pressed.
        :param e: keyboard event.
        """
        if e.key() == Qt.Key_F5:
            """
            F5 updates the table
            """
            username = self.userFilterComboBox.currentText()
            if username == self.dictNoUser['No User']:
                username=None
            self.refreshViewTable(createTable=True)
            self.consolidateLogs()
        elif e.key() == Qt.Key_Escape:
            """
            Esc closes the window.
            """
            self.hide()

    def refreshViewTable(self, idListString=None, createTable=False):
        """
        Refreshes the view table.
        :param idListString: ID list string for filtering table.
        :param createTable: boolean that indicates whether table is being created (True) or updated (False).
        """
        if createTable:
            # recreate the consolidated table
            self.consolidateLogs()
            # if table is "fully refreshed", then it is as of re-creating the view
            # instead of updating it.
            self.fillUsernameComboBox(keepSelection=(not createTable))
        self.postgisDb.createValidationHistoryViewTable(idListString=idListString) # refreshes the view
        self.projectModel.setTable('validation.process_history_view')
        self.projectModel.select()
        self.tableView.setModel(self.projectModel)        
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

    def getUsernameList(self):
        """
        Get the usernames from the log and returns it as a list.
        "Select a username..." is always the first element of this list.
        """
        log = self.postgisDb.getValidationLog()
        log = list(set(log)) # to get only unique logs, in order to fasten the for loop
        users = []
        # there may be a better way, as the current code iterates over each line for every log
        # present in the database. 
        for l in log:
            for line in l.split("\n"):
                if self.tr("Database username:").decode(self.dbEncoding) in line.decode(self.dbEncoding):
                    # treating the log string as a list of strings (lines) 
                    users.append(line.split(": ")[1])                    
        # in order to "Select a username..." always be first and the list to only have unique names
        # and for the last item to be processes with username retrieving error 
        return [self.dictNoUser['No User']] + sorted(list(set(users))) + [self.dictNoUser['Error']]

    def getUserProcessbyId(self, username=None):
        """
        Returns a string containing a list of process ID by username (format: (int)(id_1, id_2, ...)).
        :param username: user whose processes are supposed to be shown.
        """
        ids = "("
        logs, idL = self.postgisDb.getValidationLog(idList=True)
        if username == self.dictNoUser['No User']:
            # case no user is specified, no filter should be applied
            return
        elif username == self.dictNoUser['Error']:
            # if username wasn't retrieved, the string pattern in log is different
            for idx, log in enumerate(logs):
                for line in log.split("\n"):
                    # treating the log string as a list of strings (lines) 
                    if self.tr("{0}").format(self.dictNoUser['User Name Error']).decode(self.dbEncoding) in line.decode(self.dbEncoding):
                        # buiding up the string
                        ids += "{0}, ".format(idL[idx])
        else:
            for idx, log in enumerate(logs):
                for line in log.split("\n"):
                    # treating the log string as a list of strings (lines) 
                    if self.tr("Database username: {0}").format(username).decode(self.dbEncoding) in line.decode(self.dbEncoding):
                        # buiding up the string
                        ids += "{0}, ".format(idL[idx])                
        # fixing the string's ending
        ids = (ids + ")").replace(", )", ")")
        if ids == "()":
            # in case there's no id to be filtered
            return "(-9999)"
        return ids
    
    def fillUsernameComboBox(self, keepSelection=False):
        """
        Loads the username list to the combobox.
        :param keepSelection: boolean indicating if selection on comboBox should be kept and 
                              usernames list is not updated.
        """
        username = self.userFilterComboBox.currentText()
        if keepSelection:
            # if there's a user already selected it is expected
            # to keep that user selected upon table update.
            idx = max(0, self.userFilterComboBox.findText(username)) # case idx = -1
            self.userFilterComboBox.setCurrentIndex(idx)
        else:
            userList = self.getUsernameList()
            self.userFilterComboBox.clear()
            self.userFilterComboBox.addItems(userList)
            self.userFilterComboBox.setCurrentIndex(0)
        # in order to indexChanged signal not trigger the repopulating method 
    
    def consolidateLogs(self):
        """
        This method consolidates the log messages of each stage of process into one
        big log message. It keeps the first ID and timestamp of process instance and
        the status of the last instance is conserved. Table validation.compact_process_history
        is created and populated.
        """
        fullHistory = self.postgisDb.getValidationHistory()
        for idx, log in enumerate(fullHistory):
            try:
                sameProcessName = fullHistory[idx-1][1] == fullHistory[idx][1]
            except:
                sameProcessName = False
            if idx == 0:
                # starting loop initiates the compact log list
                compactHistory = [log]
            elif sameProcessName and fullHistory[idx][3] != 3:
                # if it is a continuation of the same process, logs are concatenated
                compactHistory[len(compactHistory) - 1][2] += r"\n" + fullHistory[idx][2]
                compactHistory[len(compactHistory) - 1][3] = fullHistory[idx][3]
            else:
                # if status is "Running", it is a new instance of the same process previously
                compactHistory.append(fullHistory[idx])
        self.postgisDb.createCompactValidationHistory(compactHistory)

    @pyqtSlot(int)
    def on_userFilterComboBox_currentIndexChanged(self):
        """
        Filters the view to only show the process ran by a given User.
        """
        username = self.userFilterComboBox.currentText()
        if username == '':
            # if the index was set on first execution, no action is required.
            return
        username = self.userFilterComboBox.currentText()
        # if no user is specified, list should not be filtered
        if username != self.dictNoUser['No User']:
            idListString = self.getUserProcessbyId(username=username)
        else:
            idListString = None
        self.refreshViewTable(idListString=idListString, createTable=False)
