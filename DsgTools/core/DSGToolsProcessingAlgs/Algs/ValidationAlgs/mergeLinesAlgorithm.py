# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-31
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
import os
import concurrent.futures
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import graphHandler

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessingFeatureSourceDefinition,
    QgsProcessing,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsWkbTypes,
    QgsProcessingParameterMultipleLayers,
)

from .validationAlgorithm import ValidationAlgorithm


class MergeLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    IGNORE_VIRTUAL_FIELDS = "IGNORE_VIRTUAL_FIELDS"
    IGNORE_PK_FIELDS = "IGNORE_PK_FIELDS"
    ALLOW_CLOSED_LINES_ON_OUTPUT = "ALLOW_CLOSED_LINES_ON_OUTPUT"
    POINT_FILTER_LAYERS = "POINT_FILTER_LAYERS"
    LINE_FILTER_LAYERS = "LINE_FILTER_LAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

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
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr("Ignore virtual fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr("Ignore primary key fields"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ALLOW_CLOSED_LINES_ON_OUTPUT,
                self.tr("Allow closed lines on output"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POINT_FILTER_LAYERS,
                self.tr("Point Filter Layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_FILTER_LAYERS,
                self.tr("Line Filter Layers"),
                QgsProcessing.TypeVectorLine,
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
        layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        ignoreVirtual = self.parameterAsBool(
            parameters, self.IGNORE_VIRTUAL_FIELDS, context
        )
        ignorePK = self.parameterAsBool(parameters, self.IGNORE_PK_FIELDS, context)
        allowClosedLines = self.parameterAsBool(
            parameters, self.ALLOW_CLOSED_LINES_ON_OUTPUT, context
        )
        pointFilterLyrList = self.parameterAsLayerList(
            parameters, self.POINT_FILTER_LAYERS, context
        )
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINE_FILTER_LAYERS, context
        )
        geographicBoundaryLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        nSteps = (
            9
            + 3 * (pointFilterLyrList != [])
            + 3 * (lineFilterLyrList != [])
            + (geographicBoundaryLyr is not None)
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building aux structures"))
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        if localCache.featureCount() == 0:
            return {}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        localCache = (
            self.algRunner.runExtractByLocation(
                inputLyr=localCache,
                intersectLyr=geographicBoundaryLyr,
                predicate=AlgRunner.Intersects,
                context=context,
                feedback=multiStepFeedback,
            )
            if geographicBoundaryLyr is not None
            else localCache
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = self.algRunner.runExtractSpecificVertices(
            inputLyr=localCache,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = self.algRunner.runCreateFieldWithExpression(
            inputLyr=nodesLayer,
            expression="$id",
            fieldName="nfeatid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building graph aux structures"))
        (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkMultiGraph,
        ) = graphHandler.buildAuxStructures(
            nx,
            nodesLayer=nodesLayer,
            edgesLayer=localCache,
            feedback=multiStepFeedback,
            graphType=graphHandler.GraphType.MULTIGRAPH,
            useWkt=False,
            computeNodeLayerIdDict=False,
            addEdgeLength=True,
        )
        currentStep += 1
        constraintNodeIds = set()

        if pointFilterLyrList:
            # Merge point layers if multiple
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Identifying constraint nodes from point layers...")
            )
            mergedPointLyr = self.algRunner.runMergeVectorLayers(
                pointFilterLyrList, context, multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                mergedPointLyr, context, multiStepFeedback, is_child_algorithm=True
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            # Find nodes that intersect with points
            nodesFromPoints = self.algRunner.runExtractByLocation(
                inputLyr=nodesLayer,
                intersectLyr=mergedPointLyr,
                predicate=[self.algRunner.Intersects],
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1

            for nodeFeat in nodesFromPoints.getFeatures():
                geom = nodeFeat.geometry()
                geomWkb = geom.asWkb()
                constraintNodeIds.add(nodeDict[geomWkb])

        if lineFilterLyrList:
            # Merge line layers if multiple
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Identifying constraint nodes from line layers...")
            )
            mergedLineLyr = self.algRunner.runMergeVectorLayers(
                lineFilterLyrList, context, multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                mergedLineLyr, context, multiStepFeedback, is_child_algorithm=True
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            # Find nodes that intersect with lines
            nodesFromLines = self.algRunner.runExtractByLocation(
                inputLyr=nodesLayer,
                intersectLyr=mergedLineLyr,
                predicate=[self.algRunner.Intersects],
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1

            for nodeFeat in nodesFromLines.getFeatures():
                geom = nodeFeat.geometry()
                geomWkb = geom.asWkb()
                constraintNodeIds.add(nodeDict[geomWkb])
        if geographicBoundaryLyr is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            # Find nodes that intersect with points
            nodesOutsideGeographicBounds = self.algRunner.runExtractByLocation(
                inputLyr=nodesLayer,
                intersectLyr=geographicBoundaryLyr,
                predicate=[self.algRunner.Disjoint],
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1

            for nodeFeat in nodesOutsideGeographicBounds.getFeatures():
                geom = nodeFeat.geometry()
                geomWkb = geom.asWkb()
                constraintNodeIds.add(nodeDict[geomWkb])
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Finding mergeable edges"))
        outputGraphDict = graphHandler.find_mergeable_edges_on_graph(
            nx=nx,
            G=networkMultiGraph,
            feedback=multiStepFeedback,
            nodeIdDict=nodeIdDict,
            allowClosedLines=allowClosedLines,
        )
        nSteps = len(outputGraphDict)
        if nSteps == 0:
            return {}
        stepSize = 100 / nSteps

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        attributeNameList = [
            f.name()
            for f in layerHandler.getFieldsFromAttributeBlackList(
                originalLayer=inputLyr,
                attributeBlackList=attributeBlackList,
                ignoreVirtualFields=ignoreVirtual,
            )
        ]

        def computeLambda(x):
            return graphHandler.filter_mergeable_graphs_using_attibutes(
                nx=nx,
                G=x,
                featDict=edgeDict,
                attributeNameList=attributeNameList,
                isMulti=QgsWkbTypes.isMultiType(inputLyr.wkbType()),
                nodeIdDict=nodeIdDict,
                allowClosedLines=allowClosedLines,
                constraintNodeIds=constraintNodeIds,
            )

        futures = set()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Submitting merge task to thread"))
        for current, G in enumerate(outputGraphDict.values()):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(computeLambda, G))
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Evaluating results"))
        outputFeatSet, idsToDeleteSet = set(), set()
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            featSet, idsToDelete = future.result()
            outputFeatSet |= featSet
            idsToDeleteSet |= idsToDelete
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Saving changes on input layer"))

        def updateLambda(x):
            return inputLyr.changeGeometry(x["featid"], x.geometry())

        inputLyr.startEditing()
        inputLyr.beginEditCommand(
            f"Merging lines with same attribute set from {inputLyr.name()}"
        )
        list(map(updateLambda, outputFeatSet))
        inputLyr.deleteFeatures(list(idsToDeleteSet))
        inputLyr.endEditCommand()

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "mergelineswithsameattributeset"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Merge lines with same attribute set")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Line Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Line Handling"

    def tr(self, string):
        return QCoreApplication.translate("MergeLinesAlgorithm", string)

    def createInstance(self):
        return MergeLinesAlgorithm()
