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

import os, json

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSlot, pyqtSignal, QItemSelectionModel
from qgis.PyQt.QtWidgets import (QWidget,
                                 QHeaderView,
                                 QTableWidgetItem,
                                 QAbstractItemView)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'orderedTableWidget.ui')
)

class OrderedTableWidget(QWidget, FORM_CLASS):
    rowAdded = pyqtSignal(int)
    rowRemoved = pyqtSignal(int)
    # rowModified = pyqtSignal(int)

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
            col : {
                "name" : header,
                "type" : prop["type"],
                "editable" if prop["type"] == "item" else "class" : \
                    prop["editable" if prop["type"] == "item" else "class"],
                "getter" : prop["getter"] if "getter" in prop else None,
                "setter" : prop["setter"] if "setter" in prop else None
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
    
    def getValue(self, row, column):
        """
        Gets value from row, column item according to type.
        If it is an item type, returns item.text()
        Else, returns the getter funcion applied to the item.
        """
        if self.headers[column]['type'] == 'item':
            return self.tableWidget.item(row, column).text()
        else:
            getter = self.headers[column]['getter']
            widget = self.tableWidget.cellWidget(row, column)
            if not getter:
                raise Exception(self.tr('Getter must be defined for widget type'))
            return getattr(widget, getter)

    def setValue(self, row, column, value):
        """
        Sets value from row, column item according to type.
        If it is an item type, applies item.setText()
        Else, applies the value to the item using the setter function.
        """
        if self.headers[column]['type'] == 'item':
            return self.tableWidget.item(row, column).setText(value)
        else:
            setter = self.headers[column]['setter']
            widget = self.tableWidget.cellWidget(row, column)
            if not setter:
                raise Exception(self.tr('Setter must be defined for widget type'))
            return getattr(widget, setter)(value)

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

    def horizontalHeader(self):
        """
        Retrieves table's horizontal header object
        :return: (QHeaderView) table's horizontal header object.
        """
        return self.tableWidget.horizontalHeader()

    def setSectionResizeMode(self, col, mode):
        """
        Set resizing policy of a column.
        :param col: (int) column index to have its resize policy changed.
        :param mode: (str) resize policy identifier.
        """
        policies = {
            "interactive" : QHeaderView.Interactive,
            "stretch" : QHeaderView.Stretch,
            "fixed" : QHeaderView.Fixed,
            "resizetocontents" : QHeaderView.ResizeToContents,
        }
        if col < 0 or col >= self.rowCount() or mode not in policies:
            return
        header = self.horizontalHeader()
        header.setSectionResizeMode(col, policies[mode])

    def resizeSection(self, col, width):
        """
        Resizes a column width, if resize policy allows.
        :param col: (int) column index to be resized.
        :param width: (width) new column width.
        """
        if col < 0 or col >= self.rowCount():
            return
        self.horizontalHeader().resizeSection(col, width)

    def sectionSize(self, col):
        """
        Retrieves a column's width.
        :param col: (int) column index to be have its width identified.
        :return: (int) column's width
        """
        return self.horizontalHeader().sectionSize(col)

    def addNewRow(self, row=None):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        """
        row = row if row is not None else self.rowCount()
        self.tableWidget.insertRow(row)
        for header, properties in self.headers.items():
            if properties["type"] == "item":
                item = QTableWidgetItem()
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
                    row,
                    properties["col"],
                    value if value is not None else properties["class"]()
                )

    def removeRow(self, row=None):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        :param contents: (dict) a map to items to be filled.
        """
        # row = row if row is not None else self.rowCount() - 1
        self.tableWidget.removeRow(row)
        self.rowRemoved.emit(row)

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

    def itemAt(self, row, col):
        """
        Similiar to item, but returns QTableWIdgetItem instead of its text.
        :param row: (int) item's row to be read.
        :param col: (int) item's column to be read.
        :return: (QTableWIdgetItem/QWidget) cell contents.
        """
        if row >= self.rowCount() or col >= self.columnCount() \
           or row < 0 or col < 0:
            return None
        for header, properties in self.headers.items():
            if col == properties["col"]:
                if properties["type"] == "item":
                    return self.tableWidget.item(row, col)
                else:
                    return self.tableWidget.cellWidget(row, col)

    def selectedIndexes(self):
        """
        :return: (list-of-QModelIndex) table's selected indexes.
        """
        return self.tableWidget.selectionModel().selectedItems()

    def selectedItems(self):
        """
        List of all rows that have selected items on the table.
        :return: (set) selected items (text or widgets).
        """
        items = set()
        for idx in self.selectedIndexes():
            items.add(self.item(idx.row(), idx.column()))
        return items

    def selectedRows(self, reverseOrder=False):
        """
        List of all rows that have selected items on the table.
        :param reverOrder: (bool) indicates if the row order is reversed.
        :return: (list-of-int) ordered list of selected rows' indexes.
        """
        return sorted(
            set(i.row() for i in self.tableWidget.selectionModel().selectedRows()),
            reverse=reverseOrder
        )

    def selectedColumns(self, reverseOrder=False):
        """
        List of all columns that have selected items on the table.
        :param reverOrder: (bool) indicates if the column order is reversed.
        :return: (list-of-int) ordered list of selected columns' indexes.
        """
        return sorted(
            set(i.column() for i in self.tableWidget.selectionModel().selectedColumns()),
            reverse=reverseOrder
        )

    def selectRow(self, row):
        """
        Clears all selected rows and selects row.
        :param row: (int) index for the row to be select.
        """
        self.tableWidget.selectionModel().select(
            self.tableWidget.selectionModel().model().index(row, 0),
            QItemSelectionModel.SelectionFlags(
                QItemSelectionModel.Clear |
                QItemSelectionModel.Select |
                QItemSelectionModel.Current |
                QItemSelectionModel.Rows
            )
        )

    def addRowToSelection(self, row):
        """
        Adds a row to selection.
        :param row: (int) index for the row to be added to selection.
        """
        if row not in self.selectedRows():
            self.tableWidget.selectionModel().select(
                self.tableWidget.selectionModel().model().index(row, 0),
                QItemSelectionModel.SelectionFlags(
                    QItemSelectionModel.Clear |
                    QItemSelectionModel.Select |
                    QItemSelectionModel.Current |
                    QItemSelectionModel.Rows
                )
            )
        self.rowAdded.emit(row)

    def moveRowUp(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row <= 0:
            return
        self.addRow(self.row(row), row - 1)
        self.removeRow(row + 1)
        self.addRowToSelection(row - 1)

    def moveRowDown(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row >= self.rowCount() - 1:
            return
        self.addRow(self.row(row), row + 2)
        self.removeRow(row)
        self.addRowToSelection(row + 1)

    @pyqtSlot()
    def on_removePushButton_clicked(self):
        """
        Method triggered when remove button is clicked.
        """
        if not self.tableWidget.selectionModel().hasSelection():
            return
        self.tableWidget.setUpdatesEnabled(False)
        for row in self.selectedRows():
            self.removeRow(row)
        self.tableWidget.setUpdatesEnabled(True)

    @pyqtSlot()
    def on_addPushButton_clicked(self):
        """
        Method triggered when add button is clicked.
        Adds a row below selected rows or, if no row is selected, adds it as
        last item.
        """
        rows = self.selectedRows()
        if rows:
            row = max(rows) + 1
            self.addRow({}, row)
            self.selectRow(row)
        else:
            self.addRow({})
            self.selectRow(self.rowCount() - 1)
        
    @pyqtSlot()
    def on_moveUpPushButton_clicked(self):
        """
        Method triggered when move row up button is clicked.
        """
        if not self.tableWidget.selectionModel().hasSelection():
            return
        # selected rows method is sorted!
        selected = self.selectedRows()
        for row in selected:
            self.moveRowUp(row)

    @pyqtSlot()
    def on_moveDownPushButton_clicked(self):
        """
        Method triggered when move row down button is clicked.
        """
        if not self.tableWidget.selectionModel().hasSelection():
            return
        selected = self.selectedRows(True)
        for row in selected:
            self.moveRowDown(row)
    
    def exportState(self):
        """
        Exports the state of the interface
        The state of the interface is a dictionary used to populate it.
        """
        for row in self.tab:
            pass

    def importState(self, stateDict):
        """
        Imports the state of the interface
        :param stateDict: dict of the state of the interface. The state
        of the interface is a dictionary used to populate it.
        """
        pass
