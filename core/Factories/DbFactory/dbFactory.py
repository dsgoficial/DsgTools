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
from builtins import object
import os

from qgis.PyQt.QtSql import QSqlDatabase

#DSG Tools imports
from .spatialiteDb import SpatialiteDb
from .postgisDb import PostgisDb

from qgis.core import QgsMessageLog, Qgis

class DbFactory(object):
    def createDbFactory(self,driverName):
        #TODO Treat none return
        if not ('QPSQL' in QSqlDatabase.drivers()): #Driver wasn't loaded
            raise Exception('QT PSQL driver not installed!')
        if not ('QSQLITE' in QSqlDatabase.drivers()): #Driver wasn't loaded
            raise Exception('QT QSQLITE driver not installed!')
        
        if driverName == "QSQLITE":
            return SpatialiteDb()
        if driverName == "QPSQL":
            return PostgisDb()
        else:
            return None