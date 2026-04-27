# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-04-10
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Brazilian Army
        email                : ...
 ***************************************************************************/
"""

import uuid

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea,
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)
import numpy as np


class GeneralizeContourLinesAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    ELEVATION_ATTR = "ELEVATION_ATTR"
    MIN_CLOSED_LENGTH = "MIN_CLOSED_LENGTH"
    FRAME = "FRAME"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input contour lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ELEVATION_ATTR,
                self.tr("Elevation attribute"),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_CLOSED_LENGTH,
                self.tr("Minimum length for closed contours (meters)"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=200,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FRAME,
                self.tr("Frame layer (clip boundary)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr("Prepared contour lines")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            from scipy.interpolate import splprep, splev
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python scipy library. Please install this library and try again."
                )
            )
        inputLayer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        elevAttr = self.parameterAsString(parameters, self.ELEVATION_ATTR, context)
        minClosedLength = self.parameterAsDouble(
            parameters, self.MIN_CLOSED_LENGTH, context
        )
        frameLayer = self.parameterAsVectorLayer(parameters, self.FRAME, context)

        if inputLayer is None:
            raise QgsProcessingException(self.tr("Invalid input layer"))
        if frameLayer is None:
            raise QgsProcessingException(self.tr("Invalid frame layer"))

        sourceCrs = inputLayer.sourceCrs()
        projectedCrs = self._getProjectedCrs(inputLayer)
        toProjected = QgsCoordinateTransform(
            sourceCrs, projectedCrs, context.transformContext()
        )
        toOriginal = QgsCoordinateTransform(
            projectedCrs, sourceCrs, context.transformContext()
        )
        needsTransform = sourceCrs != projectedCrs

        # Build frame geometry (dissolve all frame features)
        frameGeom = QgsGeometry()
        for frameFeat in frameLayer.getFeatures():
            g = frameFeat.geometry()
            if g.isNull() or g.isEmpty():
                continue
            frameGeom = g if frameGeom.isNull() else frameGeom.combine(g)

        if frameGeom.isNull() or frameGeom.isEmpty():
            raise QgsProcessingException(self.tr("Frame layer has no valid geometries"))

        # Transform frame to input CRS if needed
        frameCrs = frameLayer.sourceCrs()
        if frameCrs != sourceCrs:
            frameToInput = QgsCoordinateTransform(
                frameCrs, sourceCrs, context.transformContext()
            )
            frameGeom.transform(frameToInput)

        # Output fields (EDGV schema)
        outFields = QgsFields()
        outFields.append(QgsField("id", QVariant.String, "varchar", 254))
        outFields.append(QgsField("cota", QVariant.Int, "int4"))
        outFields.append(QgsField("indice", QVariant.Int, "int2"))
        outFields.append(QgsField("depressao", QVariant.Int, "int2"))
        outFields.append(QgsField("visivel", QVariant.Int, "int2"))
        outFields.append(QgsField("dentro_massa_dagua", QVariant.Int, "int2"))
        outFields.append(QgsField("texto_edicao", QVariant.String, "varchar", 255))
        outFields.append(QgsField("observacao", QVariant.String, "varchar", 255))

        (sink, destId) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outFields,
            QgsWkbTypes.MultiLineString,
            sourceCrs,
        )

        # Step 1: Collect all single-part lines grouped by elevation
        feedback.setProgressText(self.tr("Step 1/6: Collecting and exploding geometries..."))
        elevGroups = {}
        featureCount = inputLayer.featureCount()
        total = 100.0 / featureCount if featureCount else 0

        for current, feat in enumerate(inputLayer.getFeatures()):
            if feedback.isCanceled():
                return {self.OUTPUT: destId}

            geom = feat.geometry()
            if geom.isNull() or geom.isEmpty():
                continue

            cotaValue = feat[elevAttr]
            if cotaValue is None or cotaValue == QVariant():
                continue
            cotaValue = int(cotaValue)

            # Explode multipart to single parts
            parts = self._explodeToParts(geom)
            if cotaValue not in elevGroups:
                elevGroups[cotaValue] = []
            elevGroups[cotaValue].extend(parts)

            feedback.setProgress(int(current * total * 0.1))

        feedback.setProgress(10)
        if feedback.isCanceled():
            return {self.OUTPUT: destId}

        # Step 2: Merge connected lines per elevation group
        feedback.setProgressText(self.tr("Step 2/6: Merging connected lines..."))
        mergedLines = []
        groupCount = len(elevGroups)
        for i, (cota, parts) in enumerate(elevGroups.items()):
            if feedback.isCanceled():
                return {self.OUTPUT: destId}

            merged = self._mergeConnectedLines(parts)
            for line in merged:
                mergedLines.append((cota, line))

            feedback.setProgress(10 + int((i / max(groupCount, 1)) * 10))

        feedback.setProgress(20)
        if feedback.isCanceled():
            return {self.OUTPUT: destId}

        # Step 3: Remove duplicate vertices
        feedback.setProgressText(self.tr("Step 3/6: Validating geometries..."))
        validLines = []
        for cota, geom in mergedLines:
            geom.removeDuplicateNodes()
            if not geom.isNull() and not geom.isEmpty():
                validLines.append((cota, geom))
        mergedLines = validLines

        # Step 4: Filter closed curves by minimum length
        feedback.setProgressText(
            self.tr("Step 4/6: Filtering small closed contours (< %1 m)...").replace(
                "%1", str(minClosedLength)
            )
        )
        filteredLines = []
        da = QgsDistanceArea()
        da.setSourceCrs(sourceCrs, context.transformContext())
        da.setEllipsoid(context.ellipsoid())

        for cota, geom in mergedLines:
            if feedback.isCanceled():
                return {self.OUTPUT: destId}

            polyline = self._geometryToPolyline(geom)
            if polyline is None:
                continue

            isClosed = self._isClosed(polyline)
            if isClosed:
                length = da.measureLength(geom)
                if length < minClosedLength:
                    continue

            filteredLines.append((cota, geom))

        feedback.setProgress(35)
        if feedback.isCanceled():
            return {self.OUTPUT: destId}

        # Step 5: Generalization chain: Douglas(2m) → NURBfit(degree=3) → Douglas(3m)
        feedback.setProgressText(
            self.tr("Step 5/6: Generalizing (Douglas → NURBfit → Douglas)...")
        )
        generalizedLines = []
        lineCount = len(filteredLines)

        for i, (cota, geom) in enumerate(filteredLines):
            if feedback.isCanceled():
                return {self.OUTPUT: destId}

            # Transform to projected CRS for metric Douglas-Peucker
            if needsTransform:
                geom.transform(toProjected)

            # Douglas-Peucker 2m
            geom = geom.simplify(2.0)
            if geom.isNull() or geom.isEmpty():
                continue

            # NURBfit (degree=3, s=0 interpolation)
            geom = self._nurbfitSmooth(geom)
            if geom.isNull() or geom.isEmpty():
                continue

            # Douglas-Peucker 3m
            geom = geom.simplify(3.0)
            if geom.isNull() or geom.isEmpty():
                continue

            # Transform back to original CRS
            if needsTransform:
                geom.transform(toOriginal)

            generalizedLines.append((cota, geom))

            feedback.setProgress(35 + int((i / max(lineCount, 1)) * 45))

        feedback.setProgress(80)
        if feedback.isCanceled():
            return {self.OUTPUT: destId}

        # Step 6: Clip by frame and create output features
        feedback.setProgressText(self.tr("Step 6/6: Clipping by frame and writing output..."))
        outputCount = len(generalizedLines)

        for i, (cota, geom) in enumerate(generalizedLines):
            if feedback.isCanceled():
                return {self.OUTPUT: destId}

            clipped = geom.intersection(frameGeom)
            if clipped.isNull() or clipped.isEmpty():
                continue

            # Ensure MultiLineString output
            if clipped.wkbType() in (
                QgsWkbTypes.LineString,
                QgsWkbTypes.LineStringZ,
                QgsWkbTypes.LineStringM,
                QgsWkbTypes.LineStringZM,
            ):
                clipped = QgsGeometry.collectGeometry([clipped])
            elif clipped.wkbType() in (
                QgsWkbTypes.GeometryCollection,
                QgsWkbTypes.GeometryCollectionZ,
            ):
                # Extract only line parts from geometry collection
                lineParts = []
                for part in clipped.asGeometryCollection():
                    if part.type() == Qgis.GeometryType.Line:
                        lineParts.append(part)
                if not lineParts:
                    continue
                clipped = QgsGeometry.collectGeometry(lineParts)

            # Skip non-line results (point intersections, etc.)
            if clipped.type() != Qgis.GeometryType.Line:
                continue

            outFeat = QgsFeature(outFields)
            outFeat.setGeometry(clipped)
            outFeat.setAttributes([
                str(uuid.uuid4()),     # id
                int(cota),             # cota
                2,                     # indice
                2,                     # depressao
                1,                     # visivel
                2,                     # dentro_massa_dagua
                str(int(cota)),        # texto_edicao
                "",                    # observacao
            ])
            sink.addFeature(outFeat, QgsFeatureSink.FastInsert)

            feedback.setProgress(80 + int((i / max(outputCount, 1)) * 20))

        feedback.setProgress(100)
        return {self.OUTPUT: destId}

    def _getProjectedCrs(self, layer):
        """Return a suitable projected CRS for metric operations.
        If the layer CRS is already projected (metric), return it as-is.
        Otherwise compute the UTM zone from the layer extent centroid.
        """
        crs = layer.sourceCrs()
        if not crs.isGeographic():
            return crs
        extent = layer.extent()
        lon = extent.center().x()
        lat = extent.center().y()
        zone = int((lon + 180) / 6) + 1
        epsg = 32600 + zone if lat >= 0 else 32700 + zone
        return QgsCoordinateReferenceSystem(f"EPSG:{epsg}")

    def _explodeToParts(self, geometry):
        """Explode a (possibly multi-part) geometry into single LineString geometries."""
        parts = []
        if geometry.isMultipart():
            for part in geometry.asMultiPolyline():
                if len(part) >= 2:
                    parts.append(QgsGeometry.fromPolylineXY(part))
        else:
            polyline = geometry.asPolyline()
            if len(polyline) >= 2:
                parts.append(QgsGeometry.fromPolylineXY(polyline))
        return parts

    def _mergeConnectedLines(self, geometries):
        """Merge a list of single-part line geometries that share endpoints.
        Equivalent to FME LineCombiner.
        """
        if not geometries:
            return []
        # Collect all into a single multi-line and use mergeLines
        multi = QgsGeometry.collectGeometry(geometries)
        merged = multi.mergeLines()
        if merged.isNull() or merged.isEmpty():
            return geometries
        # The result may be multi-part (disjoint groups)
        if merged.isMultipart():
            result = []
            for part in merged.asMultiPolyline():
                if len(part) >= 2:
                    result.append(QgsGeometry.fromPolylineXY(part))
            return result
        else:
            return [merged]

    def _geometryToPolyline(self, geometry):
        """Extract a polyline (list of QgsPointXY) from a geometry."""
        if geometry.isMultipart():
            parts = geometry.asMultiPolyline()
            return parts[0] if parts else None
        return geometry.asPolyline()

    def _isClosed(self, polyline, tolerance=1e-8):
        """Check if a polyline is closed (ring)."""
        if len(polyline) < 3:
            return False
        return polyline[0].distance(polyline[-1]) < tolerance

    def _nurbfitSmooth(self, geometry, degree=3):
        """Apply NURBfit B-spline interpolation (s=0) to a line geometry."""
        if geometry.isMultipart():
            parts = []
            for part in geometry.asMultiPolyline():
                smoothed = self._nurbfitLine(part, degree)
                if smoothed:
                    parts.append(smoothed)
            if parts:
                return QgsGeometry.fromMultiPolylineXY(parts)
            return geometry
        else:
            polyline = geometry.asPolyline()
            smoothed = self._nurbfitLine(polyline, degree)
            if smoothed:
                return QgsGeometry.fromPolylineXY(smoothed)
            return geometry

    def _nurbfitLine(self, line, degree=3):
        """Apply B-spline interpolation to a polyline."""
        from scipy.interpolate import splprep, splev
        if len(line) <= degree + 1:
            return line

        x = np.array([p.x() for p in line])
        y = np.array([p.y() for p in line])

        closed = self._isClosed(line)
        if closed:
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
                [x_norm, y_norm], s=0, k=degree, per=1 if closed else 0
            )

            numPoints = len(line) * 10
            u_new = np.linspace(0, 1, numPoints)
            xn_new, yn_new = splev(u_new, tck)

            x_new = xn_new * scale + x_min
            y_new = yn_new * scale + y_min

            output = [
                QgsPointXY(float(xi), float(yi))
                for xi, yi in zip(x_new, y_new)
            ]

            if not closed:
                output[0] = QgsPointXY(float(x[0]), float(y[0]))
                output[-1] = QgsPointXY(float(x[-1]), float(y[-1]))
            else:
                output[-1] = output[0]

            return output
        except Exception:
            return line

    def name(self):
        return "generalizecontourlines"

    def displayName(self):
        return self.tr("Generalize Contour Lines")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeContourLinesAlgorithm", string)

    def createInstance(self):
        return GeneralizeContourLinesAlgorithm()

    def shortHelpString(self):
        return self.tr(
            "Prepares raw contour lines for cartographic production following "
            "the EDGV standard.\n\n"
            "The algorithm performs the following steps:\n"
            "1. Explodes multipart geometries and merges connected lines at "
            "the same elevation\n"
            "2. Removes duplicate vertices\n"
            "3. Filters out closed contours shorter than the specified minimum "
            "length\n"
            "4. Applies a three-step generalization chain:\n"
            "   a) Douglas-Peucker simplification (2 m tolerance)\n"
            "   b) NURBfit B-spline interpolation (degree 3)\n"
            "   c) Douglas-Peucker simplification (3 m tolerance)\n"
            "5. Clips the result to the frame boundary\n"
            "6. Creates output features with EDGV attributes (id, cota, "
            "indice, depressao, visivel, dentro_massa_dagua, texto_edicao)\n\n"
            "The algorithm handles non-metric coordinate systems by "
            "automatically projecting to an appropriate UTM zone for metric "
            "operations.\n\n"
            "Parameters:\n"
            "- Input contour lines: Raw contour line layer\n"
            "- Elevation attribute: Field containing the elevation value\n"
            "- Minimum length for closed contours: Closed contour lines "
            "shorter than this value (in meters) will be removed\n"
            "- Frame layer: Polygon layer used to clip the output"
        )
