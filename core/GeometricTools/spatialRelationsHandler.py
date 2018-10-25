# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-05-01
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, \
                      QgsCoordinateTransform, QgsWkbTypes, edit, QgsCoordinateReferenceSystem, QgsProject, \
                      QgsProcessingMultiStepFeedback
from qgis.PyQt.Qt import QObject, QVariant
from qgis.analysis import QgsGeometrySnapper, QgsInternalGeometrySnapper

from .featureHandler import FeatureHandler
from .geometryHandler import GeometryHandler

class SpatialRelationsHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(SpatialRelationsHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.featureHandler = FeatureHandler(iface)
        self.geometryHandler = GeometryHandler(iface)
    
    def relateDrainagesWithContours(self, drainageLyr, contourLyr, frameLinesLyr, heightFieldName, threshold, topologyRadius, feedback=None):
        """
        Checks the conformity between directed drainages and contours. Drainages must be propperly directed.
        :param drainageLyr: QgsVectorLayer (line) with drainage lines. This must have a primary key field;
        :param contourLyr: QgsVectorLayer (line) with contour lines. This must have a primary key field;
        :param frameLinesLyrLyr: QgsVectorLayer (line) with frame lines;
        :param heightFieldName: (str) name of the field that stores contour's height;
        :param threshold: (int) equidistance between contour lines;
        :param threshold: (float) topology radius;
        Process steps:
        1- Build spatial indexes;
        2- Compute intersections between drainages and contours;
        3- Relate intersections grouping by drainages: calculate the distance between the start point and 
        each intersection, then order the points by distance. If the height of each point does not follow
        this order, flag the intersection.
        4- After relating everything, 
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(self.tr('Building drainage spatial index...'))
        drainageSpatialIdx, drainageIdDict = self.featureHandler.buildSpatialIndexAndIdDict
        (
            inputLyr=drainageLyr,
            feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(self.tr('Building contour spatial index...'))
        contourSpatialIdx, contourIdDict = self.featureHandler.buildSpatialIndexAndIdDict
        (
            inputLyr=contourLyr,
            feedback=multiStepFeedback
        )

    def buildIntersectionDict(self, drainageLyr, drainageIdDict, drainageSpatialIdx, contourIdDict, contourSpatialIdx):
        intersectionDict = dict()
        firstNode = lambda x:self.geometryHandler.getFirstNode(drainageLyr, x)
        lastNode = lambda x:self.geometryHandler.getLastNode(drainageLyr, x)
        addItemsToIntersectionDict = lambda x:self.addItemsToIntersectionDict(
            dictItem=x,
            contourSpatialIdx=contourSpatialIdx,
            contourIdDict=contourIdDict,
            intersectionDict=intersectionDict,
            firstNode=firstNode,
            lastNode=lastNode
        )
        # map for, this means: for item in drainageIdDict.items() ...
        list(map(addItemsToIntersectionDict, drainageIdDict.items()))
        return intersectionDict
    
    def addItemsToIntersectionDict(self, dictItem, contourSpatialIdx, contourIdDict, intersectionDict, firstNode, lastNode):
        gid, feat = dictItem
        featBB = feat.geometry().boundingBox()
        featid = feat.id()
        featGeom = feat.geometry()
        intersectionDict[featid] = {
            'start_point':firstNode(featGeom), 
            'end_point':lastNode(featGeom),
            'intersection_list':[]
            }
        for candidateId in contourSpatialIdx.intersects(featBB):
            candidate = contourIdDict[candidateId]
            if candidate.geometry().intersects(featGeom):
                intersectionDict[featid]['intersection_list'].append(candidate)

    
    def validateIntersections(self, drainageIdDict, drainageSpatialIdx, contourIdDict, contourSpatialIdx):
        