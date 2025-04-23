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
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsWkbTypes,
    QgsVectorLayer
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class AnchoredSnapperAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    LINE_ANCHOR_LAYERS = "LINE_ANCHOR_LAYERS"
    POLYGON_ANCHOR_LAYERS = "POLYGON_ANCHOR_LAYERS"
    ANCHOR_SELECTED = "ANCHOR_SELECTED"  # New parameter for anchor layers selection
    TOLERANCE = "TOLERANCE"
    BEHAVIOR = "BEHAVIOR"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer to be snapped"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features from input layer")
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_ANCHOR_LAYERS,
                self.tr("Line anchor layers"),
                QgsProcessing.TypeVectorLine,
                optional=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGON_ANCHOR_LAYERS,
                self.tr("Polygon anchor layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True
            )
        )
        
        # New parameter for anchor layers selected features
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ANCHOR_SELECTED, 
                self.tr("Process only selected features from anchor layers"),
                defaultValue=False
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
            self.tr("Snap to anchor nodes (single layer only)"),
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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        layerHandler = LayerHandler()
        
        # Get parameters
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        anchorOnlySelected = self.parameterAsBool(parameters, self.ANCHOR_SELECTED, context)
        
        # Get anchor layers
        lineAnchorLayers = self.parameterAsLayerList(parameters, self.LINE_ANCHOR_LAYERS, context)
        polygonAnchorLayers = self.parameterAsLayerList(parameters, self.POLYGON_ANCHOR_LAYERS, context)
        
        if not lineAnchorLayers and not polygonAnchorLayers:
            raise QgsProcessingException(
                self.tr("You must provide at least one anchor layer (line or polygon)")
            )
        
        snapTolerance = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        geographicBoundaryLyr = self.parameterAsVectorLayer(parameters, self.GEOGRAPHIC_BOUNDARY, context)
        
        # Setup progress feedback
        totalSteps = 8  # Updated step count 
        multiStepFeedback = QgsProcessingMultiStepFeedback(totalSteps, feedback)
        currentStep = 0
        
        # Step 1: Create aux structure for input layer
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating auxiliary structure for input layer..."))
        
        inputLyrList = [inputLyr]
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        
        # Step 2: Create spatial index for auxiliary layer
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index for input layer..."))
        algRunner.runCreateSpatialIndex(
            auxLyr, context, multiStepFeedback, is_child_algorithm=True
        )
        currentStep += 1
        
        # Step 3: Prepare anchor layers - handle selected features if necessary
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Preparing anchor layers..."))
        
        # Process line anchor layers - special handling for selection
        processed_lineAnchorLayers = []
        for lyr in lineAnchorLayers:
            if anchorOnlySelected and lyr.selectedFeatureCount() > 0:
                # Save selected features to a temporary layer
                temp_lyr = algRunner.runSaveSelectedFeatures(
                    lyr, context, feedback=multiStepFeedback
                )
                processed_lineAnchorLayers.append(temp_lyr)
            else:
                processed_lineAnchorLayers.append(lyr)
        
        # Process polygon anchor layers - special handling for selection
        processed_polygonAnchorLayers = []
        for lyr in polygonAnchorLayers:
            if anchorOnlySelected and lyr.selectedFeatureCount() > 0:
                # Save selected features to a temporary layer
                temp_lyr = algRunner.runSaveSelectedFeatures(
                    lyr, context, feedback=multiStepFeedback
                )
                processed_polygonAnchorLayers.append(temp_lyr)
            else:
                processed_polygonAnchorLayers.append(lyr)
        currentStep += 1
        
        # Step 4: Convert polygons to lines
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Converting polygons to lines..."))
        
        polygon_line_layers = []
        for poly_lyr in processed_polygonAnchorLayers:
            line_lyr = algRunner.runPolygonsToLines(
                poly_lyr, context, feedback=multiStepFeedback, is_child_algorithm=True
            )
            polygon_line_layers.append(line_lyr)
        currentStep += 1
        
        # Step 5: Merge all line layers
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Merging all line layers..."))
        
        all_line_layers = processed_lineAnchorLayers + polygon_line_layers
        if not all_line_layers:
            raise QgsProcessingException(
                self.tr("No valid anchor layers to process")
            )
            
        mergedAnchorLayer = algRunner.runMergeVectorLayers(
            all_line_layers, context, feedback=multiStepFeedback
        )
        currentStep += 1
        
        # Step 6: Convert lines to single parts (without exploding)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Converting lines to single parts..."))
        
        singlePartLines = algRunner.runMultipartToSingleParts(
            mergedAnchorLayer, context, feedback=multiStepFeedback
        )
        currentStep += 1
        
        # Step 7: Create spatial index on merged layer
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating spatial index on anchor layer..."))
        
        algRunner.runCreateSpatialIndex(
            singlePartLines, context, multiStepFeedback, is_child_algorithm=True
        )
        currentStep += 1
        
        # Step 8: Run snap operation using algRunner
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Running snap operation..."))
        
        snappedLyrOutput = algRunner.runSnapLayerOnLayer(
            inputLayer=auxLyr,
            referenceLayer=singlePartLines,
            tol=snapTolerance,
            behavior=behavior,
            context=context,
            onlySelected=False,  # We already handled selection
            feedback=multiStepFeedback,
            buildCache=False,
            is_child_algorithm=True
        )
        
        # Step 9: Add unshared vertices on intersections and shared edges
        multiStepFeedback.setProgressText(self.tr("Adding unshared vertices on intersections and shared edges..."))
        
        # Determine primitives to use in addUnsharedVertexOnSharedEdges
        primitiveDict = {
            QgsWkbTypes.PointGeometry: [],
            QgsWkbTypes.LineGeometry: [],
            QgsWkbTypes.PolygonGeometry: [],
        }
        
        # Add snapped layer to appropriate dict entry
        primitiveDict[snappedLyrOutput.geometryType()].append(snappedLyrOutput)
        
        # Add anchor layer to line dict
        primitiveDict[QgsWkbTypes.LineGeometry].append(singlePartLines)
        
        # Run the add unshared vertex algorithm
        if primitiveDict[QgsWkbTypes.LineGeometry]:
            algRunner.runAddUnsharedVertexOnSharedEdges(
                inputLinesList=primitiveDict[QgsWkbTypes.LineGeometry],
                inputPolygonsList=primitiveDict[QgsWkbTypes.PolygonGeometry],
                searchRadius=snapTolerance,
                selected=False,  # We already handled selection above
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True
            )
        
        # Step 10: Update original layers
        multiStepFeedback.setProgressText(self.tr("Updating original layers..."))
        
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, 
            auxLyr,  # Use the original auxLyr as it was modified in place
            feedback=multiStepFeedback, 
            onlySelected=onlySelected
        )
        
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
