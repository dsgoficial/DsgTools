 
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
from .SupportedDrivers.multiSpatialiteSelectorWidget import MultiSpatialiteSelectorWidget
from .SupportedDrivers.multiShapefileSelectorWidget import MultiShapefileSelectorWidget
from .SupportedDrivers.multiGeopackageSelectorWidget import MultiGeopackageSelectorWidget
from .SupportedDrivers.multiNewDsSelector import MultiNewDsSelector
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
            DsgEnums.NoDriver : lambda : None,
            DsgEnums.PostGIS : lambda : MultiPostgisSelectorWidget(),
            DsgEnums.NewPostGIS : lambda : MultiNewDsSelector(),
            DsgEnums.SpatiaLite : lambda : MultiSpatialiteSelectorWidget(),
            DsgEnums.NewSpatiaLite : lambda : MultiNewDsSelector(),
            DsgEnums.Shapefile : lambda : MultiShapefileSelectorWidget(),
            DsgEnums.NewShapefile : lambda : MultiNewDsSelector(),
            DsgEnums.Geopackage : lambda : MultiGeopackageSelectorWidget(),
            DsgEnums.NewGeopackage : lambda : MultiNewDsSelector()
        }
        return dialogDict[driver]()
