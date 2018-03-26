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
        print nodeDict

    def setNodeType(self, nodePoint, dictStartingEndingLines, frameLayer=''):
        """
        Sets the node type given all lines that flows from and to it.
        :param nodePoint: point to be classified.
        :param dictStartingEndingLines: dict of { 'start' : [lines], 'end' : [lines] }
        :return: returns the point type.
        """
        hasStartLine = bool(dictStartingEndingLines['start'])
        hasEndLine = bool(dictStartingEndingLines['end'])
        # "exclusive or"
        startXORendLine = (hasStartLine != hasEndLine)
        # case 1: all lines either flow in or out 
        if startXORendLine:
            # case 1.a: point is over the frame
            pass


    def fillNodeTable(self, dictNode):
        """
        Method to populate validation.aux_validation_nodes_p with all nodes.
        :param dictNode: dictionary containing info of all lines reaching from and to each node.
        """
        pass

    def execute(self):
        lyr = self.iface.activeLayer()
        self.identifyAllNodes(lyr)
