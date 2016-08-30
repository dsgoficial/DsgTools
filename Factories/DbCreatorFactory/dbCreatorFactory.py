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
import os

from PyQt4.QtSql import QSqlDatabase

#DSG Tools imports
from DsgTools.Factories.DbCreatorFactory.spatialiteDbCreator import SpatialiteDbCreator
from DsgTools.Factories.DbCreatorFactory.postgisDbCreator import PostgisDbCreator

class DbCreatorFactory:
    def createDbCreatorFactory(self, driverName, createParam, version):
        #TODO Treat none return
        if not ('QPSQL' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT PSQL driver not installed!', 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return None
        if not ('QSQLITE' in QSqlDatabase.drivers()): #Driver wasn't loaded
            QgsMessageLog.logMessage('QT QSQLITE driver not installed!', 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return None        
        
        if driverName == "QSQLITE":
            return SpatialiteDbCreator(createParam, version)
        if driverName == "QPSQL":
            return PostgisDbCreator(createParam, version)
        else:
            return None