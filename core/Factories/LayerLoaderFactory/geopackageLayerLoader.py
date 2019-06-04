# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-24
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
import os

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer,QgsDataSourceUri, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog, Qgis, QgsProject, QgsEditorWidgetSetup
from qgis.utils import iface

#DsgTools imports
from .spatialiteLayerLoader import SpatialiteLayerLoader
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class GeopackageLayerLoader(SpatialiteLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(GeopackageLayerLoader, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'geopackage'
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
            return

        self.buildUri()

    def loadLayer(self, inputParam, parentNode, uniqueLoad, stylePath, domLayerDict):
        """
        Loads a layer
        :param lyrName: Layer nmae
        :param idSubgrupo: sub group id
        :param uniqueLoad: boolean to mark if the layer should only be loaded once
        :param stylePath: path to the styles used
        :param domLayerDict: domain dictionary
        :return:
        """
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr:
            return lyr
        self.setDataSource('', '_'.join([schema,tableName]), geomColumn, '')
        vlayer = QgsVectorLayer("{0}|table={1}".format(self.abstractDb.db.databaseName(), tableName), tableName, "ogr")
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", Qgis.Critical)
        QgsProject.instance().addMapLayer(vlayer, addToLegend = False)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        vlayer = self.setMulti(vlayer,domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
        parentNode.addLayer(vlayer)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer. 
        """
        # parent class reimplementation
        schema = layer.split('_')[0]
        table = layer[len(schema) + 1:]
        lyrName, schema, geomColumn, tableName, srid = self.getParams(table)
        self.setDataSource('', layer, geomColumn, '')
        return QgsVectorLayer("{0}|table={1}".format(self.abstractDb.db.databaseName(), table), table, "ogr")
