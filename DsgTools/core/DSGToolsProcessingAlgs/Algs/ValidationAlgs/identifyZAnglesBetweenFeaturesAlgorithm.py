# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho@eb.mil.br
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

import math
import os

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsGeometryUtils,
    QgsPoint,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProject,
    QgsWkbTypes,
    QgsProcessingMultiStepFeedback,
    QgsSpatialIndex,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help
from DsgTools.core.Utils.threadingTools import concurrently


class IdentifyZAnglesBetweenFeaturesAlgorithm(ValidationAlgorithm):

    INPUT = "INPUT"
    ANGLE = "ANGLE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input"),
                [
                    QgsProcessing.TypeVectorLine,
                    QgsProcessing.TypeVectorPolygon,
                ],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ANGLE,
                self.tr("Minimum angle"),
                QgsProcessingParameterNumber.Double,
                defaultValue=300,
                minValue=270,
                maxValue=360,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Flags"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        angle = self.parameterAsDouble(parameters, self.ANGLE, context)
        featsToAnalyse = []

        crs = QgsProject.instance().crs()
        self.fields = QgsFields()
        self.fields.append(QgsField("source", QVariant.String))

        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, self.fields, QgsWkbTypes.LineString, crs
        )

        # Initialize caches
        feedback.pushInfo(self.tr("Building feature cache..."))
        self.feature_cache = {}  # Feature cache (id -> feature)
        self.geom_cache = {}  # Geometry cache (id -> geometry)
        self.vertex_cache = {}  # Vertex cache (id -> list of vertices)

        # Build feature and geometry caches up front to avoid repeated getFeatures calls
        feature_count = inputSource.featureCount()

        # Calculate appropriate batch size based on feature count
        # For very large datasets, we'll process in manageable chunks
        batch_size = min(50000, max(1000, feature_count // 10))

        # Cache in batches to show progress and avoid memory issues with very large datasets
        total_cached = 0
        current_batch = []

        for feat in inputSource.getFeatures():
            feat_id = feat.id()
            self.feature_cache[feat_id] = feat
            self.geom_cache[feat_id] = feat.geometry()
            total_cached += 1

            # Show progress for large datasets
            if total_cached % 10000 == 0:
                feedback.pushInfo(
                    self.tr(f"Cached {total_cached}/{feature_count} features...")
                )

            # Check for cancellation
            if feedback.isCanceled():
                return {self.OUTPUT: dest_id}

        # Build spatial index
        feedback.pushInfo(self.tr("Building spatial index..."))
        self.spatial_index = QgsSpatialIndex()
        for feat_id, geom in self.geom_cache.items():
            self.spatial_index.addFeature(self.feature_cache[feat_id])

        # Pre-compute angle thresholds
        self.angle_threshold = angle
        self.angle_threshold_complement = 360 - angle

        # Get geometry type
        geometry_type = QgsWkbTypes.geometryType(inputSource.wkbType())

        # Set up multistep feedback
        nSteps = 2 if geometry_type == QgsWkbTypes.LineGeometry else 1
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback) if nSteps > 1 else feedback
        )
        currentStep = 0

        # Process based on geometry type
        if geometry_type == QgsWkbTypes.LineGeometry:
            # First process Z angles within each line
            multiStepFeedback.setProgressText(
                self.tr("Evaluating Z angles within lines")
            )
            multiStepFeedback.setCurrentStep(currentStep)

            # Process all features using concurrently
            for result in concurrently(
                lambda feat_id: self.process_internal_line(
                    feat_id, angle, inputSource.sourceName()
                ),
                self.feature_cache.keys(),  # Pass feature IDs instead of features
                feedback=multiStepFeedback,
            ):
                if result:
                    featsToAnalyse.extend(result)

            currentStep += 1
            multiStepFeedback.setProgressText(
                self.tr("Evaluating Z angles between features")
            )
            multiStepFeedback.setCurrentStep(currentStep)

            # Process line intersections
            between_lines_results = self.caseBetweenLines(
                inputSource, angle, feedback=multiStepFeedback
            )
            featsToAnalyse.extend(between_lines_results)

        else:  # Polygon geometry
            multiStepFeedback.setProgressText(
                self.tr("Evaluating Z angles within polygons")
            )

            # Process all features using concurrently
            for result in concurrently(
                lambda feat_id: self.process_internal_area(
                    feat_id, angle, inputSource.sourceName()
                ),
                self.feature_cache.keys(),  # Pass feature IDs instead of features
                feedback=multiStepFeedback,
            ):
                if result:
                    featsToAnalyse.extend(result)

        # Add all found features to the sink
        sink.addFeatures(featsToAnalyse)

        # Clear caches to free memory
        self.feature_cache = {}
        self.geom_cache = {}
        self.vertex_cache = {}

        return {self.OUTPUT: dest_id}

    def process_internal_line(self, feat_id, angle, source_name):
        """Process a single line feature to find Z angles within it"""
        results = []

        # Get geometry from cache
        geometry = self.geom_cache[feat_id]
        if geometry.isEmpty():
            return []

        # Get all vertices - cache for this feature if not already cached
        if feat_id not in self.vertex_cache:
            self.vertex_cache[feat_id] = list(geometry.vertices())

        all_vertices = self.vertex_cache[feat_id]

        # Skip features with too few vertices
        if len(all_vertices) < 4:
            return []

        # Process sets of 4 consecutive vertices
        for i in range(len(all_vertices) - 3):
            v1, v2, v3, v4 = all_vertices[i : i + 4]

            # Calculate angles directly
            angle1 = math.degrees(
                QgsGeometryUtils.angleBetweenThreePoints(
                    v1.x(), v1.y(), v2.x(), v2.y(), v3.x(), v3.y()
                )
            )
            angle2 = math.degrees(
                QgsGeometryUtils.angleBetweenThreePoints(
                    v2.x(), v2.y(), v3.x(), v3.y(), v4.x(), v4.y()
                )
            )

            # Check if this forms a Z angle based on thresholds
            if self._is_z_angle(angle1, angle2):
                newFeat = QgsFeature(self.fields)
                if isinstance(v1, QgsPoint):
                    newFeat.setGeometry(QgsGeometry.fromPolyline([v1, v2, v3, v4]))
                elif isinstance(v1, QgsPointXY):
                    newFeat.setGeometry(QgsGeometry.fromPolylineXY([v1, v2, v3, v4]))
                newFeat.setAttribute("source", source_name)
                results.append(newFeat)

        return results

    def process_internal_area(self, feat_id, angle, source_name):
        """Process a single polygon feature to find Z angles within it"""
        results = []

        # Get geometry from cache
        geom = self.geom_cache[feat_id]
        if geom.isEmpty():
            return []

        # Process both multipolygon and regular polygon types
        multiPolygons = (
            geom.asMultiPolygon()[0] if geom.isMultipart() else geom.asPolygon()
        )

        for ring in multiPolygons:
            # Need at least 4 vertices to form a Z angle
            if len(ring) < 4:
                continue

            # Process consecutive sets of 4 vertices along the polygon ring
            for i in range(len(ring) - 3):
                v1, v2, v3, v4 = ring[i : i + 4]

                angle1 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        v1.x(), v1.y(), v2.x(), v2.y(), v3.x(), v3.y()
                    )
                )
                angle2 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        v2.x(), v2.y(), v3.x(), v3.y(), v4.x(), v4.y()
                    )
                )

                if self._is_z_angle(angle1, angle2):
                    newFeat = QgsFeature(self.fields)
                    if isinstance(v1, QgsPoint):
                        newFeat.setGeometry(QgsGeometry.fromPolyline([v1, v2, v3, v4]))
                    elif isinstance(v1, QgsPointXY):
                        newFeat.setGeometry(
                            QgsGeometry.fromPolylineXY([v1, v2, v3, v4])
                        )
                    newFeat.setAttribute("source", source_name)
                    results.append(newFeat)

            # Check the wraparound case (last vertices connected to first)
            if len(ring) >= 4:
                v1, v2, v3, v4 = ring[-3], ring[-2], ring[-1], ring[1]

                angle1 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        v1.x(), v1.y(), v2.x(), v2.y(), v3.x(), v3.y()
                    )
                )
                angle2 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        v2.x(), v2.y(), v3.x(), v3.y(), v4.x(), v4.y()
                    )
                )

                if self._is_z_angle(angle1, angle2):
                    newFeat = QgsFeature(self.fields)
                    if isinstance(v1, QgsPoint):
                        newFeat.setGeometry(QgsGeometry.fromPolyline([v1, v2, v3, v4]))
                    elif isinstance(v1, QgsPointXY):
                        newFeat.setGeometry(
                            QgsGeometry.fromPolylineXY([v1, v2, v3, v4])
                        )
                    newFeat.setAttribute("source", source_name)
                    results.append(newFeat)

        return results

    def caseBetweenLines(self, lines, angle, feedback=None):
        """Find Z angles formed at the intersections between line features"""
        featsToAnalyse = []

        # Process lines to find intersections and potential Z angles
        def process_line_pair(pair_data):
            if feedback is not None and feedback.isCanceled():
                return None

            feat1_id, feat2_id = pair_data

            # Skip if we've already processed this pair
            if feat1_id >= feat2_id:
                return None

            # Get features and geometries directly from caches - MUCH FASTER
            # No need to call getFeatures() again
            feat1 = self.feature_cache[feat1_id]
            feat2 = self.feature_cache[feat2_id]

            gfeat1 = self.geom_cache[feat1_id]
            gfeat2 = self.geom_cache[feat2_id]

            # Skip if geometries don't intersect
            if not gfeat1.intersects(gfeat2):
                return None

            results = []

            # Check if intersection forms a valid Z angle
            intersection = gfeat1.intersection(gfeat2)
            if intersection.wkbType() == QgsWkbTypes.Point:
                # Get closest vertices to intersection
                intersection_point = intersection.asPoint()

                (
                    _,
                    g1VertexIdx,
                    g1PreviousVertexIdx,
                    g1NextVertexIdx,
                    _,
                ) = gfeat1.closestVertex(intersection_point)
                (
                    _,
                    g2VertexIdx,
                    g2PreviousVertexIdx,
                    g2NextVertexIdx,
                    _,
                ) = gfeat2.closestVertex(intersection_point)

                # Get vertices from cache or create and cache them
                if feat1_id not in self.vertex_cache:
                    self.vertex_cache[feat1_id] = list(gfeat1.vertices())
                if feat2_id not in self.vertex_cache:
                    self.vertex_cache[feat2_id] = list(gfeat2.vertices())

                vg1 = self.vertex_cache[feat1_id]
                vg2 = self.vertex_cache[feat2_id]

                # Check for valid configurations that could form Z angles
                # Case 1: Intersection at endpoints
                if (
                    g1NextVertexIdx == g2PreviousVertexIdx == -1
                    and g1PreviousVertexIdx > 0
                    and g2NextVertexIdx < len(vg2) - 1
                ):
                    # Create sequence of 4 points that might form a Z angle
                    points = [
                        vg1[g1PreviousVertexIdx - 1],
                        vg1[g1PreviousVertexIdx],
                        vg1[g1VertexIdx],
                        vg2[g2NextVertexIdx],
                    ]

                    # Calculate angles between points
                    angle1 = math.degrees(
                        QgsGeometryUtils.angleBetweenThreePoints(
                            points[0].x(),
                            points[0].y(),
                            points[1].x(),
                            points[1].y(),
                            points[2].x(),
                            points[2].y(),
                        )
                    )
                    angle2 = math.degrees(
                        QgsGeometryUtils.angleBetweenThreePoints(
                            points[1].x(),
                            points[1].y(),
                            points[2].x(),
                            points[2].y(),
                            points[3].x(),
                            points[3].y(),
                        )
                    )

                    # Check if this forms a Z angle
                    if self._is_z_angle(angle1, angle2):
                        newFeat = QgsFeature(self.fields)
                        if isinstance(points[0], QgsPoint):
                            newFeat.setGeometry(QgsGeometry.fromPolyline(points))
                        elif isinstance(points[0], QgsPointXY):
                            newFeat.setGeometry(QgsGeometry.fromPolylineXY(points))
                        newFeat.setAttribute("source", lines.sourceName())
                        results.append(newFeat)

                # Case 2: Reverse direction intersection
                elif (
                    g2NextVertexIdx == g1PreviousVertexIdx == -1
                    and g2PreviousVertexIdx > 0
                    and g1NextVertexIdx < len(vg1) - 1
                ):
                    # Create sequence of 4 points that might form a Z angle
                    points = [
                        vg2[g2PreviousVertexIdx - 1],
                        vg2[g2PreviousVertexIdx],
                        vg2[g2VertexIdx],
                        vg1[g1NextVertexIdx],
                    ]

                    # Calculate angles between points
                    angle1 = math.degrees(
                        QgsGeometryUtils.angleBetweenThreePoints(
                            points[0].x(),
                            points[0].y(),
                            points[1].x(),
                            points[1].y(),
                            points[2].x(),
                            points[2].y(),
                        )
                    )
                    angle2 = math.degrees(
                        QgsGeometryUtils.angleBetweenThreePoints(
                            points[1].x(),
                            points[1].y(),
                            points[2].x(),
                            points[2].y(),
                            points[3].x(),
                            points[3].y(),
                        )
                    )

                    # Check if this forms a Z angle
                    if self._is_z_angle(angle1, angle2):
                        newFeat = QgsFeature(self.fields)
                        if isinstance(points[0], QgsPoint):
                            newFeat.setGeometry(QgsGeometry.fromPolyline(points))
                        elif isinstance(points[0], QgsPointXY):
                            newFeat.setGeometry(QgsGeometry.fromPolylineXY(points))
                        newFeat.setAttribute("source", lines.sourceName())
                        results.append(newFeat)

            # Check for 3-way intersections (when dealing with short segments)
            if len(results) == 0 and len(self.vertex_cache.get(feat1_id, [])) == 2:
                # Find other line features that might intersect with feat2
                bbox = gfeat2.boundingBox()
                candidate_ids = self.spatial_index.intersects(bbox)

                # Look for features that intersect with feat2
                for feat3_id in candidate_ids:
                    # Skip cases we've already processed or self-intersections
                    if not (feat3_id < feat1_id and feat3_id < feat2_id):
                        continue

                    gfeat3 = self.geom_cache[feat3_id]

                    # Check if feat3 touches feat1 at an endpoint
                    if gfeat3.touches(gfeat1):
                        # Test if these three features form a Z angle
                        three_way_results = self._check_three_way_intersection(
                            gfeat1,
                            gfeat2,
                            gfeat3,
                            feat1_id,
                            feat2_id,
                            feat3_id,
                            lines.sourceName(),
                        )
                        if three_way_results:
                            results.extend(three_way_results)

            return results

        # Prepare all possible feature pairs to process
        all_feature_ids = list(self.feature_cache.keys())

        # Use spatial index to reduce the number of potential pairs to check
        potential_pairs = []

        for feat1_id in all_feature_ids:
            # Get the bounding box from the cached geometry
            bbox = self.geom_cache[feat1_id].boundingBox()

            # Find potential candidates using spatial index
            candidates = self.spatial_index.intersects(bbox)

            # Only consider feature pairs where ID2 > ID1 to avoid duplicates
            candidates = [c for c in candidates if c > feat1_id]

            # Add candidate pairs to the list
            potential_pairs.extend([(feat1_id, candidate) for candidate in candidates])

        # Process pairs using concurrently
        feedback.pushInfo(
            self.tr(f"Processing {len(potential_pairs)} potential feature pairs")
        )
        for result in concurrently(
            process_line_pair, potential_pairs, feedback=feedback
        ):
            if result:
                featsToAnalyse.extend(result)

        return featsToAnalyse

    def _check_three_way_intersection(
        self, g1, g2, g3, feat1_id, feat2_id, feat3_id, source_name
    ):
        """Check if three line features form Z angles at their intersections"""
        results = []

        # Get intersection points
        inter12 = g1.intersection(g2)
        inter23 = g2.intersection(g3)

        # Verify intersections are valid points
        if (
            inter12.wkbType() != QgsWkbTypes.Point
            or inter23.wkbType() != QgsWkbTypes.Point
        ):
            return []

        inter12 = inter12.asPoint()
        inter23 = inter23.asPoint()

        # Get closest vertices to intersections
        _, g1VertexIdx, g1PreviousVertexIdx, g1NextVertexIdx, _ = g1.closestVertex(
            inter12
        )
        _, g3VertexIdx, g3PreviousVertexIdx, g3NextVertexIdx, _ = g3.closestVertex(
            inter23
        )

        # Get vertices from cache or create and cache them
        if feat1_id not in self.vertex_cache:
            self.vertex_cache[feat1_id] = list(g1.vertices())
        if feat3_id not in self.vertex_cache:
            self.vertex_cache[feat3_id] = list(g3.vertices())

        vg1 = self.vertex_cache[feat1_id]
        vg3 = self.vertex_cache[feat3_id]

        # Case 1: First configuration
        if g1NextVertexIdx == g3PreviousVertexIdx == -1:
            # Only process if we have valid vertex indices
            if (
                g1PreviousVertexIdx >= 0
                and g1VertexIdx >= 0
                and g3VertexIdx >= 0
                and g3NextVertexIdx >= 0
            ):

                points = [
                    vg1[g1PreviousVertexIdx],
                    vg1[g1VertexIdx],
                    vg3[g3VertexIdx],
                    vg3[g3NextVertexIdx],
                ]

                # Calculate angles
                angle1 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        points[0].x(),
                        points[0].y(),
                        points[1].x(),
                        points[1].y(),
                        points[2].x(),
                        points[2].y(),
                    )
                )
                angle2 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        points[1].x(),
                        points[1].y(),
                        points[2].x(),
                        points[2].y(),
                        points[3].x(),
                        points[3].y(),
                    )
                )

                # Check if this forms a Z angle
                if self._is_z_angle(angle1, angle2):
                    newFeat = QgsFeature(self.fields)
                    if isinstance(points[0], QgsPoint):
                        newFeat.setGeometry(QgsGeometry.fromPolyline(points))
                    elif isinstance(points[0], QgsPointXY):
                        newFeat.setGeometry(QgsGeometry.fromPolylineXY(points))
                    newFeat.setAttribute("source", source_name)
                    results.append(newFeat)

        # Case 2: Reverse configuration
        elif g3NextVertexIdx == g1PreviousVertexIdx == -1:
            # Only process if we have valid vertex indices
            if (
                g3PreviousVertexIdx >= 0
                and g3VertexIdx >= 0
                and g1VertexIdx >= 0
                and g1NextVertexIdx >= 0
            ):

                points = [
                    vg3[g3PreviousVertexIdx],
                    vg3[g3VertexIdx],
                    vg1[g1VertexIdx],
                    vg1[g1NextVertexIdx],
                ]

                # Calculate angles
                angle1 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        points[0].x(),
                        points[0].y(),
                        points[1].x(),
                        points[1].y(),
                        points[2].x(),
                        points[2].y(),
                    )
                )
                angle2 = math.degrees(
                    QgsGeometryUtils.angleBetweenThreePoints(
                        points[1].x(),
                        points[1].y(),
                        points[2].x(),
                        points[2].y(),
                        points[3].x(),
                        points[3].y(),
                    )
                )

                # Check if this forms a Z angle
                if self._is_z_angle(angle1, angle2):
                    newFeat = QgsFeature(self.fields)
                    if isinstance(points[0], QgsPoint):
                        newFeat.setGeometry(QgsGeometry.fromPolyline(points))
                    elif isinstance(points[0], QgsPointXY):
                        newFeat.setGeometry(QgsGeometry.fromPolylineXY(points))
                    newFeat.setAttribute("source", source_name)
                    results.append(newFeat)

        return results

    def _is_z_angle(self, angle1, angle2):
        """Check if two angles form a Z angle pattern based on threshold criteria"""
        # Using pre-computed thresholds for efficiency
        return (
            angle1 > self.angle_threshold and angle2 < self.angle_threshold_complement
        ) or (
            angle1 < self.angle_threshold_complement and angle2 > self.angle_threshold
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyzanglesbetweenfeatures"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Z Angles Between Features")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Basic Geometry Construction Issues Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Basic Geometry Construction Issues Handling"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyZAnglesBetweenFeaturesAlgorithm", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyZAnglesBetweenFeaturesAlgorithm()
