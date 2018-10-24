# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from builtins import object
import os

from .postgisLayerLoader import PostGISLayerLoader
from .spatialiteLayerLoader import SpatialiteLayerLoader
from .geopackageLayerLoader import GeopackageLayerLoader

class LayerLoaderFactory(object):
    def makeLoader(self, iface, abstractDb, loadCentroids=False):
        """
        Returns the specific layer loader
        :param iface:
        :param abstractDb:
        :return:
        """
        driverName = abstractDb.getType()
        loaders = {
            'GPKG' : lambda : GeopackageLayerLoader(iface, abstractDb, loadCentroids),
            'QSQLITE' : lambda : SpatialiteLayerLoader(iface, abstractDb, loadCentroids),
            'QPSQL' : lambda : PostGISLayerLoader(iface, abstractDb, loadCentroids)
        }
        return loaders[driverName]() if driverName in loaders else None
