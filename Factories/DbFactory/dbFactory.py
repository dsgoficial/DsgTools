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

from PyQt4.QtSql import QSqlDatabase

#DSG Tools imports
from DsgTools.Factories.DbFactory.spatialiteDb import SpatialiteDb
from DsgTools.Factories.DbFactory.postgisDb import PostgisDb

class DbFactory:
    def createDbFactory(self,driverName):
        #TODO Treat none return
        if not ('QPSQL' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT PSQL driver not installed!', 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return None
        if not ('QSQLITE' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT QSQLITE driver not installed!', 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return None        
        
        if driverName == "QSQLITE":
            return SpatialiteDb()
        if driverName == "QPSQL":
            return PostgisDb()
        else:
            return None