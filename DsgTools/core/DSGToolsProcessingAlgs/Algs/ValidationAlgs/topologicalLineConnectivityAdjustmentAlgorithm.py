# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsProcessingException,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class TopologicalLineConnectivityAdjustment(ValidationAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Search Radius"),
            parentParameterName=self.INPUT_LAYERS,
            defaultValue=1e-6,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT_LAYERS)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(13, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runRemoveSmallLines(
            inputLyr=coverage,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        coverage.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        outputLyr = algRunner.runSnapGeometriesToLayer(
            coverage,
            coverage,
            tol,
            context,
            feedback=multiStepFeedback,
            behavior=AlgRunner.SnapToAnchorNodes,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runRemoveSmallLines(
            inputLyr=outputLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        outputLyr.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        dangleLyr = algRunner.runIdentifyDangles(
            outputLyr,
            tol,
            context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        currentStep += 1
        if dangleLyr.featureCount() == 0:
            return {}

        multiStepFeedback.setCurrentStep(currentStep)
        dangleSnappedToGrid = algRunner.runSnapToGrid(
            inputLayer=dangleLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runRemoveDuplicatedGeometries(
            inputLyr=dangleSnappedToGrid,
            context=context,
            feedback=multiStepFeedback,
        )
        dangleSnappedToGrid.commitChanges()
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        outputAfterSnapToDangleLyr = algRunner.runSnapGeometriesToLayer(
            outputLyr,
            dangleSnappedToGrid,
            tol,
            context,
            feedback=multiStepFeedback,
            behavior=AlgRunner.AlignNodesDoNotInsertNewVertices,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runRemoveSmallLines(
            inputLyr=outputLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        outputLyr.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        fixedNodesLyr = algRunner.runRemoveDuplicateVertex(
            inputLyr=outputAfterSnapToDangleLyr,
            tolerance=1e-7,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runRemoveSmallLines(
            inputLyr=outputLyr,
            tol=tol,
            context=context,
            feedback=multiStepFeedback,
        )
        outputLyr.commitChanges()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        fixedNull = algRunner.runRemoveNull(
            inputLayer=fixedNodesLyr,
            context=context,
            feedback=multiStepFeedback
        )
        
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Updating original layers..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, fixedNull, feedback=multiStepFeedback
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
        return "topologicallineconnectivityadjustment"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Topological adjustment of the connectivity of lines")

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
        return QCoreApplication.translate(
            "TopologicalLineConnectivityAdjustment", string
        )

    def createInstance(self):
        return TopologicalLineConnectivityAdjustment()
