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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot

from functools import partial
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceConversion.ui'))

class DatasourceConversion(QtWidgets.QWizard, FORM_CLASS):
    # enum for column ordering
    COLUMN_COUNT = 8
    InDs, Filter, InEdgv, InSrc, OutDs, OutEdgv, OutSrc, ConversionMode = list(range(COLUMN_COUNT))

    def __init__(self, manager, parentMenu, parent=None):
        """
        """
        super(DatasourceConversion, self).__init__()
        self.setupUi(self)
        # self.setTitle(self.tr('Datasource Conversion Wizard'))
        self.manager = manager
        self.parentMenu = parentMenu
        self.parentButton = None
        self.connectToolSignals()
        # initiate widget dicts
        self.outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)

    def connectToolSignals(self):
        """
        Connects all tool generic signals.
        """
        # if any widget was turned active/inactive
        self.datasourceManagementWidgetIn.activeWidgetsChanged.connect(self.setTableInitialState)
        self.datasourceManagementWidgetOut.activeWidgetsChanged.connect(self.setTableInitialState)
        # if datasource is changed (e.g. user changed his postgis database selection, for instance)
        self.datasourceManagementWidgetIn.datasourceChangedSignal.connect(self.setTableInitialState)
        self.datasourceManagementWidgetOut.datasourceChangedSignal.connect(self.setTableInitialState)

    def disconnectToolSignals(self):
        """
        Connects all tool generic signals.
        """
        # if any widget was turned active/inactive
        self.datasourceManagementWidgetIn.activeWidgetsChanged.disconnect(self.setTableInitialState)
        self.datasourceManagementWidgetOut.activeWidgetsChanged.disconnect(self.setTableInitialState)
        # if datasource is changed (e.g. user changed his postgis database selection, for instance)
        self.datasourceManagementWidgetIn.datasourceChangedSignal.disconnect(self.setTableInitialState)
        self.datasourceManagementWidgetOut.datasourceChangedSignal.disconnect(self.setTableInitialState)

    def getWidgetNameDict(self, d):
        """
        Gets the name translated into widget dict from a given dict.
        :param d: (dict) dictionary  - { (str)driver : (QWidget)widget } - to have its widgets translated.
        :return: (dict) translated dict - { (str)datasource_name : (QWidget)widget }.
        """
        returnDict = dict()
        for k in d:
            for w in d[k]:
                returnDict[w.groupBox.title()] = w
        return returnDict

    def resetTable(self, enabled=False):
        """
        Resets table to initial state.
        :param enabled: (bool) indicates whether table will be enabled.
        """
        # clear possible content in it
        self.tableWidget.setEnabled(enabled)
        self.tableWidget.setColumnCount(DatasourceConversion.COLUMN_COUNT)
        # if a signal issue comes along, maybe cell shoul've been systematically removed
        # and signals disconnect for each row along. So that's where shit might be re-coded (=
        self.tableWidget.setRowCount(0)
        # set policy to make cell size adjust to content
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setHorizontalHeaderLabels([
                self.tr("Input"), self.tr("In: EDGV Version"), self.tr("Output"), self.tr("Out: EDGV Version"), 
                self.tr("Conversion Mode"), 
                ])

    def getRowInfo(self, row):
        """
        Retrieves all filled row info.
        :param row: (int) row index to have its output columns populated.
        :return: (list-of-object) a list of all information found on a given row (may be a widget or string).
        """
        # input datasource, input and output EDGV versions are always a text
        inDs = self.tableWidget.item(row, DatasourceConversion.InDs).text()
        inEdgv = self.tableWidget.item(row, DatasourceConversion.InEdgv).text()
        outEdgv = self.tableWidget.item(row, DatasourceConversion.OutEdgv).text()
        # output datasource, input and output SRC and filter status are always a QWidget
        outDs = self.tableWidget.cellWidget(idx, DatasourceConversion.OutDs)
        # however, output info might not yet have been filled
        try:
            _filter = self.tableWidget.cellWidget(idx, DatasourceConversion.Filter)
        except:
            _filter = None
        try:
            inSrc = self.tableWidget.cellWidget(idx, DatasourceConversion.InSrc)
        except:
            inSrc = None
        try:
            outSrc = self.tableWidget.cellWidget(idx, DatasourceConversion.OutSrc)
        except:
            outSrc = None
        return [inDs, _filter, inEdgv, inSrc, outDs, outEdgv, outSrc]

    def fillOutDsInfoRow(self, row):
        """
        Fills out row with output info for each output column. In here, ouput SRC and EDGV are filled. 
        :param row: (int) row index to have its output columns populated.
        :return: (list-of-object) return a list containing (str) output EDGV version and (QPushButton) output SRC.
        """
        # get only outDs widget
        outDs = self.getRowInfo(row=row)[5]
        # widget dict keys are defined as group title, which is part of outDs current text
        groupTitle = outDs.currentText().split(':')[0]
        if groupTitle in self.outDs:
            widget = self.outDs[groupTitle]
            # only fills line if dictionary is a controlled widget
            # new push button for SRC
            outSrc = QtWidgets.QPushButton()
            outSrc.setText(self.tr('SRC'))
            # get new text item to add output datasource
            edgvOut = widget.connWidget.getDatasourceEdgvVersion()
            itemEdgvOut = QtWidgets.QTableWidgetItem()
            itemEdgvOut.setText(edgvOut)
            itemEdgvOut.setFlags(Qt.ItemIsEditable) # not editable
            # add both to table
            self.tableWidget.setItem(idx, DatasourceConversion.OutSrc, outSrc)
            self.tableWidget.setCellWidget(idx, DatasourceConversion.OutEdgv, itemEdgvOut)
            return [edgvOut, outSrc]
        else:
            # if is not controlled, clear line
            pass


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
        outDsList = [self.tr('Select a datasource')] + list(map(getNameAlias, self.outDs.values()))
        # input ds dict/list
        self.inDs = self.getWidgetNameDict(self.datasourceManagementWidgetIn.activeDrivers)
        inDsList = list(self.inDs.values())
        # set the table rows # the same as the # of input ds
        self.tableWidget.setRowCount(len(inDsList))
        # initiate comboboxes control dictionaries
        outDsComboboxDict = dict()
        outModeComboboxDict = dict()
        for idx, w in enumerate(inDsList):
            # create the combobox containing all output ds
            outDsComboboxDict[idx] = QtWidgets.QComboBox()
            outDsComboboxDict[idx].addItems(outDsList)
            # create the item containing current loop's input ds
            item = QtWidgets.QTableWidgetItem()
            item.setText('{0}: {1}'.format(w.groupBox.title(), w.getDatasourceConnectionName()))
            item.setFlags(Qt.ItemIsEditable)
            # create combobox containing conversion mode options
            outModeComboboxDict[idx] = QtWidgets.QComboBox()
            outModeComboboxDict[idx].addItems(['Mode 1', 'Mode 2'])
            # populate edgv versions column
            # input is always text
            itemEdgvIn = QtWidgets.QTableWidgetItem()
            itemEdgvIn.setText(w.connWidget.getDatasourceEdgvVersion())
            itemEdgvIn.setFlags(Qt.ItemIsEditable)
            # set input datasource to first column
            self.tableWidget.setItem(idx, 0, item)
            # set edgv version for input version
            self.tableWidget.setItem(idx, 1, itemEdgvIn)
            # set classes combobox to its own row, always in the second column 
            self.tableWidget.setCellWidget(idx, 2, outDsComboboxDict[idx])
            # set conversion mode combobox to its own row, always in the third column 
            self.tableWidget.setCellWidget(idx, 4, outModeComboboxDict[idx])
            # set table output information population to its widget
            outModeComboboxDict[idx].currentIndexChanged.connect(partial(self.fillOutDsInfoRow, row=idx))
        # resize to contents
        self.tableWidget.resizeColumnsToContents()

    def initGui(self):
        """
        Instantiate GUI for user, including button shortcut (if necessary) and tool insertion on DSGTools tab on QGIS. 
        """
        callback = lambda : self.exec_() 
        self.manager.addTool(
            text=self.tr('Convert Databases'),
            callback=callback,
            parentMenu=self.parentMenu,
            icon='install.png',
            parentButton=self.parentButton,
            defaultButton=False
        )

    def unload(self):
        """
        Unloads GUI.
        """
        # disconnect all tool signals
        self.disconnectToolSignals()
        # remove every widget added to interface (in and output) and, consequently, disconnect all signals
        for d in [self.datasourceManagementWidgetIn.activeDrivers, self.datasourceManagementWidgetOut.activeDrivers]:
            for driverName, wList in d.items():
                for w in wList:
                    # removeWidget method disconnects all widget signals
                    self.datasourceManagementWidgetIn.removeWidget(w)
        # for last, removes itself
        self.setParent(None)
        del self