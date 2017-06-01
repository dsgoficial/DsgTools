# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-31
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

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customTableSelector.ui'))

class CustomTableSelector(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)

    def __init__(self, customNumber = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.fromLs = []
        self.toLs = []
        self.setupUi(self)
    
    def setFilterColumn(self, customNumber = None):
        if isinstance(customNumber, int):
            self.filterColumnKey = self.headerList[customNumber]
        elif self.headerList:
            self.filterColumnKey = self.headerList[1]
        else:
            self.filterColumnKey = self.headerList[0]
    
    def clearAll(self):
        """
        Clears everything to return to the initial state
        """
        self.fromList.clear()
        self.toList.clear()
        self.filterLineEdit.clear()
    
    def setHeaders(self, headerList, customNumber = None):
        self.headerList = headerList
        self.fromTreeWidget.setHeaderLabels(headerList)
        self.toTreeWidget.setHeaderLabels(headerList)
        self.setFilterColumn(customNumber = customNumber)
    
    def setInitialState(self, fromListDict, unique=False):
        """
        Sets the initial state
        """
        self.fromLs = []
        self.toLs = []
        self.fromTreeWidget.clear()
        self.fromTreeWidget.clear()
        self.setFromDictList(fromDictList, unique)
    
    def getParentNode(self, parentNode, textList):
        nodeFound = True
        for i in range(parentNode.childCount()):
            childNode = parentNode.child(i)
            for j in range(len(textList)):
                if childNode.text(j) != textString[j]:
                    nodeFound = False
                    break
            if nodeFound:
                return childNode
        return None

    def addItemsToTree(self, addItemDictList):
        rootNode = self.treeWidget.invisibleRootItem()
        for dictItem in addItemDictList:
            childNode = self.getParentNode(rootNode, [self.headerList[0],'',''])
            if childNode:
                pass #continue here



        # for idx in range(rootNode.childCount()):
        #     childItem = rootNode.child(idx)
        #     if childItem.text(columnNumber) == targetName:
        # nodeIndex = self.headerList.index(self.filterColumnKey)
        # parentNode = self.utils.findChildNode(rootNode, )
        # self.utils.createWidgetItem(rootNode, key, 0)
        # dbItem = self.utils.createWidgetItem(parentCustomItem, item, 1)
        # self.treeWidget.expandAll()
        # self.treeWidget.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        # self.treeWidget.header().setStretchLastSection(False)

    def addItems(self, addItemDictList, sort = True, unique = False):
        """
        Adding "from" items (QListWidget and python list)
        """
        toAddList = []
        for i in addItemDictList:
            if unique:
                if (i not in self.fromLs) and (i not in self.toLs):
                    toAddList.append(i)
            else:
                toAddList.append(i)
                self.fromLs.append(i)
        if toAddList <> []:
            self.fromList.addItems(toAddList)
            self.fromList.sortItems()
            if sort:
                self.fromLs.sort()
    
    def setFromDictList(self, fromDictList, unique=False):
        """
        Setting the "from" items (QListWidget and python list)
        """
        if unique:
            uniqueList = []
            for i in fromDictList:
                if i not in uniqueList:
                    uniqueList.append(i)
            self.fromLs = uniqueList
            self.fromList.addItems(uniqueList)
            self.fromList.sortItems()
        else:
            self.fromLs = fromDictList
            self.fromLs.sort()
            self.fromList.addItems(fromDictList)
            self.fromList.sortItems()
    
    def addItems(self, addList, unique=False):
        """
        Adding "from" items (QListWidget and python list)
        """
        toAddList = []
        for i in addList:
            if unique:
                if (i not in self.fromLs) and (i not in self.toLs):
                    toAddList.append(i)
            else:
                toAddList.append(i)
                self.fromLs.append(i)
        if toAddList <> []:
            self.fromList.addItems(toAddList)
            self.fromList.sortItems()
            self.fromLs.sort()
    
    def removeItem(self, removeItem):
        """
        Removing items (QListWidget and python list)
        """
        for i in range(self.fromList.__len__()):
            fromItem = self.fromList.item(i)
            if fromItem:
                if fromItem.text() == removeItem:
                    item = self.fromList.takeItem(i)
                    self.fromLs.remove(fromItem.text())
        for i in range(self.toList.__len__()):
            toItem = self.toList.item(i)
            if toItem:
                if toItem.text() == removeItem:
                    self.toLs.remove(toItem.text())
                    item = self.toList.takeItem(i)


    def setToList(self, toList):
        """
        Setting the "to" items (QListWidget and python list)
        """
        self.toLs = toList
        self.toList.addItems(toList)
        self.toList.sortItems()
    
    def setTitle(self,title):
        """
        Setting the title
        """
        self.groupBox.setTitle(title)

    @pyqtSlot(bool, name='on_pushButtonSelectOne_clicked')
    def selectItems(self, isSelected, selectedItems=[]):
        """
        Adds the selected items to the "to" list
        """
        if len(selectedItems) <> 0:
            listedItems = []
            for i in range(self.fromList.__len__()):
                itemToSelect = self.fromList.item(i)
                if itemToSelect.text() in selectedItems:
                    listedItems.append(i)
            listedItems.sort(reverse=True)
        else:
            listedItems = self.fromList.selectedItems()
        added = []
        for i in listedItems:
            if isinstance(i, int):
                item = self.fromList.takeItem(i)
            else:
                item = self.fromList.takeItem(self.fromList.row(i))
            self.toList.addItem(item)
            self.toLs.append(item.text())
            self.fromLs.remove(item.text())
            added.append(item.text())
        self.toList.sortItems()
        #emits added items
        if len(added) > 0:
            self.selectionChanged.emit(added,'added')
        
    @pyqtSlot(bool)
    def on_pushButtonSelectAll_clicked(self):
        """
        Adds all items to the "to" list
        """
        tam = self.fromList.__len__()
        added = []
        for i in range(tam+1,1,-1):
            item = self.fromList.takeItem(i-2)
            self.toList.addItem(item)
            self.toLs.append(item.text())
            added.append(item.text())
            self.fromLs.remove(item.text())
        self.toList.sortItems()
        #emits added items
        if len(added) > 0:
            self.selectionChanged.emit(added,'added')

    @pyqtSlot(bool)
    def on_pushButtonDeselectOne_clicked(self):
        """
        Removes the selected items from the "to" list
        """
        listedItems = self.toList.selectedItems()
        removed = []
        for i in listedItems:
            item = self.toList.takeItem(self.toList.row(i))
            self.fromLs.append(item.text())
            self.toLs.remove(item.text())
            removed.append(item.text())
            self.fromList.addItem(item)
        self.fromList.sortItems()
        #emits removed items
        if len(removed) > 0:
            self.selectionChanged.emit(removed,'removed')

    @pyqtSlot(bool)
    def on_pushButtonDeselectAll_clicked(self):
        """
        Removes all items from the "to" list
        """
        tam = self.toList.__len__()
        removed = []
        for i in range(tam+1,1,-1):
            item = self.toList.takeItem(i-2)
            self.fromLs.append(item.text())
            self.toLs.remove(item.text())
            self.fromList.addItem(item)
            removed.append(item.text())
        self.fromList.sortItems()
        #emits removed items
        if len(removed) > 0:
            self.selectionChanged.emit(removed,'removed')
    
    def on_filterLineEdit_textChanged(self, text):
        """
        Filters the items to make it easier to spot and select them
        """
        classes = [edgvClass for edgvClass in self.fromLs if text.lower() in edgvClass.lower()]
        filteredClasses = [i for i in classes if i.lower() not in [j.lower() for j in self.toLs]]
        self.fromList.clear()
        self.fromList.addItems(classes)
        self.fromList.sortItems()