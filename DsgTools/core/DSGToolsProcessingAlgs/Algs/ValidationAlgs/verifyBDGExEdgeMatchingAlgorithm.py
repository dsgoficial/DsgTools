# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-03-04
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

import tempfile
import zipfile
from pathlib import Path

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import runProcessing
from qgis.PyQt.QtCore import QCoreApplication, QMetaType
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsRectangle,
    QgsSpatialIndex,
    QgsVectorLayer,
    QgsWkbTypes,
)

from .validationAlgorithm import ValidationAlgorithm


class VerifyBDGExEdgeMatchingAlgorithm(ValidationAlgorithm):
    ZIP_FOLDER = "ZIP_FOLDER"
    SCALE = "SCALE"
    SEARCH_RADIUS = "SEARCH_RADIUS"
    ATTRIBUTE_BLACKLIST = "ATTRIBUTE_BLACKLIST"
    IGNORE_FIELD_LENGTHS = "IGNORE_FIELD_LENGTHS"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"

    # Maps our scale index → createFramesWithConstraintAlgorithm STOP_SCALE index.
    # createFramesWithConstraintAlgorithm scales:
    #   ["1000k","500k","250k","100k","50k","25k","10k","5k","2k","1k"]
    #    idx 0     1     2     3     4     5     6    7    8    9
    _SCALE_INDEX_MAP = {0: 2, 1: 3, 2: 4, 3: 5}

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.ZIP_FOLDER,
                self.tr("Folder with BDGEx zip files"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.scales = ["1:250.000", "1:100.000", "1:50.000", "1:25.000"]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE,
                self.tr("Scale"),
                options=self.scales,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr("Search radius"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0.0,
                defaultValue=0.0001,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.ATTRIBUTE_BLACKLIST,
                self.tr("Attribute blacklist (comma-separated field names to ignore)"),
                optional=True,
                defaultValue="",
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_FIELD_LENGTHS,
                self.tr("Ignore field length differences"),
                defaultValue=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr("Point Flags"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS,
                self.tr("Line Flags"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        zipFolderPath = self.parameterAsString(parameters, self.ZIP_FOLDER, context)
        scaleIdx = self.parameterAsEnum(parameters, self.SCALE, context)
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        blacklistStr = self.parameterAsString(
            parameters, self.ATTRIBUTE_BLACKLIST, context
        )
        attributeBlacklist = (
            {a.strip() for a in blacklistStr.split(",") if a.strip()}
            if blacklistStr
            else set()
        )
        ignoreFieldLengths = self.parameterAsBool(
            parameters, self.IGNORE_FIELD_LENGTHS, context
        )
        constraintScaleIdx = self._SCALE_INDEX_MAP[scaleIdx]

        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)

        # Step 1: Load zip files
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Loading zip files..."))
        zipData = self._loadZipFiles(zipFolderPath, multiStepFeedback)
        if not zipData:
            raise QgsProcessingException(
                self.tr("No valid shapefiles found in the specified folder.")
            )

        # Step 1b: Global schema validation — abort with full details on mismatch
        multiStepFeedback.pushInfo(self.tr("Validating shapefile schemas..."))
        self._validateSchemas(zipData, ignoreFieldLengths, multiStepFeedback)

        # Prepare output sink using the CRS of the first loaded layer
        refCrs = self._getRefCrs(zipData)
        fields = QgsFields()
        fields.append(QgsField("reason", QMetaType.Type.QString))
        (pointFlagSink, pointFlagSinkId) = self.parameterAsSink(
            parameters,
            self.POINT_FLAGS,
            context,
            fields,
            QgsWkbTypes.Point,
            refCrs,
        )
        if pointFlagSink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.POINT_FLAGS)
            )

        (lineFlagSink, lineFlagSinkId) = self.parameterAsSink(
            parameters,
            self.LINE_FLAGS,
            context,
            fields,
            QgsWkbTypes.LineString,
            refCrs,
        )
        if lineFlagSink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.LINE_FLAGS)
            )

        # Step 2: Build systematic grid, filter to cells with real data
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Building systematic grid..."))
        cellFeatDict, cellSpatialIdx = self._buildGrid(
            zipData, constraintScaleIdx, context, multiStepFeedback
        )
        if not cellFeatDict:
            raise QgsProcessingException(
                self.tr(
                    "No grid cells could be built from the provided data. "
                    "Check that the zip files contain valid shapefiles."
                )
            )

        # Step 3: Associate each zip with the grid cell whose extent it belongs to
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Associating grid cells with zip files..."))
        cellToZipData = self._associateCellsWithZips(
            zipData, cellFeatDict, cellSpatialIdx, multiStepFeedback
        )

        # Step 4: Find adjacent cell pairs via touches()
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr("Finding adjacent cell pairs..."))
        adjacentPairs = self._findAdjacentPairs(cellFeatDict, cellSpatialIdx)
        multiStepFeedback.pushInfo(
            self.tr("Found {0} adjacent cell pair(s).").format(len(adjacentPairs))
        )

        # Step 5: Edge matching
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Performing edge matching..."))
        self._performEdgeMatching(
            adjacentPairs,
            cellFeatDict,
            cellToZipData,
            searchRadius,
            attributeBlacklist,
            fields,
            pointFlagSink,
            lineFlagSink,
            multiStepFeedback,
        )

        return {
            self.POINT_FLAGS: pointFlagSinkId,
            self.LINE_FLAGS: lineFlagSinkId,
        }

    # -------------------------------------------------------------------------
    # Step helpers
    # -------------------------------------------------------------------------

    def _loadZipFiles(self, zipFolderPath, feedback):
        """
        Scan folder for .zip files, extract them, and load all contained
        shapefiles grouped by geometry type and layer name.

        Returns:
            dict: {
                zip_path_str: {
                    'points':   {layer_name: QgsVectorLayer, ...},
                    'lines':    {layer_name: QgsVectorLayer, ...},
                    'polygons': {layer_name: QgsVectorLayer, ...},
                },
                ...
            }
        """
        zipFiles = sorted(Path(zipFolderPath).glob("*.zip"))
        if not zipFiles:
            return {}

        zipData = {}
        nZips = len(zipFiles)
        stepSize = 100.0 / nZips

        for i, zipPath in enumerate(zipFiles):
            if feedback.isCanceled():
                break
            feedback.pushInfo(self.tr("  Extracting {0}...").format(zipPath.name))

            tempDir = tempfile.mkdtemp()
            try:
                with zipfile.ZipFile(str(zipPath), "r") as zf:
                    zf.extractall(tempDir)
            except Exception as e:
                raise QgsProcessingException(
                    self.tr("Failed to extract '{0}': {1}").format(zipPath.name, e)
                )

            layersByType = {"points": {}, "lines": {}, "polygons": {}}
            for shpPath in Path(tempDir).rglob("*.shp"):
                layerName = shpPath.stem
                lyr = QgsVectorLayer(str(shpPath), layerName, "ogr")
                if not lyr.isValid():
                    feedback.pushWarning(
                        self.tr("  Could not load '{0}'. Skipping.").format(shpPath.name)
                    )
                    continue

                geomType = lyr.geometryType()
                if geomType == QgsWkbTypes.GeometryType.PointGeometry:
                    layersByType["points"][layerName] = lyr
                elif geomType == QgsWkbTypes.GeometryType.LineGeometry:
                    layersByType["lines"][layerName] = lyr
                elif geomType == QgsWkbTypes.GeometryType.PolygonGeometry:
                    layersByType["polygons"][layerName] = lyr

            zipData[str(zipPath)] = layersByType
            feedback.setProgress(int((i + 1) * stepSize))

        return zipData

    def _validateSchemas(self, zipData, ignoreFieldLengths=False, feedback=None):
        """
        Validates that all same-named shapefiles across all zip files have
        identical field schemas (same field names, types, and lengths).

        Hard errors (always raise QgsProcessingException):
          - Fields added or removed across zip files
          - Fields whose QVariant type changed

        Soft warnings (length-only differences):
          - If ignoreFieldLengths is False: raises QgsProcessingException
          - If ignoreFieldLengths is True:  emits a warning via feedback and
            continues processing
        """
        # {layer_name: {field_name: (field_type, field_length)}}
        schemaRegistry = {}
        schemaSource = {}  # {layer_name: zip_path_str (the reference zip)}

        for zipPath, layersByType in zipData.items():
            for layers in layersByType.values():
                for layerName, lyr in layers.items():
                    currentSchema = {
                        f.name(): (f.type(), f.length()) for f in lyr.fields()
                    }

                    if layerName not in schemaRegistry:
                        schemaRegistry[layerName] = currentSchema
                        schemaSource[layerName] = zipPath
                        continue

                    refSchema = schemaRegistry[layerName]
                    if currentSchema == refSchema:
                        continue

                    added = sorted(set(currentSchema.keys()) - set(refSchema.keys()))
                    removed = sorted(set(refSchema.keys()) - set(currentSchema.keys()))

                    commonFields = currentSchema.keys() & refSchema.keys()
                    typeChanged = sorted(
                        f
                        for f in commonFields
                        if currentSchema[f][0] != refSchema[f][0]
                    )
                    lengthOnly = sorted(
                        f
                        for f in commonFields
                        if currentSchema[f][0] == refSchema[f][0]
                        and currentSchema[f][1] != refSchema[f][1]
                    )

                    # Hard errors: structural mismatches
                    hardDiffs = []
                    if added:
                        hardDiffs.append(f"Added fields: {added}")
                    if removed:
                        hardDiffs.append(f"Removed fields: {removed}")
                    if typeChanged:
                        hardDiffs.append(f"Changed field types: {typeChanged}")

                    if hardDiffs:
                        raise QgsProcessingException(
                            self.tr(
                                f"Schema mismatch for layer '{layerName}':\n"
                                f"  Reference file  : '{Path(schemaSource[layerName]).name}'\n"
                                f"  Conflicting file: '{Path(zipPath).name}'\n"
                                f"  Differences     : {'; '.join(hardDiffs)}\n"
                                f"All shapefiles with the same name must have identical "
                                f"field schemas before edge matching can proceed."
                            )
                        )

                    # Soft warnings: length-only mismatches
                    if lengthOnly:
                        lengthDetails = ", ".join(
                            f"{f} "
                            f"(ref={refSchema[f][1]}, "
                            f"current={currentSchema[f][1]})"
                            for f in lengthOnly
                        )
                        msg = self.tr(
                            f"Field length mismatch for layer '{layerName}':\n"
                            f"  Reference file  : '{Path(schemaSource[layerName]).name}'\n"
                            f"  Conflicting file: '{Path(zipPath).name}'\n"
                            f"  Fields with different lengths: {lengthDetails}"
                        )
                        if ignoreFieldLengths:
                            if feedback is not None:
                                feedback.pushWarning(msg)
                        else:
                            raise QgsProcessingException(msg)

    def _getRefCrs(self, zipData):
        """Return the CRS of the first valid layer found across all zips."""
        for layersByType in zipData.values():
            for layers in layersByType.values():
                for lyr in layers.values():
                    return lyr.crs()
        return None

    def _buildGrid(self, zipData, constraintScaleIdx, context, feedback):
        """
        Generates a systematic grid over the combined extent of all loaded data,
        then filters to only cells that contain at least one real feature:
          - Points  : checked with within(cellGeom)
          - Lines   : checked with intersection having length > 0
          - Polygons: checked with intersection having area > 0

        Returns:
            tuple: (cellFeatDict {cell_id: QgsFeature}, QgsSpatialIndex)
        """
        # Compute combined extent and pick a reference CRS
        combinedExtent = QgsRectangle()
        crs = None
        for layersByType in zipData.values():
            for layers in layersByType.values():
                for lyr in layers.values():
                    if crs is None:
                        crs = lyr.crs()
                    if not lyr.extent().isEmpty():
                        combinedExtent.combineExtentWith(lyr.extent())

        if combinedExtent.isEmpty():
            raise QgsProcessingException(
                self.tr("Could not determine a valid extent from the loaded data.")
            )

        # Create a temporary polygon layer from the combined extent so the
        # systematic grid algorithm has a valid input layer
        crsAuthId = crs.authid() if crs else "EPSG:4674"
        extentLyr = QgsVectorLayer(f"Polygon?crs={crsAuthId}", "extent_poly", "memory")
        pr = extentLyr.dataProvider()
        extentFeat = QgsFeature()
        extentFeat.setGeometry(QgsGeometry.fromRect(combinedExtent))
        pr.addFeature(extentFeat)
        extentLyr.updateExtents()

        feedback.pushInfo(self.tr("  Generating systematic grid..."))
        gridOutput = runProcessing(
            "dsgtools:createframeswithconstraintalgorithm",
            {
                "INPUT": extentLyr,
                "STOP_SCALE": constraintScaleIdx,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=False,
        )
        gridLyr = gridOutput["OUTPUT"]

        # Build spatial indices per geometry type for the cell-filtering step
        feedback.pushInfo(self.tr("  Indexing features for cell filtering..."))
        pointGeoms, lineGeoms, polyGeoms = {}, {}, {}
        pointIdx = QgsSpatialIndex()
        lineIdx = QgsSpatialIndex()
        polyIdx = QgsSpatialIndex()
        featId = 0

        for layersByType in zipData.values():
            for geomTypeKey, layers in layersByType.items():
                for lyr in layers.values():
                    for feat in lyr.getFeatures():
                        geom = feat.geometry()
                        if geom is None or geom.isEmpty():
                            continue
                        tmpFeat = QgsFeature()
                        tmpFeat.setId(featId)
                        tmpFeat.setGeometry(geom)
                        if geomTypeKey == "points":
                            pointIdx.addFeature(tmpFeat)
                            pointGeoms[featId] = geom
                        elif geomTypeKey == "lines":
                            lineIdx.addFeature(tmpFeat)
                            lineGeoms[featId] = geom
                        elif geomTypeKey == "polygons":
                            polyIdx.addFeature(tmpFeat)
                            polyGeoms[featId] = geom
                        featId += 1

        # Filter: keep only cells with at least one real feature inside
        feedback.pushInfo(self.tr("  Filtering grid cells that contain real data..."))
        cellFeatDict = {}
        cellSpatialIdx = QgsSpatialIndex()

        for cell in gridLyr.getFeatures():
            if feedback.isCanceled():
                break
            cellGeom = cell.geometry()
            if self._cellHasData(
                cellGeom,
                cellGeom.boundingBox(),
                pointIdx,
                pointGeoms,
                lineIdx,
                lineGeoms,
                polyIdx,
                polyGeoms,
            ):
                cellFeatDict[cell.id()] = cell
                cellSpatialIdx.addFeature(cell)

        feedback.pushInfo(self.tr("  {0} grid cell(s) contain data.").format(len(cellFeatDict)))
        return cellFeatDict, cellSpatialIdx

    def _cellHasData(
        self,
        cellGeom,
        cellBbox,
        pointIdx,
        pointGeoms,
        lineIdx,
        lineGeoms,
        polyIdx,
        polyGeoms,
    ):
        """
        Returns True if the cell geometry contains at least one real feature:
          - Points  : the point falls strictly within the cell (within())
          - Lines   : the geometric intersection with the cell has length > 0
                      (rules out lines that only touch the cell boundary)
          - Polygons: the geometric intersection with the cell has area > 0
        """
        for pid in pointIdx.intersects(cellBbox):
            if pointGeoms[pid].within(cellGeom):
                return True

        for lid in lineIdx.intersects(cellBbox):
            inter = lineGeoms[lid].intersection(cellGeom)
            if inter is not None and not inter.isEmpty() and inter.length() > 0:
                return True

        for fid in polyIdx.intersects(cellBbox):
            inter = polyGeoms[fid].intersection(cellGeom)
            if inter is not None and not inter.isEmpty() and inter.area() > 0:
                return True

        return False

    def _associateCellsWithZips(self, zipData, cellFeatDict, cellSpatialIdx, feedback):
        """
        Associates each zip file with the single grid cell that best contains
        its data, determined by finding the cell that contains the centroid of
        the zip's combined data extent.

        Returns:
            dict: {cell_id: layersByType_dict}
        """
        cellToZipData = {}

        for zipPath, layersByType in zipData.items():
            if feedback.isCanceled():
                break

            zipExtent = QgsRectangle()
            for layers in layersByType.values():
                for lyr in layers.values():
                    if not lyr.extent().isEmpty():
                        zipExtent.combineExtentWith(lyr.extent())

            if zipExtent.isEmpty():
                feedback.pushWarning(
                    self.tr("  No extent found for '{0}'. Skipping.").format(Path(zipPath).name)
                )
                continue

            centroid = QgsGeometry.fromPointXY(QgsPointXY(zipExtent.center()))

            foundCell = False
            for candidateId in cellSpatialIdx.intersects(zipExtent):
                cellGeom = cellFeatDict[candidateId].geometry()
                if centroid.within(cellGeom):
                    if candidateId in cellToZipData:
                        feedback.pushWarning(
                            self.tr(
                                f"  Cell {candidateId} already has an associated zip. "
                                f"'{Path(zipPath).name}' will overwrite it."
                            )
                        )
                    cellToZipData[candidateId] = layersByType
                    foundCell = True
                    break

            if not foundCell:
                feedback.pushWarning(
                    self.tr(
                        f"  Could not find a grid cell for '{Path(zipPath).name}'. "
                        f"This zip will be skipped."
                    )
                )

        return cellToZipData

    def _findAdjacentPairs(self, cellFeatDict, cellSpatialIdx):
        """
        Find all unique pairs of cells that share a border, using bounding-box
        pre-filter followed by a precise touches() check.

        Returns:
            set: of (cell_id_a, cell_id_b) tuples, always with cell_id_a < cell_id_b
        """
        pairs = set()
        for cellId, cell in cellFeatDict.items():
            cellGeom = cell.geometry()
            for candidateId in cellSpatialIdx.intersects(cellGeom.boundingBox()):
                if candidateId >= cellId:
                    continue
                if candidateId not in cellFeatDict:
                    continue
                if cellGeom.touches(cellFeatDict[candidateId].geometry()):
                    pairs.add((candidateId, cellId))
        return pairs

    def _getCellBoundaryAsLine(self, geom):
        """
        Returns all rings of a polygon geometry collected as line geometries.
        Used to extract the full cell boundary for external border computation.
        """
        flatType = QgsWkbTypes.flatType(geom.wkbType())
        rings = []
        if flatType == QgsWkbTypes.Polygon:
            rings = geom.asPolygon()
        elif flatType == QgsWkbTypes.MultiPolygon:
            for poly in geom.asMultiPolygon():
                rings.extend(poly)
        parts = [QgsGeometry.fromPolylineXY(ring) for ring in rings if ring]
        if not parts:
            return QgsGeometry()
        if len(parts) == 1:
            return parts[0]
        return QgsGeometry.collectGeometry(parts)

    def _computeExternalBorderBuffers(self, cellFeatDict, searchRadius):
        """
        For each data cell computes the part of its boundary that is NOT shared
        with any other data cell (the "external border"), then returns a buffer
        of that external border with radius ``searchRadius``.

        This is used to suppress spurious "missing connection" flags for
        features whose endpoints sit at the dataset boundary (where no adjacent
        cell with data exists on the other side).

        Returns:
            dict: {cell_id: QgsGeometry}  — empty geometry when the whole
                  boundary is shared (cell is completely surrounded by data).
        """
        localIdx = QgsSpatialIndex()
        for cell in cellFeatDict.values():
            localIdx.addFeature(cell)

        result = {}
        for cellId, cell in cellFeatDict.items():
            cellGeom = cell.geometry()

            sharedParts = []
            for neighborId in localIdx.intersects(cellGeom.boundingBox()):
                if neighborId == cellId:
                    continue
                neighborGeom = cellFeatDict[neighborId].geometry()
                if cellGeom.touches(neighborGeom):
                    shared = cellGeom.intersection(neighborGeom)
                    if shared and not shared.isEmpty():
                        sharedParts.append(shared)

            cellBoundaryLine = self._getCellBoundaryAsLine(cellGeom)

            if not sharedParts:
                externalBoundary = cellBoundaryLine
            else:
                sharedUnion = (
                    QgsGeometry.collectGeometry(sharedParts)
                    if len(sharedParts) > 1
                    else sharedParts[0]
                )
                # Tiny buffer on the shared union to absorb floating-point gaps
                externalBoundary = cellBoundaryLine.difference(
                    sharedUnion.buffer(1e-9, 3)
                )

            if (
                externalBoundary
                and not externalBoundary.isEmpty()
                and externalBoundary.length() > 0
            ):
                result[cellId] = externalBoundary.buffer(searchRadius, 5)
            else:
                result[cellId] = QgsGeometry()

        return result

    def _performEdgeMatching(
        self,
        adjacentPairs,
        cellFeatDict,
        cellToZipData,
        searchRadius,
        attributeBlacklist,
        fields,
        pointFlagSink,
        lineFlagSink,
        feedback,
    ):
        """
        For each adjacent cell pair that has data on both sides, computes the
        shared edge, buffers it by searchRadius, and runs edge matching for
        lines, points, and polygons — in both directions (A→B and B→A) so
        that missing features on either side are always flagged.

        Features whose endpoints lie near the dataset's external border (i.e.
        the portion of a cell boundary not shared with any other data cell) are
        excluded from "missing connection" flags, because there is no adjacent
        cell to connect to on that side.
        """
        nPairs = len(adjacentPairs)
        if nPairs == 0:
            feedback.pushInfo(
                self.tr("No adjacent pairs with data on both sides found.")
            )
            return

        # Precompute external border buffers once for all data cells
        feedback.pushInfo(self.tr("  Precomputing external border buffers..."))
        cellExternalBorders = self._computeExternalBorderBuffers(
            cellFeatDict, searchRadius
        )

        stepSize = 100.0 / nPairs

        for i, (cellIdA, cellIdB) in enumerate(adjacentPairs):
            if feedback.isCanceled():
                break
            feedback.setProgress(int(i * stepSize))

            if cellIdA not in cellToZipData or cellIdB not in cellToZipData:
                continue

            dataA = cellToZipData[cellIdA]
            dataB = cellToZipData[cellIdB]

            sharedEdge = (
                cellFeatDict[cellIdA]
                .geometry()
                .intersection(cellFeatDict[cellIdB].geometry())
            )
            if sharedEdge is None or sharedEdge.isEmpty():
                continue

            bufferZone = sharedEdge.buffer(searchRadius, 5)
            if bufferZone is None or bufferZone.isEmpty():
                continue

            extBufA = cellExternalBorders.get(cellIdA, QgsGeometry())
            extBufB = cellExternalBorders.get(cellIdB, QgsGeometry())

            feedback.pushInfo(self.tr("  Matching cells {0} and {1}...").format(cellIdA, cellIdB))

            for geomTypeKey in ("lines", "points", "polygons"):
                layersA = dataA.get(geomTypeKey, {})
                layersB = dataB.get(geomTypeKey, {})
                commonNames = set(layersA.keys()) & set(layersB.keys())

                for layerName in sorted(commonNames):
                    lyrA = layersA[layerName]
                    lyrB = layersB[layerName]

                    # Attributes to compare: all fields minus the blacklist
                    comparableAttrs = {
                        f.name() for f in lyrA.fields()
                    } - attributeBlacklist

                    if geomTypeKey == "lines":
                        self._matchLines(
                            lyrA,
                            lyrB,
                            bufferZone,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            layerName,
                            extBufA,
                        )
                        self._matchLines(
                            lyrB,
                            lyrA,
                            bufferZone,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            layerName,
                            extBufB,
                        )
                    elif geomTypeKey == "points":
                        self._matchPoints(
                            lyrA,
                            lyrB,
                            bufferZone,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            layerName,
                            extBufA,
                        )
                        self._matchPoints(
                            lyrB,
                            lyrA,
                            bufferZone,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            layerName,
                            extBufB,
                        )
                    elif geomTypeKey == "polygons":
                        self._matchPolygons(
                            lyrA,
                            lyrB,
                            bufferZone,
                            sharedEdge,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            lineFlagSink,
                            layerName,
                            extBufA,
                        )
                        self._matchPolygons(
                            lyrB,
                            lyrA,
                            bufferZone,
                            sharedEdge,
                            searchRadius,
                            comparableAttrs,
                            fields,
                            pointFlagSink,
                            lineFlagSink,
                            layerName,
                            extBufB,
                        )

    # -------------------------------------------------------------------------
    # Edge-matching methods
    # -------------------------------------------------------------------------

    def _getLineEndpointsInBuffer(self, lyr, bufferZone):
        """
        For every line feature in `lyr` that intersects `bufferZone`, extracts
        the start and end vertices and keeps those that fall within the buffer.

        Returns:
            list of (QgsGeometry point, QgsFeature parent_line)
        """
        endpoints = []
        bbox = bufferZone.boundingBox()

        for feat in lyr.getFeatures(QgsFeatureRequest().setFilterRect(bbox)):
            geom = feat.geometry()
            if geom is None or geom.isEmpty():
                continue
            if not geom.intersects(bufferZone):
                continue
            vtxList = list(geom.vertices())
            if not vtxList:
                continue
            for vtx in (vtxList[0], vtxList[-1]):
                pt = QgsGeometry.fromPointXY(QgsPointXY(vtx.x(), vtx.y()))
                if pt.within(bufferZone):
                    endpoints.append((pt, feat))

        return endpoints

    def _matchLines(
        self,
        lyrA,
        lyrB,
        bufferZone,
        searchRadius,
        comparableAttrs,
        fields,
        sink,
        layerName,
        externalBorderBuffer=None,
    ):
        """
        For each line endpoint from lyrA that lies within the buffer zone,
        searches for a matching endpoint in lyrB within searchRadius.

        Flags:
          - "missing neighbor"  : no lyrB endpoint found within searchRadius
          - "continuity error"  : matching endpoint found but attributes differ

        ``externalBorderBuffer`` (optional): buffered external boundary of the
        source cell.  Endpoints within this zone are skipped for "missing
        neighbor" flags because no adjacent data cell exists on that side.
        """
        endpointsA = self._getLineEndpointsInBuffer(lyrA, bufferZone)
        endpointsB = self._getLineEndpointsInBuffer(lyrB, bufferZone)

        if not endpointsA:
            return

        hasExtBuf = externalBorderBuffer and not externalBorderBuffer.isEmpty()

        # Spatial index for lyrB endpoints
        bIdxMap = {}
        bSpatialIdx = QgsSpatialIndex()
        for bIdx, (pt, feat) in enumerate(endpointsB):
            tmpFeat = QgsFeature()
            tmpFeat.setId(bIdx)
            tmpFeat.setGeometry(pt)
            bSpatialIdx.addFeature(tmpFeat)
            bIdxMap[bIdx] = (pt, feat)

        for ptA, featA in endpointsA:
            searchBbox = ptA.buffer(searchRadius, 5).boundingBox()
            candidates = bSpatialIdx.intersects(searchBbox)

            if not candidates:
                # Suppress flag if the endpoint is near the dataset's external
                # border (no adjacent data cell on that side).
                if hasExtBuf and ptA.within(externalBorderBuffer):
                    continue
                self._addFlag(
                    ptA,
                    self.tr(
                        f"[{layerName}] Line endpoint without connection at boundary."
                    ),
                    fields,
                    sink,
                )
                continue

            # Pick the closest candidate within searchRadius
            bestId = None
            bestDist = float("inf")
            for cId in candidates:
                dist = ptA.distance(bIdxMap[cId][0])
                if dist <= searchRadius and dist < bestDist:
                    bestDist = dist
                    bestId = cId

            if bestId is None:
                if hasExtBuf and ptA.within(externalBorderBuffer):
                    continue
                self._addFlag(
                    ptA,
                    self.tr(
                        f"[{layerName}] Line endpoint without connection at boundary."
                    ),
                    fields,
                    sink,
                )
                continue

            _, featB = bIdxMap[bestId]
            diffAttrs = sorted(
                attr for attr in comparableAttrs if featA[attr] != featB[attr]
            )
            if diffAttrs:
                self._addFlag(
                    ptA,
                    self.tr(
                        f"[{layerName}] Line continuity error. "
                        f"Differing attributes: {', '.join(diffAttrs)}."
                    ),
                    fields,
                    sink,
                )

    def _matchPoints(
        self,
        lyrA,
        lyrB,
        bufferZone,
        searchRadius,
        comparableAttrs,
        fields,
        sink,
        layerName,
        externalBorderBuffer=None,
    ):
        """
        For each point feature from lyrA that lies within the buffer zone,
        searches for a matching point in lyrB within searchRadius.

        Flags:
          - "missing neighbor"  : no lyrB point found within searchRadius
          - "continuity error"  : matching point found but attributes differ

        ``externalBorderBuffer`` (optional): suppresses "missing neighbor" flags
        for points that sit on the dataset's external border.
        """
        bbox = bufferZone.boundingBox()

        pointsA = [
            feat
            for feat in lyrA.getFeatures(QgsFeatureRequest().setFilterRect(bbox))
            if feat.geometry() and feat.geometry().within(bufferZone)
        ]
        pointsB = [
            feat
            for feat in lyrB.getFeatures(QgsFeatureRequest().setFilterRect(bbox))
            if feat.geometry() and feat.geometry().within(bufferZone)
        ]

        if not pointsA:
            return

        hasExtBuf = externalBorderBuffer and not externalBorderBuffer.isEmpty()

        # Spatial index for lyrB points
        bIdxMap = {}
        bSpatialIdx = QgsSpatialIndex()
        for bIdx, feat in enumerate(pointsB):
            tmpFeat = QgsFeature()
            tmpFeat.setId(bIdx)
            tmpFeat.setGeometry(feat.geometry())
            bSpatialIdx.addFeature(tmpFeat)
            bIdxMap[bIdx] = feat

        for featA in pointsA:
            ptA = featA.geometry()
            searchBbox = ptA.buffer(searchRadius, 5).boundingBox()
            candidates = bSpatialIdx.intersects(searchBbox)

            if not candidates:
                if hasExtBuf and ptA.within(externalBorderBuffer):
                    continue
                self._addFlag(
                    ptA,
                    self.tr("[{0}] Point without neighbor at boundary.").format(layerName),
                    fields,
                    sink,
                )
                continue

            bestId = None
            bestDist = float("inf")
            for cId in candidates:
                dist = ptA.distance(bIdxMap[cId].geometry())
                if dist <= searchRadius and dist < bestDist:
                    bestDist = dist
                    bestId = cId

            if bestId is None:
                if hasExtBuf and ptA.within(externalBorderBuffer):
                    continue
                self._addFlag(
                    ptA,
                    self.tr("[{0}] Point without neighbor at boundary.").format(layerName),
                    fields,
                    sink,
                )
                continue

            featB = bIdxMap[bestId]
            diffAttrs = sorted(
                attr for attr in comparableAttrs if featA[attr] != featB[attr]
            )
            if diffAttrs:
                self._addFlag(
                    ptA,
                    self.tr(
                        f"[{layerName}] Point continuity error. "
                        f"Differing attributes: {', '.join(diffAttrs)}."
                    ),
                    fields,
                    sink,
                )

    def _matchPolygons(
        self,
        lyrA,
        lyrB,
        bufferZone,
        sharedEdge,
        searchRadius,
        comparableAttrs,
        fields,
        pointSink,
        lineSink,
        layerName,
        externalBorderBuffer=None,
    ):
        """
        For each polygon in lyrA that intersects the buffer zone:

        1. Boundary-segment matching (LINE flags):
           Extracts the part of the polygon boundary that lies within a TIGHT
           buffer around the sharedEdge (clippedEdgeZone). This captures only
           the clipped straight edge of the polygon at the cell boundary, and
           deliberately excludes natural boundary segments that merely happen
           to fall inside the wider bufferZone.
           - No match found       → LINE flag on segA  ("missing continuation")
           - Match with attr diff → LINE flag on segA  ("continuity error")

        2. Vertex checking (POINT flags):
           For every polygon vertex of lyrA that intersects the sharedEdge,
           checks whether any lyrB boundary segment is within searchRadius.
           - No nearby B boundary → POINT flag on the vertex
           - Suppressed if the vertex is within ``externalBorderBuffer``
             (i.e. no adjacent data cell exists on that side of the dataset).

        ``externalBorderBuffer`` (optional): suppresses "missing connection"
        POINT flags for vertices that sit on the dataset's external border.
        """
        bbox = bufferZone.boundingBox()

        polysA = [
            feat
            for feat in lyrA.getFeatures(QgsFeatureRequest().setFilterRect(bbox))
            if feat.geometry() and feat.geometry().intersects(bufferZone)
        ]
        polysB = [
            feat
            for feat in lyrB.getFeatures(QgsFeatureRequest().setFilterRect(bbox))
            if feat.geometry() and feat.geometry().intersects(bufferZone)
        ]

        if not polysA:
            return

        hasExtBuf = externalBorderBuffer and not externalBorderBuffer.isEmpty()

        # Tight buffer: only captures polygon boundary segments that actually
        # lie on/along the shared cell edge (the clipped portion), not natural
        # boundary segments that happen to be inside the wider bufferZone.
        clippedEdgeZone = sharedEdge.buffer(searchRadius * 0.1, 5)

        # Build a spatial index over the clipped boundary segments of lyrB polygons.
        bSegIdxMap = {}
        bSegSpatialIdx = QgsSpatialIndex()
        for bIdx, feat in enumerate(polysB):
            segB = self._polygonBoundaryInBuffer(feat.geometry(), clippedEdgeZone)
            if segB is None or segB.isEmpty() or segB.length() <= 0:
                continue
            tmpFeat = QgsFeature()
            tmpFeat.setId(bIdx)
            tmpFeat.setGeometry(segB)
            bSegSpatialIdx.addFeature(tmpFeat)
            bSegIdxMap[bIdx] = (segB, feat)

        for featA in polysA:
            geomA = featA.geometry()

            # --- 1. Boundary-segment matching (LINE flags) ---
            segA = self._polygonBoundaryInBuffer(geomA, clippedEdgeZone)
            if segA is not None and not segA.isEmpty() and segA.length() > 0:
                segABuff = segA.buffer(searchRadius, 5)
                candidates = bSegSpatialIdx.intersects(segABuff.boundingBox())
                matched = [
                    bSegIdxMap[cId]
                    for cId in candidates
                    if bSegIdxMap[cId][0].intersects(segABuff)
                ]

                if not matched:
                    self._addFlag(
                        segA,
                        self.tr(
                            f"[{layerName}] Missing polygon continuation at boundary."
                        ),
                        fields,
                        lineSink,
                    )
                else:
                    for _, featB in matched:
                        diffAttrs = sorted(
                            attr
                            for attr in comparableAttrs
                            if featA[attr] != featB[attr]
                        )
                        if diffAttrs:
                            self._addFlag(
                                segA,
                                self.tr(
                                    f"[{layerName}] Polygon continuity error. "
                                    f"Differing attributes: {', '.join(diffAttrs)}."
                                ),
                                fields,
                                lineSink,
                            )

            # --- 2. Vertex checking (POINT flags) ---
            # Only vertices that intersect the sharedEdge line itself are
            # checked. These are the polygon corners that sit exactly on the
            # cell boundary (produced by the clip operation). Natural boundary
            # vertices that are merely close to the boundary are excluded.
            for vtx in geomA.vertices():
                pt = QgsGeometry.fromPointXY(QgsPointXY(vtx.x(), vtx.y()))
                if not pt.intersects(sharedEdge):
                    continue
                ptSearchBbox = pt.buffer(searchRadius, 5).boundingBox()
                hasBNeighbor = any(
                    bSegIdxMap[cId][0].distance(pt) <= searchRadius
                    for cId in bSegSpatialIdx.intersects(ptSearchBbox)
                )
                if not hasBNeighbor:
                    # Suppress if the vertex is on the dataset's external border
                    if hasExtBuf and pt.within(externalBorderBuffer):
                        continue
                    self._addFlag(
                        pt,
                        self.tr(
                            f"[{layerName}] Polygon vertex without boundary "
                            f"connection at boundary."
                        ),
                        fields,
                        pointSink,
                    )

    def _polygonBoundaryInBuffer(self, geom, bufferZone):
        """
        Returns the parts of a polygon's boundary (all rings) that fall within
        bufferZone, as a line geometry.

        QgsGeometry does not expose boundary() in Python, so this method
        converts each ring to a QgsGeometry line and intersects with bufferZone.
        Works for both Polygon and MultiPolygon geometries.

        Returns an empty QgsGeometry if no ring intersects the buffer zone
        with length > 0.
        """
        flatType = QgsWkbTypes.flatType(geom.wkbType())
        rings = []
        if flatType == QgsWkbTypes.Polygon:
            rings = geom.asPolygon()
        elif flatType == QgsWkbTypes.MultiPolygon:
            for poly in geom.asMultiPolygon():
                rings.extend(poly)

        parts = []
        for ring in rings:
            ringLine = QgsGeometry.fromPolylineXY(ring)
            inter = ringLine.intersection(bufferZone)
            if inter and not inter.isEmpty() and inter.length() > 0:
                parts.append(inter)

        if not parts:
            return QgsGeometry()
        if len(parts) == 1:
            return parts[0]
        return QgsGeometry.collectGeometry(parts)

    def _addFlag(self, geom, reason, fields, sink):
        """Creates and adds a flag feature to the output sink."""
        newFeat = QgsFeature(fields)
        newFeat.setGeometry(geom)
        newFeat["reason"] = reason
        sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    # -------------------------------------------------------------------------
    # Standard QgsProcessingAlgorithm overrides
    # -------------------------------------------------------------------------

    def name(self):
        return "verifybdgexedgematching"

    def displayName(self):
        return self.tr("Verify BDGEx Edge Matching")

    def group(self):
        return self.tr("QA Tools: Dataset Processes")

    def groupId(self):
        return "DSGTools - QA Tools: Dataset Processes"

    def tr(self, string):
        return QCoreApplication.translate("VerifyBDGExEdgeMatchingAlgorithm", string)

    def createInstance(self):
        return VerifyBDGExEdgeMatchingAlgorithm()
