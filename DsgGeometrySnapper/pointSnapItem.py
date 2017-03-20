# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-03-18
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsVertexId, QgsPointV2, QgsGeometry

from DsgTools.DsgGeometrySnapper.snapItem import SnapItem

class PointSnapItem(SnapItem):
    def __init__(self, _idx):
        """
        Constructor
        :param _idx: CoordIdx
        :param type: SnapPoint
        """
        super(PointSnapItem, self).__init__(0)
        self.idx = _idx

    def getSnapPoint(self):
        """
        Get snap point
        :return:
        """
        return self.idx.point()
