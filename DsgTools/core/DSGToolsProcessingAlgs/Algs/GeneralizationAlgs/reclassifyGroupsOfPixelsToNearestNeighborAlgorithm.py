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


import numpy as np
import numpy.ma as ma

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import rasterHandler

from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessingException,
    QgsProcessingParameterDistance,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
)


class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    OUTPUT = "OUTPUT"

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

        param = QgsProcessingParameterDistance(
            self.MIN_AREA,
            self.tr(
                "Minimun area to process. If feature's area is smaller than this value, "
                "the feature will not be split, but only reclassified to the nearest neighbour. "
                "Area in meters."
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT, self.tr("Output Raster")
            )
        )

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
        algRunner = AlgRunner()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(8, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running initial polygonize"))
        polygonLayer = algRunner.runGdalPolygonize(
            inputRaster=inputRaster,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        selectedPolygonLayer = algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=f"$area < {min_area}",
            context=context,
            feedback=multiStepFeedback,
        )
        nFeats = selectedPolygonLayer.featureCount()
        if nFeats == 0:
            return {self.OUTPUT: outputRaster}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            selectedPolygonLayer, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        polygonsWithCount = algRunner.runJoinByLocationSummary(
            inputLyr=selectedPolygonLayer,
            joinLyr=selectedPolygonLayer,
            joinFields=[],
            predicateList=[AlgRunner.Intersect],
            summaries=[0],
            feedback=multiStepFeedback,
            context=context,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Reading input numpy array"))
        x_res = inputRaster.rasterUnitsPerPixelX()
        y_res = inputRaster.rasterUnitsPerPixelY()

        ds, npRaster = rasterHandler.readAsNumpy(inputRaster, dtype=np.int8)
        transform = rasterHandler.getCoordinateTransform(ds)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Masking for each polygon"))
        crs = selectedPolygonLayer.crs()
        request = QgsFeatureRequest()
        request.setFilterExpression(""" "DN_count" = 1 """)
        self.reclassifyGroupsOfPixelsInsidePolygons(
            KDTree,
            multiStepFeedback,
            polygonsWithCount,
            x_res,
            y_res,
            npRaster,
            transform,
            crs,
            request,
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Writing output"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        request = QgsFeatureRequest()
        clause = QgsFeatureRequest.OrderByClause("$area", ascending=True)
        orderby = QgsFeatureRequest.OrderBy([clause])
        request.setOrderBy(orderby)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Evaluating remaining polygons"))

        ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int8)
        transform = rasterHandler.getCoordinateTransform(ds)
        polygonLayer = algRunner.runGdalPolygonize(
            inputRaster=outputRaster,
            context=context,
        )
        selectedPolygonLayer = algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=f"$area < {min_area}",
            context=context,
        )
        remainingFeatCount = selectedPolygonLayer.featureCount()
        if remainingFeatCount == 0:
            return {self.OUTPUT: outputRaster}

        innerFeedback = QgsProcessingMultiStepFeedback(remainingFeatCount, multiStepFeedback)
        innerFeedback.setCurrentStep(0)

        while True:
            if innerFeedback.isCanceled():
                break
            if (
                innerFeedback.isCanceled()
                or selectedPolygonLayer.featureCount() == 0
            ):
                break
            nextFeat = next(selectedPolygonLayer.getFeatures(request), None)
            if nextFeat is None:
                break
            self.processPixelGroup(
                KDTree, x_res, y_res, npRaster, transform, crs, nextFeat
            )
            rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

            ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int8)
            transform = rasterHandler.getCoordinateTransform(ds)
            polygonLayer = algRunner.runGdalPolygonize(
                inputRaster=outputRaster,
                context=context,
            )
            if (
                innerFeedback.isCanceled()
                or selectedPolygonLayer.featureCount() == 0
            ):
                break

            selectedPolygonLayer = algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"$area < {min_area}",
                context=context,
            )

            innerFeedback.setCurrentStep(remainingFeatCount - selectedPolygonLayer.featureCount() - 1)

        return {self.OUTPUT: outputRaster}

    def reclassifyGroupsOfPixelsInsidePolygons(
        self,
        KDTree,
        multiStepFeedback,
        polygonsWithCount,
        x_res,
        y_res,
        npRaster,
        transform,
        crs,
        request,
    ):
        polygonList = sorted(
            polygonsWithCount.getFeatures(request),
            key=lambda x: x.geometry().area(),
            reverse=False,
        )
        stepSize = 100 / len(polygonList)
        for current, polygonFeat in enumerate(polygonList):
            if multiStepFeedback.isCanceled():
                break
            self.processPixelGroup(
                KDTree, x_res, y_res, npRaster, transform, crs, polygonFeat
            )
            multiStepFeedback.setProgress(current * stepSize)

    def processPixelGroup(
        self, KDTree, x_res, y_res, npRaster, transform, crs, polygonFeat
    ):
        geom = polygonFeat.geometry()

        currentView = rasterHandler.getNumpyViewFromPolygon(
            npRaster=npRaster, transform=transform, geom=geom, pixelBuffer=0
        )
        mask = rasterHandler.buildNumpyNodataMaskForPolygon(
            x_res, y_res, currentView, geom, crs, valueToBurnAsMask=np.nan
        )
        v = polygonFeat["DN"]
        maskedCurrentView = ma.masked_array(
            currentView, currentView == v, np.int8
        )
        # maskedCurrentView = ma.masked_array(mask, mask==np.nan, dtype=np.int8)
        x, y = np.mgrid[0 : maskedCurrentView.shape[0], 0 : maskedCurrentView.shape[1]]
        xygood = np.array((x[~maskedCurrentView.mask], y[~maskedCurrentView.mask])).T
        xybad = np.array((x[maskedCurrentView.mask], y[maskedCurrentView.mask])).T
        maskedCurrentView[maskedCurrentView.mask] = maskedCurrentView[
            ~maskedCurrentView.mask
        ][KDTree(xygood).query(xybad)[1]]
        outputMask = currentView + mask.T
        outputMask[np.isnan(outputMask)] = maskedCurrentView[np.isnan(outputMask)]
        currentView = outputMask

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifygroupsofpixelstonearestneighboralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Groups of Pixels to Nearest Neighbor Algorithm")

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
            "ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm", string
        )

    def createInstance(self):
        return ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm()
