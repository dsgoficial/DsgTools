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

from PyQt4.QtCore import QObject, QtConcurrent

from qgis.core import QgsFeatureRequest, QgsAttributeList, QgsSpatialIndex, QgsGeometry, QgsPointV2, QgsGeometryUtils, QgsFeatureRequest, QgsFeatureIterator, QgsFeature, QgsVertexId, QgsPointV2, QgsCurvePolygonV2, QgsVertexId, QgsVectorLayer

from DsgTools.DsgGeometrySnapper.dsgSnapIndex import DsgSnapIndex

class DsgGeometrySnapper(QObject):
    SnappedToRefNode, SnappedToRefSegment, Unsnapped = range(3)
    PreferNodes, PreferClosest = range(2)

    def __init__(self, referenceLayer):
        super(DsgGeometrySnapper, self).__init__()        
        self.referenceLayer = referenceLayer
        # Build spatial index
        req = QgsFeatureRequest()
        req.setSubsetOfAttributes(QgsAttributeList())
        self.index = QgsSpatialIndex(self.referenceLayer.getFeatures(req))        
        
    def polyLineSize(self, geom, iPart, iRing):   
        nVerts = geom.vertexCount( iPart, iRing)
        if QgsCurvePolygonV2(geom):
            front = geom.vertexAt(QgsVertexId( iPart, iRing, 0))
            back = geom.vertexAt(QgsVertexId( iPart, iRing, nVerts - 1))
        if front == back:
            return nVerts - 1
        return nVerts

    def snapFeatures(self, features, snapTolerance, mode):
        for feature in features:
            self.processFeature(feature, snapTolerance, mode)
        return features

    def processFeature(self, feature, snapTolerance, mode):
        if not feature.geometry().isNull():
            feature.setGeometry(self.snapGeometry(feature.geometry(), snapTolerance, mode))

    def snapGeometry(self, geometry, snapTolerance, mode):
        center = QgsPointV2(geometry.geometry())
        if not center:
            center = QgsPointV2(geometry.geometry().boundingBox().center())

        # Get potential reference features and construct snap index
        refGeometries = []
        searchBounds = geometry.boundingBox()
        searchBounds.grow(snapTolerance)
        refFeatureIds = self.index.intersects(searchBounds)

        refFeatureRequest = QgsFeatureRequest().setFilterFids( refFeatureIds ).setSubsetOfAttributes( QgsAttributeList() )
        refFeature = None
        refFeatureIt = self.referenceLayer.getFeatures( refFeatureRequest )

        while refFeatureIt.nextFeature(refFeature):
            refGeometries.append(refFeature.geometry())

        refSnapIndex = DsgSnapIndex(center, 10 * snapTolerance)
        for geom in refGeometries:
            refSnapIndex.addGeometry( geom.geometry() )


        # Snap geometries
        subjGeom = geometry.geometry().clone()
        subjPointFlags = [[[]]]

        # Pass 1: snap vertices of subject geometry to reference vertices
        for iPart in range(len(subjGeom.partCount())):
            subjPointFlags.append([[]])
            for iRing in range(len(subjGeom.ringCount(iPart))):
                subjPointFlags[iPart].append([])
                for iVert in range(self.polyLineSize(subjGeom, iPart, iRing)):
                    snapPoint = None
                    snapSegment = None
                    vidx = QgsVertexId(iPart, iRing, iVert)
                    p = QgsPointV2(subjGeom.vertexAt(vidx))
                    if not refSnapIndex.getSnapItem(p, snapTolerance, snapPoint, snapSegment):
                        subjPointFlags[iPart][iRing].append( self.Unsnapped )
                    else:
                        if mode == self.PreferNodes:
                            # Prefer snapping to point
                            if snapPoint:
                                subjGeom.moveVertex(vidx, snapPoint.getSnapPoint(p))
                                subjPointFlags[iPart][iRing].append(self.SnappedToRefNode)
                            elif snapSegment:
                                subjGeom.moveVertex( vidx, snapSegment.getSnapPoint(p))
                                subjPointFlags[iPart][iRing].append(self.SnappedToRefSegment)
                        elif mode == self.PreferClosest:
                            nodeSnap = None
                            segmentSnap = None
                            distanceNode = sys.float_info.max
                            distanceSegment = sys.float_info.max
                            if snapPoint:
                                nodeSnap = snapPoint.getSnapPoint(p)
                                distanceNode = nodeSnap.distanceSquared(p)
                            if snapSegment:
                                segmentSnap = snapSegment.getSnapPoint(p)
                                distanceSegment = segmentSnap.distanceSquared(p)
                            if snapPoint and distanceNode < distanceSegment:
                                subjGeom.moveVertex( vidx, nodeSnap )
                                subjPointFlags[iPart][iRing].append(self.SnappedToRefNode)
                            elif snapSegment:
                                subjGeom.moveVertex( vidx, segmentSnap )
                                subjPointFlags[iPart][iRing].append(self.SnappedToRefSegment)

        #nothing more to do for points
        if QgsPointV2(subjGeom):
            return QgsGeometry(subjGeom)
        
        # SnapIndex for subject feature
        subjSnapIndex = DsgSnapIndex(center, 10 * snapTolerance)
        subjSnapIndex.addGeometry(subjGeom)
        
        origSubjGeom = subjGeom.clone()
        origSubjSnapIndex =  DsgSnapIndex(center, 10 * snapTolerance)
        origSubjSnapIndex.addGeometry(origSubjGeom.get())
        
        # Pass 2: add missing vertices to subject geometry
        for refGeom in refGeometries:
            for iPart in range(len(refGeom.geometry().partCount())):
                subjPointFlags.append([[]])
                for iRing in range(len(refGeom.geometry().ringCount(iPart))):
                    subjPointFlags[iPart].append([])
                    for iVert in range(self.polyLineSize(refGeom.geometry(), iPart, iRing)):
                        snapPoint = None
                        snapSegment = None
                        point = refGeom.geometry().vertexAt(QgsVertexId(iPart, iRing, iVert))
                        if subjSnapIndex.getSnapItem( point, snapTolerance, snapPoint, snapSegment):
                            # Snap to segment, unless a subject point was already snapped to the reference point
                            if snapPoint and QgsGeometryUtils.sqrDistance2D(snapPoint.getSnapPoint(point), point) < 1E-16:
                                continue
                            elif snapSegment:
                                # Look if there is a closer reference segment, if so, ignore this point
                                pProj = snapSegment.getSnapPoint(point)
                                closest = refSnapIndex.getClosestSnapToPoint(point, pProj)
                            if QgsGeometryUtils.sqrDistance2D(pProj, point ) > QgsGeometryUtils.sqrDistance2D(pProj, closest):
                                continue
                            # If we are too far away from the original geometry, do nothing
                            if not origSubjSnapIndex.getSnapItem( point, snapTolerance):
                                continue
                            idx = snapSegment.idxFrom
                            subjGeom.insertVertex(QgsVertexId(idx.vidx.part, idx.vidx.ring, idx.vidx.vertex + 1 ), point)
                            subjPointFlags[idx.vidx.part][idx.vidx.ring].insert(idx.vidx.vertex + 1, self.SnappedToRefNode )
                            subjSnapIndex = DsgSnapIndex(center, 10 * snapTolerance)
                            subjSnapIndex.addGeometry(subjGeom)

        # Pass 3: remove superfluous vertices: all vertices which are snapped to a segment and not preceded or succeeded by an unsnapped vertex
        for iPart in range(len(subjGeom.partCount())):
            for iRing in range(len(subjGeom.ringCount(iPart))):
                ringIsClosed = subjGeom.vertexAt(QgsVertexId(iPart, iRing, 0)) == subjGeom.vertexAt(QgsVertexId(iPart, iRing, subjGeom.vertexCount( iPart, iRing ) - 1))
                nVerts = self.polyLineSize(subjGeom, iPart, iRing)
                for iVert in range(nVerts):
                    iPrev = ( iVert - 1 + nVerts ) % nVerts
                    iNext = ( iVert + 1 ) % nVerts
                    pMid = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iVert))
                    pPrev = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iPrev))
                    pNext = subjGeom.vertexAt(QgsVertexId( iPart, iRing, iNext))

                    if subjPointFlags[iPart][iRing][iVert] == self.SnappedToRefSegment and subjPointFlags[iPart][iRing][iPrev] != self.Unsnapped and subjPointFlags[iPart][iRing][iNext] != self.Unsnapped and QgsGeometryUtils.sqrDistance2D(QgsGeometryUtils.projPointOnSegment( pMid, pPrev, pNext ), pMid ) < 1E-12:
                        if (ringIsClosed and nVerts > 3 ) or ( not ringIsClosed and nVerts > 2 ):
                            subjGeom.deleteVertex(QgsVertexId(iPart, iRing, iVert))
                            subjPointFlags[iPart][iRing].removeAt(iVert)
                            iVert -= 1
                            nVerts -= 1
                        else:
                            # Don't delete vertices if this would result in a degenerate geometry
                            break
        return QgsGeometry(subjGeom)

if name == '__main__':
    rl = QgsVectorLayer("Polygon", "x", "memory");
    ff = QgsFeature()
    refGeom = QgsGeometry.fromWkt("Polygon((0 0, 10 0, 10 10, 0 10, 0 0))");
    ff.setGeometry(refGeom)
    flist = []
    flist.append(ff)
    rl.dataProvider().addFeatures(flist)

    polygonGeom = QgsGeometry.fromWkt("Polygon((0.1 -0.1, 10.1 0, 9.9 10.1, 0 10, 0.1 -0.1))");
    snapper = DsgGeometrySnapper(rl)
    result = snapper.snapGeometry(polygonGeom, 1)
    print 'saida' result.exportToWkt()
    print 'esperado', "Polygon ((0 0, 10 0, 10 10, 0 10, 0 0))"
