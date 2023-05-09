# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-09-09
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSource,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class ExtendLinesToGeographicBoundsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    EXTEND_LENGTH = "EXTEND_LENGTH"
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
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Geographic bounds"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterDistance(
                self.EXTEND_LENGTH,
                self.tr("Extend length"),
                parentParameterName=self.INPUT,
                minValue=0,
                defaultValue=0.0001,
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
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        refSource = self.parameterAsSource(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        if refSource is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.GEOGRAPHIC_BOUNDS_LAYER)
            )
        if refSource.featureCount() == 0:
            return {self.OUTPUT: inputLyr}
        tol = self.parameterAsDouble(parameters, self.EXTEND_LENGTH, context)

        nSteps = 5
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating aux structure..."))
        auxLyr = self.layerHandler.createAndPopulateUnifiedVectorLayer(
            layerList=[inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        bufferAroundBoundsLines = self.extractGeographicBoundaryLines(
            tol, parameters, context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.extendLinesByStartOrEndPoints(
            inputLyr=auxLyr,
            boundsBuffer=bufferAroundBoundsLines,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
            startPoint=True,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.extendLinesByStartOrEndPoints(
            inputLyr=auxLyr,
            boundsBuffer=bufferAroundBoundsLines,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
            startPoint=False,
        )
        currentStep += 1

        if multiStepFeedback.isCanceled():
            return {self.OUTPUT: inputLyr}

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Updating original layer..."))
        self.layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inputLyr], auxLyr, feedback=multiStepFeedback, onlySelected=onlySelected
        )
        return {self.OUTPUT: inputLyr}

    def extractGeographicBoundaryLines(self, tol, parameters, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        dissolved = self.algRunner.runDissolve(
            inputLyr=parameters[self.GEOGRAPHIC_BOUNDS_LAYER],
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        lineLyr = self.algRunner.runPolygonsToLines(
            inputLyr=dissolved,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(2)
        segmentsLyr = self.algRunner.runExplodeLines(
            inputLyr=lineLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(3)
        bufferAroundBoundsLines = self.algRunner.runBuffer(
            inputLayer=segmentsLyr,
            distance=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(4)
        self.algRunner.runCreateSpatialIndex(
            bufferAroundBoundsLines, context, feedback=multiStepFeedback
        )
        return bufferAroundBoundsLines

    def extendLinesByStartOrEndPoints(
        self, inputLyr, boundsBuffer, tol, context, feedback, startPoint=True
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(0)
        lineExtremityPointLyr = self.algRunner.runExtractSpecificVertices(
            inputLyr=inputLyr,
            vertices="0" if startPoint else "-1",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(
            lineExtremityPointLyr, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        extractedPoints = self.algRunner.runExtractByLocation(
            lineExtremityPointLyr,
            boundsBuffer,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(3)
        expression = (
            f"featid in {tuple(i['featid'] for i in extractedPoints.getFeatures())}"
        )
        linesToExtend = self.algRunner.runFilterExpression(
            inputLyr=inputLyr,
            expression=expression,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(4)
        extendedLines = self.algRunner.runExtendLines(
            linesToExtend,
            startDistance=tol if startPoint else 0,
            endDistance=0 if startPoint else tol,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(5)
        nFeats = extendedLines.featureCount()
        if nFeats == 0:
            return
        stepSize = 100 / nFeats
        originalFeaturesToUpdateDict = {
            feat["featid"]: feat for feat in inputLyr.getFeatures(expression)
        }
        inputLyr.startEditing()
        editText = (
            "Extending lines from start points."
            if startPoint
            else "Extending lines from end points."
        )
        inputLyr.beginEditCommand(editText)
        for current, feat in enumerate(extendedLines.getFeatures()):
            if multiStepFeedback.isCanceled():
                return

            inputLyr.changeGeometry(
                originalFeaturesToUpdateDict[feat["featid"]].id(),
                feat.geometry(),
                skipDefaultValue=True,
            )
            multiStepFeedback.setProgress(stepSize * current)
        inputLyr.endEditCommand()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "extendlinestogeographicbounds"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Extend Lines To Geographic Bounds Algorithm")

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
        return QCoreApplication.translate(
            "ExtendLinesToGeographicBoundsAlgorithm", string
        )

    def createInstance(self):
        return ExtendLinesToGeographicBoundsAlgorithm()
