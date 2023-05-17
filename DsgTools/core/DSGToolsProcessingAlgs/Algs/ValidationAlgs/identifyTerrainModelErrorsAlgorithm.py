# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
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
import concurrent.futures
import os
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingContext,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler

from .validationAlgorithm import ValidationAlgorithm


class IdentifyTerrainModelErrorsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    CONTOUR_INTERVAL = "CONTOUR_INTERVAL"
    GEOGRAPHIC_BOUNDS = "GEOGRAPHIC_BOUNDS"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    INPUT_ELEVATION_POINTS = "INPUT_ELEVATION_POINTS"
    ELEVATION_POINT_ATTR = "ELEVATION_POINT_ATTR"
    GROUP_BY_SPATIAL_PARTITION = "GROUP_BY_SPATIAL_PARTITION"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input contour layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CONTOUR_ATTR,
                self.tr("Contour value field"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_ELEVATION_POINTS,
                self.tr("Input elevation points layer"),
                [QgsProcessing.TypeVectorPoint],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ELEVATION_POINT_ATTR,
                self.tr("Elevation point height value field"),
                None,
                "INPUT_ELEVATION_POINTS",
                QgsProcessingParameterField.Any,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL, self.tr("Threshold"), minValue=0, defaultValue=10
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic bounds layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.GROUP_BY_SPATIAL_PARTITION,
                self.tr("Run algothimn grouping by spatial partition"),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS, self.tr("{0} Point Flags").format(self.displayName())
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS, self.tr("{0} Line Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.spatialRealtionsHandler = SpatialRelationsHandler()
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        heightFieldName = self.parameterAsFields(
            parameters, self.CONTOUR_ATTR, context
        )[0]
        threshold = self.parameterAsDouble(parameters, self.CONTOUR_INTERVAL, context)
        geoBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDS, context
        )
        groupBySpatialPartition = self.parameterAsBool(
            parameters, self.GROUP_BY_SPATIAL_PARTITION, context
        )
        elevationPointsLyr = self.parameterAsVectorLayer(parameters, self.INPUT_ELEVATION_POINTS, context)
        elevationPointHeightFieldName = self.parameterAsFields(
            parameters, self.ELEVATION_POINT_ATTR, context
        )[0]
        if elevationPointsLyr is not None and elevationPointHeightFieldName in (None, [], ''):
            raise QgsProcessingException(self.tr('Elevation point height attribute must be selected.'))
        point_flagSink, point_flag_id = self.prepareAndReturnFlagSink(
            parameters, inputLyr, QgsWkbTypes.Point, context, self.POINT_FLAGS
        )
        line_flagSink, line_flag_id = self.prepareAndReturnFlagSink(
            parameters, inputLyr, QgsWkbTypes.LineString, context, self.LINE_FLAGS
        )

        invalidDict = (
            self.spatialRealtionsHandler.validateTerrainModel(
                contourLyr=inputLyr,
                onlySelected=onlySelected,
                heightFieldName=heightFieldName,
                elevationPointsLyr=elevationPointsLyr,
                elevationPointHeightFieldName=elevationPointHeightFieldName,
                threshold=threshold,
                geoBoundsLyr=geoBoundsLyr,
                feedback=feedback,
                context=context
            )
            if not groupBySpatialPartition
            else self.validateTerrainModelInParalel(
                contourLyr=inputLyr,
                onlySelected=onlySelected,
                heightFieldName=heightFieldName,
                elevationPointsLyr=elevationPointsLyr,
                elevationPointHeightFieldName=elevationPointHeightFieldName,
                threshold=threshold,
                geoBoundsLyr=geoBoundsLyr,
                context=context,
                feedback=feedback,
            )
        )

        for flagGeom, text in invalidDict.items():
            if feedback.isCanceled():
                break
            geom = QgsGeometry()
            geom.fromWkb(flagGeom)
            flagSink = (
                line_flagSink
                if geom.type() == QgsWkbTypes.LineGeometry
                else point_flagSink
            )
            self.flagFeature(geom, text, fromWkb=False, sink=flagSink)

        return {self.POINT_FLAGS: point_flag_id, self.LINE_FLAGS: line_flag_id}

    def validateTerrainModelInParalel(
        self,
        contourLyr,
        onlySelected,
        heightFieldName,
        elevationPointsLyr,
        threshold,
        geoBoundsLyr,
        context,
        feedback,
    ):
        flagDict = dict()
        nSteps = 3
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Splitting geographic bounds"))
        geographicBoundaryLayerList = self.layerHandler.createMemoryLayerForEachFeature(
            layer=geoBoundsLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        def compute(localGeographicBoundsLyr):
            localContext = QgsProcessingContext()
            if multiStepFeedback.isCanceled():
                return {}
            bufferedBounds = self.algRunner.runBuffer(
                inputLayer=localGeographicBoundsLyr,
                distance=1e-6,
                context=localContext,
                feedback=None,
            )
            if multiStepFeedback.isCanceled():
                return {}
            clippedContours = self.algRunner.runClip(
                inputLayer=contourLyr
                if not onlySelected
                else QgsProcessingFeatureSourceDefinition(contourLyr.id(), True),
                overlayLayer=bufferedBounds,
                context=localContext,
                feedback=None,
            )
            if multiStepFeedback.isCanceled():
                return {}
            singlePartContours = self.algRunner.runMultipartToSingleParts(
                inputLayer=clippedContours, context=localContext, feedback=None
            )
            if multiStepFeedback.isCanceled():
                return {}
            localElevationPointsLyr = self.algRunner.runExtractByLocation(
                inputLyr=elevationPointsLyr,
                intersectLyr=localGeographicBoundsLyr,
                context=localContext,
                feedback=None,
            ) if elevationPointsLyr is not None else None
            return self.spatialRealtionsHandler.validateTerrainModel(
                contourLyr=singlePartContours,
                onlySelected=False,
                heightFieldName=heightFieldName,
                elevationPointsLyr=localElevationPointsLyr,
                elevationPointHeightFieldName=elevationPointHeightFieldName,
                threshold=threshold,
                geoBoundsLyr=localGeographicBoundsLyr,
                feedback=None,
            )

        multiStepFeedback.setCurrentStep(currentStep)
        nRegions = len(geographicBoundaryLayerList)
        if nRegions == 0:
            return flagDict
        stepSize = 100 / nRegions
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        multiStepFeedback.pushInfo(
            self.tr(
                "Submitting terrain model problem identification by region tasks to thread..."
            )
        )
        for current, localGeographicBoundsLyr in enumerate(
            geographicBoundaryLayerList, start=0
        ):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(compute, localGeographicBoundsLyr))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.pushInfo(self.tr("Evaluating results..."))
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            localFlagDict = future.result()
            multiStepFeedback.pushInfo(
                self.tr(f"Identification of region {current+1}/{nRegions} is done.")
            )
            multiStepFeedback.setProgress(current * stepSize)
            flagDict.update(localFlagDict)
        return flagDict

    def extractFeaturesUsingBufferedGeographicBounds(
        self, inputLyr, geographicBounds, context, onlySelected=False, feedback=None
    ):
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        extractedLyr = self.algRunner.runExtractByLocation(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            intersectLyr=geographicBounds,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=extractedLyr, context=context, feedback=multiStepFeedback
        )
        return extractedLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyterrainmodelerrorsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Terrain Model Errors Algorithm")

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
        return QCoreApplication.translate("IdentifyTerrainModelErrorsAlgorithm", string)

    def createInstance(self):
        return IdentifyTerrainModelErrorsAlgorithm()
