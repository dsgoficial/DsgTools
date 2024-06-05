# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-06-05
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

import glob
import itertools
import zipfile
from pathlib import Path
from typing import Dict
import processing
from osgeo import gdal
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsProcessingParameterBoolean,
    QgsRasterLayer,
    QgsProcessingUtils,
    QgsVectorLayer,
)


class BatchRasterPackagingForBDGEx(QgsProcessingAlgorithm):

    INPUT_FOLDER = "INPUT_FOLDER"
    XML_TEMPLATE = "XML_TEMPLATE"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_FOLDER,
                self.tr("Pasta com os arquivos no formato tif"),
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
        inputFiles = list(
            set(
                [
                    i
                    for i in Path(inputFolder).rglob("*.tif")
                    if "browse" not in str(i).lower()
                ]
            )
        )
        nInputs = len(inputFiles)
        if nInputs == 0:
            raise QgsProcessingException(
                "Não foram encontrados arquivos .tif na pasta de entrada."
            )
        
        input_file_path = Path(inputFolder).resolve()
        output_base_path = Path(output_path).resolve()
        multiStepFeedback = QgsProcessingMultiStepFeedback(nInputs, feedback)
        self.tempFolder = QgsProcessingUtils.tempFolder()
        self.seamlinesDict = self.getSeamlinesDict(inputFolder)
        for current, input_path in enumerate(inputFiles):
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Converting {current+1}/{nInputs}: Converting file {input_path}"
                )
            )
            multiStepFeedback.setProgressText(
                self.tr(
                    f"Converting {current+1}/{nInputs}"
                )
            )
            multiStepFeedback.setCurrentStep(current)
            if feedback.isCanceled():
                break
            relative_path = Path(input_path).relative_to(input_file_path).parent
            output_dir = output_base_path / relative_path
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file_path = output_dir / input_path.name
            rasterLayer = self.getRasterLayer(input_path)
            bandcount = rasterLayer.bandCount()
            self.buildXML(rasterLayer=rasterLayer, output_xml_file=str(output_file_path).replace(".tif", '.xml'))
            processing.run(
                "gdal:warpreproject",
                {
                    "INPUT": rasterLayer,
                    "SOURCE_CRS": None,
                    "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4674"),
                    "RESAMPLING": 0,
                    "NODATA": None,
                    "TARGET_RESOLUTION": None,
                    "OPTIONS": "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE|PHOTOMETRIC=YCbCr" if bandcount > 1 else "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE",
                    "DATA_TYPE": 0,
                    "TARGET_EXTENT": None,
                    "TARGET_EXTENT_CRS": None,
                    "MULTITHREADING": True,
                    "EXTRA": "",
                    "OUTPUT": str(output_file_path),
                },
                context=context,
                feedback=multiStepFeedback,
            )

        return {
            "OUTPUT_FOLDER": output_path,
        }

    def getRasterLayer(self, input_path: str) -> QgsRasterLayer:
        options = QgsRasterLayer.LayerOptions()
        options.loadDefaultStyle = False
        rasterLayer = QgsRasterLayer(str(input_path), str(input_path), "gdal", options)
        return rasterLayer
    
    def getSeamlinesDict(self, inputFolder: str) -> Dict[str, QgsVectorLayer]:
        seamlinesDict = dict()
        for zipPath in Path(inputFolder).rglob("*.zip"):
            with zipfile.ZipFile(zipPath, 'r') as zip_ref:
                zip_ref.extractall(self.tempFolder)
        for shp in Path(self.tempFolder).rglob("*.shp"):
            if "_SEAMLINES_SHAPE" not in str(shp):
                continue
            key = str(shp.name).replace(".shp", "").replace("_SEAMLINES_SHAPE","")
            seamlinesDict[key] = QgsVectorLayer(str(shp), key, "ogr")

        return seamlinesDict
    
    def buildXML(self, rasterLayer: QgsRasterLayer, output_xml_file: str) -> None:
        pass

    def tr(self, string):
        return QCoreApplication.translate("BatchRasterPackagingForBDGEx", string)

    def createInstance(self):
        return BatchRasterPackagingForBDGEx()

    def name(self):
        return "batchrasterpackagingforbdgex"

    def displayName(self):
        return self.tr("Batch Convert Raster Files for BDGEx Packaging")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            "The algorithm converts input rasters to .tif with specs required by BDGEx. It also builds the XML of each file according to the template."
        )
