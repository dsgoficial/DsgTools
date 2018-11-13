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

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.abstractSelectionWidget import AbstractSelectionWidget
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.databaseFileLineEdit import DatabaseFileLineEdit
from DsgTools.core.dsgEnums import DsgEnums

import os

class GeopackageWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        """
        super(GeopackageWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a SpatiaLite
        self.source = DsgEnums.Geopackage
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent)
        self.selectionWidget.driver = DsgEnums.DriverGeopackage
        self.selectionWidget.connectionSelectorLineEdit.caption = self.tr('Select a Geopackage Database')
        self.selectionWidget.connectionSelectorLineEdit.filter = self.tr('Geopackage Database (*.gpkg)')

    def getNewSelectionWidget(self, parent=None):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        :return: (QWidget) driver widget supported by conversion tool.
        """
        return DatabaseFileLineEdit(parent=parent)

    def getDatasourceConnectionName(self):
        """
        Gets the Geopackage connection name.
        :return: (str) datasource connection name.
        """
        n = self.selectionWidget.connectionSelectorLineEdit.lineEdit.text()
        # n is a path and so it'll be something like /PATH/TO/datasource.sqlite or C:\PATH\TO\datasource.sqlite
        splitChar = '/' if '/' in n else '\\'
        ret = n.split(splitChar)[-1].split('.')[0] if n else ''
        return ret

    def getDatasourcePath(self):
        """
        Gets the SpatiaLite database path.
        :return: (str) datasource path name.
        """
        if self.getDatasource():
            # just return a datasource path if a valid one was loaded
            return "gpkg:{0}".format(self.selectionWidget.connectionSelectorLineEdit.lineEdit.text())
        return ''

    def setDatasource(self, newDatasource):
        """
        Sets the datasource selected on current widget.
        :param newDatasource: (dict) containing datasource name and its path.
        """
        if newDatasource:
            self.selectionWidget.connectionSelectorLineEdit.lineEdit.setText((list(newDatasource.values())[0]))

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according to its driver. 
        """
        return self.selectionWidget.abstractDb
