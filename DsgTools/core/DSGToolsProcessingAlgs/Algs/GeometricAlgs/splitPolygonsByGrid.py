# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : diniz.felipe@eb.mil.br
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
from DsgTools.core.Utils.threadingTools import concurrently

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsSpatialIndex,
    QgsProcessingParameterNumber,
)
from qgis.PyQt.QtCore import QCoreApplication

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler


class SplitPolygonsByGrid(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    X_DISTANCE = "X_DISTANCE"
    Y_DISTANCE = "Y_DISTANCE"
    NEIGHBOUR = "NEIGHBOUR"
    CLASS_FIELD = "CLASS_FIELD"
    MAX_CONCURRENCY = "MAX_CONCURRENCY"
    OUTPUT = "OUTPUT"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return SplitPolygonsByGrid()

    def name(self):
        return "polygon_split_by_grid"

    def displayName(self):
        return self.tr("Polygon Split by Grid")

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

    def shortHelpString(self):
        return self.tr(
            "Splits input polygon layer by regular grid with user-defined X and Y distances and dissolves the intersection polygons based on the nearest neighbor's ID attribute."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.X_DISTANCE,
                self.tr("X Distance"),
                parentParameterName=self.INPUT,
                minValue=0.0,
                defaultValue=0.0001,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.Y_DISTANCE,
                self.tr("Y Distance"),
                parentParameterName=self.INPUT,
                minValue=0.0,
                defaultValue=0.0001,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.NEIGHBOUR,
                self.tr("Neighbour Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CLASS_FIELD,
                self.tr("Class attribute field"),
                parentLayerParameterName=self.NEIGHBOUR,
                type=QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_CONCURRENCY,
                self.tr("Max Concurrency"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
                minValue=1,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output Layer"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        x_distance = self.parameterAsDouble(parameters, self.X_DISTANCE, context)
        y_distance = self.parameterAsDouble(parameters, self.Y_DISTANCE, context)
        neighbour_source = self.parameterAsSource(parameters, self.NEIGHBOUR, context)
        classFieldName = self.parameterAsString(parameters, self.CLASS_FIELD, context)
        max_concurrency = self.parameterAsInt(parameters, self.MAX_CONCURRENCY, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs(),
        )

        nFeats = source.featureCount()
        if nFeats == 0:
            return {self.OUTPUT: dest_id}

        stepSize = 100 / nFeats
        iterator = sorted(
            source.getFeatures(), key=lambda x: x.geometry().area(), reverse=False
        )
        if max_concurrency == 1:
            multiStepFeedback = QgsProcessingMultiStepFeedback(nFeats, feedback)
            outputFeaturesSet = set()
            for current, feature in enumerate(iterator):
                if multiStepFeedback.isCanceled():
                    return {self.OUTPUT: dest_id}
                multiStepFeedback.setCurrentStep(current)
                outputFeatures = self.compute(
                    source,
                    feature,
                    neighbour_source,
                    parameters[self.NEIGHBOUR],
                    x_distance,
                    y_distance,
                    classFieldName,
                    feedback=multiStepFeedback,
                )
                if outputFeatures is None or outputFeatures == set():
                    continue
                outputFeaturesSet = outputFeaturesSet.union(outputFeatures)
                if current % 500 == 0:
                    feedback.pushInfo(self.tr(f"Processed {current}/{nFeats}."))
            sink.addFeatures(list(outputFeaturesSet))
            return {self.OUTPUT: dest_id}
        computeLambda = lambda x: self.compute(
            source,
            x,
            neighbour_source,
            parameters[self.NEIGHBOUR],
            x_distance,
            y_distance,
            classFieldName,
        )
        for current, outputFeatures in enumerate(
            concurrently(computeLambda, iterator, max_concurrency=max_concurrency)
        ):
            if feedback.isCanceled():
                return {self.OUTPUT: dest_id}
            if outputFeatures is None:
                continue
            sink.addFeatures(outputFeatures)
            feedback.setProgress(current * stepSize)
            if current % 500 == 0:
                feedback.pushInfo(self.tr(f"Processed {current}/{nFeats}."))

        return {self.OUTPUT: dest_id}

    def compute(
        self,
        source,
        feature,
        neighbour_source,
        neighbour_source_idx,
        x_distance,
        y_distance,
        classFieldName,
        feedback=None,
    ):
        context = QgsProcessingContext()
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        if feedback is not None and feedback.isCanceled():
            return set()
        featureLayer = layerHandler.createMemoryLayerWithFeature(
            source, feature, context=context, isSource=True
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        bbox = feature.geometry().boundingBox()
        xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
        xSpacing = (
            x_distance
            if abs(xmax - xmin) > x_distance
            else min(abs(xmax - xmin) / 2, abs(ymax - ymin) / 2)
        )
        ySpacing = (
            y_distance
            if abs(ymax - ymin) > y_distance
            else min(abs(xmax - xmin) / 2, abs(ymax - ymin) / 2)
        )
        gridLayer = algRunner.runCreateGrid(
            extent=bbox,
            crs=source.sourceCrs(),
            hSpacing=xSpacing,
            vSpacing=ySpacing,
            context=context,
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        algRunner.runCreateSpatialIndex(gridLayer, context=context)
        if feedback is not None and feedback.isCanceled():
            return set()
        clippedPolygons = algRunner.runClip(gridLayer, featureLayer, context=context)
        if feedback is not None and feedback.isCanceled():
            return set()
        algRunner.runCreateSpatialIndex(clippedPolygons, context=context)
        nFeats = clippedPolygons.featureCount()
        if nFeats == 0:
            return None
        if feedback is not None and feedback.isCanceled():
            return set()
        bufferZone = algRunner.runBuffer(
            featureLayer, distance=max(xSpacing, ySpacing), context=context
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        algRunner.runCreateSpatialIndex(bufferZone, context)
        if feedback is not None and feedback.isCanceled():
            return set()
        clippedNeighbors = algRunner.runClip(
            neighbour_source_idx, bufferZone, context=context, is_child_algorithm=True
        )
        localNeighborVertexes = algRunner.runExtractVertices(
            clippedNeighbors, context=context
        )
        if (
            feedback is not None and feedback.isCanceled()
        ) or localNeighborVertexes.featureCount() == 0:
            return set()
        neighbour_idx = QgsSpatialIndex(localNeighborVertexes.getFeatures())
        neighbourFeatDict = {
            feat.id(): feat for feat in localNeighborVertexes.getFeatures()
        }
        clippedPolygons.startEditing()
        clippedPolygons.beginEditCommand("Updating features")
        clippedPolygonsDataProvider = clippedPolygons.dataProvider()
        if not any(i.name() == classFieldName for i in clippedPolygons.fields()):
            clippedPolygonsDataProvider.addAttributes(
                [i for i in neighbour_source.fields() if i.name() == classFieldName]
            )
            clippedPolygons.updateFields()
        fieldIdx = clippedPolygons.fields().indexFromName(classFieldName)
        for feat in clippedPolygons.getFeatures():
            if feedback is not None and feedback.isCanceled():
                return set()
            geom = feat.geometry()
            nearest_neighbor_id = neighbour_idx.nearestNeighbor(
                geom.centroid().asPoint(), 1
            )[0]
            destinationAttr = neighbourFeatDict[nearest_neighbor_id][classFieldName]
            clippedPolygonsDataProvider.changeAttributeValues(
                {feat.id(): {fieldIdx: destinationAttr}}
            )
        clippedPolygons.endEditCommand()
        if feedback is not None and feedback.isCanceled():
            return set()
        snappedToGrid = algRunner.runSnapToGrid(
            inputLayer=clippedPolygons, tol=1e-15, context=context
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        dissolvedLyr = algRunner.runDissolve(
            inputLyr=snappedToGrid,
            field=[classFieldName],
            context=context,
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        snappedLyr = algRunner.runSnapGeometriesToLayer(
            dissolvedLyr, localNeighborVertexes, tol=1e-6, context=context, behavior=2
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        retainedFields = algRunner.runRetainFields(
            snappedLyr, [field.name() for field in source.fields()], context=context
        )
        return set(feat for feat in retainedFields.getFeatures())
