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

class HidrographyFlowProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.nodeDict = dict()
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        self.processAlias = self.tr('Hidrography Network Directioning')
        self.parameters = { 'Only Selected' : False }
        self.dictNodeType = {
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

    def nodeOnFrame(self, nodeGeom, frameLyr):
        """
        Identify whether or not node is over the frame. Returns True if point is over the frame and false if
        node is not on frame. If identification fails, returns 'None'.
        :param node: QgsGeometry to be identified as over the frame layer or not.
        :param frameLyr: QgsVectorLayer frame layer to be checked.        
        """
        pass

    def nodeType(self, nodePoint, dictStartingEndingLinesEntry, frameLayer=''):
        """
        Sets the node type given all lines that flows from and to it.
        :param nodePoint: point to be classified.
        :param dictStartingEndingLinesEntry: dict of { 'start' : [lines], 'end' : [lines] }.
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
            # case 1.b: point that legimately only flows from
            # case 1.c: point that legimately only flows out
            # case 1.d: points that are not supposed to have one way flow (flags)
            return 0
        # case 2 "confluence"
        elif sizeFlowIn >= sizeFlowOut:
            return 1
        # case 3 "ramification"
        else:
            return 2
        
    def classifyAllNodes(self, lyr):
        """
        Classifies all nodes of features from a given layer. NÃO IRÁ FICAR
        :param lyr: target layer to which nodes identification is required.
        """
        c1, c2, c3 = 0, 0, 0
        dictNode = self.identifyAllNodes(lyr)
        for node in dictNode.keys():
            r1, r2, r3 = self.nodeType(node, dictNode[node])
            c1 += r1
            c2 += r2
            c3 += r3
        print c1, c2, c3

    def fillNodeTable(self, lyr, dictNode):
        """
        Method to populate validation.aux_validation_nodes_p with all nodes.
        :param lyr: layer which dictNode is created from.
        :param dictNode: dictionary containing info of all lines reaching from and to each node.
        """
        lyrName = lyr.name()
        crs = lyr.crs().authid().split(":")[1]
        for node in dictNode.keys():
            nodeType = self.nodeType(nodePoint=node, dictStartingEndingLinesEntry=dictNode[node])
            nWkt = QgsGeometry().fromMultiPoint([node]).exportToWkt()
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

    def selectUpstreamLines(self, firstNode, lyr, dictNode):
        """
        Selects all lines that are upstream from a initial node (it's an ending point) and returns a list of
        lines with possible wrong flow direction.
        :param initNode: initial node point target of all flow comparison. 
        """
        if not isinstance(firstNode, list):
            initNode = [firstNode]
        geomType = lyr.geometryType()
        selection = flippedLines = []
        # it's an iteractive method. Each iteration, initNode resets to the ending of last lines
        while initNode:
            for node in initNode:
                newInitNode = [] # new list of initial node(s)
                # lines that flow from an ending point are wrong
                wrongFlow = dictNode[node]['start']
                rightFlow = dictNode[node]['end']
                if wrongFlow:
                    # if point is supposed to be downward, points starting there have the wrong flow                    
                    for feat in wrongFlow:
                        if feat.id() in selection:
                            continue
                        # ADD FILTERING CONDITIONS IN HERE! (E.G. FONTE D'ÁGUA)                        
                        fn = self.getLineLastNode(lyr, feat, geomType)
                        # flip wrong lines
                        self.DsgGeometryHandler.flipFeature(lyr, feat, 1)                        
                        newInitNode.append(fn)
                        selection.append(feat.id())
                        flippedLines.append(feat.id())                
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
        # update flipped lines representation on canvas
        self.iface.mapCanvas().refresh()
        lyr.removeSelection()
        lyr.startEditing()
        lyr.setSelectedFeatures(selection)
        return flippedLines

    def execute(self):
        lyr = self.iface.activeLayer()
        d = self.identifyAllNodes(lyr)
        crs = lyr.crs().authid()
        for feat in lyr.selectedFeatures():
            n = self.getLineLastNode(lyr, feat, 1)
        print self.selectUpstreamLines(n, lyr, d)
        # self.abstractDb.createHidNodeTable(crs.split(':')[1])
        # print self.fillNodeTable(lyr, d)
