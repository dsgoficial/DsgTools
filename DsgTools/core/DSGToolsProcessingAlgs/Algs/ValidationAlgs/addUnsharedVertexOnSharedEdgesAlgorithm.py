# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-10-07
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

from itertools import chain
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class AddUnsharedVertexOnSharedEdgesAlgorithm(ValidationAlgorithm):
    INPUT_LINES = "INPUT_LINES"
    INPUT_POLYGONS = "INPUT_POLYGONS"
    SELECTED = "SELECTED"
    SEARCH_RADIUS = "SEARCH_RADIUS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr("Polygon Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.SEARCH_RADIUS, self.tr("Search Radius"), defaultValue=1.0
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputLineLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_LINES, context
        )
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        if inputLineLyrList + inputPolygonLyrList == []:
            raise QgsProcessingException(self.tr("Select at least one layer"))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        geographicBoundary = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        lyrList = list(chain(inputLineLyrList, inputPolygonLyrList))
        nLyrs = len(lyrList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nLyrs + 4, feedback)
        multiStepFeedback.setCurrentStep(0)
        flagsLyr = algRunner.runIdentifyUnsharedVertexOnSharedEdgesAlgorithm(
            lineLayerList=inputLineLyrList,
            polygonLayerList=inputPolygonLyrList,
            onlySelected=onlySelected,
            searchRadius=searchRadius,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if geographicBoundary is not None:
            multiStepFeedback.setCurrentStep(1)
            flagsLyr = algRunner.runExtractByLocation(
                flagsLyr,
                geographicBoundary,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        flagsLyr = algRunner.runSnapLayerOnLayer(
            inputLayer=flagsLyr,
            referenceLayer=flagsLyr,
            tol=searchRadius,
            context=context,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
            behavior=6,
            buildCache=False,
            is_child_algorithm=True,
        )
        for current, lyr in enumerate(lyrList):
            if feedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(
                current + 2 + (geographicBoundary is not None)
            )
            algRunner.runSnapLayerOnLayer(
                inputLayer=lyr,
                referenceLayer=flagsLyr,
                tol=searchRadius,
                context=context,
                onlySelected=onlySelected,
                feedback=multiStepFeedback,
                behavior=1,
                is_child_algorithm=True,
            )
        currentStep = current + 1 + (geographicBoundary is not None)
        multiStepFeedback.setCurrentStep(currentStep)
        newFlagsLyr = algRunner.runIdentifyUnsharedVertexOnSharedEdgesAlgorithm(
            lineLayerList=inputLineLyrList,
            polygonLayerList=inputPolygonLyrList,
            onlySelected=onlySelected,
            searchRadius=searchRadius,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if geographicBoundary is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            newFlagsLyr = algRunner.runExtractByLocation(
                newFlagsLyr, geographicBoundary, context, feedback=multiStepFeedback
            )
            currentStep += 1
        if newFlagsLyr.featureCount() == 0:
            return {}
        multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        algRunner.runCreateSpatialIndex(
            newFlagsLyr, context, multiStepFeedback, is_child_algorithm=True
        )
        multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        LayerHandler().addVertexesToLayers(
            vertexLyr=newFlagsLyr,
            layerList=list(chain(inputLineLyrList, inputPolygonLyrList)),
            searchRadius=searchRadius,
            feedback=multiStepFeedback,
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
        return "addunsharedvertexonsharededgesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Add Unshared Vertex on Shared Edges")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Vertex Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Vertex Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "AddUnsharedVertexOnSharedEdgesAlgorithm", string
        )

    def createInstance(self):
        return AddUnsharedVertexOnSharedEdgesAlgorithm()
