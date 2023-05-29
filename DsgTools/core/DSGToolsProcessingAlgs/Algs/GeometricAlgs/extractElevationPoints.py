# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-19
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from collections import defaultdict
import math
from typing import Dict, List, Tuple, Union
from uuid import uuid4
import numpy as np
import json
from itertools import chain, islice
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import geometryHandler, rasterHandler
from DsgTools.core.GeometricTools.affine import Affine
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
import processing
from osgeo import gdal, ogr
from PyQt5.QtCore import QCoreApplication, QVariant, QByteArray
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingUtils,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterFileDestination,
    QgsVectorFileWriter,
    QgsProcessingParameterEnum,
    QgsSpatialIndex,
    QgsCoordinateReferenceSystem,
    QgsRasterLayer,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingParameterField,
    QgsVectorLayerUtils,
)


class ExtractElevationPoints(QgsProcessingAlgorithm):

    INPUT_DEM = "INPUT_DEM"
    CONTOUR_LINES = "CONTOUR_LINES"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    CONTOUR_INTERVAL = "CONTOUR_INTERVAL"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    SCALE = "SCALE"
    WATER_BODIES = "WATER_BODIES"
    AREA_WITHOUT_INFORMATION_POLYGONS = "AREA_WITHOUT_INFORMATION_POLYGONS"
    NATURAL_POINT_FEATURES = "NATURAL_POINT_FEATURES"
    DRAINAGE_LINES_WITH_NAME = "DRAINAGE_LINES_WITH_NAME"
    DRAINAGE_LINES_WITHOUT_NAME = "DRAINAGE_LINES_WITHOUT_NAME"
    MAIN_ROADS = "MAIN_ROADS"
    OTHER_ROADS = "OTHER_ROADS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr("Input DEM"),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CONTOUR_LINES,
                self.tr("Contour Lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CONTOUR_ATTR,
                self.tr("Contour value field"),
                None,
                self.CONTOUR_LINES,
                QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL,
                self.tr("Contour interval"),
                minValue=0,
                defaultValue=10,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic bounds layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.scales = [
            "1:25.000",
            "1:50.000",
            "1:100.000",
            "1:250.000",
        ]

        self.distances = {
            0: 20e-3 * 25_000,
            1: 20e-3 * 50_000,
            2: 20e-3 * 100_000,
            3: 20e-3 * 250_000,
        }

        self.minContourLenghts = {
            0: 8e-3 * 25_000,
            1: 8e-3 * 50_000,
            2: 8e-3 * 100_000,
            3: 8e-3 * 250_000,
        }
        self.gridSpacingDict = {
            0: 5000,
            1: 10000,
            2: 20000,
            3: 40000,
        }
        self.contourBufferLengths = {
            0: 3.2e-3 * 25_000,
            1: 3.2e-3 * 50_000,
            2: 3.2e-3 * 100_000,
            3: 3.2e-3 * 250_000,
        }

        self.planeGridSpacingDict = {
            0: 20e-3 * 25_000,
            1: 20e-3 * 50_000,
            2: 20e-3 * 100_000,
            3: 20e-3 * 250_000,
        }

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE, self.tr("Scale"), options=self.scales, defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.WATER_BODIES,
                self.tr("Water Bodies"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AREA_WITHOUT_INFORMATION_POLYGONS,
                self.tr("Area without information layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.DRAINAGE_LINES_WITH_NAME,
                self.tr("Drainage lines with name"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.DRAINAGE_LINES_WITHOUT_NAME,
                self.tr("Drainage lines without name"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.MAIN_ROADS,
                self.tr("Main Roads"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.OTHER_ROADS,
                self.tr("Other Roads"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Output elevation points")
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        contourLyr = self.parameterAsSource(parameters, self.CONTOUR_LINES, context)
        heightFieldName = self.parameterAsFields(
            parameters, self.CONTOUR_ATTR, context
        )[0]
        contourHeightInterval = self.parameterAsDouble(
            parameters, self.CONTOUR_INTERVAL, context
        )
        geoBoundsSource = self.parameterAsSource(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        scale = self.parameterAsEnum(parameters, self.SCALE, context)
        areaWithoutInformationLyr = self.parameterAsVectorLayer(
            parameters, self.AREA_WITHOUT_INFORMATION_POLYGONS, context
        )
        waterBodiesLyr = self.parameterAsVectorLayer(
            parameters, self.WATER_BODIES, context
        )
        naturalPointFeaturesLyr = self.parameterAsVectorLayer(
            parameters, self.NATURAL_POINT_FEATURES, context
        )
        drainagesWithNameLyr = self.parameterAsVectorLayer(
            parameters, self.DRAINAGE_LINES_WITH_NAME, context
        )
        drainagesWithoutNameLyr = self.parameterAsVectorLayer(
            parameters, self.DRAINAGE_LINES_WITHOUT_NAME, context
        )
        mainRoadsLyr = self.parameterAsVectorLayer(parameters, self.MAIN_ROADS, context)
        otherRoadsLyr = self.parameterAsVectorLayer(
            parameters, self.OTHER_ROADS, context
        )
        self.bufferDist = self.distances[scale]
        self.minContourLength = self.minContourLenghts[scale]
        self.gridSpacing = self.gridSpacingDict[scale]
        self.planeGridSpacing = self.gridSpacingDict[scale]
        self.contourBufferLength = self.contourBufferLengths[scale]

        fields = QgsFields()
        fields.append(QgsField("cota", QVariant.Int))
        fields.append(QgsField("cota_mais_alta", QVariant.Bool))

        (self.sink, self.sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Point,
            inputRaster.crs(),
        )
        layerHandler = LayerHandler()
        nFeats = geoBoundsSource.featureCount()
        multiStepFeedback = QgsProcessingMultiStepFeedback(nFeats, feedback)
        for currentStep, feat in enumerate(geoBoundsSource.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr(f"Evaluating region {currentStep+1}/{nFeats}"))
            localBoundsLyr = layerHandler.createMemoryLayerWithFeature(
                geographicBoundaryLyr, feat, context
            )
            featList = self.computePoints(
                contourLyr=parameters[self.CONTOUR_LINES],
                heightFieldName=heightFieldName,
                contourHeightInterval=contourHeightInterval,
                inputRaster=inputRaster,
                geographicBoundsLyr=localBoundsLyr,
                areaWithoutInformationLyr=parameters[
                    self.AREA_WITHOUT_INFORMATION_POLYGONS
                ]
                if areaWithoutInformationLyr is not None
                else None,
                waterBodiesLyr=waterBodiesLyr,
                naturalPointFeaturesLyr=parameters[self.NATURAL_POINT_FEATURES]
                if naturalPointFeaturesLyr is not None
                else None,
                drainagesWithNameLyr=parameters[self.DRAINAGE_LINES_WITH_NAME]
                if drainagesWithNameLyr is not None
                else None,
                drainagesWithoutNameLyr=parameters[self.DRAINAGE_LINES_WITHOUT_NAME]
                if drainagesWithoutNameLyr is not None
                else None,
                mainRoadsLyr=parameters[self.MAIN_ROADS]
                if mainRoadsLyr is not None
                else None,
                otherRoadsLyr=parameters[self.OTHER_ROADS]
                if otherRoadsLyr is not None
                else None,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
            self.sink.addFeatures(featList, QgsFeatureSink.FastInsert)
        return {
            "OUTPUT": self.sink_id,
        }

    def computePoints(
        self,
        contourLyr,
        heightFieldName,
        contourHeightInterval,
        inputRaster,
        geographicBoundsLyr,
        areaWithoutInformationLyr,
        waterBodiesLyr,
        naturalPointFeaturesLyr,
        drainagesWithNameLyr,
        drainagesWithoutNameLyr,
        mainRoadsLyr,
        otherRoadsLyr,
        fields,
        context,
        feedback,
    ):
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        spatialRelationsHandler = SpatialRelationsHandler()
        nSteps = 16 + (
            naturalPointFeaturesLyr is not None
        )  # handle this count after alg is done
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Clipping raster"))
        frameCentroid = (
            [i for i in geographicBoundsLyr.getFeatures()][0].geometry().centroid()
        )
        originEpsg = QgsCoordinateReferenceSystem(
            geometryHandler.getSirgasAuthIdByPointLatLong(*frameCentroid.asPoint())
        )
        localGridSize = geometryHandler.convertDistance(
            self.gridSpacing,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        minusBufferedGeographicBoundsLyr = algRunner.runBuffer(
            inputLayer=geographicBoundsLyr,
            distance=-localGridSize / 64,
            endCapStyle=1,
            context=context,
        )
        clippedRaster = algRunner.runClipRasterLayer(
            inputRaster,
            mask=geographicBoundsLyr,
            context=context,
            feedback=feedback,
            noData=-9999,
            outputRaster=QgsProcessingUtils.generateTempFilename(
                f"clip_{str(uuid4().hex)}.tif"
            ),
        )
        clippedRasterLyr = QgsProcessingUtils.mapLayerFromString(clippedRaster, context)
        localBufferDistance = geometryHandler.convertDistance(
            self.bufferDist,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Reading raster with numpy..."))
        contourBufferLyr = algRunner.runBuffer(
            inputLayer=contourLyr,
            distance=geometryHandler.convertDistance(
                self.contourBufferLength,
                originEpsg=originEpsg,
                destinationEpsg=geographicBoundsLyr.crs(),
            ),
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        npRaster, transform = self.readAndMaskRaster(
            clippedRasterLyr,
            geographicBoundsLyr,
            areaWithoutInformationLyr,
            waterBodiesLyr,
            contourBufferLyr,
            context,
            algRunner,
            feedback=multiStepFeedback,
        )

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Getting max min feats and building exclusion polygons...")
            )
        minMaxFeats = self.getMinMaxFeatures(
            fields, npRaster, transform, distance=localBufferDistance
        )
        elevationPointsLayer = layerHandler.createMemoryLayerWithFeatures(
            featList=minMaxFeats,
            fields=fields,
            crs=clippedRasterLyr.crs(),
            wkbType=QgsWkbTypes.Point,
            context=context,
        )
        # compute number of points
        minNPoints, maxNPoints = self.getRangeOfNumberOfPoints(minMaxFeats)
        maxPointsPerGridUnit = maxNPoints // 9
        exclusionLyr = self.buildExclusionLyr(
            elevationPointsLayer,
            areaWithoutInformationLyr,
            waterBodiesLyr,
            localBufferDistance,
            context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Preparing contours..."))
        contourAreaDict, polygonLyr = self.prepareContours(
            contourLyr=contourLyr,
            geographicBoundsLyr=geographicBoundsLyr,
            heightFieldName=heightFieldName,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        # create grid
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        gridLyr, gridDict, gridLyrDict = self.buildGrid(
            geographicBoundsLyr, context, feedback=multiStepFeedback
        )

        # create points from first criteria
        if naturalPointFeaturesLyr is not None:
            if multiStepFeedback is not None:
                multiStepFeedback.setProgressText(
                    self.tr("Getting elevation points from natural points...")
                )
            elevationPointsFromNaturalPointFeatures = (
                self.getElevationPointsFromNaturalPoints(
                    npRaster=npRaster,
                    transform=transform,
                    naturalPointFeaturesLyr=naturalPointFeaturesLyr,
                    exclusionLyr=exclusionLyr,
                    polygonLyr=polygonLyr,
                    bufferDistance=localBufferDistance,
                    contourAreaDict=contourAreaDict,
                    contourHeightInterval=contourHeightInterval,
                    fields=fields,
                    gridLyr=gridLyr,
                    gridDict=gridDict,
                    gridLyrDict=gridLyrDict,
                    maxPointsPerGridUnit=maxPointsPerGridUnit,
                    context=context,
                    feedback=multiStepFeedback,
                )
            )

            self.updateExclusionLyr(
                exclusionLyr,
                elevationPointsFromNaturalPointFeatures,
                distance=localBufferDistance,
                context=context,
            )
            self.addPointsToMemoryLayer(
                elevationPointsLayer, elevationPointsFromNaturalPointFeatures, context
            )
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)

        if multiStepFeedback is not None:
            multiStepFeedback.setProgressText(
                self.tr("Getting elevation points from hilltops...")
            )

        # create points from hilltops
        elevationPointsFromHilltops = self.getElevationPointsFromHilltops(
            rasterLyr=clippedRaster,
            polygonLyr=polygonLyr,
            exclusionLyr=exclusionLyr,
            geographicBoundsLyr=geographicBoundsLyr,
            minusBuffergeographicBoundsLyr=minusBufferedGeographicBoundsLyr,
            bufferDistance=localBufferDistance,
            originEpsg=originEpsg,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromHilltops,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer, elevationPointsFromHilltops, context
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Getting elevation points from main road intersections...")
            )
        elevationPointsFromRoadIntersections = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=mainRoadsLyr,
                lineLyr2=mainRoadsLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromRoadIntersections,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer, elevationPointsFromRoadIntersections, context
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Getting elevation points from other road intersections...")
            )
        elevationPointsFromOtherRoadIntersections = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=otherRoadsLyr,
                lineLyr2=otherRoadsLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromOtherRoadIntersections,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer, elevationPointsFromOtherRoadIntersections, context
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of road and rivers with names outside polygons..."
                )
            )
        elevationPointsFromIntersectionsOfRiverWithNamesAndRoads = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithNameLyr,
                lineLyr2=mainRoadsLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiverWithNamesAndRoads,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiverWithNamesAndRoads,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of road and rivers without names..."
                )
            )

        elevationPointsFromIntersectionsOfRiversWithoutNamesAndRoads = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithoutNameLyr,
                lineLyr2=mainRoadsLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiversWithoutNamesAndRoads,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiversWithoutNamesAndRoads,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of rivers with names..."
                )
            )

        elevationPointsFromIntersectionsOfRiversWithNames = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithNameLyr,
                lineLyr2=drainagesWithNameLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiversWithNames,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiversWithNames,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of rivers with names..."
                )
            )

        elevationPointsFromIntersectionsOfRiversWithNames = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithNameLyr,
                lineLyr2=drainagesWithNameLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiversWithNames,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiversWithNames,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of rivers with and without names..."
                )
            )

        elevationPointsFromIntersectionsOfRiversWithAndWithoutNames = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithNameLyr,
                lineLyr2=drainagesWithoutNameLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiversWithAndWithoutNames,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiversWithAndWithoutNames,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr(
                    "Getting elevation points from intersections of rivers without names..."
                )
            )

        elevationPointsFromIntersectionsOfRiversWithoutNames = (
            self.getElevationPointsFromLineIntersections(
                lineLyr1=drainagesWithoutNameLyr,
                lineLyr2=drainagesWithoutNameLyr,
                geographicBoundsLyr=minusBufferedGeographicBoundsLyr,
                npRaster=npRaster,
                transform=transform,
                polygonLyr=polygonLyr,
                bufferDistance=localBufferDistance,
                exclusionLyr=exclusionLyr,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                gridLyr=gridLyr,
                gridDict=gridDict,
                maxPointsPerGridUnit=maxPointsPerGridUnit,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        self.updateExclusionLyr(
            exclusionLyr,
            elevationPointsFromIntersectionsOfRiversWithoutNames,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer,
            elevationPointsFromIntersectionsOfRiversWithoutNames,
            context,
        )
        if elevationPointsLayer.featureCount() > maxNPoints:
            return elevationPointsLayer.getFeatures()

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(
                self.tr("Getting elevation points from plane areas...")
            )

        planeAreasElevationPoints = self.getElevationPointsFromPlaneAreas(
            contourLyr=contourLyr,
            geographicBoundsLyr=geographicBoundsLyr,
            rasterLyr=clippedRasterLyr,
            exclusionLyr=exclusionLyr,
            polygonLyr=polygonLyr,
            originEpsg=originEpsg,
            bufferDistance=localBufferDistance,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )
        self.updateExclusionLyr(
            exclusionLyr,
            planeAreasElevationPoints,
            distance=localBufferDistance,
            context=context,
        )
        self.addPointsToMemoryLayer(
            elevationPointsLayer, planeAreasElevationPoints, context
        )
        return elevationPointsLayer.getFeatures()

    def readAndMaskRaster(
        self,
        clippedRasterLyr,
        geographicBoundsLyr,
        areaWithoutInformationLyr,
        waterBodiesLyr,
        contourBufferLyr,
        context,
        algRunner,
        feedback,
    ):
        nSteps = (
            3 + (areaWithoutInformationLyr is not None) + (waterBodiesLyr is not None)
        )
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        ds, npRaster = rasterHandler.readAsNumpy(clippedRasterLyr)
        transform = rasterHandler.getCoordinateTransform(ds)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        if (
            areaWithoutInformationLyr is not None
            and areaWithoutInformationLyr.featureCount() > 0
        ):
            npRaster = self.maskFeaturesFromLayerOnRaster(
                rasterLyr=clippedRasterLyr,
                geographicBoundsLyr=geographicBoundsLyr,
                maskLyr=areaWithoutInformationLyr,
                context=context,
                algRunner=algRunner,
                feedback=multiStepFeedback,
                npRaster=npRaster,
            )
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)

        if waterBodiesLyr is not None and waterBodiesLyr.featureCount() > 0:
            npRaster = self.maskFeaturesFromLayerOnRaster(
                rasterLyr=clippedRasterLyr,
                geographicBoundsLyr=geographicBoundsLyr,
                maskLyr=waterBodiesLyr,
                context=context,
                algRunner=algRunner,
                feedback=multiStepFeedback,
                npRaster=npRaster,
            )
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        npRaster = self.maskFeaturesFromLayerOnRaster(
            rasterLyr=clippedRasterLyr,
            geographicBoundsLyr=geographicBoundsLyr,
            maskLyr=contourBufferLyr,
            context=context,
            algRunner=algRunner,
            feedback=multiStepFeedback,
            npRaster=npRaster,
        )
        nanIndexes = np.isnan(npRaster)
        npRaster = (np.rint(npRaster)).astype(float)
        npRaster[nanIndexes] = np.nan
        return npRaster, transform

    def getRangeOfNumberOfPoints(self, featList):
        minValue = min(featList, key=lambda x: x["cota"])["cota"]
        maxValue = max(featList, key=lambda x: x["cota"])["cota"]
        if abs(maxValue - minValue) > 250:
            return (50, 150)
        return (25, 75)

    def buildExclusionLyr(
        self,
        elevationPointsLayer: QgsVectorLayer,
        areaWithoutInformationLyr: QgsVectorLayer,
        waterBodiesLyr: QgsVectorLayer,
        bufferDistance: float,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> QgsVectorLayer:
        algRunner = AlgRunner()
        buffer = algRunner.runBuffer(
            elevationPointsLayer,
            distance=bufferDistance,
            context=context,
            feedback=feedback,
        )
        layerList = [buffer]
        for lyr in [areaWithoutInformationLyr, waterBodiesLyr]:
            if lyr is not None:
                auxLyr = algRunner.runMultipartToSingleParts(
                    lyr, context, is_child_algorithm=True
                )
                layerList.append(auxLyr)
        outputLyr = (
            buffer
            if len(layerList) == 1
            else algRunner.runMergeVectorLayers(layerList, context)
        )
        algRunner.runCreateSpatialIndex(outputLyr, context, is_child_algorithm=True)
        return outputLyr

    def addPointsToMemoryLayer(
        self, lyr: QgsVectorLayer, featList: List, context: QgsProcessingContext
    ) -> None:
        lyr.startEditing()
        lyr.beginEditCommand("adding features")
        lyr.addFeatures(featList)
        lyr.endEditCommand()
        lyr.commitChanges()
        AlgRunner().runCreateSpatialIndex(
            inputLyr=lyr, context=context, is_child_algorithm=True
        )

    def prepareContours(
        self,
        contourLyr: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        heightFieldName: str,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> Tuple[Dict, QgsVectorLayer]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(5, feedback)
            if feedback is not None
            else None
        )
        spatialRelatonsHandler = SpatialRelationsHandler()
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        clippedContourLyr = AlgRunner().runClip(
            inputLayer=contourLyr,
            overlayLayer=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        clippedContourLyr = AlgRunner().runMultipartToSingleParts(
            inputLayer=clippedContourLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        emptyList = [feat.id() for feat in clippedContourLyr.getFeatures() if feat.geometry().isEmpty()]
        if emptyList != []:
            clippedContourLyr.startEditing()
            clippedContourLyr.beginEditCommand("deleting empty")
            clippedContourLyr.deleteFeatures(emptyList)
            clippedContourLyr.endEditCommand()
            clippedContourLyr.commitChanges()
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        (
            contourSpatialIdx,
            contourIdDict,
            _,
            __,
        ) = spatialRelatonsHandler.buildSpatialIndexAndIdDictRelateNodesAndAttributeGroupDict(
            inputLyr=clippedContourLyr,
            attributeName=heightFieldName,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        contourAreaDict, polygonLyr = spatialRelatonsHandler.buildContourAreaDict(
            inputLyr=clippedContourLyr,
            geoBoundsLyr=geographicBoundsLyr,
            attributeName=heightFieldName,
            contourSpatialIdx=contourSpatialIdx,
            contourIdDict=contourIdDict,
            depressionExpression=None,  # TODO
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        AlgRunner().runCreateSpatialIndex(
            polygonLyr, context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        return contourAreaDict, polygonLyr

    def buildGrid(
        self,
        geographicBoundsLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> Tuple[QgsVectorLayer, Dict[QByteArray, int], Dict[QByteArray, QgsVectorLayer]]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        boundsGeom = [i for i in geographicBoundsLyr.getFeatures()][0].geometry()
        xmin, ymin, xmax, ymax = boundsGeom.boundingBox().toRectF().getCoords()
        hSpacing = abs(xmax - xmin) / 3
        vSpacing = abs(ymax - ymin) / 3
        gridLyr = AlgRunner().runCreateGrid(
            extent=geographicBoundsLyr.extent(),
            crs=geographicBoundsLyr.crs(),
            hSpacing=hSpacing,
            vSpacing=vSpacing,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / 9
        gridDict = defaultdict(int)
        gridLyrDict = dict()
        for current, feat in enumerate(gridLyr.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            geom = feat.geometry()
            geomWkb = geom.asWkb()
            gridDict[geomWkb] = 0
            gridLyrDict[geomWkb] = LayerHandler().createMemoryLayerWithFeature(
                geographicBoundsLyr, feat, context
            )
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return gridLyr, gridDict, gridLyrDict

    def getElevationPointsFromNaturalPoints(
        self,
        npRaster: np.array,
        transform: Affine,
        naturalPointFeaturesLyr: QgsVectorLayer,
        exclusionLyr: QgsVectorLayer,
        polygonLyr: QgsVectorLayer,
        bufferDistance: float,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List[QgsFeature]:
        nFeats = naturalPointFeaturesLyr.featureCount()
        if nFeats == 0:
            return
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        pointList = self.getElevationPointsFromLayer(
            npRaster, transform, naturalPointFeaturesLyr, fields
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        return self.filterWithAllCriteria(
            inputPointList=pointList,
            referenceLyr=naturalPointFeaturesLyr,
            exclusionLyr=exclusionLyr,
            polygonLyr=polygonLyr,
            bufferDistance=bufferDistance,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )

    def getElevationPointsFromLayer(self, npRaster, transform, lyr, fields):
        pointList = rasterHandler.createFeatureListWithPointList(
            pointList=lyr.getFeatures(),
            fieldName="cota",
            fields=fields,
            npRaster=npRaster,
            transform=transform,
        )
        return filter(lambda x: x is not None, pointList)

    def validateGeneratedPointsAgainstTerrainModel(
        self,
        elevationPoints: List[QgsFeature],
        polygonLyr: QgsVectorLayer,
        contourAreaDict: Dict,
        threshold: float,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        flagDict = SpatialRelationsHandler().findElevationPointsOutOfThreshold(
            elevationPoints=elevationPoints,
            polygonLyr=polygonLyr,
            contourAreaDict=contourAreaDict,
            threshold=threshold,
            elevationPointHeightFieldName="cota",
            context=context,
            feedback=feedback,
        )
        return (
            elevationPoints
            if flagDict == dict()
            else [
                point
                for point in elevationPoints
                if point.geometry().asWkb() not in flagDict
            ]
        )

    def getElevationPointsFromLineIntersections(
        self,
        lineLyr1,
        lineLyr2,
        geographicBoundsLyr,
        npRaster,
        transform,
        exclusionLyr: QgsVectorLayer,
        polygonLyr: QgsVectorLayer,
        bufferDistance: float,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        if lineLyr1 is None or lineLyr2 is None:
            return []
        algRunner = AlgRunner()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(14, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        localLineLyr1 = algRunner.runClip(
            lineLyr1,
            overlayLayer=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            localLineLyr1, context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        localLineLyr2 = algRunner.runClip(
            lineLyr2,
            overlayLayer=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            localLineLyr2, context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        if localLineLyr1.featureCount() == 0 or localLineLyr2.featureCount() == 0:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        lineIntersectionPointsLyr = algRunner.runLineIntersections(
            localLineLyr1, intersectLyr=localLineLyr2, context=context, feedback=feedback
        )
        if lineIntersectionPointsLyr.featureCount() == 0:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        intersectionBuffers = algRunner.runBuffer(
            inputLayer=lineIntersectionPointsLyr,
            distance=1e-5,
            context=context,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            intersectionBuffers,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        extractedLines1 = algRunner.runExtractByLocation(
            inputLyr=localLineLyr1,
            intersectLyr=intersectionBuffers,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            extractedLines1,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        extractedLines2 = algRunner.runExtractByLocation(
            inputLyr=localLineLyr2,
            intersectLyr=intersectionBuffers,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            extractedLines2,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        intersectedLines = AlgRunner().runSplitLinesWithLines(
            inputLyr=extractedLines1,
            linesLyr=extractedLines2,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            intersectedLines,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        filteredPointsIntersections = self.keepThirdOrderOrHigherPoints(
            points=lineIntersectionPointsLyr,
            linesLyr=intersectedLines,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        pointList = rasterHandler.createFeatureListWithPointList(
            pointList=filteredPointsIntersections,
            fieldName="cota",
            fields=fields,
            npRaster=npRaster,
            transform=transform,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        return self.filterWithAllCriteria(
            inputPointList=filter(lambda x: x is not None, pointList),
            referenceLyr=localLineLyr1,
            exclusionLyr=exclusionLyr,
            polygonLyr=polygonLyr,
            bufferDistance=bufferDistance,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )

    def getMinMaxFeatures(self, fields, npRaster, transform, distance):
        featSet = set()
        maxCoordinatesArray = rasterHandler.getMaxCoordinatesFromNpArray(npRaster)
        maxFeatList = (
            rasterHandler.createFeatureListWithPixelValuesFromPixelCoordinatesArray(
                maxCoordinatesArray,
                fieldName="cota",
                fields=fields,
                npRaster=npRaster,
                transform=transform,
            )
        )
        featSet |= self.filterFeaturesByBuffer(maxFeatList, distance, cotaMaisAlta=True)

        minCoordinatesArray = rasterHandler.getMinCoordinatesFromNpArray(npRaster)
        minFeatList = (
            rasterHandler.createFeatureListWithPixelValuesFromPixelCoordinatesArray(
                minCoordinatesArray,
                fieldName="cota",
                fields=fields,
                npRaster=npRaster,
                transform=transform,
            )
        )
        featSet |= self.filterFeaturesByBuffer(minFeatList, distance)
        return list(featSet)

    def filterWithAllCriteria(
        self,
        inputPointList: List[QgsFeature],
        referenceLyr: QgsVectorLayer,
        exclusionLyr: QgsVectorLayer,
        polygonLyr: QgsVectorLayer,
        bufferDistance: float,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        candidatesPointLyr = LayerHandler().createMemoryLayerWithFeatures(
            featList=inputPointList,
            fields=fields,
            crs=referenceLyr.crs(),
            wkbType=QgsWkbTypes.Point,
            context=context,
        )
        pointList = self.filterFeaturesByDistanceAndExclusionLayer(
            candidatesPointLyr=candidatesPointLyr,
            exclusionLyr=exclusionLyr,
            distance=bufferDistance,
            context=context,
            feedback=multiStepFeedback,
        )
        if len(pointList) == []:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        pointList = self.validateGeneratedPointsAgainstTerrainModel(
            elevationPoints=pointList,
            polygonLyr=polygonLyr,
            contourAreaDict=contourAreaDict,
            threshold=contourHeightInterval,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        newCandidatesPointLyr = LayerHandler().createMemoryLayerWithFeatures(
            featList=pointList,
            fields=fields,
            crs=referenceLyr.crs(),
            wkbType=QgsWkbTypes.Point,
            context=context,
        )
        return self.filterPointsAgainstGrid(
            pointLyr=newCandidatesPointLyr,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            feedback=multiStepFeedback,
        )

    def filterFeaturesByBuffer(
        self, filterFeatList: List, distance, cotaMaisAlta=False
    ):
        outputSet = set()
        exclusionGeom = None
        for feat in filterFeatList:
            geom = feat.geometry()
            buffer = geom.buffer(distance, -1)
            if exclusionGeom is not None and exclusionGeom.intersects(geom):
                continue
            feat["cota_mais_alta"] = cotaMaisAlta
            exclusionGeom = (
                buffer if exclusionGeom is None else exclusionGeom.combine(buffer)
            )
            outputSet.add(feat)
        return outputSet

    def filterFeaturesByDistanceAndExclusionLayer(
        self,
        candidatesPointLyr: QgsVectorLayer,
        exclusionLyr: QgsVectorLayer,
        distance: float,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)

        disjointLyr = AlgRunner().runExtractByLocation(
            candidatesPointLyr,
            exclusionLyr,
            predicate=[2],
            context=context,
            feedback=multiStepFeedback,
        )
        nFeats = disjointLyr.featureCount()
        if nFeats == 0:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        outputSet, exclusionSet = set(), set()
        stepSize = 100 / nFeats
        for current, feat in enumerate(disjointLyr.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            if feat.id() in exclusionSet:
                multiStepFeedback.setProgress(current * stepSize)
                continue
            outputSet.add(feat)
            geom = feat.geometry()
            buffer = geom.buffer(distance, -1)
            bbox = buffer.boundingBox()
            for candidateFeat in disjointLyr.getFeatures(bbox):
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    break
                if candidateFeat.id() == feat.id():
                    continue
                if not candidateFeat.geometry().intersects(buffer):
                    continue
                exclusionSet.add(candidateFeat.id())
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return list(outputSet)

    def filterPointsAgainstGrid(
        self,
        pointLyr: QgsVectorLayer,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        feedback: QgsFeedback,
    ) -> List[QgsFeature]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(9, feedback)
            if feedback is not None
            else None
        )
        outputSet = set()
        for currentStep, feat in enumerate(gridLyr.getFeatures()):
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            geom = feat.geometry()
            bbox = geom.boundingBox()
            geomWkb = geom.asWkb()
            if gridDict[geomWkb] >= maxPointsPerGridUnit:
                continue
            gridFeats = [
                f for f in pointLyr.getFeatures(bbox) if f.geometry().intersects(geom)
            ]
            if gridFeats == []:
                continue
            selectedGridFeatsSet = set(
                islice(gridFeats, maxPointsPerGridUnit - gridDict[geomWkb])
            )
            gridDict[geomWkb] += len(selectedGridFeatsSet)
            outputSet |= selectedGridFeatsSet
        return list(outputSet)

    def updateExclusionLyr(
        self,
        exclusionLyr: QgsVectorLayer,
        pointList: List,
        distance: float,
        context: QgsProcessingContext,
    ) -> None:
        exclusionLyr.startEditing()
        exclusionLyr.beginEditCommand("updating exclusion layer")
        for feat in pointList:
            geom = feat.geometry()
            buffer = geom.buffer(distance, -1)
            newFeat = QgsVectorLayerUtils.createFeature(exclusionLyr, buffer)
            exclusionLyr.addFeature(newFeat)
        exclusionLyr.endEditCommand()
        exclusionLyr.commitChanges()
        AlgRunner().runCreateSpatialIndex(
            exclusionLyr, context, is_child_algorithm=True
        )

    def maskFeaturesFromLayerOnRaster(
        self,
        rasterLyr,
        geographicBoundsLyr,
        maskLyr,
        context,
        algRunner,
        feedback,
        npRaster,
    ):
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
        clippedArea = algRunner.runClip(
            maskLyr,
            geographicBoundsLyr,
            context,
            multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
        npMask = (
            None
            if clippedArea.featureCount() == 0
            else rasterHandler.buildNumpyNodataMask(
                rasterLyr=rasterLyr, vectorLyr=clippedArea
            )
        )
        if npMask is not None:
            npMask.resize(npRaster.shape, refcheck=False)
            npRaster = npRaster + npMask
        return npRaster

    def getElevationPointsFromHilltops(
        self,
        rasterLyr: QgsRasterLayer,
        polygonLyr: QgsVectorLayer,
        exclusionLyr: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        minusBuffergeographicBoundsLyr: QgsVectorLayer,
        bufferDistance: float,
        originEpsg: QgsCoordinateReferenceSystem,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List[QgsFeature]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        pointList = self.extractElevationPointsFromHilltops(
            polygonLayer=polygonLyr,
            rasterLyr=rasterLyr,
            geographicBoundsLyr=geographicBoundsLyr,
            minusBuffergeographicBoundsLyr=minusBuffergeographicBoundsLyr,
            originEpsg=originEpsg,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        return self.filterWithAllCriteria(
            inputPointList=pointList,
            referenceLyr=polygonLyr,
            exclusionLyr=exclusionLyr,
            polygonLyr=polygonLyr,
            bufferDistance=bufferDistance,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )

    def extractElevationPointsFromHilltops(
        self,
        polygonLayer: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        minusBuffergeographicBoundsLyr: QgsVectorLayer,
        rasterLyr: QgsRasterLayer,
        originEpsg: QgsCoordinateReferenceSystem,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback = None,
    ) -> List:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(3, feedback)
            if feedback is not None
            else None
        )
        spatialRelationsHandler = SpatialRelationsHandler()
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Finding hilltops..."))
        hillTopsLyr = spatialRelationsHandler.createHilltopLayerFromPolygonLayer(
            polygonLayer=polygonLayer,
            context=context,
            feedback=multiStepFeedback,
            computeOrder=True,
        )
        algRunner.runCreateSpatialIndex(
            hillTopsLyr, context=context, is_child_algorithm=True
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            currentStep += 1
        minContourLength = geometryHandler.convertDistance(
            self.minContourLength,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        minusBufferLength = geometryHandler.convertDistance(
            self.contourBufferLength,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        clippedHilltops = algRunner.runClip(
            inputLayer=hillTopsLyr,
            overlayLayer=minusBuffergeographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        nFeats = hillTopsLyr.featureCount()
        if nFeats == 0:
            return []
        stepSize = 100 / nFeats
        featList = []
        minArea = minContourLength**2 / (4 * math.pi)
        hilltopList = sorted(
            filter(
                lambda x: x["order_count"] > 1
                and x.geometry().length() > minContourLength
                and x.geometry().area() > minArea,
                clippedHilltops.getFeatures(),
            ),
            key=lambda x: (x["order_count"], 1.0 / x.geometry().area()),
            reverse=True,
        )
        for current, hilltopFeat in enumerate(hilltopList):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            geom = hilltopFeat.geometry()
            minusBuffer = geom.buffer(minusBufferLength, -1)
            if minusBuffer.isEmpty():
                continue
            localHilltopLyr = layerHandler.createMemoryLayerWithFeature(
                hillTopsLyr, hilltopFeat, context
            )
            clippedRaster = algRunner.runClipRasterLayer(
                rasterLyr,
                mask=localHilltopLyr,
                context=context,
                noData=-9999,
                outputRaster=QgsProcessingUtils.generateTempFilename(
                    f"local_clip_{str(uuid4().hex)}.tif"
                ),
            )
            clippedRasterLyr = QgsProcessingUtils.mapLayerFromString(
                clippedRaster, context
            )
            if clippedRasterLyr is None:
                continue
            newFeat = rasterHandler.createMaxPointFeatFromRasterLayer(
                inputRaster=clippedRasterLyr,
                fields=fields,
                fieldName="cota",
            )
            featList.append(newFeat)

            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        return featList

    def keepThirdOrderOrHigherPoints(
        self,
        points: Union[List, QgsVectorLayer],
        linesLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List[QgsFeature]:
        iterator = (
            points.getFeatures() if isinstance(points, QgsVectorLayer) else points
        )
        nFeats = (
            points.featureCount() if isinstance(points, QgsVectorLayer) else len(points)
        )
        if nFeats == 0:
            return []
        featDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(1, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / nFeats
        for current, feat in enumerate(iterator):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            geom = feat.geometry()
            geomWkb = geom.asWkb()
            if geomWkb in featDict:
                continue
            buffer = geom.buffer(1e-5, -1)
            bbox = buffer.boundingBox()
            nFeats = sum(
                1
                for _ in (
                    i
                    for i in linesLyr.getFeatures(bbox)
                    if i.geometry().intersects(geom)
                )
            )
            if nFeats < 3:
                continue
            featDict[geomWkb] = feat  # uses dict to remove duplicated features
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        return list(featDict.values())

    def getElevationPointsFromPlaneAreas(
        self,
        contourLyr: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        rasterLyr: QgsRasterLayer,
        exclusionLyr: QgsVectorLayer,
        polygonLyr: QgsVectorLayer,
        originEpsg: QgsCoordinateReferenceSystem,
        bufferDistance: float,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        gridLyr: QgsVectorLayer,
        gridDict: Dict[QByteArray, int],
        maxPointsPerGridUnit: int,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List[QgsFeature]:
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        localGridSize = geometryHandler.convertDistance(
            self.planeGridSpacing,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        planeGrid = algRunner.runCreateGrid(
            extent=geographicBoundsLyr.extent(),
            crs=geographicBoundsLyr.crs(),
            hSpacing=localGridSize,
            vSpacing=localGridSize,
            context=context,
            feedback=multiStepFeedback,
        )
        algRunner.runCreateSpatialIndex(planeGrid, context, is_child_algorithm=True)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        candidateGridLyr = algRunner.runExtractByLocation(
            inputLyr=contourLyr,
            intersectLyr=planeGrid,
            predicate=[2],
            context=context,
            feedback=multiStepFeedback,
        )
        nFeats = candidateGridLyr.featureCount()
        if nFeats == 0:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / nFeats
        pointList = []
        for current, feat in enumerate(candidateGridLyr.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            localGridLyr = layerHandler.createMemoryLayerWithFeature(
                candidateGridLyr, feat, context
            )
            clippedRaster = algRunner.runClipRasterLayer(
                rasterLyr,
                mask=localGridLyr,
                context=context,
                noData=-9999,
                outputRaster=QgsProcessingUtils.generateTempFilename(
                    f"local_clip_{str(uuid4().hex)}.tif"
                ),
            )
            clippedRasterLyr = QgsProcessingUtils.mapLayerFromString(
                clippedRaster, context
            )
            if clippedRasterLyr is None:
                continue
            newFeatList = rasterHandler.createMaxPointFeatListFromRasterLayer(
                inputRaster=clippedRasterLyr,
                fields=fields,
                fieldName="cota",
            )
            pointList += newFeatList
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        return self.filterWithAllCriteria(
            inputPointList=pointList,
            referenceLyr=polygonLyr,
            exclusionLyr=exclusionLyr,
            polygonLyr=polygonLyr,
            bufferDistance=bufferDistance,
            contourAreaDict=contourAreaDict,
            contourHeightInterval=contourHeightInterval,
            gridLyr=gridLyr,
            gridDict=gridDict,
            maxPointsPerGridUnit=maxPointsPerGridUnit,
            fields=fields,
            context=context,
            feedback=multiStepFeedback,
        )

    def tr(self, string):
        return QCoreApplication.translate("ExtractElevationPoints", string)

    def createInstance(self):
        return ExtractElevationPoints()

    def name(self):
        return "extractelevationpoints"

    def displayName(self):
        return self.tr("Extract Elevation Points")

    def group(self):
        return self.tr("Geometric Algorithms")

    def groupId(self):
        return '"DSGTools: Geometric Algorithms"'

    def shortHelpString(self):
        return self.tr("This algorithm extracts elevation points from DEM.")
