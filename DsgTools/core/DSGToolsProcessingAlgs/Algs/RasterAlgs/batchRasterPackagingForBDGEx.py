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

from collections import defaultdict
import glob
import itertools
import re
import zipfile
import json
import xml.dom.minidom
import datetime
from pathlib import Path
from typing import Dict, List, Union
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
import processing
from osgeo import gdal
from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsRasterLayer,
    QgsProcessingUtils,
    QgsVectorLayer,
    QgsFeatureSource,
    QgsFeedback,
    QgsProcessingContext,
    QgsGeometry,
)


class BatchRasterPackagingForBDGEx(QgsProcessingAlgorithm):

    INPUT_FOLDER = "INPUT_FOLDER"
    XML_TEMPLATE_FILE = "XML_TEMPLATE_FILE"
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
            QgsProcessingParameterFile(
                self.XML_TEMPLATE_FILE,
                self.tr("XML template"),
                behavior=QgsProcessingParameterFile.File,
                fileFilter="XML (*.xml)",
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
        self.xml_template_path = self.parameterAsFile(
            parameters,
            self.XML_TEMPLATE_FILE,
            context,
        )
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
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

        self.tempFolder = QgsProcessingUtils.tempFolder()
        input_folder_path = Path(inputFolder).resolve()
        output_base_path = Path(output_path).resolve()
        self.shapefilesDict = self.getShapefilesDict(inputFolder)
        nInputs = 1 + sum(
            [
                v.get("TILE_SHAPE", None).featureCount()
                for v in self.shapefilesDict.values()
                if v.get("TILE_SHAPE", None) is not None
            ]
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(nInputs, feedback)
        self.inputFilesDict = {
            p.name: {"path": p, "size_in_gb": p.stat().st_size / (1024**3)}
            for p in inputFiles
        }
        multiStepFeedback.setCurrentStep(0)
        self.relatedPolygonsDict = self.relatePolygons(multiStepFeedback, context)

        for current, (folderKey, geomDict) in enumerate(
            self.relatedPolygonsDict.items(), start=1
        ):
            for inner, (geomWkb, fileNameList) in enumerate(geomDict.items()):
                currentIndex = current * inner
                multiStepFeedback.pushInfo(
                    self.tr(f"Evaluating {currentIndex+1}/{nInputs} seamlines")
                )
                multiStepFeedback.setProgressText(
                    self.tr(f"Evaluating {currentIndex+1}/{nInputs} seamlines")
                )
                multiStepFeedback.setCurrentStep(currentIndex)
                if multiStepFeedback.isCanceled():
                    break
                if len(fileNameList) == 0:
                    continue
                diskSize = sum(
                    self.inputFilesDict.get(fileName, {}).get("size_in_gb", 0)
                    for fileName in fileNameList
                )
                input_path = self.inputFilesDict.get(fileNameList[0], {}).get(
                    "path", None
                )
                if input_path is None:
                    raise QgsProcessingException("Invalid Path")
                relative_path = Path(input_path).relative_to(input_folder_path).parent
                output_dir = output_base_path / relative_path
                output_dir.mkdir(parents=True, exist_ok=True)
                prefix = "".join(re.findall(r"R\d+C\d+", input_path.name))
                output_file_path = output_dir / str(input_path.name).replace(
                    prefix, str(inner)
                )
                if diskSize < 2:
                    vrt = self.algRunner.runBuildVRT(
                        inputRasterList=[
                            str(self.inputFilesDict[f]["path"]) for f in fileNameList
                        ],
                        context=context,
                        feedback=multiStepFeedback,
                        outputLyr=QgsProcessingUtils.generateTempFilename(
                            f"{folderKey}{inner}.tif"
                        ),
                    )
                    rasterLayer = (
                        self.getRasterLayer(vrt)
                        if not isinstance(vrt, QgsRasterLayer)
                        else vrt
                    )
                    geom = QgsGeometry()
                    geom.fromWkb(geomWkb)
                    clipLayer = self.layerHandler.createMemoryLayerFromGeometry(
                        geom, rasterLayer.crs()
                    )
                    multiStepFeedback.setCurrentStep(currentIndex + 1)
                    clipped = self.algRunner.runClipRasterLayer(
                        inputRaster=rasterLayer,
                        mask=clipLayer,
                        context=context,
                        feedback=multiStepFeedback,
                        outputRaster=str(output_file_path),
                    )
                    multiStepFeedback.setCurrentStep(currentIndex + 2)
                    bandcount = rasterLayer.bandCount()
                    self.algRunner.runGdalWarp(
                        rasterLayer=rasterLayer,
                        targetCrs=QgsCoordinateReferenceSystem("EPSG:4674"),
                        resampling=0,
                        options="COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE|PHOTOMETRIC=YCbCr"
                        if bandcount > 1
                        else "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE",
                        multiThreading=True,
                        outputLyr=str(output_file_path),
                        context=context,
                        feedback=multiStepFeedback,
                    )
                    multiStepFeedback.setCurrentStep(currentIndex + 3)
                    self.buildXML(
                        rasterLayer=clipped,
                        matchedFeature=self.shapefilesDict[folderKey]["FEAT_DICT"][
                            geomWkb
                        ],
                        output_xml_file=str(output_file_path).replace(".tif", ".xml"),
                    )

        return {
            "OUTPUT_FOLDER": output_path,
        }

    def getRasterLayer(self, input_path: str) -> QgsRasterLayer:
        options = QgsRasterLayer.LayerOptions()
        options.loadDefaultStyle = False
        rasterLayer = QgsRasterLayer(
            str(input_path), Path(input_path).stem, "gdal", options
        )
        return rasterLayer

    def getShapefilesDict(
        self, inputFolder: str
    ) -> Dict[str, Union[QgsVectorLayer, Dict[QByteArray, QgsFeature], Path]]:
        shapefilesDict = defaultdict(dict)
        for zipPath in Path(inputFolder).rglob("*.zip"):
            with zipfile.ZipFile(zipPath, "r") as zip_ref:
                zip_ref.extractall(self.tempFolder)
        for shp in Path(self.tempFolder).rglob("*.shp"):
            if "_SEAMLINES_SHAPE" in str(shp):
                key = str(shp.name).replace(".shp", "").replace("_SEAMLINES_SHAPE", "")
                shapefilesDict[key]["SEAMLINES_SHAPE"] = QgsVectorLayer(
                    str(shp), key, "ogr"
                )
            elif "_TILE_SHAPE" in str(shp):
                key = str(shp.name).replace(".shp", "").replace("_TILE_SHAPE", "")
                shapefilesDict[key]["TILE_SHAPE"] = QgsVectorLayer(str(shp), key, "ogr")
                shapefilesDict[key]["FEAT_DICT"] = dict()
                for feat in shapefilesDict[key]["TILE_SHAPE"].getFeatures():
                    geom = feat.geometry()
                    geomWkb = geom.asWkb()
                    shapefilesDict[key]["FEAT_DICT"][geomWkb] = feat

            else:
                continue

        return shapefilesDict

    def relatePolygons(
        self, feedback: QgsFeedback, context: QgsProcessingContext
    ) -> Dict[str, Dict[QByteArray, List[str]]]:
        relatedItemsDict = defaultdict(lambda: defaultdict(list))
        nItems = len(self.shapefilesDict)
        if nItems == 0:
            return relatedItemsDict
        multiStepFeedback = QgsProcessingMultiStepFeedback(4 * nItems, feedback)
        for current, (key, valueDict) in enumerate(self.shapefilesDict.items()):
            if multiStepFeedback.isCanceled():
                break
            if "SEAMLINES_SHAPE" not in valueDict or "TILE_SHAPE" not in valueDict:
                multiStepFeedback.setCurrentStep(4 * current + 3)
                continue
            multiStepFeedback.setCurrentStep(4 * current)
            if multiStepFeedback.isCanceled():
                break
            if (
                valueDict["SEAMLINES_SHAPE"].hasSpatialIndex()
                != QgsFeatureSource.SpatialIndexPresence.SpatialIndexPresent
            ):
                self.algRunner.runCreateSpatialIndex(
                    inputLyr=valueDict["SEAMLINES_SHAPE"],
                    context=context,
                    feedback=multiStepFeedback,
                    is_child_algorithm=True,
                )
            multiStepFeedback.setCurrentStep(4 * current + 1)
            if multiStepFeedback.isCanceled():
                break
            if (
                valueDict["TILE_SHAPE"].hasSpatialIndex()
                != QgsFeatureSource.SpatialIndexPresence.SpatialIndexPresent
            ):
                self.algRunner.runCreateSpatialIndex(
                    inputLyr=valueDict["TILE_SHAPE"],
                    context=context,
                    feedback=multiStepFeedback,
                    is_child_algorithm=True,
                )
            multiStepFeedback.setCurrentStep(4 * current + 2)
            if multiStepFeedback.isCanceled():
                break
            joinnedSeamline = self.algRunner.runJoinAttributesByLocation(
                inputLyr=valueDict["SEAMLINES_SHAPE"],
                joinLyr=valueDict["TILE_SHAPE"],
                predicateList=[AlgRunner.Intersect],
                method=0,
                context=context,
                feedback=multiStepFeedback,
            )
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(4 * current + 3)
            for feat in joinnedSeamline.getFeatures():
                if multiStepFeedback.isCanceled():
                    break
                geom = feat.geometry()
                geomKey = geom.asWkb()
                relatedItemsDict[key][geomKey].append(feat["fileName"])
        return relatedItemsDict

    def buildXML(
        self,
        rasterLayer: QgsRasterLayer,
        matchedFeature: QgsFeature,
        output_xml_file: str,
    ) -> None:
        extent = rasterLayer.extent()
        prefix = "".join(re.findall(r"R\d+C\d+", rasterLayer.name()))
        substitutions = {
            "X_MIN": f"{extent.xMinimum()}",
            "X_MAX": f"{extent.xMaximum()}",
            "Y_MIN": f"{extent.yMinimum()}",
            "Y_MAX": f"{extent.xMaximum()}",
            "NOME_PRODUTO": f"""{matchedFeature["source"]}_{matchedFeature["productTyp"].replace(" ","_")}_{re.sub("T.+", "", matchedFeature["acquisitio"]).replace("-","")}_{prefix}""",
            "DATA_IMAGEM": re.sub("T.+", "", matchedFeature["acquisitio"]),
        }
        with open(self.xml_template_path, "r") as f:
            xmlstring = f.read()
        pattern = re.compile(r"{{([^{}]+)}}")
        xmlstring = re.sub(pattern, lambda m: substitutions[m.group(1)], xmlstring)
        with open(output_xml_file, "w") as f:
            f.write(xmlstring)

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
