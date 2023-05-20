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

from uuid import uuid4
import numpy as np
import json
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import rasterHandler
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
)


class ExtractElevationPoints(QgsProcessingAlgorithm):

    INPUT_DEM = "INPUT_DEM"
    CONTOUR_LINES = "CONTOUR_LINES"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    SCALE = "SCALE"
    AREA_WITHOUT_INFORMATION_POLYGONS = "AREA_WITHOUT_INFORMATION_POLYGONS"
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

        # self.distances = {
        #     0:
        # }

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE, self.tr("Scale"), options=self.scales, defaultValue=0
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
        fields,
        context,
        feedback,
    ):
        algRunner = AlgRunner()
        nSteps = 4 if areaWithoutInformationLyr is None else 6
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
            clippedArea = algRunner.runClip(
                areaWithoutInformationLyr,
                geographicBoundsLyr,
                context,
                multiStepFeedback,
            )
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)
            npMask = (
                None
                if clippedArea.featureCount() == 0
                else rasterHandler.buildNumpyNodataMask(
                    rasterLyr=clippedArea, vectorLyr=clippedArea
                )
            )
            if npMask is not None:
                npMask.resize(npRaster.shape, refcheck=False)
                npRaster = npRaster + npMask
            if multiStepFeedback is not None:
                currentStep += 1
                multiStepFeedback.setCurrentStep(currentStep)

        maxCoordinates = rasterHandler.getMaxCoordinatesFromNpArray(npRaster)
        maxFeat = rasterHandler.createFeatureWithPixelValueFromPixelCoordinates(
            maxCoordinates,
            fieldName="cota",
            fields=fields,
            npRaster=npRaster,
            transform=transform,
        )
        maxFeat["cota_mais_alta"] = True
        featList.append(maxFeat)

        minCoordinates = rasterHandler.getMinCoordinatesFromNpArray(npRaster)
        minFeat = rasterHandler.createFeatureWithPixelValueFromPixelCoordinates(
            minCoordinates,
            fieldName="cota",
            fields=fields,
            npRaster=npRaster,
            transform=transform,
        )
        featList.append(minFeat)
        return featList

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
