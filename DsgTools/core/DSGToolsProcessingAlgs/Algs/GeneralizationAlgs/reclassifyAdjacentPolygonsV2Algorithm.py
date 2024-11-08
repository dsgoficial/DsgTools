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

import concurrent.futures
from typing import List

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
    QgsFeatureRequest,
    QgsVectorLayer,
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
        polygonsLyrs = self.parameterAsLayerList(
            parameters, self.INPUT_POLYGONS, context
        )
        visualAcuity = self.parameterAsDouble(parameters, self.VISUAL_ACUITY, context)
        scale = self.parameterAsDouble(parameters, self.MAP_SCALE, context)

        nSteps = 23
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
        multiStepFeedback.setProgressText(self.tr("Polygons to Lines"))
        polygonsToLines = self.algRunner.runPolygonsToLines(
            inputLyr=cacheLyr, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Polygons to Lines"))
        interval = visualAcuity * scale * 1000
        densified = self.algRunner.runDensifyByInterval(
            inputLayer=polygonsToLines,
            interval=interval,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Explode Lines"))
        exploded = self.algRunner.runExplodeLines(
            inputLyr=densified, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Extracting centroids from exploded lines")
        )
        centroids = self.algRunner.runCentroids(
            inputLayer=exploded, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Creating spatial index on centroids")
        )
        self.algRunner.runCreateSpatialIndex(
            centroids,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating voronoi polygons"))
        voronoi = self.algRunner.runVoronoiPolygons(
            inputLayer=centroids, buffer=5, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index on voronoi"))
        self.algRunner.runCreateSpatialIndex(
            voronoi,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Creating PK Field for each polygon layer")
        )
        pkField = "featidpolygons"
        polygonsLyrsWithPK = self.createFieldForMultipleLayers(
            polygonsLyrs,
            context,
            multiStepFeedback,
            expression="$id",
            fieldName=pkField,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Creating Area Field for each polygon layer")
        )
        areaField = "areapolygons"
        polygonsLyrsWithArea = self.createFieldForMultipleLayers(
            polygonsLyrsWithPK,
            context,
            multiStepFeedback,
            expression="area($geometry)",
            fieldName=areaField,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Merging Polygons Inputs"))
        # creates 'layer' field when merged
        mergedLyr = self.algRunner.runMergeVectorLayers(
            inputList=polygonsLyrsWithArea, context=context, feedback=multiStepFeedback
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText("Creating pk field for centroids")
        pkFieldCentroid = "featidcentroids"
        centroidsWithPkField = self.algRunner.runCreateFieldWithExpression(
            inputLyr=centroids,
            expression="$id",
            fieldType=1,
            fieldName=pkFieldCentroid,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Joining centroids and polygons"))

        self.algRunner.runCreateSpatialIndex(
            mergedLyr,
            context,
            feedback=multiStepFeedback,
        )
        joinedPrefix = "polygons_attributes_"
        joinedByNearest = self.algRunner.runJoinAttributesByNearest(
            inputLayer=centroidsWithPkField,
            inputLayer2=mergedLyr,
            joinedPrefix=joinedPrefix,
            context=context,
            feedback=multiStepFeedback,
        )
        self.filterFeatsWithSameAttributes(
            joinedByNearest,
            fieldToCompare=pkFieldCentroid,
            fieldToFilter=joinedPrefix + areaField,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Joining voronoi and centroids"))
        self.algRunner.runCreateSpatialIndex(
            joinedByNearest,
            context,
            is_child_algorithm=True,
        )
        joinedByLocation = self.algRunner.runJoinAttributesByLocation(
            inputLyr=voronoi,
            joinLyr=joinedByNearest,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Clipping voronoi polygons"))
        self.algRunner.runCreateSpatialIndex(
            joinedByLocation,
            context,
            is_child_algorithm=True,
        )
        clipped = self.algRunner.runClip(
            inputLayer=joinedByLocation,
            overlayLayer=cacheLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index on clipped"))
        self.algRunner.runCreateSpatialIndex(
            clipped,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Dissolving"))
        dissolved = self.algRunner.runDissolve(
            inputLyr=clipped,
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
            tolerance=visualAcuity * 100,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Joining by attribute"))

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
            originalLayerList=polygonsLyrs, newLayerList=joinedLayers
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Snapping vertexes to grid")
        )  # talvez pode gerar vertice duplicado?

        self.runSnapToGridAndUpdateList(
            layerList=polygonsLyrs,
            tolerance=visualAcuity * 100,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Adding unshared vertexes"))
        self.algRunner.runAddUnsharedVertexOnSharedEdges(
            inputLinesList=[],
            inputPolygonsList=polygonsLyrs,
            searchRadius=visualAcuity * 1000,
            context=context,
            feedback=multiStepFeedback,
        )
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

    def updateOriginalLayer(self, originalLayerList, newLayerList):
        newLayersDict = {layer.name(): layer for layer in newLayerList}
        for layer in originalLayerList:
            newLayer = newLayersDict.get(layer.name(), None)
            if newLayer is None:
                continue
            layer.startEditing()
            layer.beginEditCommand(self.tr("Adding new features"))
            for feat in newLayer.getFeatures():
                newFeat = QgsFeature(layer.fields())
                newFeat["id"] = feat["polygons_attributes_id"]
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
