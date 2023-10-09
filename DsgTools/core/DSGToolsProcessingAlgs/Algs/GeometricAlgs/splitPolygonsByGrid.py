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
    QgsFields,
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsFeature,
)
from qgis.PyQt.QtCore import QCoreApplication

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler


class SplitPolygonsByGrid(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    X_DISTANCE = "X_DISTANCE"
    Y_DISTANCE = "Y_DISTANCE"
    MIN_AREA = "MIN_AREA"
    NEIGHBOUR = "NEIGHBOUR"
    CLASS_FIELD = "CLASS_FIELD"
    MAX_CONCURRENCY = "MAX_CONCURRENCY"
    OUTPUT = "OUTPUT"

    def tr(self, string):
        return QCoreApplication.translate("SplitPolygonsByGrid", string)

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
            QgsProcessingParameterDistance(
                self.Y_DISTANCE,
                self.tr("Y Distance"),
                parentParameterName=self.INPUT,
                minValue=0.0,
                defaultValue=0.0001,
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_AREA,
            self.tr(
                "Minimun area to process. If feature's area is smaller than this value, "
                "the feature will not be split, but only reclassified to the nearest neighbour."
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)
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
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        source = self.parameterAsSource(parameters, self.INPUT, context)
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        x_distance = self.parameterAsDouble(parameters, self.X_DISTANCE, context)
        y_distance = self.parameterAsDouble(parameters, self.Y_DISTANCE, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
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
        request = QgsFeatureRequest()
        clause = QgsFeatureRequest.OrderByClause("$area")
        orderby = QgsFeatureRequest.OrderBy([clause])
        request.setOrderBy(orderby)
        iterator = source.getFeatures(request)
        nSteps = nFeats + 2
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Extracting vertexes..."))
        verticesLyr = self.algRunner.runExtractVertices(
            inputLyr=parameters[self.NEIGHBOUR],
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index..."))
        self.algRunner.runCreateSpatialIndex(
            verticesLyr, context=context, feedback=multiStepFeedback, is_child_algorithm=True,
        )
        multiStepFeedback.setProgressText(self.tr("Processing features..."))

        def prepare_data(feature):
            geom = feature.geometry()
            bbox = geom.boundingBox()
            try:
                featureLayer = self.layerHandler.createMemoryLayerWithFeature(
                    source, feature, context=context, isSource=True
                )
            except:
                return None, None
            if bbox.isEmpty() or bbox.isNull() or not bbox.isFinite():
                return None, None
            try:
                localNeighborVertexes = self.algRunner.runExtractByExtent(
                    inputLayer=verticesLyr, extent=bbox, context=context, clip=True
                )
            except:
                return None, None
            return featureLayer, localNeighborVertexes

        def output_data(feature):
            newFeat = QgsFeature(source.fields())
            newFeat.setGeometry(feature.geometry())
            newFeat[classFieldName] = feature[classFieldName]
            return newFeat
            
        
        if max_concurrency == 1:
            for current, feature in enumerate(iterator, start=2):
                if multiStepFeedback.isCanceled():
                    return {self.OUTPUT: dest_id}
                multiStepFeedback.setCurrentStep(current)
                geom = feature.geometry()
                if geom.isNull() or geom.isEmpty():
                    continue
                featureLayer, localNeighborVertexes = prepare_data(feature)
                if featureLayer is None:
                    continue
                if multiStepFeedback.isCanceled():
                    return {self.OUTPUT: dest_id}
                outputFeatures = self.compute(
                    localNeighborVertexes=localNeighborVertexes,
                    feature=feature,
                    featureLayer=featureLayer,
                    x_distance=x_distance,
                    y_distance=y_distance,
                    classFieldName=classFieldName,
                    source_fields=source.fields(),
                    min_area=min_area,
                    feedback=multiStepFeedback,
                )
                if outputFeatures is None or outputFeatures == set():
                    if current % 500 == 0:
                        multiStepFeedback.pushInfo(
                            self.tr(f"Processed {current}/{nFeats}.")
                        )
                    continue
                sink.addFeatures(list(map(output_data, outputFeatures)))
                if current % 500 == 0:
                    multiStepFeedback.pushInfo(
                        self.tr(f"Processed {current}/{nFeats}.")
                    )
            return {self.OUTPUT: dest_id}

        def compute_in_paralel(feature):
            featureLayer, localNeighborVertexes = prepare_data(feature)
            return self.compute(
                localNeighborVertexes=localNeighborVertexes,
                feature=feature,
                featureLayer=featureLayer,
                x_distance=x_distance,
                y_distance=y_distance,
                classFieldName=classFieldName,
                source_fields=QgsFields(source.fields()),
                min_area=min_area,
                feedback=feedback,
            )

        for current, outputFeatures in enumerate(
            concurrently(compute_in_paralel, iterator, max_concurrency=max_concurrency),
            start=2,
        ):
            multiStepFeedback.setCurrentStep(current)
            if multiStepFeedback.isCanceled():
                return {self.OUTPUT: dest_id}
            if outputFeatures is None or outputFeatures == set():
                continue
            sink.addFeatures(list(map(output_data, outputFeatures)))
            if current % 500 == 0:
                multiStepFeedback.pushInfo(self.tr(f"Processed {current}/{nFeats}."))

        return {self.OUTPUT: dest_id}

    def compute(
        self,
        localNeighborVertexes,
        feature,
        featureLayer,
        x_distance,
        y_distance,
        classFieldName,
        source_fields,
        min_area,
        feedback=None,
    ):
        context = QgsProcessingContext()
        algRunner = AlgRunner()
        if feedback is not None and feedback.isCanceled():
            return set()
        if (
            (feedback is not None and feedback.isCanceled())
            or feature is None
            or localNeighborVertexes is None
            or featureLayer is None
            or isinstance(localNeighborVertexes, str)
            or localNeighborVertexes.featureCount() == 0
        ):
            return set()
        neighbour_idx = QgsSpatialIndex(localNeighborVertexes.getFeatures())
        neighbourFeatDict = {
            feat.id(): feat for feat in localNeighborVertexes.getFeatures()
        }
        geometry = feature.geometry()
        if geometry.isEmpty() or geometry.isNull():
            return set()
        bbox = geometry.boundingBox()
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
        if geometry.area() <= min_area or geometry.area() <= xSpacing * ySpacing:
            nearest_neighbor_ids = neighbour_idx.nearestNeighbor(
                geometry.centroid().asPoint(), 1
            )
            if nearest_neighbor_ids == []:
                return set()
            nearest_neighbor_id = nearest_neighbor_ids[0]
            if nearest_neighbor_id not in neighbourFeatDict:
                return set()
            feature[classFieldName] = neighbourFeatDict[nearest_neighbor_id][
                classFieldName
            ]
            returnSet = set()
            returnSet.add(feature)
            return returnSet
        gridLayer = algRunner.runCreateGrid(
            extent=bbox,
            crs=featureLayer.crs(),
            hSpacing=xSpacing,
            vSpacing=ySpacing,
            context=context,
            is_child_algorithm=True,
        )
        if feedback is not None and feedback.isCanceled():
            return set()
        algRunner.runCreateSpatialIndex(gridLayer, context=context, is_child_algorithm=True)
        if feedback is not None and feedback.isCanceled():
            return set()
        try:
            clippedPolygons = algRunner.runClip(
                gridLayer, featureLayer, context=context
            )
        except:
            clippedPolygons = None
        if (
            not isinstance(clippedPolygons, QgsVectorLayer)
            or clippedPolygons.featureCount() < 4
        ):
            nearest_neighbors = neighbour_idx.nearestNeighbor(
                geometry.centroid().asPoint(), 1
            )
            if nearest_neighbors == []:
                return set()
            nearest_neighbor_id = nearest_neighbors[0]
            if nearest_neighbor_id not in neighbourFeatDict:
                return set()
            feature[classFieldName] = neighbourFeatDict[nearest_neighbor_id][
                classFieldName
            ]
            returnSet = set()
            returnSet.add(feature)
            return returnSet
        clippedPolygons.startEditing()
        if feedback is not None and feedback.isCanceled():
            return set()
        algRunner.runCreateSpatialIndex(clippedPolygons, context=context, is_child_algorithm=True)
        nFeats = clippedPolygons.featureCount()
        if nFeats == 0:
            return None
        clippedPolygons.beginEditCommand("Updating features")
        clippedPolygonsDataProvider = clippedPolygons.dataProvider()
        if not any(i.name() == classFieldName for i in clippedPolygons.fields()):
            clippedPolygonsDataProvider.addAttributes(
                [i for i in source_fields if i.name() == classFieldName]
            )
            clippedPolygons.updateFields()
        fieldIdx = clippedPolygons.fields().indexFromName(classFieldName)
        for feat in clippedPolygons.getFeatures():
            if feedback is not None and feedback.isCanceled():
                return set()
            geom = feat.geometry()
            if geom.isEmpty() or geom.isNull():
                continue
            nearest_neighbor_ids = neighbour_idx.nearestNeighbor(
                geom.centroid().asPoint(), 1
            )
            if nearest_neighbor_ids == []:
                continue
            nearest_neighbor_id = nearest_neighbor_ids[0]
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
        retainedFields = algRunner.runRetainFields(
            dissolvedLyr, [field.name() for field in source_fields], context=context
        )
        return set(feat for feat in retainedFields.getFeatures())
