# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-01-31
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Brazilian Army
        email                : ...
 ***************************************************************************/
"""

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsWkbTypes,
    QgsGeometry,
    QgsLineString,
    QgsMultiLineString,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingUtils,
    QgsPointXY,
)
import numpy as np
from scipy.interpolate import splprep, splev


class NURBFitSmoothingAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    DEGREE = "DEGREE"
    SEGMENT_LENGTH = "SEGMENT_LENGTH"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.DEGREE,
                self.tr("Degree of basis polynomial"),
                type=QgsProcessingParameterNumber.Integer,
                minValue=2,
                defaultValue=3,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEGMENT_LENGTH,
                self.tr("Segment length (0 = automatic)"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Smoothed"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        degree = self.parameterAsInt(parameters, self.DEGREE, context)
        segment_length = self.parameterAsDouble(
            parameters, self.SEGMENT_LENGTH, context
        )

        if input_layer is None:
            raise QgsProcessingException(self.tr("Invalid input layer"))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            input_layer.fields(),
            QgsWkbTypes.LineString,
            input_layer.sourceCrs(),
        )

        total = 100.0 / input_layer.featureCount() if input_layer.featureCount() else 0
        features = input_layer.getFeatures()

        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            geom = feature.geometry()
            if geom.isNull() or geom.isEmpty():
                continue

            smoothed_geom = self._smooth_geometry(geom, degree, segment_length)
            if smoothed_geom is not None:
                out_feature = QgsFeature()
                out_feature.setGeometry(smoothed_geom)
                out_feature.setAttributes(feature.attributes())
                sink.addFeature(out_feature, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def _smooth_geometry(self, geometry, degree, segment_length):
        """Smooth a line geometry using B-spline (NURBfit)"""
        if geometry.isMultipart():
            parts = []
            for part in geometry.asMultiPolyline():
                smoothed = self._smooth_line(part, degree, segment_length)
                if smoothed:
                    parts.append(smoothed)
            if parts:
                return QgsGeometry.fromMultiPolylineXY(parts)
        else:
            line = geometry.asPolyline()
            smoothed = self._smooth_line(line, degree, segment_length)
            if smoothed:
                return QgsGeometry.fromPolylineXY(smoothed)
        return None

    def _smooth_line(self, line, degree, segment_length):
        """Apply B-spline smoothing to a line"""
        if len(line) < degree + 1:
            return line

        x = [p.x() for p in line]
        y = [p.y() for p in line]

        try:
            tck, u = splprep([x, y], s=0, k=min(degree, len(line) - 1))

            if segment_length <= 0:
                num_points = len(line) * 10
            else:
                total_length = sum(
                    line[i].distance(line[i + 1]) for i in range(len(line) - 1)
                )
                num_points = max(int(total_length / segment_length), len(line))

            u_new = np.linspace(0, 1, num_points)
            x_new, y_new = splev(u_new, tck)

            output_list = [QgsPointXY(float(x_new[i]), float(y_new[i])) for i in range(len(x_new))]

        except Exception:
            return line
        output_list[0] = QgsPointXY(float(x[0]), float(y[0]))
        output_list[-1] = QgsPointXY(float(x[-1]), float(y[-1]))
        return output_list

    def name(self):
        return "nurbfitsmoothingalgorithm"

    def displayName(self):
        return self.tr("NURBfit Line Smoothing")

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
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return NURBFitSmoothingAlgorithm()

    def shortHelpString(self):
        return self.tr(
            "Smooths line geometries using NURBfit algorithm (B-Spline curves).\n\n"
            "The algorithm fits B-Spline curves to input features and strokes the results "
            "to output linear geometry. Higher degrees produce smoother curves.\n\n"
            "Parameters:\n"
            "- Degree: Polynomial degree (2-5 recommended, higher = smoother)\n"
            "- Segment Length: Length of output segments in map units (0 = automatic, "
            "generates 10x original points)"
        )
