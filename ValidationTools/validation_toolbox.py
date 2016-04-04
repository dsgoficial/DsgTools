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

# Qt imports
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QApplication, QCursor, QMenu, QTableWidgetItem
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceURI

import qgis as qgis
from qgis.core import QgsMessageLog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_toolbox.ui'))

#DsgTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory
from DsgTools.ValidationTools.validation_config import ValidationConfig
from DsgTools.ValidationTools.validationManager import ValidationManager
from DsgTools.ValidationTools.validation_history import ValidationHistory
from DsgTools.ValidationTools.rules_editor import RulesEditor

class ValidationToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, codeList):
        """Constructor."""
        super(ValidationToolbox, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        #TODO enable tab when db is set
        self.layerFactory = LayerFactory()
        self.edgvLayer = None
        self.flagLyr = None
        self.iface = iface
        self.codeList = codeList
        self.databaseLineEdit.setReadOnly(True)
        self.configWindow = ValidationConfig()
        self.configWindow.widget.connectionChanged.connect(self.updateDbLineEdit)
        self.validationManager = None
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.createMenuEditFlagStatus)

    def createMenuEditFlagStatus(self, position):
        menu = QMenu()
        item = self.tableView.indexAt(position)
        if item:
            menu.addAction(self.tr('Zoom to flag'), self.zoomToFlag)
            menu.addAction(self.tr('Set Visited'), self.setFlagVisited)
            menu.addAction(self.tr('Set Unvisited'), self.setFlagUnvisited)
        menu.exec_(self.tableView.viewport().mapToGlobal(position))
    
    @pyqtSlot()
    def on_theSelectionModel_selectionChanged(self):
        print 'mudou'
    
    def setFlagVisited(self):
        print 'visited'

    def setFlagUnvisited(self):
        print 'unvisited'
    
    def zoomToFlag(self):
        idx =  self.tableView.selectionModel().selection().indexes()[0].data()
        
        dimension = self.tableView.selectionModel().selection().indexes()[6].data()
        if dimension == 0:
            layer = 'aux_flags_validacao_p'
        elif dimension == 1:
            layer = 'aux_flags_validacao_l'
        elif dimension == 2:
            layer = 'aux_flags_validacao_a'
            
        flagLyr = self.loadFlagLyr(layer)
        self.iface.mapCanvas().refresh()
        flagLyr.select(idx)
        bbox = flagLyr.boundingBoxOfSelected()
        flagLyr.removeSelection()
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()
    
    def loadFlagLyr(self, layer):
        if not self.checkFlagsLoaded(layer):
            dbName = self.configWindow.widget.abstractDb.getDatabaseName()
            edgvLayer = self.layerFactory.makeLayer(self.configWindow.widget.abstractDb, self.codeList, 'validation.'+layer)
            groupList =  qgis.utils.iface.legendInterface().groups()
            if dbName in groupList:
                return  edgvLayer.load(self.configWindow.widget.crs,groupList.index(dbName))
            else:
                parentTreeNode = qgis.utils.iface.legendInterface().addGroup(self.configWindow.widget.abstractDb.getDatabaseName(), -1)
                return  edgvLayer.load(self.configWindow.widget.crs,parentTreeNode)
        else:
            loadedLayers = self.iface.mapCanvas().layers()
            for lyr in loadedLayers:
                if lyr.name() == layer:
                    return lyr
    
    def checkFlagsLoaded(self, layer):
        loadedLayers = self.iface.mapCanvas().layers()
        candidateLyrs = []
        for lyr in loadedLayers:
            if lyr.name() == layer:
                candidateLyrs.append(lyr)
        for lyr in candidateLyrs:
            if self.configWindow.widget.abstractDb.isLyrInDb(lyr):
                return True
        return False

    @pyqtSlot(bool)
    def on_openDbPushButton_clicked(self):
        self.configWindow.show()

    @pyqtSlot(bool)
    def on_historyButton_clicked(self):
        historyWindow = ValidationHistory(self.configWindow.widget.abstractDb)
        historyWindow.exec_()
    
    @pyqtSlot()
    def updateDbLineEdit(self):
        database, self.scale, self.tolerance = '', '', ''
        try:
            self.configWindow.widget.abstractDb.checkAndOpenDb()
            database = self.configWindow.widget.comboBoxPostgis.currentText()
            self.databaseLineEdit.setText(database)
            self.scale = self.configWindow.scaleComboBox.currentText()
            self.tolerance = self.configWindow.toleranceLineEdit.text()
            parametersDict = dict()
            parametersDict['tolerance'] = self.tolerance
            self.validationManager = ValidationManager(self.configWindow.widget.abstractDb, parametersDict)
            self.populateProcessList()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            self.processTreeWidget.clear()

        self.databaseLineEdit.setText(database)
    
    def populateProcessList(self):
        self.processTreeWidget.clear()
        self.edgvLayer = None
        self.flagLyr = None
        rootItem = self.processTreeWidget.invisibleRootItem()
        procList = self.validationManager.processList
        for i in range(len(procList)):
            item = QtGui.QTreeWidgetItem(rootItem)
            item.setText(0, str(i+1))
            item.setText(1, procList[i])
            
            status = None
            try:
                status = self.configWindow.widget.abstractDb.getValidationStatusText(procList[i])
            except Exception as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
                QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                status = 'Error! Check log!'
                
            if not status:
                item.setText(2, 'Not yet ran')
            else:
                item.setText(2, status)
        pass
    
    @pyqtSlot(bool)
    def on_runButton_clicked(self):
        processName = self.processTreeWidget.selectedItems()[0].text(1)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        procReturn = self.validationManager.executeProcess(processName)
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Process error. Check log for details.'))
        else:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!
            pass
        pass

    @pyqtSlot(int)
    def on_validationTabWidget_currentChanged(self):
        if self.validationTabWidget.currentIndex() == 1 and self.configWindow.widget.abstractDb <> None:
            self.projectModel = QSqlTableModel(None,self.configWindow.widget.abstractDb.db)
            self.projectModel.setTable('validation.aux_flags_validacao')
            self.projectModel.select()
            self.tableView.setModel(self.projectModel)
        pass    
    
    @pyqtSlot(bool)
    def on_rulesEditorButton_clicked(self):
        try:
            self.configWindow.widget.abstractDb.checkAndOpenDb()
            dlg = RulesEditor(self.configWindow.widget.abstractDb)
            dlg.exec_()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database not loaded or a problem occurred.\n')+str(e.args[0]))

