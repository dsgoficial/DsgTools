# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-10
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from PyQt5.QtCore import QCoreApplication

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterType,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyInvalidAttributeCombinationsAlgorithm(ValidationAlgorithm):
    ATTRIBUTE_RULES = "ATTRIBUTE_RULES"
    BEHAVIOR = "BEHAVIOR"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        hierarchy = ParameterAttributeRules(
            self.ATTRIBUTE_RULES, description=self.tr("Attribute Rules")
        )
        hierarchy.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.attributeRulesWrapper.AttributeRulesWrapper"
            }
        )
        self.addParameter(hierarchy)

        self.modes = [
            self.tr("Prefer aligning nodes, insert extra vertices where required"),
            self.tr("Prefer closest point, insert extra vertices where required"),
            self.tr("Prefer aligning nodes, don't insert new vertices"),
            self.tr("Prefer closest point, don't insert new vertices"),
            self.tr("Move end points only, prefer aligning nodes"),
            self.tr("Move end points only, prefer closest point"),
            self.tr("Snap end points to end points only"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR, self.tr("Behavior"), options=self.modes, defaultValue=0
            )
        )

    def parameterAsAttributeRules(self, parameters, name, context):
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        snapDict = self.parameterAsSnapHierarchy(
            parameters, self.SNAP_HIERARCHY, context
        )

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        nSteps = 0
        for item in snapDict:
            nSteps += len(item["snapLayerList"])
        currStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        for current, item in enumerate(snapDict):
            refLyr = item["referenceLayer"]
            for i, lyr in enumerate(item["snapLayerList"]):
                if multiStepFeedback.isCanceled():
                    break
                multiStepFeedback.setCurrentStep(currStep)
                multiStepFeedback.pushInfo(
                    self.tr(
                        "Snapping geometries from layer {input} to {reference} with snap {snap}..."
                    ).format(
                        input=lyr.name(), reference=refLyr.name(), snap=item["snap"]
                    )
                )
                layerHandler.snapToLayer(
                    lyr,
                    refLyr,
                    item["snap"],
                    behavior,
                    onlySelected=onlySelected,
                    feedback=multiStepFeedback,
                )
                currStep += 1
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyinvalidattributecombinations"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Invalid Attribute Combinations")

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
        return QCoreApplication.translate(
            "IdentifyInvalidAttributeCombinationsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyInvalidAttributeCombinationsAlgorithm()


class ParameterAttributeRulesType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterAttributeRules(name)  # mudar

    def metadata(self):
        return {
            "widget_wrapper": "DSGTools.gui.ProcessingUI.attributeRulesWrapper.AttributeRulesWrapper"
        }  # mudar

    def name(self):
        return QCoreApplication.translate("Processing", "Attribute Rules")

    def id(self):
        return "attribute_rules"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "An attribute rules type. Used in the Identify Invalid Attribute Combinations algorithm.",
        )


class ParameterAttributeRules(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterAttributeRules(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "attribute_rules"

    def checkValueIsAcceptable(self, value, context=None):
        # if not isinstance(value, list):
        #     return False
        # for field_def in value:
        #     if not isinstance(field_def, dict):
        #         return False
        #     if 'name' not in field_def.keys():
        #         return False
        #     if 'type' not in field_def.keys():
        #         return False
        #     if 'expression' not in field_def.keys():
        #         return False
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
