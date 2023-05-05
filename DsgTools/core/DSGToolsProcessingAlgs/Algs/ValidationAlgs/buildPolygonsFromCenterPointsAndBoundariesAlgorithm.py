# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-18
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

import concurrent.futures
import os
from uuid import uuid4
from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
import processing
from processing.tools import dataobjects
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsFields,
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
    QgsProcessingUtils,
    QgsVectorLayer,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingContext,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class BuildPolygonsFromCenterPointsAndBoundariesAlgorithm(ValidationAlgorithm):
    INPUT_CENTER_POINTS = "INPUT_CENTER_POINTS"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    BOUNDARY_LINE_LAYER = "BOUNDARY_LINE_LAYER"
    CONSTRAINT_LINE_LAYERS = "CONSTRAINT_LINE_LAYERS"
    CONSTRAINT_POLYGON_LAYERS = "CONSTRAINT_POLYGON_LAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    SUPPRESS_AREA_WITHOUT_CENTROID_FLAG = "SUPPRESS_AREA_WITHOUT_CENTROID_FLAG"
    CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS = (
        "CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS"
    )
    MERGE_OUTPUT_POLYGONS = "MERGE_OUTPUT_POLYGONS"
    GROUP_BY_SPATIAL_PARTITION = "GROUP_BY_SPATIAL_PARTITION"
    OUTPUT_POLYGONS = "OUTPUT_POLYGONS"
    INVALID_POLYGON_LOCATION = "INVALID_POLYGON_LOCATION"
    UNUSED_BOUNDARY_LINES = "UNUSED_BOUNDARY_LINES"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_CENTER_POINTS,
                self.tr("Center Point Layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT_CENTER_POINTS",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.BOUNDARY_LINE_LAYER,
                self.tr("Line Boundary"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_LINE_LAYERS,
                self.tr("Line Constraint Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_POLYGON_LAYERS,
                self.tr("Polygon Constraint Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.MERGE_OUTPUT_POLYGONS,
                self.tr("Merge output polygons with same attribute set"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS,
                self.tr("Check output polygons for invalid geometries"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SUPPRESS_AREA_WITHOUT_CENTROID_FLAG,
                self.tr("Suppress area without center point flag"),
                defaultValue=False,
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
                self.OUTPUT_POLYGONS, self.tr("Output Polygons")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.INVALID_POLYGON_LOCATION,
                self.tr("Invalid Polygon Location Flags from {0}").format(
                    self.displayName()
                ),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.UNUSED_BOUNDARY_LINES,
                self.tr("Unused Boundary Flags from {0}").format(self.displayName()),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("Polygon Flags from {0}").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputCenterPointLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_CENTER_POINTS, context
        )
        if inputCenterPointLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT_CENTER_POINTS)
            )
        boundaryLineLyr = self.parameterAsVectorLayer(
            parameters, self.BOUNDARY_LINE_LAYER, context
        )
        constraintLineLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_LINE_LAYERS, context
        )
        if boundaryLineLyr is None and constraintLineLyrList == []:
            raise QgsProcessingException(
                self.tr(
                    "There must be at least one boundary layer or one constraint line list."
                )
            )
        constraintPolygonLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_POLYGON_LAYERS, context
        )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        fields = self.layerHandler.getFieldsFromAttributeBlackList(
            inputCenterPointLyr, attributeBlackList
        )
        groupBySpatialPartition = self.parameterAsBool(
            parameters, self.GROUP_BY_SPATIAL_PARTITION, context
        )
        (output_polygon_sink, output_polygon_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_POLYGONS,
            context,
            fields,
            QgsWkbTypes.Polygon,
            inputCenterPointLyr.sourceCrs(),
        )
        suppressPolygonWithoutCenterPointFlag = self.parameterAsBool(
            parameters, self.SUPPRESS_AREA_WITHOUT_CENTROID_FLAG, context
        )
        checkInvalidOnOutput = self.parameterAsBool(
            parameters, self.CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS, context
        )
        mergeOutput = self.parameterAsBool(
            parameters, self.MERGE_OUTPUT_POLYGONS, context
        )

        self.prepareFlagSink(
            parameters, inputCenterPointLyr, QgsWkbTypes.Polygon, context
        )
        (
            unused_boundary_flag_sink,
            unused_boundary_flag_sink_id,
        ) = self.parameterAsSink(
            parameters,
            self.UNUSED_BOUNDARY_LINES,
            context,
            boundaryLineLyr.fields() if boundaryLineLyr is not None else QgsFields(),
            QgsWkbTypes.LineString,
            boundaryLineLyr.sourceCrs()
            if boundaryLineLyr is not None
            else inputCenterPointLyr.sourceCrs(),
        )
        nSteps = (
            3 + (mergeOutput + 1) + checkInvalidOnOutput
        )  # boolean sum, if true, sums 1 to each term
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        polygonFeatList, flagDict = (
            self.computePolygonsFromCenterPointAndBoundaries(
                context,
                inputCenterPointLyr,
                boundaryLineLyr,
                constraintLineLyrList,
                constraintPolygonLyrList,
                onlySelected,
                geographicBoundaryLyr,
                attributeBlackList,
                suppressPolygonWithoutCenterPointFlag,
                multiStepFeedback,
            )
            if not groupBySpatialPartition or geographicBoundaryLyr.featureCount() <= 1
            else self.computePolygonsFromCenterPointAndBoundariesGroupingBySpatialPartition(
                context,
                inputCenterPointLyr,
                boundaryLineLyr,
                constraintLineLyrList,
                constraintPolygonLyrList,
                onlySelected,
                geographicBoundaryLyr,
                attributeBlackList,
                suppressPolygonWithoutCenterPointFlag,
                multiStepFeedback,
            )
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        invalid_polygon_sink, invalid_polygon_sink_id = self.prepareInvalidPolygonFlags(
            parameters, context, inputCenterPointLyr
        )
        currentStep += 1
        sink, sink_id = QgsProcessingUtils.createFeatureSink(
            "memory:",
            context,
            fields,
            QgsWkbTypes.Polygon,
            inputCenterPointLyr.sourceCrs(),
        )
        sink.addFeatures(polygonFeatList, QgsFeatureSink.FastInsert)

        multiStepFeedback.setCurrentStep(currentStep)
        self.checkUnusedBoundariesAndWriteOutput(
            context,
            boundaryLineLyr,
            geographicBoundaryLyr,
            sink_id,
            unused_boundary_flag_sink,
            multiStepFeedback,
        )
        currentStep += 1

        if mergeOutput:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Dissolving output..."))
            dissolvedLyr = self.algRunner.runDissolve(
                sink_id,
                context,
                feedback=multiStepFeedback,
                field=[field.name() for field in fields],
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            dissolvedLyr = self.algRunner.runMultipartToSingleParts(
                dissolvedLyr, context=context, feedback=multiStepFeedback
            )
            polygonFeatList = [feat for feat in dissolvedLyr.getFeatures()]
            currentStep += 1
        self.writeOutputPolygons(
            output_polygon_sink, multiStepFeedback, polygonFeatList, flagDict
        )
        currentStep += 1
        if checkInvalidOnOutput:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Checking invalid geometries..."))
            self.checkInvalidOnOutput(
                inputCenterPointLyr,
                multiStepFeedback,
                polygonFeatList,
                invalid_polygon_sink,
            )
            currentStep += 1

        return {
            self.OUTPUT_POLYGONS: output_polygon_sink_id,
            self.FLAGS: self.flag_id,
            self.INVALID_POLYGON_LOCATION: invalid_polygon_sink_id,
            self.UNUSED_BOUNDARY_LINES: unused_boundary_flag_sink_id,
        }

    def checkUnusedBoundariesAndWriteOutput(
        self,
        context,
        boundaryLineLyr,
        geographicBoundaryLyr,
        output_polygon_sink_id,
        unused_boundary_flag_sink,
        feedback,
    ):
        if boundaryLineLyr is None:
            return
        nSteps = 9 if geographicBoundaryLyr is None else 11
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setProgressText(self.tr("Checking unused boundaries..."))
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building cache..."))
        builtPolygonsLyr = processing.run(
            "native:addautoincrementalfield",
            parameters={
                "INPUT": output_polygon_sink_id,
                "FIELD_NAME": "featid",
                "START": 1,
                "GROUP_FIELDS": [],
                "SORT_EXPRESSION": "",
                "SORT_ASCENDING": True,
                "SORT_NULLS_FIRST": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )["OUTPUT"]
        currentStep += 1

        multiStepFeedback.setProgressText(self.tr("Converting built polygons to lines..."))
        multiStepFeedback.setCurrentStep(currentStep)
        polygonLines = self.algRunner.runPolygonsToLines(
            inputLyr=builtPolygonsLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setProgressText(self.tr("Exploding lines..."))
        multiStepFeedback.setCurrentStep(currentStep)
        explodedPolygonLines = self.algRunner.runExplodeLines(
            inputLyr=polygonLines,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setProgressText(self.tr("Building spatial index..."))
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=explodedPolygonLines,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        multiStepFeedback.setProgressText(self.tr("Exploding boudary lines..."))
        multiStepFeedback.setCurrentStep(currentStep)
        segments = self.algRunner.runExplodeLines(
            boundaryLineLyr, context, feedback=multiStepFeedback, is_child_algorithm=True,
        )
        currentStep += 1

        self.algRunner.runCreateSpatialIndex(
            inputLyr=segments,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        if geographicBoundaryLyr is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            segments = self.algRunner.runClip(
                segments,
                geographicBoundaryLyr,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            currentStep += 1
            self.algRunner.runCreateSpatialIndex(
                inputLyr=segments,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            currentStep += 1

        multiStepFeedback.setProgressText(self.tr("Running spatial join..."))
        multiStepFeedback.setCurrentStep(currentStep)
        unmatchedLines = processing.run(
            "native:joinattributesbylocation",
            {
                'INPUT':segments,
                'PREDICATE':[2],
                'JOIN':polygonLines,
                'JOIN_FIELDS':[],
                'METHOD':0,
                'DISCARD_NONMATCHING':False,
                'PREFIX':'',
                'NON_MATCHING':'memory:',
            },
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )['NON_MATCHING']
        
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing unused boundaries flags..."))
        self.algRunner.runCreateSpatialIndex(
            inputLyr=unmatchedLines,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        multiStepFeedback.setCurrentStep(currentStep)
        mergedSegments = processing.run(
            "native:dissolve",
            {"INPUT": unmatchedLines, "OUTPUT": "memory:"},
            context=context,
            feedback=multiStepFeedback,
        )["OUTPUT"]
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        flagLyr = self.algRunner.runMultipartToSingleParts(
            mergedSegments, context, feedback=multiStepFeedback
        )
        unused_boundary_flag_sink.addFeatures(
            flagLyr.getFeatures(), QgsFeatureSink.FastInsert
        )

    def checkInvalidOnOutput(
        self,
        inputCenterPointLyr,
        feedback,
        polygonFeatList,
        invalid_polygon_sink,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setProgressText(
            self.tr("Checking for invalid geometries on output polygons...")
        )
        multiStepFeedback.setCurrentStep(0)
        invalidGeomFlagDict, _ = self.layerHandler.identifyInvalidGeometries(
            polygonFeatList,
            len(polygonFeatList),
            inputCenterPointLyr,
            ignoreClosed=False,
            fixInput=False,
            parameterDict=None,
            geometryType=None,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        flagLambda = lambda x: self.flagFeature(
            flagGeom=x[1]["geom"], flagText=x[1]["reason"], sink=invalid_polygon_sink
        )
        list(map(flagLambda, invalidGeomFlagDict.items()))

    def prepareInvalidPolygonFlags(self, parameters, context, inputCenterPointLyr):
        (invalid_polygon_sink, invalid_polygon_sink_id) = self.parameterAsSink(
            parameters,
            self.INVALID_POLYGON_LOCATION,
            context,
            self.getFlagFields(),
            QgsWkbTypes.Point,
            inputCenterPointLyr.sourceCrs(),
        )

        return invalid_polygon_sink, invalid_polygon_sink_id

    def writeOutputPolygons(
        self, output_polygon_sink, multiStepFeedback, polygonFeatList, flagDict
    ):
        multiStepFeedback.setProgressText(self.tr("Writing output..."))
        output_polygon_sink.addFeatures(polygonFeatList, QgsFeatureSink.FastInsert)
        nItems = len(flagDict)
        for current, (flagGeom, flagText) in enumerate(flagDict.items()):
            if multiStepFeedback.isCanceled():
                break
            self.flagFeature(flagGeom, flagText, fromWkb=True)
            multiStepFeedback.setProgress(current * 100 / nItems)

    def computePolygonsFromCenterPointAndBoundaries(
        self,
        context,
        inputCenterPointLyr,
        boundaryLineLyr,
        constraintLineLyrList,
        constraintPolygonLyrList,
        onlySelected,
        geographicBoundaryLyr,
        attributeBlackList,
        suppressPolygonWithoutCenterPointFlag,
        multiStepFeedback,
    ):
        multiStepFeedback.pushInfo(
            self.tr("Starting {0}...").format(self.displayName())
        )
        multiStepFeedback.setProgressText(
            self.tr("Computing polygons from center points and boundaries...")
        )
        (
            polygonFeatList,
            flagDict,
        ) = self.layerHandler.getPolygonsFromCenterPointsAndBoundaries(
            inputCenterPointLyr,
            geographicBoundaryLyr=geographicBoundaryLyr,
            constraintLineLyrList=constraintLineLyrList + [boundaryLineLyr]
            if boundaryLineLyr is not None
            else constraintLineLyrList,
            constraintPolygonLyrList=constraintPolygonLyrList,
            onlySelected=onlySelected,
            suppressPolygonWithoutCenterPointFlag=suppressPolygonWithoutCenterPointFlag,
            context=context,
            feedback=multiStepFeedback,
            attributeBlackList=attributeBlackList,
            algRunner=self.algRunner,
        )

        return polygonFeatList, flagDict

    def computePolygonsFromCenterPointAndBoundariesGroupingBySpatialPartition(
        self,
        context,
        inputCenterPointLyr,
        boundaryLineLyr,
        constraintLineLyrList,
        constraintPolygonLyrList,
        onlySelected,
        geographicBoundaryLyr,
        attributeBlackList,
        suppressPolygonWithoutCenterPointFlag,
        feedback,
    ):
        polygonFeatList = []
        flagDict = dict()
        nSteps = 5 + 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Splitting geographic bounds"))
        geographicBoundaryLayerList = self.layerHandler.createMemoryLayerForEachFeature(
            layer=geographicBoundaryLyr, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing constraint lines"))
        constraintLinesLyr = (
            self.algRunner.runMergeVectorLayers(
                inputList=constraintLineLyrList,
                context=context,
                feedback=multiStepFeedback,
            )
            if len(constraintLineLyrList) > 0
            else None
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if constraintLinesLyr is not None:
            self.algRunner.runCreateSpatialIndex(
                constraintLinesLyr, context, multiStepFeedback
            )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing constraint polygons"))
        constraintPolygonsLyr = (
            self.algRunner.runMergeVectorLayers(
                inputList=constraintPolygonLyrList,
                context=context,
                feedback=multiStepFeedback,
            )
            if len(constraintPolygonLyrList) > 0
            else None
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if constraintPolygonsLyr is not None:
            self.algRunner.runCreateSpatialIndex(
                constraintPolygonsLyr, context, multiStepFeedback
            )
        currentStep += 1

        def compute(localGeographicBoundsLyr):
            context = QgsProcessingContext()
            if multiStepFeedback.isCanceled():
                return [], {}
            localInputCenterPointLyr = self.extractFeaturesUsingGeographicBounds(
                inputLyr=inputCenterPointLyr,
                geographicBounds=localGeographicBoundsLyr,
                feedback=None,
                context=context,
                onlySelected=onlySelected,
            )
            if multiStepFeedback.isCanceled():
                return [], {}
            localBoundaryLineLyr = self.extractFeaturesUsingGeographicBounds(
                inputLyr=boundaryLineLyr,
                geographicBounds=localGeographicBoundsLyr,
                feedback=None,
                context=context,
                onlySelected=onlySelected,
            )
            if multiStepFeedback.isCanceled():
                return [], {}
            localLinesConstraintLyr = (
                self.extractFeaturesUsingGeographicBounds(
                    inputLyr=constraintLinesLyr,
                    geographicBounds=localGeographicBoundsLyr,
                    feedback=None,
                    context=context,
                    onlySelected=onlySelected,
                )
                if constraintLinesLyr is not None
                else None
            )
            if multiStepFeedback.isCanceled():
                return [], {}
            localPolygonsConstraintLyr = (
                self.extractFeaturesUsingGeographicBounds(
                    inputLyr=constraintPolygonsLyr,
                    geographicBounds=localGeographicBoundsLyr,
                    feedback=None,
                    context=context,
                    onlySelected=onlySelected,
                )
                if constraintPolygonsLyr is not None
                else None
            )
            if multiStepFeedback.isCanceled():
                return [], {}
            return self.layerHandler.getPolygonsFromCenterPointsAndBoundariesAlt(
                localInputCenterPointLyr,
                geographicBoundaryLyr=localGeographicBoundsLyr,
                constraintLineLyrList=[localLinesConstraintLyr, localBoundaryLineLyr]
                if localLinesConstraintLyr is not None
                else [localBoundaryLineLyr],
                constraintPolygonLyrList=[localPolygonsConstraintLyr]
                if localPolygonsConstraintLyr is not None
                else [],
                onlySelected=False,  # the selected features were already filtered
                suppressPolygonWithoutCenterPointFlag=suppressPolygonWithoutCenterPointFlag,
                context=context,
                feedback=None,
                attributeBlackList=attributeBlackList,
                algRunner=AlgRunner(),
            )

        multiStepFeedback.setCurrentStep(currentStep)
        nRegions = len(geographicBoundaryLayerList)
        if nRegions == 0:
            return polygonFeatList, flagDict
        stepSize = 100 / nRegions
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        multiStepFeedback.setProgressText(
            self.tr("Submitting building polygon tasks to thread...")
        )
        for current, localGeographicBoundsLyr in enumerate(
            geographicBoundaryLayerList, start=0
        ):
            if multiStepFeedback.isCanceled():
                pool.shutdown(cancel_futures=True)
                break
            futures.add(pool.submit(compute, localGeographicBoundsLyr))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Evaluating results..."))
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                pool.shutdown(cancel_futures=True)
                break
            localPolygonFeatList, localFlagDict = future.result()
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Building polygons from region {current+1}/{nRegions} is done."
                )
            )
            multiStepFeedback.setProgress(current * stepSize)
            polygonFeatList += localPolygonFeatList
            flagDict.update(localFlagDict)
        return polygonFeatList, flagDict

    def checkUnusedBoundariesAndWriteOutputGroupingBySpatialPartition(
        self,
        context,
        boundaryLineLyr,
        geographicBoundaryLyr,
        output_polygon_sink_id,
        unused_boundary_flag_sink,
        feedback,
    ):
        if boundaryLineLyr is None:
            return
        nRegions = geographicBoundaryLyr.featureCount()
        if nRegions == 0:
            return
        nSteps = 5
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setProgressText(self.tr("Checking unused boundaries..."))
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures: creating local cache..."))
        polygonLyr = self.algRunner.runAddAutoIncrementalField(
            inputLyr=output_polygon_sink_id,
            fieldName="featid",
            context=context,
            feedback=multiStepFeedback,   
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=polygonLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1


        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Splitting geographic bounds"))
        geographicBoundaryLayerList = self.layerHandler.createMemoryLayerForEachFeature(
            layer=geographicBoundaryLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        def compute(localGeographicBoundsLyr):
            context = QgsProcessingContext()
            algRunner = AlgRunner()
            if multiStepFeedback.isCanceled():
                return
            localBoundaries = algRunner.runClip(
                boundaryLineLyr,
                localGeographicBoundsLyr,
                context=context,
                feedback=None,
                is_child_algorithm=True,
            )
            if multiStepFeedback.isCanceled():
                return
            localBoundaries = algRunner.runAddAutoIncrementalField(
                inputLyr=localBoundaries,
                fieldName="local_featid",
                context=context,
                feedback=None
            )
            if multiStepFeedback.isCanceled():
                return
            segments = self.algRunner.runExplodeLines(
                localBoundaries, context, feedback=None, is_child_algorithm=True
            )
            if multiStepFeedback.isCanceled():
                return
            segments = algRunner.runAddAutoIncrementalField(
                inputLyr=segments,
                fieldName="seg_featid",
                context=context,
                feedback=None
            )
            if multiStepFeedback.isCanceled():
                return
            flags = SpatialRelationsHandler().checkDE9IM(
                layerA=segments,
                layerB=polygonLyr,
                mask="*1*******",
                cardinality="1..*",
                feedback=None,
                ctx=context,
            )
            if multiStepFeedback.isCanceled():
                return
            featidList = list(
                set(i["seg_featid"] for i in segments.getFeatures(list(flags.keys())))
            )
            if multiStepFeedback.isCanceled():
                return
            if len(featidList) == 0:
                return
            expressionStr = f"seg_featid in {tuple(featidList)}"
            if ",)" in expressionStr:
                expressionStr = expressionStr.replace(",)", ")")
            segmentedFlags = algRunner.runFilterExpression(
                segments,
                expression=expressionStr,
                context=context,
                feedback=None,
            )
            if multiStepFeedback.isCanceled():
                return
            mergedSegments = processing.run(
                "native:dissolve",
                {"INPUT": segmentedFlags, "OUTPUT": "memory:"},
                context=context,
                feedback=None,
            )["OUTPUT"]
            if multiStepFeedback.isCanceled():
                return
            flagLyr = algRunner.runMultipartToSingleParts(
                mergedSegments, context, feedback=None
            )
            return flagLyr


        multiStepFeedback.setCurrentStep(currentStep)

        stepSize = 100 / nRegions
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        multiStepFeedback.pushInfo(
            self.tr("Submitting verifying unused boundaries tasks to thread...")
        )
        for current, localGeographicBoundsLyr in enumerate(
            geographicBoundaryLayerList, start=0
        ):
            if multiStepFeedback.isCanceled():
                pool.shutdown(cancel_futures=True)
                break
            futures.add(pool.submit(compute, localGeographicBoundsLyr))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.pushInfo(self.tr("Evaluating results..."))
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            localFlagLyr = future.result()
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Verifying unused boundaries from region {current+1}/{nRegions} is done."
                )
            )
            multiStepFeedback.setProgress(current * stepSize)
            if localFlagLyr is None or localFlagLyr.featureCount() == 0:
                continue
            unused_boundary_flag_sink.addFeatures(
                localFlagLyr.getFeatures(), QgsFeatureSink.FastInsert
            )

    def extractFeaturesUsingGeographicBounds(
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
        return "buildpolygonsfromcenterpointsandboundariesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Build Polygons From Center Points and Boundaries")

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
            "BuildPolygonsFromCenterPointsAndBoundariesAlgorithm", string
        )

    def createInstance(self):
        return BuildPolygonsFromCenterPointsAndBoundariesAlgorithm()
