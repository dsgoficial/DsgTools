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
        self.parameters = { 'Only Selected' : False, 'Snap' : 2.0 }
        self.nodeTypeExceptionsDict = {
                                        0 : 'Flag',
                                        1 : 'Fonte d\'Água',
                                        2 : 'Sumidouro',
                                        3 : 'Moldura'
                                       }

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
        :param frameLyrContour: bounding box for the frame layer to be checked.
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
        :param frameLyrContour: bounding box for the frame layer to be checked.
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
                    return 1
                # case 1.a.ii: waterway is flowing to mapped area (point over the frame has on line ending line(s))
                elif hasStartLine:
                    return 2
            # case 1.b: point that legitimately only flows from
            # case 1.c: point that legitimately only flows out
            # case 1.d: points that are not supposed to have one way flow (flags)
            return 0
        # case 2 "confluence"
        elif sizeFlowIn >= sizeFlowOut:
            return 3
        # case 3 "ramification"
        else:
            return 4
        
    def classifyAllNodes(self, dictNode, frameLyrContour, searchRadius, nodeList=None):
        """
        Classifies all nodes of features from a given layer.
        :param dictNode: dictionaty of flow in and out for each hidrography node to be classified.
        :param nodeList: a list of nodes (QgsPoint) to be classified. If not given, whole dict is going 
                         to be classified. Node MUST be in dict given, if not, it'll be ignored.
        :return: a dictionary of node and its node type (int) 
        """
        nodeTypeDict = dict()
        nodeKeys = dictNode.keys()
        if not nodeList:
            nodeList = nodeKeys
        for node in nodeList:
            if node not in nodeKeys:
                continue
            nodeTypeDict[node] = self.nodeType(nodePoint=node, dictStartingEndingLinesEntry=dictNode[node], \
                                               frameLyrContour=frameLyrContour, searchRadius=searchRadius)
        return nodeTypeDict

    def fillNodeTable(self, lyr, dictNode, frameLyrBoundingBox, searchRadius):
        """
        Method to populate validation.aux_validation_nodes_p with all nodes.
        :param lyr: layer which dictNode is created from.
        :param dictNode: dictionary containing info of all lines reaching from and to each node.
        """
        lyrName = lyr.name()
        crs = lyr.crs().authid().split(":")[1]
        for node in dictNode.keys():
            # classify points
            nodeType = self.nodeType(nodePoint=node, dictStartingEndingLinesEntry=dictNode[node], \
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

    def selectUpstreamLines(self, firstNode, lyr, dictNode, flipWrongLines=False):
        """
        Selects all lines that are upstream from a initial node (should be an ending point) and returns a list of
        lines with possible wrong flow direction.
        :param firstNode: initial node point target of all flow comparison.
        :param flipWrongLines: if set True, it'll flip all lines that may have wrong flow
        """
        if not isinstance(firstNode, list):
            initNode = [firstNode]
        else:
            initNode = firstNode
        geomType = lyr.geometryType()
        selection, flippedLines, newInitNode = [], [], []
        # it's an iteractive method. Each iteration, initNode resets to the ending of last lines
        while initNode:
            for node in initNode:
                # lines that flow from a starting point are wrong
                wrongFlow = dictNode[node]['start']
                rightFlow = dictNode[node]['end']
                if wrongFlow:
                    for feat in wrongFlow:
                        if feat.id() in selection:
                            continue
                        # ADD FILTERING CONDITIONS IN HERE! (E.G. FONTE D'ÁGUA)                        
                        fn = self.getLineLastNode(lyr, feat, geomType)
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
                        fn = self.getLineInitialNode(lyr, feat, geomType)
                        newInitNode.append(fn)
                        selection.append(feat.id())
            # check new starts up to no new starts are found
            initNode = newInitNode
            newInitNode = [] # new list of initial node(s)
        lyr.removeSelection()
        lyr.startEditing()
        lyr.setSelectedFeatures(selection)
        # update flipped lines representation on canvas
        self.iface.mapCanvas().refresh()
        return flippedLines

    def selectDownstreamLines(self, firstNode, lyr, dictNode, flipWrongLines=False):
        """
        Selects all lines that are downstream from a initial node (should be a starting point) and returns a list of
        lines with possible wrong flow direction.
        :param initNode: initial node point target of all flow comparison.
        :param flipWrongLines: if set True, it'll flip all lines that may have wrong flow.        
        """
        if not isinstance(firstNode, list):
            initNode = [firstNode]
        else:
            initNode = firstNode
        geomType = lyr.geometryType()
        selection, flippedLines, newInitNode = [], [], []
        # it's an iteractive method. Each iteration, initNode resets to the ending of last lines
        while initNode:
            for node in initNode:
                # lines that flow from an ending point are wrong
                wrongFlow = dictNode[node]['end']
                rightFlow = dictNode[node]['start']
                if wrongFlow:
                    for feat in wrongFlow:
                        if feat.id() in selection:
                            continue
                        # ADD FILTERING CONDITIONS IN HERE! (E.G. FONTE D'ÁGUA)                        
                        fn = self.getLineInitialNode(lyr, feat, geomType)
                        # flip wrong lines
                        if flipWrongLines:
                            self.DsgGeometryHandler.flipFeature(lyr, feat, geomType)
                        newInitNode.append(fn)
                        flippedLines.append(feat.id())
                        selection.append(feat.id())                        
                if rightFlow:
                    # if lines end there, then they are connected and flowing that way
                    for feat in rightFlow:
                        if feat.id() in selection:
                            continue
                        fn = self.getLineLastNode(lyr, feat, geomType)
                        newInitNode.append(fn)
                        selection.append(feat.id())
            # check new starts up to no new starts are found
            initNode = newInitNode
            newInitNode = [] # new list of initial node(s)
        lyr.removeSelection()
        lyr.startEditing()
        lyr.setSelectedFeatures(selection)
        # update flipped lines representation on canvas
        self.iface.mapCanvas().refresh()
        return flippedLines

    def execute(self):
        # PARÂMETROS PARA TESTE
        frame, pt_drenagem, trecho_drenagem = None, None, None
        searchRadius = 2.0
        for lyer in self.canvas.layers():
            if lyer.name() == 'aux_moldura_a':
                frameLayer = lyer
                frame = [feat for feat in lyer.getFeatures()]
                frame = frame[0]
            elif lyer.name() == 'aux_hid_nodes_p':
                pt_drenagem = lyer
            elif lyer.name() == 'hid_trecho_drenagem_l':
                trecho_drenagem = lyer
            elif trecho_drenagem and pt_drenagem and frame:
                break
        frame = self.DsgGeometryHandler.getFeatureNodes(frameLayer, frame)
        frame = QgsGeometry().fromPolyline(frame[0][0])
        d = self.identifyAllNodes(trecho_drenagem)
        crs = trecho_drenagem.crs().authid()
        for feat in pt_drenagem.selectedFeatures():
            n = feat.geometry().asMultiPoint()
        # # TESTE DE SELEÇÃO DE UPSTREAM
        # print self.selectUpstreamLines(n, trecho_drenagem, d)
        # # TESTE DE SELEÇÃO DE DOWNSTREAM
        print self.selectDownstreamLines(n, trecho_drenagem, d)
        # # TESTE DE POPULAÇÃO DAS TABELAS
        # self.abstractDb.createHidNodeTable(crs.split(':')[1])
        # print self.fillNodeTable(trecho_drenagem, d, frame, searchRadius)
        # # TESTE DE CLASSIFICAÇÃO DOS NÓS
        # print self.classifyAllNodes(d, frame, searchRadius)
        # if self.parameters['Only Selected']:
