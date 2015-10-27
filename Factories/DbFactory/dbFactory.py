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
    def createDbFactory(self,driverName):
        if driverName == "QSQLITE":
            return SpatialiteDb()
        if driverName == "QPSQL":
            return PostgisDb()
        else:
            return None


if __name__ == '__main__':
    dbF = DbFactory()
    gen=dbF.createDbFactory("QPSQL")
    gen.connectDatabaseWithServerName('local_m_1915_4')
    domain = gen.getDomainDict()
    print domain
    