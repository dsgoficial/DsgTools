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

from DsgTools.Factories.LayerFactoryV2.postgis_layerV2 import PostGISLayerV2
from DsgTools.Factories.LayerFactoryV2.spatialite_layerV2 import SpatialiteLayerV2
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class LayerFactory:
    def makeFactory(self, iface, abstractDb):
        driverName = abstractDb.getType()
        if driverName == "QSQLITE":
            return SpatialiteLayerV2(iface, abstractDb)
        if driverName == "QPSQL":
            return PostGISLayerV2(iface, abstractDb)
        else:
            return None
