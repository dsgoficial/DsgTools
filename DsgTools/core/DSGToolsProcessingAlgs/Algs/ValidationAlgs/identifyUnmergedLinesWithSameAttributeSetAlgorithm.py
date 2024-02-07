# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-19
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

import concurrent.futures
from collections import defaultdict
import os

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import graphHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeatureRequest,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingException,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyUnmergedLinesWithSameAttributeSetAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    IGNORE_VIRTUAL_FIELDS = "IGNORE_VIRTUAL_FIELDS"
    IGNORE_PK_FIELDS = "IGNORE_PK_FIELDS"
    POINT_FILTER_LAYERS = "POINT_FILTER_LAYERS"
    LINE_FILTER_LAYERS = "LINE_FILTER_LAYERS"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [
                    QgsProcessing.TypeVectorLine,
                ],
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
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
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
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBoolean(parameters, self.SELECTED, context)
        pointFilterLyrList = self.parameterAsLayerList(
            parameters, self.POINT_FILTER_LAYERS, context
        )
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINE_FILTER_LAYERS, context
        )
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)
        if inputLyr is None or inputLyr.featureCount() == 0:
            return {"FLAGS": self.flag_id}
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        attributeNameList = self.layerHandler.getAttributesFromBlackList(
            inputLyr,
            attributeBlackList,
            ignoreVirtualFields=self.parameterAsBoolean(
                parameters, self.IGNORE_VIRTUAL_FIELDS, context
            ),
            excludePrimaryKeys=self.parameterAsBoolean(
                parameters, self.IGNORE_PK_FIELDS, context
            ),
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(11, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Building local cache on input layer...")
        )
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
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = self.algRunner.runExtractSpecificVertices(
            inputLyr=localCache,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
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
        multiStepFeedback.setProgressText(self.tr("Building graph aux structures"))
        (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkBidirectionalMultiGraph,
        ) = graphHandler.buildAuxStructures(
            nx,
            nodesLayer=nodesLayer,
            edgesLayer=localCache,
            feedback=multiStepFeedback,
            useWkt=False,
            computeNodeLayerIdDict=False,
            addEdgeLength=True,
            graphType=graphHandler.GraphType.MULTIGRAPH,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Finding mergeable edges"))
        outputGraphDict = graphHandler.find_mergeable_edges_on_graph(
            nx=nx,
            G=networkBidirectionalMultiGraph,
            feedback=multiStepFeedback,
            nodeIdDict=nodeIdDict,
        )
        nSteps = len(outputGraphDict)
        if nSteps == 0:
            return {"FLAGS": self.flag_id}

        multiStepFeedback.setProgressText(
            self.tr("Building aux structure on input point list...")
        )
        multiStepFeedback.setCurrentStep(currentStep)
        mergedPointLyr = (
            self.algRunner.runMergeVectorLayers(
                pointFilterLyrList, context, multiStepFeedback
            )
            if pointFilterLyrList
            else None
        )
        currentStep += 1

        multiStepFeedback.setProgressText(
            self.tr("Building aux structure on input line list...")
        )
        multiStepFeedback.setCurrentStep(currentStep)
        mergedLineLyr = (
            self.algRunner.runMergeVectorLayers(
                lineFilterLyrList, context, multiStepFeedback
            )
            if lineFilterLyrList
            else None
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        if mergedLineLyr is not None:
            self.algRunner.runCreateSpatialIndex(
                mergedLineLyr, context, multiStepFeedback
            )
        filterPointSet = (
            set(i.geometry().asWkb() for i in mergedPointLyr.getFeatures())
            if mergedPointLyr is not None
            else set()
        )
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)

        def computeLambda(x):
            return graphHandler.identify_unmerged_edges_on_graph(
                nx=nx,
                G=x,
                featDict=edgeDict,
                nodeIdDict=nodeIdDict,
                filterPointSet=filterPointSet,
                filterLineLayer=mergedLineLyr,
                attributeNameList=attributeNameList,
            )

        futures = set()
        currentStep += 1
        stepSize = 100 / nSteps
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Submitting identification tasks to thread")
        )
        for current, G in enumerate(outputGraphDict.values()):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(computeLambda, G))
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Evaluating results"))
        flagIdSet = set()
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            flagIdSet |= future.result()
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1

        if len(flagIdSet) == 0:
            return {"FLAGS": self.flag_id}

        def flagLambda(x):
            return self.flagFeature(
                flagGeom=nodeIdDict[x],
                flagText=self.tr("Lines with same attribute set that are not merged."),
                fromWkb=True,
            )

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Raising flags"))
        list(map(flagLambda, flagIdSet))
        return {"FLAGS": self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyunmergedlineswithsameattributeset"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Unmerged Lines With Same Attribute Set")

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
        return QCoreApplication.translate(
            "IdentifyUnmergedLinesWithSameAttributeSetAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyUnmergedLinesWithSameAttributeSetAlgorithm()
