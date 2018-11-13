# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-10
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
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.abstractSelectionWidget import AbstractSelectionWidget
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.newDatabaseLineEdit import NewDatabaseLineEdit
from DsgTools.core.dsgEnums import DsgEnums

import os

class NewSpatialiteWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated new spatialite widget.
        """
        super(NewSpatialiteWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a SpatiaLite
        self.source = DsgEnums.NewSpatiaLite
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent)
        self.selectionWidget.caption = self.tr('Create a SpatiaLite Database')
        self.selectionWidget.filter = self.tr('SpatiaLite Database (*.sqlite)')

    def getNewSelectionWidget(self, parent=None):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        :return: (QWidget) driver widget supported by conversion tool.
        """
        return NewDatabaseLineEdit(parent=parent)

    def getDatasourceConnectionName(self):
        """
        Gets the SpatiaLite connection name.
        :return: (str) datasource connection name.
        """
        n = self.selectionWidget.dsLineEdit.text()
        # n is a path and so it'll be something like /PATH/TO/datasource.sqlite or C:\PATH\TO\datasource.sqlite
        splitChar = '/' if '/' in n else '\\'
        ret = n.split(splitChar)[-1].split('.')[0] if n else ''
        return ret

    def getDatasourcePath(self):
        """
        Gets the SpatiaLite database path.
        :return: (str) datasource path name.
        """
        return "sqlite:{0}".format(self.selectionWidget.currentDb())

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
