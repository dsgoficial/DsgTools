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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QGis, QgsCoordinateTransform, QgsWKBTypes
from PyQt4.Qt import QObject

class DsgGeometryHandler(QObject):
    def __init__(self, iface, parent = None):
        super(DsgGeometryHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        self.canvas = iface.mapCanvas()
    
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

    def reprojectFeature(self, geom, referenceCrs, canvasCrs=None, coordinateTransformer=None, debugging=False):
        """
        Reprojects geom from the canvas crs to the reference crs.
        :param geom: geometry to be reprojected
        :param referenceCrs: reference CRS (coordinate reference system). 
        :param canvasCrs: canvas CRS. If not given, it'll be evaluated on runtime execution.
        :param coordinateTransformer: the coordinate transformer for canvas to reference CRS
        :param debbuging: if True, method returns the the list [geometry, canvasCrs, referenceCrs, coordinateTransformer]
        """
        if not canvasCrs:
            canvasCrs = self.canvas.mapRenderer().destinationCrs()
        if canvasCrs.authid() != referenceCrs.authid():
            if not coordinateTransformer:
                coordinateTransformer = QgsCoordinateTransform(canvasCrs, referenceCrs)
            geom.transform(coordinateTransformer)
        if debugging:
            return [geom, canvasCrs, referenceCrs, coordinateTransformer]

    def getFeatureNodes(self, layer, feature, geomType=None):
        """
        Inverts the flow from a given feature. THE GIVEN FEATURE IS ALTERED. Standard behaviour is to not
        refresh canvas map.
        :param layer: layer containing the target feature for flipping.
        :param feature: feature to be flipped.
        :param geomType: if layer geometry type is not given, it'll calculate it (0,1 or 2).
        :returns: feature as of a list of points (nodes).
        """
        if not geomType:
            geomType = layer.geometryType()
        # getting whether geometry is multipart or not
        isMulti = QgsWKBTypes.isMultiType(int(layer.wkbType()))
        geom = feature.geometry()
        if geomType == 0:
            if isMulti:
                nodes = geom.asMultiPoint()       
            else:
                nodes = geom.asPoint()              
        elif geomType == 1:
            if isMulti:
                nodes = geom.asMultiPolyline()
            else:
                nodes = geom.asPolyline()     
        elif geomType == 2:
            if isMulti:
                nodes = geom.asMultiPolygon()           
            else:
                nodes = geom.asPolygon()
        return nodes

    def flipFeature(self, layer, feature, geomType=None, refreshCanvas=False):
        """
        Inverts the flow from a given feature. THE GIVEN FEATURE IS ALTERED. Standard behaviour is to not
        refresh canvas map.
        :param layer: layer containing the target feature for flipping.
        :param feature: feature to be flipped.
        :param geomType: if layer geometry type is not given, it'll calculate it (0,1 or 2)
        :param refreshCanvas: indicates whether the canvas should be refreshed after flipping feature.
        :returns: flipped feature as of [layer, feature, geometry_type].
        """
        if not geomType:
            geomType = layer.geometryType()
        # getting whether geometry is multipart or not
        isMulti = QgsWKBTypes.isMultiType(int(layer.wkbType()))
        geom = feature.geometry()
        if geomType == 0:
            if isMulti:
                nodes = geom.asMultiPoint()
                # inverting the point list by parts
                for idx, part in enumerate(nodes):
                    nodes[idx] = part[::-1]
                # setting flipped geometry
                flippedFeatureGeom = QgsGeometry.fromMultiPoint(nodes)                
            else:
                # inverting the point list
                nodes = geom.asPoint()
                nodes = nodes[::-1]
                flippedFeatureGeom = QgsGeometry.fromPoint(nodes)                
        elif geomType == 1:
            if isMulti:
                nodes = geom.asMultiPolyline()
                for idx, part in enumerate(nodes):
                    nodes[idx] = part[::-1]
                flippedFeatureGeom = QgsGeometry.fromMultiPolyline(nodes)
            else:
                nodes = geom.asPolyline()
                nodes = nodes[::-1]
                flippedFeatureGeom = QgsGeometry.fromPolyline(nodes)         
        elif geomType == 2:
            if isMulti:
                nodes = geom.asMultiPolygon()                
                for idx, part in enumerate(nodes):
                    nodes[idx] = part[::-1]
                flippedFeatureGeom = QgsGeometry.fromMultiPolygon(nodes)                
            else:
                nodes = geom.asPolygon()
                nodes = nodes[::-1]
                flippedFeatureGeom = QgsGeometry.fromPolygon(nodes)
        # setting feature geometry to the flipped one
        # feature.setGeometry(flippedFeatureGeom)
        # layer.updateFeature(feature)
        layer.changeGeometry(feature.id(), flippedFeatureGeom)
        if refreshCanvas:
            self.iface.mapCanvas().refresh()
        return [layer, feature, geomType]
    
    # MISSING REPROJECTION
    def flipFeatureList(self, featureList, debugging=False, refreshCanvas=True):
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
            if len(item) == 3:
                geomType = item[2]
            else:
                geomType = layer.geometryType()
            try:
                revFeat = self.flipFeature(layer, feature, geomType)
                reversedFeatureList.append(revFeat)
            except:
                failedFeatureList.append(item)
        if refreshCanvas:
            self.iface.mapCanvas().refresh()
        if debugging:
            return reversedFeatureList, failedFeatureList
        else:
            return reversedFeatureList    

    def mergeLines(self, line_a, line_b, layer):
        """
        Merge 2 lines of the same layer (it is assumed that they share the same set od attributes - except for ID and geometry).
        In case sets are different, the set of geometry of line_a will be kept. If geometries don't touch, method is not applicable.
        :param line_a: (QgsFeature) main line of merging process.
        :param line_b: (QgsFeature) line to be merged to line_a.
        :param layer: (QgsVectorLayer) layer containing given lines.
        :return: (bool) True if method runs OK or False, if lines do not touch.
        """
        # check if original layer is a multipart
        isMulti = QgsWKBTypes.isMultiType(int(layer.wkbType()))
        # retrieve lines geometries
        geometry_a = line_a.geometry()
        geometry_b = line_b.geometry()
        # checking the spatial predicate touches
        if geometry_a.touches(geometry_b):
            # this generates a multi geometry
            geometry_a = geometry_a.combine(geometry_b)
            # this make a single line string if the multi geometries are neighbors
            geometry_a = geometry_a.mergeLines()
            if isMulti:
                # making a "single" multi geometry (EDGV standard)
                geometry_a.convertToMultiType()
            # updating feature
            line_a.setGeometry(geometry_a)
            # remove the aggregated line to avoid overlapping
            layer.deleteFeature(line_b.id())
            # updating layer
            layer.updateFeature(line_a)
            return True
            
        return False

    def getSegment(self, geom, referencePoint):
        if geom.isMultipart():
            multiLine = geom.asMultiPolyline()
            for i in xrange(len(multiLine)):
                line = multiLine[i]
                lineReturn = self.getSegmentFromLinestring(line, referencePoint)
                if lineReturn:
                    return lineReturn
        else:
            line = geom.asPolyline()
            lineReturn =  self.getSegmentFromLinestring(line, referencePoint)
            if lineReturn:
                    return lineReturn
        return []
    
    def getSegmentFromLinestring(self, line, referencePoint):
        lineSize = len(line)
        if line[0] == referencePoint.asPoint():
            if lineSize == 2:
                return line
            else:
                return line[0::2]
        if line[-1] == referencePoint.asPoint():
            if lineSize == 2:
                return line
            else:
                return line[-2:]
        return None