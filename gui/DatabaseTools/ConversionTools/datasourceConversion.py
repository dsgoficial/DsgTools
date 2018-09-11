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

from DsgTools.gui.CustomWidgets.ConnectionWidgets.ServerConnectionWidgets.exploreServerWidget import ExploreServerWidget

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

    def getWidgetNameDict(self, d):
        """
        Gets the name translated into widget dict from a given dict.
        :param d: (dict) dictionary  - { (str)driver : (QWidget)widget } - to have its widgets translated.
        :return: (dict) translated dict - { (str)datasource_name : (QWidget)widget }.
        """
        vl = []
        for k in d:
            vl += d[k]
        returnDict = dict()
        print(3, returnDict)
        newDictLambda = lambda w : returnDict.update({ w.getDatasourceConnectionName() : w })
        print(4, returnDict)
        map(newDictLambda, vl)
        return returnDict

    def resetTable(self, enabled=False):
        """
        Resets table to initial state.
        :param enabled: (bool) indicates whether table will be enabled.
        """
        # clear possible content in it
        self.tableWidget.setEnabled(enabled)
        self.tableWidget.setRowCount(0)

    def setTableInitialState(self):
        """
        Sets the mapping table to its initial state. Each row is composed by input datasource name, widget with
        all output datasource and conversion mode (whether -9999 would be set to all non-null restriction not respected)
        """
        self.resetTable(enabled=True)
        # output ds dict/list
        outDs = self.getWidgetNameDict(self.datasourceManagementWidgetOut.activeDrivers)
        outDsList = list(outDs.keys())
        print(1, self.datasourceManagementWidgetOut.activeDrivers)
        # set the table rows # the same as the # of input ds
        self.tableWidget.setRowCount(len(self.datasourceManagementWidgetIn.activeDrivers))
        print(2, self.datasourceManagementWidgetIn.activeDrivers)
        # initiate comboboxes control dictionaries
        outDsComboboxDict = dict()
        outModeComboboxDict = dict()
        for driverName, widgetList in self.datasourceManagementWidgetIn.activeDrivers.items():
            for idx, w in enumerate(widgetList):
                # create the combobox containing all output ds
                outDsComboboxDict[idx] = QtWidgets.QComboBox()
                outDsComboboxDict[idx].addItems(outDsList)
                # create the item containing current loop's input ds
                item = QtWidgets.QTableWidgetItem()
                item.setText('{0}: {1}'.format(driverName, w.getDatasourceConnectionName()))
                # create combobox containing conversion mode options
                outModeComboboxDict[idx] = QtWidgets.QComboBox()
                outDsComboboxDict[idx].addItems(['Mode 1', 'Mode 2'])
                # set value to its own row, always in the first column 
                self.tableWidget.setItem(idx, 0, item)
                # set classes combobox to its own row, always in the second column 
                self.tableWidget.setCellWidget(idx, 1, outDsComboboxDict[idx])
                # set conversion mode combobox to its own row, always in the third column 
                self.tableWidget.setCellWidget(idx, 2, outDsComboboxDict[idx])

    def keyPressEvent(self, e):
        """
        Binds table population to F5 (TEMPORARILY).
        :param e: keyboard event
        """
        if e.key() == Qt.Key_F5 and self.currentId() == 2:
            self.setTableInitialState()
        elif e.key() == Qt.Key_Escape:
            self.close()

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