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

import math
from itertools import product

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureSink,
    QgsField,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsRectangle,
    QgsSpatialIndex,
)


class SplitPolygons(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    PARAM = "PARAM"
    OVERLAP = "OVERLAP"
    OUTPUT = "OUTPUT"
    SPLIT_FACTORS = ["1/1", "1/4", "1/9", "1/16"]

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, "Input polygon layer", [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.PARAM,
                "Splitting factor",
                options=self.SPLIT_FACTORS,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP,
                "Overlap value",
                QgsProcessingParameterNumber.Double,
                defaultValue=0.002,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Output split polygons")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        split_factor = self.parameterAsEnum(parameters, self.PARAM, context)
        overlap = self.parameterAsDouble(parameters, self.OVERLAP, context)

        # Add a new field called "priority" to the output layer's fields
        fields = source.fields()
        fields.append(QgsField("priority", QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        # Create a spatial index
        index = QgsSpatialIndex(source)

        parts = [1, 4, 9, 16][split_factor]
        side_length = math.sqrt(1 / parts)
        col_steps = int(math.sqrt(parts))
        row_steps = col_steps

        polygons = []
        for current, feature in enumerate(features, start=1):
            if feedback.isCanceled():
                break

            geometry = feature.geometry()

            if parts == 0:
                new_feature = QgsFeature(feature)
                new_feature.setFields(fields)
                new_feature.setGeometry(geometry)
                polygons.append(new_feature)
                continue

            xmin, ymin, xmax, ymax = geometry.boundingBox().toRectF().getCoords()
            width = xmax - xmin
            height = ymax - ymin

            for i, j in product(range(col_steps), range(row_steps)):
                if feedback.isCanceled():
                    break
                x1 = xmin + (width * i * side_length)
                y1 = ymin + (height * j * side_length)
                x2 = xmin + (width * (i + 1) * side_length)
                y2 = ymin + (height * (j + 1) * side_length)

                new_geom = QgsGeometry.fromRect(QgsRectangle(x1, y1, x2, y2))

                # Use the spatial index to find intersecting features
                candidate_ids = index.intersects(new_geom.boundingBox())
                if not candidate_ids:
                    continue

                intersected_geom = new_geom.intersection(geometry)

                if intersected_geom.isEmpty():
                    continue

                # Buffer the new geometry
                buffered_geom = intersected_geom.buffer(
                    overlap, 5
                )  # 5 is the default number of segments per quarter circle

                # Use the spatial index to find intersecting features
                candidate_ids = index.intersects(buffered_geom.boundingBox())
                if not candidate_ids:
                    continue

                # Extract intersecting features
                intersecting_features = [
                    f
                    for f in source.getFeatures(
                        QgsFeatureRequest().setFilterFids(candidate_ids)
                    )
                ]

                # Dissolve only intersecting features
                dissolved_geometry = QgsGeometry.unaryUnion(
                    [f.geometry() for f in intersecting_features]
                )

                # Clip the buffered geometry by the dissolved geometry
                intersected_geom = buffered_geom.intersection(dissolved_geometry)

                if intersected_geom.isEmpty():
                    continue

                new_feature = QgsFeature(feature)
                new_feature.setGeometry(intersected_geom)
                new_feature.setFields(fields)
                polygons.append(new_feature)
            feedback.setProgress(current * total)

        polygons.sort(
            key=lambda x: (
                x.geometry().centroid().asPoint().y(),
                x.geometry().centroid().asPoint().x(),
            )
            if not x.geometry().isNull()
            else (0, 0),
            reverse=True,
        )
        for priority_counter, polygon in enumerate(polygons, start=1):
            polygon.setAttribute("priority", priority_counter)
            sink.addFeature(polygon, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}

    def name(self):
        return "splitpolygons"

    def displayName(self):
        return "Split Polygons"

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
        return QCoreApplication.translate("SplitPolygons", string)

    def createInstance(self):
        return SplitPolygons()
