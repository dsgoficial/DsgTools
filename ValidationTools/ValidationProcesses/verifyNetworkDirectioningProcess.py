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

from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsFeature, QgsWKBTypes, QgsRectangle, \
                      QgsFeatureRequest, QgsExpression
from PyQt4.QtGui import QMessageBox

import binascii, math
from collections import OrderedDict
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.ValidationTools.ValidationProcesses.hidrographyFlowProcess import HidrographyFlowParameters
from DsgTools.ValidationTools.ValidationProcesses.createNetworkNodesProcess import CreateNetworkNodesProcess
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

class VerifyNetworkDirectioningProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Class constructor.
        :param postgisDb: (DsgTools.AbstractDb) postgis database connection.
        :param iface: (QgisInterface) QGIS interface object.
        :param instantiating: (bool) indication of whether class is being instatiated.
        """
        super(VerifyNetworkDirectioningProcess, self).__init__(postgisDb, iface, instantiating)        
        self.processAlias = self.tr('Verify Network Directioning')
        self.canvas = self.iface.mapCanvas()
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        if not self.instantiating:
            # get an instance of network node creation method class object
            self.createNetworkNodesProcess = CreateNetworkNodesProcess(postgisDb=postgisDb, iface=iface, instantiating=True)
            # get standard node table name as of in the creation method class  
            self.hidNodeLayerName = self.createNetworkNodesProcess.hidNodeLayerName
            # checks whether node table exists and if it is filled
            if not self.abstractDb.checkIfTableExists('validation', self.hidNodeLayerName):
                QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr('No node table was found into chosen database. (Did you run Create Network Nodes process?)'))
                return
            # adjusting process parameters
            self.networkClassesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            networkFlowParameterList = HidrographyFlowParameters(self.networkClassesWithElemDict.keys())
            self.nodeClassesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['p'], withElements=True, excludeValidation = False)
            nodeFlowParameterList = HidrographyFlowParameters(self.nodeClassesWithElemDict.keys())            
            self.parameters = {
                                self.tr('Only Selected') : False,
                                self.tr('Network Layer') : networkFlowParameterList,
                                self.tr('Node Layer') : nodeFlowParameterList,
                                self.tr('Search Radius') : 5.0,
                                self.tr('Select All Valid Lines') : False,
                                self.tr('Allow Automatic Fixes') : True,
                                self.tr('Consider Dangles as Waterway Beginnings') : True
                              }
            # transmit these parameters to CreateNetworkNodesProcess object
            self.createNetworkNodesProcess.parameters = self.parameters
            self.nodeIdDict = None
            self.nodeDict = None
            self.nodeTypeDict = None
            # retrieving types from node creation object
            self.nodeTypeNameDict = self.createNetworkNodesProcess.nodeTypeNameDict

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

    def validateDeltaLinesAng(self, node, networkLayer, geomType=None):
        """
        Validates a set of lines connected to a node as for the angle formed between them.
        :param node: (QgsPoint) hidrography node to be validated.
        :param networkLayer: (QgsVectorLayer) hidrography line layer.
        :return: (str) if node is invalid, returns the reason of invalidation .
        """
        if not geomType:
            geomType = networkLayer.geometryType()
        azimuthDict = self.calculateAzimuthFromNode(node=node, networkLayer=networkLayer, geomType=None)
        for idx1, key1 in enumerate(azimuthDict.keys()):
            if idx1 == len(azimuthDict.keys()):
                # if first comparison element is already the last feature, all differences are already computed
                break
            for idx2, key2 in enumerate(azimuthDict.keys()):
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
                        return self.tr('Lines {0} and {1} have conflicting directions ({2:.2f} deg).').format(key1.id(), key2.id(), absAzimuthDifference)
                elif absAzimuthDifference != 90:
                    # if it's any other disposition, lines can have the same orientation
                    continue
                else:
                    # if lines touch each other at a right angle, then it is impossible to infer waterway direction
                    return self.tr('Cannot infer directions for lines {0} and {1} (Right Angle)').format(key1.id(), key2.id())
        return

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
                        reason = self.tr('Lines {0} and {1} have conflicting directions ({2:.2f} deg).').format(key1.id(), key2.id(), absAzimuthDifference)
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
                    CreateNetworkNodesProcess.Flag : None, # 0 - Flag (fim de trecho sem 'justificativa espacial')
                    CreateNetworkNodesProcess.Sink : 'in', # 1 - Sumidouro
                    CreateNetworkNodesProcess.WaterwayBegin : 'out', # 2 - Fonte D'Água
                    CreateNetworkNodesProcess.DownHillNode : 'in', # 3 - Interrupção à Jusante
                    CreateNetworkNodesProcess.UpHillNode : 'out', # 4 - Interrupção à Montante
                    CreateNetworkNodesProcess.Confluence : 'in and out', # 5 - Confluência
                    CreateNetworkNodesProcess.Ramification : 'in and out', # 6 - Ramificação
                    CreateNetworkNodesProcess.AttributeChange : 'in and out', # 7 - Mudança de Atributo
                    CreateNetworkNodesProcess.NodeNextToWaterBody : 'in or out', # 8 - Nó próximo a corpo d'água
                    CreateNetworkNodesProcess.AttributeChangeFlag : None, # 9 - Nó de mudança de atributos conectado em linhas que não mudam de atributos
                    CreateNetworkNodesProcess.ConstantFlowNode : 'in and out' # 10 - Há igual número de linhas (>1 para cada fluxo) entrando e saindo do nó
                    # CreateNetworkNodesProcess.NodeOverload : None # 10 - Mais 
                   }
        # if node is introduced by operator's modification, it won't be saved to the layer
        if node not in self.nodeTypeDict.keys() and not self.unclassifiedNodes:
            self.unclassifiedNodes = True
            QMessageBox.warning(self.iface.mainWindow(), self.tr('Error!'), self.tr('There are unclassified nodes! Node (re)creation process is recommended before this process.'))
            return None, None, None
        flow = flowType[self.nodeTypeDict[node]]
        nodePointDict = self.nodeDict[node]
        # getting all connected lines to node that are not already validated
        linesNotValidated = list( set( nodePointDict['start']  + nodePointDict['end'] ) - set(connectedValidLines) )
        # starting dicts of valid and invalid lines
        validLines, invalidLines = dict(), dict()
        if not flow:
            # flags have all lines flagged
            if self.nodeTypeDict[node] == CreateNetworkNodesProcess.Flag:
                reason = self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
            elif self.nodeTypeDict[node] == CreateNetworkNodesProcess.AttributeChangeFlag:
                id1, id2 = self.nodeDict[node]['start'][0].id(), self.nodeDict[node]['end'][0].id()
                reason = self.tr('Redundant node. Connected lines ({0}, {1}) share the same set of attributes.').format(id1, id2)
            # elif self.nodeTypeDict[node] == CreateNetworkNodesProcess.NodeOverload:
            #     reason = self.tr('Node is overloaded. Check acquisition norms. If more than 3 lines is valid for your project, ignore flag.')
            for line in linesNotValidated:
                invalidLines[line.id()] = line
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
                        reason += self.tr('Line {0} does not end at a node with IN flow type (node type is {1}). ').format(lineID, self.nodeTypeDict[node])
            elif flow == 'out':
                if node == initialNode:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                        invalidLines[lineID] = line
                        reason += self.tr('Line {0} does not start at a node with OUT flow type (node type is {1}). ')\
                        .format(lineID, self.nodeTypeNameDict[self.nodeTypeDict[node]])
            elif flow == 'in and out':
                if bool(len(nodePointDict['start'])) != bool(len(nodePointDict['end'])):
                    # if it's an 'in and out' flow and only one of dicts is filled, then there's an inconsistency
                    invalidLines[lineID] = line
                    thisReason = self.tr('Lines are either flowing only in or out of node. Node classification is {0}.'\
                    .format(self.nodeTypeNameDict[self.nodeTypeDict[node]]))
                    if thisReason not in reason:
                        reason += thisReason
                elif node in [initialNode, finalNode]:
                    if lineID not in validLines.keys():
                        validLines[lineID] = line
                elif lineID not in invalidLines.keys():
                    invalidLines[lineID] = line
                    reason += self.tr('Line {0} seems to be invalid (unable to point specific reason). ').format(lineID)
            elif flow == 'in or out':
                # these nodes can either be a waterway beginning or end
                # No invalidation reasons were thought at this point...
                if lineID not in validLines.keys():
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
            deltaLinesCheckList = [CreateNetworkNodesProcess.Confluence, CreateNetworkNodesProcess.Ramification] # nodes that have an unbalaced number ratio of flow in/out
        # check coherence to node type and waterway flow
        val, inval, reason = self.checkNodeTypeValidity(node=node, connectedValidLines=connectedValidLines,\
                                                    networkLayer=networkLayer, geomType=geomType)
        # checking angle validity
        if self.nodeTypeDict[node] in deltaLinesCheckList:
            # check for connected lines angles coherence
            val2, inval2, reason2 = self.validateDeltaLinesAngV2(node=node, networkLayer=networkLayer, connectedValidLines=connectedValidLines, geomType=geomType)
            # if any invalid line was validated on because of node type, it shall be moved to invalid dict
            if inval2:
                # remove any validated line in this iteration
                for lineId, line in inval2.iteritems():
                    val.pop(lineId, None)
                # insert into invalidated dict
                inval.update(inval2)
                # updates reason
                if reason:
                    reason = ". ".join([reason, reason2])
                else:
                    reason = reason2
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

    def checkAllNodesValidity(self, networkLayer, nodeList=None):
        """
        For every node over the frame [or set as a line beginning], checks for network coherence regarding
        to previous node classification and its current direction. Method takes that bordering points are 
        correctly classified. CARE: 'nodeTypeDict' MUST BE THE ONE TAKEN FROM DATABASE, NOT RETRIEVED OTF.
        :param networkLayer: (QgsVectorLayer) hidrography lines layer from which node are created from.
        :param nodeList: a list of target node points (QgsPoint). If not given, all nodeDict will be read.
        :return: (dict) flag dictionary ( { (QgsPoint) node : (str) reason } ), (dict) dictionaries ( { (int)feat_id : (QgsFeature)feat } ) of invalid and valid lines.
        """
        startingNodeTypes = [CreateNetworkNodesProcess.DownHillNode, CreateNetworkNodesProcess.UpHillNode, CreateNetworkNodesProcess.WaterwayBegin] # node types that are over the frame contour and line BEGINNINGS
        deltaLinesCheckList = [CreateNetworkNodesProcess.Confluence, CreateNetworkNodesProcess.Ramification] # nodes that have an unbalaced number ratio of flow in/out
        if not nodeList:
            # 'nodeList' must start with all nodes that are on the frame (assumed to be well directed)
            nodeList = []
            for node in self.nodeTypeDict.keys():
                if self.nodeTypeDict[node] in startingNodeTypes:
                    nodeList.append(node)
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
        flippedLinesIds, mergedLinesString = [], "" 
        while nodeList:
            for node in nodeList:
                if node not in visitedNodes:
                    # set node as visited
                    visitedNodes.append(node)
                # check coherence to node type and waterway flow
                val, inval, reason = self.checkNodeValidity(node=node, connectedValidLines=validLines.values(),\
                                                            networkLayer=networkLayer, deltaLinesCheckList=deltaLinesCheckList, geomType=geomType)
                # nodes to be removed from next nodes
                removeNode = []
                # if a reason is given, then node is invalid (even if there are no invalid lines connected to it).
                if reason:
                    # try to fix node issues
                    # note that val, inval and reason MAY BE MODIFIED - and there is no problem...
                    flippedLinesIds_, mergedLinesString_ = self.fixNodeFlagsNew(node=node, valDict=val, invalidDict=inval, reason=reason, \
                                                                            connectedValidLines=validLines.values(), networkLayer=networkLayer, \
                                                                            geomType=geomType, deltaLinesCheckList=deltaLinesCheckList)
                    # keep track of all modifications made
                    if flippedLinesIds_:
                        # IDs not registered yet will be added to final list
                        addIds = set(flippedLinesIds_) - set(flippedLinesIds)
                        # IDs that are registered will be removed (flipping a flipped line returns to original state)
                        removeIds = set(flippedLinesIds_) - addIds
                        flippedLinesIds = list( (set(flippedLinesIds) - removeIds) ) + list( addIds  )
                    if mergedLinesString_:
                        if not mergedLinesString:
                            mergedLinesString = mergedLinesString_
                        else:
                            ", ".join([mergedLinesString, mergedLinesString_])
                    # if node is still invalid, add to nodeFlagList and add/update its reason
                    if reason:
                        if node not in nodeFlags.keys():
                            nodeFlags[node] = reason
                        else:
                            nodeFlags[node] += "; " + reason
                    # get next nodes connected to invalid lines
                    for line in inval.values():
                        if line in self.nodeDict[node]['end']:
                            removeNode.append(self.getFirstNode(lyr=networkLayer, feat=line))
                        else:
                            removeNode.append(self.getLastNode(lyr=networkLayer, feat=line))
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

    def checkAllNodesValidityOld(self, networkLayer, nodeList=None):
        """
        For every node over the frame [or set as a line beginning], checks for network coherence regarding
        to previous node classification and its current direction. Method takes that bordering points are 
        correctly classified. CARE: 'nodeTypeDict' MUST BE THE ONE TAKEN FROM DATABASE, NOT RETRIEVED OTF.
        :param networkLayer: (QgsVectorLayer) hidrography lines layer from which node are created from.
        :param nodeList: a list of target node points (QgsPoint). If not given, all nodeDict will be read.
        :return: (dict) flag dictionary ( { (QgsPoint) node : (str) reason } ), (dict) dictionaries ( { (int)feat_id : (QgsFeature)feat } ) of invalid and valid lines.
        """
        startingNodeTypes = [CreateNetworkNodesProcess.DownHillNode, CreateNetworkNodesProcess.UpHillNode, CreateNetworkNodesProcess.WaterwayBegin] # node types that are over the frame contour and line BEGINNINGS
        if not nodeList:
            # 'nodeList' must start with all nodes that are on the frame (assumed to be well directed)
            nodeList = []
            for node in self.nodeTypeDict.keys():
                if self.nodeTypeDict[node] in startingNodeTypes:
                    nodeList.append(node)
        # if no node to start the process is found, process ends here
        if not nodeList:
            return None, None, self.tr("No network starting point was found")
        geomType = networkLayer.geometryType()
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
                val, inval, reason = self.checkNodeTypeValidity(node=node, connectedValidLines=validLines.values(),\
                                                            networkLayer=networkLayer, geomType=geomType)
                # if node type test does have valid lines to iterate over
                validLines.update(val)
                invalidLines.update(inval)
                newNextNodes += self.getNextNodes(node=node, networkLayer=networkLayer, geomType=geomType)
                # if a reason is given, then node is invalid (even if there are no invalid lines connected to it).
                if reason:
                    if node not in nodeFlags.keys():
                        # if node is invalid, add to nodeFlagList
                        nodeFlags[node] = reason
                    else:
                        nodeFlags[node] += reason
                    # and remove next nodes connected to invalid lines
                    removeNode = []
                    for line in inval.values():
                        if line in self.nodeDict[node]['end']:
                            removeNode.append(self.getFirstNode(lyr=networkLayer, feat=line))
                        else:
                            removeNode.append(self.getLastNode(lyr=networkLayer, feat=line))
                    newNextNodes = list( set(newNextNodes) - set(removeNode) )
                # if node type is a ramification or a confluence, it checks validity by angles formed by their (last part of) lines
                if self.nodeTypeDict[node] in deltaLinesCheckList:
                    invalidationReason = self.validateDeltaLinesAng(node=node, networkLayer=networkLayer, geomType=geomType)
                    newNextNodesFromDeltaCheck = self.getNextNodes(node=node, networkLayer=networkLayer, geomType=geomType)
                    # if the line would be valid as per node type but it is invalid because of its angle, 
                    # it should be removed from valid list and all following nodes, should be removed 
                    # from next node sequence.
                    if invalidationReason:
                        for line in (self.nodeDict[node]['start'] + self.nodeDict[node]['end']):
                            # invalidating a possible false positive
                            validLines.pop(line.id(), None)
                            # remove false positive next nodes from the list of actual next nodes
                            newNextNodes = list( set(newNextNodes) - set(newNextNodesFromDeltaCheck) )
                        if node not in nodeFlags.keys():
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
        :param nodeFlags: (dict) dictionary containing invalid node and its reason ( { (QgsPoint) node : (str) reason } )
        :param tableSchema: (str) name of schema containing hidrography node table.
        :param tableName: (str) name of hidrography node table.
        :param geometryColumn: (str) name of geometric column on table.
        :return: ( list-of- ( (str)feature_identification, (int)feat_id, (str)invalidation_reason, (hex)geometry, (str)geom_column ) ) list of invalidations found.
        """
        recordList = []
        countNodeNotInDb = 0
        for node, reason in nodeFlags.iteritems():
            if self.nodeIdDict[node] is not None:
                featid = self.nodeIdDict[node]
            else:
                # if node is not previously classified on database, but then motivates a flag, it should appear on Flags list
                featid = -9999
                countNodeNotInDb += 1
            geometry = binascii.hexlify(QgsGeometry.fromMultiPoint([node]).asWkb())
            recordList.append(('{0}.{1}'.format(tableSchema, tableName), featid, reason, geometry, geometryColumn))
        if countNodeNotInDb:
            # in case there are flagged nodes that are not loaded in DB, user is notified
            msg = self.tr('There are {0} flagged nodes that were introduced to network. Node reclassification is indicated.').format(countNodeNotInDb)
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        return recordList

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
        for r in fixableReasonExcertsDict.keys():
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
            # self.tr('Line {0} does not end at a node with IN flow type (node type is {1}). ')
            # self.tr('Line {0} does not start at a node with OUT flow type (node type is {1}). ')
            return [reason.split(self.tr(" does"))[0].split(" ")[1]]
        elif reasonType == 3:
            # Line before being built: self.tr('Lines {0} and {1} have conflicting directions ({2:.2f} deg).')
            lineId1 = reason.split(self.tr(" and "))[0].split(" ")[1]
            lineId2 = reason.split(self.tr(" and "))[1].split(" ")[0]
            return [lineId1, lineId2]
        elif reasonType == 4:
            # Line before being built: self.tr('Redundant node. Connected lines ({0}, {1}) share the same set of attributes.')
            lineId1 = reason.split(self.tr(", "))[0].split("(")[1]
            lineId2 = reason.split(self.tr(", "))[1].split(")")[0]
            return [lineId1, lineId2]

    # method for automatic fix
    def isDangle(self, node, networkLayer, searchRadius):
        """
        Checks whether node is a dangle into network (connected to a first order line).
        :param node: (QgsPoint) node to be validated.
        :param networkLayer: (QgsVectorLayer) network layer (line layer).
        :param searchRadius: (float) limit distance to another line.
        :return: (bool) indication whether node is a dangle.
        """
        qgisPoint = QgsGeometry.fromPoint(node)
        # building a buffer around node with search radius for intersection with Layer Frame
        buf = qgisPoint.buffer(searchRadius, -1).boundingBox().asWktPolygon()
        buf = QgsGeometry.fromWkt(buf)
        # building bounding box around node for feature requesting
        bbRect = QgsRectangle(node.x()-searchRadius, node.y()-searchRadius, node.x()+searchRadius, node.y()+searchRadius)
        # check if buffer intersects features from water bodies layers
        count = 0
        for feat in networkLayer.getFeatures(QgsFeatureRequest(bbRect)):
            if buf.intersects(feat.geometry()):
                count += 1
                res = (count > 1)
                if res:
                    # to avoid as many iterations as possible
                    return res
        return res

    def flipSingleLine(self, line, layer, geomType=None):
        """
        Flips a given single line.
        :param line: (QgsFeature) line to be flipped.
        :param layer: (QgsVectorLayer) layer containing target feature.
        :param geomType: (int) layer geometry type code.
        """
        self.DsgGeometryHandler.flipFeature(layer=layer, feature=line, geomType=geomType)

    def fixNodeFlagsNew(self, node, valDict, invalidDict, reason, connectedValidLines, networkLayer, geomType=None, deltaLinesCheckList=None):
        """
        Tries to fix issues flagged on node
        """
        # initiate lists of lines that were flipped/merged
        flippedLinesIds, mergedLinesString = [], ""
        # get reason type
        reasonType = self.getReasonType(reason=reason)
        if not reasonType:
            # if node invalidation reason is not among the fixable ones, method stops here.
            return flippedLinesIds, mergedLinesString
        ## try to fix node issues
        featIdFlipCandidates = self.getLineIdFromReason(reason=reason, reasonType=reasonType)
        if reasonType in [1, 2]:
            # original message: self.tr('Line {0} does not end at a node with IN flow type (node type is {1}). ')
            # original message: self.tr('Line {0} does not start at a node with OUT flow type (node type is {1}). ')
            for lineId in featIdFlipCandidates:
                line = invalidDict[int(lineId)]
                if line not in connectedValidLines:
                    # only non-valid lines may be modified
                    self.flipSingleLine(line=line, layer=networkLayer, geomType=geomType)
                    # if a line is flipped it must be changed in self.nodeDict
                    # getting first and last nodes
                    first = self.getFirstNode(lyr=networkLayer, feat=line, geomType=geomType)
                    last = self.getLastNode(lyr=networkLayer, feat=line, geomType=geomType)
                    self.createNetworkNodesProcess.changeLineDict(nodeList=[first, last], line=line)
                    # update this nodeDict with the one from createNetworkNodesProcess object
                    self.nodeDict[node] = self.createNetworkNodesProcess.nodeDict[node]
                    flippedLinesIds.append(lineId)
        elif reasonType == 3:
            pass
        elif reasonType == 4:
            pass
        elif reasonType == 5:
            pass
        else:
            # in case, for some reason, an strange value is given to reasonType
            return False
        # check if node is fixed and update its dictionaries and invalidation reason
        valDict, invalidDict, reason = self.checkNodeValidity(node=node, connectedValidLines=connectedValidLines, \
                                        networkLayer=networkLayer, geomType=geomType, deltaLinesCheckList=deltaLinesCheckList)
        return flippedLinesIds, mergedLinesString

    def logAlteredFeatures(self, flippedLines, mergedLinesString):
        """
        Logs the list of flipped/merged lines, if any.
        :param flippedLines: (list-of-int) list of flipped lines.
        :param mergedLinesString: (str) text containing all merged lines (in the form of 'ID1 to ID2, ID3, to ID4')
        :return: (bool) whether or not a message was shown.
        """
        # building warning message
        warning = ''
        if flippedLines and mergedLinesString:
            warning = self.tr("Lines that were flipped while directioning hidrography lines: {0}\n").format(",".join(flippedLines))
            warning += self.tr("Lines that were merged while directioning hidrography lines: {0}\n").format(",".join(mergedLinesString))
        elif flippedLines:
            warning = self.tr("Lines that were flipped while directioning hidrography lines: {0}\n").format(", ".join(flippedLines))
        elif mergedLinesString:
            warning = self.tr("Lines that were merged while directioning hidrography lines: {0}\n").format(", ".join(mergedLinesString))
        if warning:
            # warning is only raised when there were flags fixed
            warning = self.tr('\n{0}: Flipped/Merged Lines\n{1}').format(self.processAlias, warning)
            QgsMessageLog.logMessage(warning, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return True
        return False

    # method for automatic fix
    def fixNodeFlags(self, nodeFlags, networkLayer, geomType=None):
        """
        Tries to fix the flag raised.
        :param nodeFlags: (dict) dictionary containing invalid node and its reason ( { (QgsPoint) node : (str) reason } ).
        :param networkLayer: (QgsVectorLayer) layer containing network lines.
        :param geomType: (int) geometry type of network lines layer.
        :return: (dict) dictionary containing invalid node and its reason ( { (QgsPoint) node : (str) reason } ).
        """
        # IDs from features to be flipped and to be merged
        lineIdsForFlipping, mergedLinesString = [], []
        fixedFlags = dict()
        if not geomType:
            geomType = networkLayer.geometryType()
        for node, reason in nodeFlags.iteritems():
            reasonType = self.getReasonType(reason=reason)
            if not reasonType:
                # skip node if it's not fixable (reason type 0)
                continue
            featIdFlipCandidates = self.getLineIdFromReason(reason=reason, reasonType=reasonType)
            if reasonType in [1, 2]:
                # if it's a line flowing the wrong way, they will be flipped
                lineIdsForFlipping += featIdFlipCandidates
            elif reasonType == 3:
                # in case there are conflicting lines and one of them must be flipped
                if len(self.nodeDict[node]['start']) > len(self.nodeDict[node]['end']):
                    # the line to be flipped is in the largest dict, given that confluence/ramification points would turn
                    # into sinks/water sources
                    checkFeatIdList = [str(f.id()) for f in self.nodeDict[node]['start']]
                else:
                    checkFeatIdList = [str(f.id()) for f in self.nodeDict[node]['end']]
                if featIdFlipCandidates[0] in checkFeatIdList:
                    lineIdsForFlipping += [featIdFlipCandidates[0]]
                else:
                    lineIdsForFlipping += [featIdFlipCandidates[1]]
                # add them to return dict in order to not lose track of fixed problems
                fixedFlags[node] = reason
            elif reasonType == 4:
                # case where lines do not change attribute but there is a network node between them
                line_b = self.nodeDict[node]['end'][0]
                line_a = self.nodeDict[node]['start'][0]
                self.DsgGeometryHandler.mergeLines(line_a=line_a, line_b=line_b, layer=networkLayer)
                mergedLinesString += [self.tr('{0} to {1}').format(line_b.id(), line_a.id())]
                fixedFlags[node] = reason
            elif reasonType == 5 and self.parameters[self.tr('Consider Dangles as Waterway Beginnings')]:
                # case where node is not a sink not a node next to water body and has an "in" flow
                if len(self.nodeDict[node]['end']) == 1 and self.createNetworkNodesProcess.isDangle(node=node, networkLayer=networkLayer, searchRadius=self.parameters[self.tr('Search Radius')]):
                    # only dangles are considered waterway beginnings
                    lineIdsForFlipping.append(str(self.nodeDict[node]['end'][0].id()))
        for node in fixedFlags.keys():
            # pop it from original dict
            nodeFlags.pop(node, None)
        flipFeatureListIterator = networkLayer.getFeatures(QgsFeatureRequest(QgsExpression('id in ({0})'.format(', '.join(lineIdsForFlipping)))))
        networkLayer.startEditing()
        networkLayer.beginEditCommand('Merging lines')
        for feat in flipFeatureListIterator:
            # flip every feature indicated as a fixable flag
            if self.checkBlackListLine(layer=networkLayer, line=feat):
                lineIdsForFlipping.remove(str(feat.id()))
            else:
                self.DsgGeometryHandler.flipFeature(layer=networkLayer, feature=feat, geomType=geomType)
        networkLayer.endEditCommand()
        # building warning message
        warning = ''
        if lineIdsForFlipping and mergedLinesString:
            warning = self.tr("Lines that were flipped while directioning hidrography lines: {0}\n").format(",".join(lineIdsForFlipping))
            warning += self.tr("Lines that were merged while directioning hidrography lines: {0}\n").format(",".join(mergedLinesString))
        elif lineIdsForFlipping:
            warning = self.tr("Lines that were flipped while directioning hidrography lines: {0}\n").format(", ".join(lineIdsForFlipping))
        elif mergedLinesString:
            warning = self.tr("Lines that were merged while directioning hidrography lines: {0}\n").format(", ".join(mergedLinesString))
        if warning:
            # warning is only raised when there were flags fixed
            warning = self.tr('\n{0}: Flipped/Merged Lines\n{1}').format(self.processAlias, warning)
            QgsMessageLog.logMessage(warning, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        return fixedFlags

    # method for automatic fix
    def checkBlackListLine(self, layer, line, blackList=None):
        """
        Checks whether line is connected to a waterway beginning.
        :param layer: (QgsVectorLayer) layer containing target line.
        :param line: (QgsFeature) line to be checked if is mutable or not.
        :param blackList: (list-of-int) list of all blacklisted types
        :return: (bool) whether or not line is considered always well directed, regardless of other lines.
        """
        if not blackList:
            blackList = [CreateNetworkNodesProcess.DownHillNode, CreateNetworkNodesProcess.UpHillNode, CreateNetworkNodesProcess.Sink]
        first = self.getFirstNode(lyr=layer, feat=line, geomType=1)
        last = self.getLastNode(lyr=layer, feat=line, geomType=1)
        return bool((self.nodeTypeDict[first]  in blackList) or (self.nodeTypeDict[last] in blackList))

    # method for automatic fix
    def recursiveFixFlags(self, nodeFlags, networkLayer, geomType=None, maximumCycles=9):
        """
        Runs the fixing method for as long as flags are found and being fixed, or maximum cycles isn't reached.
        :param nodeFlags: (dict) dictionary of nodes and their invalidation reasons { (QgsPoint)node : (str)reason }. MAY BE MODIFIED.
        :param networkLayer: (QgsVectorLayer) layer containig network lines.
        :param geomType: (int) network lines layer geometry type.
        :param maximumCycles: (int) maximum amount of fixing cycles (-1, as first iteration is off-loop) per process execution.
        :return: (dict) dictionary of flags that were fixed and their reasons.
        """
        if not geomType:
            geomType = networkLayer.geometryType()
        # get first fix
        fixedFlags = self.fixNodeFlags(nodeFlags=nodeFlags, networkLayer=networkLayer, geomType=geomType)
        if not fixedFlags:
            # in case method didn't fix any flags
            return fixedFlags
        newFixedFlags = fixedFlags
        # update nodes classification if there are any fixed nodes
        # self.abstractDb.clearHidNodeTable(self.hidNodeLayerName)
        # self.fillNodeTable(networkLayer=networkLayer)
        count = 0
        while count < maximumCycles or newFixedFlags:
            newNodeFlags, inval, val = self.checkAllNodesValidity(networkLayer=networkLayer)
            newFixedFlags = self.fixNodeFlags(nodeFlags=nodeFlags, networkLayer=networkLayer, geomType=geomType)
            # every cycle implies in a new node reclassification as nodes have changed their types on canvas
            # self.abstractDb.clearHidNodeTable(self.hidNodeLayerName)
            # self.fillNodeTable(networkLayer=networkLayer)
            if newNodeFlags.keys() in nodeFlags.keys():
                # in case a subset of flags is raised again by process, fixing method is no longer effective 
                # thus no fixing method will be applied
                break
            if newFixedFlags:
                # in case the fixed flags are the same as before
                if not list( set(newFixedFlags.keys()) -  set(fixedFlags.keys()) ):
                    break
            else:
                # in case there are no new fixed flags
                break
            # adds newly fixed flags to dict
            fixedFlags.update(newFixedFlags)
            # in case fixing method isn't effective and fix doesn't really fix it
            for node in newNodeFlags.keys():
                if node in fixedFlags.keys():
                    # remove it from fixed nodes list
                    fixedFlags.pop(node)
            # cycle has finished
            count += 1
        for node in fixedFlags.keys():
            # remove all fixed flags from flags dict
            if node in nodeFlags.keys():
                nodeFlags.pop(node)
        return fixedFlags

    def getNodeTypeDictFromNodeLayer(self, networkNodeLayer):
        """
        Get all node info (dictionaries for start/end(ing) lines and node type) from node layer.
        :param networkNodeLayer: (QgsVectorLayer) network node layer.
        :return: (tuple-of-dict) node type dict and node id dict, respectively
        """
        nodeTypeDict, nodeIdDict = dict(), dict()
        isMulti = QgsWKBTypes.isMultiType(int(networkNodeLayer.wkbType()))
        for feat in networkNodeLayer.getFeatures():
            if isMulti:
                node = feat.geometry().asMultiPoint()[0]                    
            else:
                node = feat.geometry().asPoint()
            nodeTypeDict[node] = feat['node_type']
            nodeIdDict[node] = feat['id']
        return nodeTypeDict, nodeIdDict

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
            hidNodeLyrKey = self.parameters[self.tr('Node Layer')]
            # remake the key from standard string
            k = ('{},{},{},{},{}').format(
                                        hidNodeLyrKey.split('.')[0],\
                                        hidNodeLyrKey.split('.')[1].split(r' (')[0],\
                                        hidNodeLyrKey.split('(')[1].split(', ')[0],\
                                        hidNodeLyrKey.split('(')[1].split(', ')[1],\
                                        hidNodeLyrKey.split('(')[1].split(', ')[2].replace(')', '')
                                        )
            nodecl = self.nodeClassesWithElemDict[k]
            # getting network lines and nodes layers
            networkNodeLayer = self.loadLayerBeforeValidationProcess(nodecl)
            networkLayer = self.loadLayerBeforeValidationProcess(hidcl)
            crs = networkLayer.crs().authid()
            # node layer has the same CRS as the hidrography lines layer
            nodeSrid = networkLayer.crs().authid().split(':')[1]
            searchRadius = self.parameters['Search Radius']
            # getting node info from network node layer
            self.nodeDict = self.createNetworkNodesProcess.identifyAllNodes(networkLayer=networkLayer)
            # update createNetworkNodesProcess object node dictionary
            self.createNetworkNodesProcess.nodeDict = self.nodeDict
            self.nodeTypeDict, self.nodeIdDict = self.getNodeTypeDictFromNodeLayer(networkNodeLayer=networkNodeLayer)
            # validation method FINALLY starts...
            nodeFlags, inval, val = self.checkAllNodesValidity(networkLayer=networkLayer)
            # start recursive method in case flags are raised
            if self.parameters[self.tr('Allow Automatic Fixes')] and nodeFlags:
                # this method alters database classification, hence it can only be used with it selected
                fixedFlags = self.recursiveFixFlags(nodeFlags=nodeFlags, networkLayer=networkLayer)
                # update node info
                # self.createNetworkNodesProcess.clearHidNodeLayer(nodeLayer=networkLayer, nodeList=self.nodeIdDict.values())
                self.nodeDict = self.createNetworkNodesProcess.identifyAllNodes(networkLayer=networkLayer)
                # self.nodeTypeDict, self.nodeIdDict = self.getNodeTypeDictFromNodeLayer(networkNodeLayer=networkNodeLayer)
            # if there are no starting nodes into network, a warning is raised
            if not isinstance(val, dict):
                # in that case method checkAllNodesValidity() returns None, None, REASON
                QMessageBox.warning(self.iface.mainWindow(), self.tr('Error!'), self.tr('No initial node was found!'))
                self.finishedWithError()
                return 0
            # if user set to select valid lines
            if self.parameters[self.tr('Select All Valid Lines')]:
                networkLayer.setSelectedFeatures(val.keys())
            # getting recordList to be loaded to validation flag table
            recordList = self.buildFlagList(nodeFlags, 'validation', self.hidNodeLayerName, 'geom')
            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                if self.parameters[self.tr('Only Selected')]:
                    percValid = float(len(val))*100.0/float(len(networkLayer.selectedFeatures()))
                else:
                    percValid = float(len(val))*100.0/float(networkLayer.featureCount())
                msg = self.tr('{0} nodes may be invalid ({1:.2f}' + '%' +  'of network is well directed). Check flags.')\
                            .format(numberOfProblems, percValid)
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.INFO)
            else:
                msg = self.tr('Network has coherent directions.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
