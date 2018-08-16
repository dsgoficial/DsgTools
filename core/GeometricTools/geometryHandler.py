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
from __future__ import absolute_import
from builtins import range
import math
from math import pi
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, \
                      QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateTransform, \
                      QgsWkbTypes, QgsProject, QgsVertexId, Qgis, QgsWkbTypes
from qgis.PyQt.Qt import QObject

class GeometryHandler(QObject):
    def __init__(self, iface=None, parent=None):
        super(GeometryHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if self.iface:
            self.canvas = iface.mapCanvas()
    
    def getClockWiseList(self, pointList):
        pointSum = 0
        for i in range(len(pointList) - 1):
            pointSum += (pointList[i+1].x() - pointList[i].x())*(pointList[i+1].y() + pointList[i].y())
        if pointSum > 0:
            return pointList
        else:
            return pointList[::-1]
    
    def reprojectWithCoordinateTransformer(self, geom, coordinateTransformer):
        if coordinateTransformer:
            geom.transform(coordinateTransformer)
        return geom
    
    def adjustGeometry(self, geom, parameterDict):
        geomList = []
        if geom is not None:
            if 'geometry' in dir(geom):
                if not parameterDict['hasMValues']:
                    geom.geometry().dropMValue()
                if not parameterDict['hasZValues']:
                    geom.geometry().dropZValue()
            if parameterDict['isMulti'] and not geom.isMultipart():
                geom.convertToMultiType()
                geomList.append(geom)
            if not parameterDict['isMulti'] and geom.isMultipart():
                #deaggregate here
                parts = geom.asGeometryCollection()
                for part in parts:
                    part.convertToSingleType()
                    geomList.append(part)
            else:
                geomList.append(geom)
        return geomList

    def reprojectFeature(self, geom, referenceCrs, destinationCrs=None, coordinateTransformer=None, debugging=False):
        """
        Reprojects geom from the canvas crs to the reference crs.
        :param geom: geometry to be reprojected
        :param referenceCrs: reference CRS (coordinate reference system). 
        :param canvasCrs: canvas CRS. If not given, it'll be evaluated on runtime execution.
        :param coordinateTransformer: the coordinate transformer for canvas to reference CRS
        :param debbuging: if True, method returns the the list [geometry, canvasCrs, referenceCrs, coordinateTransformer]
        """
        if not destinationCrs:
            destinationCrs = QgsProject.instance().crs()
        if destinationCrs.authid() != referenceCrs.authid():
            if not coordinateTransformer:
                coordinateTransformer = QgsCoordinateTransform(destinationCrs, referenceCrs, QgsProject.instance())
            geom.transform(coordinateTransformer)
        if debugging:
            return [geom, canvasCrs, referenceCrs, coordinateTransformer]

    def reprojectSearchArea(self, layer, geom):
        """
        Reprojects search area if necessary, according to what is being searched.
        :param layer: (QgsVectorLayer) layer which target rectangle has to have same SRC.
        :param geom: (QgsRectangle) rectangle representing search area.
        :return: (QgsRectangle) rectangle representing reprojected search area.
        """
        #geom always have canvas coordinates
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        #getting srid from something like 'EPSG:31983'
        srid = layer.crs().authid()
        if epsg == srid:
            return geom
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        crsDest = QgsCoordinateReferenceSystem(srid)
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance()) # here we have to put authid, not srid
        auxGeom = QgsGeometry.fromRect(geom)
        auxGeom.transform(coordinateTransformer)
        return auxGeom.boundingBox()

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
        isMulti = QgsWkbTypes.isMultiType(int(layer.wkbType()))
        geom = feature.geometry()
        if geomType == 0:
            if isMulti:
                nodes = geom.asMultiPoint()
                # inverting the point list by parts
                for idx, part in enumerate(nodes):
                    nodes[idx] = part[::-1]
                # setting flipped geometry
                flippedFeatureGeom = QgsGeometry.fromMultiPointXY(nodes)                
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
                flippedFeatureGeom = QgsGeometry.fromMultiPolylineXY(nodes)
            else:
                nodes = geom.asPolyline()
                nodes = nodes[::-1]
                flippedFeatureGeom = QgsGeometry.fromPolylineXY(nodes)         
        elif geomType == 2:
            if isMulti:
                nodes = geom.asMultiPolygon()                
                for idx, part in enumerate(nodes):
                    nodes[idx] = part[::-1]
                flippedFeatureGeom = QgsGeometry.fromMultiPolygonXY(nodes)                
            else:
                nodes = geom.asPolygon()
                nodes = nodes[::-1]
                flippedFeatureGeom = QgsGeometry.fromPolygonXY(nodes)
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
    
    def getOutOfBoundsAngleInPolygon(self, feat, part, angle, outOfBoundsList):
        for linearRing in part.asPolygon():
            linearRing = self.getClockWiseList(linearRing)
            nVertex = len(linearRing)-1
            for i in range(nVertex):
                if i == 0:
                    vertexAngle = (linearRing[i].azimuth(linearRing[-2]) - linearRing[i].azimuth(linearRing[i+1]) + 360)
                else:
                    vertexAngle = (linearRing[i].azimuth(linearRing[i-1]) - linearRing[i].azimuth(linearRing[i+1]) + 360)
                vertexAngle = math.fmod(vertexAngle, 360)
                if vertexAngle > 180:
                    # if angle calculated is the outter one
                    vertexAngle = 360 - vertexAngle
                if vertexAngle < angle:
                    geomDict = {'angle':vertexAngle,'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(linearRing[i])}
                    outOfBoundsList.append(geomDict)
    
    def getOutOfBoundsAngleInLine(self, feat, part, angle, outOfBoundsList):
        line = part.asPolyline()
        nVertex = len(line)-1
        for i in range(1,nVertex):
            vertexAngle = (line[i].azimuth(line[i-1]) - line[i].azimuth(line[i+1]) + 360)
            vertexAngle = math.fmod(vertexAngle, 360)
            if vertexAngle > 180:
                vertexAngle = 360 - vertexAngle
            if vertexAngle < angle:
                geomDict = {'angle':vertexAngle,'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(line[i])}
                outOfBoundsList.append(geomDict)
    
    def getOutOfBoundsAngle(self, feat, angle):
        outOfBoundsList = []
        geom = feat.geometry()
        for part in geom.asGeometryCollection():
            if part.type() == QgsWkbTypes.PolygonGeometry:
                self.getOutOfBoundsAngleInPolygon(feat, part, angle, outOfBoundsList)
            if part.type() == QgsWkbTypes.LineGeometry:
                self.getOutOfBoundsAngleInLine(feat, part, angle, outOfBoundsList)            
        return outOfBoundsList

    def getAngleBetweenSegments(self, part):
        line = part.asPolyline()
        vertexAngle = (line[1].azimuth(line[0]) - line[1].azimuth(line[2]) + 360)
        vertexAngle = math.fmod(vertexAngle, 360)
        if vertexAngle > 180:
            vertexAngle = 360 - vertexAngle
        return vertexAngle

    def getOutOfBountsAngleInSegmentList(self, segmentList, angle):
        for line1, line2 in combinations(segmentList, 2):
            geom = line1.combine(line2)
            part = geom.mergeLines()
            if len(part.asPolyline()) > 2:
                vertexAngle = self.getAngleBetweenSegments(part)
                if vertexAngle < angle:
                    return vertexAngle
        return None

    def getSegmentDict(self, lineLyr):
        segmentDict = dict()
        geomList = []
        for feat in lineLyr.getFeatures():
            geom = feat.geometry()
            if geom not in geomList:
                geomList.append(geom)
                lineList = geom.asPolyline()
                if lineList[0] not in segmentDict:
                    segmentDict[lineList[0]] = []
                segmentDict[lineList[0]].append(QgsGeometry.fromPolyline([lineList[0], lineList[1]]))
                if lineList[-1] not in segmentDict:
                    segmentDict[lineList[-1]] = []
                segmentDict[lineList[-1]].append(QgsGeometry.fromPolyline([lineList[-1], lineList[-2]]))
        return segmentDict
    
    def handleGeometry(self, geom, parameterDict = {}, coordinateTransformer = None):
        outputList = []
        for geom in self.adjustGeometry(geom, parameterDict):
            outputList += [self.reprojectWithCoordinateTransformer(geom, coordinateTransformer)]
        return outputList
    
    def getOuterShellAndHoles(self, geom, isMulti):
        outershells, donutholes = [], []
        for part in geom.asGeometryCollection():
            for current, item in enumerate(part.asPolygon()):
                newGeom = QgsGeometry.fromPolygonXY([item])
                if isMulti:
                    newGeom.convertToMultiType()
                if current == 0:
                    outershells.append(newGeom)
                else:
                    donutholes.append(newGeom)
        return outershells, donutholes
                
