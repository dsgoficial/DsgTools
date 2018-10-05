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
                       QgsProcessingException,
                       QgsField,
                       QgsFields)
from DsgTools.core.GeometricTools.networkHandler import NetworkHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm

class CreateNetworkNodesAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = 'NETWORK_LAYER'
    SINK_LAYER = 'SINK_LAYER'
    REF_LAYER = 'REF_LAYER'
    WATER_BODY_LAYERS = 'WATER_BODY_LAYERS'
    MAX_CYCLES = 'MAX_CYCLES'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    NETWORK_NODES = 'NETWORK_NODES'

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
                self.REF_LAYER,
                self.tr('Reference layer'),
                [QgsProcessing.TypeVectorPoint]
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
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.NETWORK_NODES,
                self.tr('Node layer')
            )
        )
        self.nodeIdDict = None
        self.nodeDict = None
        self.nodeTypeDict = None
    
    def getFields(self):
        fields = QgsFields()
        fields.append(QgsField('node_type', QVariant.String))
        fields.append(QgsField('layer'), QVariant.String)
        return fields

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
        (nodeSink, dest_id) = self.parameterAsSink(parameters, self.NETWORK_NODES,
                context, self.getFields(), QgsWkbTypes.Point, networkLayer.sourceCrs())
        
        waterBodyClasses = self.parameterAsLayer(parameters, self.WATER_BODY_LAYERS, context)
        # get water sink layer
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        # get frame layer
        frameLayer = self.parameterAsLayer(parameters, self.REF_LAYER, context)
        if frameLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REF_LAYER))
        frame = layerHandler.getFrameOutterBounds(frameLayer, self.algRunner, context)
        # prepare point flag sink
        self.prepareFlagSink(parameters, networkLayer, networkLayer.wkbType(), context)
        # get search radius
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        self.nodeDict = networkHandler.identifyAllNodes(networkLayer=networkLayer)
        self.nodeTypeDict = self.classifyAllNodes(
                networkLayer=networkLayer,
                frameLyrContourList=frame,
                waterBodiesLayers=waterBodyClasses,
                searchRadius=searchRadius,
                waterSinkLayer=waterSinkLayer
            )
        self.fillNodeSink(nodeSink=nodeSink, networkLineLayerName=networkLayer.name())
        return {self.NETWORK_NODES : dest_id}

    def fillNodeSink(self, nodeSink, networkLineLayerName):
        """
        Populate hidrography node layer with all nodes.
        :param nodeSink: (QgsFeatureSink) hidrography nodes layer.
        :param networkLineLayerName: (str) network line layer name.
        """
        # get fields from layer in order to create new feature with the same attribute map
        fields = self.getFields()
        # to avoid unnecessary calculation inside loop
        nodeTypeKeys = self.nodeTypeDict.keys()
        # initiate new features list
        featList = []
        for node in self.nodeDict:
            # set attribute map
            feat = QgsFeature(fields)
            # set geometry
            feat.setGeometry(QgsGeometry.fromMultiPoint([node]))
            feat['node_type'] = self.nodeTypeDict[node] if node in nodeTypeKeys else None
            feat['layer'] = networkLineLayerName
            featList.append(feat)
        nodeSink.addFeatures(featList, QgsFeatureSink.FastInsert)

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
        return self.tr('Create Network Nodes')

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
        return CreateNetworkNodesAlgorithm()