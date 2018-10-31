# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
                               (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
                               esperidiao.joao@eb.mil.br
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
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor
from qgis.core import QgsMessageLog, Qgis

from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'databaseFileLineEdit.ui'))

class DatabaseFileLineEdit(QtWidgets.QWidget, FORM_CLASS):
    connectionChanged = pyqtSignal()
    dbChanged = pyqtSignal(AbstractDb)
    problemOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Class constructor.
        :param: (QWidget) widget parent to new DatabaseFileLineEdit instance.
        """
        super(DatabaseFileLineEdit, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.serverAbstractDb = None
        self.displayDict = {'2.1.3':'EDGV 2.1.3', '2.1.3 Pro':'EDGV 2.1.3 Pro', 'FTer_2a_Ed':'EDGV FTer 2a Ed', 'Non_EDGV':self.tr('Other database model'), '3.0':'EDGV 3.0'}
        self.instantiateAbstractDb = False
        self.connectionSelectorLineEdit.lineEdit.setText(self.tr('Select datasource'))

    def closeDatabase(self):
        """
        Unsets any selected database.
        """
        try:
            self.abstractDb.db.close()
            del self.abstractDb
            self.abstractDb = None
        except:
            self.abstractDb = None

    def clear(self):
        """
        Unsets any selected database and clears db directory, if necessary.
        """
        self.connectionSelectorLineEdit.lineEdit.clear()
        self.connectionSelectorLineEdit.lineEdit.setText(self.tr('Select datasource'))
        self.closeDatabase()
    
    def currentDb(self):
        """
        Returns current loaded datasource name, if any.
        :return: (str) current loaded datasource name; an empty string if no ds is selected.
        """
        text = self.connectionSelectorLineEdit.lineEdit.text()
        if text == self.tr('Select datasource'):
            return None
        else:
            dirSplit = '/' if '/' in text else '\\'
            text = text.split(dirSplit)[-1].split('.')[0] if text else ''
            return text
    
    @pyqtSlot(str, name = 'on_lineEdit_textChanged')
    def loadDatabase(self, currentText):
        """
        Loads the selected database
        """
        try:
            if not self.currentDb():
                # in case no datasource was selected
                self.closeDatabase()
            elif not self.instantiateAbstractDb:
                self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
                self.abstractDb.connectDatabase(conn=currentText)
                self.abstractDb.checkAndOpenDb()
                self.dbChanged.emit(self.abstractDb)
                self.connectionChanged.emit()
        except Exception as e:
            self.closeDatabase()
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
    
    @pyqtSlot(bool)
    def on_infoPushButton_clicked(self):
        """
        Exhibits information about selected database.
        """
        pass
