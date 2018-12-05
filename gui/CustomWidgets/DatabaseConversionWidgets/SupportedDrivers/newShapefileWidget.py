# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-15
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
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import pyqtSlot

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.abstractSelectionWidget import AbstractSelectionWidget
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.newDatabaseLineEdit import NewDatabaseLineEdit
from DsgTools.core.dsgEnums import DsgEnums

import os

class NewShapefileWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated new Shapefile widget.
        """
        super(NewShapefileWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a Shapefile
        self.source = DsgEnums.NewShapefile
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent)
        self.selectionWidget.caption = self.tr('Select a Directory for Shapes to be Saved At')
        self.selectionWidget.filter = self.tr('Shapefile Database')
        # connect datasource selection to this ones
        self.selectionWidget.selectFilePushButton.clicked.disconnect(self.selectionWidget.selectDatasource)
        self.selectionWidget.selectFilePushButton.clicked.connect(self.selectDatasource)

    def getNewSelectionWidget(self, parent=None):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        :return: (QWidget) driver widget supported by conversion tool.
        """
        return NewDatabaseLineEdit(parent=parent)

    def getDatasourceConnectionName(self):
        """
        Gets the Shapefile connection name.
        :return: (str) datasource connection name.
        """
        ret = self.selectionWidget.dsLineEdit.text()
        if ret:
            # path is something like /PATH/TO/datasource/***.shp or C:\PATH\TO\datasource\***.shp
            splitChar = '/' if '/' in ret else '\\'
            if len(ret) > 4:
                # datasource connection name for a shape 'database' is its parent folder
                ret = ret.split(splitChar)[-1] if ret[-4:].lower() != '.shp' else ret.split(splitChar)[:-4]
        ret = ret if ret != self.tr("New Database") else ''
        return ret

    def getDatasourcePath(self):
        """
        Gets the Shapefile database path.
        :return: (str) datasource path name.
        """
        return "shp:{0}".format(self.selectionWidget.currentDb())

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according to its driver. 
        """
        return self.selectionWidget.abstractDb

    def getDatasourceEdgvVersion(self):
        """
        Gets EDGV version selected.
        """
        return self.selectionWidget.edgvVersion()

    def selectDatasource(self):
        """
        Opens dialog for file/directory selection.
        """
        # model of implementation for reimplementation
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.Directory)
        fd.setOption(QFileDialog.ShowDirsOnly, True)
        directory = fd.getExistingDirectory(caption=self.selectionWidget.caption)
        if directory:
            if len(directory) > 4:
                # datasource connection name for a shape 'database' is its parent folder
                directory = directory if directory[-4:].lower() != '.shp' else directory[:-4]
            # set only directories as line text
            self.selectionWidget.dsLineEdit.setText(directory)
        self.selectionWidget.loadDatabase(currentText=directory)
