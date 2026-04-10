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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsGeometry,
    QgsFeature,
    QgsFeatureSink,
    QgsPointXY,
)
import numpy as np
from scipy.interpolate import splprep, splev


class NURBFitSmoothingAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    DEGREE = "DEGREE"
    SMOOTHING_FACTOR = "SMOOTHING_FACTOR"
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
                self.SMOOTHING_FACTOR,
                self.tr("Smoothing factor (0 = interpolation only)"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=1.0,
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
        smoothing_factor = self.parameterAsDouble(
            parameters, self.SMOOTHING_FACTOR, context
        )
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
            input_layer.wkbType(),
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

            smoothed_geom = self._smooth_geometry(geom, degree, smoothing_factor, segment_length, feedback)
            if smoothed_geom is not None:
                out_feature = QgsFeature()
                out_feature.setGeometry(smoothed_geom)
                out_feature.setAttributes(feature.attributes())
                sink.addFeature(out_feature, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def _is_closed(self, line, tolerance=1e-8):
        """Check if line is closed (ring)"""
        if len(line) < 3:
            return False
        return line[0].distance(line[-1]) < tolerance

    def _smooth_geometry(self, geometry, degree, smoothing_factor, segment_length, feedback=None):
        """Smooth a line geometry using B-spline (NURBfit)"""
        if geometry.isMultipart():
            parts = []
            for part in geometry.asMultiPolyline():
                smoothed = self._smooth_line(part, degree, smoothing_factor, segment_length, feedback)
                if smoothed:
                    parts.append(smoothed)
            if parts:
                return QgsGeometry.fromMultiPolylineXY(parts)
        else:
            line = geometry.asPolyline()
            smoothed = self._smooth_line(line, degree, smoothing_factor, segment_length, feedback)
            if smoothed:
                return QgsGeometry.fromPolylineXY(smoothed)
        return None

    def _smooth_line(self, line, degree, smoothing_factor, segment_length, feedback=None):
        """Apply B-spline smoothing to a line"""
        if len(line) <= degree + 1:
            return line

        x = np.array([p.x() for p in line])
        y = np.array([p.y() for p in line])

        is_closed = self._is_closed(line)

        if is_closed:
            x[-1] = x[0]
            y[-1] = y[0]

        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()
        scale = max(x_max - x_min, y_max - y_min)
        if scale < 1e-12:
            return line
        x_norm = (x - x_min) / scale
        y_norm = (y - y_min) / scale

        try:
            tck, u = splprep(
                [x_norm, y_norm],
                s=smoothing_factor,
                k=degree,
                per=1 if is_closed else 0,
            )

            if segment_length <= 0:
                num_points = len(line) * 10
            else:
                total_length = sum(
                    line[i].distance(line[i + 1]) for i in range(len(line) - 1)
                )
                num_points = max(int(total_length / segment_length), len(line))

            u_new = np.linspace(0, 1, num_points)
            xn_new, yn_new = splev(u_new, tck)

            x_new = xn_new * scale + x_min
            y_new = yn_new * scale + y_min

            output_list = [
                QgsPointXY(float(xi), float(yi))
                for xi, yi in zip(x_new, y_new)
            ]

            if not is_closed:
                output_list[0] = QgsPointXY(float(x[0]), float(y[0]))
                output_list[-1] = QgsPointXY(float(x[-1]), float(y[-1]))
            else:
                output_list[-1] = output_list[0]

            return output_list

        except Exception as e:
            if feedback:
                feedback.pushWarning(
                    self.tr(f"Could not smooth line with {len(line)} vertices: {str(e)}")
                )
            return line

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
            "- Smoothing factor: Controls how much the curve deviates from the original "
            "vertices. 0 = exact interpolation (no smoothing), higher values = more "
            "smoothing. Recommended range: 0.1 to 10.\n"
            "- Segment Length: Length of output segments in map units (0 = automatic, "
            "generates 10x original points)"
        )
