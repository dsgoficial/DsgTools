# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-12-02
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
from pathlib import Path
import shutil
from typing import Dict, List
import zipfile
from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.abstractConvertDatabaseAlgorithm import AbstractDatabaseAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.conversionParameterTypes import ParameterDbConversion
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DbTools.dbConversionHandler import (
    write_output_features,
)

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingException,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsProcessingParameterProviderConnection,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterString,
    QgsFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsProcessingParameterField,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterCrs,
    QgsProcessingParameterFile,
)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler


class ExportPostGISDataToShapefile(AbstractDatabaseAlgorithm):
    INPUT_DATABASE = "INPUT_DATABASE"
    INPUT_LAYERS_TO_EXCLUDE = "INPUT_LAYERS_TO_EXCLUDE"
    CONVERSION_MAPS_STRUCTURE = "CONVERSION_MAPS_STRUCTURE"
    TEMPLATE_SHAPEFILES_FOLDER = "TEMPLATE_SHAPEFILES_FOLDER"
    OUTPUT_CRS = "OUPUT_CRS"
    GEOGRAPHIC_BOUNDS = "GEOGRAPHIC_BOUNDS"
    GEOGRAPHIC_BOUNDS_NAME_FIELD = "GEOGRAPHIC_BOUNDS_NAME_FIELD"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    EXPORT_ZIP = "EXPORT_ZIP"
    LOAD_EXPORTED_SHAPEFILES = "LOAD_EXPORTED_SHAPEFILES"
    NOT_CONVERTED_POINT = "NOT_CONVERTED_POINT"
    NOT_CONVERTED_LINE = "NOT_CONVERTED_LINE"
    NOT_CONVERTED_POLYGON = "NOT_CONVERTED_POLYGON"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        origin_db_param = QgsProcessingParameterProviderConnection(
            self.INPUT_DATABASE,
            self.tr("Input Database (connection name)"),
            "postgres",
        )
        self.addParameter(origin_db_param)

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_LAYERS_TO_EXCLUDE,
                description=self.tr(
                    "Input layers to be excluded (csv format, can use * patterns)"
                ),
                multiLine=False,
                defaultValue="aux_moldura_area_continua_a,delimitador*,centroide*",
                optional=True,
            )
        )

        hierarchy = ParameterDbConversion(
            self.CONVERSION_MAPS_STRUCTURE, description=self.tr("Conversion maps")
        )
        hierarchy.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.dbConversionWrapper.DbConversionWrapper"
            }
        )
        self.addParameter(hierarchy)
        
        self.addParameter(
            QgsProcessingParameterFile(
                self.TEMPLATE_SHAPEFILES_FOLDER,
                self.tr("Template Shapefiles Folder"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterCrs(
                self.OUTPUT_CRS,
                self.tr("Output CRS"),
                defaultValue=QgsCoordinateReferenceSystem(4674),
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic Bounds"),
                [QgsWkbTypes.PolygonGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic Bounds"),
                [QgsWkbTypes.PolygonGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.GEOGRAPHIC_BOUNDS_NAME_FIELD,
                self.tr("MI"),
                parentLayerParameterName=self.GEOGRAPHIC_BOUNDS,
                type=QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.EXPORT_ZIP,
                self.tr("Export .zip of each generated folder"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_EXPORTED_SHAPEFILES,
                self.tr("Load exported shapefiles"),
                defaultValue=True,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                self.tr('Output folder'),
                
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_POINT,
                self.tr("Points not converted"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_LINE,
                self.tr("Lines not converted"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_POLYGON,
                self.tr("Polygons not converted"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputConnectionName = self.parameterAsConnectionName(
            parameters, self.INPUT_DATABASE, context
        )
        layerExclusionFilter = self.parameterAsString(
            parameters, self.INPUT_LAYERS_TO_EXCLUDE, context
        )
        layerExclusionFilter = (
            layerExclusionFilter.split(",") if layerExclusionFilter else None
        )
        
        conversionMapList = self.parameterAsConversionMapList(
            parameters, self.CONVERSION_MAPS_STRUCTURE, context
        )
        geographicBoundLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDS, context
        )
        miField = self.parameterAsFields(parameters, self.GEOGRAPHIC_BOUNDS_NAME_FIELD, context)[0]
        templatePath = self.parameterAsString(
            parameters, self.TEMPLATE_SHAPEFILES_FOLDER, context
        )
        zipOutputs = self.parameterAsBool(
            parameters, self.EXPORT_ZIP, context
        )
        loadExportedShapefiles = self.parameterAsBool(
            parameters, self.LOAD_EXPORTED_SHAPEFILES, context
        )
        outputFolder = self.parameterAsString(
            parameters,
            self.OUTPUT_FOLDER,
            context
        )
        if len(conversionMapList) == 0:
            raise QgsProcessingException(self.tr("There must be at least one conversion map selected."))
        
        nGeographicBoundsFeats = geographicBoundLyr.featureCount()
        if nGeographicBoundsFeats == 0:
            raise QgsProcessingException(self.tr("There must be at least one feature on the geographic bounds layer"))
        nSteps = 1 + nGeographicBoundsFeats * (7 + loadExportedShapefiles)
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Loading layers with elements from input database")
            )
        inputLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName,
            feedback=multiStepFeedback,
            context=context,
            layerExclusionFilter=layerExclusionFilter,
        )
        if len(inputLayerList) == 0:
            raise QgsProcessingException(self.tr("There must be at least one layer with features in the input database"))
        currentStep += 1
        self.fields = self.fieldsFlag()
        outputCrs = self.parameterAsCrs(parameters, self.OUTPUT_CRS, context)

        self.buildOutputSinks(parameters, context, outputCrs)
        templateFileDict = self.buildTemplateFileDict(templatePath=templatePath)
        
        for i, geographicBoundsFeat in enumerate(geographicBoundLyr.getFeatures(), start=1):
            localGeographicBoundLyr = self.layerHandler.createMemoryLayerWithFeature(
                layer=geographicBoundLyr, feat=geographicBoundsFeat, context=context
            )
            destinationPath = Path(outputFolder) / geographicBoundsFeat[miField]
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
                multiStepFeedback.setProgressText(self.tr(f"Processing MI {geographicBoundsFeat[miField]} ({i}/{nGeographicBoundsFeats})"))
            clippedLayerDict = self.prepareInputData(
                inputLayerList, localGeographicBoundLyr, outputCrs, context, multiStepFeedback
            )
            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            convertedFeatureDict = self.convertFeaturesWithConversionMaps(conversionMapList, clippedLayerDict, multiStepFeedback)
            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            outputLayerDict = self.copyFilesFromTemplate(
                layerNameList=list(convertedFeatureDict.keys()),
                destinationPath=destinationPath,
                templateFileDict=templateFileDict,
                outputCrs=outputCrs
            )
            
            if loadExportedShapefiles:
                currentStep += 1
                if multiStepFeedback is not None:
                    multiStepFeedback.setCurrentStep(currentStep)
                self.algRunner.runDSGToolsLoadShapefile(
                    inputFolder=str(destinationPath),
                    context=context,
                    feedback=multiStepFeedback
                )
            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            notConvertedDict = write_output_features(
                {k.split(".")[-1]: v for k, v in convertedFeatureDict.items()},
                outputLayerDict=outputLayerDict,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)

            if len(notConvertedDict) > 0:
                stepSize = 100 / len(notConvertedDict)
                for geomType, featDictList in notConvertedDict.items():
                    if multiStepFeedback.isCanceled():
                        break
                    list(
                        map(
                            lambda x: self.flagSinkDict[geomType].addFeature(
                                self.buildFlagFeat(x), QgsFeatureSink.FastInsert
                            ),
                            featDictList,
                        )
                    )

            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
                multiStepFeedback.pushInfo(self.tr("Commiting changes"))
            stepSize = 100 / len(outputLayerDict)
            for current, (lyrName, lyr) in enumerate(outputLayerDict.items()):
                lyr.commitChanges()
                if multiStepFeedback is not None:
                    multiStepFeedback.setProgress(current * stepSize)
            
            currentStep += 1
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            if zipOutputs:
                self.buildZipOutputs(
                    sourceFolder=destinationPath,
                    destinationPath=Path(outputFolder) / f"{geographicBoundsFeat[miField]}.zip",
                )
            

        return {
                self.OUTPUT_FOLDER: outputFolder,
                self.NOT_CONVERTED_POINT: self.point_flag_id,
                self.NOT_CONVERTED_LINE: self.line_flag_id,
                self.NOT_CONVERTED_POLYGON: self.poly_flag_id,
            }
    
    def buildTemplateFileDict(self, templatePath: str) -> Dict[str, List[Path]]:
        templateFileDict = defaultdict(list)
        p = Path(templatePath)
        extensions = ['.shp', '.shx', '.prj', '.dbf', '.sbn', '.sbx', '.cpg', '.xml']
        for f in p.glob("*"):
            if f.suffix not in extensions:
                continue
            templateFileDict[f.stem].append(f)
        return templateFileDict
    
    def copyFilesFromTemplate(self, layerNameList: List[str], destinationPath: str, templateFileDict: Dict[str, List[str]], outputCrs: QgsCoordinateReferenceSystem) -> Dict[str, QgsVectorLayer]:
        outputDict = dict()
        destinationDir = Path(destinationPath)
        destinationDir.mkdir(parents=True, exist_ok=True)
        for layerName in layerNameList:
            for filePath in templateFileDict[layerName]:
                destinationFile = destinationDir / filePath.name
                shutil.copy(filePath, destinationFile)
            lyr = QgsVectorLayer(str(destinationDir / f"{layerName}.shp"), layerName, 'ogr')
            lyr.setCrs(outputCrs)
            outputDict[layerName] = lyr
        return outputDict
    
    def buildZipOutputs(self, sourceFolder, destinationPath: str):
        with zipfile.ZipFile(destinationPath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in sourceFolder.rglob("*"):
                zipf.write(file, file.relative_to(sourceFolder.parent))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "exportdatabasetoshapefile"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Export PostGIS data to Shapefile")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Data Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Data Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ExportPostGISDataToShapefile", string)

    def createInstance(self):
        return ExportPostGISDataToShapefile()
