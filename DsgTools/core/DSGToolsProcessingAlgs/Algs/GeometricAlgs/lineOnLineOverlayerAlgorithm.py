# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-05-23
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
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsFeature,
    QgsFields,
    QgsProcessingException,
    QgsFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsWkbTypes,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class LineOnLineOverlayerAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm that splits input lines at intersections with reference lines.
    It also ensures that intersection points are added as vertices to reference lines
    if they don't already exist there.
    """

    INPUT = "INPUT"
    REFERENCE_LINES = "REFERENCE_LINES"
    SNAP_TOLERANCE = "SNAP_TOLERANCE"
    OUTPUT_SPLIT_LINES = "OUTPUT_SPLIT_LINES"
    OUTPUT_MODIFIED_REFERENCES = "OUTPUT_MODIFIED_REFERENCES"

    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm.
        """
        # Add the input line features source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input line layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        # Add the reference line layers parameter
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.REFERENCE_LINES,
                self.tr("Reference line layers"),
                QgsProcessing.TypeVectorLine,
            )
        )

        # Add snap tolerance parameter for vertex insertion
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SNAP_TOLERANCE,
                self.tr("Snap tolerance for vertex insertion"),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.001,
                minValue=0.0,
                optional=True,
            )
        )

        # Add the output parameter for split lines
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_SPLIT_LINES, self.tr("Split input lines")
            )
        )

        # Add the output parameter for modified reference lines
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_MODIFIED_REFERENCES, self.tr("Modified reference lines")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Initialize algRunner for processing operations
        algRunner = AlgRunner()

        # Retrieve the feature sources
        input_line_source = self.parameterAsSource(parameters, self.INPUT, context)

        # Get reference line layers
        reference_line_layers = self.parameterAsLayerList(
            parameters, self.REFERENCE_LINES, context
        )

        # Get snap tolerance
        snap_tolerance = self.parameterAsDouble(
            parameters, self.SNAP_TOLERANCE, context
        )

        # Create output sinks
        (split_lines_sink, split_lines_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_SPLIT_LINES,
            context,
            input_line_source.fields(),
            input_line_source.wkbType(),
            input_line_source.sourceCrs(),
        )

        # For reference lines, we'll use the fields from the first reference layer

        # Check if inputs are valid
        if input_line_source is None:
            raise QgsProcessingException(self.tr("Invalid input line layer"))

        if not reference_line_layers:
            raise QgsProcessingException(
                self.tr("At least one reference line layer is required")
            )

        # Define total processing steps
        total_steps = 10
        multiStepFeedback = QgsProcessingMultiStepFeedback(total_steps, feedback)
        current_step = 0

        multiStepFeedback.pushInfo("Starting line-on-line overlay algorithm...")

        # Step 1: Merge all reference line layers into one
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Merging reference line layers...".format(
                current_step + 1, total_steps
            )
        )

        merged_reference_lines = (
            algRunner.runMergeVectorLayers(
                reference_line_layers,
                context,
                feedback=multiStepFeedback,
                crs=input_line_source.sourceCrs(),
            )
            if len(reference_line_layers) > 1
            else reference_line_layers[0]
        )
        outputFields = merged_reference_lines.fields()
        (modified_refs_sink, modified_refs_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_MODIFIED_REFERENCES,
            context,
            outputFields,
            QgsWkbTypes.LineString,
            input_line_source.sourceCrs(),
        )
        current_step += 1

        # Step 2: Create spatial indexes for better performance
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Creating spatial indexes...".format(
                current_step + 1, total_steps
            )
        )

        algRunner.runCreateSpatialIndex(
            parameters[self.INPUT], context, feedback=multiStepFeedback
        )
        algRunner.runCreateSpatialIndex(
            merged_reference_lines, context, feedback=multiStepFeedback
        )
        current_step += 1

        # Step 3: Find intersection points between input lines and reference lines
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Finding line intersections...".format(
                current_step + 1, total_steps
            )
        )

        intersection_points = algRunner.runLineIntersections(
            parameters[self.INPUT],
            merged_reference_lines,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        current_step += 1

        # Step 4: Split input lines at intersection points
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Splitting input lines at intersections...".format(
                current_step + 1, total_steps
            )
        )

        snapped_initial_lines = algRunner.runSnapGeometriesToLayer(
            parameters[self.INPUT],
            intersection_points,
            snap_tolerance,
            context,
            feedback=multiStepFeedback,
            behavior=AlgRunner.AlignNodesDoNotInsertNewVertices,
        )
        current_step += 1
        multiStepFeedback.setCurrentStep(current_step)

        self_split_lines = algRunner.runSplitLinesWithLines(
            snapped_initial_lines,
            snapped_initial_lines,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        current_step += 1
        multiStepFeedback.setCurrentStep(current_step)

        split_input_lines = algRunner.runSplitLinesWithLines(
            self_split_lines,
            merged_reference_lines,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        current_step += 1

        # Step 5: Convert split lines to single parts (in case multipart geometries were created)
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Converting to single part geometries...".format(
                current_step + 1, total_steps
            )
        )

        single_part_lines = algRunner.runMultipartToSingleParts(
            split_input_lines,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        current_step += 1

        # Step 6: Snap intersection points to reference lines to add vertices
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Adding intersection vertices to reference lines...".format(
                current_step + 1, total_steps
            )
        )

        # This operation modifies the reference lines by adding vertices at intersection points
        modified_reference_lines = algRunner.runSnapGeometriesToLayer(
            merged_reference_lines,
            intersection_points,
            snap_tolerance,
            context,
            feedback=multiStepFeedback,
            behavior=AlgRunner.AlignNodesInsertExtraVerticesWhereRequired,  # Prefer aligning nodes, insert extra vertices where required
        )
        current_step += 1

        # Step 7: Clean and prepare the split input lines
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Cleaning split lines...".format(current_step + 1, total_steps)
        )

        # Remove any null geometries that might have been created during processing
        cleaned_split_lines = algRunner.runRemoveNull(
            single_part_lines,
            context,
            feedback=multiStepFeedback,
        )
        current_step += 1

        # Step 8: Output the results
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo(
            "Step {}/{}: Writing output features...".format(
                current_step + 1, total_steps
            )
        )

        # Function to output split line features with filtered attributes
        def outputSplitLineFeature(feat):
            split_lines_sink.addFeature(feat, QgsFeatureSink.FastInsert)

        # Function to output modified reference line features
        def outputModifiedReferenceFeature(feat):
            modified_refs_sink.addFeature(feat, QgsFeatureSink.FastInsert)

        # Write split input lines to output
        list(map(outputSplitLineFeature, cleaned_split_lines.getFeatures()))

        # Write modified reference lines to output
        list(
            map(outputModifiedReferenceFeature, modified_reference_lines.getFeatures())
        )

        multiStepFeedback.pushInfo(
            "Line-on-line overlay algorithm completed successfully!"
        )

        return {
            self.OUTPUT_SPLIT_LINES: split_lines_dest_id,
            self.OUTPUT_MODIFIED_REFERENCES: modified_refs_dest_id,
        }

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("LineOnLineOverlayerAlgorithm", string)

    def createInstance(self):
        return LineOnLineOverlayerAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return "lineonlineoverlayer"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr(
            "Line on Line Overlayer"
        )

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return "DSGTools - Geometric Algorithms"

    def shortHelpString(self):
        """
        Returns a short helper string for the algorithm.
        """
        return self.tr(
            "This algorithm splits input lines at every intersection with reference lines "
            "and ensures that intersection points are added as vertices to reference lines. "
            "It preserves the original attributes from the input lines in the split output."
        )
