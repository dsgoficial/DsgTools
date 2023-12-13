# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import range
from copy import deepcopy
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QTreeWidgetItem

from ....core.Utils.utils import Utils


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "customTableSelector.ui")
)


class CustomTableSelector(QtWidgets.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list, str)

    def __init__(self, customNumber=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.fromLs = []
        self.toLs = []
        self.utils = Utils()
        self.setupUi(self)
        self.filterColumnKeyList = [0]

    def resizeTrees(self):
        """
        Expands headers
        """
        self.fromTreeWidget.expandAll()
        self.fromTreeWidget.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.fromTreeWidget.header().setStretchLastSection(False)
        self.toTreeWidget.expandAll()
        self.toTreeWidget.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.toTreeWidget.header().setStretchLastSection(False)

    def sortItems(self, treeWidget):
        """
        Sorts items from input treeWidget
        """
        rootNode = treeWidget.invisibleRootItem()
        rootNode.sortChildren(0, Qt.AscendingOrder)
        for i in range(rootNode.childCount()):
            rootNode.child(i).sortChildren(1, Qt.AscendingOrder)

    def setTitle(self, title):
        """
        Setting the title
        """
        self.groupBox.setTitle(title)

    def setFilterColumn(self, customNumber=None):
        """
        Chooses which column is going to be used in the filter
        """
        if isinstance(customNumber, list):
            self.filterColumnKeyList = deepcopy(customNumber)
        elif isinstance(customNumber, int):
            self.filterColumnKeyList = [customNumber]
        elif self.headerList:
            self.filterColumnKeyList = [1]
        else:
            self.filterColumnKeyList = [0]

    def clearAll(self):
        """
        Clears everything to return to the initial state
        """
        self.filterLineEdit.clear()

    def setHeaders(self, headerList, customNumber=None):
        """
        Sets fromTreeWidget and toTreeWidget headers
        """
        self.headerList = headerList
        self.fromTreeWidget.setHeaderLabels(headerList)
        self.toTreeWidget.setHeaderLabels(headerList)
        self.setFilterColumn(customNumber=customNumber)

    def setInitialState(self, fromDictList, unique=False, selectedDictList=None):
        """
        Sets the initial state
        """
        selectedDictList = [] if selectedDictList is None else selectedDictList
        self.fromLs = []
        self.toLs = []
        self.fromTreeWidget.clear()
        self.fromTreeWidget.clear()
        if not isinstance(fromDictList, int):
            self.addItemsToTree(
                self.fromTreeWidget,
                fromDictList,
                self.fromLs,
                unique=unique,
                selectedDictList=selectedDictList,
            )
            if selectedDictList:
                self.pushButtonSelectOne.clicked.emit()

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

    def addItemsToTree(
        self,
        treeWidget,
        addItemDictList,
        controlList,
        unique=False,
        selectedDictList=None,
    ):
        """
        Adds items from addItemDictList in treeWidget.
        addItemDictList = [-list of dicts with keys corresponding to header list texts-]
        unique: only adds item if it is not in already in tree
        """
        selectedDictList = [] if selectedDictList is None else selectedDictList
        rootNode = treeWidget.invisibleRootItem()  # invisible root item
        for dictItem in addItemDictList:
            firstColumnChild = self.getChildNode(
                rootNode,
                [dictItem[self.headerList[0]]] + [""] * (len(self.headerList) - 1),
            )  # looks for a item in the format ['first column text', '','',...,'']
            if not firstColumnChild:
                firstColumnChild = self.utils.createWidgetItem(
                    rootNode, dictItem[self.headerList[0]], 0
                )
            textList = [
                dictItem[self.headerList[i]] for i in range(len(self.headerList))
            ]
            if not unique:
                item = self.utils.createWidgetItem(firstColumnChild, textList)
                itemList = self.getItemList(item)
                controlList.append(itemList)
                continue
            childNode = self.getChildNode(firstColumnChild, textList)
            if not childNode:
                item = self.utils.createWidgetItem(firstColumnChild, textList)
                if selectedDictList:
                    item.setSelected(True)
                itemList = self.getItemList(item)
                if itemList not in controlList:
                    controlList.append(itemList)
        self.resizeTrees()
        self.sortItems(treeWidget)

    def getItemList(self, item, returnAsDict=False):
        """
        Gets item as a list
        """
        returnItem = dict() if returnAsDict else []
        for i in range(item.columnCount()):
            if returnAsDict:
                returnItem[self.headerList[i]] = item.text(i)
            else:
                returnItem.append(item.text(i))
        return returnItem

    def getLists(self, sender):
        """
        Returns a list composed by (originTreeWidget, --list that controls previous originTreeWidget--, destinationTreeWidget, --list that controls previous destinationTreeWidget--)
        """
        text = sender.text()
        if text == ">":
            return self.fromTreeWidget, self.fromLs, self.toTreeWidget, self.toLs, False
        if text == ">>":
            return self.fromTreeWidget, self.fromLs, self.toTreeWidget, self.toLs, True
        if text == "<":
            return self.toTreeWidget, self.toLs, self.fromTreeWidget, self.fromLs, False
        if text == "<<":
            return self.toTreeWidget, self.toLs, self.fromTreeWidget, self.fromLs, True

    @pyqtSlot(bool, name="on_pushButtonSelectOne_clicked")
    @pyqtSlot(bool, name="on_pushButtonDeselectOne_clicked")
    @pyqtSlot(bool, name="on_pushButtonSelectAll_clicked")
    @pyqtSlot(bool, name="on_pushButtonDeselectAll_clicked")
    def selectItems(self, isSelected, selectedItems=None):
        """
        Adds the selected items to the "to" list
        """
        # gets lists
        selectedItems = [] if selectedItems is None else selectedItems
        (
            originTreeWidget,
            originControlLs,
            destinationTreeWidget,
            destinationControlLs,
            allItems,
        ) = self.getLists(self.sender())
        # root nodes
        originRoot = originTreeWidget.invisibleRootItem()
        destinationRoot = destinationTreeWidget.invisibleRootItem()
        selectedItemList = []
        self.getSelectedItems(originRoot, selectedItemList)
        for i in range(originRoot.childCount())[::-1]:
            catChild = originRoot.child(i)
            # if son of originRootNode is selected, adds it to destinationRootNode
            moveNode = allItems or (catChild in selectedItemList)
            # get destination parent, creates one in destination if not exists
            destinationCatChild = self.getDestinationNode(destinationRoot, catChild)
            for j in range(catChild.childCount())[::-1]:
                nodeChild = catChild.child(j)
                moveChild = (nodeChild in selectedItemList) or moveNode
                if self.moveChild(catChild, j, destinationCatChild, moveChild):
                    itemList = self.getItemList(nodeChild)
                    destinationControlLs.append(itemList)
                    originControlLs.pop(originControlLs.index(itemList))
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
        """
        If node is selected, removes node from parentNode and adds it to destinationNode
        """
        if not isSelected:
            return False
        child = parentNode.takeChild(idx)
        destinationNode.addChild(child)
        return True

    def getDestinationNode(self, destinationRoot, catChild, returnNew=True):
        """
        Looks for node in destination and returns it. If none is found, creates one and returns it
        """
        # get destination parent, creates one in destination if not exists
        destinationCatChild = None
        if isinstance(catChild, list):
            comparisonText = catChild[0]
            if returnNew:
                itemTextList = [catChild[i] for i in range(len(catChild))]
        else:
            comparisonText = catChild.text(0)
            if returnNew:
                itemTextList = [catChild.text(i) for i in range(catChild.columnCount())]

        for i in range(destinationRoot.childCount()):
            candidate = destinationRoot.child(i)
            if candidate.text(0) == comparisonText:
                # if candidate is found, returns candidate
                return candidate
        # if candidate is not found, creates one and returns it
        if returnNew:
            if not destinationCatChild:
                return QTreeWidgetItem(destinationRoot, itemTextList)
        else:
            return None

    def on_filterLineEdit_textChanged(self, text):
        """
        Filters the items to make it easier to spot and select them
        """
        lowerText = text.lower()
        allTuples = [tuple(node[i].lower() for i in self.filterColumnKeyList) for node in self.fromLs]
        itemTupleList = set(
            t for t in allTuples if any(lowerText in i for i in t)
        )
        destinationTupleSet = set(
            tuple(
                node[i].lower() for i in self.filterColumnKeyList for node in self.toLs
            )
        )
        filteredItems = itemTupleList - destinationTupleSet
        if filteredItems == set():
            filteredItems = itemTupleList
        self.filterTree(self.fromTreeWidget, self.fromLs, filteredItems)
        self.resizeTrees()

    def filterTree(self, treeWidget, controlList, filterList):
        """
        Actual filter
        """
        treeWidget.clear()
        rootNode = treeWidget.invisibleRootItem()
        # remove items that are not in filterList
        for item in controlList:
            if tuple(item[i].lower() for i in self.filterColumnKeyList) not in filterList:
                continue
            firstColumnChild = self.getChildNode(
                rootNode, [item[0]] + [""] * (len(item) - 1)
            )  # looks for a item in the format ['first column text', '','',...,'']
            if firstColumnChild is None:
                firstColumnChild = self.utils.createWidgetItem(rootNode, item[0], 0)
            QTreeWidgetItem(firstColumnChild, item)
        rootNode.sortChildren(0, Qt.AscendingOrder)
        for i in range(rootNode.childCount()):
            rootNode.child(i).sortChildren(1, Qt.AscendingOrder)

    def getSelectedNodes(self, concatenated=True):
        """
        Returns a list of selected nodes converted into a string separated by ','
        """
        selected = []
        rootNode = self.toTreeWidget.invisibleRootItem()
        for i in range(rootNode.childCount()):
            catNode = rootNode.child(i)
            for j in range(catNode.childCount()):
                item = catNode.child(j)
                if concatenated:
                    catList = [item.text(i) for i in range(item.columnCount())]
                    selected.append(",".join(catList))
                else:
                    selected.append(item)
        return selected

    def addItemsToWidget(self, itemList, unique=False):
        """
        Adds items to tree that is already built.
        """
        self.addItemsToTree(self.fromTreeWidget, itemList, self.fromLs, unique=unique)

    def removeItemsFromWidget(self, removeList):
        """
        Searches both lists and removes items that are in removeList
        """
        self.removeItemsFromTree(removeList, self.fromTreeWidget, self.fromLs)
        self.removeItemsFromTree(removeList, self.toTreeWidget, self.toLs)

    def removeItemsFromTree(self, dictItemList, treeWidget, controlList):
        """
        Searches treeWidget and removes items that are in removeList and updates controlList
        """
        treeRoot = treeWidget.invisibleRootItem()
        catList = [i[self.headerList[0]] for i in dictItemList]
        returnList = []
        for i in range(treeRoot.childCount())[::-1]:
            catChild = treeRoot.child(i)
            if catChild.text(0) not in catList:
                continue
            for j in range(catChild.childCount())[::-1]:
                nodeChild = catChild.child(j)
                nodeChildDict = self.getItemList(nodeChild, returnAsDict=True)
                nodeChildDict[self.headerList[0]] = catChild.text(0)
                if nodeChildDict not in dictItemList:
                    continue
                catChild.takeChild(j)
                itemList = self.getItemList(nodeChild)
                controlList.pop(controlList.index(itemList))
        for i in range(treeRoot.childCount())[::-1]:
            if treeRoot.child(i).childCount() == 0:
                treeRoot.takeChild(i)
        treeRoot.sortChildren(0, Qt.AscendingOrder)
        for i in range(treeRoot.childCount()):
            treeRoot.child(i).sortChildren(1, Qt.AscendingOrder)
