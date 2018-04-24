# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-03-26
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

from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsFeature, QgsWKBTypes
from qgis.gui import QgsMapTool

import processing, binascii, math
from collections import OrderedDict
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class HidrographyFlowProcess(ValidationProcess):
    # ATENÇÃO: PASSAR OS TIPOS DE NÓS PARA UM ENUM!
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor.
        """
        super(HidrographyFlowProcess, self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Hidrography Network Directioning')
        self.hidNodeLayerName = 'aux_hid_nodes_p'
        self.canvas = self.iface.mapCanvas()
        self.QgsMapTool = QgsMapTool(self.canvas)
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        if not self.instantiating:
            # getting tables with elements (line primitive)
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
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
            self.parameters = {
                                'Only Selected' : False,
                                'Search Radius' : 5.0,
                                'Reference and Layers': OrderedDict( {
                                                                       'referenceDictList':{},
                                                                       'layersDictList':interfaceDict
                                                                     } )
                                #'Classes' :  interfaceDictList
                              }
            self.nodeDbIdDict = None
            self.nodeDict = None
            self.nodeTypeDict = None

    def getFrameContour(self, frameLayer):
        """
        Read frame contour, frame, hidrography lines and hidrgrography node layers.
        :param frameLayer: (QgsVectorLayer) frame layer.
        :return: (QgsGeometry) frame contour.
        """
        frame = [feat for feat in frameLayer.getFeatures()]
        frame = frame[0]
        frame = self.DsgGeometryHandler.getFeatureNodes(frameLayer, frame)
        frame = QgsGeometry().fromPolyline(frame[0][0])
        return frame
    
    def identifyAllNodes(self, hidLineLayer):
        """
        Identifies all nodes from a given layer (or selected features of it). The result is returned as a dict of dict.
        :param hidLineLayer: target layer to which nodes identification is required.
        :return: { node_id : { start : [feature_which_starts_with_node], end : feature_which_ends_with_node } }.
        """
        nodeDict = dict()
        isMulti = QgsWKBTypes.isMultiType(int(hidLineLayer.wkbType()))
        if self.parameters['Only Selected']:
            features = hidLineLayer.selectedFeatures()
        else:
            features = [feat for feat in hidLineLayer.getFeatures()]
        for feat in features:
            nodes = self.DsgGeometryHandler.getFeatureNodes(hidLineLayer, feat)
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
                        temp = nodes[0]
                        nodes = temp                
                # initial node
                pInit, pEnd = nodes[0], nodes[-1]
                # filling starting node information into dictionary
                if pInit not in nodeDict.keys():
                    # if the point is not already started into dictionary, it creates a new item
                    nodeDict[pInit] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pInit]['start']:
                    nodeDict[pInit]['start'].append(feat)                            
                # filling ending node information into dictionary
                if pEnd not in nodeDict.keys():
                    nodeDict[pEnd] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pEnd]['end']:
                    nodeDict[pEnd]['end'].append(feat)
        return nodeDict

    def nodeOnFrame(self, node, frameLyrContour, searchRadius):
        """
        Identify whether or not node is over the frame. Returns True if point is over the frame and false if
        node is not on frame. If identification fails, returns 'None'.
        :param node: node (QgsPoint) to be identified as over the frame layer or not.
        :param frameLyrContour: (QgsGeometry) border line for the frame layer to be checked.
        :param searchRadius: maximum distance to frame layer such that the feature is considered touching it.
        :return: (bool) whether node is as close as searchRaius to frame contour.
        """
        qgisPoint = QgsGeometry.fromPoint(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1).boundingBox().asWktPolygon()
        buf = QgsGeometry.fromWkt(buf)
        return buf.intersects(frameLyrContour)

    def nodeType(self, nodePoint, frameLyrContour, searchRadius):
        """
        Get the node type given all lines that flows from/to it.
        :param nodePoint: (QgsPoint) point to be classified.
        :param frameLyrContour: (QgsGeometry) border line for the frame layer to be checked.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :return: returns the (int) point type.
        """
        dictStartingEndingLinesEntry = self.nodeDict[nodePoint]
        sizeFlowOut = len(dictStartingEndingLinesEntry['start'])
        sizeFlowIn = len(dictStartingEndingLinesEntry['end'])
        hasStartLine = bool(sizeFlowOut)
        hasEndLine = bool(sizeFlowIn)
        # "exclusive or"
        startXORendLine = (hasStartLine != hasEndLine)
        # case 1: all lines either flow in or out 
        if startXORendLine:
            # case 1.a: point is over the frame
            if self.nodeOnFrame(node=nodePoint, frameLyrContour=frameLyrContour, searchRadius=searchRadius):
                # case 1.a.i: waterway is flowing away from mapped area (point over the frame has one line ending line)
                if hasEndLine:
                    return 3
                # case 1.a.ii: waterway is flowing to mapped area (point over the frame has one line starting line)
                elif hasStartLine:
                    return 4
            # case 1.b: point that legitimately only flows from
            elif hasEndLine:
                return 1
            # case 1.c: point that legitimately only flows out
            elif hasStartLine:
                return 2
            # case 1.d: points that are not supposed to have one way flow (flags)
            return 0        
        elif sizeFlowIn > sizeFlowOut:
            # case 2 "confluence"
            return 5
        elif sizeFlowIn == sizeFlowOut:
            # case 4 "attribute change"
            return 7
        else:
            # case 3 "ramification"
            return 6

    def classifyAllNodes(self, frameLyrContour, searchRadius, nodeList=None):
        """
        Classifies all identified nodes from the hidrography line layer.
        :param frameLyrContour: (QgsFeature) border line for the frame layer.
        :param searchRadius: (float) maximum distance to frame layer such that the feature is considered touching it.
        :param nodeList: a list of nodes (QgsPoint) to be classified. If not given, whole dict is going 
                         to be classified. Node MUST be in dict given, if not, it'll be ignored.
        :return: a (dict) dictionary of node and its node type ( { (QgsPoint)node : (int)nodeType } ). 
        """
        nodeTypeDict = dict()
        nodeKeys = self.nodeDict.keys()
        if not nodeList:
            nodeList = nodeKeys
        for node in nodeList:
            if node not in nodeKeys:
                # in case user decides to use a list of nodes to work on, given nodes that are not identified will be ignored
                continue
            nodeTypeDict[node] = self.nodeType(nodePoint=node, frameLyrContour=frameLyrContour, searchRadius=searchRadius)
        return nodeTypeDict

    def fillNodeTable(self, hidLineLayer):
        """
        Populate hidrography node layer with all nodes.
        :param hidLineLayer: (QgsVectorLayer) hidrography lines layer.
        """
        lyrName = hidLineLayer.name()
        crs = hidLineLayer.crs().authid().split(":")[1]
        for node in self.nodeDict.keys():
            # get node geometry as wkt for database loading
            nWkt = QgsGeometry().fromMultiPoint([node]).exportToWkt()
            # if node is loaded into database, the following method returns True
            if self.abstractDb.insertHidValNode(layerName=lyrName, node=nWkt, nodeType=self.nodeTypeDict[node], crs=crs):
                continue
            else:
                return False
        return True

    def getFirstNode(self, lyr, feat, geomType=None):
        """
        Returns the starting node of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
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

    def calculateAzimuthFromNode(self, node, hidLineLayer, geomType=None):
        """
        Computate all azimuths from (closest portion of) lines flowing in and out of a given node.
        :param node: (QgsPoint) hidrography node reference for line and angle calculation.
        :param hidLineLayer: (QgsVectorLayer) hidrography line layer.
        :param geomType: (int) layer geometry type (1 for lines).
        :return: dict of azimuths of all lines ( { featId : azimuth } )
        """
        if not geomType:
            geomType = hidLineLayer.geometryType()
        nodePointDict = self.nodeDict[node]
        azimuthDict = dict()
        for line in nodePointDict['start']:
            # if line starts at node, then angle calculate is already azimuth
            endNode = self.getSecondNode(lyr=hidLineLayer, feat=line, geomType=geomType)
            azimuthDict[line] = node.azimuth(endNode)
        for line in nodePointDict['end']:
            # if line ends at node, angle must be adapted in order to get azimuth
            endNode = self.getPenultNode(lyr=hidLineLayer, feat=line, geomType=geomType)
            azimuthDict[line] = node.azimuth(endNode)
        return azimuthDict

    def checkLineDirectionConcordance(self, line_a, line_b, hidLineLayer, geomType=None):
        """
        Given two lines, this method checks whether lines flow to/from the same node or not.
        If they do not have a common node, method returns false.
        :param line_a: (QgsFeature) line to be compared flowing to a common node.
        :param line_b: (QgsFeature) the other line to be compared flowing to a common node.
        :param hidLineLayer: (QgsVectorLayer) hidrography line layer.
        :return: (bool) True if lines are flowing to/from the same.
        """
        if not geomType:
            geomType = hidLineLayer.geometryType()
        # first and last node of each line
        fn_a = self.getFirstNode(lyr=hidLineLayer, feat=line_a, geomType=geomType)
        ln_a = self.getLastNode(lyr=hidLineLayer, feat=line_a, geomType=geomType)
        fn_b = self.getFirstNode(lyr=hidLineLayer, feat=line_b, geomType=geomType)
        ln_b = self.getLastNode(lyr=hidLineLayer, feat=line_b, geomType=geomType)
        # if lines are flowing to/from the same node (they are flowing the same way)
        return (fn_a == fn_b or ln_a == ln_b)

    def validateDeltaLinesAng(self, node, hidLineLayer, geomType=None):
        """
        Validates a set of lines connected to a node as for the angle formed between them.
        :param node: (QgsPoint) hidrography node to be validated.
        :param hidLineLayer: (QgsVectorLayer) hidrography line layer.
        :return: if node is invalid, returns the reason of invalidation (str).
        """
        if not geomType:
            geomType = hidLineLayer.geometryType()
        azimuthDict = self.calculateAzimuthFromNode(node=node, hidLineLayer=hidLineLayer, geomType=None)
        for idx1, key1 in enumerate(azimuthDict.keys()):
            if idx1 == len(azimuthDict.keys()):
                # if first comparison element is already the last feature, all differences are already computed
                break
            for idx2, key2 in enumerate(azimuthDict.keys()):
                if idx1 >= idx2:
                    # in order to calculate only f1 - f2, f1 - f3, f2 - f3 (for 3 features, for instance)
                    continue
                absAzimuthDifference = math.fmod((azimuthDict[key1] - azimuthDict[key2] + 360), 360)
                if absAzimuthDifference < 90:
                    # if it's a 'beak', lines cannot have opposing directions (e.g. cannot flow to/from the same node)
                    if not self.checkLineDirectionConcordance(line_a=key1, line_b=key2, hidLineLayer=hidLineLayer, geomType=geomType):
                        return self.tr('Lines {0} and {1} have conflicting directions ({2:.3g} deg).').format(key1.id(), key2.id(), absAzimuthDifference)
                elif absAzimuthDifference != 90:
                    # if it's any other disposition, lines can have the same orientation
                    continue
                else:
                    # if lines touch each other at a right angle, then it is impossible to infer waterway direction
                    return self.tr('Cannot infer directions for lines {0} and {1} (Right Angle)').format(key1.id(), key2.id())
        return

    def checkNodeValidity(self, node, connectedValidLines, hidLineLayer, geomType=None):
        """
        Checks if lines connected to a node have their flows compatible to node type and valid lines
        connected to it.
        :param node: (QgsPoint) node which lines connected to it are going to be verified.
        :param connectedValidLines: list of (QgsFeature) lines connected to 'node' that are already verified.
        :param hidLineLayer: (QgsVectorLayer) layer that contains the lines of analyzed network.
        :param geomType: (int) layer geometry type. If not given, it'll be evaluated OTF.
        :return: (str) if node is invalid, returns the invalidation reason string.
        """
        # getting flow permitions based on node type
        # reference is node (e.g. 'in' = lines  are ENDING at analyzed node)
        flowType = {
                    0 : None, # Flag
                    1 : 'in', # Sumidouro
                    2 : 'out', # Fonte D'Água
                    3 : 'in', # Interrupção à Jusante
                    4 : 'out', # Interrupção à Montante
                    5 : 'in and out', # Confluência
                    6 : 'in and out', # Ramificação
                    7 : 'in and out' # Mudança de Atributo
                   }
        # if node is introduced by operator's modification, it won't be saved to the layer
        if node not in self.nodeTypeDict.keys():
            # then it'll be introduced to the node type from database
            self.nodeTypeDict[node] = self.nodeCurrentTypeDict[node]
        flow = flowType[self.nodeTypeDict[node]]
        nodePointDict = self.nodeDict[node]
        # getting all connected lines to node that are not already validated
        linesNotValidated = list( set( nodePointDict['start']  + nodePointDict['end'] ) - set(connectedValidLines) )
        # starting dicts of valid and invalid lines
        validLines, invalidLines = dict(), dict()
        if not flow:
            # flags have all lines flagged
            reason = self.tr('Node was flagged upon classification.')
            for line in linesNotValidated:
                invalidLines[line.id()] = line
            return validLines, invalidLines, reason
        if not linesNotValidated:
            # if there are no lines to be validated, method returns None
            return validLines, invalidLines, ''
        # if 'geomType' is not given, it must be evaluated
        if not geomType:
            geomType = hidLineLayer.geometryType()
        # reason message in case of invalidity
        reason = ''
        for line in linesNotValidated:
            # getting last and initial node from analyzed line
            finalNode = self.getLastNode(lyr=hidLineLayer, feat=line, geomType=geomType)
            initialNode = self.getFirstNode(lyr=hidLineLayer, feat=line, geomType=geomType)
            # line ID
            lineID = line.id()
            # comparing extreme nodes to find out if flow is compatible to node type
            if flow == 'in':
                if node == finalNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
                        reason += self.tr('Line {0} does not end at a node with IN flow type (node type is {1}). ').format(lineID, self.nodeTypeDict[node])
            elif flow == 'out':
                if node == initialNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
                        reason += self.tr('Line {0} does not start at a node with OUT flow type (node type is {1}). ').format(lineID, self.nodeTypeDict[node])
            elif flow == 'in and out':
                if bool(len(nodePointDict['start'])) != bool(len(nodePointDict['end'])):
                    # if it's an 'in and out' flow and only one of dicts is filled, then there's an inconsistency
                    invalidLines[lineID] = line
                    thisReason = self.tr('Lines are either flowing only in or out of node. Node classification is {0}.'.format(self.nodeTypeDict[node]))
                    if thisReason not in reason:
                        reason += thisReason
                elif node in [initialNode, finalNode]:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
                        reason += self.tr('Line {0} seems to be invalid (unable to point specific reason). ').format(lineID)
        return  validLines, invalidLines, reason

    def getNodeTypeFromDb(self, nodeLayerName, hidrographyLineLayerName, nodeCrs, nodeList=None):
        """
        Returns a dictionary of node type as of database point of view.
        :param nodeLayerName: (str) layer name which feature owner of node point belongs to.
        :param hidrographyLineLayerName: (str) hidrography lines layer name from which node are created from.
        :param nodeCrs: (int) CRS for node layer (EPSG number).
        :param nodeList: a list of target node points (QgsPoint). If not given, dictNode keys will be read as node list.
        :return: (dict) node type according to database information.
        """
        nodeWkt, dbNTD, dbNodeTypeDict = dict(), dict(), dict()
        if not nodeList:
            nodeList = self.nodeDict.keys()
        for node in nodeList:
            # mapping WKT conversions
            # nodeGeom = binascii.hexlify(QgsGeometry.fromMultiPoint([node]).asWkb())
            # nodeWkt[nodeGeom] = node
            # nodeWkt[QgsGeometry().fromMultiPoint([node]).exportToWkt()] = node
            temp = self.abstractDb.getNodesGeometry([QgsGeometry().fromMultiPoint([node]).exportToWkt()], \
                    nodeLayerName, hidrographyLineLayerName, nodeCrs)
            if temp:
                dbNodeTypeDict[node] = temp.values()[0]
        # dbNTD = self.abstractDb.getNodesGeometry(nodeWkt.keys(), nodeLayerName, hidrographyLineLayerName, nodeCrs)
        # for nWkt in dbNTD.keys():
        #     if nWkt in nodeWkt.keys():
        #         # if node is not in original dict, it'll be ignored 
        #         dbNodeTypeDict[nodeWkt[nWkt]] = dbNTD[nWkt]
        return dbNodeTypeDict

    def getNodeDbIdFromNode(self, nodeLayerName, hidrographyLineLayerName, nodeCrs, nodeList=None):
        """
        Returns a dictionary of node type as of database point of view.
        :param nodeLayerName: (str) layer name which feature owner of node point belongs to.
        :param hidrographyLineLayerName: (str) hidrography lines layer name from which node are created from.
        :param nodeCrs: (int) CRS for node layer (EPSG number).
        :return: (dict) node ID according to database information.
        """
        nodeWkt, dbNTD, dbNodeIdDict = dict(), dict(), dict()
        if not nodeList:
            nodeList = self.nodeDict.keys()
        for node in nodeList:
            # mapping WKT conversions
            # nodeWkt[QgsGeometry().fromMultiPoint([node]).exportToWkt()] = node
            nWkt = QgsGeometry().fromMultiPoint([node]).exportToWkt()
            nodeId = self.abstractDb.getNodeId(nWkt, nodeLayerName, hidrographyLineLayerName, nodeCrs)
            dbNodeIdDict[node] = nodeId
        # dbNTD = self.abstractDb.getNodesGeometry(nodeWkt.keys(), nodeLayerName, hidrographyLineLayerName, nodeCrs)
        # for nWkt in dbNTD.keys():
        #     if nWkt in nodeWkt.keys():
        #         # if node is not in original dict, it'll be ignored 
        #         dbNodeTypeDict[nodeWkt[nWkt]] = dbNTD[nWkt]
        return dbNodeIdDict

    def getNextNodes(self, node, hidLineLayer, geomType=None):
        """
        It returns a list of all other nodes for each line connected to target node.
        :param node: (QgsPoint) node based on which next nodes will be gathered from. 
        :param hidLineLayer: (QgsVectorLayer) hidrography line layer.
        :return: a list of (QgsPoint) the other node of lines connected to given hidrography node.
        """
        if not geomType:
            geomType = hidLineLayer.geometryType()
        nextNodes = []
        nodePointDict = self.nodeDict[node]
        for line in nodePointDict['start']:
            # if line starts at target node, the other extremity is a final node
            nextNodes.append(self.getLastNode(lyr=hidLineLayer, feat=line, geomType=geomType))
        for line in nodePointDict['end']:
            # if line ends at target node, the other extremity is a initial node
            nextNodes.append(self.getFirstNode(lyr=hidLineLayer, feat=line, geomType=geomType))
        return nextNodes

    def checkAllNodesValidity(self, hidLineLyr, nodeCrs, nodeList=None):
        """
        For every node over the frame [or set as a line beginning], checks for network coherence regarding
        to previous node classification and its current direction. Method takes that bordering points are 
        correctly classified. CARE: 'nodeTypeDict' MUST BE THE ONE TAKEN FROM DATABASE, NOT RETRIEVED OTF.
        :param hidLineLyr: (QgsVectorLayer) hidrography lines layer from which node are created from.
        :param nodeCrs: (str) string containing node layer EPSG code. 
        :param nodeList: a list of target node points (QgsPoint). If not given, all nodeDict will be read.
        :return: (dict) flag dictionary ( { (QgsPoint) node : (str) reason } ), (dict) dictionaries ( { (int)feat_id : (QgsFeature)feat } ) of invalid and valid lines.
        """
        nodeOnFrame = [3, 4, 2] # node types that are over the frame contour and line BEGINNINGS
        deltaLinesCheckList = [5, 6] # nodes that have an unbalaced number ratio of flow in/out
        if not nodeList:
            # 'nodeList' must start with all nodes that are on the frame (assumed to be well directed)
            nodeList = []
            for node in self.nodeTypeDict.keys():
                if self.nodeTypeDict[node] in nodeOnFrame:
                    nodeList.append(node)
        # if no node on frame is found, process ends here
        if not nodeList:
            return None, None
        geomType = hidLineLyr.geometryType()
        # initiating the list of nodes already checked and the list of nodes to be checked next iteration
        visitedNodes, newNextNodes = [], []
        nodeFlags = dict()
        # starting dict of (in)valid lines to be returned by the end of method
        validLines, invalidLines = dict(), dict()
        while nodeList:
            for node in nodeList:
                if node not in visitedNodes:
                    # set node as visited
                    visitedNodes.append(node)
                # check coherence to node type and waterway flow
                val, inval, reason = self.checkNodeValidity(node=node, connectedValidLines=validLines.values(),\
                                                            hidLineLayer=hidLineLyr, geomType=geomType)
                # if node type test does have valid lines to iterate over
                validLines.update(val)
                invalidLines.update(inval)
                newNextNodes += self.getNextNodes(node=node, hidLineLayer=hidLineLyr, geomType=geomType)
                if inval:
                    if node not in nodeFlags.keys():
                        # if node is invalid, add to nodeFlagList
                        nodeFlags[node] = reason
                    else:
                        nodeFlags[node] += reason
                    # and remove next nodes connected to invalid lines
                    removeNode = []
                    for line in inval.values():
                        if line in self.nodeDict[node]['end']:
                            removeNode.append(self.getFirstNode(lyr=hidLineLyr, feat=line))
                        else:
                            removeNode.append(self.getLastNode(lyr=hidLineLyr, feat=line))
                    newNextNodes = list( set(newNextNodes) - set(removeNode) )
                # if node type is a ramification or a confluence, it checks validity by angles formed by their (last part of) lines
                if self.nodeTypeDict[node] in deltaLinesCheckList:
                    invalidationReason = self.validateDeltaLinesAng(node=node, hidLineLayer=hidLineLyr, geomType=geomType)
                    newNextNodesFromDeltaCheck = self.getNextNodes(node=node, hidLineLayer=hidLineLyr, geomType=geomType)
                    # if the line would be valid as per node type but it is invalid because of its angle, 
                    # it should be removed from valid list and all following nodes, should be removed 
                    # from next node sequence.
                    if invalidationReason:
                        for line in (self.nodeDict[node]['start'] + self.nodeDict[node]['end']):
                            # invalidating a possible false positive
                            validLines.pop(line.id(), None)
                            # remove false positive next nodes from the list of actual next nodes
                            newNextNodes = list( set(newNextNodes) - set(newNextNodesFromDeltaCheck) )
                        if node not in nodeFlags:
                            nodeFlags[node] = invalidationReason
                        else:
                            nodeFlags[node] += invalidationReason
                    else:
                        newNextNodes += newNextNodesFromDeltaCheck
            # remove nodes that were already visited
            newNextNodes = list( set(newNextNodes) - set(visitedNodes) )
            # if new nodes are detected, repeat for those
            nodeList = newNextNodes
            newNextNodes = []
        return nodeFlags, invalidLines, validLines

    def buildFlagList(self, nodeFlags, tableSchema, tableName, geometryColumn):
        """
        Builds record list from pointList to raise flags.
        :param nodeFlags:
        :param tableSchema:
        :param tableName:
        :param geometryColumn:
        :return:
        """
        recordList = []
        for node, reason in nodeFlags.iteritems():
            featid = self.nodeDbIdDict[node]
            geometry = binascii.hexlify(QgsGeometry.fromMultiPoint([node]).asWkb())
            recordList.append(('{0}.{1}'.format(tableSchema, tableName), featid, reason, geometry, geometryColumn))
        return recordList

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
            refKey = self.parameters['Reference and Layers'][0]
            classesWithElemKeys = self.parameters['Reference and Layers'][1]
            if len(classesWithElemKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            elif len(classesWithElemKeys) > 1:
                self.setStatus(self.tr('More than one class selected. Please select only the hidrography lines layer.'), 1) #Finished
                return 1
            else:
                hidLineLyrKey = classesWithElemKeys[0]
            if not refKey:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                return 1
            # preparing reference layer
            refcl = self.classesWithElemDict[refKey]
            frameLayer = self.loadLayerBeforeValidationProcess(refcl)
            # preparing hidrography lines layer
            hidcl = self.classesWithElemDict[hidLineLyrKey]
            trecho_drenagem = self.loadLayerBeforeValidationProcess(hidcl)
            # getting dictionaries of nodes information 
            frame = self.getFrameContour(frameLayer=frameLayer)
            self.nodeDict = self.identifyAllNodes(hidLineLayer=trecho_drenagem)
            crs = trecho_drenagem.crs().authid()
            # node layer has the same CRS as the hidrography lines layer
            nodeCrs = trecho_drenagem.crs().authid().split(':')[1]
            searchRadius = self.parameters['Search Radius']
            # getting current type for hidrography nodes as it is on screen now
            self.nodeCurrentTypeDict = self.classifyAllNodes(frameLyrContour=frame, searchRadius=self.parameters['Search Radius'])
            try:
                self.nodeTypeDict = self.getNodeTypeFromDb(nodeLayerName=self.hidNodeLayerName, hidrographyLineLayerName=trecho_drenagem.name(), nodeCrs=nodeCrs)
            except:
                pass
            if not self.nodeTypeDict:
                try:
                    self.nodeTypeDict = self.classifyAllNodes(frameLyrContour=frame, searchRadius=self.parameters['Search Radius'])
                    self.abstractDb.createHidNodeTable(crs.split(':')[1])
                    self.fillNodeTable(hidLineLayer=trecho_drenagem)
                except:
                    self.setStatus(self.tr('Could not create and load hidrography nodes layer.'), 1) #Finished
                    return 1
            self.nodeDbIdDict = self.getNodeDbIdFromNode(nodeLayerName=self.hidNodeLayerName, hidrographyLineLayerName=trecho_drenagem.name(), nodeCrs=nodeCrs)
            nodeFlags, inval, val = self.checkAllNodesValidity(hidLineLyr=trecho_drenagem, nodeCrs=nodeCrs)
            # getting recordList to be loaded to validation flag table
            recordList = self.buildFlagList(nodeFlags, 'validation', self.hidNodeLayerName, 'geom')
            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                msg = self.tr('{0} lines may be incorrectly directed. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('All lines are correctly directed.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
