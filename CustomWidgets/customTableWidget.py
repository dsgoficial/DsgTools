# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-04-07
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customTableWidget.ui'))

class ValidatedItemDelegate(QtGui.QStyledItemDelegate):
    def defineValidatorList(self, validatorList):
        self.validatorList = validatorList

    def createEditor(self, widget, option, index):
        if not index.isValid():
            return 0
        idx = index.column()
        if self.validatorList[idx]:
            editor = QtGui.QLineEdit(widget)
            validator = QtGui.QRegExpValidator(self.validatorList[idx], editor)
            editor.setValidator(validator)
            return editor
        return super(ValidatedItemDelegate, self).createEditor(widget, option, index)

class CustomTableWidget(QtGui.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
    
    def setHeaders(self, headerList):
        for header in headerList:
            currColumn = self.tableWidget.columnCount()
            self.tableWidget.insertColumn(currColumn)
        self.tableWidget.setHorizontalHeaderLabels(headerList)
    
    def setValidator(self, validatorList):
        itemDelegate = ValidatedItemDelegate()
        itemDelegate.defineValidatorList(validatorList)
        self.tableWidget.setItemDelegate(itemDelegate)
    
    @pyqtSlot(bool)
    def on_addPushButton_clicked(self):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(rowCount+1, column, QtGui.QTableWidgetItem(''))
        
    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selected = self.tableWidget.selectedIndexes()
        rowList = [i.row() for i in selected]
        rowList.sort(reverse=True)
        for row in rowList:
            self.tableWidget.removeRow(row)
