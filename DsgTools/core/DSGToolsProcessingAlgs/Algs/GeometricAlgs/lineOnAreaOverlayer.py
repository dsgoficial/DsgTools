# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-28
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
 ********
 """

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
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
                       QgsProcessingMultiStepFeedback)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class LineOnAreaOverlayerAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm splits polygons with overlay lines and preserves attributes.
    Uses DsgTools algRunner for processing execution.
    Implements line elimination for small polygons.
    Optimized with spatial indexes for better performance.
    """

    # Constants used to refer to parameters and outputs
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    OVERLAY_LINES = 'OVERLAY_LINES'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    MIN_AREA = 'MIN_AREA'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm.
        """
        # Add the input polygon features source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_POLYGONS,
                self.tr('Input polygon layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        # Add the overlay line layers parameter
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.OVERLAY_LINES,
                self.tr('Overlay line layers'),
                QgsProcessing.TypeVectorLine
            )
        )

        # Add the attribute blacklist parameter
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT_POLYGONS",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )

        # Add the minimum area parameter
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_AREA,
                self.tr('Minimum area (in square meters)'),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.0,
                optional=True,
                minValue=0.0
            )
        )

        # Add the output parameter
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Split polygons')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Initialize algRunner
        algRunner = AlgRunner()
        
        self.POLYGON_SOURCE_ID = 'original_polygon'
        self.OVERLAY_SOURCE_ID = 'overlay_line'
        
        # Retrieve the feature sources
        polygon_source = self.parameterAsSource(
            parameters,
            self.INPUT_POLYGONS,
            context
        )
        
        # Get overlay line layers
        overlay_line_layers = self.parameterAsLayerList(
            parameters,
            self.OVERLAY_LINES,
            context
        )

        # Get attribute blacklist
        attr_blacklist = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        
        # Get minimum area parameter
        min_area = self.parameterAsDouble(
            parameters,
            self.MIN_AREA,
            context
        )
        
        outputFields = QgsFields()
        for field in polygon_source.fields():
            if field.name() in attr_blacklist:
                continue
            outputFields.append(field)
        (output_sink, output_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outputFields,
            polygon_source.wkbType(),
            polygon_source.sourceCrs(),
        )
        
        # Check if inputs are valid
        if polygon_source is None:
            raise QgsProcessingException(self.tr('Invalid input polygon layer'))
        
        if not overlay_line_layers:
            raise QgsProcessingException(self.tr('At least one overlay line layer is required'))
        
        # Determine number of steps for feedback
        # Basic flow has 9 steps, plus extra steps for small polygon handling if min_area > 0
        total_steps = 9
        if min_area > 0:
            # Add 6 more steps for the small polygon handling
            total_steps += 6
        
        # Create multi-step feedback to track all processing steps
        multiStepFeedback = QgsProcessingMultiStepFeedback(total_steps, feedback)
        current_step = 0
            
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo('Starting polygon splitting algorithm...')
        
        # Step 1: Convert the original polygons to lines
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo('Step 1/{}:Converting polygons to lines...'.format(total_steps))
        polygon_lines_layer = algRunner.runPolygonsToLines(
            parameters[self.INPUT_POLYGONS], 
            context, 
            feedback=multiStepFeedback,
        )
        
        polygon_lines_layer.setName("original_polygon")
        multiStepFeedback.pushInfo('Merging overlay line layers...')
        overlay_lines_merged = algRunner.runMergeVectorLayers(
            [polygon_lines_layer] + overlay_line_layers,
            context,
            feedback=multiStepFeedback,
            crs=polygon_source.sourceCrs()
        )
        current_step += 1
        
        # Step 3: Split all lines with each other
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo('Step 3/{}:Splitting lines...'.format(total_steps))
        
        # First, merge polygon lines and overlay lines
        all_line_layers = [polygon_lines_layer]
        if overlay_lines_merged:
            all_line_layers.append(overlay_lines_merged)
        
        merged_lines_layer = algRunner.runMergeVectorLayers(
            all_line_layers,
            context,
            feedback=multiStepFeedback,
            crs=polygon_source.sourceCrs()
        )
        exploded_lines = algRunner.runExplodeLines(
            merged_lines_layer,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )
        current_step += 1
        
        # Step 4: First polygonize attempt
        multiStepFeedback.setCurrentStep(current_step)
        multiStepFeedback.pushInfo('Step 4/{}:Initial polygonization...'.format(total_steps))
        polygonized_layer = algRunner.runPolygonize(
            exploded_lines,
            context,
            keepFields=True,
            feedback=multiStepFeedback
        )
        current_step += 1
        multiStepFeedback.setCurrentStep(current_step)
        polygonized_layer = algRunner.runMultipartToSingleParts(
            inputLayer=polygonized_layer,
            context=context,
            feedback=multiStepFeedback
        )
        current_step += 1
        multiStepFeedback.setCurrentStep(current_step)
        polygonized_layer = algRunner.runCreateFieldWithExpression(
            inputLyr=polygonized_layer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        current_step += 1
        
        # Only proceed with line elimination if a minimum area is specified
        if min_area > 0:
            multiStepFeedback.setCurrentStep(current_step)
            multiStepFeedback.pushInfo('Step 5/{}:Calculating polygon areas...'.format(total_steps))
            area_layer = algRunner.runCreateFieldWithExpression(
                polygonized_layer,
                "$area",
                'area',
                context,
                fieldType=0,  # Decimal field type
                feedback=multiStepFeedback,
                is_child_algorithm=True
            )
            current_step += 1
            # Step 6: Identify small polygons
            multiStepFeedback.setCurrentStep(current_step)
            multiStepFeedback.pushInfo('Step 6/{}:Identifying polygons smaller than {}...'.format(total_steps, min_area))
            
            # Identify small polygons
            small_polygons_layer = algRunner.runFilterExpression(
                area_layer,
                f'"area" < {min_area}',
                context,
                feedback=multiStepFeedback,
            )
            current_step += 1
            
            # Check if we have any small polygons
            small_polygons_count = small_polygons_layer.featureCount()
            
            if small_polygons_count > 0:
                exploded_lines = algRunner.runCreateFieldWithExpression(
                    inputLyr=exploded_lines,
                    expression="$id",
                    fieldName="lfid",
                    fieldType=1,
                    context=context,
                    feedback=multiStepFeedback,
                )
                current_step += 1
                multiStepFeedback.pushInfo(f'Found {small_polygons_count} small polygons that need elimination')
                smallPolygonIds = [f["featid"] for f in small_polygons_layer.getFeatures()]
                multiStepFeedback.setCurrentStep(current_step)
                candidateLinesToBeRemoved = algRunner.runFilterExpression(
                    inputLyr=exploded_lines,
                    expression=f"'featid' in ({','.join(map(str, smallPolygonIds))})",
                    context=context,
                    feedback=multiStepFeedback,
                )
                current_step += 1
                multiStepFeedback.setCurrentStep(current_step)
                algRunner.runCreateSpatialIndex(candidateLinesToBeRemoved, context, multiStepFeedback)
                current_step += 1
                algRunner.runCreateSpatialIndex(
                    exploded_lines,
                    context,
                    feedback=multiStepFeedback
                )
                current_step += 1
                
                current_step += 1
                multiStepFeedback.setCurrentStep(current_step)
                allCandidateLinesToBeRemoved = algRunner.runExtractByLocation(
                    exploded_lines,
                    candidateLinesToBeRemoved,
                    context=context,
                    predicate=AlgRunner.Equals,
                    feedback=multiStepFeedback
                )
                lineIdsToBeRemoved = set(
                    f["lfid"] for f in allCandidateLinesToBeRemoved.getFeatures()
                )
                lineIdsToBeRemoved = lineIdsToBeRemoved.union(set(f["lfid"] for f in candidateLinesToBeRemoved.getFeatures()))
                cleaned_lines = algRunner.runFilterExpression(
                    exploded_lines,
                    expression=f"'lfid' not in ({','.join(map(str, lineIdsToBeRemoved))})",
                    context=context,
                    feedback=multiStepFeedback,
                    is_child_algorithm=True,
                )
                # Step 11: Re-run polygonize with the cleaned lines
                multiStepFeedback.setCurrentStep(current_step)
                multiStepFeedback.pushInfo('Step 11/{}:Re-running polygonize after line elimination...'.format(total_steps))
                polygonized_layer = algRunner.runPolygonize(
                    cleaned_lines,
                    context,
                    feedback=multiStepFeedback
                )
        else:
            # No minimum area specified, so no filtering
            multiStepFeedback.pushInfo('No minimum area specified, skipping line elimination')
        
        # Calculate what step we're on next (depends on whether min_area was > 0)
        next_step = min(current_step, total_steps - 3)
        multiStepFeedback.setCurrentStep(next_step)
        multiStepFeedback.pushInfo('Step {}/{}:Calculating point on surface...'.format(next_step + 1, total_steps))
        center_point_layer = algRunner.runPointOnSurface(
            polygonized_layer,
            context,
            allParts=True,  # Set to True to get a point for each part of multipolygons
            feedback=multiStepFeedback
        )
        next_step += 1
        
        multiStepFeedback.setCurrentStep(next_step)
        center_point_layer = algRunner.runMultipartToSingleParts(
            inputLayer=center_point_layer,
            context=context,
            feedback=multiStepFeedback
        )
        next_step += 1
        
        # Step: Join attributes from original polygons
        multiStepFeedback.setCurrentStep(next_step)
        multiStepFeedback.pushInfo('Step {}/{}:Joining attributes from original polygons...'.format(next_step + 1, total_steps))
        
        fields_to_keep = [field.name() for field in outputFields]
        
        # Create spatial indexes for better performance in spatial joins
        multiStepFeedback.pushInfo('Creating spatial indexes for final attribute joins...')
        algRunner.runCreateSpatialIndex(
            center_point_layer,
            context,
            feedback=multiStepFeedback
        )
        
        algRunner.runCreateSpatialIndex(
            parameters[self.INPUT_POLYGONS],
            context,
            feedback=multiStepFeedback
        )
        
        # Join attributes from original polygons to points using spatial relationship
        join_layer = algRunner.runJoinAttributesByLocation(
            center_point_layer,
            parameters[self.INPUT_POLYGONS],
            context,
            predicateList=[0],  # Within predicate
            joinFields=fields_to_keep,
            method=0,  # Take attributes from the first located feature
            discardNonMatching=False,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )
        next_step += 1
        
        # Final step: Spatial join back to the filtered polygons
        multiStepFeedback.setCurrentStep(next_step)
        multiStepFeedback.pushInfo('Step {}/{}:Final spatial join...'.format(next_step + 1, total_steps))
        
        # Create spatial indexes for better performance
        algRunner.runCreateSpatialIndex(
            polygonized_layer,
            context,
            feedback=multiStepFeedback
        )
        
        algRunner.runCreateSpatialIndex(
            join_layer,
            context,
            feedback=multiStepFeedback
        )
        
        final_result_lyr = algRunner.runJoinAttributesByLocation(
            polygonized_layer,
            join_layer,
            context,
            predicateList=[0],  # Contains predicate
            joinFields=fields_to_keep,
            method=0,  # Take attributes from the first located feature
            discardNonMatching=False,
            feedback=multiStepFeedback,
        )
        
        multiStepFeedback.pushInfo('Algorithm completed successfully!')
        def outputFeature(feat):
            newFeat = QgsFeature(outputFields)
            for field in outputFields:
                newFeat[field.name()] = feat[field.name()]
            newFeat.setGeometry(feat.geometry())
            output_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        list(map(outputFeature, final_result_lyr.getFeatures()))
        return {self.OUTPUT: output_dest_id}

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('LineOnAreaOverlayerAlgorithm', string)

    def createInstance(self):
        return LineOnAreaOverlayerAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'lineonareaoverlayer'

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr('Line on Area Overlayer')

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
        Returns a short helper string for the algorithm.
        """
        return self.tr('This algorithm splits polygons with overlay lines and preserves original attributes.')
