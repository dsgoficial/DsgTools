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
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        """
        super(DatasourceManagementWidget, self).__init__()
        self.setupUi(self)
        self.fillSupportedDatasouces()
        self.connectToolSignals()
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

    def elementToDict(self, k, e, d):
        """
        Sets and element to a dict composed by list as values.
        :param k: (str) key entry for the new value.
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
                w.show()
            else:
                w = DatasourceContainerWidget(source=currentDbSource, inputContainer=inputPage)
                # connect removal widget signal to new widget
                w.removeWidget.connect(self.removeWidget)
            # update dict of active widgets
            self.elementToDict(k=currentDbSource, e=w, d=self.activeDrivers)
            # add new driver container to GUI 
            self.datasourceLayout.addWidget(w)
        else:
            # if no tech is selected, inform user and nothing else
            pass

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
        self.elementToDict(k=w.source, e=w, d=self.inactiveDrivers)
