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
)


class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
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
        self.algRunner = AlgRunner()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        nodata = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(12, feedback)
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
        out = self.reclassifyGroupsOfPixelsInsidePolygons(
            KDTree,
            multiStepFeedback,
            polygonsWithCount,
            npRaster,
            transform,
            request,
            nodata,
        )

        if not out:
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
        multiStepFeedback.pushInfo(self.tr("Writing output"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        request = QgsFeatureRequest()
        clause = QgsFeatureRequest.OrderByClause("$area", ascending=True)
        orderby = QgsFeatureRequest.OrderBy([clause])
        request.setOrderBy(orderby)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Evaluating remaining polygons"))

        ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int16)
        transform = rasterHandler.getCoordinateTransform(ds)
        polygonLayer = self.algRunner.runGdalPolygonize(
            inputRaster=outputRaster,
            context=context,
        )
        selectedPolygonLayer = self.algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=f"""$area < {min_area} and "DN" != {nodata} """,
            context=context,
        )
        polygonsNotOnEdge = self.algRunner.runExtractByLocation(
            inputLyr=selectedPolygonLayer,
            intersectLyr=explodedBboxLine,
            context=context,
            predicate=[AlgRunner.Disjoint],
            feedback=multiStepFeedback,
        )
        remainingFeatCount = polygonsNotOnEdge.featureCount()
        if remainingFeatCount == 0:
            return {self.OUTPUT: outputRaster}

        multiStepFeedback.pushInfo(
            self.tr(f"Evaluating {remainingFeatCount} groups of remaining pixels")
        )

        innerFeedback = QgsProcessingMultiStepFeedback(
            remainingFeatCount, multiStepFeedback
        )
        innerFeedback.setCurrentStep(0)

        while True:
            if innerFeedback.isCanceled():
                break
            if innerFeedback.isCanceled() or polygonsNotOnEdge.featureCount() == 0:
                break
            nextFeat = next(polygonsNotOnEdge.getFeatures(request), None)
            if nextFeat is None:
                break
            self.processPixelGroup(KDTree, npRaster, transform, nextFeat, nodata)
            rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds, outputType=gdal.GDT_Int16)

            ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int16)
            transform = rasterHandler.getCoordinateTransform(ds)
            if innerFeedback.isCanceled():
                break
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=outputRaster,
                context=context,
            )
            if innerFeedback.isCanceled() or selectedPolygonLayer.featureCount() == 0:
                break

            selectedPolygonLayer = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"""$area < {min_area} and "DN" != {nodata} """,
                context=context,
            )
            if innerFeedback.isCanceled():
                break
            polygonsNotOnEdge = self.algRunner.runExtractByLocation(
                inputLyr=selectedPolygonLayer,
                intersectLyr=explodedBboxLine,
                context=context,
                predicate=[AlgRunner.Disjoint],
            )

            innerFeedback.setCurrentStep(
                remainingFeatCount - polygonsNotOnEdge.featureCount()
            )

        return {self.OUTPUT: outputRaster}

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
            npRaster=npRaster, transform=transform, geom=geom, pixelBuffer=2
        )
        v = polygonFeat["DN"]
        originalCopy = np.array(currentView)
        maskedCurrentView = ma.masked_array(currentView, currentView == v, np.int16)
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == nodata, dtype=np.int16
        )
        x, y = np.mgrid[0 : maskedCurrentView.shape[0], 0 : maskedCurrentView.shape[1]]
        xygood = np.array((x[~maskedCurrentView.mask], y[~maskedCurrentView.mask])).T
        xybad = np.array((x[maskedCurrentView.mask], y[maskedCurrentView.mask])).T
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
