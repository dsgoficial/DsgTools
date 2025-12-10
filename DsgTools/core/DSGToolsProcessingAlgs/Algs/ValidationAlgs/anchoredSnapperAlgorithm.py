# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-04-23
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
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsWkbTypes,
    QgsVectorLayer,
    QgsProcessingParameterVectorLayer,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class AnchoredSnapperAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    POINT_ANCHOR_LAYERS = "POINT_ANCHOR_LAYERS"
    LINE_ANCHOR_LAYERS = "LINE_ANCHOR_LAYERS"
    POLYGON_ANCHOR_LAYERS = "POLYGON_ANCHOR_LAYERS"
    ANCHOR_SELECTED = "ANCHOR_SELECTED"
    TOLERANCE = "TOLERANCE"
    BEHAVIOR = "BEHAVIOR"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT,
                self.tr("Input layers to be snapped"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr("Process only selected features from input layers"),
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POINT_ANCHOR_LAYERS,
                self.tr("Point anchor layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_ANCHOR_LAYERS,
                self.tr("Line anchor layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGON_ANCHOR_LAYERS,
                self.tr("Polygon anchor layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ANCHOR_SELECTED,
                self.tr("Process only selected features from anchor layers"),
                defaultValue=False,
            )
        )

        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Snap Tolerance"),
            parentParameterName=self.INPUT,
            defaultValue=1.0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

        self.modes = [
            self.tr("Prefer aligning nodes, insert extra vertices where required"),
            self.tr("Prefer closest point, insert extra vertices where required"),
            self.tr("Prefer aligning nodes, don't insert new vertices"),
            self.tr("Prefer closest point, don't insert new vertices"),
            self.tr("Move end points only, prefer aligning nodes"),
            self.tr("Move end points only, prefer closest point"),
            self.tr("Snap end points to end points only"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR, self.tr("Behavior"), options=self.modes, defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

    def groupLayersByGeometryType(self, layers):
        """
        Group layers by their geometry type.
        Returns a dictionary with geometry types as keys and lists of layers as values.
        """
        grouped = {
            QgsWkbTypes.PointGeometry: [],
            QgsWkbTypes.LineGeometry: [],
            QgsWkbTypes.PolygonGeometry: [],
        }
        
        for layer in layers:
            geomType = layer.geometryType()
            if geomType in grouped:
                grouped[geomType].append(layer)
        
        return grouped

    def prepareAnchorLayers(self, pointAnchorLayers, lineAnchorLayers, polygonAnchorLayers, 
                           anchorOnlySelected, algRunner, context, feedback):
        """
        Prepare anchor layers: handle selection and convert polygons to lines.
        Returns merged and indexed anchor layers for lines and points.
        """
        # Process point anchor layers
        processed_pointAnchorLayers = []
        for lyr in pointAnchorLayers:
            if anchorOnlySelected and lyr.selectedFeatureCount() > 0:
                temp_lyr = algRunner.runSaveSelectedFeatures(
                    lyr, context, feedback=feedback
                )
                processed_pointAnchorLayers.append(temp_lyr)
            else:
                processed_pointAnchorLayers.append(lyr)

        # Process line anchor layers
        processed_lineAnchorLayers = []
        for lyr in lineAnchorLayers:
            if anchorOnlySelected and lyr.selectedFeatureCount() > 0:
                temp_lyr = algRunner.runSaveSelectedFeatures(
                    lyr, context, feedback=feedback
                )
                processed_lineAnchorLayers.append(temp_lyr)
            else:
                processed_lineAnchorLayers.append(lyr)

        # Process polygon anchor layers
        processed_polygonAnchorLayers = []
        for lyr in polygonAnchorLayers:
            if anchorOnlySelected and lyr.selectedFeatureCount() > 0:
                temp_lyr = algRunner.runSaveSelectedFeatures(
                    lyr, context, feedback=feedback
                )
                processed_polygonAnchorLayers.append(temp_lyr)
            else:
                processed_polygonAnchorLayers.append(lyr)

        # Convert polygons to lines
        polygon_line_layers = []
        for poly_lyr in processed_polygonAnchorLayers:
            line_lyr = algRunner.runPolygonsToLines(
                poly_lyr, context, feedback=feedback, is_child_algorithm=True
            )
            polygon_line_layers.append(line_lyr)

        # Merge and prepare line anchors
        mergedLineAnchor = None
        all_line_layers = processed_lineAnchorLayers + polygon_line_layers
        if all_line_layers:
            mergedLineAnchor = algRunner.runMergeVectorLayers(
                all_line_layers, context, feedback=feedback
            )
            singlePartLines = algRunner.runMultipartToSingleParts(
                mergedLineAnchor, context, feedback=feedback
            )
            algRunner.runCreateSpatialIndex(
                singlePartLines, context, feedback, is_child_algorithm=True
            )
            mergedLineAnchor = singlePartLines

        # Merge and prepare point anchors
        mergedPointAnchor = None
        if processed_pointAnchorLayers:
            mergedPointAnchor = algRunner.runMergeVectorLayers(
                processed_pointAnchorLayers, context, feedback=feedback
            )
            singlePartPoints = algRunner.runMultipartToSingleParts(
                mergedPointAnchor, context, feedback=feedback
            )
            algRunner.runCreateSpatialIndex(
                singlePartPoints, context, feedback, is_child_algorithm=True
            )
            mergedPointAnchor = singlePartPoints

        return mergedLineAnchor, mergedPointAnchor

    def processGeometryGroup(self, inputLayers, mergedLineAnchor, mergedPointAnchor,
                            snapTolerance, behavior, onlySelected, algRunner, 
                            layerHandler, context, feedback):
        """
        Process a group of layers with the same geometry type.
        """
        if not inputLayers:
            return

        geomType = inputLayers[0].wkbType()
        
        feedback.pushInfo(
            self.tr(f"Processing {len(inputLayers)} layer(s) of type {QgsWkbTypes.displayString(geomType)}...")
        )

        # Create aux structure for input layers
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLayers,
            geomType=geomType,
            onlySelected=onlySelected,
            feedback=feedback,
        )

        # Create spatial index
        algRunner.runCreateSpatialIndex(
            auxLyr, context, feedback, is_child_algorithm=True
        )

        # Snap to line anchors if available
        snappedLyr = auxLyr
        if mergedLineAnchor:
            snappedLyr = algRunner.runSnapLayerOnLayer(
                inputLayer=snappedLyr,
                referenceLayer=mergedLineAnchor,
                tol=snapTolerance,
                behavior=behavior,
                context=context,
                onlySelected=False,
                feedback=feedback,
                buildCache=False,
                is_child_algorithm=True,
            )

        # Snap to point anchors if available
        if mergedPointAnchor:
            snappedLyr = algRunner.runSnapLayerOnLayer(
                inputLayer=snappedLyr,
                referenceLayer=mergedPointAnchor,
                tol=snapTolerance,
                behavior=behavior,
                context=context,
                onlySelected=False,
                feedback=feedback,
                buildCache=False,
                is_child_algorithm=True,
            )

        # Add unshared vertices for line and polygon geometries
        # if geomType in [QgsWkbTypes.LineGeometry, QgsWkbTypes.PolygonGeometry]:
        #     primitiveDict = {
        #         QgsWkbTypes.PointGeometry: [],
        #         QgsWkbTypes.LineGeometry: [],
        #         QgsWkbTypes.PolygonGeometry: [],
        #     }

        #     primitiveDict[snappedLyr.geometryType()].append(snappedLyr)
            
        #     if mergedLineAnchor:
        #         primitiveDict[QgsWkbTypes.LineGeometry].append(mergedLineAnchor)

        #     if primitiveDict[QgsWkbTypes.LineGeometry]:
        #         algRunner.runAddUnsharedVertexOnSharedEdges(
        #             inputLinesList=primitiveDict[QgsWkbTypes.LineGeometry],
        #             inputPolygonsList=primitiveDict[QgsWkbTypes.PolygonGeometry],
        #             searchRadius=snapTolerance,
        #             selected=False,
        #             context=context,
        #             feedback=feedback,
        #             is_child_algorithm=True,
        #         )

        # Update original layers
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLayers,
            auxLyr,
            feedback=feedback,
            onlySelected=onlySelected,
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        layerHandler = LayerHandler()

        # Get parameters
        inputLayers = self.parameterAsLayerList(parameters, self.INPUT, context)
        if not inputLayers:
            raise QgsProcessingException(
                self.tr("You must provide at least one input layer")
            )

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        anchorOnlySelected = self.parameterAsBool(
            parameters, self.ANCHOR_SELECTED, context
        )

        # Get anchor layers
        pointAnchorLayers = self.parameterAsLayerList(
            parameters, self.POINT_ANCHOR_LAYERS, context
        )
        lineAnchorLayers = self.parameterAsLayerList(
            parameters, self.LINE_ANCHOR_LAYERS, context
        )
        polygonAnchorLayers = self.parameterAsLayerList(
            parameters, self.POLYGON_ANCHOR_LAYERS, context
        )

        if not pointAnchorLayers and not lineAnchorLayers and not polygonAnchorLayers:
            raise QgsProcessingException(
                self.tr("You must provide at least one anchor layer (point, line or polygon)")
            )

        snapTolerance = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        geographicBoundaryLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )

        # Group input layers by geometry type
        groupedLayers = self.groupLayersByGeometryType(inputLayers)
        
        # Count non-empty groups
        activeGroups = sum(1 for layers in groupedLayers.values() if layers)
        
        # Setup progress feedback
        totalSteps = 1 + (activeGroups * 2)  # Prepare anchors + (process + update) per group
        multiStepFeedback = QgsProcessingMultiStepFeedback(totalSteps, feedback)
        currentStep = 0

        # Prepare anchor layers (only once for all groups)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing anchor layers..."))
        
        mergedLineAnchor, mergedPointAnchor = self.prepareAnchorLayers(
            pointAnchorLayers,
            lineAnchorLayers,
            polygonAnchorLayers,
            anchorOnlySelected,
            algRunner,
            context,
            multiStepFeedback,
        )
        
        if not mergedLineAnchor and not mergedPointAnchor:
            raise QgsProcessingException(
                self.tr("No valid anchor layers to process")
            )
        
        currentStep += 1

        # Process each geometry type group
        for geomType, layers in groupedLayers.items():
            if not layers:
                continue
            
            multiStepFeedback.setCurrentStep(currentStep)
            geomTypeName = QgsWkbTypes.displayString(geomType)
            multiStepFeedback.setProgressText(
                self.tr(f"Processing {geomTypeName} layers...")
            )
            
            self.processGeometryGroup(
                layers,
                mergedLineAnchor,
                mergedPointAnchor,
                snapTolerance,
                behavior,
                onlySelected,
                algRunner,
                layerHandler,
                context,
                multiStepFeedback,
            )
            
            currentStep += 1

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "anchoredsnapper"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Anchored Snapper")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Snap Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Snap Processes"

    def tr(self, string):
        return QCoreApplication.translate("AnchoredSnapperAlgorithm", string)

    def createInstance(self):
        return AnchoredSnapperAlgorithm()
