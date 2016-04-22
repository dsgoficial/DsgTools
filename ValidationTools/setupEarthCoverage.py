# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
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
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'setupEarthCoverage.ui'))

class SetupEarthCoverage(QtGui.QWizard, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, areas, lines, parent=None):
        '''Constructor.'''
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.areas = areas
        self.lines = lines
        self.areasCustomSelector.setFromList(self.areas)
        self.areasCustomSelector.setTitle(self.tr('Areas'))
        self.linesCustomSelector.setFromList(self.lines)
        self.linesCustomSelector.setTitle(self.tr('Lines'))
        self.areasCustomSelector.selectionChanged.connect(self.populateClasses)
        self.linesCustomSelector.selectionChanged.connect(self.populateDelimiters)
        self.button(QtGui.QWizard.FinishButton).clicked.connect(self.writeToDisk)
        #TODO: insert attribute filter for delimiter
    
    def populateClasses(self):
        self.treeWidget.clear()
        selectedAreaClasses = []
        for i in range(self.areasCustomSelector.toList.__len__()):
            selectedAreaClasses.append(self.areasCustomSelector.toList.item(i).text())
        selectedAreaClasses.sort()
        for i in range(len(selectedAreaClasses)):
            treeItem = QtGui.QTreeWidgetItem()
            treeItem.setText(0,selectedAreaClasses[i])
            self.treeWidget.insertTopLevelItem(0,treeItem)
        self.linesCustomSelector.selectionChanged.emit()


    def populateDelimiters(self):
        delimiterList = []
        for i in range(self.linesCustomSelector.toList.__len__()):
            delimiterList.append(self.linesCustomSelector.toList.item(i).text())
        for i in range(self.treeWidget.invisibleRootItem().childCount()):
            for delimiter in delimiterList:
                treeItem = QtGui.QTreeWidgetItem(self.treeWidget.invisibleRootItem().child(i))
                treeItem.setText(1,delimiter)
                treeItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                treeItem.setCheckState(1,Qt.Checked)
            self.treeWidget.invisibleRootItem().child(i).setExpanded(True)

    def getEarthCoverageDict(self):
        invRootItem = self.treeWidget.invisibleRootItem()
        earthCoverageDict = dict()
        for i in range(invRootItem.childCount()):
            childClass = invRootItem.child(i)
            earthCoverageDict[childClass.text(0)] = []
            for j in range(childClass.childCount()):
                if childClass.child(j).checkState(1) == Qt.Checked:
                    earthCoverageDict[childClass.text(0)].append(childClass.child(j).text(1))
        return earthCoverageDict

    def writeToDisk(self):
        fileName = os.path.join(os.path.dirname(__file__), 'ValidationConfig', 'earthCoverage.cfg')
        try:
            with open(fileName, 'w') as outfile:
                json.dump(self.getEarthCoverageDict(), outfile, sort_keys=True, indent=2)
        except Exception as e:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving file! \n')+e.args[0])
            return
        self.coverageChanged.emit()

        
    