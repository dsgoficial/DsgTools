# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-03
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import (QWidget,
                                 QTableWidgetItem,
                                 QAbstractItemView)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'orderedTableWidget.ui')
)

class OrderedTableWidget(QWidget, FORM_CLASS):
    def __init__(self, parent=None, headerMap=None):
        """
        Class constructor.
        :param headerMap: (dict) a map from each header to be shown and type of
                           cell content (e.g. widget or item).
        :param parent: (QtWidgets.*) any widget parent to current instance.
        """
        super(OrderedTableWidget, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setHeaders(headerMap or {})

    def setHeaders(self, headerMap):
        """
        Sets headers to table and prepare each row for their contents.
        """
        self.clear()
        self.headers = { 
            header : {
                "col" : col,
                "type" : prop["type"],
                "editable" if prop["type"] == "item" else "class" : \
                    prop["editable" if prop["type"] == "item" else "class"]
            } for col, (header, prop) in enumerate(headerMap.items())
        }
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(list(self.headers.keys()))

    def clear(self):
        """
        Resets table to initial state.
        """
        for row in range(self.rowCount()):
            self.tableWidget.removeRow(row)
        self.tableWidget.setRowCount(0)

    def rowCount(self):
        """
        Counting of current rows on table.
        :return: (int) row count.
        """
        return self.tableWidget.rowCount()

    def columnCount(self):
        """
        Counting of current columns on table.
        :return: (int) column count.
        """
        return len(self.headers)

    def addRow(self, contents, row=None):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        :param contents: (dict) a map to items to be filled.
        """
        row = row if row is not None else self.rowCount()
        self.tableWidget.insertRow(row)
        for header, properties in self.headers.items():
            value = contents[header] if header in contents else None
            if properties["type"] == "item":
                item = QTableWidgetItem(value)
                # it "flips" current state, which, by default, is "editable"
                if not properties["editable"]:
                    item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(
                    row, properties["col"], item
                )
            else:
                self.tableWidget.setCellWidget(
                    row, properties["col"], properties["class"]()
                )

    def removeRow(self, row=None):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        :param contents: (dict) a map to items to be filled.
        """
        row = row if row is not None else self.rowCount() - 1
        self.tableWidget.removeRow(row)

    def row(self, row):
        """
        Reads all items from a row.
        :param row: (int) row to be read.
        :return: (dict) a map to row's contents.
        """
        if row >= self.rowCount() or row < 0:
            return {}
        contents = dict()
        for header, properties in self.headers.items():
            col = properties["col"]
            if properties["type"] == "item":
                item = self.tableWidget.item(row, col)
                contents[header] = item.text() if item is not None else None
            else:
                contents[header] = self.tableWidget.cellWidget(row, col)
        return contents

    def item(self, row, col):
        """
        Reads the contents from a table cell.
        :param row: (int) item's row to be read.
        :param col: (int) item's column to be read.
        :return: (str/QWidget) cell contents.
        """
        if row >= self.rowCount() or col >= self.columnCount() \
           or row < 0 or col < 0:
            return None
        for header, properties in self.headers.items():
            if col == properties["col"]:
                if properties["type"] == "item":
                    return self.tableWidget.item(row, col).text()
                else:
                    return self.tableWidget.cellWidget(row, col)

    def selectedItems(self):
        """
        List of all rows that have selected items on the table.
        :return: (list-of-int) selected rows' indexes.
        """
        return self.tableWidget.selectedItems()

    def selectedRows(self, reverseOrder=False):
        """
        List of all rows that have selected items on the table.
        :param reverOrder: (bool) indicates if the row order is reversed.
        :return: (list-of-int) ordered list of selected rows' indexes.
        """
        rows = set()
        for item in self.selectedItems():
            rows.add(item.row())
        return sorted(rows, reverse=reverseOrder)

    def selectedColumns(self, reverseOrder=False):
        """
        List of all columns that have selected items on the table.
        :param reverOrder: (bool) indicates if the column order is reversed.
        :return: (list-of-int) ordered list of selected columns' indexes.
        """
        cols = set()
        for item in self.selectedItems():
            cols.add(item.column())
        return sorted(cols, reverse=reverseOrder)

    def selectRow(self, row):
        """
        Adds a row to selection.
        """
        if row not in self.selectedRows():
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
            self.tableWidget.selectRow(row)
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def moveRowUp(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row == 0:
            return
        self.addRow(self.row(row), row - 1)
        self.removeRow(row + 1)
        self.selectRow(row - 1)

    def moveRowDown(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row == self.rowCount() - 1:
            return
        self.addRow(self.row(row), row + 2)
        self.removeRow(row)
        self.selectRow(row + 1)

    @pyqtSlot()
    def on_removePushButton_clicked(self):
        """
        Method triggered when remove button is clicked.
        """
        rows = self.selectedRows()
        while rows:
            self.removeRow(rows[0])
            rows = self.selectedRows()

    @pyqtSlot()
    def on_addPushButton_clicked(self):
        """
        Method triggered when add button is clicked.
        """
        self.addRow({})
        
    @pyqtSlot()
    def on_moveUpPushButton_clicked(self):
        """
        Method triggered when move row up button is clicked.
        """
        # selected rows method is sorted!
        for row in self.selectedRows():
            if row - 1 in self.selectedRows():
                continue
            self.moveRowUp(row)

    @pyqtSlot()
    def on_moveDownPushButton_clicked(self):
        """
        Method triggered when move row down button is clicked.
        """
        for row in self.selectedRows(True):
            if row + 1 in self.selectedRows():
                continue
            self.moveRowDown(row)
