# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-06
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
from DsgTools.core.GeometricTools import layerHandler
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
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSource,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsProject,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class SnapLayerOnLayerAndUpdateAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    REFERENCE_LAYER = "REFERENCE_LAYER"
    BUILD_CACHE = "BUILD_CACHE"
    TOLERANCE = "TOLERANCE"
    BEHAVIOR = "BEHAVIOR"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.REFERENCE_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Search Radius"),
            parentParameterName=self.INPUT,
            defaultValue=1.0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)
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
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BUILD_CACHE, self.tr("Build local cache of the reference layer")
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer with snapped features")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        refLyr = self.parameterAsSource(parameters, self.REFERENCE_LAYER, context)
        if refLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.REFERENCE_LAYER)
            )
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        buildLocalCache = self.parameterAsBool(parameters, self.BUILD_CACHE, context)
        nSteps = 6 if buildLocalCache else 4
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating aux structure..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(auxLyr, context, multiStepFeedback)
        currentStep += 1

        if buildLocalCache:
            multiStepFeedback.setProgressText(self.tr("Building local cache..."))
            multiStepFeedback.setCurrentStep(currentStep)
            refLyr = algRunner.runAddAutoIncrementalField(
                refLyr, context, multiStepFeedback, is_child_algorithm=True
            )
            currentStep += 1

            multiStepFeedback.setCurrentStep(currentStep)
            algRunner.runCreateSpatialIndex(refLyr, context, multiStepFeedback, is_child_algorithm=True)
            currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Running snap..."))
        snapped = algRunner.runSnapGeometriesToLayer(
            inputLayer=auxLyr,
            referenceLayer=refLyr if buildLocalCache else parameters[self.REFERENCE_LAYER],
            tol=tol,
            behavior=behavior,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        if multiStepFeedback.isCanceled():
            return {self.OUTPUT: inputLyr}

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr], snapped, feedback=multiStepFeedback, onlySelected=onlySelected
        )
        return {self.OUTPUT: inputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "snaplayeronlayer"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Snap layer on layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Manipulation Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Manipulation Processes)"

    def tr(self, string):
        return QCoreApplication.translate("SnapLayerOnLayerAndUpdateAlgorithm", string)

    def createInstance(self):
        return SnapLayerOnLayerAndUpdateAlgorithm()
