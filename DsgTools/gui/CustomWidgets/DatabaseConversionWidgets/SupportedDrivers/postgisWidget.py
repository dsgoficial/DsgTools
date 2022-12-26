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

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.abstractSelectionWidget import (
    AbstractSelectionWidget,
)
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.connectionComboBox import (
    ConnectionComboBox,
)
from DsgTools.core.dsgEnums import DsgEnums

import os


class PostgisWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        """
        super(PostgisWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a PostGIS
        self.source = DsgEnums.PostGIS
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent, isStatic=True)

    def getNewSelectionWidget(self, parent=None, isStatic=True):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        :param isStatic: (bool) indicates whether server selection will be static (no default).
        :return: (QWidget) driver widget, if it's supported by conversion tool.
        """
        return ConnectionComboBox(parent=parent, isStatic=True)

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        return (
            self.selectionWidget.connectionSelectorComboBox.currentText()
            if self.selectionWidget
            else ""
        )

    def getDatasourcePath(self):
        """
        Gets the PostGIS connection path (server:port).
        :return: (str) datasource connection name.
        """
        abstractDb = self.getDatasource()
        if abstractDb:
            host, port, username, _ = abstractDb.getDatabaseParameters()
            return "pg:{2}@{0}:{1}.{3}".format(
                host, port, username, self.getDatasourceConnectionName()
            )
        return ""

    def setDatasource(self, newDatasource):
        """
        Sets the datasource selected on current widget.
        :param newDatasource: (dict) { db : (host, port, username, password) }.
        """
        # the input parameter is a dict due to a standard behavior on the other widgets (keep parallel)
        if self.selectionWidget:
            for db, (
                serverName,
                host,
                port,
                username,
                password,
            ) in newDatasource.items():
                self.selectionWidget.setHost(serverName)
                self.selectionWidget.connectionSelectorComboBox.setCurrentIndex(
                    self.selectionWidget.connectionSelectorComboBox.findText(db)
                )
                return  # first item will be set (if more than one is given)

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according to its driver.
        """
        return self.selectionWidget.abstractDb
