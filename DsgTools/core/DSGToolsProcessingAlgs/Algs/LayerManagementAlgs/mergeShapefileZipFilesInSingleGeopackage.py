# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-08-21
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

import os
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterCrs,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsProcessingContext,
    QgsFeedback,
    QgsProcessingMultiStepFeedback
)
from qgis.PyQt.QtCore import QCoreApplication

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class MergeShapefileZipFilesInSingleGeopackage(QgsProcessingAlgorithm):
    """
    Processing algorithm to merge multiple zipped shapefiles into a single GeoPackage.
    Layers with the same name are consolidated together using native QGIS merge functionality.
    """
    
    INPUT_ZIPS = 'INPUT_ZIPS'
    OUTPUT_GPKG = 'OUTPUT_GPKG'
    DESTINATION_CRS = 'DESTINATION_CRS'
    
    def __init__(self):
        super().__init__()
        self.algRunner = AlgRunner()
    
    def tr(self, string):
        return QCoreApplication.translate('MergeShapefileZipFilesInSingleGeopackage', string)
    
    def createInstance(self):
        return MergeShapefileZipFilesInSingleGeopackage()
    
    def name(self):
        return 'mergeshapefilezipfilesinsinglegeopackage'
    
    def displayName(self):
        return self.tr('Merge Shapefile Zip Files In a Single Geopackage')
    
    def group(self):
        return self.tr("Layer Management Algorithms")
    
    def groupId(self):
        return "DSGTools - Layer Management Algorithms"
    
    def shortHelpString(self):
        return self.tr("""
        This algorithm merges multiple zipped shapefiles into a single GeoPackage.
        
        Features:
        - Extracts shapefiles from multiple zip archives
        - Groups layers by name (case-insensitive)
        - Merges layers with the same name into single layers using QGIS native merge
        - Preserves all attributes from merged layers
        - Reprojects all layers to the specified destination CRS
        - Outputs all consolidated layers to a single GeoPackage
        
        Parameters:
        - Input ZIP files: Multiple zip files containing shapefiles
        - Output GeoPackage: Path for the output .gpkg file
        - Destination CRS: Coordinate reference system for the output layers (all layers will be reprojected to this CRS)
        """)
    
    def initAlgorithm(self, config=None):
        # Input: Multiple zip files
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_ZIPS,
                self.tr('Input ZIP files'),
                QgsProcessing.TypeFile
            )
        )
        
        # Output: GeoPackage file
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_GPKG,
                self.tr('Output GeoPackage'),
                'GeoPackage files (*.gpkg)'
            )
        )
        
        # Option to specify destination CRS
        self.addParameter(
            QgsProcessingParameterCrs(
                self.DESTINATION_CRS,
                self.tr('Destination CRS'),
                defaultValue=QgsCoordinateReferenceSystem("EPSG:4674"),
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        # Get parameters
        zip_files = self.parameterAsFileList(parameters, self.INPUT_ZIPS, context)
        output_gpkg = self.parameterAsFileOutput(parameters, self.OUTPUT_GPKG, context)
        destination_crs = self.parameterAsCrs(parameters, self.DESTINATION_CRS, context)
        
        if not zip_files:
            raise QgsProcessingException(self.tr('No input ZIP files specified'))
        
        # Set up multi-step feedback
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        
        # Dictionary to group layers by name
        layers_by_name = defaultdict(list)
        
        # Create temporary directory for extraction
        temp_dir = tempfile.mkdtemp()
        loaded_layers = []  # Keep track of loaded layers for cleanup

        # Step 1: Extract ZIP files
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr('Extracting ZIP files...'))
        
        total_files = len(zip_files)
        for i, zip_file in enumerate(zip_files):
            if multiStepFeedback.isCanceled():
                return {}
            
            multiStepFeedback.setProgress(int((i / total_files) * 100))
            multiStepFeedback.setProgressText(self.tr(f'Processing ZIP file {i+1}/{total_files}: {os.path.basename(zip_file)}'))
            
            # Extract ZIP file
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                multiStepFeedback.reportError(self.tr(f'Error extracting {zip_file}: {str(e)}'))
                continue
        
        # Step 2: Search for shapefiles
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr('Searching for shapefiles...'))
        
        shapefiles = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.shp'):
                    shapefiles.append(os.path.join(root, file))
        
        if not shapefiles:
            raise QgsProcessingException(self.tr('No shapefiles found in the ZIP files'))
        
        multiStepFeedback.setProgressText(self.tr(f'Found {len(shapefiles)} shapefiles'))
        
        # Step 3: Load shapefiles and group by name
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(self.tr('Loading and grouping shapefiles...'))
        
        for i, shp_path in enumerate(shapefiles):
            if multiStepFeedback.isCanceled():
                return {}
            
            multiStepFeedback.setProgress(int((i / len(shapefiles)) * 100))
            
            layer_name = Path(shp_path).stem
            multiStepFeedback.setProgressText(self.tr(f'Loading shapefile: {layer_name}'))
            
            # Group by layer name (case-insensitive)
            normalized_name = layer_name.lower()
            layers_by_name[normalized_name].append({
                'original_name': layer_name,
                'path': shp_path
            })
        
        if not layers_by_name:
            raise QgsProcessingException(self.tr('No valid shapefiles found'))
        
        # Remove output file if it exists
        if os.path.exists(output_gpkg):
            os.remove(output_gpkg)
        
        # Step 4: Process layer groups
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.setProgressText(self.tr('Merging layers and creating GeoPackage...'))
        
        consolidated_count = 0
        total_layer_groups = len(layers_by_name)
        
        for group_idx, (normalized_name, layer_group) in enumerate(layers_by_name.items()):
            if multiStepFeedback.isCanceled():
                return {}
            
            multiStepFeedback.setProgress(int((group_idx / total_layer_groups) * 100))
            
            # Use the original name from the first layer in the group
            output_layer_name = layer_group[0]['original_name']
            multiStepFeedback.setProgressText(self.tr(f'Merging layer group: {output_layer_name} ({len(layer_group)} layers)'))
            
            # Prepare layers for merging
            layers_to_merge = []
            target_crs = destination_crs
            
            # If no destination CRS specified, use the first layer's CRS
            # Multiple layers - merge them
            multiStepFeedback.setProgressText(self.tr(f'Merging {len(layers_to_merge)} layers for {output_layer_name}'))
            merged_layer = self.algRunner.runMergeVectorLayers(
                inputList=[item["path"] for item in layer_group],
                context=context,
                feedback=multiStepFeedback,
                crs=target_crs,
                is_child_algorithm=True,
            )
            merged_layer = self.algRunner.runDropFields(
                merged_layer,
                fieldList=['layer', 'path', 'ID', 'id'],
                context=context,
                feedback=multiStepFeedback,
            )
            
            # Save merged layer to GeoPackage
            save_options = QgsVectorFileWriter.SaveVectorOptions()
            save_options.driverName = 'GPKG'
            save_options.layerName = output_layer_name
            save_options.actionOnExistingFile = (
                QgsVectorFileWriter.CreateOrOverwriteFile if consolidated_count == 0
                else QgsVectorFileWriter.CreateOrOverwriteLayer
            )
            
            # Write to GeoPackage
            if isinstance(merged_layer, str):
                # If algRunner returned a path, load the layer
                temp_layer = QgsVectorLayer(merged_layer, 'temp', 'ogr')
                source_layer = temp_layer
            else:
                source_layer = merged_layer
            
            # Correção na chamada do writeAsVectorFormat
            error, error_message = QgsVectorFileWriter.writeAsVectorFormat(
                source_layer,
                output_gpkg,
                save_options
            )
            
            if error != QgsVectorFileWriter.NoError:
                raise QgsProcessingException(
                    self.tr(f'Error writing layer {output_layer_name} to GeoPackage: {error_message}')
                )
            
            consolidated_count += 1
            multiStepFeedback.pushInfo(self.tr(f'Merged {len(layer_group)} layers into: {output_layer_name}'))
        
        multiStepFeedback.pushInfo(self.tr(f'Successfully created GeoPackage with {consolidated_count} consolidated layers'))
        multiStepFeedback.pushInfo(self.tr(f'Output: {output_gpkg}'))
        
        return {self.OUTPUT_GPKG: output_gpkg}

