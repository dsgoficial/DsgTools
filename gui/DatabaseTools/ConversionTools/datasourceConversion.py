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
from qgis.PyQt.QtCore import Qt

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceConversion.ui'))

class DatasourceConversion(QtWidgets.QWizard, FORM_CLASS):
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
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        # set policy to make cell size adjust to content
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setHorizontalHeaderLabels([self.tr("Input"), self.tr("Output"), self.tr("Conversion Mode")])

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
        outDsList = list(map(getNameAlias, self.outDs.values()))
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
            # create combobox containing conversion mode options
            outModeComboboxDict[idx] = QtWidgets.QComboBox()
            outModeComboboxDict[idx].addItems(['Mode 1', 'Mode 2'])
            # set value to its own row, always in the first column
            self.tableWidget.setItem(idx, 0, item)
            # set classes combobox to its own row, always in the second column 
            self.tableWidget.setCellWidget(idx, 1, outDsComboboxDict[idx])
            # set conversion mode combobox to its own row, always in the third column 
            self.tableWidget.setCellWidget(idx, 2, outModeComboboxDict[idx])
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
        pass
