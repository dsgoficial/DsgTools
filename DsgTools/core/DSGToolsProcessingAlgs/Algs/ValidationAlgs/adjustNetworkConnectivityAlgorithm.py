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
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class AdjustNetworkConnectivityAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.TOLERANCE,
                self.tr("Snap radius"),
                parentParameterName=self.INPUT,
                minValue=0,
                defaultValue=1.0,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        if inputLyr is None or inputLyr.featureCount() == 0:
            return {}
        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(
            self.tr("Identifying dangles on {layer}...").format(layer=inputLyr.name())
        )
        dangleLyr = algRunner.runIdentifyDangles(
            inputLyr,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        if dangleLyr.featureCount() == 0:
            return {}

        multiStepFeedback.setCurrentStep(1)
        if multiStepFeedback.isCanceled():
            return {}
        layerHandler.filterDangles(dangleLyr, tol, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        if multiStepFeedback.isCanceled():
            return {}
        algRunner.runCreateSpatialIndex(inputLyr=dangleLyr, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
        multiStepFeedback.setCurrentStep(3)
        if multiStepFeedback.isCanceled():
            return {}
        multiStepFeedback.pushInfo(self.tr("Finding original segments"))
        algRunner.runCreateSpatialIndex(inputLyr=dangleLyr, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
        originalSegments = algRunner.runExtractByLocation(
            inputLyr=inputLyr,
            intersectLyr=dangleLyr,
            context=context,
            predicate=[algRunner.Disjoint],
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        multiStepFeedback.setCurrentStep(4)
        if multiStepFeedback.isCanceled():
            return {}
        algRunner.runCreateSpatialIndex(inputLyr=originalSegments, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
        multiStepFeedback.setCurrentStep(5)
        if multiStepFeedback.isCanceled():
            return {}
        multiStepFeedback.pushInfo(
            self.tr("Snapping layer {layer} to dangles...").format(
                layer=inputLyr.name()
            )
        )
        snappedDangles = algRunner.runSnapGeometriesToLayer(
            inputLayer=dangleLyr,
            referenceLayer=originalSegments,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
            behavior=algRunner.PreferClosestDoNotInsertNewVertices,
            is_child_algorithm=True,
        )
        multiStepFeedback.setCurrentStep(6)
        if multiStepFeedback.isCanceled():
            return {}
        algRunner.runSnapLayerOnLayer(
            inputLayer=inputLyr,
            referenceLayer=snappedDangles,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
            behavior=algRunner.PreferClosestInsertExtraVerticesWhereRequired,
        )
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "adjustnetworkconnectivity"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Adjust Network Connectivity")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Network Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Network Processes"

    def tr(self, string):
        return QCoreApplication.translate("AdjustNetworkConnectivityAlgorithm", string)

    def createInstance(self):
        return AdjustNetworkConnectivityAlgorithm()
