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
from typing import Dict, List, Tuple, Union
from uuid import uuid4
import numpy as np
import json
from itertools import chain
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import geometryHandler, rasterHandler
from DsgTools.core.GeometricTools.affine import Affine
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
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
                self.CONTOUR_INTERVAL, self.tr("Contour interval"), minValue=0, defaultValue=10
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
        )
        contourHeightInterval = self.parameterAsDouble(parameters, self.CONTOUR_INTERVAL, context)
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
        naturalPointFeaturesLyr = self.parameterAsVectorLayer(parameters, self.NATURAL_POINT_FEATURES, context)
        drainagesWithNameLyr = self.parameterAsVectorLayer(parameters, self.DRAINAGE_LINES_WITH_NAME, context)
        drainagesWithoutNameLyr = self.parameterAsVectorLayer(parameters, self.DRAINAGE_LINES_WITHOUT_NAME, context)
        mainRoadsLyr = self.parameterAsVectorLayer(parameters, self.MAIN_ROADS, context)
        otherRoadsLyr = self.parameterAsVectorLayer(parameters, self.OTHER_ROADS, context)
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
                contourLyr=contourLyr,
                heightFieldName=heightFieldName,
                contourHeightInterval=contourHeightInterval,
                inputRaster=inputRaster,
                geographicBoundsLyr=localBoundsLyr,
                areaWithoutInformationLyr=areaWithoutInformationLyr,
                waterBodiesLyr=waterBodiesLyr,
                naturalPointFeaturesLyr=naturalPointFeaturesLyr,
                drainagesWithNameLyr=drainagesWithNameLyr,
                drainagesWithoutNameLyr=drainagesWithoutNameLyr,
                mainRoadsLyr=mainRoadsLyr,
                otherRoadsLyr=otherRoadsLyr,
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
        nSteps = (
            4 + (naturalPointFeaturesLyr is not None) #handle this count after alg is done
        )
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Clipping raster"))
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
            multiStepFeedback.setProgressText(self.tr("Reading raster with numpy..."))
        npRaster, transform = self.readAndMaskRaster(
            clippedRasterLyr,
            geographicBoundsLyr,
            areaWithoutInformationLyr,
            waterBodiesLyr,
            context,
            algRunner,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Getting max min feats and building exclusion polygons..."))
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
        exclusionLyr = self.buildExclusionLyr(elevationPointsLayer, areaWithoutInformationLyr, waterBodiesLyr, localBufferDistance, context, feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        contourAreaDict, polygonLyr = self.prepareContours(contourLyr, geographicBoundsLyr, context, feedback=multiStepFeedback)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        # create grid

        # create points from first criteria
        if naturalPointFeaturesLyr is not None:
            elevationPointsFromNaturalPointFeatures = self.getElevationPointsFromNaturalPoints(
                npRaster=npRaster,
                transform=transform,
                naturalPointFeaturesLyr=naturalPointFeaturesLyr,
                exclusionLyr=exclusionLyr,
                bufferDistance=localBufferDistance,
                contourAreaDict=contourAreaDict,
                contourHeightInterval=contourHeightInterval,
                fields=fields,
                context=context,
                feedback=multiStepFeedback,
            )

            self.updateExclusionLyr(exclusionLyr, elevationPointsFromNaturalPointFeatures)
            self.addPointsToMemoryLayer(elevationPointsLayer, elevationPointsLayer, context)
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)
            

        # create points from hilltops

        # create points from road intersections
        localMainRoads = algRunner.runClip(
            mainRoadsLyr,
            overlayLayer=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        roadIntersectionFeatList = self.getContourValuesFromMainRoadIntersections(
            mainRoads=localMainRoads,
            gridLayer=None,
            pointsLayer=elevationPointsLayer,
            fields=fields,
            npRaster=npRaster,
            transform=transform,
            algRunner=algRunner,
            context=context,
            feedback=multiStepFeedback,
        )
        self.addPointsToMemoryLayer(elevationPointsLayer, roadIntersectionFeatList, context)
        return elevationPointsLayer.getFeatures()

    def readAndMaskRaster(self, clippedRasterLyr, geographicBoundsLyr, areaWithoutInformationLyr, waterBodiesLyr, context, algRunner, feedback):
        nSteps = (
            2 + (areaWithoutInformationLyr is not None) + (waterBodiesLyr is not None)
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
        nanIndexes = np.isnan(npRaster)
        npRaster = (np.rint(npRaster)).astype(float)
        npRaster[nanIndexes] = np.nan
        return npRaster,transform
    
    def getRangeOfNumberOfPoints(self, featList):
        minValue = min(featList, key = lambda x: x["cota"])
        maxValue = max(featList, key = lambda x: x["cota"])
        if abs(maxValue-minValue) > 250:
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
        outputLyr = buffer if len(layerList) == 1 else algRunner.runMergeVectorLayers(
            layerList, context
        )
        algRunner.runCreateSpatialIndex(outputLyr, context, is_child_algorithm=True)
        return outputLyr
        

    
    def addPointsToMemoryLayer(self, lyr: QgsVectorLayer, featList: List, context: QgsProcessingContext) -> None:
        lyr.startEditing()
        lyr.beginEditCommand("adding features")
        lyr.addFeatures(featList)
        lyr.endEditCommand()
        lyr.commitChanges()
        AlgRunner().runCreateSpatialIndex(inputLyr=lyr, context=context, is_child_algorithm=True)
    
    def prepareContours(
        self,
        contourLyr: QgsVectorLayer,
        geographicBoundsLyr: QgsVectorLayer,
        heightFieldName: str,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> Tuple[Dict, QgsVectorLayer]:
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(4, feedback)
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
        AlgRunner().runCreateSpatialIndex(polygonLyr, context, feedback=multiStepFeedback, is_child_algorithm=True)
        return contourAreaDict, polygonLyr
    
    def getElevationPointsFromNaturalPoints(
        self,
        npRaster: np.array,
        transform: Affine,
        naturalPointFeaturesLyr: QgsVectorLayer,
        exclusionLyr: QgsVectorLayer,
        bufferDistance: float,
        contourAreaDict: Dict,
        contourHeightInterval: float,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> List:
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
        pointList = self.getElevationPointsFromLayer(npRaster, transform, naturalPointFeaturesLyr, fields)
        candidatesPointLyr = LayerHandler().createMemoryLayerWithFeatures(
            featList=pointList,
            fields=fields,
            crs=naturalPointFeaturesLyr.crs(),
            wkbType=QgsWkbTypes.Point,
            context=context
        )
        pointList = self.filterFeaturesByDistanceAndExclusionLayer(
            candidatesPointLyr=candidatesPointLyr,
            exclusionLyr=exclusionLyr,
            distance=bufferDistance,
            context=context,
            feedback=multiStepFeedback
        )
        if len(pointList) == []:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        return self.validateGeneratedPointsAgainstTerrainModel(
            elevationPoints=pointList,
            contourAreaDict=contourAreaDict,
            threshold=contourHeightInterval,
            context=context,
            feedback=multiStepFeedback
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

    def validateGeneratedPointsAgainstTerrainModel(self, elevationPoints, contourAreaDict, threshold, context, feedback):
        flagDict = SpatialRelationsHandler().findElevationPointsOutOfThreshold(
            elevationPoints=elevationPoints,
            contourAreaDict=contourAreaDict,
            threshold=threshold,
            elevationPointHeightFieldName="cota",
            context=context,
            feedback=feedback
        )
        return elevationPoints if flagDict == dict() else [
            point for point in elevationPoints if point.geometry().asWkb() not in flagDict
        ]
    
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
            candidatesPointLyr, exclusionLyr, predicate=[2], context=context, feedback=multiStepFeedback
        )
        nFeats = disjointLyr.featureCount()
        if nFeats == 0:
            return []
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        outputSet, exclusionSet = set(), set()
        stepSize = 100/nFeats
        for current, feat in disjointLyr.getFeatures():
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


    def updateExclusionLyr(self, exclusionLyr: QgsVectorLayer, pointList: List, distance: float, context: QgsProcessingContext) -> None:
        exclusionLyr.startEditing()
        exclusionLyr.beginEditCommand("updating exclusion layer")
        for feat in pointList:
            geom = feat.geometry()
            buffer = geom.buffer(distance, -1)
            newFeat = QgsVectorLayerUtils.createFeature(exclusionLyr, buffer)
            exclusionLyr.addFeature(newFeat)
        exclusionLyr.endEditCommand()
        exclusionLyr.commitChanges()
        AlgRunner().runCreateSpatialIndex(exclusionLyr, context, is_child_algorithm=True)

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

    def extractElevationPointsFromHilltops(
        self,
        contourLinesLyr: QgsVectorLayer,
        geoBoundsLyr: QgsVectorLayer,
        rasterLyr: QgsRasterLayer,
        fields: QgsFields,
        context: QgsProcessingContext,
        feedback: QgsFeedback = None
    ) -> List:
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback) if feedback is not None else None
        spatialRelationsHandler = SpatialRelationsHandler()
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        polygonLayer = spatialRelationsHandler.buildTerrainPolygonLayerFromContours(
            inputLyr=contourLinesLyr,
            geoBoundsLyr=geoBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
            createSpatialIndex=True
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        hillTopsLyr = spatialRelationsHandler.createHilltopLayerFromPolygonLayer(
            polygonLayer=polygonLayer,
            context=context,
            feedback=multiStepFeedback
        )
        nFeats = hillTopsLyr.featureCount()
        if nFeats == 0:
            return []
        stepSize = 100/nFeats
        featList = []
        for current, hilltopFeat in enumerate(hillTopsLyr.getFeatures()):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            localHilltopLyr = layerHandler.createMemoryLayerWithFeature(
                hillTopsLyr, hilltopFeat, context
            )
            clippedRaster = algRunner.runClipRasterLayer(
                rasterLyr,
                mask=localHilltopLyr,
                context=context,
                feedback=feedback,
                noData=-9999,
                outputRaster=QgsProcessingUtils.generateTempFilename(
                    f"local_clip_{str(uuid4().hex)}.tif"
                ),
            )
            clippedRasterLyr = QgsProcessingUtils.mapLayerFromString(clippedRaster, context)
            newFeat = rasterHandler.createMaxPointFeatFromRasterLayer(
                inputRaster=clippedRasterLyr,
                fields=fields,
                fieldName="cota",
            )
            featList.append(newFeat)

            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        
        return featList
    
    
    def keepThirdOrderOrHigherPoints(self, points: Union[List, QgsVectorLayer], linesLyr: QgsVectorLayer, context: QgsProcessingContext, feedback: QgsFeedback) -> List:
        iterator = points.getFeatures() if isinstance(points, QgsVectorLayer) else points
        nFeats = points.featureCount() if isinstance(points, QgsVectorLayer) else len(points)
        if nFeats == 0:
            return []
        featDict = dict()
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
        algRunner = AlgRunner()
        if multiStepFeedback is not None:
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        splitLines = algRunner.runSplitLinesWithLines(
            linesLyr, context, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(splitLines, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
        if multiStepFeedback is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
        #count feats
        stepSize = 100/nFeats
        for current, feat in enumerate(iterator):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled:
                break
            geom = feat.geometry()
            geomWkb = geom.asWkb()
            if geomWkb in featDict:
                continue
            buffer = geom.buffer(1e-5, -1)
            bbox = buffer.boundingBox()
            nFeats = len(i for i in splitLines.getFeatures(bbox) if i.geometry().intersects(geom))
            if nFeats < 3:
                continue
            featDict[geomWkb] = feat # uses dict to remove duplicated features
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

        return list(featDict.values())

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
