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

    def flipFeature(self, layer, feature):
        """
        Inverts the flow from a given feature. THE GIVEN FEATURE IS ALTERED.
        :param layer: layer containing the target feature for flipping.
        :param feature: feature to be flipped.
        :returns: flipped feature.
        """
        geom = feature.geometry()
        nodes = geom.asPolyline()
        flippedFeatureGeom = QgsGeometry.fromPolyline(nodes.reverse())
        layer.changeGeometry(feature.id(), flippedFeatureGeom)
        return flippedFeatureGeom
    
    # MISSING REPROJECTION
    def flipFeatureList(self, featureList, debugging=False):
        """
        Inverts the flow from all features of a given list. ALL GIVEN FEATURES ARE ALTERED.
        :param featureList: list of features to be flipped ([layer, feature[, geometry_type]).
        :param debugging: optional parameter to indicate whether or not a list of features that failed
                          to be reversed should be returner. 
        :returns: list of flipped features.
        """
        reversedFeatureList = []
        failedFeatureList = []
        for item in featureList:
            layer, feature = item[0], item[1]
            if not isinstance(layer, QgsVectorLayer):
                # ignore non-vector layers.
                continue
            try:
                reversedFeatureList.append(self.flipFeature(layer, feature))
            except:
                failedFeatureList.append(self.flipFeature(layer, feature))
        if debugging and failedFeatureList:
            return reversedFeatureList, failedFeatureList
        else:
            return reversedFeatureList
