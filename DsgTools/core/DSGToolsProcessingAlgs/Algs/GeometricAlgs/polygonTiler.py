# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 205-03-31
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
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterBoolean,
    QgsFeature,
    QgsGeometry,
    QgsRectangle,
    QgsWkbTypes,
    QgsField,
)
from PyQt5.QtCore import QVariant


class PolygonTilerAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm splits input polygons into a grid of the specified number of rows and columns,
    similar to FME's tiler functionality.
    """

    # Constants used to reference the parameters
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"
    INCLUDE_PARTIAL = "INCLUDE_PARTIAL"

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
            "This algorithm splits input polygons into a grid of the specified number of rows and columns."
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

        # Add the number of rows parameter
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ROWS,
                self.tr("Number of rows"),
                QgsProcessingParameterNumber.Integer,
                2,  # Default value
                False,  # Optional
                1,  # Minimum value
                1000,  # Maximum value
            )
        )

        # Add the number of columns parameter
        self.addParameter(
            QgsProcessingParameterNumber(
                self.COLUMNS,
                self.tr("Number of columns"),
                QgsProcessingParameterNumber.Integer,
                2,  # Default value
                False,  # Optional
                1,  # Minimum value
                1000,  # Maximum value
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
        rows = self.parameterAsInt(parameters, self.ROWS, context)
        columns = self.parameterAsInt(parameters, self.COLUMNS, context)
        include_partial = self.parameterAsBool(
            parameters, self.INCLUDE_PARTIAL, context
        )

        # Check for cancellation
        if feedback.isCanceled():
            return {}

        # Get the fields from the source layer and add row and column fields
        fields = source.fields()
        fields.append(QgsField("_row", QVariant.Int))
        fields.append(QgsField("_column", QVariant.Int))

        # Create the output feature sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
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

            # Calculate the width and height of each cell
            cell_width = bbox.width() / columns
            cell_height = bbox.height() / rows

            # Check for very small cells that might cause precision issues
            if cell_width < 1e-10 or cell_height < 1e-10:
                feedback.pushInfo(
                    self.tr(
                        f"Warning: Very small cell size for feature {feature.id()}. Consider using fewer rows/columns."
                    )
                )

            # Create a grid of cells
            for row in range(rows):
                for col in range(columns):
                    # Check for cancellation regularly
                    if feedback.isCanceled():
                        break

                    # Calculate the bounding box for this cell
                    cell_min_x = bbox.xMinimum() + col * cell_width
                    cell_min_y = bbox.yMinimum() + row * cell_height
                    cell_max_x = cell_min_x + cell_width
                    cell_max_y = cell_min_y + cell_height

                    cell_bbox = QgsRectangle(
                        cell_min_x, cell_min_y, cell_max_x, cell_max_y
                    )

                    # Create a polygon from the cell's bounding box
                    cell_geom = QgsGeometry.fromRect(cell_bbox)

                    # Check intersection with original geometry
                    if cell_geom.intersects(geom):
                        # Get the intersection
                        intersection = cell_geom.intersection(geom)

                        # Skip empty intersections
                        if intersection.isEmpty():
                            continue

                        # Skip if we don't want partial intersections and the cell is not completely within the original geometry
                        if not include_partial and not geom.contains(cell_geom):
                            continue

                        # Create a new feature for the cell
                        new_feat = QgsFeature(fields)
                        # Copy attributes from the original feature
                        for i in range(source.fields().count()):
                            new_feat[i] = feature[i]
                        # Set the row and column attributes
                        new_feat["_row"] = row
                        new_feat["_column"] = col
                        new_feat.setGeometry(intersection)

                        # Add the feature to the sink
                        sink.addFeature(new_feat)
                        tiles_created += 1

            # Update the progress
            feedback.setProgress(int(current * total))

        # Report the number of tiles created
        feedback.pushInfo(
            self.tr(
                f"Created {tiles_created} tiles from {source.featureCount()} input features"
            )
        )

        # Return the output layer
        return {self.OUTPUT: dest_id}
