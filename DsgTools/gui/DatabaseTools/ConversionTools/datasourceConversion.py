# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-05
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from functools import partial
import os, json

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from qgis.PyQt.QtGui import QIcon, QCursor
from qgis.utils import iface
from qgis.core import Qgis, QgsApplication, QgsMessageLog, Qgis
from qgis.gui import QgsCollapsibleGroupBox, QgsMessageBar

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.genericDialogLayout import GenericDialogLayout
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.textBrowserDialog import TextBrowserDialog
from DsgTools.core.DbTools.dbConverter import DbConverter

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceConversion.ui'))

class DatasourceConversion(QtWidgets.QWizard, FORM_CLASS):
    # enum for column ordering
    COLUMN_COUNT = 7
    # InDs, Filter, SpatialFilterFanOut, InEdgv, OutDs, OutEdgv, outCrs, ConversionMode = list(range(COLUMN_COUNT))
    InDs, Filter, InEdgv, OutDs, OutEdgv, outCrs, ConversionMode = list(range(COLUMN_COUNT))

    def __init__(self, manager, parentMenu, parentButton, parent=None):
        """
        Class constructor.
        :param manager:
        :param parentMenu: menu to which conversion tool will be listed
        :param parent: (QWidget) widget parent to a datasource conversion GUI widget.
        """
        super(DatasourceConversion, self).__init__()
        self.setupUi(self)
        # self.setTitle(self.tr('Datasource Conversion Wizard'))
        self.manager = manager
        self.parentMenu = parentMenu
        self.parentButton = parentButton
        # fill output datasources including new datasources options
        self.datasourceManagementWidgetOut.fillSupportedDatasources(inputPage=False)
        self.connectToolSignals()
        # initiate widget dicts
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)
        # set table to its initial state
        self.resetTable(enabled=True)
        # set pages titles
        self.page(0).setTitle(self.tr('Input Datasources'))
        self.page(1).setTitle(self.tr('Output Datasources'))
        self.page(2).setTitle(self.tr('Conversion Map and Summary'))
        # set policy to make cell size adjust to content
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        
    def connectToolSignals(self):
        """
        Connects all tool generic signals.
        """
        # if any widget was turned active/inactive
        self.datasourceManagementWidgetIn.activeWidgetAdded.connect(self.addInputDatasource)
        self.datasourceManagementWidgetOut.activeWidgetAdded.connect(self.addOutputDatasource)
        self.datasourceManagementWidgetIn.activeWidgetRemoved.connect(self.removeInputDatasource)
        self.datasourceManagementWidgetOut.activeWidgetRemoved.connect(self.removeOutputDatasource)
        # if datasource is changed (e.g. user changed his postgis database selection, for instance)
        self.datasourceManagementWidgetIn.widgetUpdated.connect(self.updateInputInformation)
        self.datasourceManagementWidgetOut.widgetUpdated.connect(self.updateOutputInformation)
        # erase all options settled
        self.refreshPushButton.clicked.connect(self.setTableInitialState)
        # conversion mapping start
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.startConversion)

    def disconnectToolSignals(self):
        """
        Connects all tool generic signals.
        """
        # if any widget was turned active/inactive
        self.datasourceManagementWidgetIn.activeWidgetAdded.disconnect(self.addInputDatasource)
        self.datasourceManagementWidgetOut.activeWidgetAdded.disconnect(self.addOutputDatasource)
        self.datasourceManagementWidgetIn.activeWidgetRemoved.disconnect(self.removeInputDatasource)
        self.datasourceManagementWidgetOut.activeWidgetRemoved.disconnect(self.removeOutputDatasource)
        # if datasource is changed (e.g. user changed his postgis database selection, for instance)
        self.datasourceManagementWidgetIn.widgetUpdated.disconnect(self.updateInputInformation)
        self.datasourceManagementWidgetOut.widgetUpdated.disconnect(self.updateOutputInformation)
        self.refreshPushButton.clicked.disconnect(self.setTableInitialState)
        self.button(QtWidgets.QWizard.FinishButton).clicked.disconnect(self.startConversion)

    def getWidgetNameDict(self, d):
        """
        Gets the name translated into widget dict from a given dict.
        :param d: (dict) dictionary  - { (str)driver : (DatasourceContainerWidget)widget } - to have its widgets translated.
        :return: (dict) translated dict - { (str)datasource_name : (DatasourceContainerWidget)widget }.
        """
        returnDict = dict()
        for k in d:
            for containerWidget in d[k]:
                returnDict[containerWidget.groupBox.title()] = containerWidget
        return returnDict

    def replicateFirstRowContent(self, col):
        """
        Replicates first row value to all the other rows from a selected column.
        :param col: (int) column to have its first row replicated.
        """
        if col in [DatasourceConversion.OutDs, DatasourceConversion.ConversionMode]: #, DatasourceConversion.SpatialFilterFanOut]:
            value = None
            for row in range(self.tableWidget.rowCount()):
                widget = self.getRowContents(row=row)[col]
                if widget.isEnabled():
                    if value is None:
                        # # if widget is enabled, capture its value
                        # if col == DatasourceConversion.SpatialFilterFanOut:
                        #     value = self.getRowContents(row=row)[col].isChecked()
                        # else:
                        value = widget.currentText()
                    else:
                        # if value is captured from first activated widget, set it to all following activated widgets
                        # # if widget is active, set its value
                        # if col == DatasourceConversion.SpatialFilterFanOut:
                        #     widget.setChecked(value)
                        # else:
                        widget.setCurrentText(value)

    def resetTable(self, enabled=False):
        """
        Resets table to initial state.
        :param enabled: (bool) indicates whether table will be enabled.
        """
        # clear possible content in it
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(row)
        self.tableWidget.setEnabled(enabled)
        self.tableWidget.setColumnCount(DatasourceConversion.COLUMN_COUNT)
        # if a signal issue comes along, maybe cell shoul've been systematically removed
        # and signals disconnect for each row along. So that's where shit might be re-coded (=
        self.tableWidget.setRowCount(0)
        # map header to its enum
        headerDict = {
            DatasourceConversion.InDs : self.tr("Input"),
            DatasourceConversion.Filter : self.tr("Filters"),
            # DatasourceConversion.SpatialFilterFanOut : self.tr("Spatial Fan-out"),
            DatasourceConversion.InEdgv : self.tr("In: EDGV Version"),
            DatasourceConversion.OutDs : self.tr("Output"),
            DatasourceConversion.outCrs : self.tr("Out: CRS"),
            DatasourceConversion.OutEdgv : self.tr("Out: EDGV Version"),
            DatasourceConversion.ConversionMode : self.tr("Conversion Mode")
        }
        # make the order always follow as presented at enum
        self.tableWidget.setHorizontalHeaderLabels(list([headerDict[i] for i in range(DatasourceConversion.COLUMN_COUNT)]))
        # connect header double click signal to first row contents replicate to the other rows
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.replicateFirstRowContent)

    def addInputDatasource(self, containerWidget, resizeColumns=True):
        """
        Adds a row to table with an input container widget's informaation.
        :param containerWidget:
        :param resizeColumns: (bool)
        """
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)
        # create a 'function' to get datasource exposing name and create the output list
        getNameAlias = lambda widget : '{0}: {1}'.format(widget.groupBox.title(), widget.getDatasourceConnectionName())
        # use it in a map loop to get output list
        outDsList = [self.tr('Select a datasource')] + sorted(list(map(getNameAlias, self.outDs.values())))
        # update table rows #
        lastRow = self.tableWidget.rowCount()
        self.tableWidget.insertRow(lastRow)
        # crsIcon = QIcon(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'icons', 'CRS_qgis.svg'))
        # create the item containing current loop's input ds
        t = '{0}: {1}'.format(containerWidget.groupBox.title(), containerWidget.getDatasourceConnectionName())
        self.addItemToTable(col=DatasourceConversion.InDs, row=lastRow, text=t, isEditable=False)
        # populate edgv versions column
        # input is always text
        t = containerWidget.connectionWidget.getDatasourceEdgvVersion()
        self.addItemToTable(col=DatasourceConversion.InEdgv, row=lastRow, text=t, isEditable=False)
        # create filter push button
        filterPushButton = QtWidgets.QPushButton()
        filterPushButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'icons', 'filter.png'))
        )
        # # create  push button
        # fanOutCheckBox = QtWidgets.QCheckBox()
        # # set enable status if necessary
        # fanOutCheckBox.setEnabled(bool(containerWidget.filters()['spatial_filter']))
        # # add tooltip to it
        # fanOutCheckBox.setToolTip(self.tr('Fan-out by filtered features from reference layer'))
        # create the combobox containing all output ds
        outDsComboBox = QtWidgets.QComboBox()
        outDsComboBox.addItems(outDsList)
        # create combobox containing conversion mode options
        convModeComboBox = QtWidgets.QComboBox()
        convModeComboBox.addItems([
            self.tr('Choose Conversion Mode'), self.tr('Flexible Conversion'), self.tr('Strict Conversion')
        ])
        # set each widget to their column
        self.tableWidget.setCellWidget(lastRow, DatasourceConversion.OutDs, outDsComboBox)
        self.tableWidget.setCellWidget(lastRow, DatasourceConversion.Filter, filterPushButton)
        # self.tableWidget.setCellWidget(lastRow, DatasourceConversion.SpatialFilterFanOut, fanOutCheckBox)
        self.tableWidget.setCellWidget(lastRow, DatasourceConversion.ConversionMode, convModeComboBox)
        # start filter widget
        filterPushButton.clicked.connect(partial(self.prepareRowFilterDialog, container=containerWidget))
        # set table output information population to its widget
        outDsComboBox.currentIndexChanged.connect(partial(self.fillOutDsInfoRow, row=lastRow))
        if resizeColumns:
            # resize to contents
            self.tableWidget.resizeColumnsToContents()

    def removeInputDatasource(self, containerWidget):
        """
        Removes the map table row containing a given input information.
        :param containerWidget: (DatasourceContainerWidget) input container widget. 
        """
        row, _ = self.getInputDatasourceRow(inputDatasourceWidget=containerWidget)
        self.tableWidget.removeRow(row)
        # after the row is removed, it is also necessary to update datasources names, given that group boxes were renamed
        for row in range(self.tableWidget.rowCount()):
            inDs = self.getRowContents(row=row)[DatasourceConversion.InDs]
            widget = self.inDs[inDs.split(':')[0]]
            t = '{0}: {1}'.format(widget.groupBox.title(), widget.getDatasourceConnectionName())
            self.addItemToTable(col=DatasourceConversion.InDs, row=row, text=t, isEditable=False)
        # update input map - if map was updated before it would not be possible to retrieve widget (name changed)
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)

    def addOutputDatasource(self, containerWidget):
        """
        Updates datasource options for every row in table widget.
        :param containerWidget: (DatasourceContainerWidget) output container widget. 
        """
        # update output map
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        # get new datasource info
        dsName = '{0}: {1}'.format(containerWidget.groupBox.title(), containerWidget.getDatasourceConnectionName())
        for row in range(self.tableWidget.rowCount()):
            outCombobox = self.getRowContents(row=row)[DatasourceConversion.OutDs]
            outCombobox.addItem(dsName)

    def removeOutputDatasource(self, containerWidget):
        """
        Removes output option from evey row in table widget. 
        :param containerWidget: (DatasourceContainerWidget) output container widget. 
        """
        # update output map
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        # get new datasource info
        getNewDsNames = lambda widget : '{0}: {1}'.format(widget.groupBox.title(), widget.getDatasourceConnectionName())
        newDsNames = [self.tr('Select a datasource')] + sorted(list(map(getNewDsNames, self.outDs.values())))
        groupTitle = containerWidget.groupBox.title()
        # initiate its index
        dsIdx = None
        for row in range(self.tableWidget.rowCount()):
            outDsCombobox = self.getRowContents(row=row)[DatasourceConversion.OutDs]
            if outDsCombobox:
                # retrieve replaced datasource old index
                if dsIdx is None:
                    # retrive old name
                    oldName = ''
                    for i in range(outDsCombobox.count()):
                        if groupTitle in outDsCombobox.itemText(i):
                            oldName = outDsCombobox.itemText(i)
                            # once name is retrieved, cycle is no longer needed
                            break
                    # the order is the same for all rows
                    dsIdx = outDsCombobox.findText(oldName)
                # identify whether previous selection was the same as the one that changed
                currentSelectionChanged = outDsCombobox.currentIndex() == dsIdx
                if not currentSelectionChanged:
                    currentText = outDsCombobox.currentText()
                # update list of output comboboxes
                outDsCombobox.blockSignals(True)
                outDsCombobox.clear()
                outDsCombobox.addItems(newDsNames)
                outDsCombobox.blockSignals(False)
                # check if current selection is the one to be removed
                if currentSelectionChanged:
                    dsName = getNewDsNames(containerWidget)
                    # if current selection is the removed output, set selection to 0 index
                    outDsCombobox.setCurrentText(dsName)
                else:
                    outDsCombobox.setCurrentText(currentText)

    def updateInputInformation(self, containerWidget):
        """
        Updates input information.
        :param containerWidget: (DatasourceContainerWidget) input container widget. 
        """
        # update input map
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)
        # get input row
        row, _ = self.getInputDatasourceRow(inputDatasourceWidget=containerWidget)
        # get new datasource info
        dsName = '{0}: {1}'.format(containerWidget.groupBox.title(), containerWidget.getDatasourceConnectionName())
        inEdgv = containerWidget.connectionWidget.getDatasourceEdgvVersion()
        # update edgv and input name
        self.addItemToTable(col=DatasourceConversion.InDs, row=row, text=dsName, isEditable=False)
        self.addItemToTable(col=DatasourceConversion.InEdgv, row=row, text=inEdgv, isEditable=False)

    def updateOutputInformation(self, containerWidget):
        """
        Updates input information.
        :param containerWidget: (DatasourceContainerWidget) output container widget. 
        """
        # update output map
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        # get new datasource info
        groupTitle = containerWidget.groupBox.title()
        dsName = '{0}: {1}'.format(groupTitle, containerWidget.getDatasourceConnectionName())
        outEdgv = containerWidget.connectionWidget.getDatasourceEdgvVersion()
        # initiate its index
        dsIdx = None
        for row in range(self.tableWidget.rowCount()):
            outDsCombobox = self.getRowContents(row=row)[DatasourceConversion.OutDs]
            if outDsCombobox:
                # retrieve replaced datasource old index
                if dsIdx is None:
                    # retrive old name
                    oldName = ''
                    for i in range(outDsCombobox.count()):
                        if groupTitle in outDsCombobox.itemText(i):
                            oldName = outDsCombobox.itemText(i)
                            # once name is retrieved, cycle is no longer needed
                            break
                    # the order is the same for all rows
                    dsIdx = outDsCombobox.findText(oldName)
                outDsCombobox.setItemText(dsIdx, dsName)
                # update output info, if current selection is the same as before
                # check if current selection is the one to be removed
                if outDsCombobox.currentIndex() == dsIdx:
                    # if current selection is the removed output, set selection to 0 index
                    outDsCombobox.setCurrentIndex(dsIdx)

    def getRowContents(self, row):
        """
        Retrieves all filled row info.
        :param row: (int) row index to have its output columns populated.
        :return: (list-of-object) a list of all information found on a given row (may be a widget or string).
        """
        # input datasource, input and output EDGV versions are always a text
        inDs = self.tableWidget.item(row, DatasourceConversion.InDs).text()
        inEdgv = self.tableWidget.item(row, DatasourceConversion.InEdgv).text()
        outEdgvItem = self.tableWidget.item(row, DatasourceConversion.OutEdgv)
        outEdgv = outEdgvItem.text() if outEdgvItem else ''
        conversionMode = self.tableWidget.cellWidget(row, DatasourceConversion.ConversionMode)
        # output datasource, input and output SRC and filter status are always a QWidget
        outDs = self.tableWidget.cellWidget(row, DatasourceConversion.OutDs)
        # however, output info might not yet have been filled
        try:
            _filter = self.tableWidget.cellWidget(row, DatasourceConversion.Filter)
        except:
            _filter = None
        # try:
        #     spatialFanOut = self.tableWidget.cellWidget(row, DatasourceConversion.SpatialFilterFanOut)
        # except:
        #     spatialFanOut = None
        try:
            outCrs = self.tableWidget.cellWidget(row, DatasourceConversion.outCrs)
        except:
            outCrs = None
        # return [inDs, _filter, spatialFanOut, inEdgv, outDs, outEdgv, outCrs, conversionMode]
        return [inDs, _filter, inEdgv, outDs, outEdgv, outCrs, conversionMode]

    def getInputDatasourceRow(self, inputDatasourceWidget):
        """
        Returns row containing given input datasource container widget.
        :param inputDatasourceWidget: (DatasourceContainerWidget) input container widget.
        :return: (tuple-of-objects) row number containing target input datasource and row contents.
                                    If not found, -1 and an empty list are returned.
        """
        inputText = inputDatasourceWidget.groupBox.title()
        for row in range(self.tableWidget.rowCount()):
            # inDs, _filter, spatialFanOut, inEdgv, outDs, outEdgv, outCrs, conversionMode = self.getRowContents(row=row)
            inDs, _filter, inEdgv, outDs, outEdgv, outCrs, conversionMode = self.getRowContents(row=row)
            if inputText in inDs:
                # return row, [inDs, _filter, spatialFanOut, inEdgv, outDs, outEdgv, outCrs, conversionMode]
                return row, [inDs, _filter, inEdgv, outDs, outEdgv, outCrs, conversionMode]
        return -1, []


    def clearOutDsInforRow(self, row):
        """
        Clears output information for a given row.
        :param row: (int) row to have its output info cleared.
        """
        # add an empty item to it
        self.addItemToTable(col=DatasourceConversion.OutEdgv, row=row, isEditable=False)
        outCrsPb = self.getRowContents(row=row)[DatasourceConversion.outCrs]
        if outCrsPb:
            outCrsPb.setEnabled(False)

    def fillOutDsInfoRow(self, row):
        """
        Fills out row with output info for each output column. In here, ouput SRC and EDGV are filled. 
        :param row: (int) row index to have its output columns populated.
        :return: (list-of-object) return a list containing (str) output EDGV version and (QPushButton) output SRC.
        """
        # clear current content, if any
        try:
            self.clearOutDsInforRow(row=row)
        except:
            pass
        # get only outDs widget
        outDs = self.getRowContents(row=row)[DatasourceConversion.OutDs]
        # widget dict keys are defined as group title, which is part of outDs current text
        if outDs:
            groupTitle = outDs.currentText().split(':')[0]
            crsIcon = QIcon(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'icons', 'CRS_qgis.svg'))
        else:
            return []
        if groupTitle in self.outDs:
            containerWidget = self.outDs[groupTitle]
            # only fills line if dictionary is a controlled widget
            # new push button for SRC
            outCrs = QtWidgets.QPushButton()
            outCrs.setIcon(crsIcon)
            # get new text item to add output datasource
            edgvOut = containerWidget.connectionWidget.getDatasourceEdgvVersion()
            edgvOut = edgvOut[5:] if 'EDGV' in edgvOut else edgvOut
            itemEdgvOut = QtWidgets.QTableWidgetItem()
            itemEdgvOut.setText(edgvOut)
            itemEdgvOut.setFlags(Qt.ItemIsEditable) # not editable
            # add both to table
            self.tableWidget.setCellWidget(row, DatasourceConversion.outCrs, outCrs)
            self.tableWidget.setItem(row, DatasourceConversion.OutEdgv, itemEdgvOut)
            return [edgvOut, outCrs]
        else:
            # if is not controlled, clear line
            return []

    def getNewTableItem(self, text='', isEditable=True):
        """
        Gets an item to be added to the table that may be set to not be editable.
        :param text: (str) name to be exposed on table cell.
        :param isEditable: (bool) boolean indicating whether cell content should be editable.
        :return: (QTableWidgetItem) item to be added as a table cell.
        """
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        if not isEditable:
            item.setFlags(Qt.ItemIsEditable) # not editable
        return item

    def addItemToTable(self, col, row, text='', isEditable=True):
        """
        Adds an item to the mapping table into a given column and row.
        :param col: (int) column containing new item.
        :param row: (int) row containing new item.
        :param text: (str) name to be exposed on table cell.
        :param isEditable: (bool) boolean indicating whether cell content should be editable.
        :return: (QTableWidgetItem) item added.
        """
        newItem = self.getNewTableItem(text=text, isEditable=isEditable)
        self.tableWidget.setItem(row, col, newItem)
        return newItem

    def prepareRowFilterDialog(self, container):
        """
        Prepares filter dialog for current dataset in a given row.
        :param container: (DatasourceContainerWidget) container widget added to the GUI.
        """
        if container.filterDlg is None:
            container.refreshFilterDialog()
        container.filterDlg.enableEdition(False)
        container.filterDlg.okPushButton.hide()
        container.filterDlg.cancelPushButton.hide()
        container.on_filterPushButton_clicked()
        container.filterDlg.okPushButton.show()
        container.filterDlg.cancelPushButton.show()
        container.filterDlg.enableEdition(True)

    def setTableInitialState(self):
        """
        Sets the mapping table to its initial (populated) state. Each row is composed by input datasource name, widget with
        all output datasource and conversion mode (whether -9999 would be set to all non-null restriction not respected).
        """
        self.resetTable(enabled=True)
        # output ds dict/list
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        # create a 'function' to get datasource exposing name and create the output list
        getNameAlias = lambda widget : '{0}: {1}'.format(widget.groupBox.title(), widget.getDatasourceConnectionName())
        outDsList = [self.tr('Select a datasource')] + sorted(list(map(getNameAlias, self.outDs.values())))
        # input ds dict/list
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)
        for groupTitle in sorted(self.inDs.keys()):
            self.addInputDatasource(containerWidget=self.inDs[groupTitle], resizeColumns=False)
        self.tableWidget.resizeColumnsToContents()

    def getConversionMap(self):
        """
        Creates the conversion map JSON based on table widget contents.
        :return: (dict) the conversion map. (SPECIFY FORMAT!)
        """
        # initiate conversion map dict
        conversionMap = dict()
        # get the row count from table widget and iterate over it
        for row in range(self.tableWidget.rowCount()):
            # get row contents
            # inDs, _, spatialFanOut, _, outDs, _, _, conversionMode = self.getRowContents(row=row)
            inDs, _, _, outDs, _, _, conversionMode = self.getRowContents(row=row)
            # initiate this row's mapping dict and fill it
            rowMapping = dict()
            # get input information to be mapped - input datasource identification and filtering options
            containerWidget = self.inDs[inDs.split(':')[0]] # input group box title (widget's dict key)
            inputDatasourceId =  containerWidget.connectionWidget.getDatasourcePath()
            inputFilteredLayers = containerWidget.filters()
            # get output information to be mapped - output datasource identification and if it's
            containerWidget = self.outDs[outDs.currentText().split(':')[0]] # output group box title (widget's dict key)
            # populate row's conversion map
            rowMapping['outDs'] = containerWidget.connectionWidget.getDatasourcePath(),  # still to decide what to fill up in here
            rowMapping['outDs'] = rowMapping['outDs'][-1] # I DON'T KNOW WHY, BUT THAT'S THE ONLY WAY THIS COMES OUT AS A TUPLE.
            rowMapping['filter'] = inputFilteredLayers
            # rowMapping['spatialFanOut'] = spatialFanOut.isChecked()
            # parameter indicating whether it is a new datasource
            rowMapping['createDs'] = self.tr('new') in outDs.currentText().split(':')[0]
            if self.tr('new') in outDs.currentText().split(':')[0]:
                # if a new datasource will be created, EDGV version and CRS will be needed
                rowMapping['edgv'] = containerWidget.connectionWidget.selectionWidget.edgvVersion()
                rowMapping['crs'] = containerWidget.connectionWidget.selectionWidget.authId()
            rowMapping['conversionMode'] = conversionMode.currentIndex()
            # it is possible for the same dataset to be chosen for different outputs, in order to prevent instantiating it
            # more than once, map it all to the same dict entry and control layer/feature flux through filter entry
            if inputDatasourceId not in conversionMap:
                # setting the conversion map key to input datasource path will secure that conversions using the same ds
                # as data origin will make it be read only once
                conversionMap[inputDatasourceId] = [rowMapping]
            else:
                conversionMap[inputDatasourceId].append(rowMapping)
        return conversionMap

    def getParameterDict(self):
        """
        Gets the conversion parameter dict. Alias for getConversionMap().
        :return: (dict) the conversion map. (SPECIFY FORMAT!)
        """
        return self.getConversionMap()

    def exportConversionJson(self, filepath=None):
        """
        Exports conversion mapping structure to a JSON file.
        :param filepath: (str) file path for output JSON mapping file.
        """
        conversionMap = self.getConversionMap()
        if not filepath:
            filepath = os.path.join(os.path.dirname(__file__), 'conversion_map.json')
        with open(filepath, 'w') as fp:
            json.dump(conversionMap, fp, indent=4, sort_keys=True)

    def validateJson(self, inputJson):
        """
        Validates JSON file containing conversion mapping parameters.
        :param inputJson: (str) JSON file path.
        :return: (bool) whether JSON is valid.
        """
        conversionMap = json.loads(inputJson)
        pass

    @staticmethod
    def checkEdgvConversion(edgvIn, edgvOut):
        """
        Checks if the mapping conversion is available. It is an static method as one
        might want to check conversion maps availability regardless to be executing it.
        :param edgvIn: (str) input EDGV version.
        :param edgvOut: (str) output EDGV version.
        """
        # TO DO
        return edgvIn == edgvOut and edgvOut != ''

    def validate(self):
        """
        Verifies contents displayed on mapping table in order to infer its validity
        as datasource conversion map.
        :return: (bool) map validity status.
        """
        # validate map
        msg = self.invalidatedReason()
        if msg:
            # if an invalidation reason was given, warn user and nothing else.
            msgBar = QgsMessageBar(self)
            # if window is resized, msgBar stays, not ideal, but works for now
            # maybe we should connect to some parent resizing signal or something...
            msgBar.resize(QSize(self.geometry().size().width(), msgBar.geometry().height()))
            msgBar.pushMessage(self.tr('Warning!'), msg, level=Qgis.Warning, duration=5)
            QgsMessageLog.logMessage(msg, 'DSGTools Plugin', Qgis.Critical)
        return msg == ''

    def validateCurrentPage(self):
        """
        Reimplementation of QWizard's method.
        """
        if self.currentId() == 2:
            return self.validate()
        # validation per page may be added in here
        return True

    def invalidatedReason(self):
        """
        Verifies contents displayed on mapping table in order to infer its validity
        as datasource conversion map.
        :return: (str) invalidation reason.
        """
        if self.tableWidget.rowCount() == 0:
            return self.tr("No datasets were selected (input or output)")
        for obj in [self.datasourceManagementWidgetIn, self.datasourceManagementWidgetOut]:
            # validate in/ouput
            msg = obj.validate()
            if msg:
                return msg
        # lists of inputs/outputs already checked
        inChecked, outChecked = [], set()
        # it is assumed that containers' contents were already checked previously
        for row in range(self.tableWidget.rowCount()):
            # get row contents
            # inDsName, _, _, inEdgv, outDs, _, outEdgv, conversionMode = self.getRowContents(row=row)
            inDsName, _, inEdgv, outDs, outEdgv, _, conversionMode = self.getRowContents(row=row)
            outDsName = outDs.currentText()
            # FTer was discontinued. conv should not allow dataset creation for this EDGV version
            if outEdgv == 'EDGV 2.1.3 F Ter' and self.tr('new') in outDsName.split(' #')[0]:
                return self.tr('EDGV 2.1.3 F Ter model was terminated. DSGTools no longer support its creation (row {1})').format(inDsName, row + 1)
            # check if a conversion mode was selected
            if conversionMode.currentText() == self.tr('Choose Conversion Mode'):
                return self.tr('Conversion mode not selected for input {0} (row {1})').format(inDsName, row + 1)
            # check if EDGV versions are compatible
            if not self.checkEdgvConversion(edgvIn=inEdgv, edgvOut=outEdgv):
                return self.tr('Conversion map unavailable for {0} to {1} (row {2})').format(inEdgv, outEdgv, row + 1)
            # # add input to the checked ones list
            # inChecked.append(inDsName)
            # add output to checked ones list, if it's not 'select a datasource'
            if outDsName == self.tr('Select a datasource'):
                return self.tr('Output datasource not selected for {0} (row {1})').format(inDsName, row + 1)
            outChecked.add(outDsName)
        # last check: if all chosen outputs are listed
        splitAlias = lambda x : x.split(':')[0]
        if len(outChecked) != len(self.outDs):
            # if not all outputs were used, user should remove it (or may have wrongfully chosen a different dataset)
            notUsed = set(self.outDs.keys()) - set(map(splitAlias, outChecked))
            msg = self.tr('Output datasource {0} was not used.') if len(notUsed) == 1 else self.tr('Output datasources {0} were not used.')
            return msg.format(", ".join(notUsed))
        return ''

    def cancelConversion(self, conversionTask, summaryDlg):
        """
        Cancels a conversion task.
        :param conversionTask: (DbConverter) conversion task to be cancelled.
        :param summaryDlg: (TextBrowserDialog) dialog in which task's log is directed to.
        """
        if not conversionTask.feedback.isCanceled():
            conversionTask.feedback.cancel()
            summaryDlg.cancelPushButton.setEnabled(False)
            conversionTask.blockSignals(True)
            summaryDlg.progressBar.setValue(0)
            summaryDlg.addToHtml(self.tr('<span style="color: #ff0000;"><br><p>CONVERSION TASK WAS CANCELLED.</span></p>'))
            summaryDlg.savePushButton.setEnabled(True)

    def run(self, conversionMap):
        """
        Executes conversion itself based on a conversion map.
        :param conversionMap: (dict) the conversion map. (SPECIFY FORMAT!)
        """
        # task = DbConverter(iface, conversionMap, description=self.tr('DSGTools Dataset Conversion'))
        # summaryDlg = TextBrowserDialog(parent=iface.mainWindow())
        # summaryDlg.savePushButton.setEnabled(False)
        # task.progressChanged.connect(summaryDlg.progressBar.setValue)
        # task.taskCompleted.connect(lambda : summaryDlg.setHtml(task.output['log']))
        # task.taskCompleted.connect(lambda : summaryDlg.cancelPushButton.setEnabled(False))
        # task.taskCompleted.connect(lambda : summaryDlg.savePushButton.setEnabled(True))
        # task.conversionUpdated.connect(summaryDlg.addToHtml)
        # summaryDlg.cancelPushButton.clicked.connect(partial(self.cancelConversion, task, summaryDlg))
        # # to clear log message before repopulating with conversion summary
        # task.conversionFinished.connect(summaryDlg.clearHtml)
        # QgsApplication.taskManager().addTask(task)
        # summaryDlg.show()
        # conversion off the thread
        conv = DbConverter(iface, conversionMap, description=self.tr('DSGTools Dataset Conversion'))
        summaryDlg = TextBrowserDialog(parent=iface.mainWindow())
        summaryDlg.cancelPushButton.hide()
        summaryDlg.progressBar.hide()
        try:
            QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            if not conv.run():
                # advise conversion has failed
                msg = self.tr("Dataset conversion has finished with some errors. Check conversion log for details.")
                iface.messageBar().pushMessage(self.tr('Warning!'), msg, level=Qgis.Warning, duration=5)
            else:
                self.resetInterface()
            QtWidgets.QApplication.restoreOverrideCursor()
            summaryDlg.setHtml(conv.output['log'])
        except Exception as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            msg = self.tr("Dataset conversion has failed: '{0}'").format(', '.join(map(str, e.args)))
            iface.messageBar().pushMessage(self.tr('Warning!'), msg, level=Qgis.Warning, duration=5)
            QgsMessageLog.logMessage(':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
        summaryDlg.exec_()

    def startConversion(self, exportMap=False):
        """
        Starts the conversion process.
        """
        if self.validate():
            # from this point, interface is already validated and map produced from it also validated
            conversionMap = self.getConversionMap()
            if exportMap:
                self.exportConversionJson()
            # call conversion method taking the mapping json
            self.run(conversionMap=conversionMap)

    def populateInterface(self, parameterDict):
        """
        Populates interface with parameters from a mapping parameter dict.
        """
        pass

    def execute(self):
        """
        Changes the default icon for stack button and opens dialog.
        """
        self.parentButton.setDefaultAction(self.sender())
        self.exec_()

    def initGui(self):
        """
        Instantiate GUI for user, including button shortcut (if necessary) and tool insertion on DSGTools tab on QGIS. 
        """
        self.manager.addTool(
            text=self.tr('Convert Databases'),
            callback=self.execute,
            parentMenu=self.parentMenu,
            icon='install.png',
            parentButton=self.parentButton,
            defaultButton=False
        )

    def resetInterface(self):
        """
        Resets interface to its initial state.
        """
        # clear input/output widgets
        self.unload()
        self.connectToolSignals()
        self.setTableInitialState()
        self.restart()
        self.datasourceManagementWidgetIn.datasourceComboBox.setCurrentIndex(0)
        self.datasourceManagementWidgetOut.datasourceComboBox.setCurrentIndex(0)

    def unload(self):
        """
        Unloads GUI.
        """
        try:
            # disconnect all tool signals
            self.disconnectToolSignals()
        except:
            pass
        # remove every widget added to interface (in and output) and, consequently, disconnect all signals
        for obj in [self.datasourceManagementWidgetIn, self.datasourceManagementWidgetOut]:
            for driverName, wList in obj.activeDrivers.items():
                for w in wList:
                    # removeWidget method disconnects all widget signals
                    obj.removeWidget(w)
                    del w
