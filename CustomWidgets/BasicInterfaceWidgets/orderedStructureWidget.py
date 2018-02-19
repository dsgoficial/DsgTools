# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os, importlib
from collections import deque
# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QTableWidgetItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'orderedStructureWidget.ui'))

class OrderedStructureWidget(QtGui.QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        """
        Initializates OrderedStructureWidget
        """
        super(OrderedStructureWidget, self).__init__(parent)
        self.setupUi(self)
        self.modulePath = None
        self.package = None
        self.args = None
    
    def instantiateWidgetItem(self):
        """
        Must be reimplemented in each child.
        """
        pass
    
    @pyqtSlot(bool)
    def on_addRulePushButton_clicked(self):
        """
        1. Instantiate new line
        2. Add new line in the end
        """
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        widget = self.instantiateWidgetItem()
        self.tableWidget.setCellWidget(rowCount, 0, widget)
    
    @pyqtSlot(bool)
    def on_removeRulePushButton_clicked(self):
        """
        1. Get selected row
        2. Remove selected row
        3. Update control list
        """
        selected = self.tableWidget.selectedIndexes()
        rowList = [i.row() for i in selected]
        rowList.sort(reverse=True)
        for row in rowList:
            self.tableWidget.removeRow(row)

    @pyqtSlot(bool)
    def on_moveRuleUpPushButton_clicked(self):
        pass
    
    @pyqtSlot(bool)
    def on_moveRuleDownPushButton_clicked(self):
        pass