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

from typing import List
from uuid import uuid4
import numpy as np
import json
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import geometryHandler, rasterHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
import processing
from osgeo import gdal, ogr
from PyQt5.QtCore import QCoreApplication, QVariant
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
)


class ExtractElevationPoints(QgsProcessingAlgorithm):

    INPUT_DEM = "INPUT_DEM"
    CONTOUR_LINES = "CONTOUR_LINES"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    SCALE = "SCALE"
    WATER_BODIES = "WATER_BODIES"
    AREA_WITHOUT_INFORMATION_POLYGONS = "AREA_WITHOUT_INFORMATION_POLYGONS"
    MAIN_ROADS = "MAIN_ROADS"
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
                self.MAIN_ROADS,
                self.tr("Main Roads"),
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
        mainRoads = self.parameterAsVectorLayer(parameters, self.MAIN_ROADS, context)
        self.bufferDist = self.distances[scale]

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
            localBoundsLyr = layerHandler.createMemoryLayerWithFeature(
                geographicBoundaryLyr, feat, context
            )
            featList = self.computePoints(
                inputRaster=inputRaster,
                geographicBoundsLyr=localBoundsLyr,
                areaWithoutInformationLyr=areaWithoutInformationLyr,
                waterBodiesLyr=waterBodiesLyr,
                mainRoads=mainRoads,
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
        inputRaster,
        geographicBoundsLyr,
        areaWithoutInformationLyr,
        waterBodiesLyr,
        mainRoads,
        fields,
        context,
        feedback,
    ):
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        nSteps = (
            4 + (areaWithoutInformationLyr is not None) + (waterBodiesLyr is not None)
        )
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        featList = []
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
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
        frameCentroid = (
            [i for i in geographicBoundsLyr.getFeatures()][0].geometry().centroid()
        )
        originEpsg = QgsCoordinateReferenceSystem(
            geometryHandler.getSirgasAuthIdByPointLatLong(*frameCentroid.asPoint())
        )
        localBufferDistance = geometryHandler.convertDistance(
            self.bufferDist,
            originEpsg=originEpsg,
            destinationEpsg=geographicBoundsLyr.crs(),
        )
        if multiStepFeedback is not None:
            currentStep += 1
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
        nanIndexes = np.isnan(npRaster)
        npRaster = (np.rint(npRaster)).astype(float)
        npRaster[nanIndexes] = np.nan

        minMaxFeats = self.getMinMaxFeatures(
            fields, npRaster, transform, distance=localBufferDistance
        )
        featList += minMaxFeats
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        pointsLayer = layerHandler.createMemoryLayerWithFeatures(
            featList=featList,
            fields=fields,
            crs=clippedRasterLyr.crs(),
            wkbType=QgsWkbTypes.Point,
            context=context,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        # create grid

        # create points from first criteria

        # create points from road intersections
        localMainRoads = algRunner.runClip(
            mainRoads,
            overlayLayer=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        featList += self.getContourValuesFromMainRoadIntersections(
            mainRoads=localMainRoads,
            gridLayer=None,
            pointsLayer=pointsLayer,
            fields=fields,
            npRaster=npRaster,
            transform=transform,
            algRunner=algRunner,
            context=context,
            feedback=multiStepFeedback,
        )
        return featList

    def getContourValuesFromMainRoadIntersections(
        self,
        mainRoads,
        gridLayer,
        pointsLayer,
        fields,
        npRaster,
        transform,
        algRunner,
        context,
        feedback,
    ):
        roadIntersections = algRunner.runLineIntersections(
            mainRoads, intersectLyr=mainRoads, context=context, feedback=feedback
        )
        pointList = rasterHandler.createFeatureListWithPointList(
            pointList=roadIntersections.getFeatures(),
            fieldName="cota",
            fields=fields,
            npRaster=npRaster,
            transform=transform,
        )
        return filter(lambda x: x is not None, pointList)

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
