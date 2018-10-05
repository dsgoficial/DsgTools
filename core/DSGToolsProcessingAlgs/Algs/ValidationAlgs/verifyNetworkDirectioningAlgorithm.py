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
from DsgTools.core.GeometricTools.networkHandler import NetworkHandler
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
    WATER_BODY_LAYERS = 'WATER_BODY_LAYERS'
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
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NODE_LAYER,
                self.tr('Node layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.REF_LAYER,
                self.tr('Reference layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SINK_LAYER,
                self.tr('Water sink layer'),
                [QgsProcessing.TypeVectorPoint],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.WATER_BODY_LAYERS,
                self.tr('Water body layers'),
                QgsProcessing.TypeVectorPolygon,
                optional=True
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
                self.tr('{0} network node errors').format(self.displayName())
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr('{0} line errors').format(self.displayName())
            )
        )
        self.nodeIdDict = None
        self.nodeDict = None
        self.nodeTypeDict = None

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        #get the network handler
        layerHandler = LayerHandler()
        networkHandler = NetworkHandler()
        self.nodeTypeNameDict = networkHandler.nodeTypeDict
        # get network layer
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        if networkLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NETWORK_LAYER))
        # get network node layer
        networkNodeLayer = self.parameterAsLayer(parameters, self.NODE_LAYER, context)
        if networkLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NODE_LAYER))
        waterBodyClasses = self.parameterAsLayer(parameters, self.WATER_BODY_LAYERS, context)
        networkNodeLayer.startEditing()
        # get water sink layer
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        # get frame layer
        frameLayer = self.parameterAsLayer(parameters, self.REF_LAYER, context)
        if frameLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REF_LAYER))
        frame = layerHandler.getFrameOutterBounds(frameLayer, self.algRunner, context, feedback=feedback)
        # prepare point flag sink
        self.prepareFlagSink(parameters, networkLayer, networkLayer.wkbType(), context)
        # get search radius
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        selectValid = self.parameterAsBool(parameters, self.SELECT_ALL_VALID, context)
        networkLayerGeomType = networkLayer.geometryType()

        self.nodeDict = networkHandler.identifyAllNodes(networkLayer=networkLayer)
        # declare reclassification function from createNetworkNodesProcess object - parameter is [node, nodeTypeDict] 
        self.classifyNode = lambda x : networkHandler.nodeType(nodePoint=x[0], networkLayer=networkLayer, frameLyrContourList=frame, \
                                    waterBodiesLayers=waterBodyClasses, searchRadius=searchRadius, waterSinkLayer=waterSinkLayer, \
                                    nodeTypeDict=x[1], networkLayerGeomType=networkLayerGeomType)
        # update createNetworkNodesProcess object node dictionary
        networkHandler.nodeDict = self.nodeDict
        self.nodeTypeDict, self.nodeIdDict = networkHandler.getNodeTypeDictFromNodeLayer(networkNodeLayer=networkNodeLayer)
        # initiate nodes, invalid/valid lines dictionaries
        nodeFlags, inval, val = dict(), dict(), dict()
        # cycle count start
        cycleCount = 0
        # get max amount of orientation cycles
        MAX_AMOUNT_CYCLES = self.parameterAsInteger(parameters, self.MAX_CYCLES, context)
        MAX_AMOUNT_CYCLES = MAX_AMOUNT_CYCLES if MAX_AMOUNT_CYCLES > 0 else 1
        # validation method FINALLY starts...
        # to speed up modifications made to layers
        multiStepFeedback = QgsProcessingMultiStepFeedback(MAX_AMOUNT_CYCLES, feedback)
        multiStepFeedback.setCurrentStep(cycleCount)
        networkNodeLayer.beginEditCommand('Reclassify Nodes')
        networkLayer.beginEditCommand('Flip/Merge Lines')
        while True:
            nodeFlags_, inval_, val_ = networkHandler.directNetwork(networkLayer=networkLayer, nodeLayer=networkNodeLayer)
            cycleCount += 1
            # Log amount of cycles completed
            cycleCountLog = self.tr("Cycle {0}/{1} completed.").format(cycleCount, MAX_AMOUNT_CYCLES)
            multiStepFeedback.pushInfo(cycleCountLog)
            multiStepFeedback.setCurrentStep(cycleCount)
            self.reclassifyNodeType = dict()
            # stop conditions: max amount of cycles exceeded, new flags is the same as previous flags (there are no new issues) and no change
            # change to valid lines list was made (meaning that the algorithm did not change network state) or no flags found
            if (cycleCount == MAX_AMOUNT_CYCLES) or (not nodeFlags_) or \
            (set(nodeFlags.keys()) == set(nodeFlags_.keys()) and val == val_):
                # copy values to final dict
                nodeFlags, inval, val = nodeFlags_, inval_, val_
                # no more modifications to those layers will be done
                networkLayer.endEditCommand()
                networkNodeLayer.endEditCommand()
                # try to load auxiliary line layer to fill it with invalid lines
                flag_line_sink_id = self.createFlagLineSink(networkLayer, val, inval, networkHandler, parameters, networkLayer, context)
                invalidLinesLog = self.tr("Invalid lines were exposed in layer {0}).").format(self.tr('{0} line errors').format(self.displayName()))
                multiStepFeedback.setCurrentStep(invalidLinesLog)
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
            for node in networkHandler.nodesToPop:
                # those were nodes connected to lines that were merged and now are no longer to be used
                networkHandler.nodeDict.pop(node, None)
                networkHandler.nodeDict.pop(node, None)
            networkHandler.nodesToPop = []
        if selectValid:
            networkHandler.setSelectedFeatures(list(val.keys()))
        percValid = float(len(val))*100.0/float(networkLayer.featureCount()) if networkLayer.featureCount() else 0
        if nodeFlags:
            msg = self.tr('{0} nodes may be invalid ({1:.2f}' + '% of network is well directed). Check flags.')\
                        .format(len(nodeFlags), percValid)
        else:
            msg = self.tr('{1:.2f}' + '% of network is well directed.')\
                        .format(len(nodeFlags), percValid)
        multiStepFeedback.pushInfo(msg)
        self.buildFlagList(nodeFlags, networkLayer, multiStepFeedback)
        return {self.NETWORK_LAYER : networkLayer, self.FLAGS : self.flag_id, self.LINE_FLAGS : flag_line_sink_id}

    def buildFlagList(self, nodeFlags, source, feedback):
        """
        Builds record list from pointList to raise flags.
        :param nodeFlags: (dict) dictionary containing invalid node 
                            and its reason ( { (QgsPoint) node : (str) reason } )
        """
        recordList = []
        countNodeNotInDb = 0
        for node, reason in nodeFlags.items():
            if node in self.nodeIdDict:
                featid = self.nodeIdDict[node] if self.nodeIdDict[node] is not None else -9999
            else:
                # if node is not previously classified on database, but then motivates a flag, it should appear on Flags list
                featid = -9999
                countNodeNotInDb += 1
            flagText = 'Feature with id={id} from {lyrName} with problem: {msg}'.format(
                id=featid,
                lyrName=source.name(),
                msg=reason
            )
            flagGeom = QgsGeometry.fromMultiPoint([node])
            self.flagFeature(flagGeom, flagText)
        if countNodeNotInDb:
            # in case there are flagged nodes that are not loaded in DB, user is notified
            msg = self.tr('There are {0} flagged nodes that were introduced to network. Node reclassification is indicated.').format(countNodeNotInDb)
            feedback.pushInfo(msg)

    def createFlagLineSink(self, networkLayer, val, inval, networkHandler, parameters, source, context):
        # get non-validated lines and add it to invalid lines layer as well
        nonValidatedLines = set()
        for line in networkLayer.getFeatures():
            lineId = line.id()
            if lineId in val or lineId in inval:
                # ignore if line are validated
                continue
            nonValidatedLines.add(line)
        featList = networkHandler.getAuxiliaryLines(fields=self.getFlagFields(), invalidLinesDict=inval,\
                                        nonValidatedLines=nonValidatedLines, networkLayerName=networkLayer.name())
        flag_line_sink, flag_line_sink_id = self.prepareAndReturnFlagSink(
                                                                            parameters,
                                                                            source,
                                                                            QgsWkbTypes.Line,
                                                                            context,
                                                                            self.LINE_FLAGS
                                                                        )
        flag_line_sink.addFeatures(featList, QgsFeatureSink.FastInsert)
        return flag_line_sink_id

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
        return self.tr('Validation Tools (Network Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Network Processes)'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return VerifyNetworkDirectioningAlgorithm()