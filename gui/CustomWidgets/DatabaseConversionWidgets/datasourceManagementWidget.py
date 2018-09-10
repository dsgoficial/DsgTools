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

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.datasourceContainerWidget import DatasourceContainerWidget

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceManagementWidget.ui'))

class DatasourceManagementWidget(QtWidgets.QWizardPage, FORM_CLASS):
    """
    Class scope:
    1- manage input/output datasources selection;
    2- prepare the conversion mapping sctructure using the table as a means to translate user's intentions; and
    3- make the call to core code to do the actual conversion.
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        """
        super(DatasourceManagementWidget, self).__init__()
        self.setupUi(self)
        # adds all available drivers to conversion to GUI
        self.fillSupportedDatasouces()
        # centralize all tool signals in order to keep track of all non-standard signals used
        self.connectToolSignals()
        # keep track of all (in)active widgets on input/output GUI
        self.activeDrivers = dict()
        self.inactiveDrivers = dict()

    def connectToolSignals(self):
        """
        Connects all tool generic behavior signals.
        """
        self.addSourcePushButton.clicked.connect(self.addDatasourceSelectionFirstPage)
        pass

    def fillSupportedDatasouces(self):
        """
        Fills the datasource selection combobox with all supported drivers.
        """
        driversList = ['', 'PostGIS', 'SpatiaLite']
        self.datasourceComboBox.addItems(driversList)

    def addElementToDict(self, k, e, d):
        """
        Adds widget to a dict composed by list as values and driver names as key.
        :param k: (str) new widget's driver name.
        :param e: (QWidget) widget to be added to the dict.
        :param d: (dict) dictionary to be updated.
        :return: (bool) operation success status.
        """
        try:
            if k not in d:
                d[k] = [e]
            else:
                if e not in d[k]:
                    d[k].append(e)
            return e in d[k]
        except:
            return False

    def addDatasourceSelectionFirstPage(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        # identify if it's an input or output page call
        inputPage = (self.objectName() == 'datasourceManagementWidgetIn')
        if currentDbSource:
            # in case a valid driver is selected, add its widget to the interface
            # first checks if there are any widgets already created
            inactiveWidgets = self.inactiveDrivers[currentDbSource] if currentDbSource in self.inactiveDrivers else []
            if inactiveWidgets:
                # if there are inactive widgets, reuse them instead of instantianting new ones
                w = self.inactiveDrivers[currentDbSource][0]
                # remove widget from inactive dict
                self.inactiveDrivers[currentDbSource].remove(w)
                # re-display widget on GUI
                w.show()
            else:
                # if no unused widget is found, a new one will be instantiated
                w = DatasourceContainerWidget(source=currentDbSource, inputContainer=inputPage)
                # connect removal widget signal to new widget
                w.removeWidget.connect(self.removeWidget)
                # add new driver container to GUI 
                self.datasourceLayout.addWidget(w)
            # update dict of active widgets
            self.addElementToDict(k=currentDbSource, e=w, d=self.activeDrivers)
            # # reset all driver's groupboxes names
            # self.resetWidgetsTitle()
        else:
            # if no tech is selected, inform user and nothing else
            pass

    def resetWidgetsTitle(self):
        """
        Resets all widgets containers titles.
        """
        for driverName, widgetList in self.activeDrivers.items():
            if not widgetList:
                # if there are no active widgets for current driver, there's nothing to be updated
                continue
            for idx, w in enumerate(widgetList):
                # if there are widgets from chosen driver, reset it's group box name
                w.setGroupWidgetName(name='{0} #{1}'.format(driverName, idx + 1))

    def removeWidget(self, w):
        """
        Removes driver widget from GUI.
        :param w: (QWidget) driver widget to be removed. 
        """
        # hide widget from GUI
        w.hide()
        # remove from active dict
        self.activeDrivers[w.source].remove(w)
        # update dict of inactive widgets
        self.addElementToDict(k=w.source, e=w, d=self.inactiveDrivers)
        # reset all driver's groupboxes names
        self.resetWidgetsTitle()

    # # TABLE MAPPING MANAGEMENT STARTS HERE

    def setTableInitialState(self):
        """
        Sets the mapping table to its initial state. Each row is composed by input datasource name, widget with
        all output datasource and conversion mode (whether -9999 would be set to all non-null restriction not respected)
        """
        outDs = [self.tr('Select Output Datasource')] + [w.getDatasourceConnectionName() \
                                                        for w in self.datasourceManagementWidgetOut.activeDrivers]