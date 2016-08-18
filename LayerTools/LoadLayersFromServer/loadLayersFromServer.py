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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog, QProgressBar
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles
from DsgTools.CustomWidgets.progressWidget import ProgressWidget


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'loadLayersFromServer.ui'))

class LoadLayersFromServer(QtGui.QDialog, FORM_CLASS):
    def __init__(self, codeList, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.iface = iface
        self.codeList = codeList
        self.utils = Utils()
        self.setupUi(self)
        self.customServerConnectionWidget.postgisCustomSelector.setTitle(self.tr('Select Databases'))
        self.customServerConnectionWidget.spatialiteCustomSelector.setTitle(self.tr('Selected Spatialites'))
        self.layersCustomSelector.setTitle(self.tr('Select layers to be loaded'))
        self.domainDict = dict()
        self.customServerConnectionWidget.dbDictChanged.connect(self.updateLayersFromDbs)
        self.customServerConnectionWidget.resetAll.connect(self.resetInterface)
        self.lyrDict = dict()
    
    def resetInterface(self):
        self.layersCustomSelector.clearAll()
        #TODO: refresh optional parameters
        pass
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.close()
    
    def updateLayersFromDbs(self, type, dbList):
        errorDict = dict()
        if type == 'added':
            progress = ProgressWidget(1,len(dbList),self.tr('Reading selected databases... '), parent = self)
            for dbName in dbList:
                try:
                    geomDict = self.customServerConnectionWidget.selectedDbsDict[dbName].getGeomColumnDict()
                    for geom in geomDict.keys():
                        for lyr in geomDict[geom]:
                            schema, lyrName = lyr.split('.')
                            if lyrName not in self.lyrDict.keys():
                                self.lyrDict[lyrName] = dict()
                                self.lyrDict[lyrName]['dbList'] = []
                            self.lyrDict[lyrName]['schema'] = schema
                            self.lyrDict[lyrName]['cat'] = lyrName.split('_')[0]
                            if dbName not in self.lyrDict[lyrName]['dbList']:
                                self.lyrDict[lyrName]['dbList'].append(dbName)
                except Exception as e:
                    errorDict[dbName] = str(e.args[0])
                progress.step()
                
        elif type == 'removed':
            for lyr in self.lyrDict.keys():
                popList = []
                for i in range(len(self.lyrDict[lyr]['dbList'])):
                    if len(self.lyrDict[lyr]['dbList']) > 0:
                        if self.lyrDict[lyr]['dbList'][i] in dbList:
                            popList.append(i)
                popList.sort(reverse=True)
                for i in popList:
                    self.lyrDict[lyr]['dbList'].pop(i)
                if len(self.lyrDict[lyr]['dbList']) == 0:
                    self.lyrDict.pop(lyr)
        self.layersCustomSelector.setInitialState(self.lyrDict.keys(),unique = True)
    
    
    @pyqtSlot(bool)
    def on_showCategoriesRadioButton_toggled(self):
        if self.lyrDict <> dict():
            cats = []
            for lyr in self.lyrDict.keys():
                 if self.lyrDict[lyr]['cat'] not in cats:
                     cats.append(self.lyrDict[lyr]['cat'])
            self.layersCustomSelector.setInitialState(cats,unique = True)
    
    @pyqtSlot(bool)
    def on_showClassesRadioButton_toggled(self):
        if self.lyrDict <> dict():
            self.layersCustomSelector.setInitialState(self.lyrDict.keys(),unique = True)
            
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        #1- filter classes if categories is checked.
        selected = self.layersCustomSelector.toLs
        print selected
        selectedClasses = []
        if self.showCategoriesRadioButton.isChecked():
            for lyr in self.lyrDict.keys():
                if self.lyrDict[lyr]['cat'] in selected and lyr not in selectedClasses:
                    selectedClasses.append(lyr)
        else:
            selectedClasses = self.layersCustomSelector.toLs
        print selectedClasses
        #2- build list
        #3- Build factory dict
        #4- load for each db
        pass
