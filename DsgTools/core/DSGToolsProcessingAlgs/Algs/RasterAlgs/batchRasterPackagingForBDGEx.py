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
from pathlib import Path
from uuid import uuid4
import numpy as np
import json
import processing
from osgeo import gdal, ogr
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingUtils,
    QgsProject,
    QgsProcessingParameterFileDestination,
    QgsVectorFileWriter,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsProcessingParameterBoolean,
)
from scipy import signal


class BatchRasterPackagingForBDGEx(QgsProcessingAlgorithm):

    INPUT_FOLDER = "INPUT_FOLDER"
    USE_PHOTOMETRIC = "USE_PHOTOMETRIC"
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
            QgsProcessingParameterBoolean(
                self.USE_PHOTOMETRIC,
                self.tr("Use Photometric YCbCr"),
                defaultValue=True,
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
        usePhotometric = self.parameterAsBoolean(parameters, self.USE_PHOTOMETRIC, context)
        inputFiles = list(
            set(
                [
                    Path(i)
                    for i in itertools.chain.from_iterable(
                        [
                            glob.glob(f"{inputFolder}/**/*.tif"),
                            glob.glob(f"{inputFolder}/*.tif"),
                        ]
                    )
                    if "browse" not in str(i).lower()
                ]
            )
        )
        nInputs = len(inputFiles)
        if nInputs == 0:
            raise QgsProcessingException(
                "Não foram encontrados arquivos .tif na pasta de entrada."
            )
        stepSize = 100 / nInputs
        input_file_path = Path(inputFolder).resolve()
        output_base_path = Path(output_path).resolve()
        multiStepFeedback = QgsProcessingMultiStepFeedback(nInputs, feedback)
        for current, input_path in enumerate(inputFiles):
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Converting {current+1}/{nInputs}: Converting file {input_path}"
                )
            )
            multiStepFeedback.setCurrentStep(current)
            if feedback.isCanceled():
                break
            relative_path = Path(input_path).relative_to(input_file_path).parent
            output_dir = output_base_path / relative_path
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file_path = output_dir / input_path.name
            processing.run(
                "gdal:warpreproject",
                {
                    "INPUT": str(input_path),
                    "SOURCE_CRS": None,
                    "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4674"),
                    "RESAMPLING": 0,
                    "NODATA": None,
                    "TARGET_RESOLUTION": None,
                    "OPTIONS": "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE|PHOTOMETRIC=YCbCr" if usePhotometric else "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE",
                    "DATA_TYPE": 0,
                    "TARGET_EXTENT": None,
                    "TARGET_EXTENT_CRS": None,
                    "MULTITHREADING": False,
                    "EXTRA": "",
                    "OUTPUT": str(output_file_path),
                },
                context=context,
                feedback=multiStepFeedback,
            )

        return {
            "OUTPUT_FOLDER": output_path,
        }

    def writeOutputRaster(self, outputRaster, npRaster, ds, outputType=gdal.GDT_Int32):
        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(
            outputRaster, npRaster.shape[1], npRaster.shape[0], 1, outputType
        )
        out_ds.SetProjection(ds.GetProjection())
        out_ds.SetGeoTransform(ds.GetGeoTransform())
        out_ds.GetRasterBand(1).SetNoDataValue(-9999)
        band = out_ds.GetRasterBand(1)
        band.WriteArray(npRaster)
        band.FlushCache()
        band.ComputeStatistics(False)
        out_ds = None

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
