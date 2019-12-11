# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-22
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

from itertools import tee
from collections import defaultdict

from qgis.core import (Qgis,
                       QgsFeature,
                       QgsProject,
                       QgsGeometry,
                       QgsVectorLayer,
                       QgsSpatialIndex,
                       QgsFeatureRequest,
                       QgsProcessingContext,
                       QgsProcessingMultiStepFeedback)
from qgis.analysis import QgsGeometrySnapper, QgsInternalGeometrySnapper
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import QCoreApplication

from .featureHandler import FeatureHandler
from .geometryHandler import GeometryHandler
from .layerHandler import LayerHandler


class SpatialRelationsHandler(QObject):
    __predicates = (
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "equals"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "is not equals"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "disjoint"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "is not disjoint"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "intersects"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not intersect"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "touches"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not touch"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "crosses"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not cross"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "within"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "is not within"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "overlaps"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not overlap"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "contains"),
            QCoreApplication.translate("EnforceSpatialRulesAlgorithm", "does not contain")
        )
    EQUALS, NOTEQUALS, DISJOINT, NOTDISJOINT, INTERSECTS, NOTINTERSECTS, \
        TOUCHES, NOTTOUCHES, CROSSES, NOTCROSSES, WITHIN, NOTWITHIN, OVERLAPS, \
        NOTOVERLAPS, CONTAINS, NOTCONTAINS = range(len(__predicates))

    def __init__(self, iface = None, parent = None):
        super(SpatialRelationsHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.layerHandler = LayerHandler(iface)
        self.featureHandler = FeatureHandler(iface)
        self.geometryHandler = GeometryHandler(iface)
    
    def relateDrainagesWithContours(self, drainageLyr, contourLyr, frameLinesLyr, heightFieldName, threshold, topologyRadius, feedback=None):
        """
        Checks the conformity between directed drainages and contours.
        Drainages must be propperly directed.
        :param drainageLyr: QgsVectorLayer (line) with drainage lines.
        This must have a primary key field;
        :param contourLyr: QgsVectorLayer (line) with contour lines.
        This must have a primary key field;
        :param frameLinesLyrLyr: QgsVectorLayer (line) with frame lines;
        :param heightFieldName: (str) name of the field that stores
        contour's height;
        :param threshold: (int) equidistance between contour lines;
        :param threshold: (float) topology radius;
        Process steps:
        1- Build spatial indexes;
        2- Compute intersections between drainages and contours;
        3- Relate intersections grouping by drainages: calculate the
        distance between the start point and each intersection, then
        order the points by distance. If the height of each point does
        not follow this order, flag the intersection.
        4- After relating everything,
        """
        maxSteps = 4
        multiStepFeedback = QgsProcessingMultiStepFeedback(maxSteps, feedback) if feedback is not None else None
        currentStep = 0
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(
                self.tr('Building contour structures...')
                )
        contourSpatialIdx, contourIdDict, contourNodeDict, heightsDict = self.buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(
            inputLyr=contourLyr,
            attributeName=heightFieldName,
            feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(
                self.tr('Validating contour structures. Check 1/4...')
                )
        invalidDict = self.validateContourRelations(
            contourNodeDict,
            feedback=multiStepFeedback
            )
        if invalidDict:
            multiStepFeedback.setCurrentStep(maxSteps-1)
            return invalidDict

        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(
                self.tr('Building drainage spatial index...')
                )
        drainageSpatialIdx, drainageIdDict, drainageNodeDict = self.buildSpatialIndexAndIdDictAndRelateNodes(
            inputLyr=drainageLyr,
            feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            if multiStepFeedback.isCanceled():
                return []
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
            multiStepFeedback.pushInfo(
                self.tr('Relating contours with drainages...')
                )
        intersectionDict = self.buildIntersectionDict(
            drainageLyr,
            drainageIdDict,
            drainageSpatialIdx,
            contourIdDict,
            contourIdDict
            )

    def buildSpatialIndexAndIdDictAndRelateNodes(self, inputLyr, feedback=None, featureRequest=None):
        """
        creates a spatial index for the input layer
        :param inputLyr: (QgsVectorLayer) input layer;
        :param feedback: (QgsProcessingFeedback) processing feedback;
        :param featureRequest: (QgsFeatureRequest) optional feature request;
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        nodeDict = {}
        featCount = inputLyr.featureCount()
        size = 100/featCount if featCount else 0
        iterator = inputLyr.getFeatures() if featureRequest is None else inputLyr.getFeatures(featureRequest)
        firstAndLastNode = lambda x:self.geometryHandler.getFirstAndLastNode(inputLyr, x)
        addFeatureAlias = lambda x : self.addFeatureToSpatialIndexAndNodeDict(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            nodeDict=nodeDict,
            size=size,
            firstAndLastNode=firstAndLastNode,
            feedback=feedback
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict, nodeDict
    
    def addFeatureToSpatialIndexAndNodeDict(self, current, feat, spatialIdx, idDict, nodeDict, size, firstAndLastNode, feedback):
        """
        Adds feature to spatial index. Used along side with a python map operator
        to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param firstAndLastNode: (dict) dictionary used to relate nodes of features
        :param feedback: (QgsProcessingFeedback) feedback to be used on processing
        """
        firstNode, lastNode = firstAndLastNode(feat)
        if firstNode not in nodeDict:
            nodeDict[firstNode] = []
        nodeDict[firstNode] += [firstNode]
        if lastNode not in nodeDict:
            nodeDict[lastNode] = []
        nodeDict[lastNode] += [lastNode]
        self.layerHandler.addFeatureToSpatialIndex(current, feat, spatialIdx, idDict, size, feedback)

    def buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(self, inputLyr, attributeName, feedback=None, featureRequest=None):
        """

        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        nodeDict = {}
        attributeGroupDict = {}
        featCount = inputLyr.featureCount()
        size = 100/featCount if featCount else 0
        iterator = inputLyr.getFeatures() if featureRequest is None else inputLyr.getFeatures(featureRequest)
        firstAndLastNode = lambda x:self.geometryHandler.getFirstAndLastNode(inputLyr, x)
        addFeatureAlias = lambda x : self.addFeatureToSpatialIndexNodeDictAndAttributeGroupDict(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            nodeDict=nodeDict,
            size=size,
            firstAndLastNode=firstAndLastNode,
            attributeGroupDict=attributeGroupDict,
            attributeName=attributeName,
            feedback=feedback
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict, nodeDict, attributeGroupDict
    
    def addFeatureToSpatialIndexNodeDictAndAttributeGroupDict(self, current, feat, spatialIdx, idDict, nodeDict, size, firstAndLastNode, attributeGroupDict, attributeName, feedback):
        """
        Adds feature to spatial index. Used along side with a python map operator
        to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param firstAndLastNode: (dict) dictionary used to relate nodes of features
        :param feedback: (QgsProcessingFeedback) feedback to be used on processing
        """
        attrValue = feat[attributeName]
        if attrValue not in attributeGroupDict:
            attributeGroupDict[attrValue] = set()
        attributeGroupDict[attrValue].add(feat.geometry())
        self.addFeatureToSpatialIndexAndNodeDict(current, feat, spatialIdx, idDict, nodeDict, size, firstAndLastNode, feedback)
    
    def validateContourRelations(self, contourNodeDict, frameLinesDict, frameLinesSpatialIdx, heightFieldName, feedback=None):
        """
        param: contourNodeDict: (dict) dictionary with contour nodes
        Invalid contours:
        - Contours that relates to more than 2 other contours;
        - Contours that do not relate to any other contour and does not touch frame lines;
        """
        invalidDict = dict()
        contourId = lambda x : x.id()
        contoursNumber = len(contourNodeDict)
        step = 100/contoursNumber if contoursNumber else 0
        for current, (node, contourList) in enumerate(contourNodeDict.items()):
            if feedback is not None and feedback.isCanceled():
                break
            if len(contourList) == 1:
                if self.isDangle(node, frameLinesDict, frameLinesSpatialIdx):
                    invalidDict[node] = self.tr(
                        'Contour lines id=({ids}) touch each other and have different height values!'
                        ).format(ids=', '.join(map(contourId, contourList)))
            if len(contourList) == 2 and contourList[0][heightFieldName] != contourList[1][heightFieldName]:
                invalidDict[node] = self.tr(
                    'Contour lines id=({ids}) touch each other and have different height values!'
                    ).format(ids=', '.join(map(contourId, contourList)))
            if len(contourList) > 2:
                invalidDict[node] = self.tr(
                    'Contour lines id=({ids}) touch each other. Contour lines must touch itself or only one other.'
                    ).format(ids=', '.join(map(contourId, contourList)))
            if feedback is not None:
                feedback.setProgress(step * current)
        return invalidDict
    
    def isDangle(self, point, featureDict, spatialIdx, searchRadius=10**-15):
        """
        :param point: (QgsPointXY) node tested as dangle;
        :param featureDict: (dict) dict {featid:feat};
        :param spatialIdx: (QgsSpatialIndex) spatial index
        of features from featureDict;
        :param searchRadius: (float) search radius.
        """
        qgisPoint = QgsGeometry.fromPointXY(point)
        buffer = qgisPoint.buffer(searchRadius, -1)
        bufferBB = buffer.boundingBox()
        for featid in spatialIdx.intersects(bufferBB):
            if buffer.intersects(featureDict[featid].geometry()) and \
                qgisPoint.distance(featureDict[featid].geometry()) < 10**-9:
                return True
        return False

    def buildIntersectionDict(self, drainageLyr, drainageIdDict, drainageSpatialIdx, contourIdDict, contourSpatialIdx, feedback=None):
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
    
    def validateContourPolygons(self, contourPolygonDict, contourPolygonIdx, threshold, heightFieldName, depressionValueDict=None):
        hilltopDict = self.buildHilltopDict(
            contourPolygonDict,
            contourPolygonIdx
            )
        invalidDict = dict()
        for hilltopGeom, hilltop in hilltopDict.items():
            localFlagList = []
            polygonList = hilltop['downhill']
            feat = hilltop['feat']
            if len(polygonList) < 2:
                break
            # sort polygons by area, from minimum to max
            polygonList.sort(key=lambda x: x.geometry().area())
            #pair comparison
            a, b = tee([feat]+polygonList)
            next(b, None)
            for elem1, elem2 in zip(a, b):
                if abs(elem1[heightFieldName]-elem2[heightFieldName]) != threshold:
                    elem1GeomKey = elem1.geometry().asWkb()
                    if elem1GeomKey not in invalidDict:
                        invalidDict[elem1GeomKey] = []
                    invalidDict[elem1GeomKey] += [self.tr(
                        'Difference between contour with values {id1} \
                        and {id2} do not match equidistance {equidistance}.\
                        Probably one contour is \
                        missing or one of the contours have wrong value.\n'
                    ).format(
                        id1=elem1[heightFieldName],
                        id2=elem2[heightFieldName],
                        equidistance=threshold
                    )]
        return invalidDict
    
    def buildHilltopDict(self, contourPolygonDict, contourPolygonIdx):
        hilltopDict = dict()
        buildDictAlias = lambda x: self.initiateHilltopDict(x, hilltopDict)
        # c loop to build contourPolygonDict
        list(map(buildDictAlias, contourPolygonDict.values()))
        # iterate over contour polygon dict and build hilltopDict
        for idx, feat in contourPolygonDict.items():
            geom = feat.geometry()
            bbox = geom.boundingBox()
            geomWkb = geom.asWkb()
            for candId in contourPolygonIdx.intersects(bbox):
                candFeat = contourPolygonDict[candId]
                candGeom = candFeat.geometry()
                if candId != idx and candGeom.within(geom):
                    hilltopDict.pop(geomWkb.asWkb())
                    break
                if candId != idx and candGeom.contains(geom) \
                    and candFeat not in hilltopDict[geomWkb]['donwhill']:
                    hilltopDict[geomWkb]['donwhill'].append(candFeat)
            return hilltopDict
    
    def initiateHilltopDict(self, feat, hilltopDict):
        hilltopDict[feat.geometry().asWkb()] = {
                'feat' : feat,
                'downhill': []
            }
    
    def buildTerrainPolygons(self, featList):
        pass

    def validateContourLines(self, contourLyr, contourAttrName, refLyr, feedback=None):
        """
        1. Validate contour connectivity;
        2. Build terrain polygons by contour value;
        3. Build terrain dict;
        4. Validate contours.
        """
        pass
    
    def validateSpatialRelations(self, ruleList, createSpatialIndex=True, feedback=None):
        """
        1. iterate over rule list and get all layers.
        2. build spatial index
        3. test rule
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        spatialDict = self.buildSpatialDictFromRuleList(ruleList, feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        spatialRuleDict = self.buildSpatialRuleDict(ruleList, feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
        self.buildSpatialRelationDictOnSpatialRuleDict(
            spatialDict=spatialDict,
            spatialRuleDict=spatialRuleDict,
            feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(3)
        flagList = self.identifyInvalidRelations(spatialDict, spatialRuleDict, feedback=multiStepFeedback)
        return flagList

    def buildSpatialDictFromRuleList(self, ruleList, feedback=None):
        """
        returns {
            'key formed by layer name and filter' : {
                'spatial_index' : QgsSpatialIndex
                'feature_id_dict' : {
                    'feat_id' : 'feat'
                }
            }
        }
        """
        progressStep = 100/len(ruleList) if ruleList else 0
        spatialDict = defaultdict(dict)
        for current, rule in enumerate(ruleList):
            if feedback is not None and feedback.isCanceled():
                break
            inputKey = '_'.join(rule['input_layer'].name(), rule['input_layer_filter'])
            candidateKey = '_'.join(rule['candidate_layer'].name(), rule['candidate_layer_filter'])
            for key in [inputKey, candidateKey]:
                if key not in spatialDict:
                    spatialDict[key]['spatial_index'], spatialDict[key]['feature_id_dict'] = self.layerHandler.buildSpatialIndexAndIdDict(
                        inputLyr=rule['input_layer'],
                        featureRequest=rule['input_layer_filter']
                    )
            if feedback is not None:
                feedback.setProgress(current * progressStep)
        return spatialDict
    
    def buildSpatialRuleDict(self, ruleList, feedback=None):
        """
        ruleList comes from the ui
        Rule list has the following format:
        ruleList = [
            {
                'input_layer': QgsVectorLayer,
                'input_layer_filter' : str,
                'predicate' : str,
                'candidate_layer' : QgsVectorLayer,
                'candidate_layer_filter' : str,
                'cardinality' : str,
                'feat_relation_list' : list of pairs of (featId, relatedFeatures),
                'flag_text' : str
            }
        ]

        outputs:
        { 'input_layer_input_layer_filter' : {
                        'input_layer': QgsVectorLayer,
                        'input_layer_filter' : str,
                        'rule_list' : [
                            {
                                'predicate' : str,
                                'candidate_layer' : QgsVectorLayer,
                                'candidate_layer_filter' : str,
                                'cardinality' : str,
                                'flag_text' : str,
                                'feat_relation_list' : list of pairs of (featId, relatedFeatures)
                            }
                        ]
                    }
        }
        """
        spatialRuleDict = defaultdict(
            lambda : {
                'input_layer' : None,
                'input_layer_filter' : '',
                'rule_list' : []
            }
        )
        progressStep = 100/len(ruleList) if ruleList else 0
        for current, rule in enumerate(ruleList):
            if feedback is not None and feedback.isCanceled():
                break
            key = '_'.join(rule['input_layer'].name(), rule['input_layer_filter'])
            spatialRuleDict[key]['input_layer'] = rule['input_layer']
            spatialRuleDict[key]['input_layer_filter'] = rule['input_layer_filter']
            spatialRuleDict[key]['rule_list'].append(
                {k:v for k, v in rule.items() if 'input' not in k}
            )
            if feedback is not None:
                feedback.setProgress(current * progressStep)
        return spatialRuleDict

    def buildSpatialRelationDictOnSpatialRuleDict(self, spatialDict, spatialRuleDict, feedback=None):
        """
        layerFeatureDict = {
            'layer_name' = {
                featId : QgsFeature
            }
        }
        spatialIndexDict = {
            'layer_name' : QgsSpatialIndex
        }
        spatialRuleDict = { 'input_layer_input_layer_filter' : {
                                                                    'input_layer': QgsVectorLayer,
                                                                    'input_layer_filter' : str,
                                                                    'rule_list' : [
                                                                        {
                                                                            'predicate' : str,
                                                                            'candidate_layer' : QgsVectorLayer,
                                                                            'candidate_layer_filter' : str,
                                                                            'cardinality' : str,
                                                                            'flag_text' : str
                                                                        }
                                                                    ]
                                                                }
        }

        """
        totalSteps = self.countSteps(spatialRuleDict, spatialDict)
        progressStep = 100/totalSteps if totalSteps else 0
        counter = 0
        for inputKey, inputDict in spatialRuleDict.items():
            if feedback is not None and feedback.isCanceled():
                break
            keyRuleList = ['_'.join(i['candidate_layer'], i['candidate_layer_filter']) for i in inputDict['rule_list']]
            for featId, feat in spatialDict[inputKey]['feature_id_dict']:
                if feedback is not None and feedback.isCanceled():
                    break
                for idx, rule in enumerate(inputDict['rule_list']):
                    if feedback is not None and feedback.isCanceled():
                        break
                    rule['feat_relation_list'].append( 
                        (
                            featId, self.relateFeatureAccordingToPredicate(
                                feat=feat,
                                rule=rule,
                                key=keyRuleList[idx],
                                predicate=rule['predicate'],
                                spatialDict=spatialDict
                            )
                        )
                    )
                    counter+=1
                    if feedback is not None:
                        feedback.setProgress(counter * progressStep)
    
    def countSteps(self, spatialRuleDict, spatialDict):
        """
        Counts the number of steps of execution.
        """
        steps = len(spatialRuleDict)
        for k,v in spatialRuleDict.items():
            steps += len(v['rule_list'])
            steps += len(spatialDict[k]['feature_id_dict'])
        return steps

    def identifyInvalidRelations(self, spatialDict, spatialRuleDict, feedback=None):
        """
        Identifies invalid spatial relations and returns a list with flags to be raised.
        """
        totalSteps = self.countSteps(spatialRuleDict, spatialDict)
        progressStep = 100/totalSteps if totalSteps else 0
        counter = 0
        invalidFlagList = []
        for inputKey, inputDict in spatialRuleDict:
            if feedback is not None and feedback.isCanceled():
                        break
            inputLyrName = inputDict['input_layer']
            for rule in inputDict['rule_list']:
                if feedback is not None and feedback.isCanceled():
                        break
                candidateLyrName = inputDict['candidate_layer']
                candidateKey = '_'.join(candidateLyrName, inputDict['candidate_layer_filter'])
                sameLayer = True if inputKey == candidateKey else False
                lambdaCompair = self.parseCardinalityAndGetLambdaToIdentifyProblems(
                    cardinality=rule['cardinality'],
                    necessity=rule['necessity'],
                    isSameLayer=sameLayer
                )
                for featId, relatedFeatures in rule['feat_relation_list']:
                    if feedback is not None and feedback.isCanceled():
                        break
                    inputFeature=spatialDict[inputKey][featId]
                    if lambdaCompair(relatedFeatures):
                        if inputLyrName == candidateLyrName and inputFeature in relatedFeatures:
                            relatedFeatures.pop(inputFeature)
                        invalidFlagList += self.buildSpatialFlags(
                            inputFeature=inputFeature,
                            relatedFeatures=relatedFeatures,
                            flagText=rule['flag_text']
                        )
                    if feedback is not None:
                        feedback.setProgress(counter * progressStep)
                        counter += 1
        return invalidFlagList
    
    def buildSpatialFlags(self, inputLyrName, inputFeature, candidateLyrName, relatedFeatures, flagText):
        input_id = inputFeature.id()
        inputGeom = inputFeature.geometry()
        spatialFlags = []
        for feat in relatedFeatures:
            flagGeom = inputGeom.intersection(feat.geometry().constGet())
            flagText = self.tr('Feature from {input} with id {input_id} violates the following predicate with feature from {candidate} with id {candidate_id}: {predicate_text}').format(
                input=inputLyrName,
                input_id=input_id,
                candidate=candidateLyrName,
                candidate_id=feat.id(),
                predicate_text=flagText
            )
            spatialFlags.append(
                {
                    'flagGeom' : flagGeom,
                    'flagText' : flagText
                }
            )
        return spatialFlags

    def availablePredicates(self):
        """
        Returns the name of all available predicates.
        :return: (tuple-of-str) list of available predicates.
        """
        return {i: p for i, p in enumerate(self.__predicates)}

    def getCardinalityTest(self, cardinality):
        """
        Parses cardinality string and gets a callable to check if the iterable
        tested is not complying with the cardinality.
        :param cardinality: (str) cardinality string to be tested against.
        """
        if cardinality is None:
            return lambda x: len(x) != 0
        min_card, max_card = cardinality.split('..')
        if max_card == '*':
            test = lambda x : len(x) < int(min_card)
        elif min_card == max_card:
            test = lambda x: len(x) != int(min_card)
        else:
            test = lambda x : len(x) < int(min_card) or len(x) > int(max_card)
        return test
                
    def testPredicate(self, predicate, engine, targetGeometries):
        """
        Applies a predicate test to a given feature from a list of features.
        :param predicate: (int) topological relation code to be tested against.
        :param engine: (QgsGeometryEngine) reference feature's QGIS structure
                       for based on geometries for faster spatial operations.
        :param targetGeometries: (dict) maps feature ids to their geometries
                                 that will be tested.
        :return: (set-of-int) feature ids that comply with the predicate. 
        """
        # negatives are disregarded. method simply apply the predicate comparison
        positives = set()
        methods = {
            self.EQUALS : "isEqual",
            self.DISJOINT : "disjoint",
            self.INTERSECTS : "intersects",
            self.TOUCHES : "touches",
            self.CROSSES : "crosses",
            self.WITHIN : "within",
            self.OVERLAPS : "overlaps",
            self.CONTAINS : "contains"
        }
        if predicate not in methods:
            raise NotImplementedError(
                self.tr("Invalid predicate ({0}).").format(predicate)
            )
        predicateMethod = methods[predicate]
        for test_fid, test_geom in targetGeometries.items():
            if getattr(engine, predicateMethod)(test_geom.constGet()):
                positives.add(test_fid)
        return positives

    def checkPredicate(self, layerA, layerB, predicate, cardinality, ctx=None, feedback=None):
        """
        Checks if a duo of layers comply with a spatial predicate at a given
        cardinality.
        :param layerA: (QgsVectorLayer) reference layer.
        :param layerB: (QgsVectorLayer) layer to have its features spatially
                    compared to reference layer.
        :param predicate: (str) topological comparison method to be applied.
        :param cardinality: (str) a formatted string that informs minimum and
                            maximum occurences of a spatial predicate.
        
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map from offended feature IDs to the list of its
                offending features.
        """
        flags = defaultdict(list)
        # getFlagGeometryMethod = {
        #     # fill up with appropriate methods
        # }[predicate]
        getFlagGeometryMethod = lambda a, b: a.intersection(b)
        testingMethod = self.getCardinalityTest(cardinality)
        layerNameA = layerA.name()
        layerNameB = layerB.name()
        geometriesB = {f.id(): f.geometry() for f in layerB.getFeatures()}
        for featA in layerA.getFeatures():
            geomA = featA.geometry()
            engine = QgsGeometry.createGeometryEngine(geomA.constGet())
            engine.prepareGeometry()
            positives = self.testPredicate(predicate, engine, geometriesB)
            if testingMethod(positives):
                fidA = featA.id()
                for fidB in positives:
                    flags[fidA] += [{
                        "text": self.tr(
                            "feature {fidA} from layer {layer_a} {pred} feature"
                            " {fidB} from layer {layer_b}."
                            .format(
                                fidA=fidA, layer_a=layerNameA, pred=predicate,
                                layer_b=layerNameB, fidB=fidB
                            )
                        ),
                        "geom": getFlagGeometryMethod(geomA, geometriesB[fidB])
                    }]
        return flags

    def setupLayer(self, layerName, exp, ctx=None, feedback=None):
        """
        Retrieves layer from canvas and applies filtering expression. If CRS is
        different than project's, layer is reprojected.
        :param layerName: (str) layer's name on canvas.
        :param exp: (str) filtering expression to be applied to target layer.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (QgsVectorLayer) layer ready to be compared.
        """
        lh = LayerHandler()
        ctx = ctx or QgsProcessingContext()
        if exp:
            layer = lh.filterByExpression(
                layerName, exp, ctx, feedback
            )
        else:
            # this will raise an error if layer is not loaded
            layer = QgsProject.instance().mapLayersByName(layerName)
            if not layer:
                return
            layer = layer[0]
        projectCrs = QgsProject.instance().crs()
        if layer.crs() != projectCrs:
            layer = lh.runReprojectLayer(layer, projectCrs)
        return layer

    def enforceRule(self, rule, ctx=None, feedback=None):
        """
        Applies a given set of spatial restrictions to a duo of layers.
        :param rule: (dict) a map to spatial rule's parameters.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map from offended feature's ID to offenders feature set.
        """
        lh = LayerHandler()
        ctx = ctx or QgsProcessingContext()
        layerA = self.setupLayer(
            rule["layer_a"], rule["filter_a"], ctx, feedback
        )
        layerB = self.setupLayer(
            rule["layer_b"], rule["filter_b"], ctx, feedback
        )
        return self.checkPredicate(
            layerA, layerB, rule["predicate"], rule["cardinality"], ctx, feedback
        )

    def enforceRules(self, ruleSet, ctx=None, feedback=None):
        """
        Applies a set of spatial rules to current active layers on canvas.
        :param ruleSet: (dict) all rules that should be applied to canvas.
        :param ctx: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (dict) a map of offended rules to its flags.
        """
        out = dict()
        ctx = ctx or QgsProcessingContext()
        for rule in ruleSet:
            if feedback is not None:
                feedback.pushInfo(
                    self.tr("Checking rule {0}...").format(rule["name"])
                )
            flags = self.enforceRule(rule, ctx, feedback)
            if flags:
                out[rule["name"]] = flags
                feedback.pushInfo(
                    self.tr("Rule {0} raised flags").format(rule["name"])
                )
            else:
                feedback.pushInfo(
                    self.tr("Rule {0} did not raise flags\n")
                    .format(rule["name"])
                )
        return out

    def verifyTopologicalRelation(self, predicate, layerA, layerB, cardinality, context=None, feedback=None):
        """
        Verifies a given topological relation between two layers, returning a
        vector layer pointing where these predicates have happened.
        :param predicate: (int) topological relation to be tested.
        :param layerA: (QgsVectorLayer) reference layer to be tested.
        :param layerB: (QgsVectorLayer) the other layer to be tested.
        :param cardinality: (str) a string representing the upper and lower
                            bounds of occurrences an event can happen between
                            the target layers.
        :param context: (QgsProcessingContext) environment context in which 
                        layer is retrieved and setup.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (QgsVectorLayer) layer containing features representing the
                 occurrences of the given test (their flags).
        """
        # TO BE REMOVED
        denials = [
            self.NOTEQUALS,
            self.NOTDISJOINT,
            self.NOTINTERSECTS,
            self.NOTTOUCHES,
            self.NOTCROSSES,
            self.NOTWITHIN,
            self.NOTOVERLAPS,
            self.NOTCONTAINS
        ]
        output = dict()
        if predicate in denials:
            # denials always follow the "positives", hence -1
            # denials are ALWAYS absolute (cardinality is not applicable)
            predicate -= 1
            predicateTest = lambda x: len(x) > 0
        else:
            predicateTest = self.getCardinalityTest(cardinality)
        for feat in layerA.getFeatures():
            flags = self.testPredicate(
                predicate,
                feat,
                layerB.getFeatures(
                    QgsFeatureRequest(feat.geometry().boundingBox())
                )
            )
            if predicateTest(flags):
                # still missing how to get flag geometry
                output[feat.id()] = flags
        return output
