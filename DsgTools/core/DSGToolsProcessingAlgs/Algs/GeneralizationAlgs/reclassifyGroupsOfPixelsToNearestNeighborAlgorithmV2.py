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
import os
from typing import Any, Dict, List, Set, Tuple, Optional
from uuid import uuid4
import numpy as np
import numpy.ma as ma
from osgeo import gdal
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from copy import deepcopy

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import ValidationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools import rasterHandler

from PyQt5.QtCore import QCoreApplication

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
    QgsProcessingUtils,
    QgsGeometry
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

class ReclassifyGroupsOfPixelsToNearestNeighborAlgorithmV2(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_AREA = "MIN_AREA"
    NODATA_VALUE = "NODATA_VALUE"
    USE_THREADS = "USE_THREADS"
    OUTPUT = "OUTPUT"
    
    def initAlgorithm(self, config):
        """Parameter setting."""
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr("Input Single Band Image"),
            )
        )

        param = QgsProcessingParameterDistance(
            self.MIN_AREA,
            self.tr("Minimum area to process"),
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
            QgsProcessingParameterBoolean(
                self.USE_THREADS,
                self.tr("Use multithreading"),
                defaultValue=True
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr("Output Raster")
            )
        )

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

    def compute_nearest_neighbors(
        self,
        xygood: np.ndarray,
        xybad: np.ndarray,
        tree: Optional[Any] = None
    ) -> np.ndarray:
        """Compute nearest neighbors using provided or new KDTree"""
        if tree is None:
            from scipy.spatial import KDTree
            tree = KDTree(xygood)
        return tree.query(xybad)[1]

    def process_window(self, window_data, window, transform, min_area, feedback=None, context=None):
        """Process a single raster window, handling one polygon at a time"""
        from scipy.spatial import KDTree
        changes_made = False
        context = QgsProcessingContext() if context is None else context
        
        # Validate window data dimensions
        if window_data is None or window_data.size == 0:
            return None
            
        rows, cols = window_data.shape
        if rows <= 0 or cols <= 0:
            return None
        
        while True:
            if feedback is not None and feedback.isCanceled():
                break
                
            # Create and write temporary raster
            temp_output = QgsProcessingUtils.generateTempFilename(
                f"temp_window_{str(uuid4().hex)}.tif"
            )
            
            rasterHandler.writeOutputRaster(temp_output, window_data.T)
                
            # Polygonize current window state
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=temp_output,
                context=context,
                feedback=feedback
            )
            
            # Filter small polygons within the window
            selectedPolygons = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"""$area < {min_area} and "DN" != {self.nodata_value}""",
                context=context,
                feedback=feedback
            )
            
            if selectedPolygons.featureCount() == 0:
                break
                
            request = QgsFeatureRequest()
            clause = QgsFeatureRequest.OrderByClause("$area", ascending=True)
            orderby = QgsFeatureRequest.OrderBy([clause])
            request.setOrderBy(orderby)

            # Process one polygon at a time
            feat = next(selectedPolygons.getFeatures(request))
            current_geom = feat.geometry()
            current_value = feat['DN']
            
            # Get view and mask for the single polygon
            view, mask = rasterHandler.getNumpyViewAndMaskFromPolygon(
                npRaster=window_data,
                transform=transform,
                geom=current_geom,
                pixelBuffer=2
            )
            
            if view is None or view.size == 0:
                continue
                
            # Create masked array for processing
            masked_view = ma.masked_array(
                view,
                view == current_value,
                np.int16
            )
            masked_view = ma.masked_array(
                masked_view,
                view == self.nodata_value,
                dtype=np.int16
            )
            
            if masked_view.mask.all():
                continue
                
            # Create coordinate grids
            x, y = np.mgrid[0:masked_view.shape[0], 0:masked_view.shape[1]]
            xygood = np.array((x[~masked_view.mask], y[~masked_view.mask])).T
            xybad = np.array((x[masked_view.mask], y[masked_view.mask])).T
            
            if len(xygood) == 0 or len(xybad) == 0:
                continue
            
            # Compute nearest neighbors
            tree = KDTree(xygood)
            nearest_indices = tree.query(xybad)[1]
            masked_view[masked_view.mask] = masked_view[~masked_view.mask][nearest_indices]
            
            # Create change mask and apply changes
            result_view = masked_view.data
            changes_mask = (result_view != view) & ~np.isnan(mask)
            
            if changes_mask.any():
                # Apply changes to window data
                x_start = max(0, window.get('x_start', 0))
                y_start = max(0, window.get('y_start', 0))
                window_data[
                    x_start:x_start + view.shape[0],
                    y_start:y_start + view.shape[1]
                ][changes_mask] = result_view[changes_mask]
                changes_made = True
        
        if changes_made:
            return {
                'window_data': window_data,
                'changes_made': True,
                'window': window
            }
        return None

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
                region_id=f"region_{component_idx}"
            )
            regions.append(region)
        
        return regions

    def get_raster_window(self, npRaster, transform, geometry, buffer_size=2):
        """Get raster window corresponding to geometry extent with buffer"""
        # Add buffer to bounding box
        bbox = geometry.boundingBox()
        pixel_size = max(abs(transform[0]), abs(transform[4]))
        bbox.grow(buffer_size * pixel_size)
        
        # Convert bbox to pixel coordinates
        # Convert world coordinates to pixel coordinates using the inverse transform
        # For an affine transform:
        # [x'] = [a b c] [x]
        # [y'] = [d e f] [y]
        # [1 ] = [0 0 1] [1]
        # where (x',y') are world coords and (x,y) are pixel coords
        # To get pixel coords, we need to solve for (x,y):
        # x = (x' - c)/a
        # y = (y' - f)/e
        min_x = int((bbox.xMinimum() - transform[2]) / transform[0])
        min_y = int((bbox.yMinimum() - transform[5]) / transform[4])
        max_x = int((bbox.xMaximum() - transform[2]) / transform[0])
        max_y = int((bbox.yMaximum() - transform[5]) / transform[4])
        
        # Get window coordinates
        window = {
            'x_start': max(0, int(min_x)),
            'x_end': min(npRaster.shape[0], int(max_x) + 1),
            'y_start': max(0, int(min_y)),
            'y_end': min(npRaster.shape[1], int(max_y) + 1)
        }
        
        # Extract window
        window_data = npRaster[
            window['x_start']:window['x_end'],
            window['y_start']:window['y_end']
        ].copy()
        
        return window_data, window

    def process_independent_groups(self, regions, transform, min_area, use_threads, feedback, context):
        """Process independent raster regions"""
        all_results = []
        processLambda = lambda x: self.process_window(x.window_data, x.window, transform, min_area)
        
        if use_threads and len(regions) > 1:
            for result in concurrently(
                processLambda, regions, max_concurrency=5
            ):
                if result is None:
                    continue
                all_results.append(result)
                
            # with ThreadPoolExecutor(max_workers=os.cpu_count()-1) as executor:
            #     futures = []
            #     for region in regions:
            #         if feedback.isCanceled():
            #             break
            #         futures.append(
            #             executor.submit(
            #                 self.process_window,
            #                 region.window_data,
            #                 region.window,
            #                 transform,
            #                 min_area,
            #             )
            #         )
                
            #     for future in as_completed(futures):
            #         if feedback.isCanceled():
            #             break
            #         result = future.result()
            #         if result is not None:
            #             all_results.append(result)
        else:
            for region in regions:
                if feedback.isCanceled():
                    break
                result = self.process_window(
                    region.window_data,
                    region.window,
                    transform,
                    min_area,
                    feedback,
                    context,
                )
                if result is not None:
                    all_results.append(result)
        
        return all_results

    def processAlgorithm(self, parameters, context, feedback):
        """Main processing algorithm"""
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(self.tr("This algorithm requires scipy."))
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(self.tr("This algorithm requires networkx."))
            
        self.algRunner = AlgRunner()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        min_area = self.parameterAsDouble(parameters, self.MIN_AREA, context)
        self.nodata_value = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        use_threads = self.parameterAsBool(parameters, self.USE_THREADS, context)
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        
        # Initial raster read
        ds, npRaster = rasterHandler.readAsNumpy(inputRaster, dtype=np.int16)
        transform = rasterHandler.getCoordinateTransform(ds)
        
        # Get edge boundaries
        bbox_lines = self.computeBboxLine(parameters, context, feedback)
        
        # Main processing loop
        iteration = 0
        while True:
            if feedback.isCanceled():
                break
                
            # Polygonize current raster state
            polygonLayer = self.algRunner.runGdalPolygonize(
                inputRaster=outputRaster if iteration > 0 else inputRaster,
                context=context,
                feedback=feedback
            )
            
            # Filter small polygons
            selectedPolygons = self.algRunner.runFilterExpression(
                inputLyr=polygonLayer,
                expression=f"""$area < {min_area} and "DN" != {self.nodata_value}""",
                context=context,
                feedback=feedback
            )
            
            if selectedPolygons.featureCount() == 0:
                break
                
            # Remove edge polygons
            interior_polygons = self.algRunner.runExtractByLocation(
                inputLyr=selectedPolygons,
                intersectLyr=bbox_lines,
                context=context,
                predicate=[AlgRunner.Disjoint],
                feedback=feedback
            )
            
            if interior_polygons.featureCount() == 0:
                break
            
            # Prepare groups for processing
            regions = self.aggregate_polygons_to_regions(
                nx,
                interior_polygons,
                npRaster,
                transform,
                feedback,
                context
            )
            
            # Process all groups using threads if enabled
            changes_made = self.process_independent_groups(
                regions,
                transform,
                min_area,
                use_threads,
                feedback,
                context,
            )
            
            # Only write output and continue if changes were made
            if changes_made:
                # Write intermediate result
                rasterHandler.writeOutputRaster(outputRaster, npRaster.T, ds)
            else:
                # No changes were made, we can exit the loop
                break
            
            iteration += 1
            
            # Optional: add iteration limit
            if iteration > 100:  # Prevent infinite loops
                feedback.pushWarning(
                    self.tr("Maximum iteration limit reached. Some small polygons may remain.")
                )
                break
        
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
    
    def process_pixel_group(
        self,
        KDTree,
        pixel_group: RegionGroup,
        nodata: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Process a single pixel group and return changed pixels"""
        original_view = np.array(pixel_group.buffer_view)
        
        # Create masked array for processing
        masked_view = ma.masked_array(
            pixel_group.buffer_view,
            pixel_group.buffer_view == pixel_group.dn_value,
            np.int16
        )
        masked_view = ma.masked_array(
            masked_view,
            pixel_group.buffer_view == nodata,
            dtype=np.int16
        )
        
        # Create coordinate grids
        x, y = np.mgrid[0:masked_view.shape[0], 0:masked_view.shape[1]]
        xygood = np.array((x[~masked_view.mask], y[~masked_view.mask])).T
        xybad = np.array((x[masked_view.mask], y[masked_view.mask])).T
        
        if len(xygood) == 0 or len(xybad) == 0:
            return None, None
        
        # Compute nearest neighbors
        tree = KDTree(xygood)
        nearest_indices = tree.query(xybad)[1]
        masked_view[masked_view.mask] = masked_view[~masked_view.mask][nearest_indices]
        
        # Create change mask
        result_view = masked_view.data
        changes_mask = (result_view != original_view) & ~np.isnan(pixel_group.mask)
        
        return result_view[changes_mask], changes_mask

    def process_group_wrapper(self, group_data):
        """Wrapper for thread processing"""
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(self.tr("This algorithm requires scipy."))
            
        results = []
        for pixel_group in group_data:
            result_pixels, change_mask = self.process_pixel_group(
                KDTree,
                pixel_group,
                self.nodata_value
            )
            if result_pixels is not None:
                results.append((pixel_group.pixel_coords, result_pixels, change_mask))
        return results

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
