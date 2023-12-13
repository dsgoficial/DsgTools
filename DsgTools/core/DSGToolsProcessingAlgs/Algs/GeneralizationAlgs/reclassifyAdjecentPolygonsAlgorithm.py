# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from collections import defaultdict
import itertools
import json
import os

import concurrent.futures

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingException,
    QgsProcessingParameterDistance,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsGeometry,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExpression,
    QgsFeatureRequest,
    QgsProcessingContext
)


class ReclassifyAdjacentPolygonsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    LABEL_FIELD = "LABEL_FIELD"
    LABEL_ORDER = "LABEL_RULES"
    DISSOLVE_ATTRIBUTE_LIST = "DISSOLVE_ATTRIBUTE_LIST"
    DISSOLVE_OUTPUT = "DISSOLVE_OUTPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.LABEL_FIELD,
                self.tr("Class label field on input polygons"),
                None,
                self.INPUT,
                QgsProcessingParameterField.Any,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.FILTER_EXPRESSION,
                self.tr("Filter expression for input"),
                None,
                self.INPUT,
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.LABEL_ORDER,
                description=self.tr("Label order"),
                multiLine=False,
                defaultValue="",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DISSOLVE_OUTPUT, self.tr("Dissolve Output")
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.DISSOLVE_ATTRIBUTE_LIST,
                self.tr("Fields to consider on dissolve"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
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
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        filterExpression = self.parameterAsExpression(parameters, self.FILTER_EXPRESSION, context)
        if filterExpression == '':
            filterExpression = None
        classFieldName = self.parameterAsFields(parameters, self.LABEL_FIELD, context)[0]
        labelListStr = self.parameterAsString(parameters, self.LABEL_ORDER, context)
        classOrderList = None if labelListStr == '' else labelListStr.split(",")
        field = [f for f in inputLyr.fields() if f.name() == classFieldName][0]
        if field.type() == QVariant.Int:
            classOrderList = list(map(int, classOrderList))
        elif field.type() == QVariant.Double:
            classOrderList = list(map(float, classOrderList))
        dissolveOutput = self.parameterAsBool(parameters, self.DISSOLVE_OUTPUT, context)
        dissolveFields = self.parameterAsFields(
            parameters, self.DISSOLVE_ATTRIBUTE_LIST, context
        )
        dissolveFields = list(set(dissolveFields).union({classFieldName}))
        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            inputLyr.fields(),
            inputLyr.wkbType(),
            inputLyr.sourceCrs(),
        )
        if output_sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        nSteps = 6 +  (dissolveOutput is True)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating cache layer"))
        cacheLyr = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldType=1,
            fieldName="featid",
            feedback=multiStepFeedback,
            context=context,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index on cache"))
        self.algRunner.runCreateSpatialIndex(cacheLyr, context, feedback=multiStepFeedback)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        G, featDict, idSet = self.buildAuxStructures(
            nx, cacheLyr, context, filterExpression=filterExpression, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        anchorIdsSet = set(featDict.keys()).difference(idSet)
        fieldNames = [field.name() for field in inputLyr.fields()]
        multiStepFeedback.setProgressText(self.tr("Performing reclassification"))
        featureIdsToUpdateSet = self.reclassifyPolygons(
            G=G,
            featDict=featDict,
            anchorIdsSet=anchorIdsSet,
            candidateIdSet=idSet,
            fieldNames=dissolveFields, 
            feedback=multiStepFeedback,
            classFieldName=classFieldName,
            classOrderList=classOrderList,
        )
        currentStep += 1

        multiStepFeedback.setProgressText(self.tr("Changing attributes from cache"))
        multiStepFeedback.setCurrentStep(currentStep)
        nFeatsToUpdate = len(featureIdsToUpdateSet)
        if nFeatsToUpdate == 0:
            return {self.OUTPUT: output_sink_id}
        stepSize = 100 / nFeatsToUpdate
        cacheLyr.startEditing()
        cacheLyr.beginEditCommand("Updating features")
        cacheLyrDataProvider = cacheLyr.dataProvider()
        fieldIdx = cacheLyrDataProvider.fields().indexFromName(classFieldName)
        for current, (featid, classValue) in enumerate(featureIdsToUpdateSet):
            if multiStepFeedback.isCanceled():
                break
            cacheLyrDataProvider.changeAttributeValues(
                {
                    featid: {
                        fieldIdx: classValue
                    }
                }
            )
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1
        cacheLyr.endEditCommand()

        multiStepFeedback.setCurrentStep(currentStep)
        if dissolveOutput:
            multiStepFeedback.setProgressText(self.tr("Dissolving Polygons"))
            mergedLyr = self.algRunner.runDissolve(
                inputLyr=cacheLyr,
                context=context,
                feedback=multiStepFeedback,
                field=dissolveFields,
                is_child_algorithm=True,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            mergedLyr = self.algRunner.runMultipartToSingleParts(
                inputLayer=mergedLyr, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
        else:
            mergedLyr = cacheLyr

        nFeats = mergedLyr.featureCount()
        if nFeats == 0:
            return {self.OUPUT: output_sink_id}
        stepSize = 100 / nFeats
        multiStepFeedback.setProgressText(self.tr("Building Outputs"))
        for current, feat in enumerate(mergedLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            output_sink.addFeature(feat)
            multiStepFeedback.setProgress(current * stepSize)

        # Compute the number of steps to display within the progress bar and
        # get features from source

        return {self.OUTPUT: output_sink_id}

    def buildAuxStructures(self, nx, inputLyr, context, filterExpression=None, feedback=None):
        G = nx.Graph()
        featDict = dict()
        idSet = set()
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        candidatesLayer = self.algRunner.runFilterExpression(
            inputLyr=inputLyr, expression=filterExpression, context=context, feedback=multiStepFeedback
        )
        nFeats = candidatesLayer.featureCount()
        multiStepFeedback.setCurrentStep(1)

        def compute(feat, featLayer):
            context = QgsProcessingContext()
            algRunner = AlgRunner()
            itemSet = set()
            featId = feat['featid']
            if multiStepFeedback.isCanceled():
                return itemSet
            extractedFeaturesLayer = algRunner.runExtractByLocation(
                inputLyr=inputLyr,
                intersectLyr=featLayer,
                context=context,
                is_child_algorithm=True
            )
            if multiStepFeedback.isCanceled():
                return itemSet
            extractedBoundariesLayer = algRunner.runPolygonsToLines(
                inputLyr=extractedFeaturesLayer, context=context
            )
            if multiStepFeedback.isCanceled():
                return itemSet
            algRunner.runCreateSpatialIndex(
                inputLyr=extractedBoundariesLayer,
                context=context
            )
            if multiStepFeedback.isCanceled():
                return itemSet
            splitBounds = algRunner.runClip(extractedBoundariesLayer, featLayer, context=context)
            if multiStepFeedback.isCanceled():
                return itemSet
            for candidateFeat in splitBounds.getFeatures():
                if multiStepFeedback.isCanceled():
                    return set((None, None, None, -1))
                candidateFeatId = candidateFeat['featid']
                if candidateFeatId == featId:
                    continue
                candidateLength = candidateFeat.geometry().length()
                if candidateLength <= 0:
                    continue
                itemSet.add(
                    (featId, candidateFeatId, candidateFeat, candidateLength)
                )
            return itemSet

        def build_graph(item):
            featId, candidateFeatId, candidateFeat, intersectionLength = item
            if featId is None:
                return
            if candidateFeatId not in featDict:
                featDict[candidateFeatId] = candidateFeat
            G.add_edge(featId, candidateFeatId)
            G[featId][candidateFeatId]["length"] = intersectionLength

        if nFeats == 0:
            return G, featDict, idSet
        multiStepFeedback.pushInfo(f"Submitting {nFeats} features to thread.")
        stepSize = 100 / nFeats
        logInterval = 1000
        futures = set()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()-1)
        for current, feat in enumerate(candidatesLayer.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            featId = feat['featid']
            featDict[featId] = feat
            idSet.add(featId)
            featLayer = self.layerHandler.createMemoryLayerWithFeature(inputLyr, feat, context)
            # result = compute(feat, featLayer)
            # list(map(build_graph, result))
            futures.add(executor.submit(compute, feat, featLayer))
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(1)
        nFeats = len(featDict)
        stepSize = 100/nFeats
        if nFeats == 0:
            return G, featDict, idSet

        multiStepFeedback.setProgressText(self.tr(f"Starting the processess of building graph using parallel computing. Evaluating {nFeats:n} features."))
        candidateCount = 0
        for candidateCount, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            result = future.result()
            list(map(build_graph, result))
            if candidateCount % logInterval == 0:
                multiStepFeedback.setProgressText(self.tr(f"Evaluated {candidateCount:n} / {nFeats:n} features."))
            multiStepFeedback.setProgress(candidateCount * stepSize)

        multiStepFeedback.pushInfo(self.tr(f"{nFeats:n} evaluated. Found {candidateCount:n} candidates to evaluate in next step."))
        return G, featDict, idSet

    def reclassifyPolygons(
        self, G, featDict, anchorIdsSet, candidateIdSet, fieldNames, classFieldName, feedback, classOrderList=None
    ):
        visitedSet = set()
        featureIdsToUpdateSet = set()
        nIds = len(candidateIdSet)
        if nIds == 0:
            return featureIdsToUpdateSet
        stepSize = 100 / nIds
        processedFeats = 0

        def chooseId(G, id, candidateIdSet):
            if classOrderList is None:
                return max(candidateIdSet, key=lambda x: G[id][x]["length"])
            auxDict = defaultdict(list)
            sortedIdsByLength = sorted(candidateIdSet, key=lambda x:G[id][x]["length"], reverse=True)
            if len(sortedIdsByLength) == 1:
                return sortedIdsByLength[0]
            for i in sortedIdsByLength:
                auxDict[featDict[i][classFieldName]].append(i)
            for key in classOrderList:
                if key not in auxDict or len(auxDict[key]) == 0:
                    continue
                return auxDict[key][0]
        for id in set(node for node in G.nodes if G.degree(node) == 1) - anchorIdsSet:
            if feedback.isCanceled():
                return featureIdsToUpdateSet
            anchorId = set(G.neighbors(id)).pop()
            featDict[id][classFieldName] = featDict[anchorId][classFieldName]
            featureIdsToUpdateSet.add((id, featDict[id][classFieldName]))
            visitedSet.add(id)
            processedFeats += 1
            feedback.setProgress(processedFeats * stepSize)
        visitedHolesSet = set(visitedSet)
        originalAnchorIdSet = anchorIdsSet
        while True:
            newAnchors = set()
            for anchorId in anchorIdsSet:
                if feedback.isCanceled():
                    return featureIdsToUpdateSet
                anchorNeighborIdsSet = set(G.neighbors(anchorId)) - originalAnchorIdSet
                for id in sorted(
                    anchorNeighborIdsSet - visitedSet - anchorIdsSet - originalAnchorIdSet,
                    key=lambda x: featDict[x].geometry().area(),
                ):
                    if feedback.isCanceled():
                        return featureIdsToUpdateSet
                    # d = set(G.neighbors(id)) - anchorIdsSet - visitedSet
                    candidateIdSet = set(G.neighbors(id)).intersection(anchorIdsSet)
                    if candidateIdSet == set():
                        continue
                    if len(candidateIdSet) > 1:
                        newAnchors.add(id)
                    visitedSet.add(id)
                    processedFeats += 1
                    chosenId = chooseId(G, id, candidateIdSet)
                    featDict[id][classFieldName] = featDict[chosenId][classFieldName]
                    featureIdsToUpdateSet.add((id, featDict[chosenId][classFieldName]))
                    newAnchors.add(id)
                    feedback.setProgress(processedFeats * stepSize)
            anchorIdsSet = newAnchors
            if anchorIdsSet == set():
                break
        return featureIdsToUpdateSet

    def getAttributesFromFeature(self, newFeat, originalFeat):
        pass

    def reclassifyPolygonsInParalel(self, G, featDict, anchorIdsSet, idSet):
        pass

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifyadjacentpolygonsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Adjacent Polygons")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Generalization Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ReclassifyAdjacentPolygonsAlgorithm", string)

    def createInstance(self):
        return ReclassifyAdjacentPolygonsAlgorithm()
