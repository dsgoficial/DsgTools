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

import fnmatch
import json
from typing import Any, Dict, List, Optional
from PyQt5.QtCore import QVariant, QMetaType, QDateTime
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DbTools.dbConversionHandler import (
    FeatureProcessor,
    MappingFeatureProcessor,
    convert_features,
    write_output_features,
)
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import (
    LayerLoaderFactory,
)
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProviderConnectionException,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsProviderRegistry,
    QgsProject,
    QgsProcessingParameterProviderConnection,
    QgsProcessingAlgorithm,
    QgsProcessingParameterGeometry,
    QgsDataSourceUri,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterType,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingContext,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsProcessingFeatureSource,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsCoordinateReferenceSystem,
)
from qgis.utils import iface

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.dsgEnums import DsgEnums


class ConvertDatabasesAlgorithm(QgsProcessingAlgorithm):
    INPUT_DATABASE = "INPUT_DATABASE"
    INPUT_LAYERS_TO_EXCLUDE = "INPUT_LAYERS_TO_EXCLUDE"
    DESTINATION_DATABASE = "DESTINATION_DATABASE"
    CONVERSION_MAPS_STRUCTURE = "CONVERSION_MAPS_STRUCTURE"
    COMMIT_OUTPUT_FEATURES = "COMMIT_OUTPUT_FEATURES"
    GEOGRAPHIC_BOUNDS = "GEOGRAPHIC_BOUNDS"
    NOT_CONVERTED_POINT = "NOT_CONVERTED_POINT"
    NOT_CONVERTED_LINE = "NOT_CONVERTED_LINE"
    NOT_CONVERTED_POLYGON = "NOT_CONVERTED_POLYGON"

    def flags(self):
        return (
            super().flags()
            | QgsProcessingAlgorithm.FlagNotAvailableInStandaloneTool
            | QgsProcessingAlgorithm.FlagRequiresProject
            | QgsProcessingAlgorithm.FlagNoThreading
        )

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

        destination_db_param = QgsProcessingParameterProviderConnection(
            self.DESTINATION_DATABASE,
            self.tr("Destination Database (connection name)"),
            "postgres",
        )
        self.addParameter(destination_db_param)

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
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic Bounds"),
                [QgsWkbTypes.PolygonGeometry],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.COMMIT_OUTPUT_FEATURES,
                self.tr("Commit converted features to destination layers"),
                defaultValue=False,
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
        destinationConnectionName = self.parameterAsConnectionName(
            parameters, self.DESTINATION_DATABASE, context
        )
        conversionMapList = self.parameterAsConversionMapList(
            parameters, self.CONVERSION_MAPS_STRUCTURE, context
        )
        geographicBoundLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDS, context
        )
        commitChanges = self.parameterAsBool(
            parameters, self.COMMIT_OUTPUT_FEATURES, context
        )
        nSteps = 7 + len(conversionMapList)
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if inputConnectionName == destinationConnectionName:
            raise QgsProcessingException(self.tr("The destination connection must be different than the input connection!"))
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
            return {}
        currentStep += 1
        self.fields = self.fieldsFlag()
        outputCrs = self.getOutputCRS(destinationConnectionName)

        point_flag_sink, point_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_POINT,
            context,
            self.fields,
            QgsWkbTypes.Point,
            outputCrs,
        )
        line_flag_sink, line_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_LINE,
            context,
            self.fields,
            QgsWkbTypes.LineString,
            outputCrs,
        )
        poly_flag_sink, poly_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_POLYGON,
            context,
            self.fields,
            QgsWkbTypes.Polygon,
            outputCrs,
        )
        self.flagSinkDict = {
            QgsWkbTypes.Point: point_flag_sink,
            QgsWkbTypes.MultiPoint: point_flag_sink,
            QgsWkbTypes.LineString: line_flag_sink,
            QgsWkbTypes.MultiLineString: line_flag_sink,
            QgsWkbTypes.Polygon: poly_flag_sink,
            QgsWkbTypes.MultiPolygon: poly_flag_sink,
        }

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Clipping input layer list"))
        clippedLayerDict = self.prepareInputData(
            inputLayerList, geographicBoundLyr, outputCrs, context, multiStepFeedback
        )
        for lyr in inputLayerList:
            QgsProject.instance().removeMapLayer(lyr.id())
        currentStep += 1
        nStepsOnText = len(conversionMapList) if len(conversionMapList) > 0 else 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr(f"Converting Features: step 1/{nStepsOnText}"))
        firstConversionData = conversionMapList[0] if len(conversionMapList) > 0 else None
        featureProcessor = MappingFeatureProcessor(
            mappingDictPath=firstConversionData["conversionJson"],
            mappingType=firstConversionData["mode"],
        ) if firstConversionData is not None else FeatureProcessor()
        convertedFeatureDict = convert_features(
            inputLayerDict={
                lyrName: lyr
                for lyrName, lyr in clippedLayerDict.items()
                if lyr.featureCount() > 0
            },
            featureProcessor=featureProcessor,
            feedback=multiStepFeedback,
            layerNameAttr="layer_name",
        )
        currentStep += 1
        for currentConversionStep, conversionData in enumerate(conversionMapList[1::], start=2):
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
                multiStepFeedback.pushInfo(self.tr(f"Converting Features: step {currentConversionStep}/{len(conversionMapList)}"))
            featureProcessor = MappingFeatureProcessor(
                mappingDictPath=conversionData["conversionJson"],
                mappingType=conversionData["mode"],
            )
            convertedFeatureDict = convert_features(
                inputLayerDict=convertedFeatureDict,
                featureProcessor=featureProcessor,
                feedback=multiStepFeedback,
            )
            currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Loading output layers"))
        destinationLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName=destinationConnectionName,
            feedback=multiStepFeedback,
            context=context,
            layerNameList=list(convertedFeatureDict.keys()),
            addToCanvas=True,
            withElements=False,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Writing to output"))
        outputLayerDict = {lyr.name(): lyr for lyr in destinationLayerList}
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
        multiStepFeedback.setCurrentStep(currentStep)
        if not commitChanges:
            return {
                self.NOT_CONVERTED_POINT: point_flag_id,
                self.NOT_CONVERTED_LINE: line_flag_id,
                self.NOT_CONVERTED_POLYGON: poly_flag_id,
            }
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Commiting changes"))
        stepSize = 100 / len(outputLayerDict)
        for current, (lyrName, lyr) in enumerate(outputLayerDict.items()):
            if multiStepFeedback is not None:
                multiStepFeedback.pushInfo(
                    self.tr(f"Commiting changes for layer {lyrName}")
                )
            lyr.commitChanges()
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return {
            self.NOT_CONVERTED_POINT: point_flag_id,
            self.NOT_CONVERTED_LINE: line_flag_id,
            self.NOT_CONVERTED_POLYGON: poly_flag_id,
        }

    def parameterAsConversionMapList(self, parameters, name, context):
        return parameters[name]

    def fieldsFlag(self) -> QgsFields:
        fields = QgsFields()
        fields.append(QgsField("layer_name", QVariant.String))
        fields.append(QgsField("attribute_map", QVariant.String))
        return fields

    def buildFlagFeat(self, featMap: Dict[str, Any]) -> QgsFeature:
        newFeat = QgsFeature(self.fields)
        geom = featMap.pop("geom")
        newFeat.setGeometry(geom)
        newFeat["layer_name"] = featMap.get("layer_name_original", featMap.get("layer_name", None))
        for k, v in featMap.items():
            if isinstance(v, QDateTime):
                featMap[k] = v.toString()
        newFeat["attribute_map"] = json.dumps(featMap, default=str)
        return newFeat
    
    def getOutputCRS(self, connectionName: str) -> QgsCoordinateReferenceSystem:
        abstractDb = self.getAbstractDb(connectionName)
        srid = abstractDb.findEPSG()
        del abstractDb
        return QgsCoordinateReferenceSystem(int(srid))

    def getLayersFromDbConnectionName(
        self,
        inputConnectionName: str,
        feedback: QgsProcessingFeedback,
        context: QgsProcessingContext,
        layerNameList: Optional[List[QgsVectorLayer]] = None,
        addToCanvas: Optional[bool] = False,
        withElements: Optional[bool] = True,
        layerExclusionFilter: Optional[List[str]] = None,
    ) -> List[QgsVectorLayer]:
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        inputAbstractDb = self.getAbstractDb(inputConnectionName)
        layerLoader = LayerLoaderFactory().makeLoader(iface, inputAbstractDb)
        inputParamList = inputAbstractDb.listGeomClassesFromDatabase(
            withElements=withElements
        )
        if layerNameList is not None and layerNameList != []:
            inputParamList = list(set(inputParamList).intersection(set(layerNameList)))
        inputParamList = list(map(lambda x: x.split(".")[-1], inputParamList))

        if layerExclusionFilter is not None:
            wildCardFilterList = [fi for fi in layerExclusionFilter if "*" in fi]
            wildCardLayersSet = set()
            for wildCardFilter in wildCardFilterList:
                wildCardLayersSet = wildCardLayersSet.union(
                    set(fnmatch.filter(inputParamList, wildCardFilter))
                )
            layerNamesToExclude = (
                set(layerExclusionFilter) - set(wildCardFilterList) | wildCardLayersSet
            )
            inputParamList = list(set(inputParamList) - layerNamesToExclude)
        multiStepFeedback.setCurrentStep(1)
        loadedLayerList = layerLoader.loadLayersInsideProcessing(
            inputParamList, addToCanvas=addToCanvas, uniqueLoad=True, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        if addToCanvas:
            AlgRunner().runDSGToolsGroupLayers(
                inputList=loadedLayerList,
                context=context,
                feedback=multiStepFeedback,
            )
        del inputAbstractDb
        del layerLoader
        return loadedLayerList

    def getAbstractDb(self, inputConnectionName: str) -> AbstractDb:
        try:
            md = QgsProviderRegistry.instance().providerMetadata("postgres")
            conn = md.createConnection(inputConnectionName)
        except QgsProviderConnectionException:
            raise QgsProcessingException(
                self.tr("Could not retrieve connection details for {}").format(
                    inputConnectionName
                )
            )
        uri = QgsDataSourceUri(conn.uri())
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(
            uri.host(),
            int(uri.port()),
            uri.database(),
            uri.username(),
            uri.password(),
        )
        return abstractDb

    def prepareInputData(
        self,
        inputLayerList: List[QgsVectorLayer],
        geographicBoundLyr: QgsProcessingFeatureSource,
        outputCrs: QgsCoordinateReferenceSystem,
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ) -> Dict[str, QgsVectorLayer]:
        outputDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2 * len(inputLayerList), feedback)
            if feedback is not None
            else None
        )
        schema_table_layer_dict = {
            layer.name(): f"{uri.schema()}.{uri.table()}"
            for layer in inputLayerList
            for uri in [QgsDataSourceUri(layer.dataProvider().dataSourceUri())]
        }
        for currentIdx, lyr in enumerate(inputLayerList):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return outputDict
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(2 * currentIdx)
            clippedLyr = self.clipAndReprojectInputLayer(lyr, geographicBoundLyr, outputCrs, context, multiStepFeedback)
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(2 * currentIdx + 1)
            key = schema_table_layer_dict[lyr.name()]
            outputDict[key] = self.algRunner.runCreateFieldWithExpression(
                inputLyr=clippedLyr,
                expression=f"'{key}'",
                fieldType=2,
                fieldName="layer_name",
                feedback=multiStepFeedback,
                context=context,
                is_child_algorithm=False,
            )
        return outputDict

    def clipAndReprojectInputLayer(self, lyr: QgsVectorLayer, geographicBoundLyr: QgsVectorLayer, outputCrs: QgsCoordinateReferenceSystem, context: QgsProcessingContext, multiStepFeedback: QgsProcessingMultiStepFeedback) -> QgsVectorLayer:
        subMultiStepFeedback = QgsProcessingMultiStepFeedback(geographicBoundLyr.featureCount() + 1, multiStepFeedback) if multiStepFeedback is not None else None
        if geographicBoundLyr is None or geographicBoundLyr.featureCount() == 0 or lyr.name() in ["aux_moldura_a", "aux_moldura_area_continua_a"]:
            return self.algRunner.runMergeVectorLayers(
                inputList=[lyr], context=context, feedback=subMultiStepFeedback, crs=outputCrs
            )
        clipList = []
        for current, clipLayer in enumerate(
                self.layerHandler.createMemoryLayerForEachFeature(
                    layer=geographicBoundLyr, context=context
                )
            ):
            if subMultiStepFeedback is not None and subMultiStepFeedback.isCanceled():
                break
            if subMultiStepFeedback is not None:
                subMultiStepFeedback.setCurrentStep(current)
            clipped = self.algRunner.runClip(
                inputLayer=lyr,
                overlayLayer=clipLayer,
                context=context,
                is_child_algorithm=True,
            )
            clipList.append(clipped)
        if subMultiStepFeedback is not None:
            subMultiStepFeedback.setCurrentStep(current+1)
        clippedLyr = self.algRunner.runMergeVectorLayers(
            inputList=clipList, context=context, feedback=subMultiStepFeedback, crs=outputCrs
        )
        return clippedLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "convertdatabasesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Convert Databases")

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
        return QCoreApplication.translate("ConvertDatabasesAlgorithm", string)

    def createInstance(self):
        return ConvertDatabasesAlgorithm()


class ParameterDbConversionType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterDbConversion(name)  # mudar

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.dbConversionWrapper.DbConversionWrapper"
        }  # mudar

    def name(self):
        return QCoreApplication.translate("Processing", "Database Conversion Maps")

    def id(self):
        return "db_conversion_maps"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "A list of database conversion maps. Used in the Convert Database algorithm.",
        )


class ParameterDbConversion(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterDbConversion(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "db_conversion_maps"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return json.dumps(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
