# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-04-07
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
from builtins import range
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QFileDialog


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "customTableWidget.ui")
)


class ValidatedItemDelegate(QtWidgets.QStyledItemDelegate):
    def defineValidatorList(self, validatorList, maskList=None):
        self.validatorList = validatorList
        if not maskList:
            self.maskList = [None] * len(self.validatorList)
        else:
            self.maskList = maskList

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


class CustomTableWidget(QtWidgets.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()

    def __init__(self, parent=None):
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

    @pyqtSlot(bool, name="on_addPushButton_clicked")
    def addItems(self, itemList=[]):
        if isinstance(itemList, bool):
            oneItemList = ["" for i in range(self.tableWidget.columnCount())]
            self.addOneItem(oneItemList)
        else:
            for item in itemList:
                self.addOneItem(item)

    def addOneItem(self, oneItemList):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        for i in range(len(oneItemList)):
            newItem = QtGui.QTableWidgetItem(oneItemList[i])
            self.tableWidget.setItem(rowCount, i, newItem)

    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selected = self.tableWidget.selectedIndexes()
        rowList = [i.row() for i in selected]
        rowList.sort(reverse=True)
        for row in rowList:
            self.tableWidget.removeRow(row)
            self.validatorList.pop(row)
            self.maskList.pop(row)

    def clearItems(self):
        rowList = list(range(self.tableWidget.rowCount()))
        rowList.sort(reverse=True)
        for row in rowList:
            self.tableWidget.removeRow(row)
