# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtXml import *

from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

from ui_manageComplex import Ui_Dialog

class ManageComplexDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        self.db = None

        QObject.connect(self.filePushButton, SIGNAL(("clicked()")), self.setFile)
        QObject.connect(self.fileLineEdit, SIGNAL(("editingFinished()")), self.loadDb)
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged (int)"), self.updateTableView)
        
        QObject.connect(self.addRow, SIGNAL(("clicked()")), self.addComplex)
        QObject.connect(self.removeRow, SIGNAL(("clicked()")), self.removeComplex)
        QObject.connect(self.updateButton, SIGNAL(("clicked()")), self.updateTable)
        QObject.connect(self.cancelButton, SIGNAL(("clicked()")), self.cancel)

    def __del__(self):
        if self.db:
            self.db.close()        

    def setFile(self):
        #obtaining the database file name
        fd = QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.fileLineEdit.setText(self.filename)
            
        self.loadDb()

    def loadDb(self):
        #opening the database
        self.filename = self.fileLineEdit.text()
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.filename)
        self.db.open()
        
        self.populateComboBox()

    def populateComboBox(self):
        #getting all complex tables
        self.comboBox.clear()
        
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
        while query.next():
            name = query.value(0)
            if 'Complexo' in name:
                self.comboBox.addItem(query.value(0))        

    def updateTableView(self):
        #table name
        table = self.comboBox.currentText()
        
        ##setting the model in the view
        self.projectModel = QSqlTableModel(None, self.db)
        self.projectModel.setTable(table)
        #manual commit rule
        self.projectModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.projectModel.select()
        
        self.tableView.setModel(self.projectModel)
        self.tableView.show()

    def addComplex(self):
        self.projectModel.insertRow(self.projectModel.rowCount())
        
    def removeComplex(self):
        selectionModel = self.tableView.selectionModel()
        selectedRows = selectionModel.selectedRows()
        for row in selectedRows:
            self.projectModel.removeRow(row.row())

    def cancel(self):
        if self.db:
            self.db.close()
        self.done(0)

    def updateTable(self): 
        #commmiting all pending changes
        if not self.projectModel.submitAll():
            #In case something went wrong we show the message to the user
            QMessageBox.warning(self.iface.mainWindow(), "Error!", self.projectModel.lastError().text())
