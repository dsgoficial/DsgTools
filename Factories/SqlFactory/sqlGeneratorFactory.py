# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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

from DsgTools.Factories.SqlFactory.spatialiteSqlGenerator import SpatialiteSqlGenerator
from DsgTools.Factories.SqlFactory.postgisSqlGenerator import PostGISSqlGenerator

class SqlGeneratorFactory:
    def createSqlGenerator(self, isSpatialite):
        if isSpatialite:
            return SpatialiteSqlGenerator()
        else:
            return PostGISSqlGenerator()
