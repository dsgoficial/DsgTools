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

from DsgTools.core.dsgEnums import DsgEnums

class AbstractSelectionWidget(QtWidgets.QWidget):
    """
    Class parent to to each selection widget available to be added to a widget container.
    Class scope:
    1- Define common methods to all manageable drivers
    2- Set and define generic behavior method for reimplementation in all children.
    """
    def __init__(self, source, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        """
        super(DatasourceSelectionWidgetFactory, self).__init__()
        self.source = ''
        self.abstractDb = None

    def getSelectionWidgetName(self, source=None):
        """
        Gets selection widget to be returned to user as selectionWidget attribute.
        :param source: (DsgEnum.int) driver enum to have its name exposed.
        :return: (str) selection widget user-friendly name for selected driver.
        """
        if not source:
            source = self.source
        sourceNameDict = {
            '' : self.tr('No database selected.'),
            DsgEnums.NoDriver : self.tr('Select a datasource driver'),
            DsgEnums.PostGIS : 'PostGIS',
            DsgEnums.NewPostGIS : self.tr('PostGIS (create new database)'),
            DsgEnums.SpatiaLite : 'SpatiaLite',
            DsgEnums.NewSpatiaLite : self.tr('SpatiaLite (create new database)'),
            DsgEnums.Shapefile : 'Shapefile',
            DsgEnums.NewShapefile : self.tr('Shapefile (create new database)'),
            DsgEnums.Geopackage : 'Geopackage',
            DsgEnums.NewGeopackage : self.tr('Geopackage (create new database)')
        }
        return sourceNameDict[source]

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        # to be reimplemented
        return ''

    # def getPostgisConnectionName(self):
    #     """
    #     Gets the PostGIS connection name.
    #     """
    #     return self.connWidget.connectionSelectorComboBox.currentText()

    # def getSpatialiteConnectionName(self):
    #     """
    #     Gets the SpatiaLite connection name.
    #     """
    #     n = self.connWidget.connectionSelectorLineEdit.lineEdit.text()
    #     # n is a path and so it'll be something like /PATH/TO/datasource.sqlite or C:\PATH\TO\datasource.sqlite
    #     splitChar = '/' if '/' in n else '\\'
    #     ret = n.split(splitChar)[-1].split('.')[0] if n else ''
    #     return ret

    def setDatasource(self, newDatasource):
        """
        Gets the datasource selected on current widget.
        :param newDatasource: (object) new datasource to be set.
        """
        # to be reimplemented
        pass

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according. 
        """
        return self.abstractDb
