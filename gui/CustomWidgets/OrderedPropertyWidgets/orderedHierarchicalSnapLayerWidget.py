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
from builtins import range
from collections import OrderedDict

from qgis.core import QgsProject

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.snapWithLayerChooserWidget import \
    SnapWithLayerChooserWidget
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedStructureWidget import \
    OrderedStructureWidget

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import QSettings, Qt, pyqtSignal, pyqtSlot
from qgis.PyQt.QtWidgets import QTableWidgetItem


class OrderedHierarchicalSnapLayerWidget(OrderedStructureWidget):

    def __init__(self, parent=None):
        """
        Initializates OrderedHierarchicalSnapLayerWidget
        """
        super(OrderedHierarchicalSnapLayerWidget, self).__init__(parent)
        self.args = None
        self.tableWidget.setHorizontalHeaderLabels([self.tr('Snap Order')])
        self.widgetKey = 'snapChooserWidgetList'
    
    def instantiateWidgetItem(self):
        # blackList = self.getBlackList()
        return SnapWithLayerChooserWidget()
    
    def setInitialState(self, layerList):
        self.args = layerList
    
    def getHierarchicalSnapDict(self):
        snapList = self.getParameterDict()[self.widgetKey]
        snapDictList = []
        for i in range(len(snapList)-1):
            snapItemDict = dict()
            snapItemDict['referenceLayer'] = snapList[i]['layer']
            snapItemDict['snap'] = snapList[i]['snap']
            snapItemDict['snapLayerList'] = [i['layer'] for i in snapList[(i+1)::]]
            snapDictList.append(snapItemDict)
        return snapDictList
    
    @pyqtSlot(bool, name = 'on_addRulePushButton_clicked')
    def addItem(self, parameterDict=None):
        """
        1. Use super to instantiate parent's add item
        2. Connect new item's layerComboBox.currentIndexChanged signal to self.componentsRefresher
        """
        row = self.tableWidget.rowCount()
        if row < len(QgsProject.instance().mapLayers()):
            super(OrderedHierarchicalSnapLayerWidget, self).addItem(parameterDict=parameterDict)
            newItemWidget = self.tableWidget.cellWidget(row-1, 0)
            # if newItemWidget is not None:
            #     newItemWidget.layerComboBox.currentIndexChanged.connect(self.componentsRefresher)
            #     newItemWidget.layerComboBox.currentIndexChanged.emit(-1)
    
    @pyqtSlot(bool, name='on_removeRulePushButton_clicked')
    def removeItem(self):
        """
        1. Get selected row
        2. Remove selected row
        3. Update control list
        """
        super(OrderedHierarchicalSnapLayerWidget, self).removeItem()
        # self.componentsRefresher(onDelete=True)
    
    def componentsRefresher(self, onDelete=False):
        """
        1. Get all widgets
        2. Iterate over widgets and build black list from selected texts
        3. Disable all signals
        4. Refresh all combos with remaining values plus selected one
        5. Reconnect signals
        """
        #1. get widgetList and blackList:
        widgetList = []
        blackList = []
        #3. disconect signals
        for idx in range(self.tableWidget.rowCount()):
            widget = self.tableWidget.cellWidget(idx, 0)
            try:
                widget.layerComboBox.layerChanged.disconnect(self.componentsRefresher)
            except:
                pass
            if widget.layerComboBox.currentIndex() > 0:
                blackList += [widget.layerComboBox.currentLayer()]
        #4. refresh combos
        for widget in widgetList:
            widget.refresh(blackList)
        #5. reconnect signals
        for widget in widgetList:
            widget.layerComboBox.layerChanged.connect(self.componentsRefresher)
    
    def getBlackList(self):
        blackList = []
        for i in range(self.tableWidget.rowCount()):
            widget = self.tableWidget.cellWidget(i,0)
            if widget is not None and widget.layerComboBox.currentIndex() > 0:
                blackList.append(widget.layerComboBox.currentLayer())
        return blackList
