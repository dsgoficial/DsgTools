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
    def __init__(self, iface, db, table):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        self.db = db
        self.table = table

        QObject.connect(self.addRow, SIGNAL(("clicked()")), self.addComplex)
        QObject.connect(self.removeRow, SIGNAL(("clicked()")), self.removeComplex)
        QObject.connect(self.updateButton, SIGNAL(("clicked()")), self.updateTable)
        QObject.connect(self.cancelButton, SIGNAL(("clicked()")), self.cancel)
        
        self.updateTableView()

    def __del__(self):
        if self.db:
            self.db.close()        

    def updateTableView(self):
        ##setting the model in the view
        self.projectModel = QSqlTableModel(None, self.db)
        self.projectModel.setTable(self.table)
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
            
        rowCount = self.projectModel.rowCount()
        table = []
        for i in range(rowCount):
            row = []
            record = self.projectModel.record(i)
            complexNameField = record.field("nome")
            complexIdField = record.field("OGC_FID")
            complexName = complexNameField.value()
            complexId = complexIdField.value()
            className = self.comboBox.currentText()
            row.append(className)
            row.append(complexName)
            row.append(complexId)
            table.append(row)
        
        #Emit the signal to update the complex tree
        self.emit( SIGNAL( "tableUpdated(PyQt_PyObject)" ), table)
            
