# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-01-22
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

import re
import zipfile
from xml.etree import ElementTree
from pathlib import Path
from typing import List
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsFeature,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeedback,
    QgsVectorFileWriter,
    QgsField,
)


class PrepareRasterFilesForPackagingForBDGEx(QgsProcessingAlgorithm):

    INPUT_FOLDER = "INPUT_FOLDER"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_FOLDER,
                self.tr("Pasta com os arquivos no formato zip"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER, self.tr("Pasta para salvar os arquivos exportados")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        output_path = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)
        inputFolder = self.parameterAsFile(parameters, self.INPUT_FOLDER, context)
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputFiles = list(
            set(
                [
                    i
                    for i in Path(inputFolder).rglob("*.zip")
                ]
            )
        )
        nInputs = len(inputFiles)
        if nInputs == 0:
            raise QgsProcessingException(
                "Não foram encontrados arquivos .zip na pasta de entrada."
            )
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        self.unzipFiles(inputFiles, output_path, multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        self.process_delivery_metadata(output_path, multiStepFeedback)
        
        return {
            "OUTPUT_FOLDER": output_path,
        }
    
    def unzipFiles(self, inputFiles: List[str], output_path: str, feedback: QgsFeedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(len(inputFiles), feedback)
        for currentStep, zipPath in enumerate(inputFiles):
            multiStepFeedback.setCurrentStep(currentStep)
            if multiStepFeedback.isCanceled():
                break
            with zipfile.ZipFile(zipPath, "r") as zip_ref:
                zip_ref.extractall(output_path)
    
    def extract_metadata(self, xml_content):
        # Parse XML
        root = ElementTree.fromstring(xml_content)
        
        # Extract namespace automatically
        # The namespace is typically in the root tag in format like {namespace}tag
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0].strip('{')
        
        # Create the namespace dictionary
        ns = {'dm': namespace} if namespace else {}
        
        # Create xpath prefix based on whether we have a namespace
        xpath_prefix = './/dm:' if namespace else './/'
        
        # Extract the requested fields
        metadata = {
            'sensorVehicle': root.find(f'{xpath_prefix}product/{xpath_prefix}sensorVehicle', ns).text,
            'earliestAcquisitionTime': root.find(f'{xpath_prefix}product/{xpath_prefix}earliestAcquisitionTime', ns).text,
            'catalogIdentifier': root.find(f'{xpath_prefix}product/{xpath_prefix}catalogIdentifier', ns).text,
            'relativeDirectory': root.find(f'{xpath_prefix}product/{xpath_prefix}productFile/{xpath_prefix}relativeDirectory', ns).text
        }
        
        return metadata
    
    def process_delivery_metadata(self, root_dir, feedback=None):
        # Find all DeliveryMetadata.xml files
        root_path = Path(root_dir)
        metadata_files = list(root_path.rglob('DeliveryMetadata.xml'))
        
        # Create feedback object
        total_steps = len(metadata_files)
        multiStepFeedback = QgsProcessingMultiStepFeedback(total_steps, feedback) if feedback else None
        
        for current_step, metadata_file in enumerate(metadata_files):
            # Update progress
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(current_step)
                multiStepFeedback.pushInfo(f'Processing metadata file {current_step + 1}/{total_steps}: {metadata_file}')
            
            try:
                # Read and extract metadata
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                metadata_dict = self.extract_metadata(xml_content)
                
            except FileNotFoundError:
                if multiStepFeedback is not None:
                    multiStepFeedback.reportError(f"Could not find metadata file: {metadata_file}")
                continue
            except PermissionError:
                if multiStepFeedback is not None:
                    multiStepFeedback.reportError(f"Permission denied when accessing: {metadata_file}")
                continue
            except ElementTree.ParseError:
                if multiStepFeedback is not None:
                    multiStepFeedback.reportError(f"Invalid XML format in file: {metadata_file}")
                continue
            
            # Check for cancellation
            if multiStepFeedback and multiStepFeedback.isCanceled():
                if multiStepFeedback is not None:
                    multiStepFeedback.pushInfo('Process canceled by user')
                return
                
            # Find the PRODUCT_SHAPE shapefile
            metadata_dir = metadata_file.parent
            product_shape_files = list(metadata_dir.rglob('*_PRODUCT_SHAPE.shp'))
            
            if not product_shape_files:
                if multiStepFeedback is not None:
                    multiStepFeedback.pushInfo(f"No PRODUCT_SHAPE file found for {metadata_file}")
                continue
                
            for product_shape_file in product_shape_files:
                if multiStepFeedback is not None:
                    multiStepFeedback.pushInfo(f'Processing shapefile: {product_shape_file}')
                    
                try:
                    # Load the source shapefile
                    source_layer = QgsVectorLayer(str(product_shape_file), "source", "ogr")
                    if not source_layer.isValid():
                        raise QgsProcessingException(f"Failed to load source layer: {product_shape_file}")

                    # Create new filename
                    original_name = product_shape_file.stem
                    new_name = original_name.replace('_PRODUCT_SHAPE', '_SEAMLINES_SHAPE')
                    output_file = str(product_shape_file.parent / f"{new_name}.shp")

                    # Create field mappings for the new layer
                    fields = source_layer.fields()
                    
                    # Add new fields for metadata
                    fields.append(QgsField("sensorVeh", QVariant.String))
                    fields.append(QgsField("acquisitio", QVariant.String))
                    fields.append(QgsField("catIdent", QVariant.String))
                    fields.append(QgsField("relDir", QVariant.String))
                    fields.append(QgsField("_filename", QVariant.String))

                    # Create the writer
                    writer = QgsVectorFileWriter(
                        output_file,
                        "UTF-8",
                        fields,
                        source_layer.wkbType(),
                        source_layer.crs(),
                        "ESRI Shapefile"
                    )

                    if writer.hasError() != QgsVectorFileWriter.NoError:
                        raise QgsProcessingException(f"Error creating writer for {output_file}")

                    # Get total feature count for progress
                    feature_count = source_layer.featureCount()
                    
                    # Copy features and add metadata
                    for feature_idx, feature in enumerate(source_layer.getFeatures()):
                        # Check for cancellation
                        if multiStepFeedback and multiStepFeedback.isCanceled():
                            del writer
                            if multiStepFeedback is not None:
                                multiStepFeedback.pushInfo('Process canceled by user')
                            return
                            
                        # Update progress message
                        if multiStepFeedback and feature_idx % 100 == 0:  # Update every 100 features
                            multiStepFeedback.setProgress(
                                current_step * 100 + (feature_idx / feature_count) * 100
                            )
                            
                        new_feature = QgsFeature(fields)
                        new_feature.setGeometry(feature.geometry())
                        
                        # Copy existing attributes
                        for i in range(feature.fields().count()):
                            new_feature[i] = feature[i]
                            
                        # Add metadata attributes
                        new_feature["sensorVeh"] = metadata_dict["sensorVehicle"]
                        new_feature["acquisitio"] = metadata_dict["earliestAcquisitionTime"]
                        new_feature["catIdent"] = f'ID_{metadata_dict["catalogIdentifier"]}'
                        new_feature["relDir"] = metadata_dict["relativeDirectory"]
                        new_feature["_filename"] = f'{metadata_dict["sensorVehicle"]}_{feature["bandInfo"]}_{re.sub("T.+", "", metadata_dict["earliestAcquisitionTime"]).replace("-","")}_{metadata_dict["catalogIdentifier"]}_R_{metadata_dict["relativeDirectory"].replace("/GIS_FILES", "")}'.replace(" ","_").replace("/GIS_FILES", "")
                        
                        writer.addFeature(new_feature)

                    # Clean up
                    del writer
                    if multiStepFeedback is not None:
                        multiStepFeedback.pushInfo(f"Created {output_file}")
                except PermissionError:
                    if multiStepFeedback is not None:
                        multiStepFeedback.reportError(f"Permission denied when creating output file")
                    continue
                except OSError as e:
                    if multiStepFeedback is not None:
                        multiStepFeedback.reportError(f"OS error when processing shapefile: {str(e)}")
                    continue
        
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo('Processing completed')
            

    def getRasterLayer(self, input_path: str) -> QgsRasterLayer:
        options = QgsRasterLayer.LayerOptions()
        options.loadDefaultStyle = False
        rasterLayer = QgsRasterLayer(
            str(input_path), Path(input_path).stem, "gdal", options
        )
        return rasterLayer

    def tr(self, string):
        return QCoreApplication.translate("PrepareRasterFilesForPackagingForBDGEx", string)

    def createInstance(self):
        return PrepareRasterFilesForPackagingForBDGEx()

    def name(self):
        return "preparerasterfilesforpackagingforbdgex"

    def displayName(self):
        return self.tr("Prepare Files for Raster Packaging for BDGEx")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            "The algorithm unzips the inputs and builds the seamlines files with necessary information."
        )
