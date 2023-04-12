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
)


class ReclassifyAdjacentPolygonsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    LABEL_FIELD = "LABEL_FIELD"
    MAX_AREA = "MAX_AREA"
    LABEL_ORDER = "LABEL_RULES"
    DISSOLVE_ATTRIBUTE_LIST = "DISSOLVE_ATTRIBUTE_LIST"
    DISSOLVE_OUTPUT = "DISSOLVE_OUTPUT"
    CHUNK_SIZE = "CHUNK_SIZE"
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
            QgsProcessingParameterString(
                self.LABEL_ORDER,
                description=self.tr("Label order"),
                multiLine=False,
                defaultValue="",
                optional=True,
            )
        )

        param = QgsProcessingParameterDistance(
            self.MAX_AREA,
            self.tr("Maximum area"),
            parentParameterName=self.INPUT,
            defaultValue=0.0001,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

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
            QgsProcessingParameterNumber(
                self.CHUNK_SIZE,
                self.tr("Chunk size on thread processing"),
                minValue=1,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=10000
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
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        maxAreaToDissolve = self.parameterAsDouble(parameters, self.MAX_AREA, context)
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
        chunk_size = self.parameterAsInt(parameters, self.CHUNK_SIZE, context)
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
        nSteps = 7 if dissolveOutput else 6
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating cache layer"))
        cacheLyr = algRunner.runCreateFieldWithExpression(
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
        algRunner.runCreateSpatialIndex(cacheLyr, context, feedback=multiStepFeedback)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        G, featDict, idSet = self.buildAuxStructures(
            nx, cacheLyr, maxAreaToDissolve, chunk_size, multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        anchorIdsSet = set(featDict.keys()).difference(idSet)
        fieldNames = [field.name() for field in inputLyr.fields()]
        multiStepFeedback.setProgressText(self.tr("Performing reclassification"))
        featuresToUpdateSet = self.reclassifyPolygons(
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
        nFeatsToUpdate = len(featuresToUpdateSet)
        if nFeatsToUpdate == 0:
            return {self.OUTPUT: output_sink_id}
        stepSize = 100 / nFeatsToUpdate
        cacheLyr.startEditing()
        cacheLyr.beginEditCommand("Updating features")
        cacheLyrDataProvider = cacheLyr.dataProvider()
        indexDict = {
            fieldName: cacheLyrDataProvider.fields().indexFromName(fieldName)
            for fieldName in fieldNames
        }
        for current, featid in enumerate(idSet):
            if multiStepFeedback.isCanceled():
                break
            # featid = feat['featid']
            cacheLyrDataProvider.changeAttributeValues(
                {
                    featid: {
                        indexDict[fieldName]: featDict[featid][fieldName]
                        for fieldName in dissolveFields
                    }
                }
            )
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1
        cacheLyr.endEditCommand()

        multiStepFeedback.setCurrentStep(currentStep)
        if dissolveOutput:
            multiStepFeedback.setProgressText(self.tr("Dissolving Polygons"))
            mergedLyr = algRunner.runDissolve(
                inputLyr=cacheLyr,
                context=context,
                feedback=multiStepFeedback,
                field=dissolveFields,
                is_child_algorithm=True,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            mergedLyr = algRunner.runMultipartToSingleParts(
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

    def buildAuxStructures(self, nx, inputLyr, tol, chunk_size, feedback):
        G = nx.Graph()
        featDict = dict()
        idSet = set()
        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return G, featDict, idSet
        stepSize = 100 / nFeats
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()

        def compute(feat):
            itemList = []
            geom = feat.geometry()
            featId = feat.id()
            bbox = geom.boundingBox()
            engine = QgsGeometry.createGeometryEngine(geom.constGet())
            engine.prepareGeometry()
            for candidateFeat in inputLyr.getFeatures(bbox):
                if feedback.isCanceled():
                    return [(None, None, None, -1)]
                candidateFeatId = candidateFeat.id()
                if candidateFeatId == featId:
                    continue
                candidateGeom = candidateFeat.geometry()
                candidateGeomConstGet = candidateGeom.constGet()
                if not engine.intersects(candidateGeomConstGet):
                    continue
                intersectionGeom = engine.intersection(candidateGeomConstGet)
                if intersectionGeom.length() <= 0:
                    continue
                itemList.append(
                    (featId, candidateFeatId, candidateFeat, intersectionGeom.length())
                )
            return itemList
        
        def compute_chunk(chunk):
            return itertools.chain.from_iterable(
                map(compute, chunk)
            )
        
        def batched(iterable, chunk_size):
            iterator = iter(iterable)
            while chunk := tuple(itertools.islice(iterator, chunk_size)):
                yield chunk

        multiStepFeedback.pushInfo("Loading features from cache and submitting them to the thread.")
        multiStepFeedback.setCurrentStep(0)
        for current, feat in enumerate(inputLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setProgress(current * stepSize)
            if feat.geometry().area() > tol:
                continue
            featId = feat.id()
            featDict[featId] = feat
            idSet.add(featId)
        featList = list(featDict.values())
        for chunk in batched(featList, chunk_size=chunk_size):
            futures.add(pool.submit(compute_chunk, chunk))

        multiStepFeedback.setCurrentStep(1)
        nFeats = len(featDict)
        stepSize = 100/nFeats
        if nFeats == 0:
            return G, featDict, idSet

        multiStepFeedback.setProgressText(self.tr(f"Building graph with thread results. Evaluating {nFeats:n} features."))
        candidateCount = 0
        logInterval = chunk_size // 10 if chunk_size // 10 > 0 else 1
        current = 0
        for future in concurrent.futures.as_completed(futures):
            if multiStepFeedback.isCanceled():
                break
            if current % logInterval == 0:
                multiStepFeedback.setProgressText(self.tr(f"Evaluated {current:n} / {nFeats:n} features."))
            for item in future.result():
            # for item in itemList:
                current += 1
                featId, candidateFeatId, candidateFeat, intersectionLength = item
                if featId is None:
                    multiStepFeedback.setProgress(current * stepSize)
                    continue
                if candidateFeatId not in featDict:
                    featDict[candidateFeatId] = candidateFeat
                G.add_edge(featId, candidateFeatId)
                G[featId][candidateFeatId]["length"] = intersectionLength
                multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.pushInfo(self.tr(f"{nFeats:n} evaluated. Found {candidateCount:n} candidates to evaluate in next step."))
        return G, featDict, idSet

    def reclassifyPolygons(
        self, G, featDict, anchorIdsSet, candidateIdSet, fieldNames, classFieldName, feedback, classOrderList=None
    ):
        visitedSet = set()
        featuresToUpdateSet = set()
        nIds = len(candidateIdSet)
        if nIds == 0:
            return featuresToUpdateSet
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
                return featuresToUpdateSet
            anchorId = set(G.neighbors(id)).pop()
            featDict[id][classFieldName] = featDict[anchorId][classFieldName]
            featuresToUpdateSet.add(featDict[id])
            visitedSet.add(id)
            processedFeats += 1
            feedback.setProgress(processedFeats * stepSize)

        while True:
            newAnchors = set()
            for anchorId in anchorIdsSet:
                if feedback.isCanceled():
                    return featuresToUpdateSet
                anchorNeighborIdsSet = set(G.neighbors(anchorId))
                for id in sorted(
                    anchorNeighborIdsSet - visitedSet - anchorIdsSet,
                    key=lambda x: featDict[x].geometry().area(),
                ):
                    if feedback.isCanceled():
                        return featuresToUpdateSet
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
                    featuresToUpdateSet.add(featDict[id])
                    newAnchors.add(id)
                    feedback.setProgress(processedFeats * stepSize)
            anchorIdsSet = newAnchors
            if anchorIdsSet == set():
                break
        return featuresToUpdateSet

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
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ReclassifyAdjacentPolygonsAlgorithm", string)

    def createInstance(self):
        return ReclassifyAdjacentPolygonsAlgorithm()
