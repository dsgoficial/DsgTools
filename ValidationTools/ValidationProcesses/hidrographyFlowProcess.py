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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsWKBTypes
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
import processing, binascii
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler
from DsgTools.ValidationTools.ValidationProcesses.identifyDanglesProcess import IdentifyDanglesProcess
from datetime import datetime

class HidrographyFlowProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(HidrographyFlowProcess, self).__init__(postgisDb, iface, instantiating)
        self.nodeDict = dict()
        self.canvas = self.iface.mapCanvas()
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        self.danglesClass = IdentifyDanglesProcess(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Hidrography Network Directioning')
        self.parameters = { 'Only Selected' : False, 'Snap' : 2.0, 'Search Radius' : 5.0 }
        self.nodeTypeExceptionsDict = {
                                        0 : 'Flag',
                                        1 : 'Fonte d\'Água',
                                        2 : 'Sumidouro',
                                        3 : 'Moldura'
                                       }
        self.firstExec = True # TEMPORÁRIO, SÓ PARA OS TESTES
        # mounting node and node type dict
        frame, frameLayer, trecho_drenagem, pt_drenagem = self.getHidrographyLayers()
        self.nodeDict = self.identifyAllNodes(trecho_drenagem)
        self.nodeTypeDict = self.classifyAllNodes(self.nodeDict, frame, self.parameters['Search Radius'])
        print 'OBJETO REINICIADO'

    def getHidrographyLayers(self):
        """
        Read layers from canvas as returns frame contour and frame hidrography lines and 
        hidrgrography node layers.
        :return: frame contour, frame layer, hidrography lines layer, hidrography node layer
        """
        frame, frameLayer, trecho_drenagem, pt_drenagem = None, None, None, None        
        for lyer in self.canvas.layers():
            if lyer.name() == 'aux_moldura_a':
                frameLayer = lyer
                # getting frame contour (as a PolyLine feature)
                frame = [feat for feat in lyer.getFeatures()]
                frame = frame[0]
                frame = self.DsgGeometryHandler.getFeatureNodes(frameLayer, frame)
                frame = QgsGeometry().fromPolyline(frame[0][0])
            elif lyer.name() == 'aux_hid_nodes_p':
                pt_drenagem = lyer
            elif lyer.name() == 'hid_trecho_drenagem_l':
                trecho_drenagem = lyer
            elif trecho_drenagem and pt_drenagem and frame:
                break
        return frame, frameLayer, trecho_drenagem, pt_drenagem

    def identifyAllNodes(self, lyr):
        """
        Identifies all nodes from a given layer (or selected features of it). The result is returned as a dict of dict.
        :param lyr: target layer to which nodes identification is required.
        :return: { node_id : { start : [feature_id_Which_Starts_with_node], end : feature_id_Which_Ends_with_node } }.
        """
        nodeDict = dict()
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
        if self.parameters['Only Selected']:
            features = lyr.selectedFeatures()
        else:
            features = [feat for feat in lyr.getFeatures()]
        for feat in features:
            nodes = self.DsgGeometryHandler.getFeatureNodes(lyr, feat)
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
        """
        qgisPoint = QgsGeometry.fromPoint(node)
        # buildgin a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1).boundingBox().asWktPolygon()
        buf = QgsGeometry.fromWkt(buf)
        return buf.intersects(frameLyrContour)
        
    def nodeType(self, nodePoint, dictStartingEndingLinesEntry, frameLyrContour, searchRadius):
        """
        Sets the node type given all lines that flows from and to it.
        :param nodePoint: point to be classified.
        :param dictStartingEndingLinesEntry: dict of { 'start' : [lines], 'end' : [lines] }.
        :param frameLyrContour: (QgsGeometry) border line for the frame layer to be checked.
        :return: returns the point type.
        """
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
                # case 1.a.i: waterway is flowing away from mapped area (point over the frame has on line ending line(s))
                if hasEndLine:
                    return 3
                # case 1.a.ii: waterway is flowing to mapped area (point over the frame has on line ending line(s))
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
        # case 2 "confluence"
        elif sizeFlowIn >= sizeFlowOut:
            return 5
        # case 3 "ramification"
        else:
            return 6
        
    def classifyAllNodes(self, nodeDict, frameLyrContour, searchRadius, nodeList=None):
        """
        Classifies all nodes of features from a given layer.
        :param nodeDict: dictionaty of flow in and out for each hidrography node to be classified.
        :param nodeList: a list of nodes (QgsPoint) to be classified. If not given, whole dict is going 
                         to be classified. Node MUST be in dict given, if not, it'll be ignored.
        :return: a dictionary of node and its node type (int) 
        """
        nodeTypeDict = dict()
        nodeKeys = nodeDict.keys()
        if not nodeList:
            nodeList = nodeKeys
        for node in nodeList:
            if node not in nodeKeys:
                continue
            nodeTypeDict[node] = self.nodeType(nodePoint=node, dictStartingEndingLinesEntry=nodeDict[node], \
                                               frameLyrContour=frameLyrContour, searchRadius=searchRadius)
        return nodeTypeDict

    def fillNodeTable(self, lyr, nodeDict, frameLyrBoundingBox, searchRadius):
        """
        Method to populate validation.aux_validation_nodes_p with all nodes.
        :param lyr: layer which nodeDict is created from.
        :param nodeDict: dictionary containing info of all lines reaching from and to each node.
        """
        lyrName = lyr.name()
        crs = lyr.crs().authid().split(":")[1]
        for node in nodeDict.keys():
            # classify points
            nodeType = self.nodeType(nodePoint=node, dictStartingEndingLinesEntry=nodeDict[node], \
                                             frameLyrContour=frameLyrBoundingBox, searchRadius=searchRadius)
            # get node geometry as wkt for database loading
            nWkt = QgsGeometry().fromMultiPoint([node]).exportToWkt()
            # if node is loaded into database, the following method returns True
            if self.abstractDb.insertHidValNode(layerName=lyrName, node=nWkt, nodeType=nodeType, crs=crs):
                continue
            else:
                return False
        return True

    def getLineLastNode(self, lyr, feat, geomType=None):
        """
        Returns the ending point of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which last node is requested.
        :param geomType: int regarding to layer geometry type (1 for lines).
        :return: ending node point (QgsPoint).
        """
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][-1]
        return n[-1]

    def getLineInitialNode(self, lyr, feat, geomType=None):
        """
        Returns the starting point of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which initial node is requested.
        :param geomType: int regarding to layer geometry type (1 for lines).
        :return: starting node point (QgsPoint).
        """
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
        if isMulti:
            if len(n) > 1:
                return
            return n[0][0]
        return n[0]

    def selectUpDownstreamLines(self, firstNode, lyr, nodeDict, direction, ignoreWrongFlow=False, flipWrongLines=False, ignoreSelection=False):
        """
        Selects all lines that are upstream or downstream from an initial node and returns a list of
        lines with possible wrong flow direction.
        :param firstNode: initial node point target of all flow comparison.
        :param lyr: layer containing target nodes.
        :param direction: indication whether code is looking for 'downstream' or 'upstream'.
        :param nodeDict: dictionary containing info of all lines reaching from and to each node.
        :param ignoreWrongFlow: if set True, code will not set selection on 'wrong flowing lines'.
        :param flipWrongLines: if set True, it'll flip all lines that may have wrong flow.
        :param ignoreSelection: if True, method will not select any lines.
        """
        if not isinstance(firstNode, list):
            initNode = [firstNode]
        else:
            initNode = firstNode
        geomType = lyr.geometryType()
        selection, flippedLines, newInitNode = [], [], []
        upstream = (direction.lower() == 'upstream')
        downstream = (direction.lower() == 'downstream')
        if not upstream and not downstream:
            # if no VALID direction is given, nothing is done
            return
        # it's an iteractive method. Each iteration, initNode resets to the ending of last lines
        while initNode:
            for node in initNode:
                if upstream:
                    # lines that flow to a starting point are wrong
                    wrongFlow = nodeDict[node]['start']
                    rightFlow = nodeDict[node]['end']
                elif downstream:
                    # lines that flow from an ending point are wrong
                    wrongFlow = nodeDict[node]['end']
                    rightFlow = nodeDict[node]['start']
                if wrongFlow:
                    for feat in wrongFlow:
                        if feat.id() in selection:
                            continue
                        # ADD FILTERING CONDITIONS IN HERE! (E.G. FONTE D'ÁGUA)                        
                        if upstream:
                            fn = self.getLineLastNode(lyr, feat, geomType)
                        elif downstream:
                            fn = self.getLineInitialNode(lyr, feat, geomType)
                        # flip wrong lines
                        if flipWrongLines:
                            self.DsgGeometryHandler.flipFeature(lyr, feat, geomType)
                        newInitNode.append(fn)
                        flippedLines.append(feat.id())
                        selection.append(feat.id())                      
                if rightFlow:
                    # if lines end there, then they are connected and flowing that way
                    # all the endings are now new starts
                    for feat in rightFlow:
                        if feat.id() in selection:
                            continue
                        if upstream:
                            fn = self.getLineInitialNode(lyr, feat, geomType)
                        elif downstream:
                            fn = self.getLineLastNode(lyr, feat, geomType)
                        newInitNode.append(fn)
                        selection.append(feat.id())
            # check new starts up to no new starts are found
            initNode = newInitNode
            newInitNode = [] # new list of initial node(s)
        if ignoreWrongFlow:
            # remove flagged lines from selection
            selection = list(set(selection) - set(flippedLines))
        if not ignoreSelection:
            lyr.removeSelection()
            lyr.startEditing()
            lyr.setSelectedFeatures(selection)
        # update flipped lines representation on canvas
        self.iface.mapCanvas().refresh()
        return flippedLines

    def getBlackListFeatures(self, nodeDict, nodeTypeDict, nodeList=None):
        """
        Gets all features directly connected to "strong" nodes.
        Strong nodes are: water fountains or sinks and all nodes over frame (up or downstream).
        :return: a list of feature ids that are not supposed to have their course changed.
        """
        # codes for blacklisted types of nodes
        nodeTypeBl = [1, 2, 3, 4]
        featBl = []
        if not nodeList:
            nodeList = nodeDict.keys()
        for node in nodeList:
            featureList = nodeDict[node]['start'] + nodeDict[node]['end']
            for feat in featureList:
                if nodeTypeDict[node] not in nodeTypeBl:
                    continue
                # if node has blacklisted type, it'll be added to the list
                featBl.append(feat.id())
        return featBl

    def checkNodeValidity(self, node, nodeType, nodePointDict, connectedValidLines, lyr, geomType=None, returnNextNodes=True):
        """
        Checks if lines connected to a node have their flows compatible to node type and valid lines
        connected to it.
        :param node: node (QgsPoint) which lines connected to it are going to be verified.
        :param nodeType: (int) node type of target node.
        :param nodePointDict: dictionary for starting and ending lines into given node. ({ 'start' : [lines], 'end' : [lines] })
        :param connectedValidLines: list of lines (QgsFeatures) connected to 'node' that are already verified.
        :param lyr: lyr that contains analyzed node.
        :param geomType: layer geometry type. If not given, it'll be evaluated OTF.
        :param returnNextNodes: (bool) indicates whether method should return next nodes or not.
        :return: if 'returnNextNodes' is given, method returns a list of nodes connected to verified node.
        """
        # getting flow permitions based on node type
        # reference is node (e.g. 'in' = lines  are ENDING at analyzed node)
        flowType = {
                    1 : 'in', # Sumidouro
                    2 : 'out', # Fonte D'Água
                    3 : 'in', # Interrupção à Jusante
                    4 : 'out', # Interrupção à Montante
                    5 : 'in and out', # Confluência
                    6 : 'in and out' # Ramificação
                   }
        flow = flowType[nodeType]
        # getting all connected lines to node that are not validated
        linesNotValidated = list( set( nodePointDict['start']  + nodePointDict['end'] ) - set(connectedValidLines) )
        if not linesNotValidated:
            # if there are no lines to be validated, method returns None
            return
        # if 'geomType' is not given, it must be evaluated
        if not geomType:
            geomType = lyr.geometryType()
        # starting dicts of valid and invalid lines
        validLines, invalidLines = dict(), dict()
        # list of next nodes
        nextNodes = []
        for line in linesNotValidated:
            # getting last and initial node from analyzed line
            finalNode = self.getLineLastNode(lyr=lyr, feat=line, geomType=geomType)
            initialNode = self.getLineInitialNode(lyr=lyr, feat=line, geomType=geomType)
            # line ID
            lineID = line.id()
            # comparing extreme nodes to find out if flow is compatible to node type
            if flow == 'in':
                if node == finalNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                        nextNodes.append(initialNode)
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
            elif flow == 'out':
                if node == initialNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                        nextNodes.append(finalNode)
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
            elif flow == 'in and out':
                if node in [initialNode, finalNode]:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                        if node == initialNode:
                            nextNodes.append(finalNode)
                        else:
                            nextNodes.append(initialNode)
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
        if returnNextNodes:
            return validLines, invalidLines, nextNodes
        return  validLines, invalidLines


    def getFlagsForAllFrameNodes(self, lyr, nodeDict, nodeTypeDict, nodeList=None, blacklist=True, flipWrongLines=False, ignoreWrongFlow=False, ignoreSelection=True):
        """
        Gets all possible wrong flow lines to be treated. If blacklist argument is given,
        list will be filtered with blacklisted lines, according to current modelling rules.
        """
        frameNodeTypes = [3, 4]
        flagLineList = []
        if not nodeList:
            nodeList = nodeDict.keys()
        featBlackList = self.getBlackListFeatures(nodeDict=nodeDict, nodeTypeDict=nodeTypeDict,\
                                                  nodeList=nodeList)
        for node in nodeList:
            if nodeTypeDict[node] not in frameNodeTypes:
                continue
            # if node is on frame, we add to flags all pointed lines to be flipped that are not blacklisted
            elif nodeTypeDict[node] == 3:
                # if waterway is 'going outside' of mapped region, we want to get all upstream lines
                direction = 'upstream'
            elif nodeTypeDict[node] == 4:
                # if waterway is 'going inside' of mapped region, we want to get all downstream lines
                direction = 'downstream'
            flagCandidates = self.selectUpDownstreamLines(firstNode=node, lyr=lyr, nodeDict=nodeDict, \
                                                          direction=direction, ignoreWrongFlow=ignoreWrongFlow, \
                                                          flipWrongLines=flipWrongLines, ignoreSelection=ignoreSelection)
            flagLineList += flagCandidates
        flagLineList = list(set(flagLineList) - set(featBlackList))
        return flagLineList

    def execute(self):
        # PARÂMETROS PARA TESTE
        searchRadius = self.parameters['Search Radius']
        frame, frameLayer, trecho_drenagem, pt_drenagem = self.getHidrographyLayers()        
        d = self.nodeDict
        dNodeType = self.nodeTypeDict
        crs = trecho_drenagem.crs().authid()
        for feat in pt_drenagem.selectedFeatures():
           n = feat.geometry().asMultiPoint()
           n = n[0] if isinstance(n, list) else n
        geomType = trecho_drenagem.geometryType()
        # # TESTE DE SELEÇÃO DE UPSTREAM
        # print self.selectUpstreamLines(n, trecho_drenagem, d)
        # # TESTE DE SELEÇÃO DE DOWNSTREAM
        # print self.selectUpDownstreamLines(n, trecho_drenagem, d, 'downstream', ignoreWrongFlow=True, flipWrongLines=False)
        # # TESTE DE POPULAÇÃO DAS TABELAS
        # self.abstractDb.createHidNodeTable(crs.split(':')[1])
        # print self.fillNodeTable(trecho_drenagem, d, frame, searchRadius)
        # self.iface.mapCanvas().refresh()
        # # TESTE DE CLASSIFICAÇÃO DOS NÓS
        # nodeTypeDict = self.classifyAllNodes(d, frame, searchRadius)
        # if self.parameters['Only Selected']:
        # # TESTE DE FLAGS DE DIRECIONAMENTO
        # flagList = self.getFlagsForAllFrameNodes(lyr=trecho_drenagem, nodeDict=d, nodeTypeDict=dNodeType)
        # print len(flagList)
        # trecho_drenagem.removeSelection()
        # trecho_drenagem.startEditing()
        # trecho_drenagem.setSelectedFeatures(flagList)
        # # TESTE DE CHECK POR NÓ
        val, inval, nextNodes = self.checkNodeValidity(n, dNodeType[n], d[n], [], trecho_drenagem, geomType)
        trecho_drenagem.setSelectedFeatures(val.keys())
        print 'Invalids: ', inval, 'Nodes: ', nextNodes
