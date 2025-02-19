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


from dataclasses import dataclass
from typing import Any, Dict, List
from uuid import uuid4
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
from DsgTools.core.Utils.threadingTools import concurrently
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
    QgsProcessingParameterBoolean,
    QgsGeometry,
    QgsProcessingUtils,
)

@dataclass
class RegionGroup:
    """Data class to store region information containing multiple pixel groups"""
    geometries: List[QgsGeometry]
    dn_values: List[int]
    window_data: np.ndarray
    window: Dict[str, int]
    region_id: str
    
    def __hash__(self):
        """Make RegionGroup hashable for caching"""
        return hash(self.region_id)
    
    def __post_init__(self):
        self.geometries = sorted(self.geometries, key=lambda x: x.area(), reverse=False)
    
    def isValid(self):
        return self.window_data.shape > (1, 1)

class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV2(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
    USE_THREADS = "USE_THREADS"
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
            QgsProcessingParameterBoolean(
                self.USE_THREADS,
                self.tr("Use multithreading"),
                defaultValue=True
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
            raise QgsProcessingException(self.tr("This algorithm requires scipy. Please install this library and try again."))
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(self.tr("This algorithm requires networkx. Please install this library and try again."))
        self.algRunner = AlgRunner()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        self.nodata_value = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        use_threads = self.parameterAsBool(parameters, self.USE_THREADS, context)
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
            expression=f"""$area < {min_area} and "DN" != {self.nodata_value} """,
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
                nodata=self.nodata_value,
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
                nodata=self.nodata_value,
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
            self.nodata_value,
        )

        if not out:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runRasterClipByExtent(
                inputRaster=inputRaster,
                extent=inputRaster.extent(),
                nodata=self.nodata_value,
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
            expression=f"""$area < {min_area} and "DN" != {self.nodata_value} """,
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

        regions = self.aggregate_polygons_to_regions(
            nx,
            polygonsNotOnEdge,
            npRaster,
            transform,
            innerFeedback,
            context
        )
        
        currentStep +=1
        innerFeedback.setCurrentStep(currentStep)
        rasterProjection = ds.GetProjection()
        # Process all groups using threads if enabled
        changes_made = self.process_independent_groups(
            regions,
            transform,
            min_area,
            use_threads,
            rasterProjection,
            innerFeedback,
            context,
        )
        currentStep +=1
        innerFeedback.setCurrentStep(currentStep)
        any_changes = False
        for change in changes_made:
            if change is not None and change['changes_made']:
                window = change['window']
                window_data = change['window_data']
                
                # Apply the window data back to the main array
                npRaster[
                    window['x_start']:window['x_end'],
                    window['y_start']:window['y_end']
                ] = window_data
                
                any_changes = True
        
        # Only write output and continue if changes were made
        if any_changes:
            # Write intermediate result
            rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)

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

    def build_polygon_graph(self, nx, polygons, context, feedback):
        """Build a graph of polygon interactions using QGIS processing"""
        graph = nx.Graph()
        
        # Add all polygons as nodes
        for feat in polygons.getFeatures():
            graph.add_node(feat.id(), geometry=feat.geometry(), dn=feat['DN'])
        
        localPolygons = self.algRunner.runCreateFieldWithExpression(
            inputLyr=polygons,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        
        # Use QGIS processing to find intersecting polygons
        intersecting_pairs = self.algRunner.runJoinAttributesByLocation(
            inputLyr=localPolygons,
            joinLyr=localPolygons,
            predicateList=[AlgRunner.Intersects],
            prefix='i_',
            discardNonMatching=True,
            context=context,
            feedback=feedback
        )
        
        # Add edges for intersecting polygons
        for feat in intersecting_pairs.getFeatures():
            if feat['featid'] == feat['i_featid']:
                continue
            graph.add_edge(feat['featid'], feat['i_featid'])
        return graph
    
    def process_window(self, window_data, window, transform, min_area, rasterProjection, pixelBuffer=2, feedback=None, context=None):
        """Process a single raster window, handling one polygon at a time"""
        from scipy.spatial import KDTree
        context = QgsProcessingContext() if context is None else context
        
        # Validate window data dimensions
        if window_data is None or window_data.size == 0:
            return None
            
        rows, cols = window_data.shape
        if rows <= 0 or cols <= 0:
            return None
        nIterations = None
        currentIteration = 0
        while True:
            if feedback is not None and feedback.isCanceled():
                break
                
            # Create and write temporary raster
            temp_output = QgsProcessingUtils.generateTempFilename(
                f"temp_window_{str(uuid4().hex)}.tif"
            )
            
            # Create a new temporary dataset with proper geotransform
            driver = gdal.GetDriverByName('GTiff')
            temp_ds = driver.Create(temp_output, rows, cols, 1, gdal.GDT_Int16)
            
            window_transform = Affine(
                transform.a,                                    # a: scale x
                transform.b,                                    # b: shear x
                transform.c + window['x_start'] * transform.a,  # c: translate x
                transform.d,                                    # d: shear y
                transform.e,                                    # e: scale y
                transform.f + window['y_start'] * transform.e   # f: translate y
            )
            
            # Set the geotransform using GDAL's expected format
            temp_ds.SetGeoTransform(window_transform.to_gdal())
            temp_ds.SetProjection(rasterProjection)  # Assuming ds is accessible or pass it as parameter
            
            # Write the data
            temp_ds.GetRasterBand(1).WriteArray(window_data.T)
            temp_ds.GetRasterBand(1).SetNoDataValue(self.nodata_value)
            
            # Flush to disk
            temp_ds.FlushCache()
            temp_ds = None
                
            # Polygonize current window state
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=temp_output,
                context=context,
            )
            
            # Filter small polygons within the window
            selectedPolygons = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"""$area < {min_area} and "DN" != {self.nodata_value}""",
                context=context,
            )
            
            if selectedPolygons.featureCount() == 0:
                break
            bbox = self.algRunner.runPolygonFromLayerExtent(
                inputLayer=polygonLayer,
                context=context,
                is_child_algorithm=True,
            )
            bboxLine = self.algRunner.runPolygonsToLines(
                inputLyr=bbox,
                context=context,
                is_child_algorithm=True,
            )
            explodedBboxLine = self.algRunner.runExplodeLines(
                inputLyr=bboxLine,
                context=context,
                is_child_algorithm=True,
            )
            polygonsNotOnEdge = self.algRunner.runExtractByLocation(
                inputLyr=selectedPolygons,
                intersectLyr=explodedBboxLine,
                context=context,
                predicate=[AlgRunner.Disjoint],
            )
            if polygonsNotOnEdge.featureCount() == 0:
                break
            if nIterations is None:
                nIterations = 10 * polygonsNotOnEdge.featureCount()
            request = QgsFeatureRequest()
            clause = QgsFeatureRequest.OrderByClause("$area", ascending=True)
            orderby = QgsFeatureRequest.OrderBy([clause])
            request.setOrderBy(orderby)

            # Process one polygon at a time
            feat = next(polygonsNotOnEdge.getFeatures(request), None)
            if feat is None:
                break
            self.processPixelGroup(KDTree, window_data, window_transform, feat, self.nodata_value, pixelBuffer=pixelBuffer)
            currentIteration += 1
            if currentIteration > nIterations:
                break
        return {
            'window_data': window_data,
            'changes_made': True,
            'window': window
        }

    def aggregate_polygons_to_regions(self, nx, polygons, npRaster, transform, feedback, context):
        """Aggregate polygons into regions based on spatial relationships"""
        regions = []
        
        # Build the graph of polygon relationships
        graph = self.build_polygon_graph(nx, polygons, context, feedback)
        
        # Get connected components (groups of related polygons)
        connected_components = list(nx.connected_components(graph))
        
        for component_idx, component in enumerate(connected_components):
            if feedback is not None and feedback.isCanceled():
                break
            
            # Get all geometries and DN values for this component
            component_geometries = []
            component_dn_values = []
            
            # Start with first geometry to build combined geometry
            first_feat = polygons.getFeature(next(iter(component)))
            combined_geom = first_feat.geometry()
            component_geometries.append(combined_geom)
            component_dn_values.append(first_feat['DN'])
            
            # Add remaining geometries
            for feat_id in component:
                if feat_id == first_feat.id():
                    continue
                feat = polygons.getFeature(feat_id)
                geom = feat.geometry()
                combined_geom = combined_geom.combine(geom)
                component_geometries.append(geom)
                component_dn_values.append(feat['DN'])
            
            # Extract window data
            window_data, window = rasterHandler.getNumpyViewFromPolygon(
                npRaster, transform, combined_geom, pixelBuffer=2, returnWindow=True
            )
            
            # Create region group
            region = RegionGroup(
                geometries=component_geometries,
                dn_values=component_dn_values,
                window_data=window_data,
                window=window,
                region_id=f"region_{component_idx}",
            )
            if not region.isValid():
                continue
            regions.append(region)
        
        return regions

    def process_independent_groups(self, regions, transform, min_area, use_threads, rasterProjection, feedback, context):
        """Process independent raster regions"""
        all_results = []
        processLambda = lambda x: self.process_window(x.window_data, x.window, transform, min_area, rasterProjection)
        
        if use_threads and len(regions) > 1:
            for result in concurrently(
                processLambda, regions, feedback=feedback
            ):
                if result is None:
                    continue
                all_results.append(result)
        else:
            for region in regions:
                if feedback.isCanceled():
                    break
                result = self.process_window(
                    region.window_data,
                    region.window,
                    transform,
                    min_area,
                    rasterProjection,
                    feedback=feedback,
                    context=context,
                )
                if result is not None:
                    all_results.append(result)
        
        return all_results
    
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
        pixelBuffer=2,
    ):
        geom = polygonFeat.geometry()

        currentView, mask = rasterHandler.getNumpyViewAndMaskFromPolygon(
            npRaster=npRaster, transform=transform, geom=geom, pixelBuffer=pixelBuffer
        )
        if currentView is None or currentView.size == 0 or currentView.shape == (1, 1):
            return
        v = polygonFeat["DN"]
        originalCopy = np.array(currentView)
        maskedCurrentView = ma.masked_array(currentView, currentView == v, np.int16)
        maskedCurrentView = ma.masked_array(
            maskedCurrentView, currentView == nodata, dtype=np.int16
        )
         # If everything is masked, return original
        if maskedCurrentView.mask.all():
            return
            
        # If nothing is masked (no pixels to change), return
        if not maskedCurrentView.mask.any():
            return
        x, y = np.mgrid[0 : maskedCurrentView.shape[0], 0 : maskedCurrentView.shape[1]]
        xygood = np.array((x[~maskedCurrentView.mask], y[~maskedCurrentView.mask])).T
        xybad = np.array((x[maskedCurrentView.mask], y[maskedCurrentView.mask])).T
        if len(xygood) == 0 or len(xybad) == 0:
            return
        maskedCurrentView[maskedCurrentView.mask] = maskedCurrentView[
            ~maskedCurrentView.mask
        ][KDTree(xygood).query(xybad)[1]]
        currentView = maskedCurrentView.data
        currentView[~np.isnan(mask)] = originalCopy[~np.isnan(mask)]
        currentView[originalCopy == nodata] = originalCopy[originalCopy == nodata]

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifygroupsofpixelstonearestneighboralgorithmv2"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Groups of Pixels to Nearest Neighbor Algorithm V2")

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
            "ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV2", string
        )

    def createInstance(self):
        return ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV2()
