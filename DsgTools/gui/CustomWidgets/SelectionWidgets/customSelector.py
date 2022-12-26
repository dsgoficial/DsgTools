# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "customSelector.ui")
)


class CustomSelector(QtWidgets.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list, str)

    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.fromLs = []
        self.toLs = []
        self.setupUi(self)

    def clearAll(self):
        """
        Clears everything to return to the initial state
        """
        self.fromLs = []
        self.toLs = []
        self.fromList.clear()
        self.toList.clear()
        self.filterLineEdit.clear()

    def setInitialState(self, fromList, unique=False):
        """
        Sets the initial state
        """
        self.clearAll()
        if not isinstance(fromList, int):
            self.setFromList(fromList, unique)

    def setFromList(self, fromList, unique=False):
        """
        Setting the "from" items (QListWidget and python list)
        """
        fromList = list(fromList)
        if unique:
            self.fromLs = list(set(fromList))
            self.fromList.addItems(self.fromLs)
            self.fromList.sortItems()
        else:
            self.fromLs = fromList
            self.fromLs.sort()
            self.fromList.addItems(fromList)
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
        if toAddList != []:
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
        self.toLs = list(toList)
        self.toList.addItems(self.toLs)
        self.toList.sortItems()

    def setTitle(self, title):
        """
        Setting the title
        """
        self.groupBox.setTitle(title)

    @pyqtSlot(bool, name="on_pushButtonSelectOne_clicked")
    def selectItems(self, isSelected, selectedItems=None):
        """
        Adds the selected items to the "to" list
        """
        selectedItems = [] if selectedItems is None else selectedItems
        if len(selectedItems) != 0:
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
        # emits added items
        if len(added) > 0:
            self.selectionChanged.emit(added, "added")

    @pyqtSlot(bool)
    def on_pushButtonSelectAll_clicked(self):
        """
        Adds all items to the "to" list
        """
        tam = self.fromList.__len__()
        added = []
        for i in range(tam + 1, 1, -1):
            item = self.fromList.takeItem(i - 2)
            self.toList.addItem(item)
            self.toLs.append(item.text())
            added.append(item.text())
            self.fromLs.remove(item.text())
        self.toList.sortItems()
        # emits added items
        if len(added) > 0:
            self.selectionChanged.emit(added, "added")

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
        # emits removed items
        if len(removed) > 0:
            self.selectionChanged.emit(removed, "removed")

    @pyqtSlot(bool)
    def on_pushButtonDeselectAll_clicked(self):
        """
        Removes all items from the "to" list
        """
        tam = self.toList.__len__()
        removed = []
        for i in range(tam + 1, 1, -1):
            item = self.toList.takeItem(i - 2)
            self.fromLs.append(item.text())
            self.toLs.remove(item.text())
            self.fromList.addItem(item)
            removed.append(item.text())
        self.fromList.sortItems()
        # emits removed items
        if len(removed) > 0:
            self.selectionChanged.emit(removed, "removed")

    def on_filterLineEdit_textChanged(self, text):
        """
        Filters the items to make it easier to spot and select them
        """
        classes = [
            edgvClass for edgvClass in self.fromLs if text.lower() in edgvClass.lower()
        ]
        filteredClasses = [
            i for i in classes if i.lower() not in [j.lower() for j in self.toLs]
        ]
        self.fromList.clear()
        self.fromList.addItems(classes)
        self.fromList.sortItems()

    def getToList(self):
        """
        Getting the "to" items (QListWidget and python list)
        """
        return self.toLs

    def resetSelections(self):
        """
        Resets possible selections, in order to refresh object to initial state
        and avoid losing items.
        """
        tam = self.toList.__len__()
        for i in range(tam + 1, 1, -1):
            item = self.toList.takeItem(i - 2)
            self.fromLs.append(item.text())
            self.toLs.remove(item.text())
            self.fromLs.sort()
            self.fromList.addItem(item)
            self.fromList.sortItems()
