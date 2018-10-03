# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-03
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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
from ...algRunner import AlgRunner
from ....dsgEnums import DsgEnums
import processing
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProject,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDistance,
                       QgsProcessingException)

class VerifyNetworkDirectioningAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = 'NETWORK_LAYER'
    NODE_LAYER = 'NODE_LAYER'
    SINK_LAYER = 'SINK_LAYER'
    REF_LAYER = 'REF_LAYER'
    WATER_BODY_LAYER = 'WATER_BODY_LAYER'
    MAX_CYCLES = 'MAX_CYCLES'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    SELECT_ALL_VALID = 'SELECT_ALL_VALID'
    FLAGS = 'FLAGS'
    LINE_FLAGS = 'LINE_FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NETWORK_LAYER,
                self.tr('Network layer'),
                [ QgsProcessing.TypeVectorLine ]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NODE_LAYER,
                self.tr('Node layer'),
                [ QgsProcessing.TypeVectorPoint ]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.REF_LAYER,
                self.tr('Reference layer'),
                [ QgsProcessing.TypeVectorPoint ]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SINK_LAYER,
                self.tr('Water sink layer'),
                [ QgsProcessing.TypeVectorPoint ],
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.WATER_BODY_LAYER,
                self.tr('Water body layers'),
                QgsProcessing.TypeVectorPolygon
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_CYCLES,
                self.tr('Maximum cycles'),
                minValue=1,
                defaultValue=2,
                type=QgsProcessingParameterNumber.Integer
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.TOLERANCE, 
                self.tr('Snap radius'), 
                parentParameterName=self.INPUT,                                         
                minValue=0, 
                defaultValue=1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr('Search radius'),
                minValue=0,
                defaultValue=1,
                type=QgsProcessingParameterNumber.Double
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECT_ALL_VALID,
                self.tr('Select all valid lines after the process')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('Network node errors on {0}').format(self.displayName())
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr('Line errors on {0}').format(self.displayName())
            )
        )
        self.nodeIdDict = None
        self.nodeDict = None
        self.nodeTypeDict = None
        self.nodeTypeNameDict = {
                                    DsgEnums.Flag : self.tr("Flag"),
                                    DsgEnums.Sink : self.tr("Sink"),
                                    DsgEnums.WaterwayBegin : self.tr("Waterway Beginning"),
                                    DsgEnums.UpHillNode : self.tr("Up Hill Node"),
                                    DsgEnums.DownHillNode : self.tr("Down Hill Node"),
                                    DsgEnums.Confluence : self.tr("Confluence"),
                                    DsgEnums.Ramification : self.tr("Ramification"),
                                    DsgEnums.AttributeChange : self.tr("Attribute Change Node"),
                                    DsgEnums.NodeNextToWaterBody : self.tr("Node Next to Water Body"),
                                    DsgEnums.AttributeChangeFlag : self.tr("Attribute Change Flag"),
                                    DsgEnums.NodeOverload : self.tr("Overloaded Node"),
                                    DsgEnums.DisconnectedLine : self.tr("Disconnected From Network")
                                }
        self.nodesToPop = []

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        # get network layer
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        if networkLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NETWORK_LAYER))
        # get network node layer
        networkNodeLayer = self.parameterAsLayer(parameters, self.NODE_LAYER, context)
        if networkLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NODE_LAYER))
        networkNodeLayer.startEditing()
        # get water sink layer
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        # get frame layer
        frameLayer = self.parameterAsLayer(parameters, self.REF_LAYER, context)
        if frameLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REF_LAYER))
        frame = self.createNetworkNodesProcess.getFrameOutterBounds(frameLayer=frameLayer) #mudar
        
        # get search radius
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        networkLayerGeomType = networkLayer.geometryType()

        self.nodeDict = self.createNetworkNodesProcess.identifyAllNodes(networkLayer=networkLayer)
        # declare reclassification function from createNetworkNodesProcess object - parameter is [node, nodeTypeDict] 
        self.classifyNode = lambda x : self.createNetworkNodesProcess.nodeType(nodePoint=x[0], networkLayer=networkLayer, frameLyrContourList=frame, \
                                    waterBodiesLayers=waterBodyClasses, searchRadius=searchRadius, waterSinkLayer=waterSinkLayer, \
                                    nodeTypeDict=x[1], networkLayerGeomType=networkLayerGeomType)
        
        

        selectValid = self.parameterAsBool(parameters, self.SELECT_ALL_VALID, context)
        
        self.prepareFlagSink(parameters, networkLayer, networkLayer.wkbType(), context)

        




        
        

        return {self.NETWORK_LAYER : networkLayer, self.FLAGS : self.flag_id, self.LINE_FLAGS : line_flag_id}

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
                    DsgEnums.Flag : None, # 0 - Flag (fim de trecho sem 'justificativa espacial')
                    DsgEnums.Sink : 'in', # 1 - Sumidouro
                    DsgEnums.WaterwayBegin : 'out', # 2 - Fonte D'Água
                    DsgEnums.DownHillNode : 'in', # 3 - Interrupção à Jusante
                    DsgEnums.UpHillNode : 'out', # 4 - Interrupção à Montante
                    DsgEnums.Confluence : 'in and out', # 5 - Confluência
                    DsgEnums.Ramification : 'in and out', # 6 - Ramificação
                    DsgEnums.AttributeChange : 'in and out', # 7 - Mudança de Atributo
                    DsgEnums.NodeNextToWaterBody : 'in or out', # 8 - Nó próximo a corpo d'água
                    DsgEnums.AttributeChangeFlag : None, # 9 - Nó de mudança de atributos conectado em linhas que não mudam de atributos
                    DsgEnums.NodeOverload : None, # 10 - Há igual número de linhas (>1 para cada fluxo) entrando e saindo do nó
                    DsgEnums.DisconnectedLine : None, # 11 - Nó conectado a uma linha perdida na rede (teria dois inícios de rede)
                    # DsgEnums.NodeOverload : None # 10 - Mais 
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
        linesNotValidated = list( set( nodePointDict['start']  + nodePointDict['end'] ) - set(connectedValidLines) )
        # starting dicts of valid and invalid lines
        validLines, invalidLines = dict(), dict()
        if not flow:
            # flags have all lines flagged
            if nodeType == CreateNetworkNodesProcess.Flag:
                reason = self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
                invalidLines = { line.id() : line for line in linesNotValidated }
            elif nodeType == CreateNetworkNodesProcess.AttributeChangeFlag:
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
                    self.nodeTypeDict[node] = CreateNetworkNodesProcess.Flag
                    # reclassify node type into layer
                    self.reclassifyNodeType[node] = CreateNetworkNodesProcess.Flag
                    reason = self.tr('Node was flagged upon classification (probably cannot be an ending hidrography node).')
            elif nodeType == CreateNetworkNodesProcess.DisconnectedLine:
                # get line connected to node
                lines = nodePointDict['start'] + nodePointDict['end']
                # just in case there's a node wrong manual reclassification so code doesn't raise an error
                ids = [str(line.id()) for line in lines]
                invalidLines = { line.id() : line for line in lines }
                reason = self.tr('Line {0} disconnected from network.').format(", ".join(ids))
            elif nodeType == CreateNetworkNodesProcess.NodeOverload:
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
            deltaLinesCheckList = [CreateNetworkNodesProcess.Confluence, CreateNetworkNodesProcess.Ramification] # nodes that have an unbalaced number ratio of flow in/out
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
        inContourConditionTypes = [CreateNetworkNodesProcess.DownHillNode, CreateNetworkNodesProcess.Sink]
        outContourConditionTypes = [CreateNetworkNodesProcess.UpHillNode, CreateNetworkNodesProcess.WaterwayBegin]
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
            map(reclassifyNodeAlias, map(initialNode, flippedLines) + map(lastNode, flippedLines))
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
        startingNodeTypes = [CreateNetworkNodesProcess.UpHillNode, CreateNetworkNodesProcess.WaterwayBegin] # node types that are over the frame contour and line BEGINNINGS
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
                        flippedLinesIds += flippedLines
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
                        flippedLinesIds = list( (set(flippedLinesIds) - removeIds) ) + list( addIds  )
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

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'verifynetworkdirectioning'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Verify Network Directioning')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return VerifyNetworkDirectioningAlgorithm()