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
from qgis.PyQt.QtWidgets import QWidget, QTableWidgetItem

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
        self.resetTable()
        self.headers = { 
            header : { "col" : col, "type" : headerMap[header] } \
                for col, header in enumerate(headerMap)
        }
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(list(self.headers.keys()))

    def resetTable(self):
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

    def addRow(self, row=None, **contents):
        """
        Adds a new row of items and fill it into table.
        :param row: (int) position to add the new row.
        :param contents: (dict) a map to items to be filled.
        """
        row = row if row is not None else self.rowCount()
        self.tableWidget.insertRow(row)
        for property_, value in contents.items():
            if property_ not in self.headers:
                # ignore properties not present on table
                continue
            if self.headers[property_]["type"] == "item":
                self.tableWidget.addItem(
                    row, self.headers[property_]["col"], QTableWidgetItem(value)
                )
            else:
                self.tableWidget.setCellWidget(
                    row, self.headers[property_]["col"], value
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
        if row >= self.rowCount():
            return {}
        self.tableWidget.insertRow(row)
        contents = dict()
        for row in self.rowCount():
            for header, properties in self.headers.items():
                col = properties["col"]
                if properties["type"] == "item":
                    contents[header] = self.tableWidget.item(row, col).text()
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
        if row >= self.rowCount() or col >= self.columnCount():
            return None
        for header, properties in self.headers.items():
            if col == properties["col"]:
                if properties["type"] == "item":
                    return self.tableWidget.item(row, col).text()
                else:
                    return self.tableWidget.cellWidget(row, col)
