# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        copyright            : (C) Brazilian Army Geographic Service
        email                : dsgtools@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Identify coverage gaps, overlaps and inconsistent edge vertexing.

The implementation uses an edge histogram instead of a polygon self-overlay.
An edge shared by exactly two polygon rings cancels.  The frame boundary is
inserted in the same histogram, so a correctly covered outer boundary also
cancels.  Remaining edges are polygonized and classified against the input
coverage.
"""

from collections import defaultdict

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsSpatialIndex,
    QgsVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


def canonical_point_key(point, grid_size):
    """Return a stable, hashable 2-D point key."""
    if grid_size > 0:
        return (
            int(round(point.x() / grid_size)),
            int(round(point.y() / grid_size)),
        )
    return (point.x(), point.y())


def canonical_segment_key(point_a, point_b, grid_size):
    """Return an orientation-independent segment key, preserving vertexing."""
    a = canonical_point_key(point_a, grid_size)
    b = canonical_point_key(point_b, grid_size)
    return (a, b) if a < b else (b, a)


def point_from_key(key, grid_size):
    """Build a point in the normalized coordinate space used by polygonize."""
    if grid_size > 0:
        return QgsPointXY(key[0] * grid_size, key[1] * grid_size)
    return QgsPointXY(key[0], key[1])


class IdentifyGapsAndOverlapsInCoverageAlgorithm(ValidationAlgorithm):
    FLAGS = "FLAGS"
    NODE_FLAGS = "NODE_FLAGS"
    INPUTLAYERS = "INPUTLAYERS"
    FRAMELAYER = "FRAMELAYER"
    SELECTED = "SELECTED"
    GRID_SIZE = "GRID_SIZE"
    MIN_AREA = "MIN_AREA"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr("Coverage Polygon Layers"),
                QgsProcessing.TypeVectorPolygon,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr("Process only selected features"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FRAMELAYER,
                self.tr("Frame Layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.GRID_SIZE,
                self.tr("Coordinate comparison tolerance"),
                defaultValue=0.00000001,
                minValue=0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_AREA,
                self.tr("Minimum error area"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                minValue=0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("Coverage Error Flags")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NODE_FLAGS,
                self.tr("Edge Node Error Flags"),
                optional=True,
                createByDefault=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layers = self.parameterAsLayerList(
            parameters, self.INPUTLAYERS, context
        )
        if not input_layers:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUTLAYERS)
            )
        frame_layer = self.parameterAsVectorLayer(
            parameters, self.FRAMELAYER, context
        )
        if frame_layer and frame_layer in input_layers:
            raise QgsProcessingException(
                self.tr("The frame layer cannot also be a coverage layer.")
            )

        crs = input_layers[0].crs()
        for layer in input_layers + ([frame_layer] if frame_layer else []):
            if layer.crs() != crs:
                raise QgsProcessingException(
                    self.tr("All coverage and frame layers must use the same CRS.")
                )

        selected_only = self.parameterAsBool(parameters, self.SELECTED, context)
        grid_size = self.parameterAsDouble(parameters, self.GRID_SIZE, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)

        self.prepareFlagSink(parameters, input_layers[0], QgsWkbTypes.Polygon, context)
        self.nodeFlagSink, self.node_flag_id = self.parameterAsSink(
            parameters,
            self.NODE_FLAGS,
            context,
            self.getFlagFields(),
            QgsWkbTypes.Point,
            crs,
        )

        multi_feedback = QgsProcessingMultiStepFeedback(5, feedback)
        multi_feedback.setCurrentStep(0)
        multi_feedback.setProgressText(self.tr("Counting coverage edges"))
        edge_count, coverage_indexes = self.buildEdgeHistogram(
            input_layers,
            frame_layer,
            selected_only,
            grid_size,
            multi_feedback,
        )
        if feedback.isCanceled():
            return {self.FLAGS: self.flag_id, self.NODE_FLAGS: self.node_flag_id}

        abnormal_keys = {key for key, count in edge_count.items() if count != 2}

        multi_feedback.setCurrentStep(1)
        multi_feedback.setProgressText(self.tr("Finding inconsistent edge nodes"))
        self.flagIntermediateNodes(abnormal_keys, grid_size, crs, multi_feedback)

        multi_feedback.setCurrentStep(2)
        multi_feedback.setProgressText(self.tr("Building unmatched edge layer"))
        edge_layer = self.buildEdgeLayer(abnormal_keys, grid_size, crs)
        if edge_layer.featureCount() == 0 or feedback.isCanceled():
            return {self.FLAGS: self.flag_id, self.NODE_FLAGS: self.node_flag_id}

        multi_feedback.setCurrentStep(3)
        multi_feedback.setProgressText(self.tr("Polygonizing unmatched edges"))
        polygons = AlgRunner().runPolygonize(
            edge_layer,
            context,
            keepFields=False,
            feedback=multi_feedback,
            outputLyr="memory:",
        )

        multi_feedback.setCurrentStep(4)
        multi_feedback.setProgressText(self.tr("Classifying coverage errors"))
        self.classifyAndFlag(
            polygons,
            coverage_indexes,
            frame_layer,
            min_area,
            multi_feedback,
        )
        return {self.FLAGS: self.flag_id, self.NODE_FLAGS: self.node_flag_id}

    def iterFeatures(self, layer, selected_only=False):
        request = QgsFeatureRequest().setSubsetOfAttributes([])
        if selected_only:
            return layer.getSelectedFeatures(request)
        return layer.getFeatures(request)

    def iterSegments(self, geometry):
        """Yield consecutive ring segments without joining distinct rings."""
        if geometry is None or geometry.isNull() or geometry.isEmpty():
            return
        abstract_geometry = geometry.constGet()
        if QgsWkbTypes.isCurvedType(geometry.wkbType()):
            abstract_geometry = abstract_geometry.segmentize()
        for polygon in abstract_geometry.coordinateSequence():
            for ring in polygon:
                if len(ring) < 2:
                    continue
                for index in range(len(ring) - 1):
                    yield ring[index], ring[index + 1]
                if ring[0] != ring[-1]:
                    yield ring[-1], ring[0]

    def buildEdgeHistogram(
        self, input_layers, frame_layer, selected_only, grid_size, feedback
    ):
        edge_count = defaultdict(int)
        coverage_indexes = []
        layers = [(layer, False) for layer in input_layers]
        if frame_layer:
            layers.append((frame_layer, True))
        total = sum(
            layer.selectedFeatureCount()
            if selected_only and not is_frame
            else layer.featureCount()
            for layer, is_frame in layers
        )
        step = 100.0 / total if total else 0.0
        current = 0
        for layer, is_frame in layers:
            spatial_index = QgsSpatialIndex() if not is_frame else None
            for feature in self.iterFeatures(layer, selected_only and not is_frame):
                if feedback.isCanceled():
                    return edge_count, coverage_indexes
                geometry = feature.geometry()
                if not is_frame:
                    spatial_index.addFeature(feature)
                for point_a, point_b in self.iterSegments(geometry):
                    key = canonical_segment_key(point_a, point_b, grid_size)
                    if key[0] == key[1]:
                        continue
                    edge_count[key] += 1
                current += 1
                feedback.setProgress(current * step)
            if spatial_index is not None:
                coverage_indexes.append((layer, spatial_index))
        return edge_count, coverage_indexes

    def buildEdgeLayer(self, edge_keys, grid_size, crs):
        layer = QgsVectorLayer(
            "LineString?crs={}".format(crs.authid()), "coverage_edge_xor", "memory"
        )
        provider = layer.dataProvider()
        features = []
        for feature_id, key in enumerate(edge_keys):
            feature = QgsFeature()
            feature.setId(feature_id)
            feature.setGeometry(
                QgsGeometry.fromPolylineXY(
                    [point_from_key(key[0], grid_size), point_from_key(key[1], grid_size)]
                )
            )
            features.append(feature)
        provider.addFeatures(features)
        layer.updateExtents()
        return layer

    def flagIntermediateNodes(self, edge_keys, grid_size, crs, feedback):
        if self.nodeFlagSink is None:
            return
        edge_keys = list(edge_keys)
        edge_layer = self.buildEdgeLayer(edge_keys, grid_size, crs)
        edge_index = QgsSpatialIndex()
        edge_dict = {}
        edge_key_dict = {}
        for feature, key in zip(edge_layer.getFeatures(), edge_keys):
            edge_index.addFeature(feature)
            edge_dict[feature.id()] = feature.geometry()
            edge_key_dict[feature.id()] = key

        tolerance = grid_size if grid_size > 0 else 1e-12
        tolerance_squared = tolerance * tolerance
        seen = set()
        size = 100.0 / len(edge_dict) if edge_dict else 0.0
        for current, (feature_id, geometry) in enumerate(edge_dict.items()):
            if feedback.isCanceled():
                return
            key = edge_key_dict[feature_id]
            for endpoint_key in key:
                point = point_from_key(endpoint_key, grid_size)
                bbox = QgsGeometry.fromPointXY(point).buffer(tolerance, 2).boundingBox()
                for candidate_id in edge_index.intersects(bbox):
                    if candidate_id == feature_id:
                        continue
                    candidate_key = edge_key_dict[candidate_id]
                    if endpoint_key in candidate_key:
                        continue
                    distance_squared, _, _, _ = edge_dict[
                        candidate_id
                    ].closestSegmentWithContext(point)
                    if distance_squared < 0 or distance_squared > tolerance_squared:
                        continue
                    if endpoint_key in seen:
                        continue
                    seen.add(endpoint_key)
                    self.flagFeature(
                        QgsGeometry.fromPointXY(point),
                        self.tr(
                            "EDGE_NODE_MISMATCH: vertex exists on only one side "
                            "of a shared edge."
                        ),
                        sink=self.nodeFlagSink,
                    )
            feedback.setProgress(current * size)

    def classifyAndFlag(
        self, polygons, coverage_indexes, frame_layer, min_area, feedback
    ):
        frame_geometries = (
            [QgsGeometry(feature.geometry()) for feature in frame_layer.getFeatures()]
            if frame_layer
            else []
        )
        total = polygons.featureCount()
        step = 100.0 / total if total else 0.0
        for current, feature in enumerate(polygons.getFeatures()):
            if feedback.isCanceled():
                return
            geometry = feature.geometry()
            if geometry.isNull() or geometry.isEmpty() or geometry.area() < min_area:
                continue
            point = geometry.pointOnSurface()
            if frame_geometries and not any(
                frame.intersects(point) for frame in frame_geometries
            ):
                continue
            covering = []
            for layer, spatial_index in coverage_indexes:
                for candidate_id in spatial_index.intersects(point.boundingBox()):
                    candidate = layer.getFeature(candidate_id)
                    if candidate.isValid() and candidate.geometry().intersects(point):
                        covering.append((layer.name(), candidate_id))
            if not covering:
                reason = self.tr(
                    "COVERFAIL_GAP: area is not covered by any input polygon."
                )
            elif len(covering) > 1:
                sources = ", ".join(
                    "{}:{}".format(layer_name, feature_id)
                    for layer_name, feature_id in covering
                )
                reason = self.tr(
                    "COVERFAIL_OVERLAP: area is covered by {count} polygons ({sources})."
                ).format(count=len(covering), sources=sources)
            else:
                continue
            self.flagFeature(geometry, reason)
            feedback.setProgress(current * step)

    def name(self):
        return "identifygapsandoverlaps"

    def displayName(self):
        return self.tr("Identify Gaps and Overlaps in Coverage Layers")

    def group(self):
        return self.tr("QA Tools: Polygon Handling")

    def groupId(self):
        return "DSGTools - QA Tools: Polygon Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyGapsAndOverlapsInCoverageAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyGapsAndOverlapsInCoverageAlgorithm()
