# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-04-15
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
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterField,
    QgsProcessingParameterBoolean,
    QgsFeatureSink,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsSpatialIndex,
    QgsRectangle,
    QgsProcessingMultiStepFeedback,
    QgsProcessingException,
)
from concurrent.futures import ThreadPoolExecutor, ThreadPoolExecutor
import math
import random


class BuildingGeneralizationAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm for generalizing building point features with rotated square symbols,
    using a Multi-Force System with Graph Constraints.
    """

    # Define constants for input and output parameters
    INPUT_BUILDINGS = "INPUT_BUILDINGS"
    INPUT_ROADS = "INPUT_ROADS"
    INPUT_WATER = "INPUT_WATER"
    INPUT_BOUNDARY = "INPUT_BOUNDARY"
    ROTATION_FIELD = "ROTATION_FIELD"
    VISIBILITY_FIELD = "VISIBILITY_FIELD"
    IMPORTANCE_FIELD = "IMPORTANCE_FIELD"
    ROAD_WIDTH_FIELD = "ROAD_WIDTH_FIELD"
    SYMBOL_SIZE = "SYMBOL_SIZE"
    MAX_DISPLACEMENT = "MAX_DISPLACEMENT"
    MAX_ITERATIONS = "MAX_ITERATIONS"
    USE_PARALLEL = "USE_PARALLEL"
    OUTPUT = "OUTPUT"

    def name(self):
        """
        Returns the unique algorithm name.
        """
        return "buildinggeneralizationalgorithm"

    def displayName(self):
        """Returns the display name shown in processing toolbox."""
        return self.tr("Building Generalization")

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
        """Returns a localized string."""
        return QCoreApplication.translate("BuildingGeneralizationAlgorithm", string)

    def createInstance(self):
        """Creates a new instance of the algorithm."""
        return BuildingGeneralizationAlgorithm()

    def shortHelpString(self):
        """
        Returns a short help string for the algorithm.
        """
        return self.tr(
            """
        This algorithm generalizes building point features with rotated square symbols.
        It uses a Multi-Force System with Graph Constraints to resolve spatial conflicts.

        Parameters:
        - Building layer: Point layer representing building locations
        - Road layer: Line layer representing roads with width attribute
        - Water body layer (optional): Polygon layer representing water bodies
        - Geographic boundary layer (optional): Polygon layer defining areas buildings cannot leave
        - Rotation field: Field to store rotation angle
        - Visibility field: Field to store visibility status
        - Importance field (optional): Field indicating building priority
        - Road width field: Field containing road width values
        - Symbol size: Size of square building symbols at target scale
        - Maximum displacement: Maximum distance buildings can be moved
        - Maximum iterations: Maximum number of displacement iterations
        - Use parallel processing: Enable parallel computation (recommended for large datasets)
        """
        )

    def initAlgorithm(self, config=None):
        """
        Configures the parameters of the algorithm.
        """
        # Input layers
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_BUILDINGS,
                self.tr("Building layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_ROADS, self.tr("Road layer"), [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_WATER,
                self.tr("Water body layer (optional)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_BOUNDARY,
                self.tr("Geographic boundary layer (optional)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        # Field parameters
        self.addParameter(
            QgsProcessingParameterField(
                self.ROTATION_FIELD,
                self.tr("Rotation field"),
                None,
                self.INPUT_BUILDINGS,
                QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.VISIBILITY_FIELD,
                self.tr("Visibility field"),
                None,
                self.INPUT_BUILDINGS,
                QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.IMPORTANCE_FIELD,
                self.tr("Importance field (optional)"),
                None,
                self.INPUT_BUILDINGS,
                QgsProcessingParameterField.Numeric,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ROAD_WIDTH_FIELD,
                self.tr("Road width field"),
                None,
                self.INPUT_ROADS,
                QgsProcessingParameterField.Numeric,
            )
        )

        # Numeric parameters
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SYMBOL_SIZE,
                self.tr("Symbol size (map units)"),
                QgsProcessingParameterNumber.Double,
                10.0,
                False,
                0.1,
                1000.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_DISPLACEMENT,
                self.tr("Maximum displacement (map units)"),
                QgsProcessingParameterNumber.Double,
                100.0,
                False,
                0.1,
                1000.0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_ITERATIONS,
                self.tr("Maximum iterations"),
                QgsProcessingParameterNumber.Integer,
                50,
                False,
                1,
                1000,
            )
        )

        # Boolean parameters
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.USE_PARALLEL, self.tr("Use parallel processing"), True
            )
        )

        # Output
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr("Generalized buildings")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Main implementation of the algorithm.
        """
        # Check for required dependencies
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
            
        try:
            from shapely.geometry import (
                Point,
                Polygon,
                LineString,
                box,
                MultiPolygon,
                MultiLineString,
            )
            from shapely.affinity import rotate, translate
            from shapely.ops import unary_union
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python shapely library. Please install this library and try again."
                )
            )
        
        self.graph = nx.Graph()
        
        # Store shapely modules for use in processor
        self.shapely_modules = {
            'Point': Point,
            'Polygon': Polygon,
            'LineString': LineString,
            'box': box,
            'MultiPolygon': MultiPolygon,
            'MultiLineString': MultiLineString,
            'rotate': rotate,
            'translate': translate,
            'unary_union': unary_union
        }
        
        building_source = self.parameterAsSource(
            parameters, self.INPUT_BUILDINGS, context
        )
        road_source = self.parameterAsSource(parameters, self.INPUT_ROADS, context)
        water_source = self.parameterAsSource(parameters, self.INPUT_WATER, context)
        boundary_source = self.parameterAsSource(
            parameters, self.INPUT_BOUNDARY, context
        )

        rotation_field = self.parameterAsString(
            parameters, self.ROTATION_FIELD, context
        )
        visibility_field = self.parameterAsString(
            parameters, self.VISIBILITY_FIELD, context
        )
        importance_field = self.parameterAsString(
            parameters, self.IMPORTANCE_FIELD, context
        )
        road_width_field = self.parameterAsString(
            parameters, self.ROAD_WIDTH_FIELD, context
        )

        symbol_size = self.parameterAsDouble(parameters, self.SYMBOL_SIZE, context)
        max_displacement = self.parameterAsDouble(
            parameters, self.MAX_DISPLACEMENT, context
        )
        max_iterations = self.parameterAsInt(parameters, self.MAX_ITERATIONS, context)
        use_parallel = self.parameterAsBool(parameters, self.USE_PARALLEL, context)

        # Create a multi-step feedback
        steps = 7  # Number of phases
        multi_feedback = QgsProcessingMultiStepFeedback(steps, feedback)

        # Initialize the output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            building_source.fields(),
            building_source.wkbType(),
            building_source.sourceCrs(),
        )

        # Create an instance of our main processor
        processor = BuildingGeneralizationProcessor(
            building_source,
            road_source,
            water_source,
            boundary_source,
            rotation_field,
            visibility_field,
            importance_field,
            road_width_field,
            symbol_size,
            max_displacement,
            max_iterations,
            use_parallel,
            sink,
            feedback,
            self.shapely_modules,  # Pass shapely modules
        )

        # Phase 1: Data Preparation and Structure Creation
        multi_feedback.setCurrentStep(0)
        multi_feedback.pushInfo("Phase 1: Data Preparation and Structure Creation")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase1_data_preparation(multi_feedback)

        # Phase 2: Initial Conflict Analysis
        multi_feedback.setCurrentStep(1)
        multi_feedback.pushInfo("Phase 2: Initial Conflict Analysis")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase2_conflict_analysis(multi_feedback)

        # Phase 3: Rotation Optimization
        multi_feedback.setCurrentStep(2)
        multi_feedback.pushInfo("Phase 3: Rotation Optimization")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase3_rotation_optimization(multi_feedback)

        # Phase 4: Multi-Force System Implementation
        multi_feedback.setCurrentStep(3)
        multi_feedback.pushInfo("Phase 4: Multi-Force System Implementation")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase4_force_system_implementation(multi_feedback)

        # Phase 5: Iterative Resolution Engine
        multi_feedback.setCurrentStep(4)
        multi_feedback.pushInfo("Phase 5: Iterative Resolution Engine")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase5_iterative_resolution(multi_feedback)

        # Phase 6: Visibility Resolution System
        multi_feedback.setCurrentStep(5)
        multi_feedback.pushInfo("Phase 6: Visibility Resolution System")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase6_visibility_resolution(multi_feedback)

        # Phase 7: Output Generation and Visualization
        multi_feedback.setCurrentStep(6)
        multi_feedback.pushInfo("Phase 7: Output Generation and Visualization")
        if multi_feedback.isCanceled():
            return {self.OUTPUT: dest_id}
        processor.phase7_output_generation(multi_feedback)

        return {self.OUTPUT: dest_id}


class BuildingGeneralizationProcessor:
    """
    Main processor class that implements the building generalization algorithm.
    """

    def __init__(
        self,
        building_source,
        road_source,
        water_source,
        boundary_source,
        rotation_field,
        visibility_field,
        importance_field,
        road_width_field,
        symbol_size,
        max_displacement,
        max_iterations,
        use_parallel,
        sink,
        feedback,
        shapely_modules,  # Add shapely modules parameter
    ):
        """
        Initialize the processor with input parameters.
        """
        self.building_source = building_source
        self.road_source = road_source
        self.water_source = water_source
        self.boundary_source = boundary_source

        self.rotation_field = rotation_field
        self.visibility_field = visibility_field
        self.importance_field = importance_field
        self.road_width_field = road_width_field

        self.symbol_size = symbol_size
        self.max_displacement = max_displacement
        self.max_iterations = max_iterations
        self.use_parallel = use_parallel

        self.sink = sink
        self.feedback = feedback
        
        # Store shapely modules for use throughout the processor
        self.shapely = shapely_modules

        # Initialize data structures
        self.buildings = (
            {}
        )  # Dictionary of building features: {id: {feature, center, polygon, rotation, visibility, importance}}
        self.roads = {}  # Dictionary of road features: {id: {feature, width, buffer}}
        self.water_bodies = (
            {}
        )  # Dictionary of water features: {id: {feature, geometry}}
        self.boundaries = (
            {}
        )  # Dictionary of boundary features: {id: {feature, geometry}}

        self.blocks = []  # List of block polygons
        self.building_blocks = {}  # Dictionary mapping building IDs to block IDs

        self.spatial_index_buildings = QgsSpatialIndex()
        self.spatial_index_roads = QgsSpatialIndex()
        self.spatial_index_water = QgsSpatialIndex()
        self.spatial_index_boundaries = QgsSpatialIndex()
        self.spatial_index_blocks = QgsSpatialIndex()

        self.graph = None  # NetworkX graph for conflict resolution

    def create_rotated_square(self, center_x, center_y, size, rotation_angle):
        """
        Create a square polygon centered at (center_x, center_y) with given size and rotation.

        Parameters:
        - center_x, center_y: Center coordinates
        - size: Square side length
        - rotation_angle: Rotation angle in degrees

        Returns:
        - Shapely Polygon representing the rotated square
        """
        half_size = size / 2
        square = self.shapely['box'](
            center_x - half_size,
            center_y - half_size,
            center_x + half_size,
            center_y + half_size,
        )
        rotated_square = self.shapely['rotate'](square, rotation_angle, origin="center")
        return rotated_square

    def phase1_data_preparation(self, feedback):
        """
        Phase 1: Data Preparation and Structure Creation
        - Create specialized spatial indexes for fast geometric operations
        - Generate initial rotated square polygons for all buildings
        - Create road buffer polygons using width attribute
        - Construct block polygons from road network
        - Partition buildings by block and geographic boundary
        """
        feedback.pushInfo("Loading building features...")
        total = (
            100.0 / self.building_source.featureCount()
            if self.building_source.featureCount()
            else 0
        )

        # Load buildings
        for current, feature in enumerate(self.building_source.getFeatures()):
            if feedback.isCanceled():
                break

            feature_id = feature.id()
            geometry = feature.geometry()
            center = geometry.asPoint()

            # Get attributes
            rotation = feature[self.rotation_field] if self.rotation_field else 0
            visibility = (
                feature[self.visibility_field] if self.visibility_field else True
            )
            importance = (
                feature[self.importance_field]
                if self.importance_field
                and self.importance_field in feature.fields().names()
                else 1
            )

            # Create rotated square polygon
            polygon = self.create_rotated_square(
                center.x(), center.y(), self.symbol_size, rotation
            )

            # Store building data
            self.buildings[feature_id] = {
                "feature": feature,
                "center": center,
                "polygon": polygon,
                "rotation": rotation,
                "visibility": visibility,
                "importance": importance,
                "original_center": self.shapely['Point'](center.x(), center.y()),
            }

            # Add to spatial index
            self.spatial_index_buildings.addFeature(feature)

            feedback.setProgress(int(current * total))

        feedback.pushInfo(f"Loaded {len(self.buildings)} building features")

        # Load roads and create buffers
        feedback.pushInfo("Loading road features and creating buffers...")
        total = (
            100.0 / self.road_source.featureCount()
            if self.road_source.featureCount()
            else 0
        )

        for current, feature in enumerate(self.road_source.getFeatures()):
            if feedback.isCanceled():
                break

            feature_id = feature.id()
            geometry = feature.geometry()

            # Get road width
            width = (
                feature[self.road_width_field]
                if self.road_width_field in feature.fields().names()
                else 0
            )

            # Create buffer
            buffer_geometry = geometry.buffer(
                width / 2, 5
            )  # 5 segments per quarter circle

            # Convert to shapely
            # Handle both single LineString and MultiLineString geometries
            if geometry.isMultipart():
                # For MultiLineString, handle each part separately
                multilines = geometry.asMultiPolyline()
                shapely_lines = []
                for line in multilines:
                    line_points = [(p.x(), p.y()) for p in line]
                    if len(line_points) >= 2:  # Ensure the line has at least 2 points
                        shapely_lines.append(self.shapely['LineString'](line_points))

                # Create a MultiLineString if we have multiple lines
                if len(shapely_lines) > 1:
                    shapely_line = self.shapely['MultiLineString'](shapely_lines)
                elif len(shapely_lines) == 1:
                    shapely_line = shapely_lines[0]
                else:
                    # Skip if no valid lines were created
                    continue
            else:
                # For simple LineString
                line_points = [(p.x(), p.y()) for p in geometry.asPolyline()]
                if len(line_points) < 2:  # Skip if not enough points
                    continue
                shapely_line = self.shapely['LineString'](line_points)

            # Extract buffer coordinates
            buffer_polygon = buffer_geometry.asPolygon()[0]
            shapely_buffer = self.shapely['Polygon']([(p.x(), p.y()) for p in buffer_polygon])

            # Store road data
            self.roads[feature_id] = {
                "feature": feature,
                "width": width,
                "line": shapely_line,
                "buffer": shapely_buffer,
            }

            # Add to spatial index
            self.spatial_index_roads.addFeature(feature)

            feedback.setProgress(int(current * total))

        feedback.pushInfo(f"Loaded {len(self.roads)} road features")

        # Load water bodies if available
        if self.water_source:
            feedback.pushInfo("Loading water body features...")
            total = (
                100.0 / self.water_source.featureCount()
                if self.water_source.featureCount()
                else 0
            )

            for current, feature in enumerate(self.water_source.getFeatures()):
                if feedback.isCanceled():
                    break

                feature_id = feature.id()
                geometry = feature.geometry()

                # Convert to shapely
                polygon_rings = geometry.asPolygon()
                if polygon_rings:
                    exterior_ring = polygon_rings[0]
                    shapely_polygon = self.shapely['Polygon']([(p.x(), p.y()) for p in exterior_ring])

                    # Store water data
                    self.water_bodies[feature_id] = {
                        "feature": feature,
                        "geometry": shapely_polygon,
                    }

                    # Add to spatial index
                    self.spatial_index_water.addFeature(feature)

                feedback.setProgress(int(current * total))

            feedback.pushInfo(f"Loaded {len(self.water_bodies)} water body features")

        # Load geographic boundaries if available
        if self.boundary_source:
            feedback.pushInfo("Loading geographic boundary features...")
            total = (
                100.0 / self.boundary_source.featureCount()
                if self.boundary_source.featureCount()
                else 0
            )

            for current, feature in enumerate(self.boundary_source.getFeatures()):
                if feedback.isCanceled():
                    break

                feature_id = feature.id()
                geometry = feature.geometry()

                # Convert to shapely
                polygon_rings = geometry.asPolygon()
                if polygon_rings:
                    exterior_ring = polygon_rings[0]
                    shapely_polygon = self.shapely['Polygon']([(p.x(), p.y()) for p in exterior_ring])

                    # Store boundary data
                    self.boundaries[feature_id] = {
                        "feature": feature,
                        "geometry": shapely_polygon,
                    }

                    # Add to spatial index
                    self.spatial_index_boundaries.addFeature(feature)

                feedback.setProgress(int(current * total))

            feedback.pushInfo(f"Loaded {len(self.boundaries)} boundary features")

        # Construct block polygons from road network
        feedback.pushInfo("Constructing block polygons from road network...")

        # Create a union of all road buffers
        road_buffers = [road["buffer"] for road in self.roads.values()]
        roads_union = self.shapely['unary_union'](road_buffers) if road_buffers else None

        if roads_union:
            # The complement of the road union gives us the blocks
            # We need to define a bounding box that encompasses all buildings
            buildings_bbox = self.building_source.sourceExtent()

            # Expand the bounding box by some margin
            margin = max(self.symbol_size * 2, self.max_displacement * 2)
            expanded_bbox = buildings_bbox.buffered(margin)

            # Create a shapely polygon from the bounding box
            bbox_polygon = self.shapely['Polygon'](
                [
                    (expanded_bbox.xMinimum(), expanded_bbox.yMinimum()),
                    (expanded_bbox.xMaximum(), expanded_bbox.yMinimum()),
                    (expanded_bbox.xMaximum(), expanded_bbox.yMaximum()),
                    (expanded_bbox.xMinimum(), expanded_bbox.yMaximum()),
                ]
            )

            # Subtract the road union from the bounding box to get blocks
            blocks_multipolygon = bbox_polygon.difference(roads_union)

            # Extract individual polygons
            if hasattr(blocks_multipolygon, 'geoms'):
                # It's a MultiPolygon or GeometryCollection
                self.blocks = list(blocks_multipolygon.geoms)
                # Filter out non-polygons if it's a GeometryCollection
                self.blocks = [geom for geom in self.blocks if geom.geom_type == 'Polygon']
            elif blocks_multipolygon.geom_type == 'Polygon':
                # It's a single Polygon
                self.blocks = [blocks_multipolygon]
            else:
                self.blocks = []

            feedback.pushInfo(f"Constructed {len(self.blocks)} block polygons")

            # Create spatial index for blocks
            for i, block in enumerate(self.blocks):
                # Convert shapely polygon to QgsGeometry
                coords = list(block.exterior.coords)
                qgs_polygon = QgsGeometry.fromPolygonXY(
                    [[QgsPointXY(x, y) for x, y in coords]]
                )

                # Create a temporary feature to add to spatial index
                feature = QgsFeature()
                feature.setGeometry(qgs_polygon)
                feature.setId(i)

                self.spatial_index_blocks.addFeature(feature)

            # Assign buildings to blocks
            feedback.pushInfo("Assigning buildings to blocks...")
            total = 100.0 / len(self.buildings) if self.buildings else 0

            for current, (building_id, building) in enumerate(self.buildings.items()):
                if feedback.isCanceled():
                    break

                point = building["original_center"]

                # Find which block contains this building
                for block_id, block in enumerate(self.blocks):
                    if block.contains(point):
                        self.building_blocks[building_id] = block_id
                        break

                feedback.setProgress(int(current * total))

            feedback.pushInfo(
                f"Assigned {len(self.building_blocks)} buildings to blocks"
            )
        else:
            feedback.pushInfo("No road features to construct blocks")

    def phase2_conflict_analysis(self, feedback):
        """
        Phase 2: Initial Conflict Analysis
        - Detect building-building overlaps using rotated square geometries
        - Identify buildings overlapping road buffers
        - Flag buildings in water bodies
        - Mark buildings outside geographic boundaries
        - Create conflict graph using NetworkX
        """
        import networkx as nx
        
        feedback.pushInfo("Initializing conflict graph...")

        # Create nodes for all buildings
        self.graph = nx.Graph()
        for building_id, building in self.buildings.items():
            self.graph.add_node(
                building_id,
                type="building",
                center=building["center"],
                polygon=building["polygon"],
                rotation=building["rotation"],
                visibility=building["visibility"],
                importance=building["importance"],
                conflicts=set(),
                block_id=self.building_blocks.get(building_id),
            )

        feedback.pushInfo(
            f"Created {self.graph.number_of_nodes()} nodes in conflict graph"
        )

        # Detect building-building overlaps
        feedback.pushInfo("Detecting building-building overlaps...")
        total = 100.0 / len(self.buildings) if self.buildings else 0
        overlap_count = 0

        # Function to process a batch of buildings in parallel
        def process_buildings_batch(building_batch):
            local_overlaps = []
            for i, (id1, building1) in enumerate(building_batch):
                polygon1 = building1["polygon"]
                # Get potential overlapping buildings using spatial index
                center1 = building1["center"]
                search_rect = QgsRectangle(
                    center1.x() - self.symbol_size,
                    center1.y() - self.symbol_size,
                    center1.x() + self.symbol_size,
                    center1.y() + self.symbol_size,
                )
                potential_ids = self.spatial_index_buildings.intersects(search_rect)

                for id2 in potential_ids:
                    # Skip self-comparison and already processed pairs
                    if id1 == id2 or id1 > id2:  # Process each pair only once
                        continue

                    building2 = self.buildings.get(id2)
                    if not building2:
                        continue

                    polygon2 = building2["polygon"]

                    # Check for overlap
                    if polygon1.intersects(polygon2):
                        overlap_area = polygon1.intersection(polygon2).area
                        if overlap_area > 0:
                            local_overlaps.append((id1, id2, overlap_area))

            return local_overlaps

        # Divide buildings into batches for parallel processing
        building_items = list(self.buildings.items())
        batch_size = (
            max(1, len(building_items) // (4 * 10))
            if self.use_parallel
            else len(building_items)
        )
        batches = [
            building_items[i : i + batch_size]
            for i in range(0, len(building_items), batch_size)
        ]

        all_overlaps = []
        if self.use_parallel and len(batches) > 1:
            # Process batches in parallel
            with ThreadPoolExecutor() as executor:
                for i, batch_overlaps in enumerate(
                    executor.map(process_buildings_batch, batches)
                ):
                    all_overlaps.extend(batch_overlaps)
                    feedback.setProgress(int((i / len(batches)) * 100))
        else:
            # Process sequentially
            for i, batch in enumerate(batches):
                batch_overlaps = process_buildings_batch(batch)
                all_overlaps.extend(batch_overlaps)
                feedback.setProgress(int((i / len(batches)) * 100))

        # Add edges to graph for building overlaps
        for id1, id2, overlap_area in all_overlaps:
            self.graph.add_edge(
                id1, id2, type="overlap", weight=overlap_area, resolved=False
            )
            self.graph.nodes[id1]["conflicts"].add(id2)
            self.graph.nodes[id2]["conflicts"].add(id1)
            overlap_count += 1

        feedback.pushInfo(f"Detected {overlap_count} building-building overlaps")

        # Identify buildings overlapping road buffers
        feedback.pushInfo("Identifying buildings overlapping road buffers...")
        total = 100.0 / len(self.buildings) if self.buildings else 0
        road_overlap_count = 0

        for current, (building_id, building) in enumerate(self.buildings.items()):
            if feedback.isCanceled():
                break

            building_polygon = building["polygon"]
            center = building["center"]

            # Get nearby roads using spatial index
            search_rect = QgsRectangle(
                center.x()
                - self.symbol_size
                - max([road["width"] for road in self.roads.values()], default=0),
                center.y()
                - self.symbol_size
                - max([road["width"] for road in self.roads.values()], default=0),
                center.x()
                + self.symbol_size
                + max([road["width"] for road in self.roads.values()], default=0),
                center.y()
                + self.symbol_size
                + max([road["width"] for road in self.roads.values()], default=0),
            )

            potential_road_ids = self.spatial_index_roads.intersects(search_rect)

            for road_id in potential_road_ids:
                road = self.roads.get(road_id)
                if not road:
                    continue

                road_buffer = road["buffer"]

                # Check for overlap
                if building_polygon.intersects(road_buffer):
                    overlap_area = building_polygon.intersection(road_buffer).area
                    if overlap_area > 0:
                        self.graph.add_edge(
                            building_id,
                            f"road_{road_id}",
                            type="road_overlap",
                            weight=overlap_area,
                            resolved=False,
                        )
                        self.graph.add_node(
                            f"road_{road_id}",
                            type="road",
                            geometry=road["line"],
                            buffer=road_buffer,
                        )
                        self.graph.nodes[building_id]["conflicts"].add(
                            f"road_{road_id}"
                        )
                        road_overlap_count += 1
                        break  # Only need to know that it overlaps with at least one road

            feedback.setProgress(int(current * total))

        feedback.pushInfo(
            f"Identified {road_overlap_count} buildings overlapping road buffers"
        )

        # Flag buildings in water bodies
        if self.water_source:
            feedback.pushInfo("Flagging buildings in water bodies...")
            total = 100.0 / len(self.buildings) if self.buildings else 0
            water_overlap_count = 0

            for current, (building_id, building) in enumerate(self.buildings.items()):
                if feedback.isCanceled():
                    break

                building_polygon = building["polygon"]
                center = building["center"]

                # Get nearby water bodies using spatial index
                search_rect = QgsRectangle(
                    center.x() - self.symbol_size,
                    center.y() - self.symbol_size,
                    center.x() + self.symbol_size,
                    center.y() + self.symbol_size,
                )

                potential_water_ids = self.spatial_index_water.intersects(search_rect)

                for water_id in potential_water_ids:
                    water = self.water_bodies.get(water_id)
                    if not water:
                        continue

                    water_geometry = water["geometry"]

                    # Check for overlap
                    if building_polygon.intersects(water_geometry):
                        overlap_area = building_polygon.intersection(
                            water_geometry
                        ).area
                        if overlap_area > 0:
                            self.graph.add_edge(
                                building_id,
                                f"water_{water_id}",
                                type="water_overlap",
                                weight=overlap_area,
                                resolved=False,
                            )
                            self.graph.add_node(
                                f"water_{water_id}",
                                type="water",
                                geometry=water_geometry,
                            )
                            self.graph.nodes[building_id]["conflicts"].add(
                                f"water_{water_id}"
                            )
                            water_overlap_count += 1
                            break  # Only need to know that it overlaps with at least one water body

                feedback.setProgress(int(current * total))

            feedback.pushInfo(
                f"Flagged {water_overlap_count} buildings in water bodies"
            )

        # Mark buildings outside geographic boundaries
        if self.boundary_source:
            feedback.pushInfo("Marking buildings outside geographic boundaries...")
            total = 100.0 / len(self.buildings) if self.buildings else 0
            outside_boundary_count = 0

            for current, (building_id, building) in enumerate(self.buildings.items()):
                if feedback.isCanceled():
                    break

                point = building["original_center"]
                center = building["center"]

                # Get nearby boundaries using spatial index
                search_rect = QgsRectangle(
                    center.x() - self.symbol_size,
                    center.y() - self.symbol_size,
                    center.x() + self.symbol_size,
                    center.y() + self.symbol_size,
                )

                potential_boundary_ids = self.spatial_index_boundaries.intersects(
                    search_rect
                )

                inside_any_boundary = False
                for boundary_id in potential_boundary_ids:
                    boundary = self.boundaries.get(boundary_id)
                    if not boundary:
                        continue

                    boundary_geometry = boundary["geometry"]

                    # Check if point is inside boundary
                    if boundary_geometry.contains(point):
                        inside_any_boundary = True
                        # Add edge to graph connecting building to its boundary
                        self.graph.add_edge(
                            building_id,
                            f"boundary_{boundary_id}",
                            type="boundary_constraint",
                            weight=1.0,
                            resolved=True,
                        )
                        self.graph.add_node(
                            f"boundary_{boundary_id}",
                            type="boundary",
                            geometry=boundary_geometry,
                        )
                        break

                if not inside_any_boundary and potential_boundary_ids:
                    outside_boundary_count += 1
                    # Mark the building as outside boundaries
                    self.graph.nodes[building_id]["outside_boundary"] = True

                feedback.setProgress(int(current * total))

            feedback.pushInfo(
                f"Marked {outside_boundary_count} buildings outside geographic boundaries"
            )

    def phase3_rotation_optimization(self, feedback):
        """
        Phase 3: Rotation Optimization
        - Implement parallel rotation calculation using ThreadPoolExecutor
        - For each building, find nearest orientable feature
        - Calculate optimal rotation angle
        - Update polygon geometry with rotation
        - Refresh spatial indexes with rotated geometries
        """
        feedback.pushInfo("Calculating optimal rotation angles...")

        # Function to calculate rotation angle for a single building
        def calculate_rotation(building_id):
            """
            Calculate rotation angle for a building based on its projection onto the nearest road.

            Parameters:
            - building_id: ID of the building to calculate rotation for

            Returns:
            - Tuple of (building_id, angle, feature_type, distance)
            """
            building = self.buildings.get(building_id)
            if not building:
                return None

            center = building["center"]
            original_center = building["original_center"]
            best_angle = 0
            min_distance = float("inf")
            feature_type = None

            # Check nearby roads for orientation
            # Use a larger search radius to ensure finding closest roads
            search_radius = max(
                self.max_displacement * 2, 100
            )  # Ensure at least 100 map units
            search_rect = QgsRectangle(
                center.x() - search_radius,
                center.y() - search_radius,
                center.x() + search_radius,
                center.y() + search_radius,
            )

            potential_road_ids = self.spatial_index_roads.intersects(search_rect)

            # Store all candidate roads and their projections
            road_candidates = []

            for road_id in potential_road_ids:
                road = self.roads.get(road_id)
                if not road:
                    continue

                line = road["line"]
                building_point = self.shapely['Point'](center.x(), center.y())

                # Handle both LineString and MultiLineString
                if isinstance(line, self.shapely['MultiLineString']):
                    for single_line in line.geoms:
                        # Project the building point onto the road
                        try:
                            # Find the nearest point on the road line to the building (projection)
                            linear_ref = single_line.project(building_point)
                            projected_point = single_line.interpolate(linear_ref)

                            # Calculate distance to projected point
                            distance = building_point.distance(projected_point)

                            # Calculate the angle at the projected point
                            # We need to find the segment where the projection falls
                            coords = list(single_line.coords)

                            # Find which segment contains the projected point
                            segment_angle = None
                            for i in range(len(coords) - 1):
                                p1 = coords[i]
                                p2 = coords[i + 1]
                                segment = self.shapely['LineString']([p1, p2])

                                # Get segment length
                                segment_length = segment.length

                                # Calculate distance from projected point to segment
                                segment_distance = segment.distance(projected_point)

                                # If projected point is on or very close to this segment
                                if segment_distance < 0.0001:  # Small threshold
                                    # Calculate angle of segment at the projected point
                                    dx = p2[0] - p1[0]
                                    dy = p2[1] - p1[1]
                                    segment_angle = math.degrees(math.atan2(dy, dx))

                                    road_candidates.append(
                                        {
                                            "distance": distance,
                                            "angle": segment_angle,
                                            "projected_point": (
                                                projected_point.x,
                                                projected_point.y,
                                            ),
                                            "type": "road",
                                        }
                                    )
                                    break

                            # If we couldn't find a segment (rare case), use the general road direction
                            if segment_angle is None and len(coords) >= 2:
                                # Use direction from first to last point
                                dx = coords[-1][0] - coords[0][0]
                                dy = coords[-1][1] - coords[0][1]
                                segment_angle = math.degrees(math.atan2(dy, dx))

                                road_candidates.append(
                                    {
                                        "distance": distance,
                                        "angle": segment_angle,
                                        "projected_point": (
                                            projected_point.x,
                                            projected_point.y,
                                        ),
                                        "type": "road",
                                    }
                                )
                        except (ValueError, ZeroDivisionError):
                            continue  # Skip problematic geometries
                else:
                    # Regular LineString
                    try:
                        # Project the building point onto the road
                        linear_ref = line.project(building_point)
                        projected_point = line.interpolate(linear_ref)

                        # Calculate distance to projected point
                        distance = building_point.distance(projected_point)

                        # Calculate the angle at the projected point
                        coords = list(line.coords)

                        # Find which segment contains the projected point
                        segment_angle = None
                        for i in range(len(coords) - 1):
                            p1 = coords[i]
                            p2 = coords[i + 1]
                            segment = self.shapely['LineString']([p1, p2])

                            # Calculate distance from projected point to segment
                            segment_distance = segment.distance(projected_point)

                            # If projected point is on or very close to this segment
                            if segment_distance < 0.0001:  # Small threshold
                                # Calculate angle of segment at the projected point
                                dx = p2[0] - p1[0]
                                dy = p2[1] - p1[1]
                                segment_angle = math.degrees(math.atan2(dy, dx))

                                road_candidates.append(
                                    {
                                        "distance": distance,
                                        "angle": segment_angle,
                                        "projected_point": (
                                            projected_point.x,
                                            projected_point.y,
                                        ),
                                        "type": "road",
                                    }
                                )
                                break

                        # If we couldn't find a segment (rare case), use the general road direction
                        if segment_angle is None and len(coords) >= 2:
                            # Use direction from first to last point
                            dx = coords[-1][0] - coords[0][0]
                            dy = coords[-1][1] - coords[0][1]
                            segment_angle = math.degrees(math.atan2(dy, dx))

                            road_candidates.append(
                                {
                                    "distance": distance,
                                    "angle": segment_angle,
                                    "projected_point": (
                                        projected_point.x,
                                        projected_point.y,
                                    ),
                                    "type": "road",
                                }
                            )
                    except (ValueError, ZeroDivisionError):
                        continue  # Skip problematic geometries

            # Check nearby water bodies for orientation if available and requested
            if self.water_source:
                # Implementation for water bodies remains the same as original
                potential_water_ids = self.spatial_index_water.intersects(search_rect)

                for water_id in potential_water_ids:
                    water = self.water_bodies.get(water_id)
                    if not water:
                        continue

                    water_geometry = water["geometry"]

                    try:
                        # Find closest point on water boundary
                        boundary = water_geometry.boundary
                        building_point = self.shapely['Point'](center.x(), center.y())
                        linear_ref = boundary.project(building_point)
                        closest_point_info = boundary.interpolate(linear_ref)
                        closest_point = (closest_point_info.x, closest_point_info.y)

                        # Calculate distance
                        distance = building_point.distance(self.shapely['Point'](closest_point))

                        # Find the nearest line segment on the boundary
                        coords = list(boundary.coords)
                        closest_segment_found = False

                        for i in range(len(coords) - 1):
                            p1 = coords[i]
                            p2 = coords[i + 1]

                            # Create line segment
                            segment = self.shapely['LineString']([p1, p2])

                            # Check if closest point is on or very near this segment
                            if (
                                segment.distance(self.shapely['Point'](closest_point)) < 0.0001
                            ):  # Small threshold
                                # Calculate angle of segment
                                dx = p2[0] - p1[0]
                                dy = p2[1] - p1[1]
                                segment_angle = math.degrees(math.atan2(dy, dx))

                                road_candidates.append(
                                    {
                                        "distance": distance,
                                        "angle": segment_angle,
                                        "projected_point": closest_point,
                                        "type": "water",
                                    }
                                )
                                closest_segment_found = True
                                break

                        # If we didn't find a segment very close to the interpolated point,
                        # use the closest segment instead
                        if not closest_segment_found:
                            min_segment_distance = float("inf")
                            closest_segment_angle = 0

                            for i in range(len(coords) - 1):
                                p1 = coords[i]
                                p2 = coords[i + 1]

                                # Create line segment
                                segment = self.shapely['LineString']([p1, p2])

                                # Calculate distance to segment
                                segment_distance = segment.distance(
                                    self.shapely['Point'](center.x(), center.y())
                                )

                                if segment_distance < min_segment_distance:
                                    min_segment_distance = segment_distance

                                    # Calculate angle of segment
                                    dx = p2[0] - p1[0]
                                    dy = p2[1] - p1[1]
                                    closest_segment_angle = math.degrees(
                                        math.atan2(dy, dx)
                                    )

                            road_candidates.append(
                                {
                                    "distance": distance,
                                    "angle": closest_segment_angle,
                                    "projected_point": closest_point,
                                    "type": "water",
                                }
                            )
                    except (ValueError, AttributeError, ZeroDivisionError):
                        continue  # Skip problematic geometries

            # Find the closest feature for alignment
            if road_candidates:
                # Prioritize road features - sort first by type (road > water) then by distance
                road_candidates.sort(
                    key=lambda x: (0 if x["type"] == "road" else 1, x["distance"])
                )

                # Use the closest feature for alignment
                closest_feature = road_candidates[0]
                min_distance = closest_feature["distance"]
                best_angle = closest_feature["angle"] + 90  # Perpendicular angle
                feature_type = closest_feature["type"]

                # Normalize angle to 0-360 range
                best_angle = best_angle % 360

            return building_id, best_angle, feature_type, min_distance

        # Process buildings in parallel or sequentially
        building_ids = list(self.buildings.keys())
        total = 100.0 / len(building_ids) if building_ids else 0

        results = []
        if self.use_parallel:
            # Process in parallel
            with ThreadPoolExecutor() as executor:
                for i, result in enumerate(
                    executor.map(calculate_rotation, building_ids)
                ):
                    if result:
                        results.append(result)

                    if i % 10 == 0:  # Update progress every 10 buildings
                        feedback.setProgress(int(i * total))
        else:
            # Process sequentially
            for i, building_id in enumerate(building_ids):
                if feedback.isCanceled():
                    break

                result = calculate_rotation(building_id)
                if result:
                    results.append(result)

                feedback.setProgress(int(i * total))

        # Update building rotations and polygons
        feedback.pushInfo("Updating building rotations and polygons...")
        road_oriented_count = 0
        water_oriented_count = 0

        feedback.pushInfo(f"Computed rotations for {len(results)} buildings")

        # Log some sample rotation data
        if results:
            sample_size = min(5, len(results))
            feedback.pushInfo(f"Sample rotation data (first {sample_size} buildings):")
            for i in range(sample_size):
                building_id, angle, feature_type, distance = results[i]
                feedback.pushInfo(
                    f"  Building {building_id}: {angle:.1f}° to {feature_type}, "
                    f"distance: {distance:.2f}"
                )

        for building_id, angle, feature_type, distance in results:
            if feature_type == "road":
                road_oriented_count += 1
            elif feature_type == "water":
                water_oriented_count += 1

            building = self.buildings[building_id]
            old_rotation = building["rotation"]

            # Update rotation
            building["rotation"] = angle

            # Recreate rotated square with new angle
            center = building["center"]
            building["polygon"] = self.create_rotated_square(
                center.x(), center.y(), self.symbol_size, angle
            )

            # Update graph node
            self.graph.nodes[building_id]["rotation"] = angle
            self.graph.nodes[building_id]["polygon"] = building["polygon"]

        feedback.pushInfo(
            f"Updated rotations for {len(results)} buildings "
            f"({road_oriented_count} road-oriented, {water_oriented_count} water-oriented)"
        )

    def phase4_force_system_implementation(self, feedback):
        """
        Phase 4: Multi-Force System Implementation
        - Develop vector-based force calculations for each force type
        - Implement spatial optimization to limit force calculations to nearby features
        - Create priority-based weighting system for conflicting forces
        - Develop block containment constraint enforcement
        - Implement adaptive force scaling for convergence
        - Add special handling for isolated buildings (no forces applied)
        """
        feedback.pushInfo("Implementing multi-force system...")

        # Define force weights
        self.force_weights = {
            "building_repulsion": 1.0,
            "road_buffer_repulsion": 2.0,
            "water_body_repulsion": 2.0,
            "position_preservation": 0.5,
            "block_containment": 5.0,
        }

        feedback.pushInfo("Force system configured with weights:")
        for force_type, weight in self.force_weights.items():
            feedback.pushInfo(f"  - {force_type}: {weight}")

        # Define maximum force magnitude (to prevent too large displacements)
        self.max_force_magnitude = self.max_displacement / self.max_iterations

        feedback.pushInfo(f"Maximum force magnitude set to: {self.max_force_magnitude}")

        # Create lookup tables and coefficients for force calculations
        # These will be used in the iterative resolution phase
        self.force_lookup = {}

        # Set adaptive force scaling factor (starts high, decreases over iterations)
        self.initial_force_scale = 1.0
        self.final_force_scale = 0.1

        # Count and report isolated buildings
        isolated_count = sum(
            1
            for node_id, node_data in self.graph.nodes(data=True)
            if node_data.get("isolated", False)
        )
        feedback.pushInfo(
            f"Found {isolated_count} isolated buildings that will not be moved"
        )

    def calculate_building_building_repulsion(self, building_id, other_id):
        """Calculate repulsion force between two overlapping buildings."""
        building1 = self.buildings[building_id]
        building2 = self.buildings[other_id]

        polygon1 = building1["polygon"]
        polygon2 = building2["polygon"]

        # Check if buildings overlap
        if not polygon1.intersects(polygon2):
            return (0, 0)

        # Calculate overlap area
        overlap_area = polygon1.intersection(polygon2).area

        if overlap_area <= 0:
            return (0, 0)

        # Get centroids
        centroid1 = (building1["center"].x(), building1["center"].y())
        centroid2 = (building2["center"].x(), building2["center"].y())

        # Calculate direction vector from building2 to building1
        dx = centroid1[0] - centroid2[0]
        dy = centroid1[1] - centroid2[1]

        # Normalize direction vector
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 0.0001:  # Avoid division by zero
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            distance = math.sqrt(dx * dx + dy * dy)

        # Calculate force magnitude based on overlap area and importance
        importance1 = building1["importance"]
        importance2 = building2["importance"]

        # Lower importance building gets pushed more
        if importance1 > importance2:
            force_magnitude = overlap_area * (importance1 / max(importance2, 0.001))
        elif importance2 > importance1:
            force_magnitude = -overlap_area * (importance2 / max(importance1, 0.001))
        else:
            force_magnitude = 0  # Equal importance, force will be applied equally later

        # Normalize force magnitude
        force_magnitude = min(force_magnitude, self.max_force_magnitude)

        # Calculate force vector
        if force_magnitude != 0:
            force_x = (dx / distance) * abs(force_magnitude)
            force_y = (dy / distance) * abs(force_magnitude)
        else:
            # Equal importance, push in a direction away from centroid
            force_x = (dx / distance) * overlap_area
            force_y = (dy / distance) * overlap_area

        return (force_x, force_y)

    def calculate_road_buffer_repulsion(self, building_id, road_id):
        """Calculate repulsion force from road buffer to building."""
        building = self.buildings[building_id]
        road_id_numeric = int(road_id.split("_")[1])
        road = self.roads[road_id_numeric]

        polygon = building["polygon"]
        buffer = road["buffer"]

        # Check if building overlaps road buffer
        if not polygon.intersects(buffer):
            return (0, 0)

        # Calculate overlap area
        overlap_area = polygon.intersection(buffer).area

        if overlap_area <= 0:
            return (0, 0)

        # Find closest point on road to building centroid
        centroid = (building["center"].x(), building["center"].y())
        road_line = road["line"]

        closest_point_info = road_line.interpolate(road_line.project(self.shapely['Point'](centroid)))
        closest_point = (closest_point_info.x, closest_point_info.y)

        # Calculate direction vector from closest road point to centroid
        dx = centroid[0] - closest_point[0]
        dy = centroid[1] - closest_point[1]

        # Normalize direction vector
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 0.0001:  # Avoid division by zero
            # Get the road direction and use perpendicular
            coords = list(road_line.coords)
            if len(coords) >= 2:
                road_dx = coords[1][0] - coords[0][0]
                road_dy = coords[1][1] - coords[0][1]
                # Perpendicular vector
                dx = -road_dy
                dy = road_dx
            else:
                # Random direction
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)

            distance = math.sqrt(dx * dx + dy * dy)

        # Normalize to unit vector
        dx /= distance
        dy /= distance

        # Calculate force magnitude based on overlap area
        force_magnitude = overlap_area * 2  # Stronger repulsion from roads

        # Normalize force magnitude
        force_magnitude = min(force_magnitude, self.max_force_magnitude)

        # Calculate force vector
        force_x = dx * force_magnitude
        force_y = dy * force_magnitude

        return (force_x, force_y)

    def calculate_water_body_repulsion(self, building_id, water_id):
        """Calculate repulsion force from water body to building."""
        building = self.buildings[building_id]
        water_id_numeric = int(water_id.split("_")[1])
        water = self.water_bodies[water_id_numeric]

        polygon = building["polygon"]
        water_geometry = water["geometry"]

        # Check if building overlaps water body
        if not polygon.intersects(water_geometry):
            return (0, 0)

        # Calculate overlap area
        overlap_area = polygon.intersection(water_geometry).area

        if overlap_area <= 0:
            return (0, 0)

        # Find closest point on water boundary to building centroid
        centroid = (building["center"].x(), building["center"].y())
        water_boundary = water_geometry.boundary

        closest_point_info = water_boundary.interpolate(
            water_boundary.project(self.shapely['Point'](centroid))
        )
        closest_point = (closest_point_info.x, closest_point_info.y)

        # Calculate direction vector from closest water point to centroid
        dx = centroid[0] - closest_point[0]
        dy = centroid[1] - closest_point[1]

        # Normalize direction vector
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 0.0001:  # Avoid division by zero
            # Get a point inside the water body away from the boundary
            interior_point = water_geometry.representative_point()
            # Direction from interior to centroid
            dx = centroid[0] - interior_point.x
            dy = centroid[1] - interior_point.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 0.0001:
                # Still too close, use random direction
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
                distance = math.sqrt(dx * dx + dy * dy)

        # Normalize to unit vector
        dx /= distance
        dy /= distance

        # Calculate force magnitude based on overlap area
        force_magnitude = overlap_area * 2  # Stronger repulsion from water bodies

        # Normalize force magnitude
        force_magnitude = min(force_magnitude, self.max_force_magnitude)

        # Calculate force vector
        force_x = dx * force_magnitude
        force_y = dy * force_magnitude

        return (force_x, force_y)

    def calculate_position_preservation(self, building_id):
        """Calculate force pulling building back to original position."""
        building = self.buildings[building_id]

        original_center = building["original_center"]
        current_center = (building["center"].x(), building["center"].y())

        # Calculate displacement vector
        dx = original_center.x - current_center[0]
        dy = original_center.y - current_center[1]

        # Calculate distance
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.0001:  # No significant displacement
            return (0, 0)

        # Normalize direction vector
        dx /= distance
        dy /= distance

        # Calculate force magnitude based on distance
        force_magnitude = min(distance * 0.2, self.max_force_magnitude / 2)

        # Calculate force vector
        force_x = dx * force_magnitude
        force_y = dy * force_magnitude

        return (force_x, force_y)

    def calculate_block_containment(self, building_id):
        """Calculate force to keep building within its original block."""
        building = self.buildings[building_id]
        block_id = self.building_blocks.get(building_id)

        if block_id is None or block_id >= len(self.blocks):
            return (0, 0)

        block = self.blocks[block_id]
        polygon = building["polygon"]

        # Check if building is still within block
        if block.contains(polygon):
            return (0, 0)

        # Find closest point on block boundary to building centroid
        centroid = (building["center"].x(), building["center"].y())
        centroid_point = self.shapely['Point'](centroid)

        if block.contains(centroid_point):
            # Center is inside but some part of polygon is outside
            # Push toward center of block
            block_centroid = block.centroid

            # Direction toward block center
            dx = block_centroid.x - centroid[0]
            dy = block_centroid.y - centroid[1]

            # Normalize
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < 0.0001:
                return (0, 0)

            dx /= distance
            dy /= distance

            # Calculate force magnitude
            force_magnitude = min(
                self.max_force_magnitude, polygon.difference(block).area * 2
            )

            return (dx * force_magnitude, dy * force_magnitude)
        else:
            # Center is outside block
            # Find closest point on block boundary
            boundary = block.boundary
            closest_point_info = boundary.interpolate(boundary.project(centroid_point))
            closest_point = (closest_point_info.x, closest_point_info.y)

            # Direction toward closest point
            dx = closest_point[0] - centroid[0]
            dy = closest_point[1] - centroid[1]

            # Normalize
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < 0.0001:
                return (0, 0)

            dx /= distance
            dy /= distance

            # Strong force to get back into block
            force_magnitude = min(self.max_force_magnitude * 2, distance)

            return (dx * force_magnitude, dy * force_magnitude)

    def phase5_iterative_resolution(self, feedback):
        """
        Phase 5: Iterative Resolution Engine
        - Create main iteration loop with progress feedback
        - Implement parallel force calculation using ProcessPoolExecutor
        - Develop geometry recreation for each iteration
        - Implement conflict detection for termination condition
        - Add early stopping mechanism for resolved areas
        - Skip isolated buildings during force calculation
        """
        feedback.pushInfo("Starting iterative displacement resolution...")

        # Initialize progress
        total_iterations = min(self.max_iterations, 100)  # Cap for reporting purposes
        iterations_per_step = max(1, total_iterations // 100)

        # Initialize counters
        num_buildings = len(self.buildings)
        initially_conflicted = sum(
            1
            for building_id in self.buildings
            if len(self.graph.nodes[building_id]["conflicts"]) > 0
        )

        # Main iteration loop
        current_conflicts = initially_conflicted
        force_scale = self.initial_force_scale

        for iteration in range(self.max_iterations):
            if feedback.isCanceled():
                break

            # Update progress
            if iteration % iterations_per_step == 0:
                progress_pct = int((iteration / total_iterations) * 100)
                feedback.setProgress(progress_pct)

                # Report current status
                if iteration > 0:
                    conflict_reduction = (
                        (initially_conflicted - current_conflicts)
                        / initially_conflicted
                        * 100
                        if initially_conflicted > 0
                        else 0
                    )
                    feedback.pushInfo(
                        f"Iteration {iteration}: {current_conflicts} buildings with conflicts "
                        f"({conflict_reduction:.1f}% reduction)"
                    )

            # Calculate force scale for this iteration (decreases over time)
            force_scale = self.initial_force_scale - (
                (self.initial_force_scale - self.final_force_scale)
                * (iteration / self.max_iterations)
            )

            # Function to calculate all forces for one building
            def calculate_forces(building_id):
                if building_id not in self.buildings:
                    return building_id, (0, 0)

                # Get building node
                node = self.graph.nodes[building_id]

                # Skip isolated buildings - these should not be moved
                if node.get("isolated", False):
                    return building_id, (0, 0)

                conflicts = node.get("conflicts", set())

                # Skip if no conflicts and already within block
                if not conflicts and not self.check_building_outside_block(building_id):
                    return building_id, (0, 0)

                # Initialize force components
                force_x = 0
                force_y = 0

                # Building-building repulsion
                for other_id in conflicts:
                    # Check if other_id is a string (road/water) or integer (building)
                    if isinstance(other_id, str) and (
                        other_id.startswith("road_") or other_id.startswith("water_")
                    ):
                        continue

                    # Only apply if other building exists
                    if other_id in self.buildings:
                        fx, fy = self.calculate_building_building_repulsion(
                            building_id, other_id
                        )
                        force_x += fx * self.force_weights["building_repulsion"]
                        force_y += fy * self.force_weights["building_repulsion"]

                # Road buffer repulsion
                for other_id in conflicts:
                    if isinstance(other_id, str) and other_id.startswith("road_"):
                        fx, fy = self.calculate_road_buffer_repulsion(
                            building_id, other_id
                        )
                        force_x += fx * self.force_weights["road_buffer_repulsion"]
                        force_y += fy * self.force_weights["road_buffer_repulsion"]

                # Water body repulsion
                if self.water_source:
                    for other_id in conflicts:
                        if isinstance(other_id, str) and other_id.startswith("water_"):
                            fx, fy = self.calculate_water_body_repulsion(
                                building_id, other_id
                            )
                            force_x += fx * self.force_weights["water_body_repulsion"]
                            force_y += fy * self.force_weights["water_body_repulsion"]

                # Position preservation
                fx, fy = self.calculate_position_preservation(building_id)
                force_x += fx * self.force_weights["position_preservation"]
                force_y += fy * self.force_weights["position_preservation"]

                # Block containment
                fx, fy = self.calculate_block_containment(building_id)
                force_x += fx * self.force_weights["block_containment"]
                force_y += fy * self.force_weights["block_containment"]

                # Apply force scaling
                force_x *= force_scale
                force_y *= force_scale

                # Limit maximum displacement per iteration
                magnitude = math.sqrt(force_x * force_x + force_y * force_y)
                if magnitude > self.max_force_magnitude:
                    scaling = self.max_force_magnitude / magnitude
                    force_x *= scaling
                    force_y *= scaling

                return building_id, (force_x, force_y)

            # Calculate forces for all buildings
            building_ids = list(self.buildings.keys())

            forces = {}
            if self.use_parallel and len(building_ids) > 100:
                # Use parallel processing for large datasets
                with ThreadPoolExecutor() as executor:
                    for building_id, force in executor.map(
                        calculate_forces, building_ids
                    ):
                        forces[building_id] = force
            else:
                # Sequential processing for smaller datasets
                for building_id in building_ids:
                    if feedback.isCanceled():
                        break
                    building_id, force = calculate_forces(building_id)
                    forces[building_id] = force

            # Apply displacements and update geometries
            max_displacement_this_iter = 0

            for building_id, (force_x, force_y) in forces.items():
                # Skip buildings with no force
                if force_x == 0 and force_y == 0:
                    continue

                building = self.buildings[building_id]

                # Skip isolated buildings (redundant check, but added for safety)
                if self.graph.nodes[building_id].get("isolated", False):
                    continue

                # Get current center
                center = building["center"]

                # Apply displacement
                new_x = center.x() + force_x
                new_y = center.y() + force_y

                # Limit total displacement to max_displacement
                original_center = building["original_center"]
                dx = new_x - original_center.x
                dy = new_y - original_center.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance > self.max_displacement:
                    scaling = self.max_displacement / distance
                    new_x = original_center.x + dx * scaling
                    new_y = original_center.y + dy * scaling

                # Check displacement magnitude for this iteration
                iter_displacement = math.sqrt(force_x**2 + force_y**2)
                max_displacement_this_iter = max(
                    max_displacement_this_iter, iter_displacement
                )

                # Update building center
                building["center"] = QgsPointXY(new_x, new_y)

                # Recreate rotated square polygon at new position
                building["polygon"] = self.create_rotated_square(
                    new_x, new_y, self.symbol_size, building["rotation"]
                )

                # Update graph node
                self.graph.nodes[building_id]["center"] = QgsPointXY(new_x, new_y)
                self.graph.nodes[building_id]["polygon"] = building["polygon"]

            # Update conflict status for all buildings
            self.update_conflict_status()

            # Count current conflicts
            current_conflicts = sum(
                1
                for building_id in self.buildings
                if len(self.graph.nodes[building_id]["conflicts"]) > 0
            )

            # Check for early termination
            if current_conflicts == 0:
                feedback.pushInfo(f"All conflicts resolved at iteration {iteration}")
                break

            # Check for convergence
            if max_displacement_this_iter < 0.01 and iteration > 10:
                feedback.pushInfo(
                    f"Convergence reached at iteration {iteration} "
                    f"(max displacement: {max_displacement_this_iter:.5f})"
                )
                break

        # Final conflict status
        final_conflicts = sum(
            1
            for building_id in self.buildings
            if len(self.graph.nodes[building_id]["conflicts"]) > 0
        )

        conflict_reduction = (
            (initially_conflicted - final_conflicts) / initially_conflicted * 100
            if initially_conflicted > 0
            else 100
        )

        feedback.pushInfo(
            f"Iterative resolution complete: {final_conflicts} buildings with conflicts "
            f"remaining ({conflict_reduction:.1f}% reduction)"
        )

        # Count how many isolated buildings remain unchanged
        isolated_count = sum(
            1
            for node_id, node_data in self.graph.nodes(data=True)
            if node_data.get("isolated", False)
        )
        feedback.pushInfo(
            f"Preserved {isolated_count} isolated buildings in their original positions with no rotation"
        )

    def check_building_outside_block(self, building_id):
        """Check if a building is outside its assigned block."""
        building = self.buildings.get(building_id)
        block_id = self.building_blocks.get(building_id)

        if building is None or block_id is None or block_id >= len(self.blocks):
            return False

        block = self.blocks[block_id]
        point = self.shapely['Point'](building["center"].x(), building["center"].y())

        return not block.contains(point)

    def update_conflict_status(self):
        """Update conflict status for all buildings in the graph."""
        # Reset conflicts
        for building_id in self.buildings:
            self.graph.nodes[building_id]["conflicts"] = set()

        # Check building-building overlaps
        for building_id, building in self.buildings.items():
            polygon = building["polygon"]
            center = building["center"]

            # Get potential overlapping buildings using spatial index
            search_rect = QgsRectangle(
                center.x() - self.symbol_size,
                center.y() - self.symbol_size,
                center.x() + self.symbol_size,
                center.y() + self.symbol_size,
            )
            potential_ids = self.spatial_index_buildings.intersects(search_rect)

            for other_id in potential_ids:
                # Skip self-comparison
                if building_id == other_id:
                    continue

                other_building = self.buildings.get(other_id)
                if not other_building:
                    continue

                other_polygon = other_building["polygon"]

                # Check for overlap
                if polygon.intersects(other_polygon):
                    overlap_area = polygon.intersection(other_polygon).area
                    if overlap_area > 0:
                        self.graph.nodes[building_id]["conflicts"].add(other_id)
                        self.graph.nodes[other_id]["conflicts"].add(building_id)

            # Check road buffer overlaps
            for road_id, road in self.roads.items():
                road_buffer = road["buffer"]

                # Check for overlap
                if polygon.intersects(road_buffer):
                    overlap_area = polygon.intersection(road_buffer).area
                    if overlap_area > 0:
                        road_node_id = f"road_{road_id}"
                        self.graph.nodes[building_id]["conflicts"].add(road_node_id)

            # Check water body overlaps
            if self.water_source:
                for water_id, water in self.water_bodies.items():
                    water_geometry = water["geometry"]

                    # Check for overlap
                    if polygon.intersects(water_geometry):
                        overlap_area = polygon.intersection(water_geometry).area
                        if overlap_area > 0:
                            water_node_id = f"water_{water_id}"
                            self.graph.nodes[building_id]["conflicts"].add(
                                water_node_id
                            )

    def phase6_visibility_resolution(self, feedback):
        """
        Phase 6: Visibility Resolution System
        - Develop conflict chain detection algorithm
        - Implement priority-based visibility assignment
        - Create final conflict check for road buffer overlaps
        - Implement special handling for unresolvable block constraints
        """
        import networkx as nx

        feedback.pushInfo("Resolving visibility for unresolvable conflicts...")

        # Count initial unresolved conflicts
        total_conflicts = sum(
            len(self.graph.nodes[building_id]["conflicts"])
            for building_id in self.buildings
        )
        total_buildings_with_conflicts = sum(
            1
            for building_id in self.buildings
            if len(self.graph.nodes[building_id]["conflicts"]) > 0
        )

        feedback.pushInfo(
            f"Remaining conflicts: {total_conflicts} conflicts among "
            f"{total_buildings_with_conflicts} buildings"
        )

        # Step 1: Mark buildings with road buffer conflicts as invisible
        road_conflict_count = 0

        for building_id in self.buildings:
            road_conflicts = [
                conflict_id
                for conflict_id in self.graph.nodes[building_id]["conflicts"]
                if isinstance(conflict_id, str) and conflict_id.startswith("road_")
            ]

            if road_conflicts:
                self.buildings[building_id]["visibility"] = False
                self.graph.nodes[building_id]["visibility"] = False
                road_conflict_count += 1

        feedback.pushInfo(
            f"Marked {road_conflict_count} buildings with road conflicts as invisible"
        )

        # Step 2: Mark buildings with water body conflicts as invisible
        water_conflict_count = 0

        if self.water_source:
            for building_id in self.buildings:
                if not self.buildings[building_id]["visibility"]:
                    continue  # Skip already invisible buildings

                water_conflicts = [
                    conflict_id
                    for conflict_id in self.graph.nodes[building_id]["conflicts"]
                    if isinstance(conflict_id, str) and conflict_id.startswith("water_")
                ]

                if water_conflicts:
                    self.buildings[building_id]["visibility"] = False
                    self.graph.nodes[building_id]["visibility"] = False
                    water_conflict_count += 1

        feedback.pushInfo(
            f"Marked {water_conflict_count} buildings with water conflicts as invisible"
        )

        # Step 3: Resolve building-building conflicts based on importance
        building_conflict_count = 0

        # First, identify all building pairs with conflicts
        conflict_pairs = []

        for building_id in self.buildings:
            if not self.buildings[building_id]["visibility"]:
                continue  # Skip already invisible buildings

            building_conflicts = [
                conflict_id
                for conflict_id in self.graph.nodes[building_id]["conflicts"]
                if not isinstance(conflict_id, str)
                or not (
                    conflict_id.startswith("road_") or conflict_id.startswith("water_")
                )
            ]

            for other_id in building_conflicts:
                if building_id < other_id:  # Process each pair only once
                    conflict_pairs.append((building_id, other_id))

        # Sort conflict pairs by total importance (highest first)
        conflict_pairs.sort(
            key=lambda pair: self.buildings[pair[0]]["importance"]
            + self.buildings[pair[1]]["importance"],
            reverse=True,
        )

        # Resolve conflicts by making less important buildings invisible
        for building_id, other_id in conflict_pairs:
            # Skip if either building is already invisible
            if (
                not self.buildings[building_id]["visibility"]
                or not self.buildings[other_id]["visibility"]
            ):
                continue

            # Compare importance
            importance1 = self.buildings[building_id]["importance"]
            importance2 = self.buildings[other_id]["importance"]

            if importance1 > importance2:
                self.buildings[other_id]["visibility"] = False
                self.graph.nodes[other_id]["visibility"] = False
                building_conflict_count += 1
            else:
                self.buildings[building_id]["visibility"] = False
                self.graph.nodes[building_id]["visibility"] = False
                building_conflict_count += 1

        feedback.pushInfo(
            f"Resolved {building_conflict_count} building-building conflicts based on importance"
        )

        # Step 4: Resolve any remaining conflicts (conflict chains)
        # Identify connected components in conflict graph
        visible_buildings = [
            building_id
            for building_id in self.buildings
            if self.buildings[building_id]["visibility"]
        ]

        # Create subgraph of only visible buildings
        visible_graph = nx.Graph()

        for building_id in visible_buildings:
            visible_graph.add_node(
                building_id, importance=self.buildings[building_id]["importance"]
            )

        for building_id in visible_buildings:
            conflicts = [
                conflict_id
                for conflict_id in self.graph.nodes[building_id]["conflicts"]
                if conflict_id in visible_buildings
                and (
                    not isinstance(conflict_id, str)
                    or not (
                        conflict_id.startswith("road_")
                        or conflict_id.startswith("water_")
                    )
                )
            ]

            for other_id in conflicts:
                visible_graph.add_edge(building_id, other_id)

        # Find connected components (conflict chains)
        connected_components = list(nx.connected_components(visible_graph))

        chain_resolution_count = 0

        for component in connected_components:
            if len(component) <= 1:
                continue  # No conflicts in single-node components

            # Keep only the most important building in each chain
            most_important = max(
                component,
                key=lambda building_id: self.buildings[building_id]["importance"],
            )

            for building_id in component:
                if building_id != most_important:
                    self.buildings[building_id]["visibility"] = False
                    self.graph.nodes[building_id]["visibility"] = False
                    chain_resolution_count += 1

        feedback.pushInfo(
            f"Resolved {chain_resolution_count} buildings in conflict chains"
        )

        # Step 5: Final check for any remaining road conflicts
        final_check_count = 0

        for building_id in self.buildings:
            if not self.buildings[building_id]["visibility"]:
                continue  # Skip already invisible buildings

            road_conflicts = [
                conflict_id
                for conflict_id in self.graph.nodes[building_id]["conflicts"]
                if isinstance(conflict_id, str) and conflict_id.startswith("road_")
            ]

            if road_conflicts:
                self.buildings[building_id]["visibility"] = False
                self.graph.nodes[building_id]["visibility"] = False
                final_check_count += 1

        feedback.pushInfo(
            f"Final check: marked {final_check_count} more buildings as invisible"
        )

        # Count final visibility statistics
        visible_count = sum(
            1
            for building_id in self.buildings
            if self.buildings[building_id]["visibility"]
        )
        invisible_count = len(self.buildings) - visible_count

        visibility_percentage = (
            (visible_count / len(self.buildings)) * 100 if self.buildings else 0
        )

        feedback.pushInfo(
            f"Visibility resolution complete: {visible_count} visible, "
            f"{invisible_count} invisible ({visibility_percentage:.1f}% visible)"
        )

    def phase7_output_generation(self, feedback):
        """
        Phase 7: Output Generation and Visualization
        - Extract final center points from rotated square polygons
        - Generate final rotation values from polygon geometry
        - Update source feature attributes and geometry
        - Create optional visualization layer for debugging
        - Generate statistics for optimization effectiveness
        """
        feedback.pushInfo("Generating output features...")

        # Prepare statistics
        total_buildings = len(self.buildings)
        visible_buildings = sum(
            1 for building in self.buildings.values() if building["visibility"]
        )
        avg_displacement = 0
        max_displacement = 0

        # Write features to output sink
        total = 100.0 / total_buildings if total_buildings > 0 else 0

        for current, (building_id, building) in enumerate(self.buildings.items()):
            if feedback.isCanceled():
                break

            # Create output feature
            feature = QgsFeature(building["feature"])

            # Update geometry (center point)
            center = building["center"]
            output_geometry = QgsGeometry.fromPointXY(center)
            feature.setGeometry(output_geometry)

            # Update attributes
            feature[self.rotation_field] = building["rotation"]
            feature[self.visibility_field] = building["visibility"]

            # Calculate displacement
            original_center = building["original_center"]
            displacement = math.sqrt(
                (center.x() - original_center.x) ** 2
                + (center.y() - original_center.y) ** 2
            )

            # Update statistics
            if building["visibility"]:
                avg_displacement += displacement
                max_displacement = max(max_displacement, displacement)

            # Add to sink
            self.sink.addFeature(feature, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))

        # Calculate final statistics
        if visible_buildings > 0:
            avg_displacement /= visible_buildings

        # Report statistics
        feedback.pushInfo("\nFinal Statistics:")
        feedback.pushInfo(f"Total buildings: {total_buildings}")
        feedback.pushInfo(
            f"Visible buildings: {visible_buildings} ({visible_buildings/total_buildings*100:.1f}%)"
        )
        feedback.pushInfo(f"Average displacement: {avg_displacement:.2f} map units")
        feedback.pushInfo(f"Maximum displacement: {max_displacement:.2f} map units")

        feedback.pushInfo("\nBuilding Generalization completed successfully!")
