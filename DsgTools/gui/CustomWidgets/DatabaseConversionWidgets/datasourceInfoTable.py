# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt

import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "datasourceInfoTable.ui")
)


class DatasourceInfoTable(QtWidgets.QDialog, FORM_CLASS):
    # create enum to manipulate headers order
    COLUMN_COUNT = 5
    Schema, Layer, GeomCol, GeomType, Srid = list(range(5))

    def __init__(self, contents, parent=None):
        """
        Class constructor.
        :param contents: (list-of-list-of-str) rows contents to be displayed.
        """
        super(DatasourceInfoTable, self).__init__(parent)
        self.setupUi(self)
        self.createTable()
        if contents:
            # if contents were given on initialization, fill table
            self.setTable(contents=contents)

    @pyqtSlot(int)
    def orderByColumn(self, col):
        """
        Displays information as ordered by given column.
        :param col: (int) column index to be used as reference.
        """
        # TO DO
        headers = {
            self.Schema: self.tr("Schema"),
            self.Layer: self.tr("Layer"),
            self.GeomCol: self.tr("Geometry Column"),
            self.GeomType: self.tr("Geometry Type"),
            self.Srid: self.tr("SRID"),
        }
        if col in headers:
            print("Just consider it ordered by {0}, ok?".format(headers[col]))

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        """
        Closes the dialog.
        """
        self.close()

    def createTable(self):
        """
        Creates table. Clears contents if it exists.
        """
        # clear possible content in it
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(row)
        self.tableWidget.setRowCount(0)
        headers = {
            self.Schema: self.tr("Schema"),
            self.Layer: self.tr("Layer"),
            self.GeomCol: self.tr("Geometry Column"),
            self.GeomType: self.tr("Geometry Type"),
            self.Srid: self.tr("SRID"),
        }
        # set column count
        self.tableWidget.setColumnCount(self.COLUMN_COUNT)
        header = self.tableWidget.horizontalHeader()
        # set column names - makes sure the order is defined by enum's order
        self.tableWidget.setHorizontalHeaderLabels(
            [headers[i] for i in range(self.COLUMN_COUNT)]
        )
        # set resize policy for each column
        [
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            for i in range(self.COLUMN_COUNT)
        ]
        # connect header double click signal to order by that column
        header.sectionDoubleClicked.connect(self.orderByColumn)

    def addItem(self, row, col, text):
        """
        Gets an item to be added to the table that may be set to not be editable.
        :param row: (int) row index to be added.
        :param col: (int) column index to be added.
        :param text: (str) name to be exposed on table cell.
        :return: (QTableWidgetItem) item added as to table cell.
        """
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        item.setFlags(Qt.ItemIsEditable)  # not editable
        self.tableWidget.setItem(row, col, item)
        return item

    def addRow(self, row, content):
        """
        Adds a full row provided a dictionary with its contents.
        :param row: (int) row index to be added.
        :param content: (dict) contents to be displayed in the selected row.
        """
        self.addItem(row=row, col=self.Schema, text=content["schema"])
        self.addItem(row=row, col=self.Layer, text=content["layer"])
        self.addItem(row=row, col=self.GeomCol, text=content["geomCol"])
        self.addItem(row=row, col=self.GeomType, text=content["geomType"])
        self.addItem(row=row, col=self.Srid, text=content["srid"])

    def setTable(self, contents):
        """
        Fills table with all given contents.
        :param contents: (list-of-dict) rows contents to be displayed.
        """
        self.tableWidget.setRowCount(len(contents))
        for row, content in enumerate(contents):
            self.addRow(row=row, content=content)
