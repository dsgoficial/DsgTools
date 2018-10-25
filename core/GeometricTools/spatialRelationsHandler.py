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
        flagDict = dict()
        firstNode = lambda x:self.geometryHandler.getFirstNode(drainageLyr, x)
        lastNode = lambda x:self.geometryHandler.getLastNode(drainageLyr, x)
        addItemsToIntersectionDict = lambda x:self.addItemsToIntersectionDict(
            dictItem=x,
            contourSpatialIdx=contourSpatialIdx,
            contourIdDict=contourIdDict,
            intersectionDict=intersectionDict,
            firstNode=firstNode,
            lastNode=lastNode,
            flagDict=flagDict
        )
        # map for, this means: for item in drainageIdDict.items() ...
        list(map(addItemsToIntersectionDict, drainageIdDict.items()))
        return intersectionDict
    
    def addItemsToIntersectionDict(self, dictItem, contourSpatialIdx, contourIdDict, intersectionDict, firstNode, lastNode, flagDict):
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
            candidateGeom = candidate.geometry()
            if candidateGeom.intersects(featGeom): #add intersection
                intersectionGeom = candidateGeom.intersection(featGeom)
                intersectionList += [intersectionGeom.asPoint()] if not intersectionGeom.asMultiPoint() else intersectionGeom.asMultiPoint()
                flagFeature = True if len(intersectionList) > 1 else False
                for inter in intersectionList:
                    if flagFeature:
                        flagDict[inter] = self.tr('Contour id={c_id} intersects drainage id={d_id} in more than one point').format(
                            c_id=candidateId,
                            d_id=gid
                        )
                    newIntersection = {
                    'contour_id' : candidateId,
                    'intersection_point' : inter
                    }
                    intersectionDict[featid]['intersection_list'].append(newIntersection)
    
    def validateIntersections(self, intersectionDict, heightFieldName, threshold):
        """
        1- Sort list
        2- 
        """
        validatedIdsDict = dict()
        invalidatedIdsDict = dict()
        for id, values in intersectionDict.items():
            interList = values['intersection_list']
            if len(interList) <= 1:
                continue
            #sort list by distance from start point
            interList.sort(key=lambda x: x['intersection_point'].geometry().distance(values['start_point']))
            referenceElement = interList[0]
            for idx, elem in enumerate(interList[1::], start=1):
                elemen_id = elem.id()
                if int(elem[heightFieldName]) != threshold*idx + int(referenceElement[heightFieldName]):
                    invalidatedIdsDict[elemen_id] = elem
                else:
                    if elemen_id not in invalidatedIdsDict:
                        validatedIdsDict[elemen_id] = elem
        for id in validatedIdsDict:
            if id in invalidatedIdsDict:
                validatedIdsDict.pop(id)
        return validatedIdsDict, invalidatedIdsDict

            