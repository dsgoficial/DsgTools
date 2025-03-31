# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-07
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

import math
import os
import concurrent.futures
from typing import List, Optional, Set, Union
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools import graphHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsFields,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingUtils,
)

from DsgTools.core.Utils.threadingTools import concurrently

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class UnbuildPolygonsAlgorithmV2(ValidationAlgorithm):
    INPUT_POLYGONS = "INPUT_POLYGONS"
    SELECTED = "SELECTED"
    CONSTRAINT_LINE_LAYERS = "CONSTRAINT_LINE_LAYERS"
    CONSTRAINT_POLYGON_LAYERS = "CONSTRAINT_POLYGON_LAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    OUTPUT_CENTER_POINTS = "OUTPUT_CENTER_POINTS"
    OUTPUT_BOUNDARIES = "OUTPUT_BOUNDARIES"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr("Polygon Layers"),
                QgsProcessing.TypeVectorPolygon,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
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
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_CENTER_POINTS, self.tr("Output Center Points")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_BOUNDARIES, self.tr("Output Boundaries")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputPolygonLyrList = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        constraintLineLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_LINE_LAYERS, context
        )
        constraintPolygonLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_POLYGON_LAYERS, context
        )
        if set(constraintPolygonLyrList).intersection(set(inputPolygonLyrList)):
            raise QgsProcessingException(
                self.tr("Input polygon layers must not be in constraint polygon list.")
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        inputPolygonLyrIdSet = set(lyr.id() for lyr in inputPolygonLyrList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(20, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building single polygon layer"))
        singleInputPolygonBoundariesLayer = self.prepareLayerList(
            inputList=inputPolygonLyrList,
            context=context,
            feedback=multiStepFeedback,
            mergeOutputs=True,
            is_child_algorithm=False,
        )[0]
        multiStepFeedback.pushInfo(self.tr("Single polygon layer built successfully"))

        outputSinkFields = singleInputPolygonBoundariesLayer.fields()
        (output_center_point_sink, output_center_point_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_CENTER_POINTS,
            context,
            outputSinkFields,
            QgsWkbTypes.Point,
            singleInputPolygonBoundariesLayer.sourceCrs(),
        )
        (output_boundaries_sink, output_boundaries_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_BOUNDARIES,
            context,
            QgsFields(),
            QgsWkbTypes.LineString,
            singleInputPolygonBoundariesLayer.sourceCrs(),
        )
        if singleInputPolygonBoundariesLayer.featureCount() == 0:
            multiStepFeedback.pushInfo(
                self.tr("No features found in input layers. Processing complete.")
            )
            return {
                self.OUTPUT_CENTER_POINTS: output_center_point_sink_id,
                self.OUTPUT_BOUNDARIES: output_boundaries_sink_id,
            }
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Preparing constraint layers"))
        inputConstraintLyrList = constraintLineLyrList + constraintPolygonLyrList
        if geographicBoundaryLyr is not None:
            inputConstraintLyrList.append(geographicBoundaryLyr)
        constraintLyrList = self.prepareLayerList(
            inputList=inputConstraintLyrList,
            context=context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Constraint layers prepared successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Merging all line layers"))
        mergedLines = self.algRunner.runMergeVectorLayers(
            inputList=constraintLyrList + [singleInputPolygonBoundariesLayer],
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.pushInfo(self.tr("Merged all line layers successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Exploding lines at intersections"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating spatial index for merged lines"))
        self.algRunner.runCreateSpatialIndex(
            mergedLines, context, feedback, is_child_algorithm=True
        )
        multiStepFeedback.pushInfo(self.tr("Spatial index created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Splitting lines at intersections"))
        intersectedLines = self.splitLinesWithParallelProcessing(
            inputLyr=mergedLines,
            linesLyr=mergedLines,
            context=context,
            feedback=multiStepFeedback,
            threshold=10_000,
        )
        multiStepFeedback.pushInfo(
            self.tr("Lines split successfully at all intersections")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Creating feature ID field for each line segment")
        )
        intersectedLines = self.algRunner.runCreateFieldWithExpression(
            inputLyr=intersectedLines,
            expression="$id",
            fieldName="featid",
            fieldType=AlgRunner.FieldTypeInteger,
            feedback=multiStepFeedback,
            context=context,
            is_child_algorithm=False,
        )
        multiStepFeedback.pushInfo(self.tr("Feature ID field created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Identifying unique boundaries"))
        uniqueBoundariesIdSet = (
            self.getUniqueBoundariesIds(
                nx=nx,
                inputLyr=intersectedLines,
                referenceSet=inputPolygonLyrIdSet,
                feedback=multiStepFeedback,
            )
            if intersectedLines.featureCount() < 10000
            else self.getUniqueBoundariesIdsWithParallelProcessing(
                nx=nx,
                inputLyr=intersectedLines,
                referenceSet=inputPolygonLyrIdSet,
                geographicBoundaryLyr=geographicBoundaryLyr,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        multiStepFeedback.pushInfo(
            self.tr(f"Found {len(uniqueBoundariesIdSet)} unique boundary segments")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if len(uniqueBoundariesIdSet) > 0:
            multiStepFeedback.pushInfo(self.tr("Filtering unique boundary lines"))
            uniqueBoundaries = self.algRunner.runFilterExpression(
                inputLyr=intersectedLines,
                expression=f"\"featid\" IN ({','.join(map(str, uniqueBoundariesIdSet))})",
                context=context,
                feedback=multiStepFeedback,
            )
            multiStepFeedback.pushInfo(
                self.tr("Unique boundary lines filtered successfully")
            )

            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Merging connected line segments"))
            self.algRunner.runDSGToolsMergeLines(
                uniqueBoundaries,
                context=context,
                attributeBlackList=[f.name() for f in uniqueBoundaries.fields()],
                feedback=multiStepFeedback,
                allowClosed=False,
                lineFilterLyrList=constraintLyrList,
            )
            multiStepFeedback.pushInfo(self.tr("Line segments merged successfully"))

            outputBoundariesLambda = lambda x: output_boundaries_sink.addFeature(x)
            list(map(outputBoundariesLambda, uniqueBoundaries.getFeatures()))
            multiStepFeedback.pushInfo(
                self.tr(f"Added {uniqueBoundaries.featureCount()} boundaries to output")
            )
        else:
            multiStepFeedback.pushInfo(self.tr("No unique boundaries found to process"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Merging input polygon layers"))
        mergedInputPolygons = self.algRunner.runMergeVectorLayers(
            inputList=parameters[self.INPUT_POLYGONS],
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Input polygon layers merged successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating layer ID field"))
        mergedInputPolygons = self.algRunner.runCreateFieldWithExpression(
            mergedInputPolygons,
            fieldName="layer_id",
            expression='"layer"',
            fieldType=AlgRunner.FieldTypeText,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Layer ID field created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Creating spatial index for merged polygons")
        )
        self.algRunner.runCreateSpatialIndex(
            mergedInputPolygons,
            context,
            feedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Spatial index created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating polygons from line network"))
        polygonizeOutput = self.algRunner.runPolygonize(
            inputLyr=intersectedLines,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.pushInfo(
            self.tr(
                f"Created {polygonizeOutput.featureCount()} polygons from line network"
            )
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating center points for each polygon"))
        centerPointLayer = self.algRunner.runPointOnSurface(
            polygonizeOutput,
            context,
            allParts=True,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Center points created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Converting multipart geometries to single parts")
        )
        centerPointLayer = self.algRunner.runMultipartToSingleParts(
            inputLayer=centerPointLayer,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating spatial index for center points"))
        self.algRunner.runCreateSpatialIndex(
            centerPointLayer,
            context,
            feedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Spatial index created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Extracting center points inside input polygons")
        )
        centerPointsInsideInput = self.algRunner.runExtractByLocation(
            centerPointLayer,
            mergedInputPolygons,
            context,
            predicate=AlgRunner.Within,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.pushInfo(
            self.tr(
                f"Extracted {centerPointsInsideInput.featureCount()} center points inside polygons"
            )
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if geographicBoundaryLyr is not None:
            multiStepFeedback.pushInfo(
                self.tr("Filtering center points by geographic boundary")
            )
            centerPointsInsideInput = self.algRunner.runExtractByLocation(
                centerPointsInsideInput,
                geographicBoundaryLyr,
                context,
                predicate=AlgRunner.Within,
                feedback=multiStepFeedback,
            )
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Filtered to {centerPointsInsideInput.featureCount()} center points within boundary"
                )
            )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Creating spatial index for filtered center points")
        )
        self.algRunner.runCreateSpatialIndex(
            centerPointsInsideInput,
            context,
            feedback,
            is_child_algorithm=True,
        )
        multiStepFeedback.pushInfo(self.tr("Spatial index created successfully"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Joining polygon attributes to center points")
        )
        final_result_lyr = self.algRunner.runJoinAttributesByLocation(
            centerPointsInsideInput,
            mergedInputPolygons,
            context=context,
            predicateList=[AlgRunner.Intersects],
            method=0,  # Take attributes from the first located feature
            discardNonMatching=False,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.pushInfo(
            self.tr(
                f"Successfully joined attributes to {final_result_lyr.featureCount()} center points"
            )
        )

        def outputFeature(feat):
            newFeat = QgsFeature(outputSinkFields)
            featFieldNames = [f.name() for f in feat.fields()]
            for field in outputSinkFields:
                if field.name() not in featFieldNames:
                    continue
                newFeat[field.name()] = feat[field.name()]
            newFeat.setGeometry(feat.geometry())
            output_center_point_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

        count = 0
        for feat in final_result_lyr.getFeatures():
            outputFeature(feat)
            count += 1

        multiStepFeedback.pushInfo(
            self.tr(f"Added {count} center points to output sink")
        )
        multiStepFeedback.pushInfo(self.tr("Processing complete!"))

        return {
            self.OUTPUT_CENTER_POINTS: output_center_point_sink_id,
            self.OUTPUT_BOUNDARIES: output_boundaries_sink_id,
        }

    def prepareLayerList(
        self,
        inputList: List[QgsVectorLayer],
        context: QgsProcessingContext,
        feedback: QgsFeedback,
        onlySelected: Optional[bool] = False,
        mergeOutputs: Optional[bool] = False,
        is_child_algorithm: Optional[bool] = True,
    ) -> List[Union[str, QgsVectorLayer]]:
        """
        This method is called to prepare the input layers before processing.
        It can be used to perform any necessary operations on the layers,
        such as filtering, transforming, or modifying them.
        """
        nSteps = len(inputList) + mergeOutputs
        if len(inputList) == 0:
            return []
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        layerList = []
        for currentStep, lyr in enumerate(inputList):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr(f"Preparing layer: {lyr.name()}"))
            outputLyr = self.prepareLayer(
                lyr,
                onlySelected=onlySelected,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            layerList.append(outputLyr)
            multiStepFeedback.pushInfo(
                self.tr(f"Layer {lyr.name()} prepared successfully")
            )
        if not mergeOutputs:
            return layerList
        multiStepFeedback.setCurrentStep(currentStep + 1)
        multiStepFeedback.pushInfo(self.tr("Merging input layers"))
        mergedLayer = (
            self.algRunner.runMergeVectorLayers(
                inputList=layerList,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=is_child_algorithm,
            )
            if len(layerList) > 1
            else layerList[0]
        )
        if is_child_algorithm == False and isinstance(mergedLayer, str):
            mergedLayer = [QgsProcessingUtils.mapLayerFromString(mergedLayer, context)]
        multiStepFeedback.pushInfo(self.tr("Layers merged successfully"))
        return mergedLayer

    def prepareLayer(
        self,
        inputLyr: QgsVectorLayer,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsFeedback] = None,
        onlySelected: Optional[bool] = False,
        is_child_algorithm: Optional[bool] = True,
    ) -> List[Union[str, QgsVectorLayer]]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        localContext = QgsProcessingContext() if context is None else context
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Adding layer id attribute"))
        layerWithId = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(
                inputLyr.id(), selectedFeaturesOnly=True
            ),
            expression="@layer_id",
            fieldName="layer_id",
            fieldType=AlgRunner.FieldTypeText,
            feedback=feedback,
            context=localContext,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Layer ID attribute added successfully"))

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            if inputLyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                multiStepFeedback.pushInfo(self.tr("Converting polygons to lines"))
        linesLyr = (
            self.algRunner.runPolygonsToLines(
                inputLyr=layerWithId,
                context=localContext,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            if inputLyr.geometryType() == QgsWkbTypes.PolygonGeometry
            else layerWithId
        )
        if (
            multiStepFeedback is not None
            and inputLyr.geometryType() == QgsWkbTypes.PolygonGeometry
        ):
            multiStepFeedback.pushInfo(
                self.tr("Polygons converted to lines successfully")
            )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Converting multipart geometries to single parts")
            )
        singlePartsLyr = self.algRunner.runMultipartToSingleParts(
            inputLayer=linesLyr,
            context=localContext,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(
                self.tr("Multipart geometries converted successfully")
            )

        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Exploding lines"))
        explodedLinesLyr = self.algRunner.runExplodeLines(
            inputLyr=singlePartsLyr,
            context=localContext,
            feedback=multiStepFeedback,
            is_child_algorithm=is_child_algorithm,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Lines exploded successfully"))

        return explodedLinesLyr

    def getUniqueBoundariesIds(
        self,
        nx,
        inputLyr: QgsVectorLayer,
        referenceSet: Set[str],
        feedback=None,
    ) -> Set[int]:
        if feedback is not None:
            feedback.pushInfo(self.tr("Building network graph from line segments"))

        G = nx.Graph()
        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return set()
        stepSize = 100 / nFeats
        for i, feat in enumerate(inputLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            startPoint, endPoint = geom.asPolyline()[0], geom.asPolyline()[-1]
            if not G.has_edge(startPoint, endPoint):
                G.add_edge(startPoint, endPoint, layerIdSet=set(), featid=feat.id())
            G[startPoint][endPoint]["layerIdSet"].add(feat["layer_id"])
            if feedback is not None and i % 1000 == 0:
                feedback.setProgress(int(i * stepSize))
                feedback.pushInfo(self.tr(f"Processed {i} of {nFeats} line segments"))

        if feedback is not None:
            feedback.pushInfo(
                self.tr("Identifying boundaries belonging only to input layers")
            )
            feedback.setProgress(100)

        result = set(
            G[startPoint][endPoint]["featid"]
            for startPoint, endPoint in G.edges()
            if G[startPoint][endPoint]["layerIdSet"].issubset(referenceSet)
        )

        if feedback is not None:
            feedback.pushInfo(self.tr(f"Found {len(result)} unique boundary segments"))

        return result

    def getUniqueBoundariesIdsWithParallelProcessing(
        self,
        nx,
        inputLyr: QgsVectorLayer,
        referenceSet: Set[str],
        geographicBoundaryLyr: Optional[QgsVectorLayer] = None,
        context: Optional[QgsProcessingContext] = None,
        feedback: Optional[QgsFeedback] = None,
    ) -> Set[int]:
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback=feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Creating grid for parallel processing"))

        layerToSplit = (
            geographicBoundaryLyr
            if geographicBoundaryLyr is not None
            else self.algRunner.runPolygonFromLayerExtent(
                inputLayer=inputLyr,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        )
        multiStepFeedback.pushInfo(self.tr("Layer extent determined for grid creation"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Creating polygon grid for parallel processing")
        )
        cpuCount = os.cpu_count() // 2
        referencePolygonLayer = self.algRunner.runDSGToolsPolygonTiler(
            inputLayer=layerToSplit,
            context=context,
            feedback=multiStepFeedback,
            rows=cpuCount,
            columns=cpuCount,
            includePartial=True,
        )
        multiStepFeedback.pushInfo(
            self.tr(
                f"Created grid with {referencePolygonLayer.featureCount()} cells for parallel processing"
            )
        )

        outputSet = set()

        def compute(inputLyr: QgsVectorLayer, polygonTile: QgsVectorLayer) -> Set[int]:
            localContext = QgsProcessingContext()
            extractedLines = self.algRunner.runExtractByLocation(
                inputLyr=inputLyr,
                overlayLyr=polygonTile,
                context=localContext,
                predicate=AlgRunner.Intersects,
                feedback=None,
            )
            return self.getUniqueBoundariesIds(
                nx=nx,
                inputLyr=extractedLines,
                referenceSet=referenceSet,
            )

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Starting parallel processing of grid cells")
        )

        nFeats = referencePolygonLayer.featureCount()
        if nFeats == 0:
            return set()
        if nFeats == 1:
            multiStepFeedback.pushInfo(
                self.tr("Only one grid cell, reverting to single-process mode")
            )
            return self.getUniqueBoundariesIds(
                nx=nx,
                inputLyr=inputLyr,
                referenceSet=referenceSet,
                feedback=multiStepFeedback,
            )

        stepSize = 100 / nFeats
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for current, polygonTile in enumerate(referencePolygonLayer.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.pushInfo(
                self.tr(f"Submitting grid cell {current+1}/{nFeats} for processing")
            )
            tileLayer = self.layerHandler.createMemoryLayerWithFeature(
                layer=referencePolygonLayer, feat=polygonTile, context=context
            )
            futures.add(pool.submit(compute, inputLyr.clone(), tileLayer))
            multiStepFeedback.setProgress(current * stepSize)
            if current % 5 == 0 and current > 0:
                multiStepFeedback.pushInfo(
                    self.tr(
                        f"Submitted {current} of {nFeats} grid cells for processing"
                    )
                )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Collecting results from parallel processing")
        )
        processedCount = 0
        totalFutures = len(futures)
        stepSize = 100 / totalFutures if totalFutures > 0 else 100

        for future in concurrent.futures.as_completed(futures):
            if multiStepFeedback.isCanceled():
                break
            processedCount += 1
            result = future.result()
            outputSet.update(result)
            multiStepFeedback.setProgress(processedCount * stepSize)

            if processedCount % 5 == 0 or processedCount == totalFutures:
                multiStepFeedback.pushInfo(
                    self.tr(
                        f"Processed {processedCount}/{totalFutures} grid cells, found {len(outputSet)} unique boundaries so far"
                    )
                )

        multiStepFeedback.pushInfo(
            self.tr(
                f"Parallel processing complete. Total unique boundaries: {len(outputSet)}"
            )
        )
        return outputSet

    def splitLinesWithParallelProcessing(
        self,
        inputLyr,
        linesLyr,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
        threshold: Optional[int] = 10000,
    ) -> QgsVectorLayer:
        inputFeatureCount = inputLyr.featureCount()
        linesFeatureCount = linesLyr.featureCount()
        totalFeatureCount = inputFeatureCount + linesFeatureCount
        if totalFeatureCount <= threshold:
            feedback.pushInfo(
                self.tr(
                    f"Doing single threaded evaluation. Total feature count: {totalFeatureCount} > threshold: {threshold}"
                )
            )
            return self.algRunner.runSplitLinesWithLines(
                inputLyr=inputLyr,
                linesLyr=linesLyr,
                context=context,
                feedback=feedback,
                is_child_algorithm=is_child_algorithm,
            )
        cpuCount = os.cpu_count() or 4
        basePartitionCount = max(2, int(math.sqrt(totalFeatureCount / 1000)))
        partitionCount = min(cpuCount * 2, basePartitionCount)
        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr(
                f"Creating {partitionCount}x{partitionCount} grid for spatial partitioning"
            )
        )
        multiStepFeedback.pushInfo("Calculating combined extent")
        extentLayer = self.algRunner.runPolygonFromLayerExtent(
            inputLyr,
            context,
            roundTo=0.0,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo("Creating processing grid")

        # Create grid with the appropriate number of rows and columns
        gridLayer = self.algRunner.runDSGToolsPolygonTiler(
            extentLayer,
            rows=partitionCount,
            columns=partitionCount,
            context=context,
            includePartial=True,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo("Processing grid cells")

        # Calculate total number of cells for progress reporting
        cellCount = gridLayer.featureCount()
        cellStep = 100 / cellCount if cellCount > 0 else 1

        def compute(lyr, intersectLyr, cellLyr):
            localContext = QgsProcessingContext()
            clippedLyr = self.algRunner.runClip(
                inputLayer=lyr,
                overlayLayer=cellLyr,
                context=localContext,
                feedback=None,
                is_child_algorithm=True,
            )
            intersectLyrRelatedToCell = self.algRunner.runExtractByLocation(
                inputLyr=intersectLyr,
                intersectLyr=cellLyr,
                context=localContext,
                predicate=AlgRunner.Intersects,
                feedback=None,
                is_child_algorithm=True,
            )
            self.algRunner.runCreateSpatialIndex(
                clippedLyr, localContext, feedback=None, is_child_algorithm=True
            )
            self.algRunner.runCreateSpatialIndex(
                intersectLyrRelatedToCell,
                localContext,
                feedback=None,
                is_child_algorithm=True,
            )
            splitLyr = self.algRunner.runSplitLinesWithLines(
                inputLyr=clippedLyr,
                linesLyr=intersectLyrRelatedToCell,
                context=localContext,
                feedback=None,
                is_child_algorithm=True,
            )
            return splitLyr

        # pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        # futures = set()
        layersToMerge = []
        for processedCount, result in concurrently(
            compute,
            [
                (inputLyr.clone(), linesLyr.clone(), gridFeatLyr)
                for gridFeatLyr in self.layerHandler.createMemoryLayerForEachFeature(
                    gridLayer, context
                )
            ],
            feedback=multiStepFeedback,
        ):

            # for i, cell in enumerate(gridLayer.getFeatures()):
            #     if multiStepFeedback.isCanceled():
            #         break
            #     cellLyr = self.layerHandler.createMemoryLayerWithFeature(
            #         layer=gridLayer, feat=cell, context=context
            #     )
            #     futures.add(
            #         pool.submit(compute, inputLyr.clone(), linesLyr.clone(), cellLyr)
            #     )
            #     multiStepFeedback.setProgress(i * cellStep)
            #     if i % 20 == 0 or i >= cellCount - 1:
            #         multiStepFeedback.pushInfo(
            #             self.tr(f"Submitted {i} of {cellCount} grid cells for processing")
            #         )
            # currentStep += 1
            # multiStepFeedback.setCurrentStep(currentStep)
            # multiStepFeedback.pushInfo(
            #     self.tr("Collecting results from parallel processing")
            # )
            # processedCount = 0
            # totalFutures = len(futures)
            # stepSize = 100 / totalFutures if totalFutures > 0 else 100
            # mergedLyr = None
            # layersToMerge = []
            # for future in concurrent.futures.as_completed(futures):
            #     if multiStepFeedback.isCanceled():
            #         break
            #     processedCount += 1
            #     result = future.result()
            if isinstance(result, str):
                result = QgsProcessingUtils.mapLayerFromString(result, context)
            if isinstance(result, QgsVectorLayer):
                layersToMerge.append(result)
            if len(layersToMerge) >= 10 or processedCount == cellCount:
                if mergedLyr is None:
                    mergedLyr = self.algRunner.runMergeVectorLayers(
                        inputList=layersToMerge,
                        context=context,
                        feedback=multiStepFeedback,
                        is_child_algorithm=True,
                    )
                else:
                    mergedLyr = self.algRunner.runMergeVectorLayers(
                        inputList=[mergedLyr] + layersToMerge,
                        context=context,
                        feedback=multiStepFeedback,
                        is_child_algorithm=True,
                    )
                layersToMerge = []
            multiStepFeedback.setProgress(processedCount * cellStep)
            if processedCount % 10 == 0 or processedCount == cellCount:
                multiStepFeedback.pushInfo(
                    self.tr(f"Processed {processedCount}/{cellCount} grid cells")
                )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Parallel processing complete"))
        multiStepFeedback.pushInfo(
            self.tr(f"Evaluation of {totalFeatureCount} elements complete.")
        )
        mergedLyr = QgsProcessingUtils.mapLayerFromString(mergedLyr, context)
        multiStepFeedback.pushInfo(
            self.tr(f"Output layer has {mergedLyr.featureCount()} segments.")
        )
        return mergedLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "unbuildpolygonsalgorithmv2"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Unbuild Polygons V2")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Polygon Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Polygon Handling"

    def tr(self, string):
        return QCoreApplication.translate("UnbuildPolygonsAlgorithm", string)

    def createInstance(self):
        return UnbuildPolygonsAlgorithmV2()
