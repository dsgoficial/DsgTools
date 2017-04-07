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
    
    @pyqtSlot(bool)
    def on_addPushButton_clicked(self):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(rowCount+1, column, QtGui.QTableWidgetItem(""))
        
    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selectedIndexes = self.tableWidget.selectedIndexes()
        
        removeList = []        
        for index in selectedIndexes:
            row = index.row()
            if row not in removeList:
                removeList.append(row)
        removeList.sort(reverse = True)
        for idx in removeList:
            self.tableWidget.removeRow(idx)
