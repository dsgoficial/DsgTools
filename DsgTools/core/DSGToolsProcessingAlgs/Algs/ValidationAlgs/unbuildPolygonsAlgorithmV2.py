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
            return {
                self.OUTPUT_CENTER_POINTS: output_center_point_sink_id,
                self.OUTPUT_BOUNDARIES: output_boundaries_sink_id,
            }
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
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
        currentStep += 1
        mergedLines = self.algRunner.runMergeVectorLayers(
            inputList=constraintLyrList + [singleInputPolygonBoundariesLayer],
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            mergedLines, context, feedback, is_child_algorithm=True
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectedLines = self.algRunner.runSplitLinesWithLines(
            inputLyr=mergedLines,
            linesLyr=mergedLines,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectedLines = self.algRunner.runCreateFieldWithExpression(
            inputLyr=intersectedLines,
            expression="$id",
            fieldName="featid",
            fieldType=AlgRunner.FieldTypeInteger,
            feedback=multiStepFeedback,
            context=context,
            is_child_algorithm=False,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        uniqueBoundariesIdSet = (
            self.getUniqueBoundariesIds(
                nx=nx,
                inputLyr=intersectedLines,
                referenceSet=inputPolygonLyrIdSet,
                feedback=multiStepFeedback,
            )
            if intersectedLines.featureCount() < 10000
            else self.getUniqueBoundariesIdsWithParallelProcessing(
                inputLyr=intersectedLines,
                referenceSet=inputPolygonLyrIdSet,
                geographicBoundaryLyr=geographicBoundaryLyr,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if len(uniqueBoundariesIdSet) > 0:
            uniqueBoundaries = self.algRunner.runFilterExpression(
                inputLyr=intersectedLines,
                expression=f"\"featid\" IN ({','.join(map(str, uniqueBoundariesIdSet))})",
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runDSGToolsMergeLines(
                uniqueBoundaries,
                context=context,
                attributeBlackList=[f.name() for f in uniqueBoundaries.fields()],
                feedback=multiStepFeedback,
                allowClosed=False,
                lineFilterLyrList=constraintLyrList,
            )
            outputBoundariesLambda = lambda x: output_boundaries_sink.addFeature(x)
            list(map(outputBoundariesLambda, uniqueBoundaries.getFeatures()))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedInputPolygons = self.algRunner.runMergeVectorLayers(
            inputList=parameters[self.INPUT_POLYGONS],
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedInputPolygons = self.algRunner.runCreateFieldWithExpression(
            mergedInputPolygons,
            fieldName="layer_id",
            expression='"layer"',
            fieldType=AlgRunner.FieldTypeText,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            mergedInputPolygons,
            context,
            feedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        polygonizeOutput = self.algRunner.runPolygonize(
            inputLyr=intersectedLines,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        centerPointLayer = self.algRunner.runPointOnSurface(
            polygonizeOutput,
            context,
            allParts=True,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        centerPointLayer = self.algRunner.runMultipartToSingleParts(
            inputLayer=centerPointLayer,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            centerPointLayer,
            context,
            feedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        centerPointsInsideInput = self.algRunner.runExtractByLocation(
            centerPointLayer,
            mergedInputPolygons,
            context,
            predicate=AlgRunner.Within,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if geographicBoundaryLyr is not None:
            centerPointsInsideInput = self.algRunner.runExtractByLocation(
                centerPointsInsideInput,
                geographicBoundaryLyr,
                context,
                predicate=AlgRunner.Within,
                feedback=multiStepFeedback,
            )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            centerPointsInsideInput,
            context,
            feedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        final_result_lyr = self.algRunner.runJoinAttributesByLocation(
            centerPointsInsideInput,
            mergedInputPolygons,
            context=context,
            predicateList=[AlgRunner.Intersects],
            method=0,  # Take attributes from the first located feature
            discardNonMatching=False,
            feedback=multiStepFeedback,
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

        list(map(outputFeature, final_result_lyr.getFeatures()))

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
            outputLyr = self.prepareLayer(
                lyr,
                onlySelected=onlySelected,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            layerList.append(outputLyr)
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
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
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
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        singlePartsLyr = self.algRunner.runMultipartToSingleParts(
            inputLayer=linesLyr,
            context=localContext,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
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
        return explodedLinesLyr

    def getUniqueBoundariesIds(
        self,
        nx,
        inputLyr: QgsVectorLayer,
        referenceSet: Set[str],
        feedback=None,
    ) -> Set[int]:

        G = nx.Graph()
        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return set()
        stepSize = 100 / nFeats
        for feat in inputLyr.getFeatures():
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            startPoint, endPoint = geom.asPolyline()[0], geom.asPolyline()[-1]
            if not G.has_edge(startPoint, endPoint):
                G.add_edge(startPoint, endPoint, layerIdSet=set(), featid=feat.id())
            G[startPoint][endPoint]["layerIdSet"].add(feat["layer_id"])
            if feedback is not None:
                feedback.setProgress(int(feat.id() * stepSize))
        return set(
            G[startPoint][endPoint]["featid"]
            for startPoint, endPoint in G.edges()
            if G[startPoint][endPoint]["layerIdSet"].issubset(referenceSet)
        )

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
        layerToSplit = (
            geographicBoundaryLyr
            if geographicBoundaryLyr is not None
            else self.algRunner.runPolygonFromLayerExtent(
                inputLyr=inputLyr,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        referencePolygonLayer = self.algRunner.runDSGToolsPolygonTiler(
            inputLayer=layerToSplit,
            context=context,
            feedback=multiStepFeedback,
            rows=os.cpu_count() // 2,
            columns=os.cpu_count() // 2,
            includePartial=True,
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
        nFeats = referencePolygonLayer.featureCount()
        if nFeats == 0:
            return set()
        if nFeats == 1:
            return self.getUniqueBoundariesIds(
                nx=nx,
                inputLyr=inputLyr,
                referenceSet=referenceSet,
            )
        stepSize = 100 / nFeats
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for current, polygonTile in enumerate(referencePolygonLayer.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            tileLayer = self.layerHandler.createMemoryLayerWithFeature(
                layer=referencePolygonLayer, feat=polygonTile, context=context
            )
            futures.add(pool.submit(compute, inputLyr.clone(), tileLayer))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for current, future in concurrent.futures.as_completed(futures):
            if multiStepFeedback.isCanceled():
                break
            outputSet.update(future.result())
            multiStepFeedback.setProgress(current * stepSize)
        return outputSet

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
