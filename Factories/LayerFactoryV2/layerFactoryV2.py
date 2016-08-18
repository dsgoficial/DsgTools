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

from DsgTools.Factories.LayerFactory.postgis_layer import PostGISLayer
from DsgTools.Factories.LayerFactory.spatialite_layer import SpatialiteLayer
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class LayerFactory:
    def makeFactory(self, abstractDb):
        driverName = abstractDb.getType()
        if driverName == "QSQLITE":
            return SpatialiteLayer(abstractDb)
        if driverName == "QPSQL":
            return PostGISLayer(abstractDb)
        else:
            return None
