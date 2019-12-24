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
from qgis.PyQt.QtCore import Qt, pyqtSlot, pyqtSignal
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
    # ordering modes
    ORDER_MODE_COUNT = 2
    ASC_ORDER, DESC_ORDER = range(ORDER_MODE_COUNT)

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
        self.setHeaderDoubleClickBehaviour()
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)


    def setHeaders(self, headerMap):
        """
        Sets headers to table and prepare each row for their contents.
        """
        #######################################################################
        # 'headers' attribute is a map that describes each column on table.   #
        # it has a mandatory set of attributes and some are optional (depends #
        # on the cell contents type). It is composed as:                      #
        # {                                                                   #
        #     col (int) : {                                                   #
        #         "header" : "Header for current column as exposed on table", #
        #         "type" : "item" or "widget",                                #
        #         "editable" or "widget" : bool or callable object to a Widget#
        #         "getter" : method for value retrieval or None, if not given #
        #         "setter" : method for value definition or None, if not given#
        #     }                                                               #
        # }                                                                   #
        #######################################################################
        self.clear()
        self.headers = headerMap
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels([
            p["header"] for p in self.headers.values()
        ])

    def replicateColumnValue(self, col):
        """
        Replicates the value from the first cell of a colums based on column 
        filled values.
        :param col: (int) column to have its first value replicated to the
                    other rows.
        """
        prop = self.headers[col]
        if "editable" in prop and not prop["editable"]:
            # ingnores non-editable columns
            return
        for row in range(self.rowCount()):
            if row == 0:
                value = self.getValue(row, col)
            else:
                self.setValue(row, col, value)

    def orderColumn(self, col):
        """
        Orders a colums based on column filled values.
        :param col: (int) column to be ordered.
        """
        if not hasattr(self, "currentRowOrder"):
            self.currentRowOrder = dict()
        if col not in self.currentRowOrder:
            self.currentRowOrder[col] = self.ASC_ORDER
        else:
            # get next mode
            self.currentRowOrder[col] = (self.currentRowOrder[col] + 1) % \
                                        self.ORDER_MODE_COUNT
        contents = []
        for row in range(self.rowCount()):
            contents.append(self.row(row))
        self.clear()
        rev = self.currentRowOrder[col] == self.DESC_ORDER
        for content in sorted(contents, key = lambda i: i[col], reverse=rev):
            self.addRow(content)

    def setHeaderDoubleClickBehaviour(self, mode=None, cols=None):
        """
        Connects header double click signal to the selected callback.
        :param mode: (str) pre-set callback mode (e.g. what will be applied to
                     each column).
        :param cols: (list-of-int) list of columns to which callback behaviour
                     is applied.
        """
        self.unsetHeaderDoubleClickBehaviour()
        self.headerDoubleClicked = {
            "replicate" : self.replicateColumnValue,
            "order" : self.orderColumn,
            "none" : lambda col : None
        }[mode or "none"]
        self.horizontalHeader().sectionDoubleClicked.connect(
            self.headerDoubleClicked
        )

    def unsetHeaderDoubleClickBehaviour(self):
        """
        Disconnects header double click signal to the selected callback.
        :return: (bool) whether behaviour was disconnected.
        """
        try:
            self.horizontalHeader().sectionDoubleClicked.disconnect(
                self.headerDoubleClicked
            )
            return True
        except:
            return False

    def clear(self):
        """
        Resets table to initial state.
        """
        for row in range(self.rowCount()):
            self.tableWidget.removeRow(row)
        self.tableWidget.setRowCount(0)
    
    def getValue(self, row, column):
        """
        Gets the value from a table cell. It uses column definitions from
        headers attribute.
        :param row: (int) target cell's row.
        :param column: (int) target cell's column.
        :return: (*) cell's contents. This might be any of widget's readable
                 inputs (int, float, str, dict, etc) - Depends on defined input
                 widget.
        """
        if self.headers[column]["type"] == "item":
            return self.tableWidget.item(row, column).text()
        else:
            getter = self.headers[column]["getter"]
            widget = self.tableWidget.cellWidget(row, column)
            if not getter:
                raise Exception(
                    self.tr("Getter method must be defined for widget type.")
                )
            return getattr(widget, getter)()

    def setValue(self, row, column, value):
        """
        Sets a value to a table cell. It uses column definitions from headers
        attribute.
        :param row: (int) target cell's row.
        :param column: (int) target cell's column.
        :param value: (*) cell's contents. This might be any of widget's
                      writeable data (int, float, str, dict, etc). Depends on
                      input widget.
        """
        if self.headers[column]['type'] == 'item':
            self.tableWidget.item(row, column).setText(value)
        else:
            setter = self.headers[column]['setter']
            widget = self.tableWidget.cellWidget(row, column)
            if not setter:
                raise Exception(
                    self.tr('Setter method must be defined for widget type.')
                )
            getattr(widget, setter)(value)

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
        for col, properties in self.headers.items():
            if properties["type"] == "item":
                item = QTableWidgetItem()
                # it "flips" current state, which, by default, is "editable"
                if not properties["editable"]:
                    item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(row, col, item)
            else:
                self.tableWidget.setCellWidget(
                    row, col, properties["widget"]()
                )
        self.rowAdded.emit(row)

    def addRow(self, contents, row=None):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        :param contents: (dict) a map to items to be filled.
        """
        row = row if row is not None else self.rowCount()
        self.tableWidget.insertRow(row)
        for col, properties in self.headers.items():
            value = contents[col] if col in contents else None
            if properties["type"] == "item":
                item = QTableWidgetItem(value)
                # it "flips" current state, which, by default, is "editable"
                if not properties["editable"]:
                    item.setFlags(Qt.ItemIsEditable)
                self.tableWidget.setItem(row, col, item)
            else:
                widget = properties["widget"]()
                if value is not None:
                    getattr(widget, properties["setter"])(value)
                self.tableWidget.setCellWidget(row, col, widget)
        self.rowAdded.emit(row)

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
        for col in self.headers:
            contents[col] = self.getValue(row, col)
        return contents

    def itemAt(self, row, col):
        """
        Retrives a cell's item: either a QTableWIdgetItem or current set
        widget.
        :param row: (int) item's row to be read.
        :param col: (int) item's column to be read.
        :return: (QTableWIdgetItem/QWidget) cell contents.
        """
        if row >= self.rowCount() or col >= self.columnCount() \
           or row < 0 or col < 0:
            return None
        if self.headers[col]["type"] == "item":
            return self.tableWidget.item(row, col)
        else:
            return self.tableWidget.cellWidget(row, col)

    def selectedIndexes(self):
        """
        :return: (list-of-QModelIndex) table's selected indexes.
        """
        return self.tableWidget.selectedIndexes()

    def selectedItems(self):
        """
        List of all rows that have selected items on the table.
        :return: (set) selected items (text or widgets).
        """
        items = set()
        for idx in self.selectedIndexes():
            items.add(self.itemAt(idx.row(), idx.column()))
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
            set(i.column() for i in self.selectedIndexes()),
            reverse=reverseOrder
        )

    def selectRow(self, row):
        """
        Clears all selected rows and selects row.
        :param row: (int) index for the row to be select.
        """
        self.clearRowSelection()
        self.addRowToSelection(row)

    def addRowToSelection(self, row):
        """
        Adds a row to selection.
        :param row: (int) index for the row to be added to selection.
        """
        if row not in self.selectedRows():
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
            self.tableWidget.selectRow(row)
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def removeRowFromSelection(self, row):
        """
        Removes a row from selection.
        :param row: (int) index for the row to be removed from selection.
        """
        if row in self.selectedRows():
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
            self.tableWidget.selectRow(row)
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def clearRowSelection(self):
        """
        Removes all selected rows from selection.
        """
        for row in self.selectedRows():
            self.removeRowFromSelection(row)

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
        rows = self.selectedRows()
        if not rows:
            return
        popped = 0
        for row in rows:
            self.removeRow(row - popped)
            popped += 1
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
            self.addNewRow(row)
            self.selectRow(row)
        else:
            self.addRow({})
            self.selectRow(self.rowCount() - 1)

    @pyqtSlot()
    def on_moveUpPushButton_clicked(self):
        """
        Method triggered when move row up button is clicked.
        """
        rows = self.selectedRows()
        if not rows:
            return
        for row in self.selectedRows():
            if row - 1 in rows:
                # rows is a copy of selected rows that is updated after the
                # item is moved
                continue
            self.moveRowUp(row)
            if row != 0:
                # this row is never aftected, hence it is "fixed"
                rows.remove(row)

    @pyqtSlot()
    def on_moveDownPushButton_clicked(self):
        """
        Method triggered when move row down button is clicked.
        """
        rows = self.selectedRows(True)
        if not rows:
            return
        lastRow = self.rowCount() - 1
        for row in self.selectedRows(True):
            if row + 1 in rows:
                continue
            self.moveRowDown(row)
            if row != lastRow:
                rows.remove(row)
    
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
