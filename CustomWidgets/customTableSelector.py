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
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt4.QtGui import QTreeWidgetItem

from DsgTools.Utils.utils import Utils


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customTableSelector.ui'))

class CustomTableSelector(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)

    def __init__(self, customNumber = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.fromLs = []
        self.toLs = []
        self.utils = Utils()
        self.setupUi(self)
    
    def resizeTrees(self):
        self.fromTreeWidget.expandAll()
        self.fromTreeWidget.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.fromTreeWidget.header().setStretchLastSection(False)
        self.toTreeWidget.expandAll()
        self.toTreeWidget.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.toTreeWidget.header().setStretchLastSection(False)
    
    def setTitle(self,title):
        """
        Setting the title
        """
        self.groupBox.setTitle(title)
    
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
    
    def setInitialState(self, fromDictList, unique=False):
        """
        Sets the initial state
        """
        self.fromLs = []
        self.toLs = []
        self.fromTreeWidget.clear()
        self.fromTreeWidget.clear()
        self.setFromDictList(fromDictList, unique)
    
    def getChildNode(self, parentNode, textList):
        """
        Returns child node with columns equals to textList items. If no node is found, return None
        """
        for i in range(parentNode.childCount()):
            nodeFound = True
            childNode = parentNode.child(i)
            for j in range(len(textList)):
                if childNode.text(j) != textList[j]:
                    nodeFound = False
                    break
            if nodeFound:
                return childNode
        return None

    def addItemsToTree(self, treeWidget, addItemDictList, controlList, unique = False):
        """
        Adds items from addItemDictList in treeWidget.
        addItemDictList = [-list of dicts with keys corresponding to header list texts-]
        unique: only adds item if it is not in already in tree
        """
        rootNode = treeWidget.invisibleRootItem() #invisible root item
        for dictItem in addItemDictList:
            firstColumnChild = self.getChildNode(rootNode, [self.headerList[0]]+['']*(len(self.headerList)-1)) #looks for a item in the format ['first column text', '','',...,'']
            if not firstColumnChild:
                firstColumnChild = self.utils.createWidgetItem(rootNode,dictItem[self.headerList[0]],0)
            textList = [dictItem[self.headerList[i]] for i in range(1,len(self.headerList))]
            if unique:
                childNode = self.getChildNode(firstColumnChild, textList)
                if not childNode:
                    self.utils.createWidgetItem(firstColumnChild,textList)
            else:
                self.utils.createWidgetItem(firstColumnChild,textList)
            for text in textList:
                if unique:
                    if text not in controlList:
                        controlList.append(text)
                else:
                    controlList.append(text)
        self.resizeTrees()
    
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


    def setToList(self, toList, unique = True):
        """
        Setting the "to" items (QListWidget and python list)
        """
        self.addItemsToTree(self.toList, toList, self.toLs, unique = unique)
        self.toList.sortItems()

    def setFromList(self, fromList, unique = True):
        """
        Setting the "from" items (QListWidget and python list)
        """
        self.addItemsToTree(self.fromLs, fromList, self.fromLs, unique = unique)
        self.fromList.sortItems()
    
    def getLists(self, sender):
        text = sender.text()
        if text == '>':
            return self.fromTreeWidget, self.fromLs, self.toTreeWidget, self.toLs, False
        if text == '>>':
            return self.fromTreeWidget, self.fromLs, self.toTreeWidget, self.toLs, True
        if text == '<':
            return self.toTreeWidget, self.toLs, self.fromTreeWidget, self.fromLs, False
        if text == '<<':
            return self.toTreeWidget, self.toLs, self.fromTreeWidget, self.fromLs, True

    @pyqtSlot(bool, name='on_pushButtonSelectOne_clicked')
    @pyqtSlot(bool, name='on_pushButtonDeselectOne_clicked')
    @pyqtSlot(bool, name='on_pushButtonSelectAll_clicked')
    @pyqtSlot(bool, name='on_pushButtonDeselectAll_clicked')
    def selectItems(self, isSelected, selectedItems=[]):
        """
        Adds the selected items to the "to" list
        """
        #gets lists
        originTreeWidget, originControlLs, destinationTreeWidget, destinationControlLs, allItems = self.getLists(self.sender())
        #root nodes
        originRoot = originTreeWidget.invisibleRootItem()
        destinationRoot = destinationTreeWidget.invisibleRootItem()
        selectedItemList = []
        self.getSelectedItems(originRoot, selectedItemList)
        for i in range(originRoot.childCount())[::-1]:
            catChild = originRoot.child(i)
            #if son of originRootNode is selected, adds it to destinationRootNode
            moveNode = allItems or (catChild in selectedItemList)
            #get destination parent, creates one in destination if not exists
            destinationCatChild = self.getDestinationNode(destinationRoot, catChild)
            for j in range(catChild.childCount())[::-1]:
                moveChild = (catChild.child(j) in selectedItemList) or moveNode
                self.moveChild(catChild, j, destinationCatChild, moveChild)
            destinationCatChild.sortChildren(1, Qt.AscendingOrder)
            if catChild.childCount() == 0:
                originRoot.takeChild(i)
            destinationRoot.sortChildren(0, Qt.AscendingOrder)
        for i in range(destinationRoot.childCount())[::-1]:
            if destinationRoot.child(i).childCount() == 0:
                destinationRoot.takeChild(i)
        destinationRoot.sortChildren(0, Qt.AscendingOrder)
        self.resizeTrees()

    def getSelectedItems(self, treeWidgetNode, itemList):
        """
        Recursive method to get all selected nodes of treeWidget
        """
        for i in range(treeWidgetNode.childCount()):
            childItem = treeWidgetNode.child(i)
            if childItem.isSelected() and (childItem not in itemList):
                itemList.append(childItem)
            for j in range(childItem.childCount()):
                self.getSelectedItems(childItem, itemList)
    
    def moveChild(self, parentNode, idx, destinationNode, isSelected):
        if isSelected:
            child = parentNode.takeChild(idx)
            destinationNode.addChild(child)
            return True
        else:
            return False

    def getDestinationNode(self, destinationRoot, catChild, returnNew = True):
        """
        Looks for node in destination and returns it. If none is found, creates one and returns it
        """
        #get destination parent, creates one in destination if not exists
        destinationCatChild = None
        for i in range(destinationRoot.childCount()):
            candidate = destinationRoot.child(i)
            if candidate.text(0) == catChild.text(0):
                #if candidate is found, returns candidate
                return candidate
        #if candidate is not found, creates one and returns it
        if returnNew:
            if not destinationCatChild:
                itemTextList = [catChild.text(i) for i in range(catChild.columnCount())]
                return QTreeWidgetItem(destinationRoot,itemTextList)
        else:
            return None
    
    def on_filterLineEdit_textChanged(self, text):
        """
        Filters the items to make it easier to spot and select them
        """
        classes = [edgvClass for edgvClass in self.fromLs if text.lower() in edgvClass.lower()]
        filteredClasses = [i for i in classes if i.lower() not in [j.lower() for j in self.toLs]]
        self.fromList.clear()
        self.fromList.addItems(classes)
        self.fromList.sortItems()