# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-04
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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
from itertools import combinations, chain
import math
from math import pi
from .geometryHandler import GeometryHandler
from .layerHandler import LayerHandler
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, \
                      QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, \
                      QgsFeature, QgsSpatialIndex, Qgis, QgsCoordinateTransform, \
                      QgsWkbTypes, QgsProject, QgsVertexId, Qgis, QgsCoordinateReferenceSystem,\
                      QgsDataSourceUri, QgsFields, QgsProcessingMultiStepFeedback
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import QVariant

class NetworkHandler(QObject):
    Flag, Sink, WaterwayBegin, UpHillNode, \
    DownHillNode, Confluence, Ramification, \
    AttributeChange, NodeNextToWaterBody, \
    AttributeChangeFlag, NodeOverload, DisconnectedLine, \
    DitchNode, SpillwayNode = list(range(14))
    def __init__(self):
        super(NetworkHandler, self).__init__()
        self.geometryHandler = GeometryHandler()
        self.layerHandler = LayerHandler()
        self.nodeDict = None
        self.nodeTypeDict = None
        self.nodeTypeNameDict = {
            NetworkHandler.Flag : self.tr("Flag"),#0
            NetworkHandler.Sink : self.tr("Sink"),#1
            NetworkHandler.WaterwayBegin : self.tr("Waterway Beginning"),#2
            NetworkHandler.UpHillNode : self.tr("Up Hill Node"),#3
            NetworkHandler.DownHillNode : self.tr("Down Hill Node"),#4
            NetworkHandler.Confluence : self.tr("Confluence"),#5
            NetworkHandler.Ramification : self.tr("Ramification"),#6
            NetworkHandler.AttributeChange : self.tr("Attribute Change Node"),#7
            NetworkHandler.NodeNextToWaterBody : self.tr("Node Next to Water Body"),#8
            NetworkHandler.AttributeChangeFlag : self.tr("Attribute Change Flag"),#9
            NetworkHandler.NodeOverload : self.tr("Overloaded Node"),#10
            NetworkHandler.DisconnectedLine : self.tr("Disconnected From Network"),#11
            NetworkHandler.DitchNode : self.tr("Node next to ditch"),#12
            NetworkHandler.SpillwayNode : self.tr("Spillway")
        }
        self.flagTextDict = {
            NetworkHandler.Flag : self.tr('Segments must be connected and with correct flow.'),
            NetworkHandler.AttributeChangeFlag : self.tr('Segments with same attribute set must be merged.'),
            NetworkHandler.DisconnectedLine : self.tr("Line disconnected From Network"),
            NetworkHandler.NodeOverload : self.tr("Node with flow problem")
        }
    
    def identifyAllNodes(self, networkLayer, onlySelected=False, feedback=None):
        """
        Identifies all nodes from a given layer (or selected features of it).
        The result is returned as a dict of dict.
        :param networkLayer: target layer to which nodes identification is required.
        :return: {
            node_id : {
                start : [feature_which_starts_with_node],
                end : feature_which_ends_with_node
                }
            }
        """
        nodeDict = dict()
        isMulti = QgsWkbTypes.isMultiType(int(networkLayer.wkbType()))
        iterator = networkLayer.getFeatures() if not onlySelected else networkLayer.getSelectedFeatures()
        featCount = networkLayer.featureCount() if not onlySelected else networkLayer.selectedFeatureCount()
        size = 100/featCount if featCount else 0
        for current, feat in enumerate(iterator):
            if feedback is not None and feedback.isCanceled():
                break
            nodes = self.geometryHandler.getFeatureNodes(networkLayer, feat)
            if nodes != []:
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
            if feedback is not None:
                feedback.setProgress(size * current)
        return nodeDict

    def changeLineDict(self, nodeList, line):
        """
        Changes a line from a dict to another (start/end). Useful when network lines are flipped and another node
        identification is too costy.
        :param nodeList: (list-of-QgsPoint) the list of nodes connected to have given line relation dictionary changed.
        :param line: (QgsFeature) line to be flipped.
        :return: whether changing was successful for each node 
        """
        for node in nodeList:
            # node's dicts
            startDict = self.nodeDict[node]['start']
            endDict = self.nodeDict[node]['end']
            if line in startDict:
                startDict.remove(line)
                endDict.append(line)
            elif line in endDict:
                startDict.append(line)
                endDict.remove(line)
            else:
                # if line is not found for some reason
                return False
        # if a nodeList is not found, method doesn't change anything
        return bool(nodeList)

    def nodeOnFrame(self, node, frameLyrContourList, searchRadius):
        """
        Identify whether or not node is over the frame. Returns True if point is over the frame and false if
        node is not on frame. If identification fails, returns 'None'.
        :param node: node (QgsPoint) to be identified as over the frame layer or not.
        :param frameLyrContourList: (list-of-QgsGeometry) border line for the frame layer to be checked.
        :param searchRadius: maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to frame contour.
        """
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        for frameContour in frameLyrContourList:
            if buf.intersects(frameContour):
                # it is condition enough one of the frame contours to be next to node
                return True
        return False

    def nodeNextToWaterBodies(self, node, waterBodiesLayers, searchRadius, auxIndexStructure=None):
        """
        Identify whether or not node is next to a water body feature.
        :param node: (QgsPoint) node to be identified as next to a water body feature.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of layers composing the water bodies on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """        
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
        # use aux spatial index if provided
        if auxIndexStructure is not None and 'waterBodiesLayers' in auxIndexStructure:
            for auxDict in auxIndexStructure['waterBodiesLayers']:
                for featid in auxDict['spatialIdx'].intersects(bbRect):
                    if buf.intersects(auxDict['idDict'][featid].geometry()):
                        # any feature component of a water body intersected is enough
                        return True
        else:
            for lyr in waterBodiesLayers:
                if lyr.geometryType() == 0:
                    # ignore point primitive layers
                    continue
                for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                    if buf.intersects(feat.geometry()):
                        # any feature component of a water body intersected is enough
                        return True
        return False

    def nodeIsWaterSink(self, node, waterSinkLayer, searchRadius, auxIndexStructure=None):
        """
        Identify whether or not node is next to a water body feature. If no water sink layer is given, method returns False
        :param node: (QgsPoint) node to be identified as coincident with a water sink feature.
        :param waterSinkLayer: (QgsVectorLayer) layer containing the water sinks on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """
        if not waterSinkLayer:
            return False
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building bounding box around node for feature requesting
        bbRect = qgisPoint.buffer(searchRadius, -1).boundingBox()
        if auxIndexStructure is not None and 'waterSinkLayer' in auxIndexStructure:
            for featid in auxIndexStructure['waterSinkLayer']['spatialIdx'].intersects(bbRect):
                if qgisPoint.distance(auxIndexStructure['waterSinkLayer']['idDict'][featid].geometry()) <= searchRadius:
                    # any feature component of a water body intersected is enough
                    return True
        else:
            # check if qgisPoint (node geometry) is over a sink classified point
            for feat in waterSinkLayer.getFeatures(QgsFeatureRequest(bbRect)):
                if qgisPoint.distance(feat.geometry()) <= searchRadius:
                    # any feature component of a water body intersected is enough
                    return True
        return False
    
    def nodeIsSpillway(self, node, spillwayLayer, searchRadius, auxIndexStructure=None):
        """
        Identify whether or not node is next to a water body feature. If no water sink layer is given, method returns False
        :param node: (QgsPoint) node to be identified as coincident with a water sink feature.
        :param waterSinkLayer: (QgsVectorLayer) layer containing the water sinks on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """
        if not spillwayLayer:
            return False
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building bounding box around node for feature requesting
        bbRect = qgisPoint.buffer(searchRadius, -1).boundingBox()
        if auxIndexStructure is not None and 'spillwayLayer' in auxIndexStructure:
            for featid in auxIndexStructure['spillwayLayer']['spatialIdx'].intersects(bbRect):
                if qgisPoint.distance(auxIndexStructure['spillwayLayer']['idDict'][featid].geometry()) <= searchRadius:
                    # any feature component of a water body intersected is enough
                    return True
        else:
            # check if qgisPoint (node geometry) is over a sink classified point
            for feat in spillwayLayer.getFeatures(QgsFeatureRequest(bbRect)):
                if qgisPoint.distance(feat.geometry()) <= searchRadius:
                    # any feature component of a water body intersected is enough
                    return True
        return False

    def checkIfHasLineInsideWaterBody(self, node, waterBodiesLayers, searchRadius=1.0):
        """
        Checks whether one of ending lines connected to given node is inside of a water body feature.
        :param node: (QgsPoint) node to be identified having an ending line inside of a water body.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of layers composing the water bodies on map.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
        # check if any wb feature inside of buffer area contains any ending line
        for line in self.nodeDict[node]['end']:
            for lyr in waterBodiesLayers:
                for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                    if feat.geometry().contains(line.geometry()):
                        # any feature component of a water body intersected is enough
                        return True
        return False

    def getAttributesFromFeature(self, feature, layer, fieldList=None):
        """
        Retrieves the attributes from a given feature, except for
        their geometry and ID column values. If a list of
        attributes is given, method will return those attributes
        if found. In case no attribute is found, None will be returned.
        :param feature: (QgsFeature) feature from which attibutes will be retrieved.
        :param layer: (QgsVectorLayer) layer containing target feature.
        :param fieldList: (list-of-str) list of field names to be exposed.
        :return: (dict-of-object) attribute values for each attribute mapped.
        """
        # fields to be ignored
        fieldList = [] if fieldList is None else fieldList
        return {field : feature[field] for field in fieldList}

    def attributeChangeCheck(self, node, networkLayer, fieldList=None):
        """
        Checks if attribute change node is in fact an attribute change.
        :param node: (QgsPoint) node to be identified as over the frame layer or not.
        :param networkLayer: (QgsVectorLayer) layer containing network lines.
        :return: (bool) if lines connected to node do change attributes.
        """
        # assuming that attribute change nodes have only 1-in 1-out lines
        lineIn = self.nodeDict[node]['end'][0]
        atrLineIn = self.getAttributesFromFeature(feature=lineIn, layer=networkLayer, fieldList=fieldList)
        lineOut = self.nodeDict[node]['start'][0]
        atrLineOut = self.getAttributesFromFeature(feature=lineOut, layer=networkLayer, fieldList=fieldList)
        # comparing their dictionary of attributes, it is decided whether they share the exact same set of attributes (fields and values)
        return atrLineIn != atrLineOut

    def isFirstOrderDangle(self, node, networkLayer, searchRadius, auxIndexStructure=None):
        """
        Checks whether node is a dangle into network (connected to a first order line).
        :param node: (QgsPoint) node to be validated.
        :param networkLayer: (QgsVectorLayer) network layer (line layer).
        :param searchRadius: (float) limit distance to another line.
        :return: (bool) indication whether node is a dangle.
        """
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
        if auxIndexStructure is not None and 'networkLayer' in auxIndexStructure:
            # check if buffer intersects features from water bodies layers
            count = 0
            for featid in auxIndexStructure['networkLayer']['spatialIdx'].intersects(bbRect):
                if buf.intersects(auxIndexStructure['networkLayer']['idDict'][featid].geometry()):
                    count += 1
                    res = (count > 1)
                    if res:
                        # to avoid as many iterations as possible
                        return False
        else:
            # check if buffer intersects features from water bodies layers
            count = 0
            for feat in networkLayer.getFeatures(QgsFeatureRequest(bbRect)):
                if buf.intersects(feat.geometry()):
                    count += 1
                    res = (count > 1)
                    if res:
                        # to avoid as many iterations as possible
                        return False
        return True

    def checkIfLineIsDisconnected(self, node, networkLayer, nodeTypeDict, geomType=None):
        """
        Checks whether a waterway beginning node connected to a line disconnected from network.
        :param node: (QgsPoint) point to be classified.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :param nodeTypeDict: (dict) all current classified nodes and theirs types.
        :param geomType: (int) network layer geometry type code.
        :return: (bool) whether node is connected to a disconnected line 
        """
        if not nodeTypeDict:
            # if there are no classified nodes, method is ineffective
            return False
        # if a line is disconnected from network, then the other end of the line would have to be classified as a waterway beginning as well
        if not geomType:
            geomType = networkLayer.geometryType()
        nextNodes = []
        # to reduce calculation time
        nodePointDict = self.nodeDict[node]
        isMulti = QgsWkbTypes.isMultiType(int(networkLayer.wkbType()))
        # get all other nodes connected to lines connected to "node"
        lines = nodePointDict['start'] + nodePointDict['end']
        if len(lines) > 1:
            # if there is at least one more line connected to node, line is not disconnected
            return False
        # get line nodes
        n = self.geometryHandler.getFeatureNodes(layer=networkLayer, feature=lines[0], geomType=geomType)
        if nodePointDict['start']:            
            # if line starts at target node, the other extremity is a final node
            if isMulti:
                if n is not None:
                    n = n[0][-1]
            elif n is not None:
                n = n[-1]
        elif nodePointDict['end']:
            # if line starts at target node, the other extremity is a initial node
            if isMulti:
                if n is not None:
                    n = n[0][0]
            elif n:
                n = n[0]
        # if next node is not among the valid ending lines, it may still be connected to a disconnected line if it is a dangle
        # validEnds = [NetworkHandler.Sink, NetworkHandler.DownHillNode, NetworkHandler.NodeNextToWaterBody]
        if n in nodeTypeDict:
            # if both ends are classified as waterway beginning, then both ends are 1st order dangles and line is disconnected.
            return nodeTypeDict[n] in [NetworkHandler.WaterwayBegin, NetworkHandler.DownHillNode, NetworkHandler.UpHillNode, NetworkHandler.NodeNextToWaterBody]
            # if nodeTypeDict[n] not in validEnds:
            #     if self.isFirstOrderDangle(node=n, networkLayer=networkLayer, searchRadius=self.parameters[self.tr('Search Radius')]):
            #         # if next node is not a valid network ending node and is a dangle, line is disconnected from network 
            #         return False
            #     return True
        # in case next node is not yet classified, method is ineffective
        return False
    
    def isNodeNextToDitch(self, node, ditchLayer, searchRadius, auxIndexStructure=None):
        """
        Checks if node is next to a ditch.
        ::param node: (QgsPoint) node to be identified as next to a water ditch feature.
        :param ditchLayer: layer composing the ditches on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """
        if not ditchLayer:
            return False
        qgisPoint = QgsGeometry.fromPointXY(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
        if auxIndexStructure is not None and 'ditchLayer' in auxIndexStructure:
            for featid in auxIndexStructure['ditchLayer']['spatialIdx'].intersects(bbRect):
                if buf.intersects(auxIndexStructure['ditchLayer']['idDict'][featid].geometry()):
                    # any feature component of a water body intersected is enough
                    return True
        else:
            # check if buffer intersects features from water bodies layers
            for feat in ditchLayer.getFeatures(QgsFeatureRequest(bbRect)):
                if buf.intersects(feat.geometry()):
                    # any feature component of a water body intersected is enough
                    return True
        return False

    def nodeType(self, nodePoint, networkLayer, frameLyrContourList, waterBodiesLayers, searchRadius, nodeTypeDict, waterSinkLayer=None, spillwayLayer=None, networkLayerGeomType=None, fieldList=None, ditchLayer=None, auxIndexStructure={}):
        """
        Get the node type given all lines that flows from/to it.
        :param nodePoint: (QgsPoint) point to be classified.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :param frameLyrContourList: (list-of-QgsGeometry) border line for the frame layer to be checked.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of all waterbodies layer.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :param nodeTypeDict: (dict) dict with all currently classified nodes and their types.
        :param waterSinkLayer: (QgsVectorLayer) water sink layer.
        :param networkLayerGeomType: (int) network layer geometry type code.
        :return: returns the (int) point type.
        """
        fieldList = [] if fieldList is None else fieldList
        # to reduce calculation time in expense of memory, which is cheap
        nodePointDict = self.nodeDict[nodePoint]
        sizeFlowOut = len(nodePointDict['start'])
        sizeFlowIn = len(nodePointDict['end'])
        hasStartLine = bool(sizeFlowOut)
        hasEndLine = bool(sizeFlowIn)
        if not networkLayerGeomType:
            networkLayerGeomType = networkLayer.geometryType()
        # "exclusive or"
        startXORendLine = (hasStartLine != hasEndLine)
        # # case 5: more than 3 lines flowing through one network line (it is forbidden as of Brazilian mapping norm EDGV)
        # if sizeFlowIn + sizeFlowOut > 3:
        #     return NetworkHandler.NodeOverload
        # case 1: all lines either flow in or out 
        if startXORendLine:
            # case 1.a: point is over the frame
            if self.nodeOnFrame(node=nodePoint, frameLyrContourList=frameLyrContourList, searchRadius=searchRadius):
                # case 1.a.i: waterway is flowing away from mapped area (point over the frame has one line ending line)
                if hasEndLine:
                    return NetworkHandler.DownHillNode
                # case 1.a.ii: waterway is flowing to mapped area (point over the frame has one line starting line)
                elif hasStartLine:
                    return NetworkHandler.UpHillNode
            # case 1.b: point that legitimately only flows from
            elif hasEndLine:
                # case 1.b.i
                if self.nodeNextToWaterBodies(node=nodePoint, waterBodiesLayers=waterBodiesLayers, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                    # it is considered that every free node on map is a starting node. The only valid exceptions are nodes that are
                    # next to water bodies and water sink holes.
                    if sizeFlowIn == 1:
                        # a node next to water has to be a lose end
                        return NetworkHandler.NodeNextToWaterBody
                # force all lose ends to be waterway beginnings if they're not dangles (which are flags)
                elif self.isFirstOrderDangle(node=nodePoint, networkLayer=networkLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                    if self.isNodeNextToDitch(node=nodePoint, ditchLayer=ditchLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                        # if point is not disconnected and is connected to a ditch
                        return NetworkHandler.DitchNode
                    # check if node is connected to a disconnected line
                    elif self.checkIfLineIsDisconnected(node=nodePoint, networkLayer=networkLayer, nodeTypeDict=nodeTypeDict, geomType=networkLayerGeomType):
                        return NetworkHandler.DisconnectedLine
                    # case 1.b.ii: node is in fact a water sink and should be able to take an 'in' flow
                    elif self.nodeIsWaterSink(node=nodePoint, waterSinkLayer=waterSinkLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                        # if a node is indeed a water sink (operator has set it to a sink)
                        return NetworkHandler.Sink
                    elif self.nodeIsSpillway(node=nodePoint, spillwayLayer=spillwayLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                        # if node is a spillway
                        return NetworkHandler.SpillwayNode
                    return NetworkHandler.WaterwayBegin
            # case 1.c: point that legitimately only flows out
            elif hasStartLine and self.isFirstOrderDangle(node=nodePoint, networkLayer=networkLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                if self.isNodeNextToDitch(node=nodePoint, ditchLayer=ditchLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                    # if point is not disconnected and is connected to a ditch
                    return NetworkHandler.DitchNode
                elif self.checkIfLineIsDisconnected(node=nodePoint, networkLayer=networkLayer, nodeTypeDict=nodeTypeDict, geomType=networkLayerGeomType):
                    return NetworkHandler.DisconnectedLine
                elif self.nodeIsWaterSink(node=nodePoint, waterSinkLayer=waterSinkLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                    # in case there's a wrongly acquired line connected to a water sink
                    return NetworkHandler.Sink
                elif self.nodeIsSpillway(node=nodePoint, spillwayLayer=spillwayLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                        # if node is a spillway
                        return NetworkHandler.SpillwayNode
                return NetworkHandler.WaterwayBegin
            # case 1.d: points that are not supposed to have one way flow (flags)
            return NetworkHandler.Flag
        elif sizeFlowIn > sizeFlowOut:
            # case 2 "confluence"
            return NetworkHandler.Confluence
        elif sizeFlowIn == sizeFlowOut:
            if sizeFlowIn > 1:
                # case 4.a: there's a constant flow through node, but there are more than 1 line
                return NetworkHandler.NodeOverload
            elif self.attributeChangeCheck(node=nodePoint, networkLayer=networkLayer, fieldList=fieldList):
                # case 4.b: lines do change their attribute set. Must use fieldList due to black list items.
                return NetworkHandler.AttributeChange
            elif self.isNodeNextToDitch(node=nodePoint, ditchLayer=ditchLayer, searchRadius=searchRadius, auxIndexStructure=auxIndexStructure):
                # case 4.c: lines next to ditches.
                return NetworkHandler.DitchNode
            else:
                # case 4.d: nodes inside the network that are there as an attribute change node but lines connected
                #           to it have the same set of attributes
                return NetworkHandler.AttributeChangeFlag
        else:
            # case 3 "ramification"
            return NetworkHandler.Ramification

    def classifyAllNodes(self, networkLayer, frameLyrContourList, waterBodiesLayers, searchRadius, waterSinkLayer=None, spillwayLayer=None, nodeList=None, feedback=None, attributeBlackList=None, ignoreVirtualFields=True, excludePrimaryKeys=True, ditchLayer=None):
        """
        Classifies all identified nodes from the hidrography line layer.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :param frameLyrContourList: (list-of-QgsFeature) border line for the frame layer.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of all classes with water bodies to be compared to.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :param nodeList: a list of nodes (QgsPoint) to be classified. If not given, whole dict is going 
                         to be classified. Node MUST be in dict given, if not, it'll be ignored.
        :param waterSinkLayer: (QgsVectorLayer) water sink layer.
        :param ditchLayer: (QgsVectorLayer) ditch layer.
        :return: a (dict) dictionary of node and its node type ( { (QgsPoint)node : (int)nodeType } ). 
        """
        networkLayerGeomType = networkLayer.geometryType()
        nodeTypeDict = dict()
        flagNodeDict = dict()
        fieldList = self.layerHandler.getAttributesFromBlackList(networkLayer, \
                                                            attributeBlackList=attributeBlackList,\
                                                            ignoreVirtualFields=ignoreVirtualFields,\
                                                            excludePrimaryKeys=excludePrimaryKeys)
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
            multiStepFeedback.setCurrentStep(0)
        auxIndexStructure = self.getAuxIndexStructure(
            networkLayer,
            waterBodiesLayers=waterBodiesLayers,
            spillwayLayer=spillwayLayer,
            waterSinkLayer=waterSinkLayer,
            ditchLayer=ditchLayer,
            feedback=multiStepFeedback)
        nodeCount = len(self.nodeDict)
        size = 100/nodeCount if nodeCount else 0
        if feedback is not None:
            multiStepFeedback.setCurrentStep(1)
        for current, node in enumerate(self.nodeDict):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            if node not in self.nodeDict:
                # in case user decides to use a list of nodes to work on, given nodes that are not identified will be ignored
                continue
            nodeClassification = self.nodeType(
                nodePoint=node,
                networkLayer=networkLayer,
                frameLyrContourList=frameLyrContourList,
                waterBodiesLayers=waterBodiesLayers,
                spillwayLayer=spillwayLayer,
                searchRadius=searchRadius,
                waterSinkLayer=waterSinkLayer,
                nodeTypeDict=nodeTypeDict,
                networkLayerGeomType=networkLayerGeomType,
                fieldList=fieldList,
                ditchLayer=ditchLayer,
                auxIndexStructure=auxIndexStructure
                )
            nodeTypeDict[node] = nodeClassification
            if nodeClassification in self.flagTextDict:
                flagNodeDict[node] = self.flagTextDict[nodeClassification]
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(size * current)
        return nodeTypeDict, flagNodeDict
    
    def getAuxIndexStructure(self, networkLayer, waterBodiesLayers=None, waterSinkLayer=None, spillwayLayer=None, ditchLayer=None, feedback=None):
        auxStructDict = dict()
        steps = 1
        if waterBodiesLayers is not None:
            steps += len(waterBodiesLayers)
        if waterSinkLayer is not None:
            steps += 1
        if ditchLayer is not None:
            steps += 1
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currStep = 0
        multiStepFeedback.setCurrentStep(currStep)
        spatialIdx, idDict = self.layerHandler.buildSpatialIndexAndIdDict(networkLayer, feedback=multiStepFeedback)
        auxStructDict['networkLayer']={'spatialIdx':spatialIdx, 'idDict':idDict}
        currStep += 1
        if waterBodiesLayers is not None:
            auxStructDict['waterBodies'] = []
            multiStepFeedback.setCurrentStep(currStep)
            for lyr in waterBodiesLayers:
                spatialIdx, idDict = self.layerHandler.buildSpatialIndexAndIdDict(lyr, feedback=multiStepFeedback)
                auxStructDict['waterBodies'].append({'spatialIdx':spatialIdx, 'idDict':idDict})
            currStep += 1
        if waterSinkLayer is not None:
            multiStepFeedback.setCurrentStep(currStep)
            spatialIdx, idDict = self.layerHandler.buildSpatialIndexAndIdDict(waterSinkLayer, feedback=multiStepFeedback)
            auxStructDict['waterSinkLayer'] = {'spatialIdx':spatialIdx, 'idDict':idDict}
            currStep += 1
        if spillwayLayer is not None:
            multiStepFeedback.setCurrentStep(currStep)
            spatialIdx, idDict = self.layerHandler.buildSpatialIndexAndIdDict(spillwayLayer, feedback=multiStepFeedback)
            auxStructDict['spillwayLayer'] = {'spatialIdx':spatialIdx, 'idDict':idDict}
            currStep += 1
        if ditchLayer is not None:
            multiStepFeedback.setCurrentStep(currStep)
            spatialIdx, idDict = self.layerHandler.buildSpatialIndexAndIdDict(ditchLayer, feedback=multiStepFeedback)
            auxStructDict['ditchLayer'] = {'spatialIdx':spatialIdx, 'idDict':idDict}
            currStep += 1
        return auxStructDict

    def clearHidNodeLayer(self, nodeLayer, nodeIdList=None, commitToLayer=False):
        """
        Clears all (or a given list of points) hidrography nodes on layer.
        :param nodeLayer: (QgsVectorLayer) hidrography nodes layer.
        :param nodeIdList: (list-of-int) list of node IDs to be cleared from layer.
        :param commitToLayer: (bool) indicates whether changes should be commited to layer.
        """
        nodeLayer.beginEditCommand('Clear Nodes')
        if not nodeIdList:
            nodeIdList = [feat.id() for feat in nodeLayer.getFeatures()]
        nodeLayer.deleteFeatures(nodeIdList)
        nodeLayer.endEditCommand()
        # commit changes to LAYER
        if commitToLayer:
            nodeLayer.commitChanges()

    def fillNodeLayer(self, nodeLayer, networkLineLayerName, commitToLayer=False):
        """
        Populate hidrography node layer with all nodes.
        :param nodeLayer: (QgsVectorLayer) hidrography nodes layer.
        :param networkLineLayerName: (str) network line layer name.
        :param commitToLayer: (bool) indicates whether changes should be commited to layer.
        """
        # if table is going to be filled, then it needs to be cleared first
        self.clearHidNodeLayer(nodeLayer=nodeLayer, commitToLayer=commitToLayer)
        # get fields from layer in order to create new feature with the same attribute map
        fields = nodeLayer.fields()
        nodeLayer.beginEditCommand('Create Nodes')
        # to avoid unnecessary calculation inside loop
        nodeTypeKeys = self.nodeTypeDict.keys()
        # initiate new features list
        featList = []
        for node in self.nodeDict:
            # set attribute map
            feat = QgsFeature(fields)
            # set geometry
            feat.setGeometry(QgsGeometry.fromMultiPointXY([node]))
            feat['node_type'] = self.nodeTypeDict[node] if node in nodeTypeKeys else None
            feat['layer'] = networkLineLayerName
            featList.append(feat)
        nodeLayer.addFeatures(featList)
        nodeLayer.endEditCommand()
        if commitToLayer:
            nodeLayer.commitChanges()

    def getFirstNode(self, lyr, feat, geomType=None):
        """
        Returns the starting node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.geometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][0]
        elif n is not None:
            return n[0]

    def getSecondNode(self, lyr, feat, geomType=None):
        """
        Returns the second node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.geometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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
        n = self.geometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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
        n = self.geometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWkbTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][-1]
        elif n is not None:
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

    def checkNodeTypeValidity(self, node, connectedValidLines, networkLayer, geomType=None):
        """
        Checks if lines connected to a node have their flows compatible to node type and valid lines
        connected to it.
        :param node: (QgsPoint) node which lines connected to it are going to be verified.
        :param connectedValidLines: list of (QgsFeature) lines connected to 'node' that are already verified.
        :param networkLayer: (QgsVectorLayer) layer that contains the lines of analyzed network.
        :param geomType: (int) layer geometry type. If not given, it'll be evaluated OTF.
        :return: (list-of-obj [dict, dict, str]) returns the dict. of valid lines, dict of inval. lines and
                 invalidation reason, if any, respectively.
        """
        # getting flow permitions based on node type
        # reference is the node (e.g. 'in' = lines  are ENDING at analyzed node)
        flowType = {
                    NetworkHandler.Flag : None, # 0 - Flag (fim de trecho sem 'justificativa espacial')
                    NetworkHandler.Sink : 'in', # 1 - Sumidouro
                    NetworkHandler.WaterwayBegin : 'out', # 2 - Fonte D'Água
                    NetworkHandler.DownHillNode : 'in', # 3 - Interrupção à Jusante
                    NetworkHandler.UpHillNode : 'out', # 4 - Interrupção à Montante
                    NetworkHandler.Confluence : 'in and out', # 5 - Confluência
                    NetworkHandler.Ramification : 'in and out', # 6 - Ramificação
                    NetworkHandler.AttributeChange : 'in and out', # 7 - Mudança de Atributo
                    NetworkHandler.NodeNextToWaterBody : 'in or out', # 8 - Nó próximo a corpo d'água
                    NetworkHandler.AttributeChangeFlag : None, # 9 - Nó de mudança de atributos conectado em linhas que não mudam de atributos
                    NetworkHandler.NodeOverload : None, # 10 - Há igual número de linhas (>1 para cada fluxo) entrando e saindo do nó
                    NetworkHandler.DisconnectedLine : None, # 11 - Nó conectado a uma linha perdida na rede (teria dois inícios de rede)
                    NetworkHandler.DitchNode : 'in and out', # 12 - Nó de vala 
                    NetworkHandler.SpillwayNode : 'out' # 13 - Vertedouro
                   }
        # to avoid calculations in expense of memory
        nodeType = self.nodeTypeDict[node]
        # if node is introduced by operator's modification, it won't be saved to the layer
        if node not in self.nodeTypeDict.keys() and not self.unclassifiedNodes:
            self.unclassifiedNodes = True
            QMessageBox.warning(self.iface.mainWindow(), self.tr('Error!'), self.tr('There are unclassified nodes! Node (re)creation process is recommended before this process.'))
            return None, None, None
        flow = flowType[int(nodeType)]
        nodePointDict = self.nodeDict[node]
        # getting all connected lines to node that are not already validated
        linesNotValidated = set( nodePointDict['start']  + nodePointDict['end'] ) - set(connectedValidLines)
        # starting dicts of valid and invalid lines
        validLines, invalidLines = dict(), dict()
        if not flow:
            # flags have all lines flagged
            if nodeType == NetworkHandler.Flag:
                reason = self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
                invalidLines = { line.id() : line for line in linesNotValidated }
            elif nodeType == NetworkHandler.AttributeChangeFlag:
                if nodePointDict['start'] and nodePointDict['end']:
                    # in case manual error is inserted, this would raise an exception
                    line1, line2 = nodePointDict['start'][0], nodePointDict['end'][0]
                    id1, id2 = line1.id(), line2.id()
                    reason = self.tr('Redundant node. Connected lines ({0}, {1}) share the same set of attributes.').format(id1, id2)
                    if line1 in linesNotValidated:
                        il = line1
                    else:
                        il = line2
                    invalidLines[il.id()] = il
                else:
                    # problem is then, reclassified as a flag
                    self.nodeTypeDict[node] = NetworkHandler.Flag
                    # reclassify node type into layer
                    self.reclassifyNodeType[node] = NetworkHandler.Flag
                    reason = self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
            elif nodeType == NetworkHandler.DisconnectedLine:
                # get line connected to node
                lines = nodePointDict['start'] + nodePointDict['end']
                # just in case there's a node wrong manual reclassification so code doesn't raise an error
                ids = [str(line.id()) for line in lines]
                invalidLines = { line.id() : line for line in lines }
                reason = self.tr('Line {0} disconnected from network.').format(", ".join(ids))
            elif nodeType == NetworkHandler.NodeOverload:
                reason = self.tr('Node is overloaded - 4 or more lines are flowing in (>= 2 lines) and out (>= 2 lines).')
                invalidLines = { line.id() : line for line in linesNotValidated }
            return validLines, invalidLines, reason
        if not linesNotValidated:
            # if there are no lines to be validated, method returns None
            return validLines, invalidLines, ''
        # if 'geomType' is not given, it must be evaluated
        if not geomType:
            geomType = networkLayer.geometryType()
        # reason message in case of invalidity
        reason = ''
        for line in linesNotValidated:
            # getting last and initial node from analyzed line
            finalNode = self.getLastNode(lyr=networkLayer, feat=line, geomType=geomType)
            initialNode = self.getFirstNode(lyr=networkLayer, feat=line, geomType=geomType)
            # line ID
            lineID = line.id()
            # comparing extreme nodes to find out if flow is compatible to node type
            if flow == 'in':
                if node == finalNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                    invalidLines[lineID] = line
                    reason = "".join([reason, self.tr('Line id={0} does not end at a node with IN flow type (node type is {1}). ').format(lineID, nodeType)])
            elif flow == 'out':
                if node == initialNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                    invalidLines[lineID] = line
                    reason = "".join([reason, self.tr('Line id={0} does not start at a node with OUT flow type (node type is {1}). ')\
                    .format(lineID, self.nodeTypeNameDict[nodeType])])
            elif flow == 'in and out':
                if bool(len(nodePointDict['start'])) != bool(len(nodePointDict['end'])):
                    # if it's an 'in and out' flow and only one of dicts is filled, then there's an inconsistency
                    invalidLines[lineID] = line
                    thisReason = self.tr('Lines are either flowing only in or out of node. Node classification is {0}.')\
                    .format(self.nodeTypeNameDict[nodeType])
                    if thisReason not in reason:
                        reason = "".join([reason, thisReason])
                elif node in [initialNode, finalNode]:
                    if lineID not in validLines:
                        validLines[lineID] = line
                elif lineID not in invalidLines:
                    invalidLines[lineID] = line
                    reason = "".join([reason, self.tr('Line {0} seems to be invalid (unable to point specific reason).').format(lineID)])
            elif flow == 'in or out':
                # these nodes can either be a waterway beginning or end
                # No invalidation reasons were thought at this point...
                if lineID not in validLines:
                    validLines[lineID] = line
        return  validLines, invalidLines, reason

    def checkNodeValidity(self, node, connectedValidLines, networkLayer, geomType=None, deltaLinesCheckList=None):
        """
        Checks whether a node is valid or not.
        :param node: (QgsPoint) node which lines connected to it are going to be verified.
        :param connectedValidLines: list of (QgsFeature) lines connected to 'node' that are already verified.
        :param networkLayer: (QgsVectorLayer) layer that contains the lines of analyzed network.
        :param geomType: (int) layer geometry type. If not given, it'll be evaluated OTF.
        :param deltaLinesCheckList: (list-of-int) node types that must be checked for their connected lines angles.
        :return: (str) if node is invalid, returns the invalidation reason string.
        """
        
        if not deltaLinesCheckList:
            deltaLinesCheckList = [NetworkHandler.Confluence, NetworkHandler.Ramification] # nodes that have an unbalaced number ratio of flow in/out
        # check coherence to node type and waterway flow
        val, inval, reason = self.checkNodeTypeValidity(node=node, connectedValidLines=connectedValidLines,\
                                                    networkLayer=networkLayer, geomType=geomType)
        # checking angle validity
        if self.nodeTypeDict[node] in deltaLinesCheckList:
            # check for connected lines angles coherence
            val2, inval2, reason2 = self.validateDeltaLinesAngV2(node=node, networkLayer=networkLayer, connectedValidLines=connectedValidLines, geomType=geomType)
            # if any invalid line was validated on because of node type, it shall be moved to invalid dict
            if reason2:
                # updates reason
                if reason:
                    reason = "; ".join([reason, reason2])
                else:
                    reason  = reason2
                # remove any validated line in this iteration
                for lineId in inval2:
                    val.pop(lineId, None)
                # insert into invalidated dict
                inval.update(inval2)
        return val, inval, reason

    def getNextNodes(self, node, networkLayer, geomType=None):
        """
        It returns a list of all other nodes for each line connected to target node.
        :param node: (QgsPoint) node based on which next nodes will be gathered from. 
        :param networkLayer: (QgsVectorLayer) hidrography line layer.
        :return: (list-of-QgsPoint) a list of the other node of lines connected to given hidrography node.
        """
        if not geomType:
            geomType = networkLayer.geometryType()
        nextNodes = []
        nodePointDict = self.nodeDict[node]
        for line in nodePointDict['start']:
            # if line starts at target node, the other extremity is a final node
            nextNodes.append(self.getLastNode(lyr=networkLayer, feat=line, geomType=geomType))
        for line in nodePointDict['end']:
            # if line ends at target node, the other extremity is a initial node
            nextNodes.append(self.getFirstNode(lyr=networkLayer, feat=line, geomType=geomType))
        return nextNodes

    def checkForStartConditions(self, node, validLines, networkLayer, nodeLayer, geomType=None):
        """
        Checks if any of next nodes is a contour condition to directioning process.
        :param node: (QgsPoint) node which needs to have its next nodes checked.
        :param validLines: (list-of-QgsFeature) lines that were alredy checked and validated.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :param nodeLayer: (QgsVectorLayer) network nodes layer.
        :param geomType: (int) network lines layer geometry type code.
        :return:
        """
        # node type granted as right as start conditions
        inContourConditionTypes = [NetworkHandler.DownHillNode, NetworkHandler.Sink]
        outContourConditionTypes = [NetworkHandler.UpHillNode, NetworkHandler.WaterwayBegin, NetworkHandler.SpillwayNode]
        if node in inContourConditionTypes + outContourConditionTypes:
            # if node IS a starting condition, method is not necessary
            return False, ''
        nodes = self.getNextNodes(node=node, networkLayer=networkLayer, geomType=geomType)
        # for faster calculation
        nodeTypeDictAlias = self.nodeTypeDict
        nodeDictAlias = self.nodeDict
        # list of flipped features, if any
        flippedLines, flippedLinesIds = [], []
        # dict indicating whether lines may be flipped or not
        nonFlippableDict, flippableDict = dict(), dict()
        # at first, we assume there are no start conditions on next nodes
        hasStartCondition = False
        for nn in nodes:
            # initiate/clear line variable
            line = None
            if nn in nodeTypeDictAlias:
                nodeType = nodeTypeDictAlias[nn]
            else:
                nodeType = self.classifyNode([nn, nodeTypeDictAlias])
                nodeTypeDictAlias[nn] = nodeType
                self.reclassifyNodeType[nn] = nodeType
            if nodeType in inContourConditionTypes:
                # if next node is a confirmed IN-flowing lines, no lines should start on it
                line = nodeDictAlias[nn]['start'][0] if nodeDictAlias[nn]['start'] else None
                hasStartCondition = True
            elif nodeType in outContourConditionTypes:
                # if next node is a confirmed OUT-flowing lines, no lines should end on it
                line = nodeDictAlias[nn]['end'][0] if nodeDictAlias[nn]['end'] else None
                hasStartCondition = True
            if line:
                # if line is given, then flipping it is necessary
                self.flipSingleLine(line=line, layer=networkLayer, geomType=geomType)
                # if a line is flipped it must be changed in self.nodeDict
                self.updateNodeDict(node=node, line=line, networkLayer=networkLayer, geomType=geomType)
                flippedLines.append(line)
                flippedLinesIds.append(str(line.id()))
                # validLines.append(line)
        # for speed-up
        initialNode = lambda x : self.getFirstNode(lyr=networkLayer, feat=x, geomType=geomType)
        lastNode = lambda x : self.getLastNode(lyr=networkLayer, feat=x, geomType=geomType)
        if flippedLines:
            # map is a for-loop in C
            reclassifyNodeAlias = lambda x : nodeLayer.changeAttributeValue(self.nodeIdDict[x], 2, int(self.reclassifyNodeType[x])) \
                                                if self.reclassifyNode(node=x, nodeLayer=nodeLayer) \
                                                else False
            map(reclassifyNodeAlias, chain(map(initialNode, flippedLines), map(lastNode, flippedLines)))
        return hasStartCondition, flippedLinesIds

    def directNetwork(self, networkLayer, nodeLayer, nodeList=None):
        """
        For every node over the frame [or set as a line beginning], checks for network coherence regarding
        to previous node classification and its current direction. Method considers bordering points as 
        correctly classified.
        :param networkLayer: (QgsVectorLayer) hidrography lines layer from which node are created from.
        :param nodeList: a list of target node points (QgsPoint). If not given, all nodeDict will be read.
        :return: (dict) flag dictionary ( { (QgsPoint) node : (str) reason } ), (dict) dictionaries ( { (int)feat_id : (QgsFeature)feat } ) of invalid and valid lines.
        """
        startingNodeTypes = [NetworkHandler.UpHillNode, NetworkHandler.WaterwayBegin, NetworkHandler.SpillwayNode] # node types that are over the frame contour and line BEGINNINGS
        deltaLinesCheckList = [NetworkHandler.Confluence, NetworkHandler.Ramification] # nodes that have an unbalaced number ratio of flow in/out
        if not nodeList:
            # 'nodeList' must start with all nodes that are on the frame (assumed to be well directed)
            nodeList = [node for node, nodeType in self.nodeTypeDict.items() if nodeType in startingNodeTypes]
            # if no node to start the process is found, process ends here
            if not nodeList:
                return None, None, self.tr("No network starting point was found")
        # to avoid unnecessary calculations
        geomType = networkLayer.geometryType()
        # initiating the list of nodes already checked and the list of nodes to be checked next iteration
        visitedNodes, newNextNodes = [], []
        nodeFlags = dict()
        # starting dict of (in)valid lines to be returned by the end of method
        validLines, invalidLines = dict(), dict()
        # initiate relation of modified features
        flippedLinesIds, mergedLinesString = set([]), ""
        while nodeList:
            for node in nodeList:
                # first thing to be done: check if there are more than one non-validated line (hence, enough information for a decision)
                if node in self.nodeDict:
                    startLines = self.nodeDict[node]['start']
                    endLines = self.nodeDict[node]['end']
                    if node not in self.nodeTypeDict:
                        # in case node is not classified
                        self.nodeTypeDict[node] = self.classifyNode([node, nodeLayer])
                        self.reclassifyNodeType[node] = self.nodeTypeDict[node]
                else:
                    # ignore node for possible next iterations by adding it to visited nodes
                    visitedNodes.append(node)
                    continue
                nodeLines = startLines + endLines
                validLinesList = validLines.values()
                if len(set(nodeLines) - set(validLinesList)) > 1:
                    hasStartCondition, flippedLines = self.checkForStartConditions(node=node, validLines=validLinesList, networkLayer=networkLayer, nodeLayer=nodeLayer, geomType=geomType)
                    if hasStartCondition:
                        flippedLinesIds |= set(flippedLines)
                    else:
                        # if it is not connected to a start condition, check if node has a valid line connected to it
                        if (set(nodeLines) & set(validLinesList)):
                            # if it does and, check if it is a valid node
                            val, inval, reason = self.checkNodeValidity(node=node, connectedValidLines=validLinesList,\
                                                                        networkLayer=networkLayer, deltaLinesCheckList=deltaLinesCheckList, geomType=geomType)
                            # if node has a valid line connected to it and it is valid, then non-validated lines are proven to be in conformity to
                            # start conditions, then they should be validated and node should be set as visited
                            if reason:
                            # if there are more than 1 line not validated yet and no start conditions around it, 
                            # node will neither be checked nor marked as visited
                                continue
                # check coherence to node type and waterway flow
                val, inval, reason = self.checkNodeValidity(node=node, connectedValidLines=validLinesList,\
                                                            networkLayer=networkLayer, deltaLinesCheckList=deltaLinesCheckList, geomType=geomType)
                # nodes to be removed from next nodes
                removeNode = []
                # if a reason is given, then node is invalid (even if there are no invalid lines connected to it).
                if reason:
                    # try to fix node issues
                    # note that val, inval and reason MAY BE MODIFIED - and there is no problem...
                    flippedLinesIds_, mergedLinesString_ = self.fixNodeFlagsNew(node=node, valDict=val, invalidDict=inval, reason=reason, \
                                                                            connectedValidLines=validLinesList, networkLayer=networkLayer, \
                                                                            nodeLayer=nodeLayer, geomType=geomType, deltaLinesCheckList=deltaLinesCheckList)
                    # keep track of all modifications made
                    if flippedLinesIds_:
                        # IDs not registered yet will be added to final list
                        addIds = set(flippedLinesIds_) - set(flippedLinesIds)
                        # IDs that are registered will be removed (flipping a flipped line returns to original state)
                        removeIds = set(flippedLinesIds_) - addIds
                        flippedLinesIds = (set(flippedLinesIds) - removeIds) | addIds
                    if mergedLinesString_:
                        if not mergedLinesString:
                            mergedLinesString = mergedLinesString_
                        else:
                            ", ".join([mergedLinesString,  mergedLinesString_])
                    # if node is still invalid, add to nodeFlagList and add/update its reason
                    if reason:
                        nodeFlags[node] = reason
                    # get next nodes connected to invalid lines
                    for line in inval.values():
                        if line in endLines:
                            removeNode.append(self.getFirstNode(lyr=networkLayer, feat=line))
                        else:
                            removeNode.append(self.getLastNode(lyr=networkLayer, feat=line))
                # set node as visited
                if node not in visitedNodes:
                    visitedNodes.append(node)
                # update general dictionaries with final values
                validLines.update(val)
                invalidLines.update(inval)
                # get next iteration nodes
                newNextNodes += self.getNextNodes(node=node, networkLayer=networkLayer, geomType=geomType)
                # remove next nodes connected to invalid lines
                if removeNode:
                    newNextNodes = list( set(newNextNodes) - set(removeNode) )
            # remove nodes that were already visited
            newNextNodes = list( set(newNextNodes) - set(visitedNodes) )
            # if new nodes are detected, repeat for those
            nodeList = newNextNodes
            newNextNodes = []
        # log all features that were merged and/or flipped
        self.logAlteredFeatures(flippedLines=flippedLinesIds, mergedLinesString=mergedLinesString)
        return nodeFlags, invalidLines, validLines

    # method for automatic fix
    def getReasonType(self, reason):
        """
        Gets the type of reason. 0 indicates non-fixable reason.
        :param reason: (str) reason of node invalidation.
        :return: (int) reason type.
        """
        fixableReasonExcertsDict = {
                                    self.tr("does not end at a node with IN flow type") : 1,
                                    self.tr("does not start at a node with OUT flow type") : 2,
                                    self.tr("have conflicting directions") : 3,
                                    self.tr('Redundant node.') : 4,
                                    self.tr('Node was flagged upon classification') : 5
                                   }
        for r in fixableReasonExcertsDict:
            if r in reason:
                return fixableReasonExcertsDict[r]
        # if reason is not one of the fixables
        return 0

    # method for automatic fix
    def getLineIdFromReason(self, reason, reasonType):
        """
        Extracts line ID from given reason.
        :param reason: (str) reason of node invalidation.
        :param reasonType: (int) invalidation reason type.
        :return: (list-of-str) line ID (int as str).
        """
        if reasonType in [1, 2]:
            # Lines before being built:
            # self.tr('Line id={0} does not end at a node with IN flow type (node type is {1}). ')
            # self.tr('Line id={0} does not start at a node with OUT flow type (node type is {1}). ')
            return [reason.split(self.tr("id="))[1].split(" ")[0]]
        elif reasonType == 3:
            # Line before being built: self.tr('Lines id={0} and id={1} have conflicting directions ({2:.2f} deg).')
            lineId1 = reason.split(self.tr("id="))[1].split(" ")[0]
            lineId2 = reason.split(self.tr("id="))[2].split(" ")[0]
            return [lineId1, lineId2]
        elif reasonType == 4:
            # Line before being built: self.tr('Redundant node. Connected lines ({0}, {1}) share the same set of attributes.')
            lineId1 = reason.split(self.tr(", "))[0].split("(")[1]
            lineId2 = reason.split(self.tr(", "))[1].split(")")[0]
            return [lineId1, lineId2]
        else:
            # all other reasons can't have their ID extracted
            return []

    def flipSingleLine(self, line, layer, geomType=None):
        """
        Flips a given single line.
        :param line: (QgsFeature) line to be flipped.
        :param layer: (QgsVectorLayer) layer containing target feature.
        :param geomType: (int) layer geometry type code.
        """
        self.geometryHandler.flipFeature(layer=layer, feature=line, geomType=geomType)

    def flipInvalidLine(self, node, networkLayer, validLines, geomType=None):
        """
        Fixes lines connected to nodes flagged as one way flowing node where it cannot be.
        :param node: (QgsPoint) invalid node to have its lines flipped.
        :param networkLayer: (QgsVectorLayer) layer containing target feature.
        :param validLines: (list-of-QgsFeature) list of all validated lines.
        :param geomType: (int) layer geometry type code.
        :return: (QgsFeature) flipped line.
        """
        # get dictionaries for speed-up
        endDict = self.nodeDict[node]['end']
        startDict = self.nodeDict[node]['start']
        amountLines = len(endDict + startDict)
        # it is considered that 
        if endDict:
            # get invalid line connected to node
            invalidLine = list(set(endDict) - set(validLines))
            if invalidLine:
                invalidLine = invalidLine[0]
        else:
            # get invalid line connected to node
            invalidLine = list(set(startDict) - set(validLines))
            if invalidLine:
                invalidLine = invalidLine[0]
        # if no invalid lines are identified, something else is wrong and flipping won't be the solution
        if not invalidLine:
            return None
        # flipping invalid line
        self.flipSingleLine(line=invalidLine, layer=networkLayer)
        return invalidLine

    def fixAttributeChangeFlag(self, node, networkLayer):
        """
        Merges the given 2 lines marked as sharing the same set of attributes.
        :param node: (QgsPoint) flagged node.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :return: (str) string containing which line was line the other.
        """
        line_a = self.nodeDict[node]['end'][0]
        line_b = self.nodeDict[node]['start'][0]
        # lines have their order changed so that the deleted line is the intial one
        self.mergeNetworkLines(line_a=line_b, line_b=line_a, layer=networkLayer)
        # the updated feature should be updated into node dict for the NEXT NODE!
        nn = self.getLastNode(lyr=networkLayer, feat=line_b, geomType=1)
        if nn in self.nodeDict: # TODO: @jpesperidiao verifica isso por favor
            for line in self.nodeDict[nn]['end']:
                if line.id() == line_b.id():
                    self.nodeDict[nn]['end'].remove(line)
                    self.nodeDict[nn]['end'].append(line_b)
        # remove attribute change flag node (there are no lines connected to it anymore)
        self.nodesToPop.append(node)
        return self.tr('{0} to {1}').format(line_a.id(), line_b.id())

    def updateNodeDict(self, node, line, networkLayer, geomType=None):
        """
        Updates node dictionary. Useful when direction of a (set of) line is changed.
        """
        # getting first and last nodes
        first = self.getFirstNode(lyr=networkLayer, feat=line, geomType=geomType)
        last = self.getLastNode(lyr=networkLayer, feat=line, geomType=geomType)
        changed = self.changeLineDict(nodeList=[first, last], line=line)
        return changed

    def reclassifyNode(self, node, nodeLayer):
        """
        Reclassifies node.
        :param node: (QgsPoint) node to be reclassified.
        :return: (bool) whether point was modified.
        """
        immutableTypes = [NetworkHandler.UpHillNode, NetworkHandler.DownHillNode, NetworkHandler.WaterwayBegin, NetworkHandler.SpillwayNode]
        if self.nodeTypeDict[node] in immutableTypes:
            # if node type is immutable, reclassification is not possible
            return False
        # get new type
        newType = self.classifyNode([node, self.nodeTypeDict])
        if self.nodeTypeDict[node] == newType:
            # if new node type is the same as new, method won't do anything
            return False
        # alter it in feature
        self.nodeTypeDict[node] = newType
        id_ = self.nodeIdDict[node]
        self.reclassifyNodeType[node] = newType
        return True

    def fixDeltaFlag(self, node, networkLayer, validLines, reason, reasonType=3, geomType=None):
        """
        Tries to fix nodes flagged because of their delta angles.
        :param node: (QgsPoint) invalid node.
        :param network: (QgsVectorLayer) contains network lines.
        :param validLines: (list-of-QgsFeature) lines already validated.
        :param reason: (str) reason of node invalidation.
        :param reasonType: (int) code for invalidation reason.
        :param geomType: (int) code for the layer that contains the network lines.
        :return: (QgsFeature) line to be flipped. If no line is identified as flippable, None is returned.
        """
        flipCandidates = self.getLineIdFromReason(reason=reason, reasonType=reasonType)
        for line in self.nodeDict[node]['start'] + self.nodeDict[node]['end']:
            lineId = str(line.id())
            if lineId in flipCandidates and line not in validLines:
                # flip line that is exposed in invalidation reason and is not previously validated
                self.flipSingleLine(line=line, layer=networkLayer, geomType=geomType)
                return line
        # if no line attend necessary requirements for flipping
        return None

    def fixNodeFlagsNew(self, node, valDict, invalidDict, reason, connectedValidLines, networkLayer, nodeLayer, geomType=None, deltaLinesCheckList=None):
        """
        Tries to fix issues flagged on node
        """
        # initiate lists of lines that were flipped/merged
        flippedLinesIds, mergedLinesString = [], []
        # support list of flipped lines
        flippedLines = []
        # get reason type
        reasonType = self.getReasonType(reason=reason)
        if not reasonType:
            # if node invalidation reason is not among the fixable ones, method stops here.
            return flippedLinesIds, mergedLinesString
        ## try to fix node issues
        if reasonType in [1, 2]:
            # original message: self.tr('Line {0} does not end at a node with IN flow type (node type is {1}). ')
            # original message: self.tr('Line {0} does not start at a node with OUT flow type (node type is {1}). ')
            # get flipping candidates
            featIdFlipCandidates = self.getLineIdFromReason(reason=reason, reasonType=reasonType)
            for lineId in featIdFlipCandidates:
                line = invalidDict[int(lineId)]
                if line not in connectedValidLines:
                    # only non-valid lines may be modified
                    self.flipSingleLine(line=line, layer=networkLayer, geomType=geomType)
                    flippedLinesIds.append(lineId)
                    flippedLines.append(line)
        elif reasonType == 3:
            # original message: self.tr('Lines {0} and {1} have conflicting directions ({2:.2f} deg).')
            line = self.fixDeltaFlag(node=node, networkLayer=networkLayer, reason=reason, validLines=connectedValidLines, reasonType=reasonType)
            if line:
                # if a line is flipped it must be changed in self.nodeDict
                self.updateNodeDict(node=node, line=line, networkLayer=networkLayer, geomType=geomType)
        elif reasonType == 4:
            # original message: self.tr('Redundant node. Connected lines ({0}, {1}) share the same set of attributes.')
            mergedLinesString = self.fixAttributeChangeFlag(node=node, networkLayer=networkLayer)
        elif reasonType == 5:
            # original message: self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
            line = self.flipInvalidLine(node=node, networkLayer=networkLayer, validLines=connectedValidLines, geomType=geomType)
            if line:
                flippedLinesIds.append(str(line.id()))
                flippedLines.append(line)
                # if a line is flipped it must be changed in self.nodeDict
                self.updateNodeDict(node=node, line=line, networkLayer=networkLayer, geomType=geomType)
        else:
            # in case, for some reason, a strange value is given to reasonType
            return [], ''
        # for speed-up
        initialNode = lambda x : self.getFirstNode(lyr=networkLayer, feat=x, geomType=geomType)
        lastNode = lambda x : self.getLastNode(lyr=networkLayer, feat=x, geomType=geomType)
        # reclassification re-evalution is only needed if lines were flipped
        if flippedLinesIds:
            # re-classify nodes connected to flipped lines before re-checking
            # map is a for-loop in C
            reclassifyNodeAlias = lambda x : nodeLayer.changeAttributeValue(self.nodeIdDict[x], 2, int(self.reclassifyNodeType[x])) \
                                                if self.reclassifyNode(node=x, nodeLayer=nodeLayer) \
                                                else None
            map(reclassifyNodeAlias, chain(map(initialNode, flippedLines), map(lastNode, flippedLines)))
            # check if node is fixed and update its dictionaries and invalidation reason
            valDict, invalidDict, reason = self.checkNodeValidity(
                node=node,
                connectedValidLines=connectedValidLines,
                networkLayer=networkLayer,
                geomType=geomType,
                deltaLinesCheckList=deltaLinesCheckList
                )
        return flippedLinesIds, mergedLinesString

    def logAlteredFeatures(self, flippedLines, mergedLinesString, feedback=None):
        """
        Logs the list of flipped/merged lines, if any.
        :param flippedLines: (list-of-int) list of flipped lines.
        :param mergedLinesString: (str) text containing all merged lines (in the form of 'ID1 to ID2, ID3, to ID4')
        :return: (bool) whether or not a message was shown.
        """
        # building warning message
        warning = ''
        if flippedLines:
            warning = "".join([warning, self.tr("Lines that were flipped while directioning hidrography lines: {0}\n\n").format(", ".join(flippedLines))])
        elif mergedLinesString:
            warning = "".join([warning, self.tr("Lines that were merged while directioning hidrography lines: {0}\n\n").format(mergedLinesString)])
        if warning:
            # warning is only raised when there were flags fixed
            if feedback is not None:
                warning = "".join([self.tr('\nVerify Network Directioning: Flipped/Merged Lines\n'), warning])
                feedback.pushInfo(warning)
            return True
        return False

    def getNodeTypeDictFromNodeLayer(self, networkNodeLayer, feedback=None):
        """
        Get all node info (dictionaries for start/end(ing) lines and node type) from node layer.
        :param networkNodeLayer: (QgsVectorLayer) network node layer.
        :return: (tuple-of-dict) node type dict and node id dict, respectively
        """
        nodeTypeDict, nodeIdDict = dict(), dict()
        isMulti = QgsWkbTypes.isMultiType(int(networkNodeLayer.wkbType()))
        featCount = networkNodeLayer.featureCount()
        size = 100/featCount if featCount else 0
        for current, feat in enumerate(networkNodeLayer.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            if isMulti:
                node = feat.geometry().asMultiPoint()[0]                    
            else:
                node = feat.geometry().asPoint()
            nodeTypeDict[node] = int(feat['node_type'])
            nodeIdDict[node] = feat.id()
            if feedback is not None:
                feedback.setProgress(size * current)
        return nodeTypeDict, nodeIdDict

    def clearAuxiliaryLinesLayer(self, invalidLinesLayer, lineIdList=None, commitToLayer=False):
        """
        Clears all (or a given list of points) invalid lines from auxiliary lines layer.
        :param invalidLinesLayer: (QgsVectorLayer) invalid lines layer.
        :param lineIdList: (list-of-int) list of lines IDs to be cleared from layer.
        :param commitToLayer: (bool) indicates whether changes should be commited to layer.
        """
        # invalid reason texts
        invalidReason = self.tr('Connected to invalid hidrography node.')
        nonVisitedReason = self.tr('Line not yet visited.')
        invalidLinesLayer.beginEditCommand('Clear Invalid Lines')
        if lineIdList is None:
            # define a function to get only feature ids for invalid lines registered in invalidLinesLayer and use it in map, for speed-up
            getInvalidLineFunc = lambda feat : feat.id() if feat['reason'] in [invalidReason, nonVisitedReason] else -9999
            # list/set combination to remove possible duplicates of -9999 and avoid unnecessary calculation
            lineIdList = list(set(map(getInvalidLineFunc, invalidLinesLayer.getFeatures())))
            if -9999 in lineIdList:
                lineIdList.remove(-9999)
        invalidLinesLayer.deleteFeatures(lineIdList)
        invalidLinesLayer.endEditCommand()
        # commit changes to LAYER
        if commitToLayer:
            invalidLinesLayer.commitChanges()

    def getAuxiliaryLines(self, fields, invalidLinesDict, nonValidatedLines, networkLayerName):
        """
        Populate from auxiliary lines layer with all invalid lines.
        :param invalidLinesDict: (dict) dictionary containing all invalid lines to be displayed.
        :param nonValidatedLines: (set) set of all non-validated network lines.
        :param commitToLayer: (bool) indicates whether changes should be commited to layer.
        """
        # prepare generic variables that will be reused
        invalidReason = self.tr('Connected to invalid hidrography node.')
        nonVisitedReason = self.tr('Line not yet visited.')
        # initiate new features list
        featList = []
        # pre-declaring method to make it faster
        newInvalidFeatFunc = lambda x : self.createNewInvalidLineFeature(feat_geom=x[0], reason=invalidReason, fields=fields)
        newNonVisitedFeatFunc = lambda x : self.createNewInvalidLineFeature(feat_geom=x[0], reason=nonVisitedReason, fields=fields)
        # add all non-validated features
        for line in nonValidatedLines:
            # create new feture
            feat = newNonVisitedFeatFunc([line.geometry(), line.id()])
            # add it to new features list
            featList.append(feat)
        # add invalid lines
        for lineId, line in invalidLinesDict.items(): 
            # create new feture
            feat = newInvalidFeatFunc([line.geometry(), lineId])
            # add it to new features list
            featList.append(feat)
        return featList
    
    def verifyNetworkDirectioning(self, networkLayer, networkNodeLayer, frame, searchRadius, waterBodyClasses=None, waterSinkLayer=None, spillwayLayer=None, ditchLayer=None, max_amount_cycles=1, attributeBlackList=None, feedback=None, selectValid=False, excludePrimaryKeys=True, ignoreVirtualFields=True):
        fieldList = self.layerHandler.getAttributesFromBlackList(networkLayer, \
                                                            attributeBlackList=attributeBlackList,\
                                                            ignoreVirtualFields=ignoreVirtualFields,\
                                                            excludePrimaryKeys=excludePrimaryKeys)
        waterBodyClasses = [] if waterBodyClasses is None else waterBodyClasses
        # update createNetworkNodesProcess object node dictionary
        stepCount = 0
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(max_amount_cycles, feedback)
            multiStepFeedback.setCurrentStep(stepCount)
        else:
            multiStepFeedback = None
        self.nodesToPop = []
        self.reclassifyNodeType = dict()
        if feedback is not None:
            multiStepFeedback.pushInfo('Identifying nodes...')
            multiStepFeedback.setCurrentStep(stepCount)
            stepCount += 1
        self.nodeDict = self.identifyAllNodes(networkLayer=networkLayer, feedback=multiStepFeedback)
        if feedback is not None:
            multiStepFeedback.pushInfo('Getting auxiliar spatial indexes...')
            multiStepFeedback.setCurrentStep(stepCount)
            stepCount += 1
        auxIndexStructure = self.getAuxIndexStructure(
            networkLayer,
            waterBodiesLayers=waterBodyClasses,
            waterSinkLayer=waterSinkLayer,
            spillwayLayer=spillwayLayer,
            ditchLayer=ditchLayer,
            feedback=multiStepFeedback
        )
        networkLayerGeomType = networkLayer.geometryType()
        networkLayer.startEditing()
        networkNodeLayer.startEditing()
        # declare reclassification function from createNetworkNodesProcess object - parameter is [node, nodeTypeDict] 
        self.classifyNode = lambda x : self.nodeType(
            nodePoint=x[0],
            networkLayer=networkLayer,
            frameLyrContourList=frame,
            waterBodiesLayers=waterBodyClasses,
            searchRadius=searchRadius,
            waterSinkLayer=waterSinkLayer,
            spillwayLayer=spillwayLayer,
            nodeTypeDict=x[1],
            networkLayerGeomType=networkLayerGeomType,
            ditchLayer=ditchLayer,
            fieldList=fieldList,
            auxIndexStructure=auxIndexStructure
            )
        if feedback is not None:
            multiStepFeedback.pushInfo('Getting node type dictionary...')
            multiStepFeedback.setCurrentStep(stepCount)
            stepCount += 1
        self.nodeTypeDict, self.nodeIdDict = self.getNodeTypeDictFromNodeLayer(networkNodeLayer=networkNodeLayer, feedback=multiStepFeedback)
        # initiate nodes, invalid/valid lines dictionaries
        nodeFlags, inval, val = dict(), dict(), dict()
        # cycle count start
        # get max amount of orientation cycles
        max_amount_cycles = max_amount_cycles if max_amount_cycles > 0 else 1
        # validation method FINALLY starts...
        # to speed up modifications made to layers
        networkNodeLayer.beginEditCommand('Reclassify Nodes')
        networkLayer.beginEditCommand('Flip/Merge Lines')
        cycleCount = 0
        while True:
            if feedback is not None:
                multiStepFeedback.pushInfo('Starting cycle {0}...'.format(cycleCount))
                multiStepFeedback.setCurrentStep(stepCount)
                stepCount += 1
            nodeFlags_, inval_, val_ = self.directNetwork(networkLayer=networkLayer, nodeLayer=networkNodeLayer)
            cycleCount += 1
            # Log amount of cycles completed
            cycleCountLog = self.tr("Cycle {0}/{1} completed.").format(cycleCount, max_amount_cycles)
            if feedback is not None:
                multiStepFeedback.pushInfo(cycleCountLog)
                multiStepFeedback.setCurrentStep(cycleCount)
            self.reclassifyNodeType = dict()
            # stop conditions: max amount of cycles exceeded, new flags is the same as previous flags (there are no new issues) and no change
            # change to valid lines list was made (meaning that the algorithm did not change network state) or no flags found
            if (cycleCount == max_amount_cycles) or (not nodeFlags_) or \
            (set(nodeFlags.keys()) == set(nodeFlags_.keys()) and val == val_):
                # copy values to final dict
                nodeFlags, inval, val = nodeFlags_, inval_, val_
                # no more modifications to those layers will be done
                networkLayer.endEditCommand()
                networkNodeLayer.endEditCommand()
                # try to load auxiliary line layer to fill it with invalid lines
                featList = self.getFlagLines(networkLayer, val, inval)
                invalidLinesLog = self.tr("Invalid lines were exposed in line flags layer.")
                if feedback is not None:
                    multiStepFeedback.pushInfo(invalidLinesLog)
                    multiStepFeedback.setCurrentStep(max_amount_cycles)
                vLines = val.keys()
                iLines = inval.keys()
                intersection = set(vLines) & set(iLines)
                if intersection:
                    map(val.pop, intersection)
                    # remove unnecessary variables
                    del vLines, iLines, intersection
                break
            # for the next iterations
            nodeFlags, inval, val = nodeFlags_, inval_, val_
            # pop all nodes to be popped and reset list
            for node in self.nodesToPop:
                # those were nodes connected to lines that were merged and now are no longer to be used
                self.nodeDict.pop(node, None)
                self.nodeDict.pop(node, None)
            self.nodesToPop = []
        if selectValid:
            networkLayer.selectByIds(list(val.keys()))
        if feedback is not None:
            percValid = float(len(val))*100.0/float(networkLayer.featureCount()) if networkLayer.featureCount() else 0
            if nodeFlags:
                msg = self.tr('{0} nodes may be invalid ({1:.2f}' + '% of network is well directed). Check flags.')\
                            .format(len(nodeFlags), percValid)
            else:
                msg = self.tr('{1:.2f}' + '% of network is well directed.')\
                            .format(len(nodeFlags), percValid)
            multiStepFeedback.pushInfo(msg)
        return nodeFlags, featList, self.nodeIdDict
    
    def getFlagLines(self, networkLayer, val, inval):
        # get non-validated lines and add it to invalid lines layer as well
        nonValidatedLines = set()
        for line in networkLayer.getFeatures():
            lineId = line.id()
            if lineId in val or lineId in inval:
                # ignore if line are validated
                continue
            nonValidatedLines.add(line)
        featList = self.getAuxiliaryLines(fields=self.getFlagFields(), invalidLinesDict=inval,\
                                        nonValidatedLines=nonValidatedLines, networkLayerName=networkLayer.name())
        return featList
    
    def mergeNetworkLines(self, line_a, line_b, layer):
        """
        Merge 2 lines of the same layer (it is assumed that they share the same set od attributes - except for ID and geometry).
        In case sets are different, the set of attributes from line_a will be kept. If geometries don't touch, method is not applicable.
        :param line_a: (QgsFeature) main line of merging process.
        :param line_b: (QgsFeature) line to be merged to line_a.
        :param layer: (QgsVectorLayer) layer containing given lines.
        :return: (bool) True if method runs OK or False, if lines do not touch.
        """
        # check if original layer is a multipart
        isMulti = QgsWkbTypes.isMultiType(int(layer.wkbType()))
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
    
    def getFlagFields(self):
        fields = QgsFields()
        fields.append(QgsField('reason',QVariant.String))
        return fields

    def createNewInvalidLineFeature(self, feat_geom, reason, fields):
        """
        Creates a new feature to be added to invalid lines layer.
        :param feat_geom: (QgsGeometry) 
        :param reason: (str) reason of line invalidation.
        :param fields: (QgsFields) object containing all fields from layer.
        :return: (QgsFeature) new feature.
        """
        # set attribute map and create new feture
        feat = QgsFeature(fields)
        # set geometry
        feat.setGeometry(feat_geom)
        return feat