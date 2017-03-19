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

from qgis.core import QgsVector, QgsPointV2

from DsgTools.DsgGeometrySnapper.snapItem import SnapItem

class SegmentSnapItem(SnapItem):
    def __init__(self, _idxFrom, _idxTo, type):
        """
        Constructor
        :param _idxFrom: CoordIdx
        :param _idxTo: CoordIdx
        :param type: SnapPoint, SnapSegment
        """
        super(SegmentSnapItem, self).__init__(type)
        self.idxFrom = _idxFrom
        self.idxto = _idxTo

    def getSnapPoint(self, p):
        """
        :param p: QgsPointV2
        :return:
        """
        return self.projPointOnSegment(p, self.idxFrom.point(), self.idxTo.point())

    def getIntersection(self, p1, p2, inter):
        """
        Get intersection on segment
        :param p1: QgsPointV2
        :param p2: QgsPointV2
        :param inter: QgsPointV2 reference
        :return: bool
        """
        q1 = self.idxFrom.point()
        q2 = self.idxTo.point()
        v = QgsVector(p2.x() - p1.x(), p2.y() - p1.y())
        w = QgsVector(q2.x() - q1.x(), q2.y() - q1.y())
        vl = v.length()
        wl = w.length()

        if self.isclose(vl, 0.) or self.isclose(wl, 0.):
            return False

        v = v / vl
        w = w / wl

        d = v.y() * w.x() - v.x() * w.y()

        if d == 0:
            return False

        dx = q1.x() - p1.x()
        dy = q1.y() - p1.y()
        k = (dy * w.x() - dx * w.y()) / d

        inter = QgsPointV2(p1.x() + v.x() * k, p1.y() + v.y() * k)

        lambdav = QgsVector(inter.x() - p1.x(), inter.y() - p1.y()) * v
        if lambdav < 0. + 1E-8 or lambdav > vl - 1E-8:
            return False

        lambdaw = QgsVector(inter.x() - q1.x(), inter.y() - q1.y()) * w
        if lambdaw < 0. + 1E-8 or lambdaw >= wl - 1E-8:
            return False

        return True

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        """
        Fuzzy compare from https://www.python.org/dev/peps/pep-0485/#proposed-implementation
        :param a:
        :param b:
        :param rel_tol:
        :param abs_tol:
        :return:
        """
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def getProjection(self, p, pProj):
        """
        Get the p projection on segment
        :param p: QgsPointV2
        :param pProj: QgsPointV2 reference
        :return: bool
        """
        s1 = QgsPointV2(self.idxFrom.point())
        s2 = QgsPointV2(self.idxTo.point())
        nx = s2.y() - s1.y()
        ny = -(s2.x() - s1.x())
        t = (p.x() * ny - p.y() * nx - s1.x() * ny + s1.y() * nx) / ((s2.x() - s1.x()) * ny - (s2.y() - s1.y()) * nx)
        if t < 0. or t > 1.:
            return False

        pProj = QgsPointV2(s1.x() + (s2.x() - s1.x()) * t, s1.y() + (s2.y() - s1.y()) * t)
        return True
