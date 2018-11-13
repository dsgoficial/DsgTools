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

from qgis.PyQt.QtWidgets import QFileDialog

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.abstractSelectionWidget import AbstractSelectionWidget
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.databaseFileLineEdit import DatabaseFileLineEdit
from DsgTools.core.dsgEnums import DsgEnums

import os

class ShapefileWidget(AbstractSelectionWidget):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated shapefile widget.
        """
        super(ShapefileWidget, self).__init__(parent=parent)
        # reset source attribute value as now it is defined as a SpatiaLite
        self.source = DsgEnums.Shapefile
        # initiate new instance of actual class widget
        self.selectionWidget = self.getNewSelectionWidget(parent=parent)
        self.selectionWidget.connectionSelectorLineEdit.caption = self.tr('Select a Directory Containing Shapefiles')
        self.selectionWidget.connectionSelectorLineEdit.filter = self.tr('Shapefile Database')
        # initiate driver for abstract db setting
        self.selectionWidget.driver = DsgEnums.DriverShapefile
        # connect datasource selection to this ones - this part is not great, sucks actually;
        # a refactory should be be executed in here...
        self.selectionWidget.connectionSelectorLineEdit.selectFilePushButton.clicked.disconnect(\
            self.selectionWidget.connectionSelectorLineEdit.on_selectFilePushButton_clicked)
        self.selectionWidget.connectionSelectorLineEdit.selectFilePushButton.clicked.connect(self.selectDatasource)

    def getNewSelectionWidget(self, parent=None):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param parent: (QWidget) widget parent to newly instantiated shapefile widget.
        :return: (QWidget) driver widget supported by conversion tool.
        """
        return DatabaseFileLineEdit(parent=parent)

    def getDatasourceConnectionName(self):
        """
        Gets the Shapefile connection name (inner directory selected).
        :return: (str) datasource connection name.
        """
        abstractDb = self.getDatasource()
        return abstractDb.getDatabaseName() if abstractDb else ''

    def setDatasource(self, newDatasource):
        """
        Sets the datasource selected on current widget.
        :param newDatasource: (object) new datasource to be set.
        """
        # to be reimplemented
        pass

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according to its driver. 
        """
        return self.selectionWidget.abstractDb

    def getDatasourcePath(self):
        """
        Gets the Shapefile connection path (fullpath).
        :return: (str) datasource connection name.
        """
        abstractDb = self.getDatasource()
        return abstractDb.databaseName() if abstractDb else ''

    def selectDatasource(self):
        """
        Opens dialog for file/directory selection.
        """
        # model of implementation for reimplementation
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.Directory)
        fd.setOption(QFileDialog.ShowDirsOnly, True)
        directory = fd.getExistingDirectory(caption=self.selectionWidget.connectionSelectorLineEdit.caption)
        if directory:
            if len(directory) > 4:
                # datasource connection name for a shape 'database' is its parent folder
                directory = directory if directory[-4:].lower() != '.shp' else directory[:-4]
            # set only directories as line text
            self.selectionWidget.connectionSelectorLineEdit.lineEdit.setText(directory)
        self.selectionWidget.loadDatabase(currentText=directory)
