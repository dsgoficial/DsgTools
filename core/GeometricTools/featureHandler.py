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
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateTransform, QgsWkbTypes
from qgis.PyQt.Qt import QObject

from .geometryHandler import GeometryHandler
from .attributeHandler import AttributeHandler

class FeatureHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(FeatureHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.geometryHandler = GeometryHandler(iface)
        self.attributeHandler = AttributeHandler(iface)
    
    def reclassifyFeatures(self, featureList, destinationLayer, reclassificationDict, coordinateTransformer, parameterDict):
        newFeatList = []
        deleteList = []
        for feat in featureList:
            geom = self.geometryHandler.reprojectWithCoordinateTransformer(feat.geometry(), coordinateTransformer)
            geomList = self.geometryHandler.adjustGeometry(geom, parameterDict)
            newFeatList += self.createFeaturesWithAttributeDict(geomList, feat, reclassificationDict, destinationLayer)
            deleteList.append(feat.id())
        return newFeatList, deleteList
    
    def createFeaturesWithAttributeDict(self, geomList, originalFeat, attributeDict, destinationLayer):
        """
        Creates a newFeatureList using each geom from geomList. attributeDict is used to set attributes
        """
        newFeatureList = []
        fields = destinationLayer.fields()
        for geom in geomList:
            newFeature = QgsFeature(fields)
            newFeature.setGeometry(geom)
            newFeature = self.attributeHandler.setFeatureAttributes(newFeature, attributeDict, oldFeat = originalFeat)
            newFeatureList.append(newFeature)
        return newFeatureList

    def createUnifiedFeature(self, unifiedLyr, feature, classname, bList = None, attributeTupple = False, coordinateTransformer = None, parameterDict = None):
        parameterDict = {} if parameterDict is None else parameterDict
        bList = [] if bList is None else bList
        newFeats = []
        for geom in self.geometryHandler.handleGeometry(feature.geometry(), parameterDict=parameterDict, coordinateTransformer=coordinateTransformer):
            newfeat = QgsFeature(unifiedLyr.fields())
            newfeat.setGeometry(feature.geometry())
            newfeat['featid'] = feature.id()
            newfeat['layer'] = classname
            if attributeTupple:
                newfeat['tupple'] = self.attributeHandler.getTuppleAttribute(feature, unifiedLyr, bList=bList)
            newFeats.append(newfeat)
        return newFeats
    
    def getNewFeatureWithoutGeom(self, referenceFeature, lyr):
        newFeat = QgsFeature(referenceFeature)
        provider = lyr.dataProvider()
        for idx in lyr.primaryKeyAttributes():
            newFeat.setAttribute(idx, None)
        return newFeat
    
    def handleFeature(self, featList, featureWithoutGeom, lyr, parameterDict = None, coordinateTransformer = None):
        parameterDict = {} if parameterDict is None else parameterDict
        geomList = []
        for feat in featList:
            geomList += self.geometryHandler.handleGeometry(feat.geometry(), parameterDict)
        geomToUpdate = None
        newFeatList = []
        if not geomList:
            return geomToUpdate, [], True
        for idx, geom in enumerate(geomList):
            if idx == 0:
                geomToUpdate = geom
                continue
            else:
                newFeat = self.getNewFeatureWithoutGeom(featureWithoutGeom, lyr)
                newFeat.setGeometry(geom)
                newFeatList.append(newFeat)
        return geomToUpdate, newFeatList, False
    
    def getFeatureOuterShellAndHoles(self, feat, isMulti):
        geom = feat.geometry()
        
        outershells, donutholes = self.geometryHandler.getOuterShellAndHoles(geom, isMulti)
        outershellList = []
        for shell in outershells:
            outerShellFeat = QgsFeature(feat)
            outerShellFeat.setGeometry(shell)
            outershellList.append(outerShellFeat)

        donutHoleList = []
        for hole in donutholes:
            newFeat = QgsFeature(feat)
            newFeat.setGeometry(hole)
            donutHoleList.append(newFeat)
        return outershellList, donutHoleList
    
    def mergeLineFeatures(self, featList, lyr, idsToRemove, networkDict, parameterDict = None, feedback = None, ignoreNetwork = False):
        parameterDict = {} if parameterDict is None else parameterDict
        changeDict = dict()
        size = 100 / len(featList)
        for current, feat_a in enumerate(featList):
            if feedback:
                if feedback.isCanceled():
                    break
            id_a = feat_a.id()
            if id_a in idsToRemove:
                continue
            for feat_b in featList:
                if feedback:
                    if feedback.isCanceled():
                        break
                id_b = feat_b.id()
                if id_a == id_b or id_b in idsToRemove:
                    continue
                geom_a = feat_a.geometry()
                geom_b = feat_b.geometry()
                if geom_a.touches(geom_b):
                    point = geom_a.intersection(geom_b).asPoint()
                    if ignoreNetwork or (point in networkDict and len(networkDict[point]) == 2):
                        newGeom = self.geometryHandler.handleGeometry(geom_a.combine(geom_b).mergeLines(), parameterDict)[0] #only one candidate is possible because features are touching
                        feat_a.setGeometry(newGeom)
                        idsToRemove.append(id_b)
                        changeDict[id_a] = newGeom
            if feedback:
                feedback.setProgress(size*current)
        for id, geom in changeDict.items():
            lyr.changeGeometry(id, geom)
    
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
    
    def getFirstNode(self, lyr, feat, geomType=None):
        """
        Returns the starting node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
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
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
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
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
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
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][-1]
        elif n:
            return n[-1]

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
        isMulti = QgsWKBTypes.isMultiType(int(networkLayer.wkbType()))
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
    