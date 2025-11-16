# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-11-16
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


from typing import Any, Dict, List, Tuple
import json
import numpy as np
import numpy.ma as ma
from osgeo import gdal

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import rasterHandler

from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.affine import Affine
from qgis.core import (
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingParameterNumber,
    QgsProject,
    QgsDistanceArea,
    QgsGeometry,
    QgsRectangle,
    QgsUnitTypes,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsProcessingParameterString,
)


class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV4(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
    GENERALIZATION_RULES = "GENERALIZATION_RULES"
    OUTPUT = "OUTPUT"
    RECLASSIFIED_POLYGONS = "RECLASSIFIED_POLYGONS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr("Input Single Band Image"),
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_AREA,
                self.tr(
                    "Default minimum area (meters²). "
                    "Polygons smaller than this will be dissolved. "
                    "Can be overridden per class using Generalization Rules."
                ),
                defaultValue=15625,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NODATA_VALUE,
                self.tr("NODATA pixel value"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=-9999,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GENERALIZATION_RULES,
                self.tr(
                    "Generalization Rules (JSON, optional). "
                    "Defines class-specific behavior for dissolution. "
                    'Format: {"class_restrictions": {source_DN: [allowed_targets], ...}, '
                    '"size_thresholds": {DN: threshold_m2, ...}}. '
                    "Note: Use integer keys (not strings). "
                    'Example: {"class_restrictions": {5: [6], 10: [11]}, '
                    '"size_thresholds": {20: 2500}}. '
                    "Restrictions are automatically bidirectional. "
                    "Classes with smaller thresholds are processed first. "
                    "If empty, algorithm behaves like V3."
                ),
                optional=True,
                defaultValue="",
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT, self.tr("Output Raster")
            )
        )

        reclassSink = QgsProcessingParameterFeatureSink(
            self.RECLASSIFIED_POLYGONS,
            self.tr("Reclassified groups of pixels (Optional)"),
            optional=True,
            createByDefault=False,
        )
        self.addParameter(reclassSink)

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python scipy library. Please install this library and try again."
                )
            )
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires networkx. Please install this library and try again."
                )
            )

        self.algRunner = AlgRunner()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        nodata = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        rulesJson = self.parameterAsString(
            parameters, self.GENERALIZATION_RULES, context
        )

        # Parse generalization rules
        classRestrictions, sizeThresholds = self.parseGeneralizationRules(
            rulesJson, min_area, feedback
        )

        # Group thresholds into processing phases
        thresholdPhases = self.groupThresholds(sizeThresholds)

        multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(thresholdPhases) * 15, feedback
        )

        if len(thresholdPhases) > 1:
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Processing in {len(thresholdPhases)} phases based on size thresholds"
                )
            )
            for idx, (threshold, dnList) in enumerate(thresholdPhases):
                if dnList == ["default"]:
                    multiStepFeedback.pushInfo(
                        self.tr(
                            f"  Phase {idx + 1}: All other classes with threshold {threshold} m²"
                        )
                    )
                else:
                    multiStepFeedback.pushInfo(
                        self.tr(
                            f"  Phase {idx + 1}: Classes {dnList} with threshold {threshold} m²"
                        )
                    )

        # Compute bbox line (used across all phases)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        explodedBboxLine = self.computeBboxLine(parameters, context, multiStepFeedback)

        # Initialize polygon sink if requested
        (polygons_sink, polygons_dest_id) = self.parameterAsSink(
            parameters,
            self.RECLASSIFIED_POLYGONS,
            context,
            None,  # Will set fields later
            QgsWkbTypes.Polygon,
            inputRaster.crs(),
        )

        # Track all specifically-thresholded DNs for default group filtering
        self.allSpecificDNs = set()

        # Read initial raster
        ds, npRaster = rasterHandler.readAsNumpy(inputRaster, dtype=np.int16)
        transform = rasterHandler.getCoordinateTransform(ds)

        # Process each phase
        for phaseIdx, (threshold, dnList) in enumerate(thresholdPhases):
            currentStep = phaseIdx * 15

            if len(thresholdPhases) > 1:
                multiStepFeedback.pushInfo(
                    self.tr(
                        f"\n{'='*60}\nPhase {phaseIdx + 1}/{len(thresholdPhases)}: "
                        f"Processing {'classes ' + str(dnList) if dnList != ['default'] else 'remaining classes'} "
                        f"with threshold {threshold} m²\n{'='*60}"
                    )
                )

            npRaster = self.processPhase(
                threshold=threshold,
                dnList=dnList,
                phaseIdx=phaseIdx,
                npRaster=npRaster,
                ds=ds,
                transform=transform,
                inputRaster=inputRaster,
                outputRaster=outputRaster,
                nodata=nodata,
                classRestrictions=classRestrictions,
                explodedBboxLine=explodedBboxLine,
                polygons_sink=polygons_sink,
                parameters=parameters,
                context=context,
                feedback=multiStepFeedback,
                KDTree=KDTree,
                nx=nx,
            )

        # Final write
        multiStepFeedback.pushInfo(self.tr("\nWriting final output raster"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        return (
            {self.OUTPUT: outputRaster}
            if polygons_sink is None
            else {
                self.OUTPUT: outputRaster,
                self.RECLASSIFIED_POLYGONS: polygons_dest_id,
            }
        )

    def parseGeneralizationRules(
        self, rulesJson: str, defaultMinArea: float, feedback: QgsFeedback
    ) -> Tuple[Dict, Dict]:
        """
        Parse generalization rules JSON with integer keys.

        Returns:
            (classRestrictions, sizeThresholds)
            classRestrictions: {source_DN: [allowed_target_DNs]}
            sizeThresholds: {DN: threshold, 'default': defaultMinArea}
        """
        if not rulesJson or not rulesJson.strip():
            # No rules - backward compatible behavior
            return None, {"default": defaultMinArea}

        try:
            rules = json.loads(rulesJson)
        except json.JSONDecodeError as e:
            raise QgsProcessingException(
                self.tr(f"Invalid JSON in Generalization Rules: {str(e)}")
            )

        # Parse class restrictions
        classRestrictions = None
        if "class_restrictions" in rules:
            rawRestrictions = rules["class_restrictions"]
            # Ensure keys are integers (JSON may parse them as strings)
            intRestrictions = {}
            for key, value in rawRestrictions.items():
                try:
                    int_key = int(key)
                    int_values = (
                        [int(v) for v in value]
                        if isinstance(value, list)
                        else [int(value)]
                    )
                    intRestrictions[int_key] = int_values
                except (ValueError, TypeError) as e:
                    feedback.pushWarning(
                        self.tr(
                            f"Skipping invalid class restriction: {key} -> {value}: {str(e)}"
                        )
                    )

            # Make bidirectional
            classRestrictions = self.makeBidirectional(intRestrictions)
            feedback.pushInfo(
                self.tr(
                    f"Loaded class restrictions (bidirectional): {classRestrictions}"
                )
            )

        # Parse size thresholds
        sizeThresholds = {"default": defaultMinArea}
        if "size_thresholds" in rules:
            rawThresholds = rules["size_thresholds"]
            for key, value in rawThresholds.items():
                try:
                    dn = int(key)
                    sizeThresholds[dn] = float(value)
                except (ValueError, TypeError):
                    if key == "default":
                        sizeThresholds["default"] = float(value)
                    else:
                        feedback.pushWarning(
                            self.tr(
                                f"Skipping invalid size threshold: {key} -> {value}"
                            )
                        )

            feedback.pushInfo(self.tr(f"Loaded size thresholds: {sizeThresholds}"))

        return classRestrictions, sizeThresholds

    def makeBidirectional(self, restrictions: Dict) -> Dict:
        """
        Ensure restrictions are bidirectional.

        Input: {5: [6], 10: [11]}
        Output: {5: [6], 6: [5], 10: [11], 11: [10]}
        """
        result = {}

        # First pass: ensure all keys and values are integers
        for source, targets in restrictions.items():
            source_int = int(source)
            targets_list = (
                [int(t) for t in targets]
                if isinstance(targets, list)
                else [int(targets)]
            )
            result[source_int] = targets_list

        # Second pass: add reverse mappings
        reverse_mappings = {}
        for source, targets in result.items():
            for target in targets:
                if target not in reverse_mappings:
                    reverse_mappings[target] = []
                if source not in reverse_mappings[target]:
                    reverse_mappings[target].append(source)

        # Merge reverse mappings
        for target, sources in reverse_mappings.items():
            if target in result:
                # Add any missing sources
                for source in sources:
                    if source not in result[target]:
                        result[target].append(source)
            else:
                result[target] = sources

        return result

    def groupThresholds(self, sizeThresholds: Dict) -> List[Tuple[float, List]]:
        """
        Group DN classes by threshold, sorted by threshold ascending.

        Input: {20: 2500, 21: 2500, 30: 5000, 'default': 15625}
        Output: [(2500, [20, 21]), (5000, [30]), (15625, ['default'])]
        """
        from collections import defaultdict

        groups = defaultdict(list)
        for dn, threshold in sizeThresholds.items():
            groups[threshold].append(dn)

        # Sort by threshold (smallest first)
        return sorted(groups.items(), key=lambda x: x[0])

    def buildFilterExpression(self, threshold: float, dnList: List, nodata: int) -> str:
        """
        Build filter expression for a specific phase.

        threshold: 2500
        dnList: [20, 21]
        nodata: -9999

        Returns: '$area < 2500 AND "DN" IN (20, 21) AND "DN" != -9999'
        """
        if dnList == ["default"]:
            # Default group - exclude all specifically-thresholded DNs
            specificDNs = [dn for dn in self.allSpecificDNs if dn != nodata]
            if specificDNs:
                return (
                    f'$area < {threshold} AND "DN" NOT IN ({",".join(map(str, specificDNs))}) '
                    f'AND "DN" != {nodata}'
                )
            else:
                return f'$area < {threshold} AND "DN" != {nodata}'
        else:
            # Specific DN group
            dnString = ",".join(map(str, dnList))
            return f'$area < {threshold} AND "DN" IN ({dnString}) AND "DN" != {nodata}'

    def processPhase(
        self,
        threshold: float,
        dnList: List,
        phaseIdx: int,
        npRaster: np.ndarray,
        ds,
        transform: Affine,
        inputRaster,
        outputRaster: str,
        nodata: int,
        classRestrictions: Dict,
        explodedBboxLine,
        polygons_sink,
        parameters: Dict,
        context: QgsProcessingContext,
        feedback: QgsProcessingMultiStepFeedback,
        KDTree,
        nx,
    ) -> np.ndarray:
        """
        Process a single phase with a specific threshold and DN list.
        """
        # Track specific DNs for default group filtering
        if dnList != ["default"]:
            self.allSpecificDNs.update(dnList)

        baseStep = phaseIdx * 15
        currentStep = baseStep + 1
        feedback.setCurrentStep(currentStep)

        # Initial polygonize
        feedback.pushInfo(self.tr("Running initial polygonize for this phase"))
        polygonLayer = self.algRunner.runGdalPolygonize(
            inputRaster=inputRaster if phaseIdx == 0 else outputRaster,
            context=context,
            feedback=feedback,
        )

        currentStep += 1
        feedback.setCurrentStep(currentStep)

        # Filter by threshold and DN list
        filterExpression = self.buildFilterExpression(threshold, dnList, nodata)
        selectedPolygonLayer = self.algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=filterExpression,
            context=context,
            feedback=feedback,
        )

        nFeats = selectedPolygonLayer.featureCount()
        feedback.pushInfo(self.tr(f"Found {nFeats} polygons matching criteria"))

        if nFeats == 0:
            feedback.pushInfo(self.tr("No polygons to process in this phase"))
            return npRaster

        currentStep += 1
        feedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            selectedPolygonLayer, context, feedback, is_child_algorithm=True
        )

        currentStep += 1
        feedback.setCurrentStep(currentStep)

        # Extract polygons not on edge
        polygonsNotOnEdge = self.algRunner.runExtractByLocation(
            inputLyr=selectedPolygonLayer,
            intersectLyr=explodedBboxLine,
            context=context,
            predicate=[AlgRunner.Disjoint],
            feedback=feedback,
        )

        if polygonsNotOnEdge.featureCount() == 0:
            feedback.pushInfo(self.tr("All polygons are on edges - skipping phase"))
            return npRaster

        currentStep += 1
        feedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            polygonsNotOnEdge, context, feedback, is_child_algorithm=True
        )

        currentStep += 1
        feedback.setCurrentStep(currentStep)

        # Join by location to count neighbors
        polygonsWithCount = self.algRunner.runJoinByLocationSummary(
            inputLyr=polygonsNotOnEdge,
            joinLyr=polygonsNotOnEdge,
            joinFields=[],
            predicateList=[AlgRunner.Intersects],
            summaries=[0],
            feedback=feedback,
            context=context,
        )

        currentStep += 1
        feedback.setCurrentStep(currentStep)

        # Process isolated polygons (DN_count = 1)
        feedback.pushInfo(self.tr("Processing isolated polygons"))
        request = QgsFeatureRequest()
        request.setFilterExpression('"DN_count" = 1')

        # Set up polygon sink fields if first use
        if polygons_sink is not None and phaseIdx == 0:
            polygons_sink.addFeatures(polygonsNotOnEdge.getFeatures())

        self.reclassifyGroupsOfPixelsInsidePolygons(
            KDTree,
            feedback,
            polygonsWithCount,
            npRaster,
            transform,
            request,
            nodata,
            classRestrictions,
        )

        currentStep += 1
        feedback.setCurrentStep(currentStep)

        # Write output after isolated polygons
        feedback.pushInfo(self.tr("Writing intermediate output"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        # Iterative processing for connected components
        nIterations = 0
        maxIterations = 10
        originalGraph = None

        feedback.pushInfo(self.tr("Processing connected components"))

        while nIterations < maxIterations:
            currentStep = baseStep + 11
            feedback.setCurrentStep(currentStep)

            # Re-read raster state
            ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int16)
            transform = rasterHandler.getCoordinateTransform(ds)

            # Re-polygonize
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=outputRaster,
                context=context,
                feedback=feedback,
            )

            currentStep += 1
            feedback.setCurrentStep(currentStep)

            # Add feature ID
            polygonLayer = self.algRunner.runCreateFieldWithExpression(
                inputLyr=polygonLayer,
                expression="$id",
                fieldName="featid",
                fieldType=1,
                context=context,
                feedback=feedback,
            )

            currentStep += 1
            feedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                polygonLayer,
                context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            currentStep += 1
            feedback.setCurrentStep(currentStep)

            # Build graph (only once)
            if originalGraph is None:
                originalGraph = self.buildGraph(
                    nx, polygonLayer, context, feedback=feedback
                )

            currentStep += 1
            feedback.setCurrentStep(currentStep)

            # Filter by threshold and DN list again
            filterExpression = self.buildFilterExpression(threshold, dnList, nodata)
            selectedPolygonLayer = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=filterExpression,
                context=context,
                feedback=feedback,
            )

            currentStep += 1
            feedback.setCurrentStep(currentStep)

            # Extract polygons not on edge
            polygonsNotOnEdge = self.algRunner.runExtractByLocation(
                inputLyr=selectedPolygonLayer,
                intersectLyr=explodedBboxLine,
                context=context,
                predicate=[AlgRunner.Disjoint],
                feedback=feedback,
            )

            remainingFeatCount = polygonsNotOnEdge.featureCount()

            if remainingFeatCount == 0:
                feedback.pushInfo(
                    self.tr(
                        f"No more polygons to process after {nIterations} iterations"
                    )
                )
                break

            if nIterations > 0:
                feedback.pushInfo(
                    self.tr(
                        f"Iteration {nIterations + 1}: Processing {remainingFeatCount} polygons"
                    )
                )

            # Build graph for current iteration
            G = self.buildGraph(nx, polygonsNotOnEdge, context, feedback)
            connected_components = list(nx.connected_components(G))

            nGroups = len(connected_components)
            feedback.pushInfo(self.tr(f"Processing {nGroups} connected components"))

            innerFeedback = QgsProcessingMultiStepFeedback(nGroups, feedback)
            crs = inputRaster.crs()

            for currentComponent, component in enumerate(connected_components):
                innerFeedback.setCurrentStep(currentComponent)
                if innerFeedback.isCanceled():
                    break

                request = QgsFeatureRequest()
                request.setFilterExpression(
                    f'"featid" in ({", ".join(map(str, component))})'
                )

                polygonDict = {
                    f["featid"]: f for f in polygonsNotOnEdge.getFeatures(request)
                }

                combined_geometry = QgsGeometry.unaryUnion(
                    [f.geometry() for f in polygonDict.values()]
                )

                currentView, _, window = rasterHandler.getNumpyViewAndMaskFromPolygon(
                    npRaster=npRaster,
                    transform=transform,
                    geom=combined_geometry,
                    pixelBuffer=2,
                    returnWindow=True,
                )

                window_transform = Affine(
                    transform.a,
                    transform.b,
                    transform.c + window["x_start"] * transform.a,
                    transform.d,
                    transform.e,
                    transform.f + window["y_start"] * transform.e,
                )

                while polygonDict:
                    if innerFeedback.isCanceled():
                        break

                    sortedNodes = sorted(
                        polygonDict.keys(),
                        key=lambda x: G.nodes[x]["area"],
                        reverse=False,
                    )
                    currentNode = sortedNodes[0]
                    feat = polygonDict.pop(currentNode)

                    if G.nodes[currentNode]["area"] > threshold:
                        continue

                    self.processPixelGroup(
                        KDTree,
                        currentView,
                        window_transform,
                        feat,
                        nodata,
                        classRestrictions,
                    )

                    dn_dict = self.buildDnDict(
                        currentView, feat.geometry(), window_transform, crs
                    )
                    self.updateGraph(feat["featid"], G, originalGraph, dn_dict)

                    npRaster[
                        window["x_start"] : window["x_end"],
                        window["y_start"] : window["y_end"],
                    ] = currentView

            nIterations += 1

            # Write after each iteration
            rasterHandler.writeOutputRaster(
                outputRaster, npRaster.T, ds, outputType=gdal.GDT_Int16
            )
            ds = None

        feedback.pushInfo(self.tr(f"Phase completed after {nIterations} iterations"))

        return npRaster

    def reclassifyGroupsOfPixelsInsidePolygons(
        self,
        KDTree,
        multiStepFeedback,
        polygonsWithCount,
        npRaster,
        transform,
        request,
        nodata,
        classRestrictions,
    ):
        """Process isolated polygons sorted by size."""
        polygonList = sorted(
            polygonsWithCount.getFeatures(request),
            key=lambda x: x.geometry().area(),
            reverse=False,
        )

        if len(polygonList) == 0:
            return False

        stepSize = 100 / len(polygonList)
        for current, polygonFeat in enumerate(polygonList):
            if multiStepFeedback.isCanceled():
                break
            self.processPixelGroup(
                KDTree, npRaster, transform, polygonFeat, nodata, classRestrictions
            )
            multiStepFeedback.setProgress(current * stepSize)

        return True

    def processPixelGroup(
        self,
        KDTree,
        npRaster,
        transform,
        polygonFeat,
        nodata,
        classRestrictions=None,
    ):
        """
        Process a single pixel group with optional class restrictions.

        If restrictions exist and valid neighbors are found, only dissolve to allowed classes.
        If restrictions exist but no valid neighbors, fall back to unrestricted dissolution.
        """
        geom = polygonFeat.geometry()
        v = polygonFeat["DN"]

        # Get view and mask
        currentView, mask = rasterHandler.getNumpyViewAndMaskFromPolygon(
            npRaster=npRaster,
            transform=transform,
            geom=geom,
            pixelBuffer=2,
            returnWindow=False,
        )

        originalCopy = np.array(currentView)

        # Standard masking (always applied)
        maskedCurrentView = ma.masked_array(currentView, np.isnan(mask), np.int16)
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == v, np.int16
        )
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == nodata, dtype=np.int16
        )

        # Try to apply restrictions if they exist
        restriction_applied = False
        allowed_targets = None

        if classRestrictions and v in classRestrictions:
            allowed_targets = classRestrictions[v]

            # Create test mask with restrictions
            restriction_mask = ~np.isin(currentView, allowed_targets)
            testMaskedView = ma.masked_array(
                maskedCurrentView, restriction_mask, dtype=np.int16
            )

            # Check if any valid neighbors exist after restriction
            x_test, y_test = np.mgrid[
                0 : testMaskedView.shape[0], 0 : testMaskedView.shape[1]
            ]
            xygood_test = np.array(
                (x_test[~testMaskedView.mask], y_test[~testMaskedView.mask])
            ).T

            if len(xygood_test) > 0:
                # Valid neighbors exist - apply restriction
                maskedCurrentView = testMaskedView
                restriction_applied = True
            # else: No valid neighbors - continue with unrestricted maskedCurrentView

        # KDTree nearest neighbor assignment
        x, y = np.mgrid[0 : maskedCurrentView.shape[0], 0 : maskedCurrentView.shape[1]]
        xygood = np.array((x[~maskedCurrentView.mask], y[~maskedCurrentView.mask])).T
        xybad = np.array((x[maskedCurrentView.mask], y[maskedCurrentView.mask])).T

        if len(xybad) <= 0 or len(xygood) <= 0:
            return

        maskedCurrentView[maskedCurrentView.mask] = maskedCurrentView[
            ~maskedCurrentView.mask
        ][KDTree(xygood).query(xybad)[1]]

        # Restore view
        currentView = maskedCurrentView.data

        # CRITICAL: Restore restricted neighbor pixels (only if restriction was applied)
        if restriction_applied:
            pixels_to_restore = (
                np.isnan(mask)
                & (originalCopy != v)  # inside the buffered window
                & (originalCopy != nodata)  # not the polygon's own DN
                & ~np.isin(  # not nodata
                    originalCopy, allowed_targets
                )  # not an allowed target
            )
            currentView[pixels_to_restore] = originalCopy[pixels_to_restore]

        # Restore outside boundary and nodata (always)
        currentView[~np.isnan(mask)] = originalCopy[~np.isnan(mask)]
        currentView[originalCopy == nodata] = originalCopy[originalCopy == nodata]

    def buildGraph(self, nx, polygonLyr, context, feedback):
        """Build graph of polygon relationships."""
        graph = nx.Graph()
        d = QgsDistanceArea()
        d.setEllipsoid(QgsProject.instance().ellipsoid())

        # Add all polygons as nodes
        for feat in polygonLyr.getFeatures():
            geom = feat.geometry()
            area = d.measureArea(geom)
            graph.add_node(feat["featid"], dn=feat["DN"], area=area)

        multiStepFeedback = QgsProcessingMultiStepFeedback(1, feedback)
        multiStepFeedback.setCurrentStep(0)

        # Find intersecting pairs
        intersectingPairs = self.algRunner.runJoinAttributesByLocation(
            inputLyr=polygonLyr,
            joinLyr=polygonLyr,
            predicateList=[AlgRunner.Intersects],
            prefix="i_",
            discardNonMatching=True,
            context=context,
            feedback=feedback,
        )

        for feat in intersectingPairs.getFeatures():
            if feat["featid"] == feat["i_featid"]:
                continue
            graph.add_edge(feat["featid"], feat["i_featid"])

        return graph

    def updateGraph(self, featid, G, originalGraph, dn_dict):
        """Update graph after polygon dissolution."""
        neighbors = set(G.neighbors(featid))
        if len(neighbors) == 0:
            return

        originalLargeNeighbors = set(originalGraph.neighbors(featid)) - neighbors
        large_dn_dict = {
            i: originalGraph.nodes[i]["dn"] for i in originalLargeNeighbors
        }

        for neighbor in neighbors:
            neighbor_dn = G.nodes[neighbor]["dn"]
            if neighbor_dn not in dn_dict:
                continue
            G.nodes[neighbor]["area"] += dn_dict[neighbor_dn] + large_dn_dict.get(
                neighbor_dn, 0
            )

        G.remove_node(featid)

    def buildDnDict(
        self, npRaster: np.ndarray, polygon: QgsGeometry, transform, crs
    ) -> Dict[int, float]:
        """Build dictionary of DN values and their areas within polygon."""
        _, window = rasterHandler.getNumpyViewFromPolygon(
            npRaster, transform, polygon, pixelBuffer=0, returnWindow=True
        )
        npView, mask = rasterHandler.getNumpyViewAndMaskFromPolygon(
            npRaster,
            transform,
            polygon,
            pixelBuffer=0,
        )
        d = QgsDistanceArea()
        d.setEllipsoid(QgsProject.instance().ellipsoid())

        pixel_width = abs(transform.a)
        pixel_height = abs(transform.e)

        if crs.isGeographic():
            # For geographic coordinates, calculate area of sample pixel
            center_x = (window["x_start"] + window["x_end"]) / 2
            center_y = (window["y_start"] + window["y_end"]) / 2
            terrain_coords = transform * (center_x, center_y)

            sample_pixel = QgsGeometry.fromRect(
                QgsRectangle(
                    terrain_coords[0],
                    terrain_coords[1],
                    terrain_coords[0] + pixel_width,
                    terrain_coords[1] + pixel_height,
                )
            )

            pixel_area = d.measureArea(sample_pixel)
        else:
            # For projected coordinates
            units = crs.mapUnits()
            conversion_factor = QgsUnitTypes.fromUnitToUnitFactor(
                units, QgsUnitTypes.SquareMeters
            )
            pixel_area = pixel_width * pixel_height * conversion_factor

        # Count occurrences of each value
        unique_values, counts = np.unique(npView[np.isnan(mask)], return_counts=True)

        # Calculate areas in square meters
        return {
            int(value): count * pixel_area
            for value, count in zip(unique_values, counts)
        }

    def computeBboxLine(
        self,
        parameters: Dict[str, Any],
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        """Compute exploded bounding box line for edge detection."""
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        bbox = self.algRunner.runPolygonFromLayerExtent(
            inputLayer=parameters[self.INPUT],
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        bboxLine = self.algRunner.runPolygonsToLines(
            inputLyr=bbox,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        explodedBboxLine = self.algRunner.runExplodeLines(
            inputLyr=bboxLine,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        self.algRunner.runCreateSpatialIndex(
            explodedBboxLine, context, multiStepFeedback, is_child_algorithm=True
        )

        return explodedBboxLine

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifygroupsofpixelstonearestneighboralgorithmv4"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Groups of Pixels to Nearest Neighbor Algorithm V4")

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

    def tr(self, string):
        return QCoreApplication.translate(
            "ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV4", string
        )

    def createInstance(self):
        return ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV4()
