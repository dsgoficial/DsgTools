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
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QFileDialog
from fileinput import filename
from DsgTools.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'setupEarthCoverage.ui'))

class SetupEarthCoverage(QtGui.QWizard, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, abstractDb, areas, lines, oldCoverage, enableSetupFromFile = True, onlySetup = False, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.areas = areas
        self.lines = lines
        self.abstractDb = abstractDb
        self.areasCustomSelector.setTitle(self.tr('Areas'))
        self.linesCustomSelector.setTitle(self.tr('Lines'))
        self.setupWizard(oldCoverage, enableSetupFromFile)
        if not onlySetup:
            self.button(QtGui.QWizard.FinishButton).clicked.connect(self.writeIntoDb)
        else:
            self.button(QtGui.QWizard.FinishButton).clicked.connect(self.createDict)
        self.button(QtGui.QWizard.NextButton).clicked.connect(self.buildTree)

    def setupFromFile(self):
        """
        Opens a earth coverage file
        """
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you want to open an earth coverage file?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        filename = QFileDialog.getOpenFileName(self, self.tr('Open Earth Coverage Setup configuration'), '', self.tr('Earth Coverage Files (*.json)'))
        return filename

    def setupWizard(self, oldCoverage, enableSetupFromFile):
        """
        Prepares the wizard
        oldCoverage: old configuration
        """
        if oldCoverage:
            self.abstractDb.dropCentroids(oldCoverage.keys())
        if enableSetupFromFile:
            filename = self.setupFromFile()
        else:
            filename = None
        if filename:
            setupDict = self.utils.readJsonFile(filename)
            areasToList = setupDict.keys()
            linesToList = []
            for key in areasToList:
                lines = setupDict[key]
                for line in lines:
                    if line not in linesToList:
                        linesToList.append(line)
            areasFromList = [area for area in self.areas if area not in areasToList]
            linesFromList = [line for line in self.lines if line not in linesToList]
            self.areasCustomSelector.setToList(areasToList)
            self.areasCustomSelector.setFromList(areasFromList)
            self.linesCustomSelector.setToList(linesToList)
            self.linesCustomSelector.setFromList(linesFromList)  
            self.checkDelimiters(setupDict)
        else:
            self.areasCustomSelector.setFromList(self.areas)
            self.linesCustomSelector.setFromList(self.lines)

    def checkDelimiters(self, setupDict):
        """
        Check delimiters
        """
        for i in range(self.treeWidget.invisibleRootItem().childCount()):
            areaItem = self.treeWidget.invisibleRootItem().child(i)
            for j in range(self.treeWidget.invisibleRootItem().child(i).childCount()):
                delimiterItem = areaItem.child(j)
                if areaItem.text(0) in setupDict.keys():
                    if delimiterItem.text(1) not in setupDict[areaItem.text(0)]:
                        delimiterItem.setCheckState(1,Qt.Unchecked)

    def loadJson(self, filename):
        """
        Loads a json file
        """
        filename = QFileDialog.getOpenFileName(self, self.tr('Open Field Setup configuration'), self.folder, self.tr('Field Setup Files (*.json)'))
        if not filename:
            return
        return self.readJsonFile(filename)

    def populateClasses(self):
        """
        Populates area classes
        """
        self.treeWidget.clear()
        selectedAreaClasses = self.areasCustomSelector.toLs
        for i in range(len(selectedAreaClasses)):
            treeItem = QtGui.QTreeWidgetItem()
            treeItem.setText(0,selectedAreaClasses[i])
            self.treeWidget.insertTopLevelItem(0,treeItem)

    def populateDelimiters(self):
        """
        Populates line classes (area delimiters)
        """
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

    def getEarthCoverageDictFromTree(self):
        """
        Gets earth coverage configuration from the tree widget
        """
        invRootItem = self.treeWidget.invisibleRootItem()
        earthCoverageDict = dict()
        for i in range(invRootItem.childCount()):
            childClass = invRootItem.child(i)
            earthCoverageDict[childClass.text(0)] = []
            for j in range(childClass.childCount()):
                if childClass.child(j).checkState(1) == Qt.Checked:
                    earthCoverageDict[childClass.text(0)].append(childClass.child(j).text(1))
        return earthCoverageDict
    
    def createDict(self):
        pass

    def writeIntoDb(self):
        """
        Writes the configuration in the database
        """
        try:
            earthDict = self.getEarthCoverageDictFromTree()
            self.abstractDb.setEarthCoverageDict(json.dumps(earthDict))
            self.abstractDb.createCentroidAuxStruct(earthDict.keys())
            self.coverageChanged.emit()
            if QMessageBox.question(self, self.tr('Question'), self.tr('Do you want to save this earth coverage setup?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                return
            filename = QFileDialog.getSaveFileName(self, self.tr('Save Earth Coverage Setup configuration'), '', self.tr('Earth Coverage Files (*.json)'))
            if not filename:
                QMessageBox.critical(self, self.tr('Critical!'), self.tr('Define a name for the earth coverage file!'))
                return
            with open(filename, 'w') as outfile:
                json.dump(earthDict, outfile, sort_keys=True, indent=4)
            QMessageBox.information(self, self.tr('Information!'), self.tr('Field setup file saved successfully!'))
            
        except Exception as e:
            self.abstractDb.rollbackEarthCoverage(earthDict.keys())
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving into database! \n')+e.args[0])
            return

    def buildTree(self):
        """
        Builds the earth coverage tree using the selected areas and lines
        """
        self.populateClasses()
        self.populateDelimiters()
        