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

from qgis.core import QgsVertexId, QgsPointV2

from DsgTools.DsgGeometrySnapper.snapItem import SnapItem

class PointSnapItem(SnapItem):
    def __init__(self, _idx, type):
        """
        Constructor
        :param _idx: CoordIdx
        :param type: SnapPoint, SnapSegment
        """
        super(PointSnapItem, self).__init__(type)
        self.idx = _idx

    def getSnapPoint(self):
        """
        Get snap point
        :return:
        """
        return self.idx.point()

    def projPointOnSegment(self, p, s1, s2):
        """
        p: QgsPointV2
        s1: QgsPointV2 of segment
        s2: QgsPointV2 of segment
        """
        nx = s2.y() - s1.y()
        ny = -( s2.x() - s1.x() )
        t = ( p.x() * ny - p.y() * nx - s1.x() * ny + s1.y() * nx ) / ( ( s2.x() - s1.x() ) * ny - ( s2.y() - s1.y() ) * nx )
        if t < 0.:
            return s1
        elif t > 1.:
            return s2
        else:
            return QgsPointV2( s1.x() + ( s2.x() - s1.x() ) * t, s1.y() + ( s2.y() - s1.y() ) * t )