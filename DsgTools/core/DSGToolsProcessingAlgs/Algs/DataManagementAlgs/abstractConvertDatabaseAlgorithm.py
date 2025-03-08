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
from PyQt5.QtCore import QVariant, QDateTime
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DbTools.dbConversionHandler import (
    FeatureProcessor,
    MappingFeatureProcessor,
    convert_features,
)
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import (
    LayerLoaderFactory,
)

from qgis.core import (
    QgsProcessingException,
    QgsProviderConnectionException,
    QgsProviderRegistry,
    QgsProcessingAlgorithm,
    QgsDataSourceUri,
    QgsProcessingMultiStepFeedback,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessingContext,
    QgsProcessingFeatureSource,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes,
)
from qgis.utils import iface

from DsgTools.core.dsgEnums import DsgEnums


class AbstractDatabaseAlgorithm(QgsProcessingAlgorithm):
    def flags(self):
        return (
            super().flags()
            | QgsProcessingAlgorithm.FlagNotAvailableInStandaloneTool
            | QgsProcessingAlgorithm.FlagRequiresProject
            | QgsProcessingAlgorithm.FlagNoThreading
        )

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
        newFeat["layer_name"] = featMap.get(
            "layer_name_original", featMap.get("layer_name", None)
        )
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
            inputParamList,
            addToCanvas=addToCanvas,
            uniqueLoad=True,
            feedback=multiStepFeedback,
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
            clippedLyr = self.clipAndReprojectInputLayer(
                lyr, geographicBoundLyr, outputCrs, context, multiStepFeedback
            )
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

    def clipAndReprojectInputLayer(
        self,
        lyr: QgsVectorLayer,
        geographicBoundLyr: QgsVectorLayer,
        outputCrs: QgsCoordinateReferenceSystem,
        context: QgsProcessingContext,
        multiStepFeedback: QgsProcessingMultiStepFeedback,
    ) -> QgsVectorLayer:
        subMultiStepFeedback = (
            QgsProcessingMultiStepFeedback(
                geographicBoundLyr.featureCount() + 1, multiStepFeedback
            )
            if multiStepFeedback is not None
            else None
        )
        if (
            geographicBoundLyr is None
            or geographicBoundLyr.featureCount() == 0
            or lyr.name() in ["aux_moldura_a", "aux_moldura_area_continua_a"]
        ):
            return self.algRunner.runMergeVectorLayers(
                inputList=[lyr],
                context=context,
                feedback=subMultiStepFeedback,
                crs=outputCrs,
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
            subMultiStepFeedback.setCurrentStep(current + 1)
        clippedLyr = self.algRunner.runMergeVectorLayers(
            inputList=clipList,
            context=context,
            feedback=subMultiStepFeedback,
            crs=outputCrs,
        )
        return clippedLyr

    def buildOutputSinks(
        self,
        parameters: Dict[str, Any],
        context: QgsProcessingContext,
        outputCrs: QgsCoordinateReferenceSystem,
    ) -> None:
        self.point_flag_sink, self.point_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_POINT,
            context,
            self.fields,
            QgsWkbTypes.Point,
            outputCrs,
        )
        self.line_flag_sink, self.line_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_LINE,
            context,
            self.fields,
            QgsWkbTypes.LineString,
            outputCrs,
        )
        self.poly_flag_sink, self.poly_flag_id = self.parameterAsSink(
            parameters,
            self.NOT_CONVERTED_POLYGON,
            context,
            self.fields,
            QgsWkbTypes.Polygon,
            outputCrs,
        )
        self.flagSinkDict = {
            QgsWkbTypes.Point: self.point_flag_sink,
            QgsWkbTypes.MultiPoint: self.point_flag_sink,
            QgsWkbTypes.LineString: self.line_flag_sink,
            QgsWkbTypes.MultiLineString: self.line_flag_sink,
            QgsWkbTypes.Polygon: self.poly_flag_sink,
            QgsWkbTypes.MultiPolygon: self.poly_flag_sink,
        }

    def convertFeaturesWithConversionMaps(
        self,
        conversionMapList: List[str],
        clippedLayerDict: Dict[str, QgsVectorLayer],
        feedback: QgsProcessingFeedback,
    ) -> Dict[str, List[Dict[str, Any]]]:
        multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(conversionMapList), feedback
        )
        currentStep = 0
        nStepsOnText = len(conversionMapList) if len(conversionMapList) > 0 else 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr(f"Converting Features: step 1/{nStepsOnText}")
            )
        firstConversionData = (
            conversionMapList[0] if len(conversionMapList) > 0 else None
        )
        featureProcessor = (
            MappingFeatureProcessor(
                mappingDictPath=firstConversionData["conversionJson"],
                mappingType=firstConversionData["mode"],
            )
            if firstConversionData is not None
            else FeatureProcessor()
        )
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
        for currentConversionStep, conversionData in enumerate(
            conversionMapList[1::], start=2
        ):
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
                multiStepFeedback.pushInfo(
                    self.tr(
                        f"Converting Features: step {currentConversionStep}/{len(conversionMapList)}"
                    )
                )
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
        return convertedFeatureDict
