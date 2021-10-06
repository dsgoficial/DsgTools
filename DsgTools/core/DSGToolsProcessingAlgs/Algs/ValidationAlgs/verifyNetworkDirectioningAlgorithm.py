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
from PyQt5.QtCore import QCoreApplication

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.networkHandler import NetworkHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
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

from ....dsgEnums import DsgEnums
from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class VerifyNetworkDirectioningAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = 'NETWORK_LAYER'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    NODE_LAYER = 'NODE_LAYER'
    SINK_LAYER = 'SINK_LAYER'
    SPILLWAY_LAYER = 'SPILLWAY_LAYER'
    REF_LAYER = 'REF_LAYER'
    WATER_BODY_LAYERS = 'WATER_BODY_LAYERS'
    MAX_CYCLES = 'MAX_CYCLES'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    SELECT_ALL_VALID = 'SELECT_ALL_VALID'
    FLAGS = 'FLAGS'
    LINE_FLAGS = 'LINE_FLAGS'
    DITCH_LAYER = 'DITCH_LAYER'

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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        #get the network handler
        layerHandler = LayerHandler()
        networkHandler = NetworkHandler()
        algRunner = AlgRunner()
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
        # get spillway layer
        spillwayLayer = self.parameterAsLayer(parameters, self.SPILLWAY_LAYER, context)
        # get frame layer
        frameLayer = self.parameterAsLayer(parameters, self.REF_LAYER, context)
        if frameLayer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REF_LAYER))
        # get ditch layer
        ditchLayer = self.parameterAsLayer(parameters, self.DITCH_LAYER, context)
        attributeBlackList = self.parameterAsFields(parameters, self.ATTRIBUTE_BLACK_LIST, context)
        ignoreVirtual = self.parameterAsBool(parameters, self.IGNORE_VIRTUAL_FIELDS, context)
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        frame = layerHandler.getFrameOutterBounds(frameLayer, algRunner, context, feedback=multiStepFeedback)
        # get search radius
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        selectValid = self.parameterAsBool(parameters, self.SELECT_ALL_VALID, context)
        max_amount_cycles = self.parameterAsInt(parameters, self.MAX_CYCLES, context)
        nodeFlags, featList, nodeIdDict = networkHandler.verifyNetworkDirectioning(
            networkLayer,
            networkNodeLayer,
            frame,
            searchRadius,
            waterBodyClasses=waterBodyClasses,
            waterSinkLayer=waterSinkLayer,
            spillwayLayer=spillwayLayer,
            max_amount_cycles=max_amount_cycles,
            feedback=multiStepFeedback,
            selectValid=selectValid,
            ditchLayer=ditchLayer,
            attributeBlackList=attributeBlackList,
            excludePrimaryKeys=ignorePK,
            ignoreVirtualFields=ignoreVirtual
        )
        multiStepFeedback.setCurrentStep(1)
        #these are counted as one set of operations
        flag_line_sink_id = self.addFeaturesToFlagLineSink(featList, parameters, networkLayer, context)
        self.prepareFlagSink(parameters, networkLayer, QgsWkbTypes.Point, context)
        self.buildFlagList(nodeFlags, networkLayer, nodeIdDict, multiStepFeedback)

        return {self.NETWORK_LAYER : networkLayer, self.FLAGS : self.flag_id, self.LINE_FLAGS : flag_line_sink_id}

    def addFeaturesToFlagLineSink(self, featList, parameters, source, context):
        """
        Adds line flags raised by networkHandler to flag line sink.
        """
        flag_line_sink, flag_line_sink_id = self.prepareAndReturnFlagSink(
                                                                            parameters,
                                                                            source,
                                                                            QgsWkbTypes.LineString,
                                                                            context,
                                                                            self.LINE_FLAGS
                                                                        )
        flag_line_sink.addFeatures(featList, QgsFeatureSink.FastInsert)
        return flag_line_sink_id
    
    def buildFlagList(self, nodeFlags, source, nodeIdDict, feedback):
        """
        Builds record list from pointList to raise flags.
        :param nodeFlags: (dict) dictionary containing invalid node 
                            and its reason ( { (QgsPoint) node : (str) reason } )
        """
        # prepare point flag sink
        countNodeNotInDb = 0
        nodeNumber = len(nodeFlags)
        size = 100/nodeNumber if nodeNumber else 0
        for current, (node, reason) in enumerate(nodeFlags.items()):
            if feedback.isCanceled():
                break
            if node in nodeIdDict:
                featid = nodeIdDict[node] if nodeIdDict[node] is not None else -9999
            else:
                # if node is not previously classified on database, but then motivates a flag, it should appear on Flags list
                featid = -9999
                countNodeNotInDb += 1
            flagText = 'Feature with id={id} from {lyrName} with problem: {msg}'.format(
                id=featid,
                lyrName=source.name(),
                msg=reason
            )
            flagGeom = QgsGeometry.fromMultiPointXY([node])
            self.flagFeature(flagGeom, flagText)
            feedback.setProgress(size * current)
        if countNodeNotInDb:
            # in case there are flagged nodes that are not loaded in DB, user is notified
            msg = self.tr('There are {0} flagged nodes that were introduced to network. Node reclassification is indicated.').format(countNodeNotInDb)
            feedback.pushInfo(msg)

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
        return self.tr('Verify Drainage Network Directioning')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Network Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Network Processes)'

    def tr(self, string):
        return QCoreApplication.translate('VerifyNetworkDirectioningAlgorithm', string)

    def createInstance(self):
        return VerifyNetworkDirectioningAlgorithm()
