# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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
import uuid

import concurrent.futures
from typing import List

from qgis.utils import iface

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
    QgsFeature,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterDistance,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingException,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExpression,
    QgsField,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsProject,
    QgsProcessingUtils,
)


class ReclassifyAdjacentPolygonsAlgorithmV2(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    INPUT_POLYGONS = "INPUT_POLYGONS"
    VISUAL_ACUITY = "VISUAL_ACUITY"
    MAP_SCALE = "MAP_SCALE"
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
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr("Polygon Layers to Fill"),
                QgsProcessing.TypeVectorPolygon,
            )
        )

        param = QgsProcessingParameterDistance(
            self.VISUAL_ACUITY,
            self.tr("Visual acuity"),
            parentParameterName=self.INPUT,
            minValue=0,
            defaultValue=0.2,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAP_SCALE,
                self.tr("Map scale (in thousands)"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=25,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        polygonsLyrsList = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        visualAcuity = self.parameterAsDouble(parameters, self.VISUAL_ACUITY, context)
        scale = self.parameterAsDouble(parameters, self.MAP_SCALE, context)
        for layer in polygonsLyrsList:
            pk_fields = layer.primaryKeyAttributes()
            if len(pk_fields) == 0:
                raise QgsProcessingException(
                    self.tr("Fill layer does not have a primary key")
                )

        nSteps = 24
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Adding id fields to fill layers"))

        pkField = "featidpolygons"
        polygonsLyrsWithPK = self.createFieldForMultipleLayers(
            polygonsLyrsList,
            context=context,
            expression="$id",
            fieldName=pkField,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Calculating area for fill layers"))
        areaField = "areapolygons"
        polygonsLyrsWithArea = self.createFieldForMultipleLayers(
            polygonsLyrsWithPK,
            context=context,
            expression="area($geometry)",
            fieldName=areaField,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Merging fill layers"))
        polygonsLyrsMerged = self.algRunner.runMergeVectorLayers(
            inputList=polygonsLyrsWithArea, context=context, feedback=multiStepFeedback
        )

        # outputLyr = polygonsLyrs

        # (output_sink, output_sink_id) = self.parameterAsSink(
        #     parameters,
        #     self.OUTPUT,
        #     context,
        #     outputLyr.fields(),
        #     outputLyr.wkbType(),
        #     outputLyr.sourceCrs(),
        # )

        # currentStep += 1
        # nFeats = outputLyr.featureCount()
        # if nFeats == 0:
        #     return {self.OUTPUT: output_sink_id}
        # stepSize = 100 / nFeats
        # multiStepFeedback.setProgressText(self.tr("Building Outputs"))
        # for current, feat in enumerate(outputLyr.getFeatures()):
        #     if multiStepFeedback.isCanceled():
        #         break
        #     output_sink.addFeature(feat)
        #     multiStepFeedback.setProgress(current * stepSize)

        # # Compute the number of steps to display within the progress bar and
        # # get features from source

        # return {self.OUTPUT: output_sink_id}

        currentStep += 1
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
        if cacheLyr.fields().indexFromName("fid") != -1:
            cacheLyr = self.algRunner.runDropFields(
                cacheLyr,
                ["fid"],
                context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
        currentStep += 1
        # Verificar vizinhos de feições da inputLyr, para ver se so tem 1 vizinho e preencher so com ele, ai continua com o resto (que tem mais de um vizinho)

        neighbour = self.algRunner.runJoinByLocationSummary(
            inputLyr=cacheLyr,
            joinLyr=polygonsLyrsMerged,
            predicateList=[0],
            joinFields=[],
            summaries=[],
            context=context,
        )

        (
            multipleNeighbours,
            oneNeighbour,
        ) = self.algRunner.runFilterExpressionWithFailOutput(
            inputLyr=neighbour,
            expression=f"{pkField}_count > 1 and layer>1",
            context=context,
            feedback=multiStepFeedback,
        )

        self.mergeFeaturesBasedOnAttributeForMultipleLayers(
            layers=polygonsLyrsList,
            mergeLyr=oneNeighbour,
            matchfield2=pkField + "_min",
            layerNameField="layer_min",
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Merging fill layers"))
        newPolygonsLyrs = self.algRunner.runMergeVectorLayers(
            inputList=polygonsLyrsWithArea, context=context, feedback=multiStepFeedback
        )

        # outputLyr = joinedOneNeighbourAndPolygonsWithArea
        # print(outputLyr.name())

        # (output_sink, output_sink_id) = self.parameterAsSink(
        #     parameters,
        #     self.OUTPUT,
        #     context,
        #     outputLyr.fields(),
        #     outputLyr.wkbType(),
        #     outputLyr.sourceCrs(),
        # )

        # currentStep += 1
        # nFeats = outputLyr.featureCount()
        # if nFeats == 0:
        #     return {self.OUTPUT: output_sink_id}
        # stepSize = 100 / nFeats
        # multiStepFeedback.setProgressText(self.tr("Building Outputs"))
        # for current, feat in enumerate(outputLyr.getFeatures()):
        #     if multiStepFeedback.isCanceled():
        #         break
        #     output_sink.addFeature(feat)
        #     multiStepFeedback.setProgress(current * stepSize)

        # # Compute the number of steps to display within the progress bar and
        # # get features from source

        # return {self.OUTPUT: output_sink_id}

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Polygons to Lines"))
        polygonsToLines = self.algRunner.runPolygonsToLines(
            inputLyr=multipleNeighbours, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Densifying lines"))
        interval = visualAcuity * scale * 1000
        densified = self.algRunner.runDensifyByInterval(
            inputLayer=polygonsToLines,
            interval=interval * 100,
            context=context,
            feedback=multiStepFeedback,
        )
        # fica muito lento em areas grandes, entao fazer voronoi para cada feicao
        layersDensified = self.layerHandler.createMemoryLayerForEachFeature(
            densified, context, returnFeature=False, feedback=multiStepFeedback
        )

        def compute(densifiedLyr, neighborsLyr, overlayLyr):
            algRunner = AlgRunner()
            local_context = context
            exploded = algRunner.runExplodeLines(
                inputLyr=densifiedLyr,
                context=local_context,
                is_child_algorithm=True,
            )
            centroids = algRunner.runCentroids(
                inputLayer=exploded,
                context=local_context,
                is_child_algorithm=True,
            )
            algRunner.runCreateSpatialIndex(
                centroids,
                context=local_context,
                is_child_algorithm=True,
            )
            uuid_value = str(uuid.uuid4()).replace("-", "")
            outputVoronoi = QgsProcessingUtils.generateTempFilename(
                "output_voronoi_{uuid}.gpkg".format(uuid=uuid_value)
            )
            voronoi = algRunner.runVoronoiPolygons(
                inputLayer=centroids,
                buffer=5,
                context=local_context,
                outputLyr=outputVoronoi,
            )
            algRunner.runCreateSpatialIndex(
                voronoi,
                context=local_context,
                is_child_algorithm=True,
            )
            pkFieldCentroid = "featidcentroids"
            centroidsWithPkField = algRunner.runCreateFieldWithExpression(
                inputLyr=centroids,
                expression="$id",
                fieldType=1,
                fieldName=pkFieldCentroid,
                context=local_context,
                is_child_algorithm=True,
            )
            joinedPrefix = "polyattr_"
            joinedByNearest = algRunner.runJoinAttributesByNearest(
                inputLayer=centroidsWithPkField,
                inputLayer2=neighborsLyr,
                joinedPrefix=joinedPrefix,
                context=local_context,
            )
            areaField = "areapolygons"
            fieldToFilter = joinedPrefix + areaField
            joinedByNearest.startEditing()
            seenFeats = dict()
            idsToRemove = []
            for feat in joinedByNearest.getFeatures():
                if feat[pkFieldCentroid] not in seenFeats:
                    seenFeats[feat[pkFieldCentroid]] = feat
                    continue
                if (
                    feat[fieldToFilter]
                    < seenFeats[feat[pkFieldCentroid]][fieldToFilter]
                ):
                    idsToRemove.append(feat.id())
                    continue
                idsToRemove.append(seenFeats[feat[pkFieldCentroid]].id())
                seenFeats[feat[pkFieldCentroid]] = feat
            joinedByNearest.deleteFeatures(idsToRemove)
            algRunner.runCreateSpatialIndex(
                joinedByNearest,
                context=local_context,
                is_child_algorithm=True,
            )
            outputJoin = QgsProcessingUtils.generateTempFilename(
                "output_join_{uuid}.gpkg".format(uuid=uuid_value)
            )
            joinedByLocation = algRunner.runJoinAttributesByLocation(
                inputLyr=voronoi,
                joinLyr=joinedByNearest,
                context=local_context,
                outputLyr=outputJoin,
            )
            algRunner.runCreateSpatialIndex(
                joinedByLocation,
                context=local_context,
                is_child_algorithm=True,
            )
            clippedLyr = algRunner.runClip(
                inputLayer=joinedByLocation,
                overlayLayer=overlayLyr,
                context=local_context,
            )
            return {feat for feat in clippedLyr.getFeatures()}

        # pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()
        featuresClippedSet = set()
        multiStepFeedback.setProgressText(
            self.tr("Submitting tasks to thread (clip)...")
        )
        nSteps = len(layersDensified)
        stepSize = 100 / nSteps if nSteps > 0 else 0
        for current, densified in enumerate(layersDensified):

            if multiStepFeedback.isCanceled():
                # pool.shutdown(cancel_futures=True)
                break
            neighbour = self.algRunner.runExtractByLocation(
                inputLyr=newPolygonsLyrs,
                intersectLyr=densified,
                context=context,
                is_child_algorithm=True,
            )
            clipper = self.algRunner.runExtractByLocation(
                inputLyr=multipleNeighbours,
                intersectLyr=densified,
                context=context,
                is_child_algorithm=True,
            )
            # futures.add(pool.submit(compute, densified, neighbour, clipper))
            multiStepFeedback.setProgress(current * stepSize)

            # currentStep += 1
            # multiStepFeedback.setCurrentStep(currentStep)
            # multiStepFeedback.setProgressText(self.tr("Evaluating results (clip)..."))
            # for current, future in enumerate(concurrent.futures.as_completed(futures)):
            #     if multiStepFeedback.isCanceled():
            #         pool.shutdown(cancel_futures=True)
            #         break
            # featuresClippedSet |= future.result()
            featuresClippedSet |= compute(densified, neighbour, clipper)
        featuresClippedList = list(featuresClippedSet)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        firstDensifiedLayer = newPolygonsLyrs
        joinedPrefix = "polyattr_"
        firstFeature = featuresClippedList[0]
        firstGeometry = firstFeature.geometry()
        fields = firstFeature.fields()
        # fields.append(QgsField("{joinedPrefix}layer", QVariant.String))
        # fields.append(QgsField(joinedPrefix + pkField, QVariant.Int))
        mergedClipped = self.layerHandler.createMemoryLayerWithFeatures(
            featList=featuresClippedList,
            fields=fields,
            crs=firstDensifiedLayer.crs(),
            wkbType=firstGeometry.wkbType(),
            context=context,
        )
        # currentStep += 1
        # multiStepFeedback.setCurrentStep(currentStep)
        # multiStepFeedback.setProgressText(self.tr("Creating spatial index on clipped"))
        # self.algRunner.runCreateSpatialIndex(
        #     mergedClipped,
        #     context,
        #     feedback=multiStepFeedback,
        #     is_child_algorithm=True,
        # )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Dissolving"))
        dissolved = self.algRunner.runDissolve(
            inputLyr=mergedClipped,
            field=[f"{joinedPrefix}layer", joinedPrefix + pkField],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Deaggregating"))
        singleParts = self.algRunner.runMultipartToSingleParts(
            inputLayer=dissolved, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Removing duplicated vertexes"))

        nonDuplicated = self.algRunner.runRemoveDuplicateVertex(
            inputLyr=singleParts,
            tolerance=visualAcuity * 10,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Joining by attribute"))
        # juntar feições preenchidas (holes reclassificados) com a camada que tais feições irão preencher

        joinedLayers = self.joinByFieldValueToList(
            layerList=polygonsLyrsWithArea,
            layerToJoin=nonDuplicated,
            fieldNameLayerList=pkField,
            fieldNameLayerToJoin=joinedPrefix + pkField,
            layerNameField=f"{joinedPrefix}layer",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Adding features to original layers"))
        self.updateOriginalLayer(
            originalLayerList=polygonsLyrsList,
            newLayerList=joinedLayers,
            prefix=joinedPrefix,
        )
        currentStep += 1
        # multiStepFeedback.setCurrentStep(currentStep)
        # multiStepFeedback.setProgressText(
        #     self.tr("Snapping vertexes to grid")
        # )  # talvez pode gerar vertice duplicado?

        # self.runSnapToGridAndUpdateList(
        #     layerList=polygonsLyrs,
        #     tolerance=visualAcuity * 100,
        #     context=context,
        #     feedback=multiStepFeedback,
        # )
        # currentStep += 1
        # multiStepFeedback.setCurrentStep(currentStep)
        # multiStepFeedback.setProgressText(self.tr("Adding unshared vertexes"))
        # self.algRunner.runAddUnsharedVertexOnSharedEdges(
        #     inputLinesList=[],
        #     inputPolygonsList=polygonsLyrs,
        #     searchRadius=visualAcuity * 1000,
        #     context=context,
        #     feedback=multiStepFeedback,
        # )
        outputLyr = nonDuplicated

        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outputLyr.fields(),
            outputLyr.wkbType(),
            outputLyr.sourceCrs(),
        )

        currentStep += 1
        nFeats = outputLyr.featureCount()
        if nFeats == 0:
            return {self.OUTPUT: output_sink_id}
        stepSize = 100 / nFeats
        multiStepFeedback.setProgressText(self.tr("Building Outputs"))
        for current, feat in enumerate(outputLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            output_sink.addFeature(feat)
            multiStepFeedback.setProgress(current * stepSize)

        # Compute the number of steps to display within the progress bar and
        # get features from source

        return {self.OUTPUT: output_sink_id}

    def createFieldForMultipleLayers(
        self,
        layers: List[QgsVectorLayer],
        context,
        feedback=None,
        expression="$id",
        fieldName="featid",
    ) -> List[QgsVectorLayer]:
        layersWithField = []
        if len(layers) == 0:
            return layersWithField
        stepSize = 100 / len(layers)
        for current, layer in enumerate(layers):
            if feedback is not None and feedback.isCanceled():
                return layersWithField
            newLayer = self.algRunner.runCreateFieldWithExpression(
                inputLyr=layer,
                expression=expression,
                fieldName=fieldName,
                context=context,
                fieldType=1,
            )
            newLayer.setName(layer.name())
            layersWithField.append(newLayer)
            if feedback is not None:
                feedback.setProgress(current * stepSize)

        return layersWithField

    def mergeFeaturesBasedOnAttributeForMultipleLayers(
        self,
        layers: List[QgsVectorLayer],
        mergeLyr,
        matchfield2,
        layerNameField,
        context,
        feedback=None,
    ) -> List[QgsVectorLayer]:
        layersMerged = []
        if len(layers) == 0:
            return layersMerged
        stepSize = 100 / len(layers)
        for current, layer in enumerate(layers):
            if feedback is not None and feedback.isCanceled():
                return layersMerged
            layerFilteredToMerge = self.algRunner.runFilterExpression(
                mergeLyr,
                expression=f"{layerNameField} = '{layer.name()}'",
                context=context,
            )
            pk_fields = layer.primaryKeyAttributes()
            matchfield1 = layer.fields()[pk_fields[0]].name()
            self.algRunner.runDSGToolsMergeFeaturesBasedOnAttributeAlgorithm(
                inputLyr=layer,
                matchfield1=matchfield1,
                mergeLyr=layerFilteredToMerge,
                matchfield2=matchfield2,
                context=context,
            )
            # newLayer.setName(layer.name())
            # layersMerged.append(newLayer)
            if feedback is not None:
                feedback.setProgress(current * stepSize)

        return

    def filterFeatsWithSameAttributes(self, layer, fieldToCompare, fieldToFilter):
        layer.startEditing()
        layer.beginEditCommand(self.tr("Removing duplicates based on field"))
        seenFeats = dict()
        idsToRemove = []
        for feat in layer.getFeatures():
            if feat[fieldToCompare] not in seenFeats:
                seenFeats[feat[fieldToCompare]] = feat
                continue
            if feat[fieldToFilter] < seenFeats[feat[fieldToCompare]][fieldToFilter]:
                idsToRemove.append(feat.id())
                continue
            idsToRemove.append(seenFeats[feat[fieldToCompare]].id())
            seenFeats[feat[fieldToCompare]] = feat
        layer.deleteFeatures(idsToRemove)
        layer.endEditCommand()

    def joinByFieldValueToList(
        self,
        layerList: List[QgsVectorLayer],
        layerToJoin,
        fieldNameLayerList,
        fieldNameLayerToJoin,
        layerNameField,
        context,
        feedback=None,
    ) -> List[QgsVectorLayer]:
        joinedLayers = []
        for layer in layerList:
            layerFilteredToJoin = self.algRunner.runFilterExpression(
                layerToJoin,
                expression=f"{layerNameField} = '{layer.name()}'",
                context=context,
            )
            joinedLayer = self.algRunner.runJoinAttributesTable(
                layerFilteredToJoin,
                fieldNameLayerToJoin,
                layer,
                fieldNameLayerList,
                method=0,
                context=context,
                discardNonMatching=True,
            )
            joinedLayer.setName(layer.name())
            joinedLayers.append(joinedLayer)
        return joinedLayers

    def runSnapToGridAndUpdateList(self, layerList, tolerance, context, feedback=None):
        for layer in layerList:
            if feedback is not None and feedback.isCanceled():
                break
            self.algRunner.runSnapToGridAndUpdate(
                inputLyr=layer, tolerance=tolerance, context=context, feedback=feedback
            )

    def updateOriginalLayer(
        self, originalLayerList, newLayerList: QgsVectorLayer, prefix
    ):
        newLayersDict = {layer.name(): layer for layer in newLayerList}
        for layer in originalLayerList:
            newLayer = newLayersDict.get(layer.name(), None)
            if newLayer is None:
                continue
            layer.startEditing()
            layer.beginEditCommand(
                self.tr(
                    f"Adding {newLayer.featureCount()} new feature(s) to layer {layer.name()}"
                )
            )
            for feat in newLayer.getFeatures():
                newFeat = QgsFeature(layer.fields())
                featFieldsName = [field.name() for field in feat.fields()]
                for field in layer.fields():
                    fieldName = field.name()
                    if prefix + fieldName in featFieldsName:
                        newFeat[fieldName] = feat[f"{prefix}{fieldName}"]
                newFeat.setGeometry(feat.geometry())
                layer.addFeature(newFeat)
            layer.endEditCommand()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifyadjacentpolygonsv2algorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Adjacent Polygons V2")

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
        return QCoreApplication.translate(
            "ReclassifyAdjacentPolygonsAlgorithmV2", string
        )

    def createInstance(self):
        return ReclassifyAdjacentPolygonsAlgorithmV2()
