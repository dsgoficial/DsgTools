# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-31
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExpression,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
    QgsFeature,
    QgsGeometry,
    QgsRectangle,
    QgsWkbTypes,
    QgsField,
    QgsExpression,
    QgsExpressionContext,
)
from PyQt5.QtCore import QVariant
import math


class PolygonTilerAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm splits input polygons into tiles of specified size or grid divisions,
    with optional overlap between tiles, similar to FME's tiler functionality.
    """

    # Constants used to reference the parameters
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    TILING_MODE = "TILING_MODE"
    X_DIMENSION = "X_DIMENSION"
    Y_DIMENSION = "Y_DIMENSION"
    INCLUDE_PARTIAL = "INCLUDE_PARTIAL"
    OVERLAP_X = "OVERLAP_X"
    OVERLAP_Y = "OVERLAP_Y"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("PolygonTilerAlgorithm", string)

    def createInstance(self):
        """
        Creates a new instance of the algorithm.
        """
        return PolygonTilerAlgorithm()

    def name(self):
        """
        Returns the unique algorithm name.
        """
        return "polygontiler"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr("Polygon Tiler")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Geometric Algorithms"

    def shortHelpString(self):
        """
        Returns a short help string for the algorithm.
        """
        return self.tr(
            "This algorithm splits input polygons into tiles using either fixed tile sizes "
            "or a specified grid division, with optional overlap between tiles.\n\n"
            "• Fixed Size Mode: X and Y dimensions represent tile width and height in map units. "
            "Overlap creates a sliding window effect.\n"
            "• Grid Division Mode: X and Y dimensions represent number of columns and rows.\n\n"
            "Both dimensions support expressions for dynamic calculation based on feature attributes or geometry."
        )

    def initAlgorithm(self, config=None):
        """
        Configures the parameters for this algorithm.
        """
        # Add the input vector layer parameter
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVectorPolygon]
            )
        )

        # Add tiling mode selection
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TILING_MODE,
                self.tr("Tiling mode"),
                options=[
                    self.tr("Fixed tile size (map units)"),
                    self.tr("Grid division (number of tiles)")
                ],
                defaultValue=0  # Fixed tile size as default
            )
        )

        # X dimension parameter (width OR columns depending on mode)
        self.addParameter(
            QgsProcessingParameterExpression(
                self.X_DIMENSION,
                self.tr("X dimension (width in map units OR number of columns)"),
                "1000",  # Default expression
                self.INPUT,  # Parent layer for context
                False  # Required parameter
            )
        )

        # Y dimension parameter (height OR rows depending on mode)
        self.addParameter(
            QgsProcessingParameterExpression(
                self.Y_DIMENSION,
                self.tr("Y dimension (height in map units OR number of rows)"),
                "1000",  # Default expression
                self.INPUT,  # Parent layer for context
                False  # Required parameter
            )
        )

        # X overlap parameter (units depend on mode)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_X,
                self.tr("X overlap (map units for fixed size, % for grid)"),
                QgsProcessingParameterNumber.Double,
                0.0,  # Default value (no overlap)
                True,  # Optional
                0.0,  # Minimum value
                999999.0,  # Maximum value
            )
        )

        # Y overlap parameter (units depend on mode)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_Y,
                self.tr("Y overlap (map units for fixed size, % for grid)"),
                QgsProcessingParameterNumber.Double,
                0.0,  # Default value (no overlap)
                True,  # Optional
                0.0,  # Minimum value
                999999.0,  # Maximum value
            )
        )

        # Add parameter to include partial intersections
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INCLUDE_PARTIAL,
                self.tr("Include partial intersections"),
                True,  # Default value
            )
        )

        # Add the output feature sink parameter
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Tiled output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Retrieve the parameters
        source = self.parameterAsSource(parameters, self.INPUT, context)
        tiling_mode = self.parameterAsEnum(parameters, self.TILING_MODE, context)
        
        # Create expression context
        expression_context = self.createExpressionContext(parameters, context, source)
        
        overlap_x = self.parameterAsDouble(parameters, self.OVERLAP_X, context)
        overlap_y = self.parameterAsDouble(parameters, self.OVERLAP_Y, context)
        include_partial = self.parameterAsBool(parameters, self.INCLUDE_PARTIAL, context)

        # Check for cancellation
        if feedback.isCanceled():
            return {}

        # Get the fields from the source layer and add tile identification fields
        self.fields = source.fields()
        self.fields.append(QgsField("_tile_row", QVariant.Int))
        self.fields.append(QgsField("_tile_col", QVariant.Int))
        self.fields.append(QgsField("_tile_id", QVariant.String))

        # Create the output feature sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            self.fields,
            QgsWkbTypes.Polygon,
            source.sourceCrs(),
        )

        # Calculate the total number of features to process
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Initialize a counter for created tiles
        tiles_created = 0

        # Process each feature
        for current, feature in enumerate(source.getFeatures()):
            # Stop if processing is canceled
            if feedback.isCanceled():
                break

            # Get the feature's geometry
            geom = feature.geometry()

            # Skip invalid, empty, or non-polygon geometries
            if geom.isEmpty() or geom.type() != QgsWkbTypes.PolygonGeometry:
                feedback.pushInfo(
                    self.tr(f"Skipping feature {feature.id()} - not a valid polygon")
                )
                continue

            # Get the bounding box of the feature
            bbox = geom.boundingBox()

            # Set feature-specific context variables
            feature_context = QgsExpressionContext(expression_context)
            feature_context.setFeature(feature)
            
            # Process based on tiling mode
            if tiling_mode == 0:  # Fixed tile size mode
                tiles_created += self._process_fixed_size_mode(
                    feature, geom, bbox, parameters, context, feature_context, 
                    overlap_x, overlap_y, include_partial, sink, feedback
                )
            else:  # Grid division mode
                tiles_created += self._process_grid_mode(
                    feature, geom, bbox, parameters, context, feature_context,
                    overlap_x, overlap_y, include_partial, sink, feedback
                )

            # Update the progress
            feedback.setProgress(int(current * total))

        # Report the number of tiles created
        mode_name = "fixed size" if tiling_mode == 0 else "grid division"
        feedback.pushInfo(
            self.tr(
                f"Created {tiles_created} tiles from {source.featureCount()} input features using {mode_name} mode"
            )
        )

        # Return the output layer
        return {self.OUTPUT: dest_id}

    def _evaluate_expression(self, expression_string, context, parameter_name):
        """Helper method to evaluate expressions safely."""
        expression = QgsExpression(expression_string)
        if expression.hasParserError():
            raise QgsProcessingException(
                self.tr(f"Error in {parameter_name} expression: {expression.parserErrorString()}")
            )
        
        result = expression.evaluate(context)
        
        try:
            return float(result)
        except (ValueError, TypeError):
            raise QgsProcessingException(
                self.tr(f"{parameter_name} expression must evaluate to a numeric value. Got: {result}")
            )

    def _process_fixed_size_mode(self, feature, geom, bbox, parameters, context, 
                                feature_context, overlap_x, overlap_y, 
                                include_partial, sink, feedback):
        """Process tiling using fixed tile sizes with sliding window overlap."""
        
        # Get dimensions from expressions (interpreted as tile width and height)
        x_dimension_expr = self.parameterAsString(parameters, self.X_DIMENSION, context)
        y_dimension_expr = self.parameterAsString(parameters, self.Y_DIMENSION, context)
        
        tile_width = self._evaluate_expression(x_dimension_expr, feature_context, "X dimension (tile width)")
        tile_height = self._evaluate_expression(y_dimension_expr, feature_context, "Y dimension (tile height)")
        
        if tile_width <= 0 or tile_height <= 0:
            feedback.pushInfo(
                self.tr(f"Skipping feature {feature.id()} - invalid tile dimensions ({tile_width} × {tile_height})")
            )
            return 0

        # Validate overlaps - cannot be equal or greater than tile dimensions
        if overlap_x >= tile_width:
            feedback.pushInfo(
                self.tr(f"Warning: X overlap ({overlap_x}) adjusted from {overlap_x} to {tile_width * 0.9} (90% of tile width)")
            )
            overlap_x = tile_width * 0.9
            
        if overlap_y >= tile_height:
            feedback.pushInfo(
                self.tr(f"Warning: Y overlap ({overlap_y}) adjusted from {overlap_y} to {tile_height * 0.9} (90% of tile height)")
            )
            overlap_y = tile_height * 0.9

        # Calculate step sizes for sliding window (distance between tile centers)
        step_x = tile_width - overlap_x
        step_y = tile_height - overlap_y
        
        # Ensure minimum step size
        if step_x <= 0:
            step_x = tile_width * 0.1
        if step_y <= 0:
            step_y = tile_height * 0.1

        # Calculate number of tiles needed to cover the entire area
        cols = max(1, math.ceil((bbox.width() - tile_width) / step_x) + 1) if bbox.width() > tile_width else 1
        rows = max(1, math.ceil((bbox.height() - tile_height) / step_y) + 1) if bbox.height() > tile_height else 1
        
        feedback.pushInfo(
            self.tr(f"Feature {feature.id()}: Creating {rows}×{cols} sliding window tiles "
                   f"(tile size: {tile_width:.1f}×{tile_height:.1f}, overlap: {overlap_x:.1f}×{overlap_y:.1f}, "
                   f"step: {step_x:.1f}×{step_y:.1f})")
        )
        
        tiles_count = 0
        
        # Create tiles using sliding window approach
        for row in range(rows):
            for col in range(cols):
                if feedback.isCanceled():
                    break
                    
                # Calculate tile bounds using step size (sliding window)
                tile_min_x = bbox.xMinimum() + col * step_x
                tile_min_y = bbox.yMinimum() + row * step_y
                tile_max_x = tile_min_x + tile_width
                tile_max_y = tile_min_y + tile_height
                
                tile_bbox = QgsRectangle(tile_min_x, tile_min_y, tile_max_x, tile_max_y)
                tile_geom = QgsGeometry.fromRect(tile_bbox)
                
                # Check intersection and create tile feature
                if self._create_tile_feature(
                    feature, geom, tile_geom, row, col, include_partial, sink
                ):
                    tiles_count += 1
        
        return tiles_count

    def _process_grid_mode(self, feature, geom, bbox, parameters, context, 
                          feature_context, overlap_x, overlap_y, 
                          include_partial, sink, feedback):
        """Process tiling using grid divisions (X=columns, Y=rows as numbers)."""
        
        # Get dimensions from expressions (interpreted as number of columns and rows)
        x_dimension_expr = self.parameterAsString(parameters, self.X_DIMENSION, context)
        y_dimension_expr = self.parameterAsString(parameters, self.Y_DIMENSION, context)
        
        columns_float = self._evaluate_expression(x_dimension_expr, feature_context, "X dimension (number of columns)")
        rows_float = self._evaluate_expression(y_dimension_expr, feature_context, "Y dimension (number of rows)")
        
        columns = max(1, min(1000, int(columns_float)))
        rows = max(1, min(1000, int(rows_float)))
        
        # Calculate base cell dimensions
        base_cell_width = bbox.width() / columns
        base_cell_height = bbox.height() / rows
        
        # Apply overlap (as percentage)
        overlap_x_fraction = overlap_x / 100.0
        overlap_y_fraction = overlap_y / 100.0
        
        cell_width = base_cell_width * (1.0 + overlap_x_fraction)
        cell_height = base_cell_height * (1.0 + overlap_y_fraction)
        
        feedback.pushInfo(
            self.tr(f"Feature {feature.id()}: Creating {rows}×{columns} grid tiles")
        )
        
        tiles_count = 0
        
        # Create tiles
        for row in range(rows):
            for col in range(columns):
                if feedback.isCanceled():
                    break
                    
                # Calculate tile center and bounds
                center_x = bbox.xMinimum() + (col + 0.5) * base_cell_width
                center_y = bbox.yMinimum() + (row + 0.5) * base_cell_height
                
                tile_min_x = center_x - cell_width / 2.0
                tile_min_y = center_y - cell_height / 2.0
                tile_max_x = center_x + cell_width / 2.0
                tile_max_y = center_y + cell_height / 2.0
                
                tile_bbox = QgsRectangle(tile_min_x, tile_min_y, tile_max_x, tile_max_y)
                tile_geom = QgsGeometry.fromRect(tile_bbox)
                
                # Check intersection and create tile feature
                if self._create_tile_feature(
                    feature, geom, tile_geom, row, col, include_partial, sink
                ):
                    tiles_count += 1
        
        return tiles_count

    def _create_tile_feature(self, original_feature, original_geom, tile_geom, 
                           row, col, include_partial, sink):
        """Helper method to create and add a tile feature."""
        
        # Check intersection with original geometry
        if not tile_geom.intersects(original_geom):
            return False
            
        # Get the intersection
        intersection = tile_geom.intersection(original_geom)
        
        # Skip empty intersections
        if intersection.isEmpty():
            return False
            
        # Skip if we don't want partial intersections and the tile is not completely within the original geometry
        if not include_partial and not original_geom.contains(tile_geom):
            return False
            
        # Create a new feature for the tile
        new_feat = QgsFeature(self.fields)
        
        # Copy attributes from the original feature
        for i in range(original_feature.fields().count()):
            new_feat[i] = original_feature[i]
            
        # Set the tile identification attributes
        new_feat["_tile_row"] = row
        new_feat["_tile_col"] = col
        new_feat["_tile_id"] = f"{row}_{col}"
        new_feat.setGeometry(intersection)
        
        # Add the feature to the sink
        sink.addFeature(new_feat)
        return True
