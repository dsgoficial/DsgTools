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


import math
from typing import Any, Dict
import numpy as np
import numpy.ma as ma

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import rasterHandler

from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

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
    QgsProcessingParameterMultipleLayers,
    QgsProcessing,
)


class ReclassifyGroupsOfPixelsToNearestNeighborWithSlidingWindowAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
    HSPACING = "HSPACING"
    VSPACING = "VSPACING"
    HOVERLAY = "HOVERLAY"
    VOVERLAY = "VOVERLAY"
    NODATA_POLYGON_LAYERS = "NODATA_POLYGON_LAYERS"
    NEGATIVE_BUFFER_DISTANCE = "BUFFER_DISTANCE"
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
                defaultValue=-9999
            )
        )

        param = QgsProcessingParameterDistance(
            self.HSPACING,
            self.tr(
                "Tile horizontal size"
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        param = QgsProcessingParameterDistance(
            self.VSPACING,
            self.tr(
                "Tile vertical size"
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        param = QgsProcessingParameterDistance(
            self.HOVERLAY,
            self.tr(
                "Tile horizontal superposition"
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        param = QgsProcessingParameterDistance(
            self.VOVERLAY,
            self.tr(
                "Tile vertical superposition"
            ),
            parentParameterName=self.INPUT,
            defaultValue=1e-8,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.NODATA_POLYGON_LAYERS,
                self.tr("Polygons with nodata values"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )

        param = QgsProcessingParameterDistance(
            self.NEGATIVE_BUFFER_DISTANCE,
            self.tr(
                "Negative buffer distance"
            ),
            parentParameterName=self.INPUT,
            defaultValue=0.001,
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
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        nodata = self.parameterAsDouble(parameters, self.NODATA_VALUE, context)
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(11, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Preparing output raster"))
        self.buildOutputRaster(outputRaster, parameters, context, multiStepFeedback)
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
        multiStepFeedback.pushInfo(self.tr("Building grid"))
        selectedGrid = self.buildGrid(parameters=parameters, context=context, inputRaster=inputRaster, polygonLayer=polygonLayer, feedback=multiStepFeedback)
        if selectedGrid is None:
            return {self.OUTPUT: outputRaster}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Reading output raster"))
        ds, npRaster = rasterHandler.readAsNumpy(outputRaster, dtype=np.int16)
        transform = rasterHandler.getCoordinateTransform(ds)
        if multiStepFeedback.isCanceled():
            return {self.OUTPUT: outputRaster}

        multiStepFeedback.pushInfo(self.tr("Computing tiles"))
        nTiles = selectedGrid.featureCount()
        innerMultiStepFeedback = QgsProcessingMultiStepFeedback(2*nTiles, multiStepFeedback)
        request = QgsFeatureRequest()
        clause1 = QgsFeatureRequest.OrderByClause("row_index", ascending=True)
        clause2 = QgsFeatureRequest.OrderByClause("col_index", ascending=True)
        orderby = QgsFeatureRequest.OrderBy([clause1, clause2])
        request.setOrderBy(orderby)
        for current, gridFeat in enumerate(selectedGrid.getFeatures(request)):
            if innerMultiStepFeedback.isCanceled():
                break
            innerMultiStepFeedback.setCurrentStep(2*current)
            innerMultiStepFeedback.pushInfo(self.tr(f"Processing tile {current+1}/{nTiles}"))
            geom = gridFeat.geometry()
            maskLyr = self.layerHandler.createMemoryLayerFromGeometry(
                geom=geom,
                crs=inputRaster.crs(),
            )
            clippedRaster = self.algRunner.runClipRasterLayer(
                inputRaster=inputRaster,
                mask=maskLyr,
                context=context,
                feedback=innerMultiStepFeedback,
            )
            innerMultiStepFeedback.setCurrentStep(2*current + 1)
            npView = rasterHandler.getNumpyViewFromPolygon(
                npRaster=npRaster, transform=transform, geom=geom, pixelBuffer=0
            )
            reclassified = self.algRunner.runDSGToolsReclassifyGroupsOfPixels(
                inputRaster=clippedRaster,
                minArea=min_area,
                nodataValue=nodata,
                context=context,
                feedback=innerMultiStepFeedback
            )
            if innerMultiStepFeedback.isCanceled():
                break
            _, reclass_npRaster = rasterHandler.readAsNumpy(reclassified, dtype=np.int16)
            npView = reclass_npRaster
            rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

        return {self.OUTPUT: outputRaster}

    def buildGrid(self, parameters, context, inputRaster, feedback, polygonLayer):
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        nodata = self.parameterAsDouble(parameters, self.NODATA_VALUE, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(8, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        selectedPolygonLayer = self.algRunner.runFilterExpression(
            inputLyr=polygonLayer,
            expression=f"""$area < {min_area} and "DN" != {nodata} """,
            context=context,
            feedback=multiStepFeedback,
        )
        nFeats = selectedPolygonLayer.featureCount()
        if nFeats == 0:
            return None

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
            feedback=multiStepFeedback
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            polygonsNotOnEdge, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building grid"))
        grid = self.algRunner.runCreateGrid(
            extent=inputRaster.extent(),
            crs=inputRaster.crs(),
            hSpacing=parameters[self.HSPACING],
            vSpacing=parameters[self.VSPACING],
            hOverlay=parameters[self.HOVERLAY],
            vOverlay=parameters[self.VOVERLAY],
            is_child_algorithm=True,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            grid, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        selectedGrid = self.algRunner.runExtractByLocation(
            inputLyr=grid,
            intersectLyr=polygonsNotOnEdge,
            context=context,
            feedback=multiStepFeedback
        )
        return selectedGrid


    

    def buildOutputRaster(self, outputRaster, parameters: Dict[str, Any], context: QgsProcessingContext, feedback: QgsFeedback):
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        nodata = self.parameterAsDouble(parameters, self.NODATA_VALUE, context)
        polygonLayerList = self.parameterAsLayerList(
            parameters, self.NODATA_POLYGON_LAYERS, context
        )
        nSteps = 1 if len(polygonLayerList) == 0 else 4
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        burnedRaster = self.algRunner.runRasterClipByExtent(
            inputRaster=inputRaster,
            extent=inputRaster.extent(),
            nodata=nodata,
            context=context,
            feedback=multiStepFeedback,
            outputLyr=outputRaster,
        )
        if len(polygonLayerList) == 0:
            return

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        mergedLyr = self.algRunner.runMergeVectorLayers(
            inputList=polygonLayerList,
            context=context,
            feedback=multiStepFeedback,
            crs=inputRaster.crs(),
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        minusBuffer = self.algRunner.runBuffer(
            inputLayer=mergedLyr,
            distance=-math.abs(parameters[self.NEGATIVE_BUFFER_DISTANCE]),
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runGdalRasterizeOverFixedValue(
            inputLayer=minusBuffer,
            inputRaster=burnedRaster,
            context=context,
            feedback=multiStepFeedback,
        )

    def computeBboxLine(self, parameters: Dict[str, Any], context: QgsProcessingContext, feedback: QgsFeedback):
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
            is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        explodedBboxLine = self.algRunner.runExplodeLines(
            inputLyr=bboxLine,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
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
        return "reclassifygroupsofpixelstonearestneighborwithslidingwindowalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Groups of Pixels to Nearest Neighbor With Sliding Window Algorithm")

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
            "ReclassifyGroupsOfPixelsToNearestNeighborWithSlidingWindowAlgorithm", string
        )

    def createInstance(self):
        return ReclassifyGroupsOfPixelsToNearestNeighborWithSlidingWindowAlgorithm()
