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

from qgis.core import (
    QgsVectorLayer,
    QgsMessageLog,
    QgsCoordinateReferenceSystem,
    Qgis,
    QgsProject,
)

from .spatialiteLayerLoader import SpatialiteLayerLoader


class GeopackageLayerLoader(SpatialiteLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(GeopackageLayerLoader, self).__init__(iface, abstractDb, loadCentroids)

        self.provider = "geopackage"

        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(":".join(e.args), "DSGTools Plugin", Qgis.Critical)
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
        vlayer = self.getLayerByName("{0}_{1}".format(schema, tableName))
        if not vlayer.isValid():
            QgsMessageLog.logMessage(
                vlayer.error().summary(), "DSGTools Plugin", Qgis.Critical
            )
        QgsProject.instance().addMapLayer(vlayer, addToLegend=False)
        crs = QgsCoordinateReferenceSystem(
            int(srid), QgsCoordinateReferenceSystem.EpsgCrsId
        )
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        vlayer = self.setMulti(vlayer, domLayerDict)
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
        :param layer: (str) table name - for GPKG it is [SCHEMA]_[CATEGORY]_[CLASS].
        :return: (QgsVectorLayer) vector layer.
        """
        # parent class reimplementation
        schema = layer.split("_")[0]
        table = layer[len(schema) + 1 :]
        lyrName, schema, geomColumn, tableName, srid = self.getParams(table)
        self.setDataSource("", layer, geomColumn, "")
        return QgsVectorLayer(
            "{0}|layername={1}".format(self.abstractDb.db.databaseName(), layer),
            table,
            "ogr",
        )
