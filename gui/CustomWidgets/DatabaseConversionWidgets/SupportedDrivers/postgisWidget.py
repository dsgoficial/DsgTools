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
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QObject

from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.connectionComboBox import ConnectionComboBox
from DsgTools.gui.CustomWidgets.databaseConversionWidget import DatasourceContainerWidgetFactory

import os

class PostgisContainerWidget(DatasourceContainerWidgetFactory):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """
    # signal to be emitted when deletion button is clicked - emits itself (QWidget)
    removeWidget = pyqtSignal(QtWidgets.QWidget)

    # available drivers 'enum'
    tr = QObject() # just to access translation method
    NoDriver, PostGIS, NewPostGIS, SpatiaLite, NewSpatiaLite = tr.tr('Select a datasource driver'),\
                                                                'PostGIS', tr.tr('PostGIS (create new database)'),\
                                                                'SpatiaLite', tr.tr('SpatiaLite (create new database)')
    del tr

    def __init__(self, source, inputContainer, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        :param inputContainer: (bool) indicates whether the chosen database is supposed to be a reading/input widget or writting/output one.
        """
        super(DatasourceContainerWidget, self).__init__()
        self.setupUi(self)
        self.source = source
        self.addDatasourceSelectionWidget()
        # self.setGroupWidgetName(name=source)
        if not inputContainer:
            # output widget should not have filtering options
            self.layerFilterPushButton.hide()

    def getNewContainerWidget(self):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :return: (QWidget) driver widget, if it's supported by conversion tool.
        """
        return ConnectionComboBox()

    def addDatasourceSelectionWidget(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        """
        # get current text on datasource techonology selection combobox
        if source:
            # in case a valid driver is selected, add its widget to the interface
            self.connWidget = self.getNewContainerWidget()
            self.driverLayout.addWidget(self.connWidget)
        else:
            # if no tech is selected, inform user and nothing else
            self.connWidget = None

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        return self.connWidget.connectionSelectorComboBox.currentText()

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (object) the object representing the target datasource according to its driver. 
        """
        return self.abstractDb
