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

from DsgTools.Factories.DbFactory.spatialiteDb import SpatialiteDb
from DsgTools.Factories.DbFactory.postgisDb import PostgisDb

class DbFactory:
    def createDbFactory(self, qtsqlDb):
        if qtsqlDb.driverName() == "QSQLITE":
            return SpatialiteDb(qtsqlDb,True)
        if qtsqlDb.driverName() == "QPSQL":
            return PostGISDb(qtsqlDb,False)
        else:
            return None