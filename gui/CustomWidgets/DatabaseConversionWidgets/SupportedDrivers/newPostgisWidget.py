# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-10-09
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
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.newConnectionLineEdit import NewConnectionLineEdit
from DsgTools.core.dsgEnums import DsgEnums

import os

class NewPostgisWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated new PostGIS widget.
        """
        super(NewPostgisWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a PostGIS
        self.source = DsgEnums.NewPostGIS
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent)

    def getNewSelectionWidget(self, parent=None):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated new PostGIS widget.
        :return: (QWidget) driver widget, if it's supported by conversion tool.
        """
        return NewConnectionLineEdit(parent=parent)

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        return self.selectionWidget.currentDb() if self.selectionWidget else ''

    def getDatasourcePath(self):
        """
        Gets the PostGIS connection path (server:port).
        :return: (str) datasource connection name.
        """
        if self.selectionWidget:
            host, port, user, _ = self.selectionWidget.viewServers.getDefaultConnectionParameters()
            return '{2}@{0}:{1}.{3}'.format(host, port, user, self.getDatasourceConnectionName())
        return ''

    def getDatasourceEdgvVersion(self):
        """
        Gets EDGV version selected.
        """
        return self.selectionWidget.edgvVersion()

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according to its driver. 
        """
        return self.selectionWidget.abstractDb
