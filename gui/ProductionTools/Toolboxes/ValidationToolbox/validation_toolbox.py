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
from __future__ import print_function
from builtins import str
from builtins import range
import os
from collections import OrderedDict
from operator import itemgetter

# Qt imports
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.QtWidgets import QApplication, QMenu, QTableWidgetItem, QMessageBox, QTreeWidgetItem
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceUri, Qgis, QgsMessageLog
import qgis as qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_toolbox.ui'))

#DsgTools core imports
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from DsgTools.core.ValidationTools.validationManager import ValidationManager
from DsgTools.core.dsgEnums import DsgEnums
#DsgTools gui imports
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.validation_config import ValidationConfig
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.validation_history import ValidationHistory
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.rules_editor import RulesEditor
from DsgTools.core.ValidationTools.ValidationProcesses.spatialRuleEnforcer import SpatialRuleEnforcer
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.attributeRulesEditor import AttributeRulesEditor

class ValidationToolbox(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, iface):
        """
        Constructor
        """
        super(ValidationToolbox, self).__init__()
        self.setupUi(self)
        self.iface = iface
        # self.configWindow = ValidationConfig()
        self.connectionSelectorComboBox.connectionChanged.connect(self.updateDbLineEdit)
        # self.connectionSelectorComboBox.dbChanged.connect(self.attributeRulePropertyManagerWidget.setParameters)
        # self.connectionSelectorComboBox.dbChanged.connect(self.validationWorkflowPropertyManagerWidget.setParameters)
        self.validationWorkflowPropertyManagerWidget.parent = self
        self.validationManager = None
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.createContextMenu)
        self.ruleEnforcer = None
        self.itemList = []
        self.filterDict = {self.tr('Process Name'):DsgEnums.ProcessName, self.tr('Class Name'):DsgEnums.ClassName}

    def addTool(self, manager, callback, parentMenu, iconBasePath, parentStackButton):
        icon_path = iconBasePath + 'validationtools.png'
        text = self.tr('Perform database validation (quality assurance)')
        action = manager.add_action(
            icon_path,
            text=text,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            parentMenu = parentMenu,
            parentButton = parentStackButton
            )
        parentStackButton.setDefaultAction(action)

    def createContextMenu(self, position):
        """
        Creates the flag menu
        """
        menu = QMenu()
        item = self.tableView.indexAt(position)
        if item:
            menu.addAction(self.tr('Zoom to flag'), self.zoomToFlag)
            menu.addAction(self.tr('Remove flag'), self.removeCurrentFlag)
        menu.exec_(self.tableView.viewport().mapToGlobal(position))
        
    
    def removeCurrentFlag(self):
        """
        Creates the remove flag menu
        """
        try:
            flagId = self.tableView.selectionModel().selection().indexes()[0].data()
        except:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('No flags were selected!'))
            return
        self.connectionSelectorComboBox.abstractDb.deleteProcessFlags(flagId = flagId)
        self.refreshFlags()
    
    def zoomToFlag(self):
        """
        Zooms the map canvas to the current selected flag
        """
        try:
            idx =  self.tableView.selectionModel().selection().indexes()[0].data()
        except:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('No flags were selected!'))
            return
        dimension = self.tableView.selectionModel().selection().indexes()[6].data()
        if dimension == 0:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOINT', 'lyrName': 'flags_validacao_p', 'tableName':'aux_flags_validacao_p', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}            
        elif dimension == 1:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTILINESTRING', 'lyrName': 'flags_validacao_l', 'tableName':'aux_flags_validacao_l', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}
        elif dimension == 2:
            layer = {'cat': 'aux', 'geom': 'geom', 'geomType':'MULTIPOLYGON', 'lyrName': 'flags_validacao_a', 'tableName':'aux_flags_validacao_a', 'tableSchema':'validation', 'tableType': 'BASE TABLE'}            
        flagLyr = self.loadFlagLyr(layer)
        flagLyr.setOpacity(50)
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
        self.layerLoader = LayerLoaderFactory().makeLoader(self.iface,self.connectionSelectorComboBox.abstractDb)
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
            if self.connectionSelectorComboBox.abstractDb.isLyrInDb(lyr):
                return True
        return False

    @pyqtSlot(bool)
    def on_historyButton_clicked(self):
        """
        Shows the validation history
        """
        historyWindow = ValidationHistory(self.connectionSelectorComboBox.abstractDb)
        historyWindow.exec_()
    
    @pyqtSlot()
    def updateDbLineEdit(self):
        """
        Updates the database information
        """
        database = ''
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.connectionSelectorComboBox.abstractDb.checkAndOpenDb()
            self.validationManager = ValidationManager(self.connectionSelectorComboBox.abstractDb, self.iface)
            # adjusting flags table model
            self.projectModel = QSqlTableModel(None,self.connectionSelectorComboBox.abstractDb.db)
            self.projectModel.setTable('validation.aux_flags_validacao')
            self.projectModel.select()
            self.tableView.setModel(self.projectModel)
            QApplication.restoreOverrideCursor()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(self.tr('Error loading db: ')+':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
            self.processTreeWidget.clear()    

    def on_filterLineEdit_textChanged(self, text):
        for i in self.itemList:
            if text.lower() in i.text(0).lower():
                i.setHidden(False)
            else:
                i.setHidden(True)
    
    def addCategories(self, rootItem):
        for key, value in self.categoriesDict.items():
            item = QTreeWidgetItem(rootItem)
            item.setText(0, value['categoryAlias'])
            value['categoryNode'] = item
    
    def populateProcessTreeList(self):
        """
        Populates process tree list, according to the category of the process
        """
        self.processTreeWidget.clear()
        rootItem = self.processTreeWidget.invisibleRootItem()
        self.addCategories(rootItem)
        self.itemList = []
        
        procList = sorted(self.validationManager.processList, key=itemgetter('alias'))
        for procItem in procList:
            item = QTreeWidgetItem(self.categoriesDict[procItem['category']]['categoryNode'])
            item.setText(0, procItem['alias'])
            self.categoriesDict[procItem['category']]['processList'].append(procItem)
            self.itemList.append(item)
        self.filterLineEdit.clear()

    @pyqtSlot(bool)
    def on_reRunButton_clicked(self):
        """
        Re-runs last process with the same attributes.
        """
        if not self.validationManager:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to run process!'))
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            procReturn = self.validationManager.runLastProcess()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
            procReturn = 0
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Process error. Check log for details.'))
        elif procReturn == -1:
            QMessageBox.information(self, self.tr('Information!'), self.tr('Process canceled by user!'))
        elif procReturn == -2:
            QMessageBox.information(self, self.tr('Information!'), self.tr('No previous process run this session.'))
        else:
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!

    @pyqtSlot(bool)
    def on_runButton_clicked(self):
        """
        Runs the current selected process
        """
        selectedItems = self.processTreeWidget.selectedItems()
        if len(selectedItems) == 0:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a process to run!'))
            return
        processName = selectedItems[0].text(1)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            procReturn = self.validationManager.executeProcessV2(processName)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
            procReturn = 0
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Process error. Check log for details.'))
        elif procReturn == -1:
            QMessageBox.information(self, self.tr('Information!'), self.tr('Process canceled by user!'))
        else:
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!
            #load flag layers
            self.loadAllFlagLayers()
        self.iface.mapCanvas().refresh() #atualizar canvas para mostrar resultado para o usuário

    @pyqtSlot(int, name='on_validationTabWidget_currentChanged')
    def refreshFlags(self):
        """
        Changes the current tab in the validation tool box
        """
        if self.validationTabWidget.currentIndex() == 1 and self.connectionSelectorComboBox.abstractDb != None:
            self.projectModel.select()
        self.refreshOnChangeProcessOrClass()

    @pyqtSlot(bool)
    def on_rulesEditorButton_clicked(self):
        """
        Opens the spatial rule editor
        """
        try:
            self.connectionSelectorComboBox.abstractDb.checkAndOpenDb()
            dlg = RulesEditor(self.connectionSelectorComboBox.abstractDb)
            dlg.exec_()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database not loaded or a problem occurred.\n')+':'.join(e.args))

    @pyqtSlot(int, name = 'on_customFilterComboBox_currentIndexChanged')
    def refreshFlagListOnClassProcessSelection(self):        
        """
        Refreshs the list of Classes or Processes accordingly to the
        type of filter chosen
        """
        filterType = self.filterTypeComboBox.currentText()
        filteredElement = self.customFilterComboBox.currentText()
        self.connectionSelectorComboBox.abstractDb.createFilteredFlagsViewTable(filterType=filterType, filteredElement=filteredElement)
        self.projectModel.setTable('validation.filtered_flags')
        self.projectModel.select()
        
    @pyqtSlot(int, name = 'on_filterTypeComboBox_currentIndexChanged')
    def refreshOnChangeProcessOrClass(self):
        """
        Refreshs the list of processes or classes available 
        for filtering the view
        """
        filterType = self.filterTypeComboBox.currentText()
        self.customFilterComboBox.clear()
        if self.connectionSelectorComboBox.abstractDb:
            listProcessesOrClasses = self.connectionSelectorComboBox.abstractDb.fillComboBoxProcessOrClasses(filterType)
            self.customFilterComboBox.addItems(listProcessesOrClasses)    

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
            self.connectionSelectorComboBox.abstractDb.checkAndOpenDb()
            dlg = AttributeRulesEditor(self.connectionSelectorComboBox.abstractDb)
            dlg.exec_()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Database not loaded or a problem occurred.\n')+':'.join(e.args))

    @pyqtSlot(bool)
    def on_clearAllPushButton_clicked(self):
        """
        Deletes all flags from validation.aux_flags
        1- Get abstractDb
        2- Delete flag
        """
        try:
            if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to clear all flags?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                return
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.connectionSelectorComboBox.abstractDb.deleteProcessFlags()
            QApplication.restoreOverrideCursor()
            #refresh
            self.refreshFlags()
            self.iface.mapCanvas().refresh()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted.\n')+':'.join(e.args))

    @pyqtSlot(bool)
    def on_clearSelectedPushButton_clicked(self):
        """
        Deletes selected flags on the panel from validation.aux_flags
        """
        try:
            if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to clear those flags?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                return
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            filterType = self.filterTypeComboBox.currentText()
            processName, layerName = None, None
            # check what is filtered
            if self.filterDict[filterType] == DsgEnums.ProcessName:
                processName = self.customFilterComboBox.currentText()
            elif self.filterDict[filterType] == DsgEnums.ClassName:
                layerName = self.customFilterComboBox.currentText()
            if (processName or layerName):
                self.connectionSelectorComboBox.abstractDb.deleteProcessFlags(processName,layerName)
            else:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted as no Process nor Class was chosen.\n'))
                return
            QApplication.restoreOverrideCursor()
            # refresh View Table with lasting flags
            self.refreshFlags()
            self.iface.mapCanvas().refresh()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Flags not deleted.\n')+':'.join(e.args))
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_processTreeWidget_itemDoubleClicked(self, item, column):
        if item.parent():
            print(item.text(0))
