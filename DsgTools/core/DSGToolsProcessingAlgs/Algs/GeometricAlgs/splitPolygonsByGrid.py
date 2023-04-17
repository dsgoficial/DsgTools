# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : diniz.felipe@eb.mil.br
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

from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterField,
                       QgsProcessingUtils,
                       QgsPointXY,
                       QgsGeometry,
                       QgsRectangle,
                       QgsFeature,
                       QgsSpatialIndex,
                       QgsWkbTypes,
                       QgsFeatureRequest)
from qgis.PyQt.QtCore import QCoreApplication

class SplitPolygonsByGrid(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    X_DISTANCE = 'X_DISTANCE'
    Y_DISTANCE = 'Y_DISTANCE'
    NEIGHBOUR = 'NEIGHBOUR'
    ID_FIELD = 'ID_FIELD'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SplitPolygonsByGrid()

    def name(self):
        return 'polygon_split_by_grid'

    def displayName(self):
        return self.tr('Polygon Split by Grid')

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
        return "DSGTools: Geometric Algorithms"

    def shortHelpString(self):
        return self.tr("Splits input polygon layer by regular grid with user-defined X and Y distances and dissolves the intersection polygons based on the nearest neighbor's ID attribute.")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr('Input Polygon Layer'), [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(
            QgsProcessingParameterDistance(
                self.X_DISTANCE, self.tr('X Distance'), parentParameterName=self.INPUT, minValue=0.0))
        self.addParameter(
            QgsProcessingParameterDistance(
                self.Y_DISTANCE, self.tr('Y Distance'), parentParameterName=self.INPUT, minValue=0.0))
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.NEIGHBOUR, self.tr('Neighbour Polygon Layer'), [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(
            QgsProcessingParameterField(
                self.ID_FIELD, self.tr('ID Attribute Field'), parentLayerParameterName=self.NEIGHBOUR, type=QgsProcessingParameterField.Numeric))
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr('Output Layer')))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        x_distance = self.parameterAsDouble(parameters, self.X_DISTANCE, context)
        y_distance = self.parameterAsDouble(parameters, self.Y_DISTANCE, context)
        neighbour_source = self.parameterAsSource(parameters, self.NEIGHBOUR, context)
        id_field = self.parameterAsString(parameters, self.ID_FIELD, context)

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               source.fields(), source.wkbType(), source.sourceCrs())

        # Create a spatial index for the Neighbour layer
        neighbour_idx = QgsSpatialIndex(neighbour_source.getFeatures())

        total_features = source.featureCount()
        progress_step = 100 / total_features if total_features else 0
        current_progress = 0  # Add this line to initialize the variable
        features = source.getFeatures()
        # Create a dictionary to store dissolved geometries
        dissolved_geometries = {}
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            input_geometry = feature.geometry()
            input_bbox = input_geometry.boundingBox()
            min_x, min_y, max_x, max_y = input_bbox.xMinimum(), input_bbox.yMinimum(), input_bbox.xMaximum(), input_bbox.yMaximum()

            for grid_geometry in self.generate_grid_cells((min_x, min_y, max_x, max_y), x_distance, y_distance):
                intersection = input_geometry.intersection(grid_geometry)
                if not intersection.isEmpty() and intersection.type() == QgsWkbTypes.PolygonGeometry:
                    # Find the nearest neighbor
                    neighbor_id = neighbour_idx.nearestNeighbor(intersection.centroid().asPoint(), 1)[0]
                    
                    # Dissolve the intersection with the existing geometry in the dictionary
                    if neighbor_id in dissolved_geometries:
                        dissolved_geometries[neighbor_id] = dissolved_geometries[neighbor_id].combine(intersection)
                    else:
                        dissolved_geometries[neighbor_id] = intersection
                        
                if feedback.isCanceled():
                    break

            current_progress += progress_step
            feedback.setProgress(current_progress)

        # Add dissolved geometries to the output sink
        for neighbor_id, dissolved_geometry in dissolved_geometries.items():
            dissolved_feature = QgsFeature(source.fields())
            dissolved_feature.setGeometry(dissolved_geometry)
            dissolved_feature.setAttribute(id_field, neighbor_id)
            sink.addFeature(dissolved_feature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}

    def generate_grid_cells(self, bbox, x_distance, y_distance):
        min_x, min_y, max_x, max_y = bbox
        x_steps = int((max_x - min_x) / x_distance) + 1
        y_steps = int((max_y - min_y) / y_distance) + 1

        for x in range(x_steps):
            for y in range(y_steps):
                grid_min_point = QgsPointXY(min_x + x * x_distance, min_y + y * y_distance)
                grid_max_point = QgsPointXY(min_x + (x + 1) * x_distance, min_y + (y + 1) * y_distance)
                grid_geometry = QgsGeometry.fromRect(QgsRectangle(grid_min_point, grid_max_point))
                yield grid_geometry
