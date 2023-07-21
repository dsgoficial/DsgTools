# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-21
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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


from collections import defaultdict
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsGeometry,
    QgsVectorLayer,
    QgsProcessingException,
    QgsExpression,
    QgsProject,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterType,
    QgsProcessingParameterDefinition,
)

from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import geometryHandler


class IdentifySmallObjectsOnLayersAlgorithm(ValidationAlgorithm):
    """
    Algorithm for verifying features closer than minium distance for each layer pair set.
    """

    SMALL_OBJECTS_PARAMETERS = "SMALL_OBJECTS_PARAMETERS"
    LINE_FLAGS = "LINE_FLAGS"
    POLYGON_FLAGS = "POLYGON_FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        smallObjectsParam = ParameterSmallObjectsOnLayers(
            self.SMALL_OBJECTS_PARAMETERS,
            description=self.tr("Minimum distance between layers"),
        )
        smallObjectsParam.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.smallObjectsOnLayersWrapper.SmallObjectsOnLayersWrapper"
            }
        )
        self.addParameter(smallObjectsParam)
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.LINE_FLAGS, self.tr("Line Flags"))
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS, self.tr("Polygon Flags")
            )
        )

    def parameterAsSmallObjectsOnLayers(self, parameters, name, context):
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
        algRunner = AlgRunner()
        smallObjectsStructure = self.parameterAsSmallObjectsOnLayers(
            parameters, self.SMALL_OBJECTS_PARAMETERS, context
        )
        (self.lineFlagSink, self.line_flag_id) = self.prepareAndReturnFlagSink(
            parameters,
            None,
            QgsWkbTypes.LineString,
            context,
            self.LINE_FLAGS,
        )
        (self.polygonFlagSink, self.polygon_flag_id) = self.prepareAndReturnFlagSink(
            parameters,
            None,
            QgsWkbTypes.Polygon,
            context,
            self.POLYGON_FLAGS,
        )
        func_dict = {
            QgsWkbTypes.LineString: lambda x: algRunner.runIdentifySmallLines(
                inputLyr=x[0],
                tol=x[1],
                context=context,
                feedback=x[2],
            ),
            QgsWkbTypes.Polygon: lambda x: algRunner.runIdentifySmallPolygons(
                inputLyr=x[0],
                tol=x[1],
                context=context,
                feedback=x[2],
            ),
        }
        nSteps = len(smallObjectsStructure) + 2
        outputDict = defaultdict(list)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        for currentStep, item in enumerate(smallObjectsStructure):
            multiStepFeedback.setCurrentStep(currentStep)
            outputLyr = func_dict[item["layer"].geometryType()](
                [item["layer"], item["tol"], multiStepFeedback]
            )
            outputDict[item["layer"].geometryType()].append(outputLyr)

        flagLambdaDict = {
            QgsWkbTypes.LineString: lambda x: self.lineFlagSink.addFeature(x),
            QgsWkbTypes.Polygon: lambda x: self.polygonFlagSink.addFeature(x),
        }
        for currentStep, (wkbType, featList) in enumerate(
            outputDict.items(), start=currentStep + 1
        ):
            multiStepFeedback.setCurrentStep(currentStep)
            mergedLyr = algRunner.runMergeVectorLayers(
                inputList=featList,
                context=context,
                feedback=multiStepFeedback,
                crs=QgsProject.instance().crs(),
            )
            list(map(flagLambdaDict[wkbType], mergedLyr.getFeatures()))
        return {
            self.LINE_FLAGS: self.line_flag_id,
            self.POLYGON_FLAGS: self.polygon_flag_id,
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifysmallobjectsonlayersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Small Objects On Layers")

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
        return QCoreApplication.translate(
            "IdentifySmallObjectsOnLayersAlgorithm", string
        )

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return IdentifySmallObjectsOnLayersAlgorithm()


class ParameterDistanceBetweenLayersType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterSmallObjectsOnLayers(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.smallObjectsOnLayersWrapper.SmallObjectsOnLayersWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", "Small Objects")

    def id(self):
        return "distance_between_layers"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "Identify small objects on layers (small lines, small first order lines, small areas, small holes).",
        )


class ParameterSmallObjectsOnLayers(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterSmallObjectsOnLayers(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "small_objects_on_layers"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
