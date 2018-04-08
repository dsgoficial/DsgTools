# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import csv
import shutil
from osgeo import gdal, ogr

# Import the PyQt and QGIS libraries
from qgis.PyQt import uic
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QMenu, QApplication, QFileDialog, QMessageBox, QTreeWidgetItem, QInputDialog, QDialog
from qgis.PyQt.QtGui import QCursor
from _csv import writer
from qgis._core import QgsAction

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_inventoryTools.ui'))

class InventoryTools(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """
        Constructor
        """
        super(InventoryTools, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        
        self.files = list()
        
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.createMenu)
        
        self.whitelistRadio.setChecked(True)

        # set most used file extensions        
        item = QTreeWidgetItem(self.treeWidget.invisibleRootItem())
        item.setText(0,'shp')
        item = QTreeWidgetItem(self.treeWidget.invisibleRootItem())
        item.setText(0,'tif')
        
    def depth(self, item):
        '''
        Calculates the depth of the item
        '''
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth
    
    def createMenu(self, position):
        '''
        Creates the popup menu that allows extension insertion and removal
        position: mouse click position
        '''
        menu = QMenu()
        
        item = self.treeWidget.itemAt(position)

        if not item:
            menu.addAction(self.tr('Insert Extension'), self.insertExtension)
        else:        
            if self.depth(item) == 1:
                menu.addAction(self.tr('Remove Extension'), self.removeExtension)
            
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        
    def insertExtension(self):
        '''
        Inserts a new extension to be analyzed
        '''
        text = QInputDialog.getText(self, self.tr('Type the extension'), self.tr('File extension'), mode=QLineEdit.Normal)
        item = QTreeWidgetItem(self.treeWidget.invisibleRootItem())
        item.setText(0,text[0])
       
    def removeExtension(self):
        '''
        Removes a extension from the list
        '''
        item = self.treeWidget.selectedItems()[0]
        index = self.treeWidget.indexOfTopLevelItem(item)
        self.treeWidget.takeTopLevelItem(index)

    def getParameters(self):
        '''
        Gets process parameters
        '''
        formatsList = []
        root = self.treeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            extension = item.text(0)
            formatsList.append(extension)
            
        return (self.parentFolderEdit.text(), self.outputFileEdit.text(), self.copyFilesCheckBox.isChecked(), \
                self.destinationFolderEdit.text(), formatsList, self.whitelistRadio.isChecked(), self.onlyGeoCheckBox.isChecked())
       
    @pyqtSlot(bool)
    def on_parentFolderButton_clicked(self):
        '''
        Opens the dialog to select the folder
        '''
        folder = QFileDialog.getExistingDirectory(self, self.tr('Select Directory'))
        self.parentFolderEdit.setText(folder)

    @pyqtSlot(bool)
    def on_copyFilesButton_clicked(self):
        '''
        Opens the dialog to define the copy destination folder
        '''
        folder = QFileDialog.getExistingDirectory(self, self.tr('Select Directory'))
        self.destinationFolderEdit.setText(folder)

    @pyqtSlot(bool)
    def on_outputFileButton_clicked(self):
        '''
        Inventory output file selection
        '''
        if self.onlyGeoCheckBox.isChecked():
            fileName, __ = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Save Output File'), filter='Shapefile (*.shp)')
        else:
            fileName, __ = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Save Output File'), filter='CSV (*.csv)')
        self.outputFileEdit.setText(fileName)
        
    @pyqtSlot(int)
    def on_copyFilesCheckBox_stateChanged(self, state):
        '''
        Slot to update the dialog when copy files definition changes
        '''
        if self.copyFilesCheckBox.isChecked():
            self.frame_3.setEnabled(True)
        else:
            self.frame_3.setEnabled(False)
     
    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        '''
        Closes the dialog
        '''
        self.done(0)

    @pyqtSlot(bool)
    def on_okButton_clicked(self):
        '''
        Runs the process
        '''
        parentFolder = self.parentFolderEdit.text()
        outputFile = self.outputFileEdit.text()

        if not parentFolder or not outputFile:
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Information!'), self.tr('Please, fill all fields.'))
            return

        if self.whitelistRadio.isChecked():
            root = self.treeWidget.invisibleRootItem()
            if root.childCount() == 0:
                QApplication.restoreOverrideCursor()
                QMessageBox.information(self, self.tr('Information!'), self.tr('Please, insert file extensions to be considered.'))
                return
        
        if self.copyFilesCheckBox.isChecked():
            destinationFolder = self.destinationFolderEdit.text()
    
            if not destinationFolder:
                QApplication.restoreOverrideCursor()
                QMessageBox.information(self, self.tr('Information!'), self.tr('Please, choose a location to save the files.'))
                return

        self.done(1)
