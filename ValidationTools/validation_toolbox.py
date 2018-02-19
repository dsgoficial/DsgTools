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
from DsgTools.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from DsgTools.ValidationTools.validation_config import ValidationConfig
from DsgTools.ValidationTools.validationManager import ValidationManager
from DsgTools.ValidationTools.validation_history import ValidationHistory
from DsgTools.ValidationTools.rules_editor import RulesEditor
from DsgTools.ValidationTools.ValidationProcesses.spatialRuleEnforcer import SpatialRuleEnforcer
from DsgTools.ValidationTools.attributeRulesEditor import AttributeRulesEditor
from DsgTools.dsgEnums import DsgEnums

class ValidationToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface):
        """
        Constructor
        """
        super(ValidationToolbox, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.edgvLayer = None
        self.flagLyr = None
        self.iface = iface
        self.databaseLineEdit.setReadOnly(True)
        self.configWindow = ValidationConfig()
        self.configWindow.widget.connectionChanged.connect(self.updateDbLineEdit)
        self.validationManager = None
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.createContextMenu)
        self.ruleEnforcer = None
        self.attributeRulesEditorPushButton.hide()
        self.itemList = []
        # self.filterDict = {self.tr('Process Name'):DsgEnums.ProcessName, self.tr('Class Name'):DsgEnums.ClassName}

    def createContextMenu(self, position):
        """
        Creates the flag menu
        """
        menu = QMenu()
        item = self.tableView.indexAt(position)
        if item:
            menu.addAction(self.tr('Zoom to flag'), self.zoomToFlag)
            menu.addAction(self.tr('Remove flag'), self.removeCurrentFlag)
#             menu.addAction(self.tr('Set Visited'), self.setFlagVisited)
#             menu.addAction(self.tr('Set Unvisited'), self.setFlagUnvisited)
        menu.exec_(self.tableView.viewport().mapToGlobal(position))
        
    
    def removeCurrentFlag(self):
        """
        Creates the remove flag menu
        """
        try:
            flagId = self.tableView.selectionModel().selection().indexes()[0].data()
        except:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('No flags were selected!'))
            return
        self.configWindow.widget.abstractDb.deleteProcessFlags(flagId = flagId)
        self.refreshFlags()

    @pyqtSlot()
    def on_theSelectionModel_selectionChanged(self):
        """
        To do.
        """
        print 'mudou'
    
    def setFlagVisited(self):
        """
        To do
        """
        print 'visited'

    def setFlagUnvisited(self): 
        """
        To do
        """
        print 'unvisited'
    
    def zoomToFlag(self):
        """
        Zooms the map canvas to the current selected flag
        """
        try:
            idx =  self.tableView.selectionModel().selection().indexes()[0].data()
        except:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('No flags were selected!'))
            return
        dimension = self.tableView.selectionModel().selection().indexes()[6].data()
        if dimension == 0:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOINT', 'lyrName': 'flags_validacao_p', 'tableName':'aux_flags_validacao_p', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}            
        elif dimension == 1:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTILINESTRING', 'lyrName': 'flags_validacao_l', 'tableName':'aux_flags_validacao_l', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}
        elif dimension == 2:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOLYGON', 'lyrName': 'flags_validacao_a', 'tableName':'aux_flags_validacao_a', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}
            
        flagLyr = self.loadFlagLyr(layer)
        flagLyr.setLayerTransparency(50)
        flagLyr.removeSelection()
        self.iface.mapCanvas().refresh()
        flagLyr.select(idx)
        bbox = flagLyr.boundingBoxOfSelected()
        mapbox = self.iface.mapCanvas().mapSettings().layerToMapCoordinates(flagLyr, bbox)
        self.iface.mapCanvas().setExtent(mapbox)
        self.iface.mapCanvas().refresh()
    
    def loadAllFlagLayers(self):
        """
        Loads all flags
        """
        pointLayer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOINT', 'lyrName': 'flags_validacao_p', 'tableName':'aux_flags_validacao_p', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}            
        lineLayer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTILINESTRING', 'lyrName': 'flags_validacao_l', 'tableName':'aux_flags_validacao_l', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}
        areaLayer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOLYGON', 'lyrName': 'flags_validacao_a', 'tableName':'aux_flags_validacao_a', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}
        self.loadFlagLyr([pointLayer, lineLayer, areaLayer])
    
    def loadFlagLyr(self, layer):
        """
        Loads the flag layer. It checks if the flag layer is already loaded, case not, it loads the flag layer into the TOC
        layer: layer name
        """
        self.layerLoader = LayerLoaderFactory().makeLoader(self.iface,self.configWindow.widget.abstractDb)
        if isinstance(layer, list):
            return self.layerLoader.load(layer, uniqueLoad = True)
        else:
            return self.layerLoader.load([layer], uniqueLoad = True)[layer['lyrName']]
    
    def checkFlagsLoaded(self, layer):
        """
        Checks if the flag layer is already loaded
        layer: layer name
        """
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
        """
        Opend dialog for database connection
        """
        self.configWindow.show()

    @pyqtSlot(bool)
    def on_historyButton_clicked(self):
        """
        Shows the validation history
        """
        historyWindow = ValidationHistory(self.configWindow.widget.abstractDb)
        historyWindow.exec_()
    
    @pyqtSlot()
    def updateDbLineEdit(self):
        """
        Updates the database information
        """
        database = ''
        try:
            self.configWindow.widget.abstractDb.checkAndOpenDb()
            database = self.configWindow.widget.comboBoxPostgis.currentText()
            self.databaseLineEdit.setText(database)
            self.validationManager = ValidationManager(self.configWindow.widget.abstractDb, self.iface)
            self.populateProcessList()
            self.databaseLineEdit.setText(database)

            # adjusting flags table model
            self.projectModel = QSqlTableModel(None,self.configWindow.widget.abstractDb.db)
            self.projectModel.setTable('validation.aux_flags_validacao')
            self.projectModel.select()
            self.tableView.setModel(self.projectModel)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(self.tr('Error loading db: ')+':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.processTreeWidget.clear()
    

    def on_filterLineEdit_textChanged(self, text):
        for i in self.itemList:
            if text.lower() in i.text(1).lower():
                i.setHidden(False)
            else:
                i.setHidden(True)

    def populateProcessList(self):
        """
        Populates the process list. It also checks the status of each available process
        """
        self.processTreeWidget.clear()
        self.edgvLayer = None
        self.flagLyr = None
        self.itemList = []
        rootItem = self.processTreeWidget.invisibleRootItem()
        procList = sorted(self.validationManager.processDict)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for i in range(len(procList)):
            item = QtGui.QTreeWidgetItem(rootItem)
            item.setText(0, str(i+1))
            item.setText(1, procList[i])
            
            status = None
            try:
                status = self.configWindow.widget.abstractDb.getValidationStatusText(self.validationManager.processDict[procList[i]])
            except Exception as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
                QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                status = 'Error! Check log!'
                
            if not status:
                item.setText(2, 'Not yet ran')
            else:
                item.setText(2, status)
            self.itemList.append(item)
        for i in range(3):
            self.processTreeWidget.resizeColumnToContents(i)
        self.filterLineEdit.clear()
        QApplication.restoreOverrideCursor()

    @pyqtSlot(bool)
    def on_reRunButton_clicked(self):
        """
        Re-runs last process with the same attributes.
        """
        if not self.validationManager:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to run process!'))
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            procReturn = self.validationManager.runLastProcess()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            procReturn = 0
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Process error. Check log for details.'))
        elif procReturn == -1:
            QtGui.QMessageBox.information(self, self.tr('Information!'), self.tr('Process canceled by user!'))
        elif procReturn == -2:
            QtGui.QMessageBox.information(self, self.tr('Information!'), self.tr('No previous process run this session.'))
        else:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!

    @pyqtSlot(bool)
    def on_runButton_clicked(self):
        """
        Runs the current selected process
        """
        selectedItems = self.processTreeWidget.selectedItems()
        if len(selectedItems) == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a process to run!'))
            return
        processName = selectedItems[0].text(1)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            procReturn = self.validationManager.executeProcessV2(processName)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            procReturn = 0
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Process error. Check log for details.'))
        elif procReturn == -1:
            QtGui.QMessageBox.information(self, self.tr('Information!'), self.tr('Process canceled by user!'))
        else:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!
            #load flag layers
            self.loadAllFlagLayers()
        self.iface.mapCanvas().refresh() #atualizar canvas para mostrar resultado para o usuário

    @pyqtSlot(int, name='on_validationTabWidget_currentChanged')
    def refreshFlags(self):
        """
        Changes the current tab in the validation tool box
        """
        if self.validationTabWidget.currentIndex() == 1 and self.configWindow.widget.abstractDb != None:
            self.projectModel.select()
            self.configWindow.widget.abstractDb.createFilteredFlagsViewTable()
        # populates the comboBoxes
        self.classFilterComboBox.clear()
        self.processFilterComboBox.clear()
        if self.configWindow.widget.abstractDb:
            listProcesses = self.configWindow.widget.abstractDb.fillComboBoxProcessOrClasses("process")
            listClasses = self.configWindow.widget.abstractDb.fillComboBoxProcessOrClasses("class")
            self.classFilterComboBox.addItems(listClasses)
            self.processFilterComboBox.addItems(listProcesses)
        self.processFilterComboBox.setCurrentIndex(0)
        self.classFilterComboBox.setCurrentIndex(0)

    @pyqtSlot(bool)
    def on_rulesEditorButton_clicked(self):
        """
        Opens the spatial rule editor
        """
        try:
            self.configWindow.widget.abstractDb.checkAndOpenDb()
            dlg = RulesEditor(self.configWindow.widget.abstractDb)
            dlg.exec_()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database not loaded or a problem occurred.\n')+':'.join(e.args))

    @pyqtSlot(int, name = 'on_procesFilterComboBox_currentIndexChanged')
    def refreshFlagListOnProcessSelection(self, classChanged=False):        
        """
        Refreshs the list of processes available for filtering the view
        """
        if self.processFilterComboBox.currentIndex() == 0:
            continue
        elif not classChanged:
            # this way, this function will not be called into a loop if
            # the class is changed. 
            self.refreshFlagListOnClassSelection(processChanged=True)

    @pyqtSlot(int, name = 'on_classFilterComboBox_currentIndexChanged')
    def refreshFlagListOnClassSelection(self, processChanged=False):
        """
        Refreshs the list of classes available for filtering the view
        """
        className = self.classFilterComboBox.currentText()
        processName = self.processFilterComboBox.currentText()
        if processName == '': # this indicates 1st execution
            self.processFilterComboBox.setCurrentIndex(0)
        if processChanged: # the signal was sent from process combo box
            # then we check if the className is in the list of classes affected
            # by that process
            listProcesses = self.configWindow.widget.abstractDb.fillComboBoxProcessOrClasses("process", filteringClass=className)

        self.processFilterComboBox.clear()
        listProcesses = self.configWindow.widget.abstractDb.fillComboBoxProcessOrClasses("process", filteringClass=className)
        self.processFilterComboBox.addItems(listProcesses)
        if processName not in listProcesses:
            self.processFilterComboBox.setCurrentIndex(0)
        processName = self.processFilterComboBox.currentText()
        self.configWindow.widget.abstractDb.createFilteredFlagsViewTable(className=className, processName=processName)
        self.projectModel.setTable('validation.filtered_flags')
        self.projectModel.select()

    @pyqtSlot(bool)
    def on_ruleEnforcerRadio_toggled(self, checked):
        """
        Toggles the spatial rule enforcer
        """
        if checked:
            self.ruleEnforcer = SpatialRuleEnforcer(self.validationManager.postgisDb, self.iface)
            self.ruleEnforcer.connectEditingSignals()
            self.ruleEnforcer.ruleTested.connect(self.refreshFlags)
        else:
            self.ruleEnforcer.disconnectEditingSignals()
            self.ruleEnforcer.ruleTested.disconnect(self.refreshFlags)
    
    @pyqtSlot(bool)
    def on_attributeRulesEditorPushButton_clicked(self):
        """
        Opens the attribute rule editor
        """
        try:
            self.configWindow.widget.abstractDb.checkAndOpenDb()
            dlg = AttributeRulesEditor(self.configWindow.widget.abstractDb)
            dlg.exec_()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database not loaded or a problem occurred.\n')+':'.join(e.args))

    @pyqtSlot(bool)
    def on_clearAllPushButton_clicked(self):
        """
        Deletes all flags from validation.aux_flags
        1- Get abstractDb
        2- Delete flag
        """
        try:
            if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to clear all flags?'), QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
                return
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.configWindow.widget.abstractDb.deleteProcessFlags()
            QApplication.restoreOverrideCursor()
            #refresh
            self.refreshFlags()
            self.iface.mapCanvas().refresh()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted.\n')+':'.join(e.args))

    @pyqtSlot(bool)
    def on_clearSelectedPushButton_clicked(self):
        """
        Deletes selected flags on the panel from validation.aux_flags
        """
        try:
            if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to clear those flags?'), QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
                return
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            # check what is filtered
            processName = self.processComboBox.currentText()
            layerName = self.customFilterComboBox.currentText()
            if (processName or layerName):
                self.configWindow.widget.abstractDb.deleteProcessFlags(processName,layerName)
            else:
                QApplication.restoreOverrideCursor()
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted as no Process nor Class was chosen.\n'))
                return
            QApplication.restoreOverrideCursor()
            # refresh View Table with lasting flags
            self.refreshFlags()
            self.iface.mapCanvas().refresh()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted.\n')+':'.join(e.args))
