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

from qgis.PyQt.QtCore import QObject
from qgis.utils import iface

from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

class AbstractSelectionWidget(QObject):
    """
    Class parent to to each selection widget available to be added to a widget container.
    Class scope:
    1- Define common methods to all manageable drivers
    2- Set and define generic behavior method for reimplementation in all children.
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        """
        super(AbstractSelectionWidget, self).__init__()
        self.source = ''
        self.selectionWidget = None

    def getSelectionWidgetName(self, source=None):
        """
        Gets selection widget to be returned to user as selectionWidget attribute.
        :param source: (DsgEnums.int) driver enum to have its name exposed.
        :return: (str) selection widget user-friendly name for selected driver.
        """
        if not source:
            return self.tr('No database selected.')
        sourceNameDict = {
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

    def getDatasourcePath(self):
        """
        Gets the datasource path.
        :return: (str) datasource path.
        """
        # to be reimplemented
        return ''

    def getNewSelectionWidget(self):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :return: (QWidget) driver widget, if it's supported by conversion tool.
        """
        # to be reimplemented
        return None

    def setDatasource(self, newDatasource):
        """
        Sets the datasource selected on current widget.
        :param newDatasource: (dict) new datasource info to be set.
        """
        # implementation for new datasources, but may be reimplemented into ALL children classes
        # for new datasources, entry is always { int : { 'edgv' : (str)edgv, 'crs' : (QgsCoordinateReferenceSystem)crs } }
        edgv = list(newDatasource.values())[0]['edgv']
        crs = list(newDatasource.values())[0]['crs']
        self.selectionWidget.edgvComboBox.setCurrentText(edgv)
        self.selectionWidget.mQgsProjectionSelectionWidget.setCrs(crs)

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (AbstractDb) the object representing the target datasource according. 
        """
        # to be reimplemented
        pass

    def getDatasourceEdgvVersion(self):
        """
        Gets current datasource selection EDGV Version.
        :return: (str) current EDGV version.
        """
        abstracDb = self.getDatasource()
        return abstracDb.getDatabaseVersion() if abstracDb else ''

    def getLayerLoader(self):
        """
        Returns the layer loader for given datasource.
        :return: (EDGVLayerLoader) layer loader.
        """
        abstracDb = self.getDatasource()
        return LayerLoaderFactory().makeLoader(iface=iface, abstractDb=abstracDb) if abstracDb else None

    def getLayersCrs(self):
        """
        Gets the CRS from all registered layers.
        """
        # may be reimplemented into children class, if needed
        abstracDb = self.getDatasource()
        crs = dict()
        if abstracDb:
            layerLoader = self.getLayerLoader()
            # alias for retrieving layer CRS and inserting it to out dict
            getCrsAlias = lambda x : crs.update({ x : layerLoader.getLayerByName(layer=x).crs().description() })
            # update crs dict
            list(map(getCrsAlias, self.getLayersDict()))
        return crs

    def getLayersDict(self):
        """
        Gets the list of all layers registered into datasource.
        :return: (dict) dictionaty for every (filled) layer contained by the selected datasource and its feature count.
        """
        abstracDb = self.getDatasource()
        if abstracDb:
            return abstracDb.listClassesWithElementsFromDatabase(useComplex=False, primitiveFilter=[])
        return {}

    def getComplexDict(self):
        """
        Gets the dict of all complex layers present in the database.
        :return: (dict) dictionaty for every (filled) complex layer contained by the selected datasource and its feature count.
        """
        abstracDb = self.getDatasource()
        if abstracDb:
            complexes = abstracDb.listComplexClassesFromDatabase()
            return abstracDb.listWithElementsFromDatabase(complexes)
        return {}

    def validate(self):
        """
        Validates selection widgets contents.
        :return: (str) invalidation reason.
        """
        return self.selectionWidget.validate() if self.selectionWidget else self.tr('Selection widget not available.')

    def isValid(self):
        """
        Validates selection widgets contents.
        :return: (bool) invalidation status.
        """
        msg = self.validate()
        return msg == ''