# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-03-06
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


from typing import Any, Dict
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
    QgsProcessingParameterDistance,
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
)


class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV3(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
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
                    "Minimun area to process. If feature's area is smaller than this value, "
                    "the feature will not be split, but only reclassified to the nearest neighbour. "
                    "Area in meters."
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
        multiStepFeedback = QgsProcessingMultiStepFeedback(15, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running initial polygonize"))
        polygonLayer = self.algRunner.runGdalPolygonize(
            inputRaster=inputRaster,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        selectedPolygonLayer = self.algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=f"""$area < {min_area} and "DN" != {nodata} """,
            context=context,
            feedback=multiStepFeedback,
        )
        nFeats = selectedPolygonLayer.featureCount()
        if nFeats == 0:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runRasterClipByExtent(
                inputRaster=inputRaster,
                extent=inputRaster.extent(),
                nodata=nodata,
                context=context,
                outputLyr=outputRaster,
                feedback=multiStepFeedback,
            )
            return {self.OUTPUT: outputRaster}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            selectedPolygonLayer, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        explodedBboxLine = self.computeBboxLine(parameters, context, multiStepFeedback)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        polygonsNotOnEdge = self.algRunner.runExtractByLocation(
            inputLyr=selectedPolygonLayer,
            intersectLyr=explodedBboxLine,
            context=context,
            predicate=[AlgRunner.Disjoint],
            feedback=multiStepFeedback,
        )
        if polygonsNotOnEdge.featureCount() == 0:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runRasterClipByExtent(
                inputRaster=inputRaster,
                extent=inputRaster.extent(),
                nodata=nodata,
                context=context,
                outputLyr=outputRaster,
                feedback=multiStepFeedback,
            )
            return {self.OUTPUT: outputRaster}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            polygonsNotOnEdge, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        polygonsWithCount = self.algRunner.runJoinByLocationSummary(
            inputLyr=polygonsNotOnEdge,
            joinLyr=polygonsNotOnEdge,
            joinFields=[],
            predicateList=[AlgRunner.Intersects],
            summaries=[0],
            feedback=multiStepFeedback,
            context=context,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Reading input numpy array"))

        ds, npRaster = rasterHandler.readAsNumpy(inputRaster, dtype=np.int16)
        transform = rasterHandler.getCoordinateTransform(ds)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Masking for each polygon"))
        request = QgsFeatureRequest()
        request.setFilterExpression(""" "DN_count" = 1 """)
        (polygons_sink, polygons_dest_id) = self.parameterAsSink(
            parameters,
            self.RECLASSIFIED_POLYGONS,
            context,
            polygonsNotOnEdge.fields(),
            QgsWkbTypes.Polygon,
            inputRaster.crs(),
        )
        if polygons_sink is not None:
            polygons_sink.addFeatures(polygonsNotOnEdge.getFeatures())
        out = self.reclassifyGroupsOfPixelsInsidePolygons(
            KDTree,
            multiStepFeedback,
            polygonsWithCount,
            npRaster,
            transform,
            request,
            nodata,
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Writing output"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        nIterations = 0
        multiStepFeedback.pushInfo(self.tr("Evaluating remaining polygons:"))
        polygonLayer = self.algRunner.runGdalPolygonize(
            inputRaster=outputRaster,
            context=context,
            feedback=multiStepFeedback,
        )
        originalGraph = None
        while True:
            currentStep = 11
            multiStepFeedback.setCurrentStep(currentStep)
            ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int16)
            transform = rasterHandler.getCoordinateTransform(ds)
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=outputRaster,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            polygonLayer = self.algRunner.runCreateFieldWithExpression(
                inputLyr=polygonLayer,
                expression="$id",
                fieldName="featid",
                fieldType=1,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                polygonLayer,
                context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            originalGraph = (
                self.buildGraph(nx, polygonLayer, context, feedback=multiStepFeedback)
                if originalGraph is None
                else originalGraph
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            selectedPolygonLayer = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"""$area < {min_area} and "DN" != {nodata} """,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            polygonsNotOnEdge = self.algRunner.runExtractByLocation(
                inputLyr=selectedPolygonLayer,
                intersectLyr=explodedBboxLine,
                context=context,
                predicate=[AlgRunner.Disjoint],
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            remainingFeatCount = polygonsNotOnEdge.featureCount()
            if remainingFeatCount == 0 or nIterations > 10:
                break
            if nIterations > 0:
                multiStepFeedback.pushInfo(
                    self.tr(f"Evaluating remaining polygons: Loop {nIterations+1}")
                )
            G = self.buildGraph(nx, polygonsNotOnEdge, context, multiStepFeedback)
            connected_components = list(nx.connected_components(G))

            multiStepFeedback.pushInfo(
                self.tr(f"Evaluating {remainingFeatCount} groups of remaining pixels")
            )
            nGroups = len(connected_components)
            innerFeedback = QgsProcessingMultiStepFeedback(nGroups, multiStepFeedback)
            crs = inputRaster.crs()

            for currentComponent, component in enumerate(connected_components):
                innerFeedback.setCurrentStep(currentComponent)
                if innerFeedback.isCanceled():
                    break
                request = QgsFeatureRequest()
                # clause = QgsFeatureRequest.OrderByClause("$area", ascending=True)
                # orderby = QgsFeatureRequest.OrderBy([clause])
                # request.setOrderBy(orderby)
                request.setFilterExpression(
                    f""" "featid" in ({', '.join(map(str, component))})"""
                )
                polygonDict = {
                    f["featid"]: f for f in polygonsNotOnEdge.getFeatures(request)
                }
                # polygonList = list(polygonsNotOnEdge.getFeatures(request))
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
                    transform.a,  # a: scale x
                    transform.b,  # b: shear x
                    transform.c + window["x_start"] * transform.a,  # c: translate x
                    transform.d,  # d: shear y
                    transform.e,  # e: scale y
                    transform.f + window["y_start"] * transform.e,  # f: translate y
                )
                while polygonDict != dict():
                    if innerFeedback.isCanceled():
                        break
                    sortedNodes = sorted(
                        polygonDict.keys(),
                        key=lambda x: G.nodes[x]["area"],
                        reverse=False,
                    )
                    currentNode = sortedNodes[0]
                    feat = polygonDict.pop(currentNode)
                    # for feat in polygonsNotOnEdge.getFeatures(request):
                    if G.nodes[currentNode]["area"] > min_area:
                        continue
                    self.processPixelGroup(
                        KDTree, currentView, window_transform, feat, nodata
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
            rasterHandler.writeOutputRaster(
                outputRaster, npRaster.T, ds, outputType=gdal.GDT_Int16
            )
            ds = None
        return (
            {self.OUTPUT: outputRaster}
            if polygons_sink is not None
            else {
                self.OUTPUT: outputRaster,
                self.RECLASSIFIED_POLYGONS: polygons_dest_id,
            }
        )

    def buildGraph(self, nx, polygonLyr, context, feedback):
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
            # For geographic coordinates, we need a sample pixel to calculate its area
            # Get center of the region for a better representation
            center_x = (window["x_start"] + window["x_end"]) / 2
            center_y = (window["y_start"] + window["y_end"]) / 2
            terrain_coords = transform * (center_x, center_y)

            # Create a sample pixel polygon at the center
            sample_pixel = QgsGeometry.fromRect(
                QgsRectangle(
                    terrain_coords[0],
                    terrain_coords[1],
                    terrain_coords[0] + pixel_width,
                    terrain_coords[1] + pixel_height,
                )
            )

            # Calculate area in square meters using QgsDistanceArea
            pixel_area = d.measureArea(sample_pixel)
        else:
            # For projected coordinates, convert to square meters based on the CRS units
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

    def reclassifyGroupsOfPixelsInsidePolygons(
        self,
        KDTree,
        multiStepFeedback,
        polygonsWithCount,
        npRaster,
        transform,
        request,
        nodata,
    ):
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
            self.processPixelGroup(KDTree, npRaster, transform, polygonFeat, nodata)
            multiStepFeedback.setProgress(current * stepSize)
        return True

    def processPixelGroup(
        self,
        KDTree,
        npRaster,
        transform,
        polygonFeat,
        nodata,
    ):
        geom = polygonFeat.geometry()

        currentView, mask = rasterHandler.getNumpyViewAndMaskFromPolygon(
            npRaster=npRaster,
            transform=transform,
            geom=geom,
            pixelBuffer=2,
            returnWindow=False,
        )
        v = polygonFeat["DN"]
        originalCopy = np.array(currentView)
        maskedCurrentView = ma.masked_array(currentView, np.isnan(mask), np.int16)
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == v, np.int16
        )
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == nodata, dtype=np.int16
        )
        x, y = np.mgrid[0 : maskedCurrentView.shape[0], 0 : maskedCurrentView.shape[1]]
        xygood = np.array((x[~maskedCurrentView.mask], y[~maskedCurrentView.mask])).T
        xybad = np.array((x[maskedCurrentView.mask], y[maskedCurrentView.mask])).T
        if len(xybad) <= 0 or len(xygood) <= 0:
            return
        maskedCurrentView[maskedCurrentView.mask] = maskedCurrentView[
            ~maskedCurrentView.mask
        ][KDTree(xygood).query(xybad)[1]]
        currentView = maskedCurrentView.data
        currentView[~np.isnan(mask)] = originalCopy[~np.isnan(mask)]
        currentView[originalCopy == nodata] = originalCopy[originalCopy == nodata]
        # currentView[~np.isnan(mask.T)] = originalCopy[~np.isnan(mask.T)]
        # outputMask = maskedCurrentView + mask.T
        # outputMask[np.isnan(mask.T)] = originalCopy[np.isnan(mask.T)]
        # currentView = outputMask

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifygroupsofpixelstonearestneighboralgorithmv3"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Groups of Pixels to Nearest Neighbor Algorithm V3")

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
            "ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV3", string
        )

    def createInstance(self):
        return ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV3()
