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
        email                : borba@dsg.eb.mil.br
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

from DsgTools.Factories.LayerLoaderFactory.postgisLayerLoader import PostGISLayerLoader
from DsgTools.Factories.LayerLoaderFactory.spatialiteLayerLoader import SpatialiteLayerLoader
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class LayerLoaderFactory:
    def makeLoader(self, iface, abstractDb):
        """
        Returns the specific layer loader
        :param iface:
        :param abstractDb:
        :return:
        """
        driverName = abstractDb.getType()
        if driverName == "QSQLITE":
            return SpatialiteLayerLoader(iface, abstractDb)
        if driverName == "QPSQL":
            return PostGISLayerLoader(iface, abstractDb)
        else:
            return None
