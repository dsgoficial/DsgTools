# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-28
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

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QFileDialog

from .abstractMultiDsSelectorWidget import AbstractMultiDsSelectorWidget
from DsgTools.core.dsgEnums import DsgEnums

import os


class MultiSpatialiteSelectorWidget(AbstractMultiDsSelectorWidget):
    """
    Class designed to retrieve a SpatiaLite database list.
    """

    def __init__(self, parent=None):
        """
        Class constructor.
        """
        super(MultiSpatialiteSelectorWidget, self).__init__()
        self.source = DsgEnums.SpatiaLite

    def getWidget(self, parent=None):
        """
        Retrieves current datasource selector dialog.
        """
        return QFileDialog()

    def getDatabaseName(self, datasourcePath):
        """
        Gets the database name from a given datasource.
        :param datasourcePath: (str) datasource path.
        :return: (str) datasource name.
        """
        return os.path.basename(datasourcePath).split(".")[0]

    def exec_(self):
        """
        Starts dialog.
        """
        # clear datasources
        self.datasources = {}
        dbList = self.selector.getOpenFileNames(
            caption=self.tr("Select SpatiaLite Datasources"),
            filter=self.tr("SpatiaLite Databases (*.sqlite)"),
        )[0]
        for db in dbList:
            self.datasources[self.getDatabaseName(datasourcePath=db)] = db
        return int(not self.datasources)  # execution code
