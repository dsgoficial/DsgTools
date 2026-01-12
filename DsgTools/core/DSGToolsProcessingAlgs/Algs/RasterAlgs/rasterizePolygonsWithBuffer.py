# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-07-17
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
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsRasterLayer,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class RasterizePolygonsWithBufferAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm that processes a list of polygon layers, performing merge, dissolve,
    negative buffer and rasterization over a base raster.
    """

    # Input parameters
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    INPUT_RASTER = 'INPUT_RASTER'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    NODATA_VALUE = 'NODATA_VALUE'
    OUTPUT_RASTER = 'OUTPUT_RASTER'

    def __init__(self):
        super().__init__()
        self.algRunner = AlgRunner()

    def tr(self, string):
        """
        Returns a translatable string with the Qt translation API.
        """
        return QCoreApplication.translate('RasterizePolygonsWithBufferAlgorithm', string)

    def createInstance(self):
        return RasterizePolygonsWithBufferAlgorithm()

    def name(self):
        return 'rasterizepolygonswithbuffer'

    def displayName(self):
        return self.tr('Rasterize Polygons with Buffer')

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            'This algorithm processes a list of polygon layers by executing:\n'
            '1. Merge of polygon layers\n'
            '2. Dissolve of merged polygons\n'
            '3. Negative buffer with specified radius\n'
            '4. Copy of input raster to output\n'
            '5. Rasterization with fixed value (nodata) over the copied raster\n\n'
            'Parameters:\n'
            '- Polygon Layers: List of polygon vector layers\n'
            '- Input Raster: Base raster for processing\n'
            '- Search Radius: Value for negative buffer (in map units)\n'
            '- NoData Value: Value to be used in rasterization (default: -9999)\n'
            '- Output Raster: Output raster file'
        )

    def initAlgorithm(self, config=None):
        """
        Define the input and output parameters of the algorithm.
        """
        # Parameter for multiple polygon layers
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                self.tr('Polygon Layers'),
                QgsProcessing.TypeVectorPolygon,
                optional=False
            )
        )

        # Parameter for input raster
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input Raster'),
                optional=False
            )
        )

        # Parameter for search radius
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr('Search Radius (Buffer)'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=-1e-4,
                optional=False
            )
        )

        # Parameter for nodata value
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NODATA_VALUE,
                self.tr('NoData Value'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=-9999,
                optional=False
            )
        )

        # Parameter for output raster
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output Raster'),
                optional=False
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Executes the processing algorithm.
        """
        # Get parameters
        polygon_layers = self.parameterAsLayerList(parameters, self.INPUT_POLYGONS, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        search_radius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        nodata_value = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        output_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        # Validations
        if not polygon_layers:
            raise QgsProcessingException(self.tr('No polygon layers provided'))

        if not input_raster:
            raise QgsProcessingException(self.tr('Input raster not provided'))

        # Setup multi-step feedback (5 steps)
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        
        multiStepFeedback.pushInfo(self.tr('Starting processing...'))

        # Step 1: Merge polygon layers
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Step 1/5: Merging polygon layers...'))
        
        merged_layer = self.algRunner.runMergeVectorLayers(
            inputList=polygon_layers,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )

        if multiStepFeedback.isCanceled():
            return {}

        # Step 2: Dissolve merged polygons
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Step 2/5: Dissolving polygons...'))
        
        dissolved_layer = self.algRunner.runDissolve(
            inputLyr=merged_layer,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )

        if multiStepFeedback.isCanceled():
            return {}

        # Step 3: Apply negative buffer
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr('Step 3/5: Applying buffer...'))
        
        buffered_layer = self.algRunner.runBuffer(
            inputLayer=dissolved_layer,
            distance=search_radius,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )

        if multiStepFeedback.isCanceled():
            return {}

        # Step 4: Copy input raster to output
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr('Step 4/5: Copying input raster to output...'))
        
        output_raster_result = self.algRunner.runGdalTranslate(
            inputRaster=input_raster,
            context=context,
            feedback=multiStepFeedback,
            outputRaster=output_raster,
            is_child_algorithm=True
        )

        if multiStepFeedback.isCanceled():
            return {}

        # Load the copied raster
        output_raster_layer = QgsRasterLayer(output_raster, "output_raster")
        if not output_raster_layer.isValid():
            raise QgsProcessingException(self.tr('Error loading output raster'))

        # Step 5: Rasterize with fixed value
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr('Step 5/5: Rasterizing polygons with fixed value...'))
        
        self.algRunner.runGdalRasterizeOverFixedValue(
            inputLayer=buffered_layer,
            inputRaster=output_raster_layer,
            value=nodata_value,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )

        if multiStepFeedback.isCanceled():
            return {}

        multiStepFeedback.pushInfo(self.tr('Processing completed successfully!'))

        return {self.OUTPUT_RASTER: output_raster}
