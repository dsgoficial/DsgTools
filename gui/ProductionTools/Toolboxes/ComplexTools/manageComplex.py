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
from builtins import map
from builtins import str
from builtins import range
import os
from uuid import uuid4

from qgis.core import QgsMessageLog

# Import the PyQt and QGIS libraries
from qgis.PyQt import uic, QtGui, QtCore
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QStyledItemDelegate, QComboBox, QItemDelegate, QDialog, QMessageBox, QListWidget, QListWidgetItem
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

#DsgTools imports
from DsgTools.QmlTools.qmlParser import QmlParser
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_manageComplex.ui'))

class CustomTableModel(QSqlTableModel):
    def __init__(self, domainDict, parent=None, db=QSqlDatabase):
        """
        Constructor
        """
        QSqlTableModel.__init__(self, parent=parent, db=db)
        self.dict = domainDict
        self.db = db

    def makeValueRelationDict(self, table, codes):
        """
        Makes the value relation dictionary. It is necessary for multi valued attributes
        """
        ret = dict()

        in_clause = '(%s)' % ",".join(map(str, codes))
        if self.db.driverName() == 'QPSQL':
            sql = 'select code, code_name from dominios.%s where code in %s' % (table, in_clause)
        elif self.db.driverName() == 'QSQLITE':
            sql = 'select code, code_name from dominios_%s where code in %s' % (table, in_clause)

        query = QSqlQuery(sql, self.db)
        while next(query):
            code = str(query.value(0))
            code_name = query.value(1)
            ret[code_name] = code

        return ret

    def flags(self, index):
        """
        Gets index flags
        """
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """
        Custom reimplementation of the method data.
        It is necessary to work with value map and value relation.
        index: column index
        role: role used to get the data
        """
        dbdata = QSqlTableModel.data(self, index, role)
        column = self.headerData(index.column(), Qt.Horizontal)
        if column in self.dict:
            if isinstance(self.dict[column], dict):
                valueMap = self.dict[column]
                if str(dbdata) in list(valueMap.values()):
                    id = list(valueMap.values()).index(str(dbdata))
                    return list(valueMap.keys())[id]
            elif isinstance(self.dict[column], tuple):
                tupla = self.dict[column]
                valueMap = self.makeValueRelationDict(tupla[0], tupla[1])
                codes = str(dbdata)[1:-1].split(',')
                code_names = list()
                for c in codes:
                    if str(c) in list(valueMap.values()):
                        id = list(valueMap.values()).index(str(c))
                        code_name = list(valueMap.keys())[id]
                        code_names.append(code_name)
                if len(code_names) > 0:
                    return '{%s}' % ','.join(code_names)
        return dbdata

    def setData(self, index, value, role=Qt.EditRole):
        """
        Custom reimplementation of the method setData.
        It is necessary to work with value map and value relation.
        index: column index to be set
        value: value to be set
        role: role used
        """
        column = self.headerData(index.column(), Qt.Horizontal)
        newValue = value
        if column in self.dict:
            if isinstance(self.dict[column], dict):
                valueMap = self.dict[column]
                newValue = int(valueMap[value])
            elif isinstance(self.dict[column], tuple):
                tupla = self.dict[column]
                valueMap = self.makeValueRelationDict(tupla[0], tupla[1])
                code_names = value[1:-1].split(',')
                codes = []
                for code_name in code_names:
                    code = valueMap[code_name]
                    codes.append(code)
                if len(codes) > 0:
                    newValue = '{%s}' % ','.join(map(str, codes))
        return QSqlTableModel.setData(self, index, newValue, role)

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent, itemsDict, column):
        """
        Constructor
        """
        QItemDelegate.__init__(self, parent)
        self.itemsDict = itemsDict
        self.column = column

    def createEditor(self, parent, option, index):
        """
        Creates a custom editor to edit value map data
        """
        # special combobox for field type
        if index.column() == self.column:
            cbo = QComboBox(parent)
            for item in self.itemsDict:
                cbo.addItem(item, self.itemsDict[item])
            return cbo
        return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """
        load data from model to editor
        """
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
        """
        save data from editor back to model
        """
        if index.column() == self.column:
            model.setData(index, editor.currentText())
        else:
            # use default
            QItemDelegate.setModelData(self, editor, model, index)

class ListWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent, itemsDict, column):
        """
        Constructor
        """
        QItemDelegate.__init__(self, parent)
        self.itemsDict = itemsDict
        self.column = column

    def createEditor(self, parent, option, index):
        """
        Creates a custom editor to edit value relation data
        """
        # special combobox for field type
        if index.column() == self.column:
            list = QListWidget(parent)
            for item in self.itemsDict:
                listItem = QListWidgetItem(item)
                listItem.setCheckState(Qt.Unchecked)
                list.addItem(listItem)
            return list
        return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """
        load data from model to editor
        """
        m = index.model()
        try:
            if index.column() == self.column:
                txt = m.data(index, Qt.DisplayRole)
                checkList = txt[1:-1].split(',')
                for i in range(editor.count()):
                    item = editor.item(i)
                    item.setCheckState(Qt.Checked if item.text() in checkList else Qt.Unchecked)
            else:
                # use default
                QItemDelegate.setEditorData(self, editor, index)
        except:
            pass

    def setModelData(self, editor, model, index):
        """
        save data from editor back to model
        """
        if index.column() == self.column:
            checkedItems = []
            for i in range(editor.count()):
                item = editor.item(i)
                if item.checkState() == Qt.Checked:
                    checkedItems.append(item.text())
            model.setData(index, '{%s}' % ','.join(checkedItems))
        else:
            # use default
            QItemDelegate.setModelData(self, editor, model, index)

class ManageComplexDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, abstractDb, table):
        """
        Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )

        #qgis interface
        self.iface = iface

        #database conenction
        if not abstractDb:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), self.tr('Select a database before managing a complex!'))
            return
        self.db = abstractDb.db
        #table name
        self.table = table
        #rows that are marked for removal
        self.toBeRemoved = []

        #adjusting the table name to match the correspondent qml file
        fileName = table.replace('complexos_', '')
        fileName = fileName.split('.')[-1]+'.qml'

        #obtaining the qml file path
        qmlDirPath = ''
        try:
            qmlDirPath = abstractDb.getQmlDir()
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
        qmlPath = os.path.join(qmlDirPath, fileName)

        #getting the domain dictionary that will be used to generate the comboboxes
        try:
            parser = QmlParser(qmlPath)
            self.domainDict = parser.getDomainDict()
        except:
            self.domainDict = dict()
            pass
        
        self.addRow.clicked.connect(self.addComplex)
        self.removeRow.clicked.connect(self.removeComplex)
        self.updateButton.clicked.connect(self.updateTable)
        self.cancelButton.clicked.connect(self.cancel)

        self.updateTableView()

    def generateDelegates(self):
        """
        Generates the custom delegates.
        It can be a combo box delegate or a list widget delegate
        """
        for key in self.domainDict:
            if isinstance(self.domainDict[key], dict):
                #self.domainDict[key] in this case is a dict
                self.generateCombo(key, self.domainDict[key])
            elif isinstance(self.domainDict[key], tuple):
                #self.domainDict[key] in this case is a tuple where index 0 is the domain table and index 1 are the codes
                self.generateList(key, self.domainDict[key])

    def generateCombo(self, column, domainValues):
        """
        Generates a combo box delegate
        """
        #creating the delegate
        combo = ComboBoxDelegate(self, domainValues, self.projectModel.fieldIndex(column))
        self.tableView.setItemDelegateForColumn(self.projectModel.fieldIndex(column), combo)

    def generateList(self, column, tupla):
        """
        Generates a lit widget delegate
        """
        #making a dict in the same way used for the Combobox delegate
        valueRelation = self.makeValueRelationDict(tupla[0], tupla[1])
        #creating the delagate
        list = ListWidgetDelegate(self, valueRelation, self.projectModel.fieldIndex(column))
        self.tableView.setItemDelegateForColumn(self.projectModel.fieldIndex(column), list)

    def makeValueRelationDict(self, table, codes):
        """
        Makes the value relation dictionary
        """
        #query to obtain the dict with code names and related codes
        ret = dict()

        in_clause = '(%s)' % ",".join(map(str, codes))
        if self.db.driverName() == 'QPSQL':
            sql = 'select code, code_name from dominios.%s where code in %s' % (table, in_clause)
        elif self.db.driverName() == 'QSQLITE':
            sql = 'select code, code_name from dominios_%s where code in %s' % (table, in_clause)

        query = QSqlQuery(sql, self.db)
        while next(query):
            code = query.value(0)
            code_name = query.value(1)
            ret[code_name] = code

        return ret

    def updateTableView(self):
        """
        Updates the table view
        """
        #setting the model in the view
        self.projectModel = CustomTableModel(self.domainDict, None, self.db)
        #adjusting the table
        self.projectModel.setTable(self.table)
        #manual commit rule
        self.projectModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        #selecting all item from the table
        self.projectModel.select()
        #creating the comboboxes and listwidgets to map the domain values
        self.generateDelegates()

        #case the first record is null we make some adjustments
        #this is not supposed to happen
        record = self.projectModel.record(0)
        if not record.value("id"):
            adjustedRecord = self.adjustRecord(record)
            self.projectModel.setRecord(0, adjustedRecord)

        self.tableView.setModel(self.projectModel)

        #Hiding columns that point to other complexes so that the user can't change them
        for i in range(self.projectModel.columnCount()):
            columnName = self.projectModel.headerData(i, Qt.Horizontal)
            if 'id_' in columnName:
                self.tableView.hideColumn(i)

        self.tableView.show()

    def addComplex(self):
        """
        Adds a new complex to the table
        """
        record = self.projectModel.record()
        adjustedRecord = self.adjustRecord(record)
        self.projectModel.insertRecord(self.projectModel.rowCount(), adjustedRecord)

    def adjustRecord(self,record):
        """
        Updates a existing record
        """
        #insert a new record with an already determined uuid value
        record.setValue("id",str(uuid4()))
        record.setValue("nome", self.tr("edit this field"))
        for i in range(self.projectModel.columnCount()):
            columnName = self.projectModel.headerData(i, Qt.Horizontal)
            if columnName in self.domainDict:
                record.setValue(columnName, self.tr("edit this field"))
        return record

    def removeComplex(self):
        """
        Removes a complex from the complex table
        """
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
        """
        Closes the dialog
        """
        self.done(0)

    def checkComplexNameField(self):
        """
        Checks the complex name field before recording it.
        """
        count = self.projectModel.rowCount()
        for i in range(count):
            record = self.projectModel.record(i)
            if record.isNull('nome'):
                QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr('The field: \'nome\' must be filled in all rows. Please, check and try again.'))
                return False
        return True

    def updateTable(self):
        """
        Updates the complex table
        """
        #checking if the name field is filled
        #Now the database checks the field "nome", therefore the method checkComplexNameField() is no longer needed

        #emit the signal to disassocite all features from the complexes marked for removal
        self.markedToRemove.emit(self.toBeRemoved)
        #commmiting all pending changes
        if not self.projectModel.submitAll():
            #In case something went wrong we show the message to the user
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Error!"), self.projectModel.lastError().text())

        #Emit the signal to update the complex tree
        self.tableUpdated.emit()