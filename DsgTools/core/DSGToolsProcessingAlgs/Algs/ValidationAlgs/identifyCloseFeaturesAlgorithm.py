# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsGeometry,
    QgsVectorLayer,
    QgsProcessingException,
    QgsExpression,
    QgsProperty,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterType,
    QgsProcessingParameterDefinition,
)

from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import geometryHandler


class IdentifyCloseFeaturesAlgorithm(ValidationAlgorithm):
    """
    Algorithm for verifying features closer than minium distance for each layer pair set.
    """

    DISTANCE_BETWEEN_LAYERS = "DISTANCE_BETWEEN_LAYERS"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        minimumDistanceParameter = ParameterDistanceBetweenLayers(
            self.DISTANCE_BETWEEN_LAYERS,
            description=self.tr("Minimum distance between layers"),
        )
        minimumDistanceParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.distanceBetweenLayersWrapper.DistanceBetweenLayersWrapper"
            }
        )
        self.addParameter(minimumDistanceParameter)
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.FLAGS, self.tr("Flags"))
        )

    def parameterAsMinimumDistanceBetweenLayers(self, parameters, name, context):
        """
        Adds data from wrapper to algorithm parameters.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters;
        :param name: parameter Name;
        :param context: (QgsProcessingContext) context in which
            processing was run;
        :return: (dict) parameters dictionary.
        """
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters.
        :param context: (QgsProcessingContext) context in which
            processing was run.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (dict) filled flag layer.
        """

        minimumDistances = self.parameterAsMinimumDistanceBetweenLayers(
            parameters, self.DISTANCE_BETWEEN_LAYERS, context
        )
        self.prepareFlagSink(parameters, None, QgsWkbTypes.MultiLineString, context)
        if not minimumDistances:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.DISTANCE_BETWEEN_LAYERS)
            )
        nSteps = len(minimumDistances)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        self.algRunner = AlgRunner()
        tempLayersDict = dict()
        for current, row in enumerate(minimumDistances):
            multiStepFeedback.setCurrentStep(current)
            self.findCloseFeatures(row, tempLayersDict, context, multiStepFeedback)

        return {self.FLAGS: self.flag_id}

    def findCloseFeatures(self, row, tempLayersDict, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        distance = row["distance"]
        layerApre = row["layerA"]
        layerBpre = row["layerB"]
        layerBuffredString = self.addBufferedLayerToDict(
            layerApre, distance, tempLayersDict, context, multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        self.addTempLayerToDict(layerBpre, tempLayersDict, context, multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        layers = layerBuffredString, layerApre, layerBpre, distance
        self.addCloseFeaturesToSink(layers, tempLayersDict, context, multiStepFeedback)

    def addBufferedLayerToDict(
        self, layerPre, distance, tempLayersDict, context, feedback
    ) -> str:
        """
        Adds a buffered layer with a specified distance to the tempLayersDict and returns the buffered layer's name.
        :param layerPre: (str) The name of the layer to be buffered.
        :param distance: (float) The buffer distance in meters.
        :param tempLayersDict: (dict) A dictionary containing temporary layers.
        """
        layerBufferedString = layerPre + "_buffered_" + str(distance)
        if layerBufferedString in tempLayersDict:
            return layerBufferedString
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        if not layerPre in tempLayersDict:
            self.addTempLayerToDict(
                layerPre, tempLayersDict, context, multiStepFeedback
            )
        multiStepFeedback.setCurrentStep(1)
        layerBuffered = self.algRunner.runBuffer(
            inputLayer=tempLayersDict[layerPre],
            distance=distance,
            context=context,
            is_child_algorithm=True,
        )
        multiStepFeedback.setCurrentStep(2)
        singlePart = self.algRunner.runMultipartToSingleParts(
            inputLayer=layerBuffered, context=context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        multiStepFeedback.setCurrentStep(3)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=singlePart, context=context, is_child_algorithm=True
        )
        tempLayersDict[layerBufferedString] = singlePart
        return layerBufferedString

    def addTempLayerToDict(self, layerPre, tempLayersDict, context, feedback):
        """
        Adds a temporary layer to tempLayersDict.
        :param layerPre: (str) The name of the temporary layer to be added.
        :param tempLayersDict: (dict) A dictionary containing temporary layers.
        """
        if layerPre in tempLayersDict:
            return
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        layer = self.algRunner.runCreateFieldWithExpression(
            layerPre, expression="$id", fieldName="feat_id", context=context
        )
        multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=layer, context=context, is_child_algorithm=True
        )
        tempLayersDict[layerPre] = layer

    def addCloseFeaturesToSink(self, layers, tempLayersDict, context, feedback):
        """
        Adds close features from layerB to the sink layer based on the buffered layerA's proximity.
        :param layers: (list) A list containing the names of the buffered layer (layerBuffredString), original layer A (layerApre), original layer B (layerBpre), and the distance.
        :param tempLayersDict: (dict) A dictionary containing the temporary layers used in the process.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        layerBuffredString, layerApre, layerBpre, distance = layers
        feedbackTxt = f"Verifying {layerApre} x {layerBpre}"
        multiStepFeedback.setProgressText(feedbackTxt)
        layerAbuffered = tempLayersDict[layerBuffredString]
        layerA = tempLayersDict[layerApre]
        lyrAPkFieldNames = self.getLayerPrimaryKeyAttributeNames(layerApre)
        lyrAPkFieldName = "feat_id" if lyrAPkFieldNames is None else lyrAPkFieldNames[0]
        idAText = self.tr(f"with feature id") if lyrAPkFieldName == "feat_id" else self.tr(f"with {lyrAPkFieldName}")
        layerB = tempLayersDict[layerBpre]
        lyrBPkFieldNames = self.getLayerPrimaryKeyAttributeNames(layerBpre)
        lyrBPkFieldName = "feat_id" if lyrBPkFieldNames is None else lyrBPkFieldNames[0]
        idBText = self.tr(f"with feature id") if lyrBPkFieldName == "feat_id" else self.tr(f"with {lyrBPkFieldName}")
        multiStepFeedback.setCurrentStep(0)
        joinedLayer = self.algRunner.runJoinAttributesByLocation(
            inputLyr=layerAbuffered,
            joinLyr=layerB,
            context=context,
            predicateList=[0],
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        wkbSet = set()
        featsId = []
        totalFeat = joinedLayer.featureCount()
        stepSize = 100 / totalFeat if totalFeat else 0
        for current, feat in enumerate(joinedLayer.getFeatures()):
            featIdSet = {feat["feat_id"], feat["feat_id_2"]}
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return
            if layerApre == layerBpre and (
                feat["feat_id"] == feat["feat_id_2"] or featIdSet in featsId
            ):
                continue
            featsId.append(featIdSet)
            expression = QgsExpression(f'"feat_id"={feat["feat_id"]}')
            request = QgsFeatureRequest(expression)
            featA = next(layerA.getFeatures(request))
            pointA = featA.geometry().asPoint()
            expression = QgsExpression(f'"feat_id"={feat["feat_id_2"]}')
            request = QgsFeatureRequest(expression)
            featB = next(layerB.getFeatures(request))
            pointB = featB.geometry().asPoint()
            geom = QgsGeometry().fromPolylineXY([pointA, pointB])
            if geom.asWkb() in wkbSet:
                continue
            wkbSet.add(geom)
            flagText = self.tr(f"Feature from layer {layerApre} with {idAText}={featA[lyrAPkFieldName]} has distance smaller than {distance} from feature from layer {layerBpre} with {idBText}={featB[lyrAPkFieldName]}")
            self.flagFeature(geom, flagText)
            multiStepFeedback.setProgress(current * stepSize)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyclosefeaturesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Close Features")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("IdentifyCloseFeaturesAlgorithm", string)

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return IdentifyCloseFeaturesAlgorithm()


class ParameterDistanceBetweenLayersType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterDistanceBetweenLayers(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.distanceBetweenLayersWrapper.DistanceBetweenLayersWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", "Distance Between Layers")

    def id(self):
        return "distance_between_layers"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "Check minimum acceptable distance between features of chosen layers.",
        )


class ParameterDistanceBetweenLayers(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterDistanceBetweenLayers(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "distance_between_layers"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
