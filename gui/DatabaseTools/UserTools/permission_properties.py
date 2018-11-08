# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-12-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QAbstractItemView

# DSGTools imports

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'permission_properties.ui'))

class PermissionProperties(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, permissionsDict, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.treeWidget.setColumnWidth(0, 400)
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = self.createItem(rootItem, 'database')

        self.createChildrenItems(dbItem, permissionsDict)
        
        self.treeWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def createItem(self, parent, text):
        """
        Creates a tree widget item
        parent: parent item
        text: item text
        """
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)
        item.setCheckState(1, QtCore.Qt.Unchecked)
        item.setCheckState(2, QtCore.Qt.Unchecked)
        item.setText(0, text)
        return item
    
    def createChildrenItems(self, parent, mydict):
        """
        Creates children items
        parent: parent item
        mydict: data dictionary used to populate tree items
        """
        #permissions
        lista = ['read', 'write']
        for key in list(mydict.keys()):
            if key in lista:
                self.setItemCheckState(parent, mydict, key)
            else:
                itemText = key
                item = self.createItem(parent, itemText)
                self.createChildrenItems(item, mydict[key])
                
    def setItemCheckState(self, item, mydict, key):
        """
        Sets item check state
        """
        if key == 'read':
            item.setCheckState(1, int(mydict[key]))
        elif key == 'write':
            item.setCheckState(2, int(mydict[key]))
            