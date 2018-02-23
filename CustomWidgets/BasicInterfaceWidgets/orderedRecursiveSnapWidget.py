# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-22
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
import os
from collections import OrderedDict
# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QTableWidgetItem

from DsgTools.CustomWidgets.BasicInterfaceWidgets.orderedStructureWidget import OrderedStructureWidget
from DsgTools.CustomWidgets.BasicInterfaceWidgets.snapChooserWidget import SnapChooserWidget

class OrderedRecursiveSnapWidget(OrderedStructureWidget):

    def __init__(self, parent=None):
        """
        Initializates OrderedRecursiveSnapWidget
        """
        super(OrderedRecursiveSnapWidget, self).__init__(parent)
        self.args = None
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Snap Order')])
        self.widgetKey = 'snapChooserWidgetList'
    
    def instantiateWidgetItem(self):
        return SnapChooserWidget(*self.args)
    
    def setInitialState(self, layerList):
        self.args = layerList
    
    def getHierarchicalSnapDict(self):
        snapList = self.getParameterDict()[self.widgetKey]
        snapDictList = []
        for i in range(len(snapList)-1):
            snapItemDict = dict()
            snapItemDict['referenceLayer'] = snapList[i]['layerName']
            snapItemDict['snap'] = snapList[i]['snap']
            snapItemDict['snapLayerList'] = [i['layerName'] for i in snapList[(i+1)::]]
            snapDictList.append(snapItemDict)
        return snapDictList
    
    @pyqtSlot(bool, name = 'on_addRulePushButton_clicked')
    def addItem(self, parameterDict = None):
        """
        1. Use super to instantiate parent's add item
        2. Connect new item's layerComboBox.currentIndexChanged signal to self.componentsRefresher
        """
        super(OrderedRecursiveSnapWidget, self).addItem(parameterDict = parameterDict)
        row = self.tableWidget.rowCount() - 1
        newItemWidget = self.tableWidget.cellWidget(row,0)
        newItemWidget.layerComboBox.currentIndexChanged.connect(self.componentsRefresher)
    
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
    
    def componentsRefresher(self):
        """
        1. Get all widgets
        2. Disable all signals
        3. Iterate over widgets and build black list from selected texts
        4. Refresh all combos with remaining values plus selected one
        5. Reconnect signals
        """
        #1. get widgetList:
        widgetList = [self.tableWidget.cellWidget(i,0) for i in range(self.tableWidget.rowCount())]
        #2. disconect signals
        for widget in widgetList:
            try:
                widget.layerComboBox.currentIndexChanged.disconnect(self.componentsRefresher)
            except:
                pass
        #3. build black list
        blackList = []
        for widget in widgetList:
            selectedText = widget.getSelectedItem()
            if selectedText:
                if selectedText not in blackList:
                    blackList.append(selectedText)
        newList = [i for i in self.args[0] if i not in blackList]
        #4. refresh combos
        for widget in widgetList:
            if widget.layerComboBox != self.sender():
                widget.refresh(newList)
        #5. reconnect signals
        for widget in widgetList:
            widget.layerComboBox.currentIndexChanged.connect(self.componentsRefresher)
        
