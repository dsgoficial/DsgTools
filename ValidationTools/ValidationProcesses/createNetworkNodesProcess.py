# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-07-03
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

from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsFeature, QgsWKBTypes, QgsRectangle, \
                      QgsFeatureRequest, QgsDataSourceURI
from PyQt4.QtGui import QMessageBox

import processing, binascii
from collections import OrderedDict
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.ValidationTools.ValidationProcesses.hidrographyFlowProcess import HidrographyFlowParameters
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class CreateNetworkNodesProcess(ValidationProcess):
    # enum for node types
    Flag, Sink, WaterwayBegin, UpHillNode, DownHillNode, Confluence, Ramification, AttributeChange, NodeNextToWaterBody, AttributeChangeFlag, ConstantFlowNode, DisconnectedLine = range(12)
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Class constructor.
        :param postgisDb: (DsgTools.AbstractDb) postgis database connection.
        :param iface: (QgisInterface) QGIS interface object.
        :param instantiating: (bool) indication of whether method is being instatiated.
        """
        super(CreateNetworkNodesProcess, self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Create Network Nodes')
        self.hidNodeLayerName = 'aux_hid_nodes_p'
        self.canvas = self.iface.mapCanvas()
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        # name for node types (check enum atop)
        self.nodeTypeNameDict = {
                                    CreateNetworkNodesProcess.Flag : self.tr("Flag"),
                                    CreateNetworkNodesProcess.Sink : self.tr("Sink"),
                                    CreateNetworkNodesProcess.WaterwayBegin : self.tr("Waterway Beginning"),
                                    CreateNetworkNodesProcess.UpHillNode : self.tr("Up Hill Node"),
                                    CreateNetworkNodesProcess.DownHillNode : self.tr("Down Hill Node"),
                                    CreateNetworkNodesProcess.Confluence : self.tr("Confluence"),
                                    CreateNetworkNodesProcess.Ramification : self.tr("Ramification"),
                                    CreateNetworkNodesProcess.AttributeChange : self.tr("Attribute Change Node"),
                                    CreateNetworkNodesProcess.NodeNextToWaterBody : self.tr("Node Next to Water Body"),
                                    CreateNetworkNodesProcess.AttributeChangeFlag : self.tr("Attribute Change Flag"),
                                    CreateNetworkNodesProcess.ConstantFlowNode : self.tr("Constant Flow Node"),
                                    CreateNetworkNodesProcess.DisconnectedLine : self.tr("Disconnected From Network")
                                    # CreateNetworkNodesProcess.NodeOverload : self.tr("Overloaded Node")
                                }
        if not self.instantiating:
            # getting tables with elements (line primitive)
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {
                                        self.tr('Category'):cat,
                                        self.tr('Layer Name'):lyrName,
                                        self.tr('Geometry\nColumn'):geom,
                                        self.tr('Geometry\nType'):geomType,
                                        self.tr('Layer\nType'):tableType
                                     }
            self.networkClassesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            networkFlowParameterList = HidrographyFlowParameters(self.networkClassesWithElemDict.keys())
            self.sinkClassesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['p'], withElements=True, excludeValidation = True)
            sinkFlowParameterList = HidrographyFlowParameters(self.sinkClassesWithElemDict.keys())            
            self.parameters = {
                                self.tr('Only Selected') : False,
                                self.tr('Network Layer') : networkFlowParameterList,
                                self.tr('Sink Layer') : sinkFlowParameterList,
                                self.tr('Search Radius') : 5.0,
                                self.tr('Reference and Water Body Layers'): OrderedDict( {
                                                                       'referenceDictList':{},
                                                                       'layersDictList':interfaceDict
                                                                     } ),
                              }
            self.nodeDict = None
            self.nodeTypeDict = None
    
    def getFrameOutterBounds(self, frameLayer):
        """
        Gets the outter bounds of all frame features composing frame layer.
        :param frameLayer: (QgsVectorLayer) frame layer.
        :return: (list-of-QgsGeometry) list of all disjuncts outter bounds of features in frame layer.
        """
        frameGeomList = []
        # dissolve every feature into a single one
        result = processing.runalg('qgis:dissolve', frameLayer, True, None, None)
        # get the layer from processing result
        outputLayer = processing.getObject(result['OUTPUT'])
        # clean possible missinformation from resulting layer
        # setting clean parameters
        tools = 'rmsa,break,rmdupl,rmdangle'
        threshold = -1
        extent = outputLayer.extent()
        (xmin, xmax, ymin, ymax) = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        snap = self.parameters[self.tr('Search Radius')]
        minArea = 0.0001
        result = processing.runalg('grass7:v.clean.advanced', outputLayer, tools, threshold, extent, snap, minArea, None, None)
        # get resulting layer
        outputLayer = processing.getObject(result['output'])
        # get all frame outter layer found
        for feat in outputLayer.getFeatures():
            geom = feat.geometry()
            # deaggregate geometry, if necessary
            geomList = self.DsgGeometryHandler.deaggregateGeometry(multiGeom=geom)
            # for every deaggregated node, get only the outter bound as a polyline (for intersection purposes)
            frameGeomList += [QgsGeometry().fromPolyline(g.asPolygon()[0]) for g in geomList]
        return frameGeomList

    def identifyAllNodes(self, networkLayer):
        """
        Identifies all nodes from a given layer (or selected features of it). The result is returned as a dict of dict.
        :param networkLayer: target layer to which nodes identification is required.
        :return: { node_id : { start : [feature_which_starts_with_node], end : feature_which_ends_with_node } }.
        """
        nodeDict = dict()
        isMulti = QgsWKBTypes.isMultiType(int(networkLayer.wkbType()))
        if self.parameters['Only Selected']:
            features = networkLayer.selectedFeatures()
        else:
            features = [feat for feat in networkLayer.getFeatures()]
        for feat in features:
            nodes = self.DsgGeometryHandler.getFeatureNodes(networkLayer, feat)
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
        qgisPoint = QgsGeometry.fromPoint(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        for frameContour in frameLyrContourList:
            if buf.intersects(frameContour):
                # it is condition enough one of the frame contours to be next to node
                return True
        return False

    def nodeNextToWaterBodies(self, node, waterBodiesLayers, searchRadius):
        """
        Identify whether or not node is next to a water body feature.
        :param node: (QgsPoint) node to be identified as next to a water body feature.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of layers composing the water bodies on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """        
        qgisPoint = QgsGeometry.fromPoint(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
        # check if buffer intersects features from water bodies layers
        for lyr in waterBodiesLayers:
            if lyr.geometryType() == 0:
                # ignore point primitive layers
                continue
            for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                if buf.intersects(feat.geometry()):
                    # any feature component of a water body intersected is enough
                    return True
        return False

    def nodeIsWaterSink(self, node, waterSinkLayer, searchRadius):
        """
        Identify whether or not node is next to a water body feature. If no water sink layer is given, method returns False
        :param node: (QgsPoint) node to be identified as coincident with a water sink feature.
        :param waterSinkLayer: (QgsVectorLayer) layer containing the water sinks on map.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to a water body element.
        """
        if not waterSinkLayer:
            return False
        qgisPoint = QgsGeometry.fromPoint(node)
        # building bounding box around node for feature requesting
        bbRect = qgisPoint.buffer(searchRadius, -1).boundingBox()
        # check if qgisPoint (node geometry) is over a sink classified point
        for feat in waterSinkLayer.getFeatures(QgsFeatureRequest(bbRect)):
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
        qgisPoint = QgsGeometry.fromPoint(node)
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

    def getAttributesFromFeature(self, feature, layer, fieldNames=None):
        """
        Retrieves the attributes from a given feature, except for their geometry and ID column values. If a list of
        attributes is given, method will return those attributes if found. In case no attribute is found, None will 
        :param feature: (QgsFeature) feature from which attibutes will be retrieved.
        :param layer: (QgsVectorLayer) layer containing target feature.
        :param fieldNames: (list-of-str) list of field names to be exposed.
        :return: (dict-of-object) attribute values for each attribute mapped.
        """
        # fields to be ignored
        ignoreList = []
        if not fieldNames:
            # retrieving key column name
            uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
            keyColumn = uri.keyColumn()
            # retrieving geometry column name
            networLayerName = layer.name()
            for key in self.networkClassesWithElemDict.keys():
                if key.split(",")[1] in networLayerName:
                    geomColumn = key.split(",")[2]
                    break
            # removing attributes that are calculated OTF
            fieldNames = [f for f in layer.fields() if f.name() not in [keyColumn, geomColumn] and '_otf' not in f.name()]
        else:
            # check if all field names given are in fact fields for the layer
            layerFields = layer.fields()
            ignoreList = [field for field in fieldNames if field not in layerFields]
        return { field.name() : feature[field.name()] for field in fieldNames if field not in ignoreList }

    def attributeChangeCheck(self, node, networkLayer):
        """
        Checks if attribute change node is in fact an attribute change.
        :param node: (QgsPoint) node to be identified as over the frame layer or not.
        :param networkLayer: (QgsVectorLayer) layer containing network lines.
        :return: (bool) if lines connected to node do change attributes.
        """        
        # assuming that attribute change nodes have only 1-in 1-out lines
        lineIn = self.nodeDict[node]['end'][0]
        atrLineIn = self.getAttributesFromFeature(feature=lineIn, layer=networkLayer)
        lineOut = self.nodeDict[node]['start'][0]
        atrLineOut = self.getAttributesFromFeature(feature=lineOut, layer=networkLayer)
        # comparing their dictionary of attributes, it is decided whether they share the exact same set of attributes (fields and values)
        return atrLineIn != atrLineOut

    def isFirstOrderDangle(self, node, networkLayer, searchRadius):
        """
        Checks whether node is a dangle into network (connected to a first order line).
        :param node: (QgsPoint) node to be validated.
        :param networkLayer: (QgsVectorLayer) network layer (line layer).
        :param searchRadius: (float) limit distance to another line.
        :return: (bool) indication whether node is a dangle.
        """
        qgisPoint = QgsGeometry.fromPoint(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1)
        # building bounding box around node for feature requesting
        bbRect = buf.boundingBox()
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
        isMulti = QgsWKBTypes.isMultiType(int(networkLayer.wkbType()))
        # get all other nodes connected to lines connected to "node"
        lines = nodePointDict['start'] + nodePointDict['end']
        if len(lines) > 1:
            # if there is at least one more line connected to node, line is not disconnected
            return False
        # get line nodes
        n = self.DsgGeometryHandler.getFeatureNodes(layer=networkLayer, feature=lines[0], geomType=geomType)
        if nodePointDict['start']:            
            # if line starts at target node, the other extremity is a final node
            if isMulti:
                if n:
                    n = n[0][-1]
            elif n:
                n = n[-1]
        elif nodePointDict['end']:
            # if line starts at target node, the other extremity is a initial node
            if isMulti:
                if n:
                    n = n[0][0]
            elif n:
                n = n[0]
        # if next node is not among the valid ending lines, it may still be connected to a disconnected line if it is a dangle
        # validEnds = [CreateNetworkNodesProcess.Sink, CreateNetworkNodesProcess.DownHillNode, CreateNetworkNodesProcess.NodeNextToWaterBody]
        if n in nodeTypeDict:
            # if both ends are classified as waterway beginning, then both ends are 1st order dangles and line is disconnected.
            return nodeTypeDict[n] == CreateNetworkNodesProcess.WaterwayBegin
            # if nodeTypeDict[n] not in validEnds:
            #     if self.isFirstOrderDangle(node=n, networkLayer=networkLayer, searchRadius=self.parameters[self.tr('Search Radius')]):
            #         # if next node is not a valid network ending node and is a dangle, line is disconnected from network 
            #         return False
            #     return True
        # in case next node is not yet classified, method is ineffective
        return False

    def nodeType(self, nodePoint, networkLayer, frameLyrContourList, waterBodiesLayers, searchRadius, nodeTypeDict, waterSinkLayer=None, networkLayerGeomType=None):
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
        #     return CreateNetworkNodesProcess.NodeOverload
        # case 1: all lines either flow in or out 
        if startXORendLine:
            # case 1.a: point is over the frame
            if self.nodeOnFrame(node=nodePoint, frameLyrContourList=frameLyrContourList, searchRadius=searchRadius):
                # case 1.a.i: waterway is flowing away from mapped area (point over the frame has one line ending line)
                if hasEndLine:
                    return CreateNetworkNodesProcess.DownHillNode
                # case 1.a.ii: waterway is flowing to mapped area (point over the frame has one line starting line)
                elif hasStartLine:
                    return CreateNetworkNodesProcess.UpHillNode                
            # case 1.b: point that legitimately only flows from
            elif hasEndLine:
                # case 1.b.i
                if self.nodeNextToWaterBodies(node=nodePoint, waterBodiesLayers=waterBodiesLayers, searchRadius=searchRadius):
                    # it is considered that every free node on map is a starting node. The only valid exceptions are nodes that are
                    # next to water bodies and water sink holes.
                    if sizeFlowIn == 1 or (sizeFlowIn > 1 and not self.checkIfHasLineInsideWaterBody(node=nodePoint, waterBodiesLayers=waterBodiesLayers)):
                        # a node next to water cannot have ANY of its EXCEEDING ending lines coming from inside a water body feature 
                        return CreateNetworkNodesProcess.NodeNextToWaterBody
                # force all lose ends to be waterway beginnings if they're not dangles (which are flags)
                elif self.isFirstOrderDangle(node=nodePoint, networkLayer=networkLayer, searchRadius=self.parameters[self.tr('Search Radius')]):
                    # check if node is connected to a disconnected line
                    if self.checkIfLineIsDisconnected(node=nodePoint, networkLayer=networkLayer, nodeTypeDict=nodeTypeDict, geomType=networkLayerGeomType):
                        return CreateNetworkNodesProcess.DisconnectedLine
                    # case 1.b.ii: node is in fact a water sink and should be able to take an 'in' flow
                    elif self.nodeIsWaterSink(node=nodePoint, waterSinkLayer=waterSinkLayer, searchRadius=searchRadius):
                        # if a node is indeed a water sink (operator has set it to a sink)
                        return CreateNetworkNodesProcess.Sink
                    return CreateNetworkNodesProcess.WaterwayBegin
            # case 1.c: point that legitimately only flows out
            elif hasStartLine and self.isFirstOrderDangle(node=nodePoint, networkLayer=networkLayer, searchRadius=self.parameters[self.tr('Search Radius')]):
                if self.checkIfLineIsDisconnected(node=nodePoint, networkLayer=networkLayer, nodeTypeDict=nodeTypeDict, geomType=networkLayerGeomType):
                    return CreateNetworkNodesProcess.DisconnectedLine
                elif self.nodeIsWaterSink(node=nodePoint, waterSinkLayer=waterSinkLayer, searchRadius=searchRadius):
                    # in case there's a wrongly acquired line connected to a water sink
                    return CreateNetworkNodesProcess.Sink
                return CreateNetworkNodesProcess.WaterwayBegin
            # case 1.d: points that are not supposed to have one way flow (flags)
            return CreateNetworkNodesProcess.Flag
        elif sizeFlowIn > sizeFlowOut:
            # case 2 "confluence"
            return CreateNetworkNodesProcess.Confluence
        elif sizeFlowIn == sizeFlowOut:
            if sizeFlowIn > 1:
                # case 4.c: there's a constant flow through node, but there are more than 1 line
                return CreateNetworkNodesProcess.ConstantFlowNode
            elif self.attributeChangeCheck(node=nodePoint, networkLayer=networkLayer):
                # case 4.a: lines do change their attribute set
                return CreateNetworkNodesProcess.AttributeChange
            else:
                # case 4.b: nodes inside the network that are there as an attribute change node but lines connected
                #           to it have the same set of attributes
                return CreateNetworkNodesProcess.AttributeChangeFlag
        else:
            # case 3 "ramification"
            return CreateNetworkNodesProcess.Ramification

    def classifyAllNodes(self, networkLayer, frameLyrContourList, waterBodiesLayers, searchRadius, waterSinkLayer=None, nodeList=None):
        """
        Classifies all identified nodes from the hidrography line layer.
        :param networkLayer: (QgsVectorLayer) network lines layer.
        :param frameLyrContourList: (list-of-QgsFeature) border line for the frame layer.
        :param waterBodiesLayers: (list-of-QgsVectorLayer) list of all classes with water bodies to be compared to.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :param nodeList: a list of nodes (QgsPoint) to be classified. If not given, whole dict is going 
                         to be classified. Node MUST be in dict given, if not, it'll be ignored.
        :param waterSinkLayer: (QgsVectorLayer) water sink layer.
        :return: a (dict) dictionary of node and its node type ( { (QgsPoint)node : (int)nodeType } ). 
        """
        networkLayerGeomType = networkLayer.geometryType()
        nodeTypeDict = dict()
        nodeKeys = self.nodeDict.keys()
        if not nodeList:
            nodeList = nodeKeys
        for node in nodeList:
            if node not in nodeKeys:
                # in case user decides to use a list of nodes to work on, given nodes that are not identified will be ignored
                continue
            nodeTypeDict[node] = self.nodeType(nodePoint=node, networkLayer=networkLayer, frameLyrContourList=frameLyrContourList, \
                                    waterBodiesLayers=waterBodiesLayers, searchRadius=searchRadius, waterSinkLayer=waterSinkLayer, \
                                    nodeTypeDict=nodeTypeDict, networkLayerGeomType=networkLayerGeomType)
        return nodeTypeDict

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
            feat.setGeometry(QgsGeometry.fromMultiPoint([node]))
            feat['node_type'] = self.nodeTypeDict[node] if node in nodeTypeKeys else None
            feat['layer'] = networkLineLayerName
            featList.append(feat)
        nodeLayer.addFeatures(featList)
        nodeLayer.endEditCommand()
        if commitToLayer:
            nodeLayer.commitChanges()

    def loadLayer(self, layerName, uniqueLoad=True):
        """
        Load a given layer to canvas.
        :param layerName: (str) layer name to be loaded.
        :param uniqueLoad: (bool) indicates that layer will be loaded to canvas only if it is not loaded already.
        :return: (QgsVectorLayer) the loaded layer.
        """
        try:
            return self.layerLoader.load([layerName], uniqueLoad=uniqueLoad)[layerName]
        except Exception as e:
            errorMsg = self.tr('Could not load the class {0}! (If you manually removed {0} from database, reloading QGIS/DSGTools Plugin might sort out the problem.\n').format(layerName)+':'.join(e.args)
            QMessageBox.critical(self.canvas, self.tr('Error!'), errorMsg)

    def execute(self):
        """
        Structures and executes the process.
        :return: (int) execution code.
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            # node type should not be calculated OTF for comparison (db data is the one perpetuated)
            # setting all method variables
            networkLayerKey = self.parameters[self.tr('Network Layer')]
            hidSinkLyrKey = self.parameters[self.tr('Sink Layer')]
            refKey, classesWithElemKeys = self.parameters[self.tr('Reference and Water Body Layers')]
            waterBodyClassesKeys = classesWithElemKeys
            if not refKey:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                return 1
            # preparing reference layer
            refcl = self.classesWithElemDict[refKey]
            frameLayer = self.loadLayerBeforeValidationProcess(refcl)
            # preparing hidrography lines layer
            # remake the key from standard string
            k = ('{},{},{},{},{}').format(
                                          networkLayerKey.split('.')[0],\
                                          networkLayerKey.split('.')[1].split(r' (')[0],\
                                          networkLayerKey.split('(')[1].split(', ')[0],\
                                          networkLayerKey.split('(')[1].split(', ')[1],\
                                          networkLayerKey.split('(')[1].split(', ')[2].replace(')', '')
                                         )
            hidcl = self.networkClassesWithElemDict[k]
            networkLayer = self.loadLayerBeforeValidationProcess(hidcl)
            # preparing the list of water bodies classes
            waterBodyClasses = []
            for key in waterBodyClassesKeys:
                wbc = self.classesWithElemDict[key]
                waterBodyClasses.append(self.loadLayerBeforeValidationProcess(wbc))
            # preparing water sink layer
            if hidSinkLyrKey and hidSinkLyrKey != self.tr('Select Layer'):
                # remake the key from standard string
                k = ('{},{},{},{},{}').format(
                                          hidSinkLyrKey.split('.')[0],\
                                          hidSinkLyrKey.split('.')[1].split(r' (')[0],\
                                          hidSinkLyrKey.split('(')[1].split(', ')[0],\
                                          hidSinkLyrKey.split('(')[1].split(', ')[1],\
                                          hidSinkLyrKey.split('(')[1].split(', ')[2].replace(')', '')
                                         )
                sinkcl = self.sinkClassesWithElemDict[k]
                waterSinkLayer = self.loadLayerBeforeValidationProcess(sinkcl)
            else:
                # if no sink layer is selected, layer should be ignored
                waterSinkLayer = None
            # getting dictionaries of nodes information 
            frame = self.getFrameOutterBounds(frameLayer=frameLayer)
            self.nodeDict = self.identifyAllNodes(networkLayer=networkLayer)
            crs = networkLayer.crs().authid()
            # node layer has the same CRS as the hidrography lines layer
            nodeSrid = networkLayer.crs().authid().split(':')[1]
            searchRadius = self.parameters[self.tr('Search Radius')]
            self.nodeTypeDict = self.classifyAllNodes(networkLayer=networkLayer, frameLyrContourList=frame, waterBodiesLayers=waterBodyClasses, searchRadius=searchRadius, waterSinkLayer=waterSinkLayer)
            # check if node table and node type domain table are created on db
            if not self.abstractDb.checkIfTableExists('validation', self.hidNodeLayerName):
                # if it does not exist, it is created
                self.abstractDb.createHidNodeTable(nodeSrid)
            # load node table into canvas
            nodeLayer = self.loadLayer(self.hidNodeLayerName)
            # to be able to update features into new layer
            nodeLayer.startEditing()
            self.fillNodeLayer(nodeLayer=nodeLayer, networkLineLayerName=networkLayer.name())
            msg = self.tr('Network nodes created into layer {}.').format(self.hidNodeLayerName)
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(': '.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
