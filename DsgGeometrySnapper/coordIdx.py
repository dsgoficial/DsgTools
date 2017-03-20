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

from qgis.core import QgsAbstractGeometryV2, QgsVertexId, QgsGeometry

class CoordIdx:
    def __init__(self, _geom, _vidx):
        """
        Constructor
        :param _geom: QgsAbstractGeometryV2
        :param _vidx: QgsVertexId
        """
        self.geom = _geom
        self.vidx = _vidx

    def point(self):
        return self.geom.vertexAt(self.vidx)

if __name__ == '__main__':
    refGeom = QgsGeometry.fromWkt("Polygon((0 0, 10 0, 10 10, 0 10, 0 0))")
    absGeomV2 = refGeom.geometry()
    vidx = QgsVertexId(0, 0, 0, QgsVertexId.SegmentVertex)
    coordIdx = CoordIdx(absGeomV2, vidx)
    print 'saida', coordIdx.point()