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
import math
import re
import shutil
from uuid import uuid4
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
    QgsProcessingParameterEnum,
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
    QgsRectangle,
    NULL,
)


class BatchRasterPackagingForBDGEx(QgsProcessingAlgorithm):

    INPUT_FOLDER = "INPUT_FOLDER"
    XML_TEMPLATE_FILE = "XML_TEMPLATE_FILE"
    IMAGE_SENSOR = "IMAGE_SENSOR"
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
        self.image_sensors = [
            self.tr("Imagens BECA"),
            self.tr("Imagens MAXAR"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.IMAGE_SENSOR,
                self.tr("Sensor"),
                options=self.image_sensors,
                defaultValue=0,
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
        idx = self.parameterAsEnum(parameters, self.IMAGE_SENSOR, context)
        imageSensor = self.image_sensors[idx]
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

        self.tempFolder = Path(QgsProcessingUtils.tempFolder()) / uuid4().hex
        if not self.tempFolder.exists():
            self.tempFolder.mkdir(parents=True, exist_ok=True)
        input_folder_path = Path(inputFolder).resolve()
        output_base_path = Path(output_path).resolve()
        self.shapefilesDict = self.getShapefilesDict(inputFolder)
        self.inputFilesDict = {
            p.name: {"path": p, "size_in_gb": p.stat().st_size / (1024**3)}
            for p in inputFiles
        }
        self.relatedPolygonsDict = self.relatePolygons(feedback, context)
        nInputs = 2 * sum(
            [
                v.get("SEAMLINES_SHAPE", None).featureCount()
                for v in self.shapefilesDict.values()
                if v.get("SEAMLINES_SHAPE", None) is not None
            ]
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(nInputs, feedback)
        currentIndex = 0
        currentSeamline = 0
        for folderKey, geomDict in self.relatedPolygonsDict.items():
            for inner, (geomWkb, fileNameList) in enumerate(geomDict.items()):
                multiStepFeedback.pushInfo(
                    self.tr(f"Evaluating {currentSeamline+1}/{nInputs//2} seamlines")
                )
                multiStepFeedback.setProgressText(
                    self.tr(f"Evaluating {currentSeamline+1}/{nInputs//2} seamlines")
                )
                multiStepFeedback.setCurrentStep(currentIndex)
                if multiStepFeedback.isCanceled():
                    break
                if len(fileNameList) == 0:
                    continue
                input_path = self.inputFilesDict.get(fileNameList[0], {}).get(
                    "path", None
                )
                if input_path is None:
                    raise QgsProcessingException("Invalid Path")
                relative_path = Path(input_path).relative_to(input_folder_path).parent
                output_dir = output_base_path / relative_path
                output_dir.mkdir(parents=True, exist_ok=True)
                prefix = "".join(re.findall(r"R\d+C\d+", input_path.name))
                diskSize = sum(
                    self.inputFilesDict.get(fileName, {}).get("size_in_gb", 0)
                    for fileName in fileNameList
                )
                matchedFeature = self.shapefilesDict[folderKey]["FEAT_DICT"][geomWkb]
                productName = self.getProductName(matchedFeature)
                output_file_path = output_dir / f"{productName}{input_path.suffix}"
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
                bandcount = rasterLayer.bandCount()
                currentIndex += 1
                for i, clipLayer in enumerate(
                    self.getClipPolygonLayers(rasterLayer, diskSize, geomWkb, context),
                    start=1,
                ):
                    multiStepFeedback.setCurrentStep(currentIndex)
                    clippedOutputPath = (
                        str(output_file_path)
                        if diskSize < 2
                        else str(
                            output_file_path.parent
                            / f"{output_file_path.stem}_{i}{output_file_path.suffix}"
                        )
                    )
                    clipped = self.algRunner.runClipRasterLayer(
                        inputRaster=rasterLayer,
                        mask=clipLayer,
                        targetCrs=QgsCoordinateReferenceSystem("EPSG:4674"),
                        options="COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE|PHOTOMETRIC=YCbCr"
                        if bandcount > 1
                        else "COMPRESS=JPEG|JPEG_QUALITY=75|TILED=TRUE",
                        context=context,
                        multiThreading=True,
                        feedback=multiStepFeedback,
                        outputRaster=clippedOutputPath,
                    )
                    currentIndex += 1
                    multiStepFeedback.setCurrentStep(currentIndex)
                    clippedRasterLayer = (
                        self.getRasterLayer(clipped)
                        if not isinstance(clipped, QgsRasterLayer)
                        else clipped
                    )
                    self.buildXML(
                        rasterLayer=clippedRasterLayer,
                        matchedFeature=matchedFeature,
                        output_xml_file=clippedOutputPath.replace(
                            ".tif", ".xml"
                        ).replace(".TIF", ".xml"),
                        productName=Path(clippedOutputPath).stem,
                    )
                    currentIndex += 1
                currentSeamline += 1
        self.cleanupTempFolder()
        return {
            "OUTPUT_FOLDER": output_path,
        }

    def getProductName(self, matchedFeature):
        if "_filename" in [f.name() for f in matchedFeature.fields()]:
            return matchedFeature["_filename"]
        productName = f"""{matchedFeature["source"]}"""
        if matchedFeature["productTyp"] != NULL:
            productName += f"""_{matchedFeature["productTyp"].replace(" ","_")}"""
        productName += f"""_{re.sub("T.+", "", matchedFeature["acquisitio"]).replace("-","")}_id_{matchedFeature['featureId']}"""
        return productName

    def getClipPolygonLayers(
        self,
        rasterLayer: QgsRasterLayer,
        diskSize: float,
        geomWkb: QByteArray,
        context: QgsProcessingContext,
    ) -> List[QgsVectorLayer]:
        geom = QgsGeometry()
        geom.fromWkb(geomWkb)
        polygonLayer = self.layerHandler.createMemoryLayerFromGeometry(
            geom, rasterLayer.crs()
        )
        if diskSize < 2:
            return [polygonLayer]
        bbox = geom.boundingBox()
        outputLayerList = []
        crs = rasterLayer.crs()
        n = math.ceil(diskSize / 2)
        for rect in self.split_rectangle(bbox, n):
            rectGeom = QgsGeometry.fromRect(rect)
            rectLyr = self.layerHandler.createMemoryLayerFromGeometry(rectGeom, crs)
            clippedLyr = self.algRunner.runClip(
                inputLayer=polygonLayer,
                overlayLayer=rectLyr,
                context=context,
                is_child_algorithm=False,
            )
            outputLayerList.append(clippedLyr)
        return outputLayerList

    @staticmethod
    def split_rectangle(rect: QgsRectangle, n: int) -> List[QgsRectangle]:
        """
        Splits a QgsRectangle into n equal parts along its largest dimension.

        :param rect: QgsRectangle to be split.
        :param n: Number of parts to split the rectangle into.
        :return: List of QgsRectangle objects representing the split parts.
        """
        # Calculate the width and height of the rectangle
        width = rect.width()
        height = rect.height()

        # Determine the largest dimension
        if width > height:
            # Split along the horizontal dimension
            part_width = width / n
            parts = []
            for i in range(n):
                part_rect = QgsRectangle(
                    rect.xMinimum() + i * part_width,
                    rect.yMinimum(),
                    rect.xMinimum() + (i + 1) * part_width,
                    rect.yMaximum(),
                )
                parts.append(part_rect)
        else:
            # Split along the vertical dimension
            part_height = height / n
            parts = []
            for i in range(n):
                part_rect = QgsRectangle(
                    rect.xMinimum(),
                    rect.yMinimum() + i * part_height,
                    rect.xMaximum(),
                    rect.yMinimum() + (i + 1) * part_height,
                )
                parts.append(part_rect)

        return parts

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
        for shp in itertools.chain.from_iterable(
            [Path(self.tempFolder).rglob("*.shp"), Path(inputFolder).rglob("*.shp")]
        ):
            if "_SEAMLINES_SHAPE" in str(shp):
                key = str(shp.name).replace(".shp", "").replace("_SEAMLINES_SHAPE", "")
                shapefilesDict[key]["SEAMLINES_SHAPE"] = QgsVectorLayer(
                    str(shp), key, "ogr"
                )
                shapefilesDict[key]["FEAT_DICT"] = dict()
                for feat in shapefilesDict[key]["SEAMLINES_SHAPE"].getFeatures():
                    geom = feat.geometry()
                    geomWkb = geom.asWkb()
                    shapefilesDict[key]["FEAT_DICT"][geomWkb] = feat
            elif "_TILE_SHAPE" in str(shp):
                key = str(shp.name).replace(".shp", "").replace("_TILE_SHAPE", "")
                shapefilesDict[key]["TILE_SHAPE"] = QgsVectorLayer(str(shp), key, "ogr")

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
        for current, (key, valueDict) in enumerate(self.shapefilesDict.items()):
            if feedback.isCanceled():
                break
            if "SEAMLINES_SHAPE" not in valueDict or "TILE_SHAPE" not in valueDict:
                continue
            if (
                valueDict["SEAMLINES_SHAPE"].hasSpatialIndex()
                != QgsFeatureSource.SpatialIndexPresence.SpatialIndexPresent
            ):
                self.algRunner.runCreateSpatialIndex(
                    inputLyr=valueDict["SEAMLINES_SHAPE"],
                    context=context,
                    is_child_algorithm=True,
                )
            if feedback.isCanceled():
                break
            if (
                valueDict["TILE_SHAPE"].hasSpatialIndex()
                != QgsFeatureSource.SpatialIndexPresence.SpatialIndexPresent
            ):
                self.algRunner.runCreateSpatialIndex(
                    inputLyr=valueDict["TILE_SHAPE"],
                    context=context,
                    is_child_algorithm=True,
                )
            if feedback.isCanceled():
                break
            joinnedSeamline = self.algRunner.runJoinAttributesByLocation(
                inputLyr=valueDict["SEAMLINES_SHAPE"],
                joinLyr=valueDict["TILE_SHAPE"],
                predicateList=[AlgRunner.Intersects],
                method=0,
                context=context,
            )
            if feedback.isCanceled():
                break
            for feat in joinnedSeamline.getFeatures():
                if feedback.isCanceled():
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
        productName: str,
        imageSensor: str,
    ) -> None:
        extent = rasterLayer.extent()
        # prefix = "".join(re.findall(r"R\d+C\d+", rasterLayer.name()))
        substitutions = {
            "X_MIN": f"{extent.xMinimum()}",
            "X_MAX": f"{extent.xMaximum()}",
            "Y_MIN": f"{extent.yMinimum()}",
            "Y_MAX": f"{extent.xMaximum()}",
            "NOME_PRODUTO": productName,
            "DATA_IMAGEM": re.sub("T.+", "", matchedFeature["acquisitio"]),
            "SENSOR_IMAGEM": imageSensor,
        }
        with open(self.xml_template_path, "r") as f:
            xmlstring = f.read()
        pattern = re.compile(r"{{([^{}]+)}}")
        xmlstring = re.sub(pattern, lambda m: substitutions[m.group(1)], xmlstring)
        with open(output_xml_file, "w") as f:
            f.write(xmlstring)

    def cleanupTempFolder(self):
        del self.shapefilesDict
        del self.inputFilesDict
        del self.relatedPolygonsDict
        folder_path = Path(self.tempFolder)
        if not folder_path.exists():
            return
        shutil.rmtree(folder_path)

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
