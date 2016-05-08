# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTableWidget, QStyledItemDelegate, QComboBox, QItemDelegate, QDialog, QMessageBox, QListWidget, QListWidgetItem
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry

#DsgTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_setup.ui'))

class CustomTableModel(QTableWidget):
    def __init__(self, domainDict, parent=None, db=QSqlDatabase):
        QTableWidget.__init__(self, parent=parent, db=db)
        self.dict = domainDict
        self.db = db

    def makeValueRelationDict(self, table, codes):
        ret = dict()

        in_clause = '(%s)' % ",".join(map(str, codes))
        if self.db.driverName() == 'QPSQL':
            sql = 'select code, code_name from dominios.%s where code in %s' % (table, in_clause)
        elif self.db.driverName() == 'QSQLITE':
            sql = 'select code, code_name from dominios_%s where code in %s' % (table, in_clause)

        query = QSqlQuery(sql, self.db)
        while query.next():
            code = str(query.value(0))
            code_name = query.value(1)
            ret[code_name] = code

        return ret

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        dbdata = QSqlTableModel.data(self, index, role)
        column = self.headerData(index.column(), Qt.Horizontal)
        if self.dict.has_key(column):
            if isinstance(self.dict[column], dict):
                valueMap = self.dict[column]
                if str(dbdata) in valueMap.values():
                    id = valueMap.values().index(str(dbdata))
                    return valueMap.keys()[id]
            elif isinstance(self.dict[column], tuple):
                tupla = self.dict[column]
                valueMap = self.makeValueRelationDict(tupla[0], tupla[1])
                codes = str(dbdata)[1:-1].split(',')
                code_names = list()
                for c in codes:
                    if str(c) in valueMap.values():
                        id = valueMap.values().index(str(c))
                        code_name = valueMap.keys()[id]
                        code_names.append(code_name)
                if len(code_names) > 0:
                    return '{%s}' % ','.join(code_names)
        return dbdata

    def setData(self, index, value, role=Qt.EditRole):
        column = self.headerData(index.column(), Qt.Horizontal)
        newValue = value
        if self.dict.has_key(column):
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

class ListWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent, itemsDict, column):
        QItemDelegate.__init__(self, parent)
        self.itemsDict = itemsDict
        self.column = column

    def createEditor(self, parent, option, index):
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
        """ load data from model to editor """
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
        """ save data from editor back to model """
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


class FieldSetup(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.setupUi(self)
        
    
    def __del__(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
        
    def getDbInfo(self):
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        elif self.versionCombo.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')

        self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
        if not self.abstractDb:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('A problem occurred! Check log for details.'))
            return
        self.abstractDb.connectDatabase(edgvPath)

        try:
            self.abstractDb.checkAndOpenDb()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
    
    def populateClassList(self):
        self.classListWidget.clear()
        try:
            geomClasses = self.abstractDb.listGeomClassesFromDatabase()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.classListWidget.addItems(geomClasses)
    
    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
        if self.versionCombo.currentIndex() <> 0:
            self.getDbInfo()
            self.populateClassList()
        else:
            self.classListWidget.clear()
    
    @pyqtSlot(int)
    def on_classListWidget_currentRowChanged(self):   
        self.buttonNameLineEdit.setText('')