# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-30
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt.QtSql import QSqlDatabase
#DSG Tools imports
from .spatialiteDbCreator import SpatialiteDbCreator
from .postgisDbCreator import PostgisDbCreator
from .geopackageDbCreator import GeopackageDbCreator

class DbCreatorFactory(object):
    def createDbCreatorFactory(self, driverName, createParam, parentWidget = None):
        #TODO Treat none return
        if not ('QPSQL' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT PSQL driver not installed!', 'DSG Tools Plugin', Qgis.Critical)
            return None
        if not ('QSQLITE' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT QSQLITE driver not installed!', 'DSG Tools Plugin', Qgis.Critical)
            return None        
        creators = {
            "QSQLITE" : SpatialiteDbCreator,
            "QPSQL" : PostgisDbCreator,
            "GPKG" : GeopackageDbCreator
        }
        return creators[driverName](createParam, parentWidget) if driverName in creators else None
