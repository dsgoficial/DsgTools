# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-13
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

from DsgTools.gui.CustomWidgets.DatasourceConversionWidgets.abstractSelectionWidget import AbstractSelectionWidget

class GeopackageWidget(AbstractSelectionWidget):
    """
    Class designed to manage geopackge widgets.
    """
    def __init__(self, parent=None):
        """
        Class contructor.
        :param parent: (QWidget) widget parent to newly instantiated geopackge widget.
        """
        super(GeopackageWidget, self).__init__(parent=parent)
        pass