# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-13
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

from DsgTools.gui.CustomWidgets.DatasourceConversionWidgets.abstractSelectionWidget import AbstractSelectionWidget

class DatasourceSelectionWidgetFactory(QtWidgets.QWidget):
    """
    Class parento to each selection widget available to be added to a widget container.
    """

    def __init__(self, source, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        """
        super(DatasourceSelectionWidgetFactory, self).__init__()
        self.abstractSelectionWidget = self.getSelectionWidget(source=source)
        
        # self.sourceNameDict = {
        #     DsgEnums.NoDriver : self.tr('Select a datasource driver'),
        #     DsgEnums.PostGIS : 'PostGIS',
        #     DsgEnums.NewPostGIS : self.tr('PostGIS (create new database)'),
        #     DsgEnums.SpatiaLite : 'SpatiaLite',
        #     DsgEnums.NewSpatiaLite : self.tr('SpatiaLite (create new database)')
        # }

    def getSelectionWidget(self, source):
        """
        Gets selection widget to be returned to user as selectionWidget attribute.
        :param source: (str) driver codename to have its widget produced.
        :return: (QWidget) selection widget for selected driver.
        """
        return selectionWidgetsDict[source]

    def setGroupWidgetName(self, name=None):
        """
        Sets the name to the group added.
        :param name: (str) name for the group.
        """
        self.groupBox.setTitle('{0}'.format(name))

    def addDatasourceSelectionWidget(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # in case a valid driver is selected, add its widget to the interface
        self.connWidget = DatabaseConversionWidgetFactory(parent=self.driverLayout, source=self.source)
        # self.driverLayout.addWidget(self.connWidget)

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        # temporarily, it'll be set to current db name
        return self.connWidget.getDatasourceConnectionName() if self.connWidget else ''

    def getPostgisConnectionName(self):
        """
        Gets the PostGIS connection name.
        """
        return self.connWidget.connectionSelectorComboBox.currentText()

    def getSpatialiteConnectionName(self):
        """
        Gets the SpatiaLite connection name.
        """
        n = self.connWidget.connectionSelectorLineEdit.lineEdit.text()
        # n is a path and so it'll be something like /PATH/TO/datasource.sqlite or C:\PATH\TO\datasource.sqlite
        splitChar = '/' if '/' in n else '\\'
        ret = n.split(splitChar)[-1].split('.')[0] if n else ''
        return ret

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (object) the object representing the target datasource according to its driver. 
        """
        return self.connWidget.abstractDb if self.connWidget else None

    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        """
        Emits widget removal signal when remove button is clicked.
        """
        self.removeWidget.emit(self)

