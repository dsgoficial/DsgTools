# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-03-15
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsField, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QGis, QgsCoordinateTransform
from PyQt4.Qt import QObject

class DsgGeometryHandler(QObject):
    def __init__(self, iface, parent = None):
        super(DsgGeometryHandler, self).__init__()
        self.parent = parent
        self.iface = iface
    
    def getFeatures(self, lyr, onlySelected = False, returnIterator = True, returnSize = True):
        if onlySelected:
            featureList = lyr.selectedFeatures()
            size = len(featureList)
        else:
            featureList = [i for i in lyr.getFeatures()] if not returnIterator else lyr.getFeatures()
            size = len(lyr.allFeatureIds())
        if returnIterator:
            return featureList, size
        else:
            return featureList
    
    def getClockWiseList(self, pointList):
        pointSum = 0
        for i in xrange(len(pointList) - 1):
            pointSum += (pointList[i+1].x() - pointList[i].x())*(pointList[i+1].y() + pointList[i].y())
        if pointSum > 0:
            return pointList
        else:
            return pointList[::-1]

    def reprojectFeature(self, geom, canvasCrs):
        """
        Reprojects geom from the canvas crs to the reference crs
        :param geom: geometry to be reprojected
        :param canvasCrs: canvas crs (from crs)
        """
        destCrs = self.reference.crs()
        if canvasCrs.authid() != destCrs.authid():
            coordinateTransformer = QgsCoordinateTransform(canvasCrs, destCrs)
            geom.transform(coordinateTransformer)

    def flipLine(self, feature):
        """
        Inverts the flow from a given feature.
        :param feature: feature to be flipped.
        :returns: flipped feature.
        """
        geom = feature.geometry()
        x = geom.asPolyline()
        print len(x), x