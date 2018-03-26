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
        self.parameters = {'Only Selected' : True}
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
                pInit = QgsFeature()
                pInit.setGeometry(QgsGeometry.fromPoint(nodes[0]))
                # final node
                pEnd = QgsFeature()
                pEnd.setGeometry(QgsGeometry.fromPoint(nodes[-1]))
                # filling starting node information into dictionary
                if pInit not in nodeDict.keys():
                    # if the point is not already started into dictionary, it creates a new item
                    nodeDict[pInit] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pInit]['start']:
                    nodeDict[pInit]['start'].append(feat)                            
                # filling ending node information into dictionary
                if pEnd not in nodeDict.keys():
                    nodeDict[pEnd] = { 'start' : [], 'end' : [] }
                if feat not in nodeDict[pInit]['start']:
                    nodeDict[pEnd]['start'].append(feat)
        return nodeDict

    def setNodeType(self, nodePoint, dictStartingEndingLines, frameLayer=''):
        """
        Sets the node type given all lines that flows from and to it.
        :param nodePoint: point to be classified.
        :param dictStartingEndingLines: dict of { 'start' : [lines], 'end' : [lines] }
        :return: returns the point type.
        """
        sizeFlowIn = len(dictStartingEndingLines['start'])
        sizeFlowOut = len(dictStartingEndingLines['end'])
        hasStartLine = bool(sizeFlowIn)
        hasEndLine = bool(sizeFlowOut)
        # "exclusive or"
        startXORendLine = (hasStartLine != hasEndLine)
        # case 1: all lines either flow in or out 
        if startXORendLine:
            # case 1.a: point is over the frame
            return 1, 0, 0
        elif sizeFlowIn >= sizeFlowOut:
            # case 2 "confluence"
            return 0, 1, 0
        else:
            # case 3 "ramification"
            return 0, 0, 1
        
    def classifyAllNodes(self, lyr):
        """
        Classifies all nodes of features from a given layer.
        :param lyr: target layer to which nodes identification is required.
        """
        c1, c2, c3 = 0, 0, 0
        dictNode = self.identifyAllNodes(lyr)
        for node in dictNode.keys():
            r1, r2, r3 = self.setNodeType(node, dictNode[node])
            c1 += r1
            c2 += r2
            c3 += r3
        print c1, c2, c3

    def fillNodeTable(self, dictNode):
        """
        Method to populate validation.aux_validation_nodes_p with all nodes.
        :param dictNode: dictionary containing info of all lines reaching from and to each node.
        """
        pass

    def getLineLastNode(self, lyr, feat, geomType=None):
        """
        Returns the ending point of a line.
        :param lyr: layer containing target feature.
        :param feat: feature which last node is requested.
        :param geomType: int regarding to layer geometry type (1 for lines).
        """
        n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=geomType)
        isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
        n = n[0] if isMulti else n
        lastNode = QgsFeature()
        lastNode.setGeometry(QgsGeometry.fromPoint(n[-1]))
        return lastNode

    def selectUpstreamLines(self, initNode, lyr, dictNode):
        """
        Selects all lines that are upstream from a initial node and returns a list of lines with
        possible wrong flow direction.
        :param initNode: initial node point target of all flow comparison. 
        """
        initNode = [initNode]
        geomType = lyr.geometryType()
        selection = flippedLines = []
        # it's an iteractive method. Each iteration, initNode resets to the ending of last lines
        while initNode:
            for node in initNode:
                newInitNode = [] # new list of initial node(s)
                wrongFlow = dictNode[node]['start']
                if wrongFlow:
                    # if point is supposed to be downward, points starting there have the wrong flow                    
                    for feat in wrongFlow:
                        # flip feature direction with wrong flow
                        # ADD FILTERING CONDITIONS IN HERE! (E.G. FONTE D'ÁGUA)
                        self.DsgGeometryHandler.flipFeature(lyr, feat, geomType)
                        flippedLines.append(feat)
                        # after flipped, get last node
                        ln = self.getLineLastNode(lyr, feat, geomType)
                        newInitNode.append(ln)
                rightFlow = dictNode[node]['end']
                if rightFlow:
                    # if lines end there, then they are connected and flowing there
                    selection += rightFlow + wrongFlow
                # all the endings are now new starts
                for feat in rightFlow:
                    ln = self.getLineLastNode(lyr, feat, geomType)
                    newInitNode.append(ln)
            # check new starts up to no new starts are found
            initNode = newInitNode
        lyr.removeSelection()
        lyr.startEditting()
        lyr.setSelectedFeatures(selection)
        return flippedLines

    def execute(self):
        lyr = self.iface.activeLayer()
        d = self.identifyAllNodes(lyr)
        for feat in lyr.selectedFeatures():
            n = self.DsgGeometryHandler.getFeatureNodes(layer=lyr, feature=feat, geomType=1)
            isMulti = QgsWKBTypes.isMultiType(int(lyr.wkbType()))
            n = n[0] if isMulti else n
            initNode = QgsFeature()
            initNode.setGeometry(QgsGeometry.fromPoint(n[0]))
        self.selectUpstreamLines(initNode, lyr, d)
