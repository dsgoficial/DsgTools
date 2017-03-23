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
import sys

from qgis.core import QGis, QgsFeatureRequest, QgsSpatialIndex, QgsGeometry, QgsPointV2, QgsFeatureRequest, QgsFeatureIterator\
, QgsFeature, QgsVertexId, QgsCurvePolygonV2, QgsVectorLayer, QgsMultiPolygonV2, QgsPolygonV2, QgsPoint, QgsCircularStringV2, QgsSurfaceV2

from DsgTools.DsgGeometrySnapper.dsgSnapIndex import DsgSnapIndex
from DsgTools.DsgGeometrySnapper.pointSnapItem import PointSnapItem
from DsgTools.DsgGeometrySnapper.segmentSnapItem import SegmentSnapItem

class DsgGeometrySnapper:
    SnappedToRefNode, SnappedToRefSegment, Unsnapped = range(3)
    PreferNodes, PreferClosest = range(2)

    def __init__(self, referenceLayer):
        """
        Constructor
        :param referenceLayer: QgsVectorLayer
        """
        self.referenceLayer = referenceLayer
        # Build spatial index
        self.index = QgsSpatialIndex(self.referenceLayer.getFeatures())
        
    def polyLineSize(self, geom, iPart, iRing):
        """
        Gets the number of vertexes
        :param geom: QgsAbstractGeometryV2
        :param iPart: int
        :param iRing: int
        :return:
        """
        nVerts = geom.vertexCount( iPart, iRing)
        if isinstance(geom, QgsMultiPolygonV2) or isinstance(geom, QgsPolygonV2) or isinstance(geom, QgsCircularStringV2):
            front = geom.vertexAt(QgsVertexId( iPart, iRing, 0, QgsVertexId.SegmentVertex))
            back = geom.vertexAt(QgsVertexId( iPart, iRing, nVerts - 1, QgsVertexId.SegmentVertex))
            if front == back:
                return nVerts - 1
        return nVerts

    def snapFeatures(self, features, snapTolerance, mode=PreferNodes):
        """
        Snap features from a layer
        :param features: list of QgsFeatures
        :param snapTolerance: float
        :param mode: DsgGeometrySnapper.PreferNodes or DsgGeometrySnapper.PreferClosest
        :return:
        """
        for feature in features:
            self.processFeature(feature, snapTolerance, mode)
        return features

    def processFeature(self, feature, snapTolerance, mode):
        """
        Process QgsFeature
        :param feature: QgsFeature
        :param snapTolerance: float
        :param mode: DsgGeometrySnapper.PreferNodes or DsgGeometrySnapper.PreferClosest
        :return:
        """
        if feature.geometry():
            feature.setGeometry(self.snapGeometry(feature.geometry(), snapTolerance, mode))
    
    def projPointOnSegment(self, p, s1, s2):
        """
        p: QgsPointV2
        s1: QgsPointV2 of segment
        s2: QgsPointV2 of segment
        """
        nx = s2.y() - s1.y()
        ny = -( s2.x() - s1.x() )
        a = ( p.x() * ny - p.y() * nx - s1.x() * ny + s1.y() * nx )
        b = ( ( s2.x() - s1.x() ) * ny - ( s2.y() - s1.y() ) * nx )
        if s1 == s2:
            return s1
        t = a / b
        if t < 0.:
            return s1
        elif t > 1.:
            return s2
        else:
            return QgsPointV2( s1.x() + ( s2.x() - s1.x() ) * t, s1.y() + ( s2.y() - s1.y() ) * t )

    def buildReferenceIndex(self, segments):
        refDict = {}
        index = QgsSpatialIndex()
        for i, segment in enumerate(segments):
            refDict[i] = segment
            feature = QgsFeature(i)
            feature.setGeometry(segment)
            index.insertFeature(feature)
        return refDict, index

    def segmentFromPoints(self, start, end):
        """
        Makes a QgsGeometry from start and end points
        :param start: QgsPoint
        :param end: QgsPoint
        :return:
        """
        return QgsGeometry.fromPolyline([start, end])

    def breakQgsGeometryIntoSegments(self, geometry):
        """
        Makes a list of QgsGeometry made with segments
        :param geometry: QgsGeometry
        :return: list of QgsGeometry
        """
        segments = []
        wbkType = geometry.wkbType()
        if wbkType == QGis.WKBPoint:
            return [geometry]
        elif wbkType == QGis.WKBMultiPoint:
            return [geometry]
        elif wbkType == QGis.WKBLineString:
            line = geometry.asPolyline()
            for i in xrange(len(line) - 1):
                segments.append(self.segmentFromPoints(line[i], line[i + 1]))
        elif wbkType == QGis.WKBMultiLineString:
            multiLine = geometry.asMultiPolyline()
            for j in xrange(len(multiLine)):
                line = multiLine[j]
                for i in xrange(len(line) - 1):
                    segments.append(self.segmentFromPoints(line[i], line[i + 1]))
        elif wbkType == QGis.WKBPolygon:
            poly = geometry.asPolygon()
            for j in xrange(len(poly)):
                line = poly[j]
                for i in xrange(len(line) - 1):
                    segments.append(self.segmentFromPoints(line[i], line[i + 1]))
        elif wbkType == QGis.WKBMultiPolygon:
            multiPoly = geometry.asMultiPolygon()
            for k in xrange(len(multiPoly)):
                poly = multiPoly[k]
                for j in xrange(len(poly)):
                    line = poly[j]
                    for i in xrange(len(line) - 1):
                        segments.append(self.segmentFromPoints(line[i], line[i + 1]))

        return segments

    def snapGeometry(self, geometry, snapTolerance, mode=PreferNodes):
        """
        Snaps a QgsGeometry in the reference layer
        :param geometry: QgsGeometry
        :param snapTolerance: float
        :param mode: DsgGeometrySnapper.PreferNodes or DsgGeometrySnapper.PreferClosest
        :return:
        """
        center = QgsPointV2(geometry.boundingBox().center())

        # Get potential reference features and construct snap index
        refGeometries = []
        searchBounds = geometry.boundingBox()
        searchBounds.grow(snapTolerance)
        # filter by bounding box to get candidates
        refFeatureIds = self.index.intersects(searchBounds)

        # End here in case we don't find candidates
        if len(refFeatureIds) == 0:
            return geometry

        # speeding up the process to consider only intersecting geometries
        refFeatureRequest = QgsFeatureRequest().setFilterFids(refFeatureIds)
        for refFeature in self.referenceLayer.getFeatures(refFeatureRequest):
            refGeometry = refFeature.geometry()
            segments = self.breakQgsGeometryIntoSegments(refGeometry)
            # testing intersection
            for segment in segments:
                if segment.intersects(searchBounds):
                    refGeometries.append(segment)

        # End here in case we don't find geometries
        if len(refGeometries) == 0:
            return geometry

        # building geometry index
        refDict, index = self.buildReferenceIndex(refGeometries)
        refSnapIndex = DsgSnapIndex(center, 10*snapTolerance)
        for geom in refGeometries:
            refSnapIndex.addGeometry(geom.geometry())

        # Snap geometries
        subjGeom = geometry.geometry().clone()
        subjPointFlags = []

        # Pass 1: snap vertices of subject geometry to reference vertices
        for iPart in xrange(subjGeom.partCount()):
            subjPointFlags.append([])
            for iRing in xrange(subjGeom.ringCount(iPart)):
                subjPointFlags[iPart].append([])
                for iVert in xrange(self.polyLineSize(subjGeom, iPart, iRing)):
                    vidx = QgsVertexId(iPart, iRing, iVert, QgsVertexId.SegmentVertex)
                    p = QgsPointV2(subjGeom.vertexAt(vidx))
                    pF = QgsPoint(p.toQPointF())
                    point2Snap = QgsGeometry.fromPoint(pF)
                    candidateIds = index.intersects(point2Snap.boundingBox())
                    features = [refDict[i] for i in candidateIds]
                    snapPoint, snapSegment = refSnapIndex.getSnapItem(p, snapTolerance)
                    success = snapPoint or snapSegment
                    if not success:
                        subjPointFlags[iPart][iRing].append(DsgGeometrySnapper.Unsnapped )
                    else:
                        if mode == DsgGeometrySnapper.PreferNodes:
                            # Prefer snapping to point
                            if snapPoint:
                                subjGeom.moveVertex(vidx, snapPoint.getSnapPoint(p))
                                subjPointFlags[iPart][iRing].append(DsgGeometrySnapper.SnappedToRefNode)
                            elif snapSegment:
                                subjGeom.moveVertex( vidx, snapSegment.getSnapPoint(p))
                                subjPointFlags[iPart][iRing].append(DsgGeometrySnapper.SnappedToRefSegment)
                        elif mode == DsgGeometrySnapper.PreferClosest:
                            nodeSnap = None
                            segmentSnap = None
                            distanceNode = sys.float_info.max
                            distanceSegment = sys.float_info.max
                            if snapPoint:
                                nodeSnap = snapPoint.getSnapPoint(p)
                                nodeSnapF = QgsPoint(nodeSnap.toQPointF())
                                distanceNode = nodeSnapF.sqrDist(pF)
                            if snapSegment:
                                segmentSnap = snapSegment.getSnapPoint(p)
                                segmentSnapF = QgsPoint(segmentSnap.toQPointF())
                                distanceSegment = segmentSnapF.sqrDist(pF)
                            if snapPoint and (distanceNode < distanceSegment):
                                subjGeom.moveVertex( vidx, nodeSnap )
                                subjPointFlags[iPart][iRing].append(DsgGeometrySnapper.SnappedToRefNode)
                            elif snapSegment:
                                subjGeom.moveVertex(vidx, segmentSnap)
                                subjPointFlags[iPart][iRing].append(DsgGeometrySnapper.SnappedToRefSegment)

        #nothing more to do for points
        if isinstance(subjGeom, QgsPointV2):
            return QgsGeometry(subjGeom)
        
        # SnapIndex for subject feature
        subjSnapIndex = DsgSnapIndex(center, 10*snapTolerance)
        segments = self.breakQgsGeometryIntoSegments(QgsGeometry(subjGeom.clone()))
        for segment in segments:
            subjSnapIndex.addGeometry(segment.geometry())
        
        origSubjSnapIndex = DsgSnapIndex(center, 10*snapTolerance)
        for segment in segments:
            origSubjSnapIndex.addGeometry(segment.geometry())
        
        # Pass 2: add missing vertices to subject geometry
        for refGeom in refGeometries:
            for iPart in xrange(refGeom.geometry().partCount()):
                for iRing in xrange(refGeom.geometry().ringCount(iPart)):
                    for iVert in xrange(self.polyLineSize(refGeom.geometry(), iPart, iRing)):
                        point = refGeom.geometry().vertexAt(QgsVertexId(iPart, iRing, iVert, QgsVertexId.SegmentVertex))
                        # QgsPoint used to calculate squared distance
                        pointF = QgsPoint(point.toQPointF())
                        snapPoint, snapSegment = subjSnapIndex.getSnapItem(point, snapTolerance)
                        success = snapPoint or snapSegment
                        if success:
                            # Snap to segment, unless a subject point was already snapped to the reference point
                            if snapPoint and (QgsPoint(snapPoint.getSnapPoint(point).toQPointF()).sqrDist(pointF) < 1E-16):
                                continue
                            elif snapSegment:
                                # Look if there is a closer reference segment, if so, ignore this point
                                pProj = snapSegment.getSnapPoint(point)
                                pProjF = QgsPoint(pProj.toQPointF())
                                closest = refSnapIndex.getClosestSnapToPoint(point, pProj)
                                closestF = QgsPoint(closest.toQPointF())
                                if pProjF.sqrDist(pointF) > pProjF.sqrDist(closestF):
                                    continue
                                # If we are too far away from the original geometry, do nothing
                                if not origSubjSnapIndex.getSnapItem(point, snapTolerance):
                                    continue
                                idx = snapSegment.idxFrom
                                subjGeom.insertVertex(QgsVertexId(idx.vidx.part, idx.vidx.ring, idx.vidx.vertex + 1, QgsVertexId.SegmentVertex), point)
                                subjPointFlags[idx.vidx.part][idx.vidx.ring].insert(idx.vidx.vertex + 1, DsgGeometrySnapper.SnappedToRefNode )
                                subjSnapIndex = DsgSnapIndex(center, 10*snapTolerance)
                                subjSnapIndex.addGeometry(subjGeom)

        # Pass 3: remove superfluous vertices: all vertices which are snapped to a segment and not preceded or succeeded by an unsnapped vertex
        for iPart in xrange(subjGeom.partCount()):
            for iRing in xrange(subjGeom.ringCount(iPart)):
                ringIsClosed = subjGeom.vertexAt(QgsVertexId(iPart, iRing, 0, QgsVertexId.SegmentVertex)) == subjGeom.vertexAt(QgsVertexId(iPart, iRing, subjGeom.vertexCount( iPart, iRing ) - 1, QgsVertexId.SegmentVertex))
                nVerts = self.polyLineSize(subjGeom, iPart, iRing)
                iVert = 0
                while iVert < nVerts:
                    iPrev = ( iVert - 1 + nVerts ) % nVerts
                    iNext = ( iVert + 1 ) % nVerts
                    pMid = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iVert, QgsVertexId.SegmentVertex))
                    pPrev = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iPrev, QgsVertexId.SegmentVertex))
                    pNext = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iNext, QgsVertexId.SegmentVertex))

                    pointOnSeg = self.projPointOnSegment( pMid, pPrev, pNext)
                    pointOnSegF = QgsPoint(pointOnSeg.toQPointF())
                    pMidF = QgsPoint(pMid.toQPointF())
                    dist = pointOnSegF.sqrDist(pMidF)

                    if subjPointFlags[iPart][iRing][iVert] == DsgGeometrySnapper.SnappedToRefSegment \
                     and subjPointFlags[iPart][iRing][iPrev] != DsgGeometrySnapper.Unsnapped \
                     and subjPointFlags[iPart][iRing][iNext] != DsgGeometrySnapper.Unsnapped \
                     and dist < 1E-12:
                        if (ringIsClosed and nVerts > 3 ) or ( not ringIsClosed and nVerts > 2 ):
                            subjGeom.deleteVertex(QgsVertexId(iPart, iRing, iVert, QgsVertexId.SegmentVertex))
                            del subjPointFlags[iPart][iRing][iVert]
                            iVert -= 1
                            nVerts -= 1
                        else:
                            # Don't delete vertices if this would result in a degenerate geometry
                            break
                    iVert += 1
        return QgsGeometry(subjGeom)

