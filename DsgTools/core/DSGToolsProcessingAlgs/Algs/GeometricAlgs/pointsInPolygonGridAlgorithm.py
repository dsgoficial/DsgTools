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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
)
import math
from qgis.core import QgsFeature, QgsGeometry, QgsPointXY, QgsWkbTypes
from itertools import product


class PointsInPolygonGridAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    X_DISTANCE = "X_DISTANCE"
    Y_DISTANCE = "Y_DISTANCE"
    OUTPUT = "OUTPUT"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return PointsInPolygonGridAlgorithm()

    def name(self):
        return "points_in_polygon_grid_old"

    def displayName(self):
        return self.tr("Points In Polygon Grid old")

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
            "Create a layer of points evenly spaced with X and Y distances for each polygon in the input layer."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.X_DISTANCE, self.tr("X Distance"), defaultValue=0.01
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.Y_DISTANCE, self.tr("Y Distance"), defaultValue=0.01
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr("Output point layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        x_distance = self.parameterAsDouble(parameters, self.X_DISTANCE, context)
        y_distance = self.parameterAsDouble(parameters, self.Y_DISTANCE, context)

        fields = source.fields()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Point,
            source.sourceCrs(),
        )

        total = 100.0 / source.featureCount() if source.featureCount() else 0

        for current, feature in enumerate(source.getFeatures()):
            if feedback.isCanceled():
                break

            geometry = feature.geometry()
            if geometry.isEmpty() or geometry.isNull():
                continue

            bbox = geometry.boundingBox()
            x_min, y_min, x_max, y_max = (
                bbox.xMinimum(),
                bbox.yMinimum(),
                bbox.xMaximum(),
                bbox.yMaximum(),
            )

            point_coordinates = (
                QgsGeometry.fromPointXY(
                    QgsPointXY(x_min + i * x_distance, y_min + j * y_distance)
                )
                for i, j in product(
                    range(int(math.ceil((x_max - x_min) / x_distance)) + 1),
                    range(int(math.ceil((y_max - y_min) / y_distance)) + 1),
                )
            )

            for point_geom in point_coordinates:
                if geometry.contains(point_geom):
                    new_feature = QgsFeature(fields)
                    new_feature.setGeometry(point_geom)
                    new_feature.setAttributes(feature.attributes())
                    sink.addFeature(new_feature)

            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}
