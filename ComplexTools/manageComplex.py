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

from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery,QSqlRecord

from ui_manageComplex import Ui_Dialog
from uuid import uuid4

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'QmlTools'))
from qmlParser import QmlParser

class CustomTableModel(QSqlTableModel):
    def __init__(self, domainDict, parent=None, db=QSqlDatabase):
        QSqlTableModel.__init__(self, parent=parent, db=db)
        self.dict = domainDict

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        code = QSqlTableModel.data(self, index, role)
        column = self.headerData(index.column(), Qt.Horizontal)
        if self.dict.has_key(column):
            dict = self.dict[column]
            if str(code) in dict.values():
                id = dict.values().index(str(code))
                return dict.keys()[id]
        return code

    def setData(self, index, value, role=Qt.EditRole):
        column = self.headerData(index.column(), Qt.Horizontal)
        newValue = value
        if self.dict.has_key(column):
            dict = self.dict[column]
            newValue = int(dict[value])
        return QSqlTableModel.setData(self, index, newValue, role)

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent, itemsDict, column):
        QItemDelegate.__init__(self, parent)
        self.itemsDict = itemsDict
        self.column = column

    def createEditor(self, parent, option, index):
        # special combobox for field type
        if index.column() == self.column:
            cbo = QComboBox(parent)
            for item in self.itemsDict:
                cbo.addItem(item, self.itemsDict[item])
            return cbo
        return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """ load data from model to editor """
        m = index.model()
        try:
            if index.column() == self.column:
                txt = m.data(index, Qt.DisplayRole)
                editor.setEditText(txt)
            else:
                # use default
                QItemDelegate.setEditorData(self, editor, index)
        except:
            pass

    def setModelData(self, editor, model, index):
        """ save data from editor back to model """
        if index.column() == self.column:
            model.setData(index, editor.currentText())
        else:
            # use default
            QItemDelegate.setModelData(self, editor, model, index)

class ManageComplexDialog(QDialog, Ui_Dialog):
    def __init__(self, iface, db, table):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )

        #qgis interface
        self.iface = iface

        #database conenction
        self.db = db
        #table name
        self.table = table
        #rows that are marked for removal
        self.toBeRemoved = []

        #adjusting the table name to match the correspondent qml file
        fileName = table.replace('complexos_', '')
        fileName = fileName.split('.')[-1]+'.qml'

        #obtaining the qml file path
        qmlPath = os.path.join(os.path.dirname(__file__), '..', 'Qmls', 'qmlEDGV30', fileName)
        print qmlPath

        #getting the domain dictionary that will be used to generate the comboboxes
        parser = QmlParser(qmlPath)
        self.domainDict = parser.getDomainDict()

        QObject.connect(self.addRow, SIGNAL(("clicked()")), self.addComplex)
        QObject.connect(self.removeRow, SIGNAL(("clicked()")), self.removeComplex)
        QObject.connect(self.updateButton, SIGNAL(("clicked()")), self.updateTable)
        QObject.connect(self.cancelButton, SIGNAL(("clicked()")), self.cancel)

        self.updateTableView()

    def generateCombos(self):
        self.combos = []
        print self.domainDict
        for key in self.domainDict:
            self.generateCombo(key, self.domainDict[key])

    def generateCombo(self, column, domainValues):
        combo = ComboBoxDelegate(self,domainValues, self.projectModel.fieldIndex(column))
        self.tableView.setItemDelegateForColumn(self.projectModel.fieldIndex(column), combo)

    def updateTableView(self):
        #setting the model in the view
        self.projectModel = CustomTableModel(self.domainDict, None, self.db)
        #adjusting the table
        self.projectModel.setTable(self.table)
        #manual commit rule
        self.projectModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        #selecting all item from the table
        self.projectModel.select()
        #creating the comboboxes to map the domain values
        self.generateCombos()

        #case the first record is null we make some adjustments
        #this is not supposed to happen
        record = self.projectModel.record(0)
        if not record.value("id"):
            record.setValue("id",str(uuid4()))
            record.setValue("nome", "edit this field")
            self.projectModel.setRecord(0, record)

        self.tableView.setModel(self.projectModel)
        self.tableView.show()

    def addComplex(self):
        record = self.projectModel.record()
        #insert a new record with an already determined uuid value
        record.setValue("id",str(uuid4()))
        self.projectModel.insertRecord(self.projectModel.rowCount(), record)

    def removeComplex(self):
        #getting the selected rows
        selectionModel = self.tableView.selectionModel()
        selectedRows = selectionModel.selectedRows()
        for row in selectedRows:
            #storing the complex to be removed
            record = self.projectModel.record(row.row())
            uuid = str(record.value("id"))
            if uuid not in self.toBeRemoved:
                self.toBeRemoved.append(uuid)
            self.projectModel.removeRow(row.row())

    def cancel(self):
        self.done(0)
        
    def checkComplexNameField(self):
        count = self.projectModel.rowCount()
        for i in range(count):
            record = self.projectModel.record(i)
            if record.isNull('nome'):
                QMessageBox.warning(self.iface.mainWindow(), "Warning!", 'The field: \'nome\' must be filled in all rows. Please, check and try again.')
                return False
        return True

    def updateTable(self):
        #checking if the name field is filled
        if not self.checkComplexNameField():
            return
         
        #emit the signal to disassocite all features from the complexes marked for removal
        self.emit(SIGNAL("markedToRemove( PyQt_PyObject )"), self.toBeRemoved)
        #commmiting all pending changes
        if not self.projectModel.submitAll():
            #In case something went wrong we show the message to the user
            QMessageBox.warning(self.iface.mainWindow(), "Error!", self.projectModel.lastError().text())

        #Emit the signal to update the complex tree
        self.emit( SIGNAL( "tableUpdated()" ))
