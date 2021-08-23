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
from itertools import combinations
import math
from math import pi
from functools import partial
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, \
                      QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateTransform, \
                      QgsWkbTypes, QgsProject, QgsVertexId, Qgis, QgsCoordinateReferenceSystem
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
            if geom.isMultipart():
                parts = geom.asGeometryCollection()
                for part in parts:
                    if parameterDict['isMulti']:
                        part.convertToMultiType()
                    geomList.append(part)
            else:
                if parameterDict['isMulti']:
                    geom.convertToMultiType()
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
        # features not yet commited to layer always have SINGLE geometry
        isMulti = QgsWkbTypes.isMultiType(int(layer.wkbType())) and feature.id() > 0
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

    def isclose(self, a, b, rel_tol=None, abs_tol=None):
        """
        Fuzzy compare from https://www.python.org/dev/peps/pep-0485/#proposed-implementation
        :param a:
        :param b:
        :param rel_tol:
        :param abs_tol:
        :return:
        """
        rel_tol = 1e-09 if rel_tol is None else rel_tol
        abs_tol = 0.0 if abs_tol is None else abs_tol
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
    def getOutOfBoundsAngleInPolygon(self, feat, part, angle, outOfBoundsList, exactAngleMatch=False, angTol=None, invalidRange=None):
        angTol = 0.1 if angTol is None else angTol
        if invalidRange is not None:
            minAngle, maxAngle = invalidRange
        for linearRing in part.asPolygon():
            linearRing = self.getClockWiseList(linearRing)
            nVertex = len(linearRing)-1
            def clause(x):
                return x < angle if not exactAngleMatch \
                    else not self.isclose(x, angle, abs_tol=angTol)
            clauseLambda = partial(clause)
            for i in range(nVertex):
                if i == 0:
                    vertexAngle = (linearRing[i].azimuth(linearRing[-2]) - linearRing[i].azimuth(linearRing[i+1]) + 360)
                else:
                    vertexAngle = (linearRing[i].azimuth(linearRing[i-1]) - linearRing[i].azimuth(linearRing[i+1]) + 360)
                vertexAngle = math.fmod(vertexAngle, 360)
                if vertexAngle > 180:
                    # if angle calculated is the outter one
                    vertexAngle = 360 - vertexAngle
                if invalidRange is not None and (vertexAngle >= minAngle and vertexAngle <= maxAngle):
                    geomDict = {'angle':vertexAngle, 'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(linearRing[i])}
                    outOfBoundsList.append(geomDict)
                    continue
                if clauseLambda(vertexAngle):
                    geomDict = {'angle':vertexAngle, 'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(linearRing[i])}
                    outOfBoundsList.append(geomDict)
    
    def getOutOfBoundsAngleInLine(self, feat, part, angle, outOfBoundsList, invalidRange=None):
        if invalidRange is not None:
            minAngle, maxAngle = invalidRange
        line = part.asPolyline()
        nVertex = len(line)-1
        for i in range(1,nVertex):
            vertexAngle = (line[i].azimuth(line[i-1]) - line[i].azimuth(line[i+1]) + 360)
            vertexAngle = math.fmod(vertexAngle, 360)
            if vertexAngle > 180:
                vertexAngle = 360 - vertexAngle
            if invalidRange is not None and (vertexAngle >= minAngle and vertexAngle <= maxAngle):
                geomDict = {'angle':vertexAngle, 'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(line[i])}
                outOfBoundsList.append(geomDict)
                continue
            if vertexAngle < angle:
                geomDict = {'angle':vertexAngle, 'feat_id':feat.id(), 'geom':QgsGeometry.fromPointXY(line[i])}
                outOfBoundsList.append(geomDict)
    
    def getInvalidBuildingAngle(self, feat, angTol):
        return self.getOutOfBoundsAngle(feat, 90, exactAngleMatch=True, angTol=angTol)
    
    def getOutOfBoundsAngle(self, feat, angle, exactAngleMatch=False, angTol=0.1, invalidRange=None):
        outOfBoundsList = []
        geom = feat.geometry()
        for part in geom.asGeometryCollection():
            if part.type() == QgsWkbTypes.PolygonGeometry:
                self.getOutOfBoundsAngleInPolygon(
                    feat,
                    part,
                    angle,
                    outOfBoundsList,
                    exactAngleMatch=exactAngleMatch,
                    angTol=angTol,
                    invalidRange=invalidRange
                )
            if part.type() == QgsWkbTypes.LineGeometry:
                self.getOutOfBoundsAngleInLine(feat,
                    part,
                    angle,
                    outOfBoundsList,
                    invalidRange=invalidRange
                )            
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
        if lineLyr.featureCount() > 0:
            toLineAlias = lambda geom : geom.asMultiPolyline()[0] if next(lineLyr.getFeatures()).geometry().isMultipart() \
                            else geom.asPolyline()
            fromLineAlias = lambda x : QgsGeometry.fromMultiPolylineXY([x]) if next(lineLyr.getFeatures()).geometry().isMultipart() \
                            else QgsGeometry.fromPolyline(x[0], x[1])
        for feat in lineLyr.getFeatures():
            geom = feat.geometry()
            if geom not in geomList:
                geomList.append(geom)
                lineList = toLineAlias(geom)
                if lineList[0] not in segmentDict:
                    segmentDict[lineList[0]] = []
                segmentDict[lineList[0]].append(fromLineAlias([lineList[0], lineList[1]]))
                if lineList[-1] not in segmentDict:
                    segmentDict[lineList[-1]] = []
                segmentDict[lineList[-1]].append(fromLineAlias([lineList[-1], lineList[-2]]))
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
    
    def getStartAndEndPointOnLine(self, geom):
        lineList = geom.asMultiPolyline() if geom.isMultipart() else [geom.asPolyline()]
        return lineList[0], lineList[len(lineList) - 1]
    
    def deaggregateGeometry(self, multiGeom):
        """
        Deaggregates a multi-part geometry into a its parts and returns all found parts. If no part is found,
        method returns original geometry.
        :param multiPartFeat: (QgsGeometry) multi part geometry to be deaggregated.
        :return: (list-of-QgsGeometry) list of deaggregated geometries
        """
        if not multiGeom or not multiGeom.get().partCount() > 1:
            return [multiGeom]
        # geometry list to be returned
        geomList = []
        parts = multiGeom.asGeometryCollection()
        for part in parts:
            if part:
                # asGeometryCollection() reads every part as single-part type geometry 
                part.convertToMultiType()
                geomList.append(part)
        return geomList

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
        isMulti = QgsWkbTypes.isMultiType(int(layer.wkbType()))
        geom = feature.geometry()
        return self.getGeomNodes(geom, geomType, isMulti)
    
    def getGeomNodes(self, geom, geomType, isMulti):
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
    
    def getFirstNode(self, lyr, feat, geomType=None):
        """
        Returns the starting node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][0]
        elif n:
            return n[0]

    def getSecondNode(self, lyr, feat, geomType=None):
        """
        Returns the second node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                # process doesn't treat multipart features that does have more than 1 part
                return
            return n[0][1]
        elif n:
            return n[1]

    def getPenultNode(self, lyr, feat, geomType=None):
        """
        Returns the penult node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which last node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: ending node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][-2]
        elif n:
            return n[-2]

    def getLastNode(self, lyr, feat, geomType=None):
        """
        Returns the ending point of a line.
        :param lyr: (QgsVectorLayer) layer containing target feature.
        :param feat: (QgsFeature) feature which last node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: ending node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][-1]
        elif n:
            return n[-1]

    def getFirstAndLastNode(self, lyr, feat, geomType=None):
        """
        Returns the first node and the last node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][0], n[0][-1]
        elif n:
            return n[0], n[-1]

    def calculateAngleDifferences(self, startNode, endNode):
        """
        Calculates the angle in degrees formed between line direction ('startNode' -> 'endNode') and vertical passing over 
        starting node.
        :param startNode: node (QgsPoint) reference for line and angle calculation.
        :param endNode: ending node (QgsPoint) for (segment of) line of which angle is required.
        :return: (float) angle in degrees formed between line direction ('startNode' -> 'endNode') and vertical passing over 'startNode'
        """
        # the returned angle is measured regarding 'y-axis', with + counter clockwise and -, clockwise.
        # Then angle is ALWAYS 180 - ang 
        return 180 - math.degrees(math.atan2(endNode.x() - startNode.x(), endNode.y() - startNode.y()))

    def calculateAzimuthFromNode(self, node, networkLayer, geomType=None):
        """
        Computate all azimuths from (closest portion of) lines flowing in and out of a given node.
        :param node: (QgsPoint) hidrography node reference for line and angle calculation.
        :param networkLayer: (QgsVectorLayer) hidrography line layer.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: dict of azimuths of all lines ( { featId : azimuth } )
        """
        if not geomType:
            geomType = networkLayer.geometryType()
        nodePointDict = self.nodeDict[node]
        azimuthDict = dict()
        for line in nodePointDict['start']:
            # if line starts at node, then angle calculate is already azimuth
            endNode = self.getSecondNode(lyr=networkLayer, feat=line, geomType=geomType)
            azimuthDict[line] = node.azimuth(endNode)
        for line in nodePointDict['end']:
            # if line ends at node, angle must be adapted in order to get azimuth
            endNode = self.getPenultNode(lyr=networkLayer, feat=line, geomType=geomType)
            azimuthDict[line] = node.azimuth(endNode)
        return azimuthDict

    def checkLineDirectionConcordance(self, line_a, line_b, networkLayer, geomType=None):
        """
        Given two lines, this method checks whether lines flow to/from the same node or not.
        If they do not have a common node, method returns false.
        :param line_a: (QgsFeature) line to be compared flowing to a common node.
        :param line_b: (QgsFeature) the other line to be compared flowing to a common node.
        :param networkLayer: (QgsVectorLayer) hidrography line layer.
        :return: (bool) True if lines are flowing to/from the same.
        """
        if not geomType:
            geomType = networkLayer.geometryType()
        # first and last node of each line
        fn_a = self.getFirstNode(lyr=networkLayer, feat=line_a, geomType=geomType)
        ln_a = self.getLastNode(lyr=networkLayer, feat=line_a, geomType=geomType)
        fn_b = self.getFirstNode(lyr=networkLayer, feat=line_b, geomType=geomType)
        ln_b = self.getLastNode(lyr=networkLayer, feat=line_b, geomType=geomType)
        # if lines are flowing to/from the same node (they are flowing the same way)
        return (fn_a == fn_b or ln_a == ln_b)

    def validateDeltaLinesAngV2(self, node, networkLayer, connectedValidLines, geomType=None):
        """
        Validates a set of lines connected to a node as for the angle formed between them.
        :param node: (QgsPoint) hidrography node to be validated.
        :param networkLayer: (QgsVectorLayer) hidrography line layer.
        :param connectedValidLines: list of (QgsFeature) lines connected to 'node' that are already verified.
        :param geomType: (int) layer geometry type. If not given, it'll be evaluated OTF.
        :return: (list-of-obj [dict, dict, str]) returns the dict. of valid lines, dict of inval. lines and
                 invalidation reason, if any, respectively.
        """
        val, inval, reason = dict(), dict(), ""
        if not geomType:
            geomType = networkLayer.geometryType()
        azimuthDict = self.calculateAzimuthFromNode(node=node, networkLayer=networkLayer, geomType=None)
        lines = azimuthDict.keys()
        for idx1, key1 in enumerate(lines):
            if idx1 == len(lines):
                # if first comparison element is already the last feature, all differences are already computed
                break
            for idx2, key2 in enumerate(lines):
                if idx1 >= idx2:
                    # in order to calculate only f1 - f2, f1 - f3, f2 - f3 (for 3 features, for instance)
                    continue
                absAzimuthDifference = math.fmod((azimuthDict[key1] - azimuthDict[key2] + 360), 360)
                if absAzimuthDifference > 180:
                    # the lesser angle should always be the one to be analyzed
                    absAzimuthDifference = (360 - absAzimuthDifference)
                if absAzimuthDifference < 90:
                    # if it's a 'beak', lines cannot have opposing directions (e.g. cannot flow to/from the same node)
                    if not self.checkLineDirectionConcordance(line_a=key1, line_b=key2, networkLayer=networkLayer, geomType=geomType):
                        reason = self.tr('Lines id={0} and id={1} have conflicting directions ({2:.2f} deg).').format(key1.id(), key2.id(), absAzimuthDifference)
                        # checks if any of connected lines are already validated by any previous iteration
                        if key1 not in connectedValidLines:
                            inval[key1.id()] = key1
                        if key2 not in connectedValidLines:
                            inval[key2.id()] = key2
                        return val, inval, reason
                elif absAzimuthDifference != 90:
                    # if it's any other disposition, lines can have the same orientation
                    continue
                else:
                    # if lines touch each other at a right angle, then it is impossible to infer waterway direction
                    reason = self.tr('Cannot infer directions for lines {0} and {1} (Right Angle)').format(key1.id(), key2.id())
                    if key1 not in connectedValidLines:
                            inval[key1.id()] = key1
                    if key2 not in connectedValidLines:
                        inval[key2.id()] = key2
                    return val, inval, reason
        if not inval:
            val = {k.id() : k for k in lines}
        return val, inval, reason
    
    def identifyAllNodes(self, networkLayer, onlySelected = False):
        """
        Identifies all nodes from a given layer (or selected features of it). The result is returned as a dict of dict.
        :param networkLayer: target layer to which nodes identification is required.
        :return: { node_id : { start : [feature_which_starts_with_node], end : feature_which_ends_with_node } }.
        """
        nodeDict = dict()
        isMulti = QgsWkbTypes.isMultiType(int(networkLayer.wkbType()))
        if onlySelected:
            features = [feat for feat in networkLayer.getSelectedFeatures()]
        else:
            features = [feat for feat in networkLayer.getFeatures()]
        for feat in features:
            nodes = self.getFeatureNodes(networkLayer, feat)
            if nodes:
                if isMulti:
                    if len(nodes) > 1:
                        # if feat is multipart and has more than one part, a flag should be raised
                        continue # CHANGE TO RAISE FLAG
                    elif len(nodes) == 0:
                        # if no part is found, skip feature
                        continue
                    else:
                        # if feat is multipart, "nodes" is a list of list
                        nodes = nodes[0]                
                # initial node
                pInit, pEnd = nodes[0], nodes[-1]
                # filling starting node information into dictionary
                if pInit not in nodeDict:
                    # if the point is not already started into dictionary, it creates a new item
                    nodeDict[pInit] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pInit]['start']:
                    nodeDict[pInit]['start'].append(feat)                            
                # filling ending node information into dictionary
                if pEnd not in nodeDict:
                    nodeDict[pEnd] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pEnd]['end']:
                    nodeDict[pEnd]['end'].append(feat)
        return nodeDict
    
    def makeQgsPolygonFromBounds(self, xmin, ymin, xmax, ymax, isMulti=True):
        """
        Creating a polygon for the given coordinates
        """
        dx = (xmax - xmin)/3
        dy = (ymax - ymin)/3
        
        polyline = []

        point = QgsPointXY(xmin, ymin)
        polyline.append(point)
        point = QgsPointXY(xmin+dx, ymin)
        polyline.append(point)
        point = QgsPointXY(xmax-dx, ymin) 
        polyline.append(point)
        point = QgsPointXY(xmax, ymin)
        polyline.append(point)
        point = QgsPointXY(xmax, ymin+dy)
        polyline.append(point)
        point = QgsPointXY(xmax, ymax-dy)
        polyline.append(point)
        point = QgsPointXY(xmax, ymax)
        polyline.append(point)
        point = QgsPointXY(xmax-dx, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin+dx, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin, ymax-dy)
        polyline.append(point)
        point = QgsPointXY(xmin, ymin+dy)
        polyline.append(point)
        point = QgsPointXY(xmin, ymin)
        polyline.append(point)

        if isMulti:
            qgsPolygon = QgsGeometry.fromMultiPolygonXY([[polyline]])
        else:
            qgsPolygon = QgsGeometry.fromPolygonXY([polyline])
        return qgsPolygon
    
    def handleGeometryCollection(self, geom, geometryType, parameterDict=None, coordinateTransformer=None):
        parameterDict = {} if parameterDict is None else parameterDict
        outputSet = set()
        for part in geom.asGeometryCollection():
            if part.type() == geometryType:
                handledList = self.handleGeometry(part, parameterDict=parameterDict, coordinateTransformer=coordinateTransformer)
                for item in handledList:
                    outputSet.add(item)
        return list(outputSet)
    
    def getFirstAndLastNodeFromGeom(self, geom):
        isMulti = geom.isMultipart()
        geomType = geom.type()
        n = self.getGeomNodes(geom, geomType, isMulti)
        if isMulti:
            if len(n) > 1:
                return
            return n[0][0], n[0][-1]
        elif n:
            return n[0], n[-1]

    def multiToSinglePart(self, geom):
        """
        Converts a multipart geometry to a list of single part.
        :param geom: (QgsGeometry) multipart geometry to be exploded.
        :return: (list-of-QgsGeometry) list of single part geometries found.
        """
        return [part for part in geom.asGeometryCollection()]

    def filterLayerByGeometry(self, listOfLayers):
        """
        Returns a dict from layers with geom type as key.
        :param listOfLayers: (QgsVectorLayer) list of layers.
        :return: (dict) dict of filtered layers.
        """
        filteredLayers = dict()

        for layer in listOfLayers:
            if layer.geometryType() == 0:
                filteredLayers['Point'] = layer
            elif layer.geometryType() == 1:
                filteredLayers['Line'] = layer
            elif layer.geometryType() == 2:
                filteredLayers['Polygon'] = layer
            else:
                pass

        return filteredLayers

