# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-14
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

from qgis.PyQt.QtWidgets import QWidget

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.postgisContainerWidget import PostgisContainerWidget
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.spatialiteContainerWidget import SpatialiteContainerWidget
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.shapefileContainerWidget import ShapefileContainerWidget
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.SupportedDrivers.geopackageContainerWidget import GeopackageContainerWidget
from DsgTools.core.dsgEnums import DsgEnums

class DatasourceSelectionWidgetFactory(QWidget):
    """
    Class designed to prepare each selection widget to be added to a widget container.
    """

    def getSelectionWidget(source, parent=None):
        """
        Gets the whole container widget, filled with selection widget, to be returned.
        :param parent: (QWidget) widget parent to newly instantiated selection widget.
        :param source: (DsgEnum.int) driver enum to have its widget produced.
        :return: (QWidget) selection widget for selected driver.
        """
        sourceDict = {
            DsgEnums.NoDriver : lambda : None,
            DsgEnums.PostGIS : lambda : PostgisContainerWidget(parent=parent),
            DsgEnums.NewPostGIS : lambda : PostgisContainerWidget(parent=parent),
            DsgEnums.SpatiaLite : lambda : SpatialiteContainerWidget(parent=parent),
            DsgEnums.NewSpatiaLite : lambda : SpatialiteContainerWidget(parent=parent),
            DsgEnums.Shapefile : lambda : ShapefileContainerWidget(parent=parent),
            DsgEnums.NewShapefile : lambda : ShapefileContainerWidget(parent=parent),
            DsgEnums.Geopackage : lambda : GeopackageContainerWidget(parent=parent),
            DsgEnums.NewGeopackage : lambda : GeopackageContainerWidget(parent=parent)
        }
        return sourceDict[source]()
