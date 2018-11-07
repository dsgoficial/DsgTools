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
from builtins import range
import os
import json

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog
from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'setupEarthCoverage.ui'))

class SetupEarthCoverage(QtWidgets.QWizard, FORM_CLASS):
    coverageChanged = pyqtSignal()
    def __init__(self, edgvVersion, areas, lines, oldCoverage, propertyList, enableSetupFromFile = True, onlySetup = False, propertyName = None, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.utils = Utils()
        self.areas = areas
        self.lines = lines
        self.propertyName = propertyName
        self.edgvVersion = edgvVersion
        self.areasCustomSelector.setTitle(self.tr('Areas'))
        self.linesCustomSelector.setTitle(self.tr('Lines'))
        self.propertyList = propertyList
        self.button(QtWidgets.QWizard.NextButton).clicked.connect(self.buildTree)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.buildDict)
        self.setupWizard(oldCoverage, enableSetupFromFile)
        self.configDict = dict()

    def setupFromFile(self):
        """
        Opens a earth coverage file
        """
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you want to open an earth coverage file?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        filename, __ = QFileDialog.getOpenFileName(self, self.tr('Open Earth Coverage Setup configuration'), '', self.tr('Earth Coverage Files (*.json)'))
        return filename

    def setupWizard(self, oldCoverage, enableSetupFromFile):
        """
        Prepares the wizard
        oldCoverage: old configuration
        """
        if oldCoverage:
            # self.abstractDb.dropCentroids(oldCoverage.keys())
            self.setupUiFromDict(oldCoverage)
            return
        else:
            self.populateFrameListWidget(self.areas)
        if enableSetupFromFile:
            filename = self.setupFromFile()
        else:
            filename = None
        if filename:
            self.setupUiFromFile(filename)
        else:
            self.areasCustomSelector.setFromList(self.areas)
            self.linesCustomSelector.setFromList(self.lines)
        if self.propertyName:
            self.nameLineEdit.setText(self.propertyName)
            self.nameLineEdit.setEnabled(False)
    
    def setupUiFromFile(self, filename):
        """
        Populates ui from parameters of json
        """
        #read json
        jsonDict = self.utils.readJsonFile(filename)
        self.setupUiFromDict(jsonDict)

    def setupUiFromDict(self, jsonDict):
        """
        Populates ui from parameters of json
        """
        #set nameLineEdit
        self.nameLineEdit.setText(jsonDict['configName'])
        #populate listWidget
        self.populateFrameListWidget(self.areas, frame = jsonDict['frameLayer'])
        linesFromList, linesToList, areasFromList, areasToList = self.populateLists(jsonDict['earthCoverageDict'])
        self.areasCustomSelector.setToList(areasToList)
        self.areasCustomSelector.setFromList(areasFromList)
        self.linesCustomSelector.setToList(linesToList)
        self.linesCustomSelector.setFromList(linesFromList)
        self.buildTree()
        self.checkDelimiters(jsonDict['earthCoverageDict'])
    
    def populateFrameListWidget(self, areas, frame = None):
        areas.sort()
        self.listWidget.clear()
        self.listWidget.addItems(areas)
        if frame:
            try:
                frameItem = self.listWidget.findItems(frame, Qt.MatchExactly)[0]
                self.listWidget.setCurrentItem(frameItem)
            except:
                pass
    
    def populateLists(self, setupDict):
        areasToList = list(setupDict.keys())
        linesToList = []
        for key in areasToList:
            lines = setupDict[key]
            for line in lines:
                if line not in linesToList:
                    linesToList.append(line)
        areasFromList = [area for area in self.areas if area not in areasToList]
        linesFromList = [line for line in self.lines if line not in linesToList]
        return linesFromList, linesToList, areasFromList, areasToList

    def checkDelimiters(self, setupDict):
        """
        Check delimiters
        """
        for i in range(self.treeWidget.invisibleRootItem().childCount()):
            areaItem = self.treeWidget.invisibleRootItem().child(i)
            for j in range(self.treeWidget.invisibleRootItem().child(i).childCount()):
                delimiterItem = areaItem.child(j)
                if areaItem.text(0) in list(setupDict.keys()):
                    if delimiterItem.text(1) not in setupDict[areaItem.text(0)]:
                        delimiterItem.setCheckState(1,Qt.Unchecked)

    def loadJson(self, filename):
        """
        Loads a json file
        """
        filename, __ = QFileDialog.getOpenFileName(self, self.tr('Open Field Setup configuration'), self.folder, self.tr('Earth Coverage Setup File (*.dsgearthcov)'))
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
    
    def buildDict(self):
        '''
        Gets earth coverage dict from interface
        '''
        self.configDict['edgvVersion'] = self.edgvVersion
        self.configDict['configName'] = self.nameLineEdit.text()
        self.configDict['frameLayer'] = self.listWidget.currentItem().text()
        self.configDict['earthCoverageDict'] = self.getEarthCoverageDictFromTree()

    def buildTree(self):
        """
        Builds the earth coverage tree using the selected areas and lines
        """
        self.populateClasses()
        self.populateDelimiters()
        self.treeWidget.expandAll()
        self.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget.header().setStretchLastSection(False)
    
    def on_filterLineEdit_textChanged(self, text):
        """
        Filters the items to make it easier to spot and select them
        """
        classes = [edgvClass for edgvClass in self.areas if text in edgvClass]
        self.listWidget.clear()
        self.listWidget.addItems(classes)
        self.listWidget.sortItems()
    
    def validateEarthCoverageTreeWidget(self):
        rootNode = self.treeWidget.invisibleRootItem()
        childCount = rootNode.childCount()
        for i in range(childCount):
            areaItem = rootNode.child(i)
            lineChildCount = areaItem.childCount()
            hasSelected = False
            for j in range(lineChildCount):
                lineChild = areaItem.child(j)
                if lineChild.checkState(1) == Qt.Checked:
                    hasSelected = True
                    break
            if not hasSelected:
                return False
        return True

    def validateCurrentPage(self):
        if self.currentId() == 0:
            errorMsg = ''
            isValidated = True
            if self.nameLineEdit.text() == '':
                errorMsg += self.tr('An Earth Coverage name must be set.\n')
                isValidated = False
            if self.nameLineEdit.text() in self.propertyList:
                errorMsg += self.tr('An Earth Coverage with this name already exists.\n')
                isValidated = False
            if self.listWidget.currentRow() == -1:
                errorMsg += self.tr('A frame layer must be chosen.\n')
                isValidated = False
            if not isValidated:
                QMessageBox.warning(self, self.tr('Error!'), errorMsg)
            return isValidated
        elif self.currentId() == 1:
            if self.areasCustomSelector.toLs == []:
                errorMsg = self.tr('Areas must be chosen for Earth Coverage.\n')
                QMessageBox.warning(self, self.tr('Error!'), errorMsg)
                return False
            return True
        elif self.currentId() == 2:
            if self.linesCustomSelector.toLs == []:
                errorMsg = self.tr('Lines must be chosen for Earth Coverage.\n')
                QMessageBox.warning(self, self.tr('Error!'), errorMsg)
                return False
            return True
        elif self.currentId() == 3:
        #at least one line selected for each area
            if not self.validateEarthCoverageTreeWidget():
                errorMsg = self.tr('At least one line must be chosen for each Earth Coverage area.\n')
                QMessageBox.warning(self, self.tr('Error!'), errorMsg)
                return False
            return True
        else:
            return True