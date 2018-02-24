# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtGui import QApplication, QCursor, QMessageBox

from qgis.core import QgsMessageLog

from DsgTools.CustomWidgets.BasicInterfaceWidgets.dsgCustomComboBox import DsgCustomComboBox
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class ConnectionComboBox(DsgCustomComboBox):
    connectionChanged = pyqtSignal()
    dbChanged = pyqtSignal(AbstractDb)
    problemOccurred = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ConnectionComboBox, self).__init__(parent)
        self.parent = parent
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.serverAbstractDb = None
        self.displayDict = {'2.1.3':'EDGV 2.1.3', 'FTer_2a_Ed':'EDGV FTer 2a Ed', 'Non_EDGV':self.tr('Other database model')}
        self.lineEdit().setPlaceholderText(self.tr('Select a database'))
        self.currentIndexChanged.connect(self.loadDatabase)
        self.instantiateAbstractDb = False
    
    def closeDatabase(self):
        try:
            self.abstractDb.db.close()
            del self.abstractDb
            self.abstractDb = None
        except:
            self.abstractDb = None

    def clear(self):
        super(ConnectionComboBox, self).clear()
        self.closeDatabase()
    
    def setServerDb(self, serverAbstractDb):
        self.serverAbstractDb = serverAbstractDb
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            if self.serverAbstractDb:
                dbList = self.serverAbstractDb.getEDGVDbsFromServer(parentWidget = self.parent)
                dbList.sort()
                self.clear()
                self.addItem(self.tr('Select Database'))
                self.addItems(dbList)
            else:
                self.clear()
                self.abstractDb = None
                return
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
        QApplication.restoreOverrideCursor()
    
    def addItems(self, items):
        itemList = []
        if items == []:
            return
        elif isinstance(items[0], tuple) and len(items[0]) == 2:
            for item in items:
                if item[1] not in self.displayDict.keys():
                    version = item[1]
                else:
                    version = self.displayDict[item[1]]
                newText = item[0] + ' ({0})'.format(version)
                itemList.append(newText)
        if itemList == []:
            itemList = items
        super(ConnectionComboBox, self).addItems(itemList)
    
    def currentDb(self):
        if self.currentIndex() == 0:
            return None
        else:
            return self.currentText().split(' (')[0]
                
    def loadDatabase(self):
        """
        Loads the selected database
        """
        try:
            if self.serverAbstractDb and self.currentIndex() > 0:
                if not self.instantiateAbstractDb:
                    self.abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
                    (host, port, user, password) = self.serverAbstractDb.getDatabaseParameters()
                    dbName = self.currentText().split(' (')[0]
                    self.abstractDb.connectDatabaseWithParameters(host, port, dbName, user, password)
                    self.abstractDb.checkAndOpenDb()
                    self.dbChanged.emit(self.abstractDb)
        except Exception as e:
            self.closeDatabase()
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)   