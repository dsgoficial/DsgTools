 
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from .SupportedDrivers.multiPostgisSelectorWidget import MultiPostgisSelectorWidget
from DsgTools.core.dsgEnums import DsgEnums

class MultiDsWidgetFactory:
    """
    Class to produce multiple datasource dialalogs.
    """
    def getMultiDsSelector(driver):
        """
        Gets the dialog to be used for selecting multiple datasources of a given driver.
        :param driver: (int) driver enum. 
        """
        dialogDict = {
            DsgEnums.PostGIS : lambda : MultiPostgisSelectorWidget()
            # DsgEnums.SpatiaLite : lambda : MultiSpatiaLiteSelectorWidget(),
            # DsgEnums.Shapefile : lambda : MultiShapefileSelectorWidget(),
            # DsgEnums.Geopackage : lambda : MultiGeopackageSelectorWidget()
        }
        return dialogDict[driver]()
