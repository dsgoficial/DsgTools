# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-05
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
from PyQt5.QtCore import QCoreApplication, QVariant

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.networkHandler import NetworkHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink, QgsField,
                       QgsFields, QgsGeometry, QgsProcessing,
                       QgsProcessingAlgorithm, QgsProcessingException,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsSpatialIndex, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class CreateNetworkNodesAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = 'NETWORK_LAYER'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    SINK_LAYER = 'SINK_LAYER'
    SPILLWAY_LAYER = 'SPILLWAY_LAYER'
    REF_LAYER = 'REF_LAYER'
    WATER_BODY_LAYERS = 'WATER_BODY_LAYERS'
    DITCH_LAYER = 'DITCH_LAYER'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    NETWORK_NODES = 'NETWORK_NODES'
    FLAGS = 'FLAGS'

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
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr('Fields to ignore'),
                None,
                'NETWORK_LAYER',
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr('Ignore virtual fields'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr('Ignore primary key fields'),
                defaultValue=True
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
            QgsProcessingParameterVectorLayer(
                self.SPILLWAY_LAYER,
                self.tr('Spillway layer'),
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
            QgsProcessingParameterVectorLayer(
                self.DITCH_LAYER,
                self.tr('Ditch layer'),
                [QgsProcessing.TypeVectorLine],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.SEARCH_RADIUS, 
                self.tr('Snap radius'), 
                parentParameterName=self.NETWORK_LAYER,                                         
                minValue=0, 
                defaultValue=1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NETWORK_NODES,
                self.tr('Node layer')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('Flags')
            )
        )
        self.nodeIdDict = None
        self.nodeDict = None
        self.nodeTypeDict = None
    
    def getFields(self):
        fields = QgsFields()
        fields.append(QgsField('node_type', QVariant.String))
        fields.append(QgsField('layer', QVariant.String))
        return fields

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        #get the network handler
        layerHandler = LayerHandler()
        networkHandler = NetworkHandler()
        algRunner = AlgRunner()
        self.nodeTypeNameDict = networkHandler.nodeTypeDict
        # get network layer
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        if networkLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NETWORK_LAYER))
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        ignoreVirtual = self.parameterAsBool(parameters, self.IGNORE_VIRTUAL_FIELDS, context)
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)
        # get network node layer
        (nodeSink, dest_id) = self.parameterAsSink(parameters, self.NETWORK_NODES,
                context, self.getFields(), QgsWkbTypes.MultiPoint, networkLayer.sourceCrs())
        #prepairs flag sink for raising errors
        self.prepareFlagSink(parameters, networkLayer, QgsWkbTypes.MultiPoint, context)
        
        waterBodyClasses = self.parameterAsLayer(parameters, self.WATER_BODY_LAYERS, context)
        waterBodyClasses = waterBodyClasses if waterBodyClasses is not None else []
        # get water sink layer
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        # get spillway layer
        spillwayLayer = self.parameterAsLayer(parameters, self.SPILLWAY_LAYER, context)
        # get frame layer
        frameLayer = self.parameterAsLayer(parameters, self.REF_LAYER, context)
        currStep = 0
        if frameLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REF_LAYER))
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(currStep)
        multiStepFeedback.pushInfo(self.tr('Preparing bounds...'))
        frame = layerHandler.getFrameOutterBounds(frameLayer, algRunner, context, feedback=multiStepFeedback)
        currStep += 1
        # get search radius
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        # get ditch layer
        ditchLayer = self.parameterAsLayer(parameters, self.DITCH_LAYER, context)

        #new step
        multiStepFeedback.setCurrentStep(currStep)
        multiStepFeedback.pushInfo(self.tr('Performing node identification...'))
        self.nodeDict = networkHandler.identifyAllNodes(networkLayer=networkLayer, feedback=multiStepFeedback) #zoado, mudar lógica
        multiStepFeedback.pushInfo(self.tr('{node_count} node(s) identificated...').format(node_count=len(self.nodeDict)))
        currStep += 1
        #new step
        multiStepFeedback.setCurrentStep(currStep)
        multiStepFeedback.pushInfo(self.tr('Performing node classification...'))
        networkHandler.nodeDict = self.nodeDict
        self.nodeTypeDict, nodeFlagDict = networkHandler.classifyAllNodes(
                networkLayer=networkLayer,
                frameLyrContourList=frame,
                waterBodiesLayers=waterBodyClasses,
                searchRadius=searchRadius,
                waterSinkLayer=waterSinkLayer,
                spillwayLayer=spillwayLayer,
                feedback=multiStepFeedback,
                attributeBlackList=attributeBlackList,
                excludePrimaryKeys=ignorePK,
                ignoreVirtualFields=ignoreVirtual,
                ditchLayer=ditchLayer
            )
        currStep += 1
        #new step
        multiStepFeedback.setCurrentStep(currStep)
        multiStepFeedback.pushInfo(self.tr('Writing nodes...'))
        self.fillNodeSink(
            nodeSink=nodeSink,
            networkLineLayerName=networkLayer.name(),
            nodeFlagDict=nodeFlagDict,
            feedback=multiStepFeedback)
        return {self.NETWORK_NODES : dest_id, self.FLAGS : self.flag_id}

    def fillNodeSink(self, nodeSink, networkLineLayerName, nodeFlagDict, feedback=None):
        """
        Populate hidrography node layer with all nodes.
        :param nodeSink: (QgsFeatureSink) hidrography nodes layer.
        :param networkLineLayerName: (str) network line layer name.
        """
        # get fields from layer in order to create new feature with the same attribute map
        fields = self.getFields()
        nPoints = len(self.nodeTypeDict)
        size = 100/nPoints if nPoints else 0
        # to avoid unnecessary calculation inside loop
        nodeTypeKeys = self.nodeTypeDict.keys()
        # initiate new features list
        featList = []
        for current, node in enumerate(self.nodeDict):
            # set attribute map
            feat = QgsFeature(fields)
            # set geometry
            nodeGeom = QgsGeometry.fromMultiPointXY([node])
            feat.setGeometry(nodeGeom)
            feat['node_type'] = self.nodeTypeDict[node] if node in nodeTypeKeys else None
            feat['layer'] = networkLineLayerName
            if node in nodeFlagDict:
                self.flagFeature(nodeGeom, nodeFlagDict[node])
            featList.append(feat)
            if feedback is not None:
                feedback.setProgress(size * current)
        nodeSink.addFeatures(featList, QgsFeatureSink.FastInsert)
    
    def flagNetworkProblems(self, nodeTypeDict):
        """
        Raises problems in network as flags.
        :param nodeTypeDict: (dict) network problems
        """
        for node in nodeTypeDict:
            pass

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createnetworknodes'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create Drainage Network Nodes')

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
        return QCoreApplication.translate('CreateNetworkNodesAlgorithm', string)

    def createInstance(self):
        return CreateNetworkNodesAlgorithm()
