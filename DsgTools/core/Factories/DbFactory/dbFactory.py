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

from qgis.PyQt.QtSql import QSqlDatabase
from qgis.core import QgsMessageLog, Qgis

# DSG Tools imports
from .spatialiteDb import SpatialiteDb
from .postgisDb import PostgisDb
from .geopackageDb import GeopackageDb
from .shapefileDb import ShapefileDb
from DsgTools.core.dsgEnums import DsgEnums

from builtins import object
import os


class DbFactory(object):
    def createDbFactory(self, driver):
        # TODO Treat none return
        if not ("QPSQL" in QSqlDatabase.drivers()):  # Driver wasn't loaded
            raise Exception("QT PSQL driver not installed!")
        if not ("QSQLITE" in QSqlDatabase.drivers()):  # Driver wasn't loaded
            raise Exception("QT QSQLITE driver not installed!")
        dbs = {
            DsgEnums.DriverSpatiaLite: lambda: SpatialiteDb(),
            DsgEnums.DriverPostGIS: lambda: PostgisDb(),
            DsgEnums.DriverGeopackage: lambda: GeopackageDb(),
            DsgEnums.DriverShapefile: lambda: ShapefileDb(),
        }
        return dbs[driver]() if driver in dbs else None
