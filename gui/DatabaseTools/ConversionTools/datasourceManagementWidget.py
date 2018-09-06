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

from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.connectionComboBox import ConnectionComboBox
from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget

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

    def getWidget(self, source):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        widgetDict = {
            'PostGIS' : ConnectionComboBox(),
            'SpatiaLite' : SelectFileWidget()
        }
        return widgetDict[source] if source in widgetDict else None

    def addDatasourceSelectionFirstPage(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        if currentDbSource:
            # in case a valid driver is selected, add its widget to the interface
            w = self.getWidget(source=currentDbSource)
            try:
                self.datasourceLayout.addWidget(w)
            except:
                pass
        else:
            # if no tech is selected, inform user and nothing else
            pass