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
    os.path.dirname(__file__), 'customSelector.ui'))

class CustomSelector(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal(list,str)

    def __init__(self, parent = None):
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
        self.fromList.clear()
        self.toList.clear()
        self.filterLineEdit.clear()        
    
    def setInitialState(self, fromList, unique = False):
        self.fromLs = []
        self.toLs = []
        self.fromList.clear()
        self.toList.clear()
        self.setFromList(fromList, unique)
    
    def setFromList(self, fromList, unique = False):
        if unique:
            uniqueList = []
            for i in fromList:
                if i not in uniqueList:
                    uniqueList.append(i)
            self.fromLs = uniqueList
            self.fromList.addItems(uniqueList)
            self.fromList.sortItems()
        else:
            self.fromLs = fromList
            self.fromLs.sort()
            self.fromList.addItems(fromList)
            self.fromList.sortItems()
    
    def addItems(self, addList, unique = False):
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

    def setToList(self, toList):
        self.toList.addItems(toList)
        self.toList.sortItems()
    
    def setTitle(self,title):
        self.groupBox.setTitle(title)

    @pyqtSlot(bool)
    def on_pushButtonSelectOne_clicked(self):
        listedItems = self.fromList.selectedItems()
        added = []
        for i in listedItems:
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
        classes = [edgvClass for edgvClass in self.fromLs if text in edgvClass]
        filteredClasses = [i for i in classes if i not in self.toLs]
        self.fromList.clear()
        self.fromList.addItems(classes)
        self.fromList.sortItems()

