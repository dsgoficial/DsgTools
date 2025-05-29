# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-02-01
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

from PyQt5.QtCore import QCoreApplication
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.PyQt.QtCore import QVariant
import json, processing
import gc
from qgis.core import (
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsProcessingParameterString,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsProcessingUtils,
    QgsProject,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsFields,
    QgsField,
    QgsProcessingParameterVectorLayer,
    QgsProcessing,
    QgsProcessingParameterEnum,
)


class BatchRunAlgorithmWithGeographicBoundsConstraint(QgsProcessingAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    INPUT_LAYER_PARAMETER_NAME = "INPUT_LAYER_PARAMETER_NAME"
    ALG_NAME = "ALG_NAME"
    PARAMETER_DICT = "PARAMETER_DICT"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    GEOGRAPHIC_BOUNDARY_PARAMETER_NAME = "GEOGRAPHIC_BOUNDARY_PARAMETER_NAME"
    MODE = "MODE"
    OUTPUT_LAYER_PARAMETER_NAME = "OUTPUT_LAYER_PARAMETER_NAME"
    OUTPUT = "OUTPUT"

    def __init__(self):
        super(BatchRunAlgorithmWithGeographicBoundsConstraint, self).__init__()
        self.flagSink = None
        self.flag_id = None
        self.flagFields = QgsFields()
        self.flagFields.append(QgsField("alg_name", QVariant.String))
        self.flagFields.append(QgsField("layer_name", QVariant.String))

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUTLAYERS, self.tr("Comma separated Input Layer Names")
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.ALG_NAME, self.tr("Name of the algorithm with provider")
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_LAYER_PARAMETER_NAME, self.tr("Name of the key of the input")
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.GEOGRAPHIC_BOUNDARY_PARAMETER_NAME,
                self.tr("Name of the key of the geographic boundary"),
                optional=True,
            )
        )
        self.modes = [
            self.tr("Only process algorithm"),
            self.tr(
                "Filter outputs: consider only features that intersects the geographic boundary"
            ),
            self.tr(
                "Filter outputs: consider only features that are within the geographic boundary"
            ),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.MODE, self.tr("Mode"), options=self.modes, defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.PARAMETER_DICT,
                description=self.tr("Json parameter dict"),
                multiLine=True,
                defaultValue="{}",
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_LAYER_PARAMETER_NAME,
                self.tr("Output layer parameter name"),
                # defaultValue="FLAGS",
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Batch run output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        gc.collect()
        gc.disable()
        layerCsv = self.parameterAsString(parameters, self.INPUTLAYERS, context)
        algParameterDict = self.loadAlgorithmParametersDict(parameters, context)
        algName = self.parameterAsString(parameters, self.ALG_NAME, context)
        inputKey = self.parameterAsString(
            parameters, self.INPUT_LAYER_PARAMETER_NAME, context
        )
        outputKey = self.parameterAsString(
            parameters, self.OUTPUT_LAYER_PARAMETER_NAME, context
        )
        geographicBoundaryLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        geographicBoundaryKey = self.parameterAsString(
            parameters, self.GEOGRAPHIC_BOUNDARY_PARAMETER_NAME, context
        )
        self.mode = self.parameterAsEnum(parameters, self.MODE, context)
        layerNameList = layerCsv.split(",") if layerCsv != "" else []
        nSteps = len(layerNameList)
        if not nSteps:
            _, flag_id = self.parameterAsSink(
                parameters,
                self.OUTPUT,
                context,
                self.flagFields,
                QgsWkbTypes.Point,
                QgsProject.instance().crs(),
            )
            gc.enable()
            gc.collect()
            return {"OUTPUT": flag_id}
        layerList = AlgRunner().runStringCsvToLayerList(layerCsv, context)
        nSteps = len(layerList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        for idx, layer_id in enumerate(layerList):
            if feedback.isCanceled():
                break
            layer = QgsProcessingUtils.mapLayerFromString(layer_id, context)
            layerName = layer.name()
            multiStepFeedback.setCurrentStep(idx)
            multiStepFeedback.pushInfo(
                self.tr(
                    f"Step {idx+1}/{nSteps}: Running algorithm {algName} on {layerName}"
                )
            )
            if layer is None:
                multiStepFeedback.pushInfo(
                    self.tr(f"Layer {layerName} not found. Skipping step.")
                )
                continue
            if layer.readOnly():
                multiStepFeedback.pushInfo(
                    self.tr(f"Layer {layerName} is read only. Skipping step.")
                )
                continue
            if layer.featureCount() == 0:
                multiStepFeedback.pushInfo(
                    self.tr(f"Layer {layerName} is empty. Skipping step.")
                )
                continue
            fieldNameSet = set(f.name() for f in layer.fields())
            currentDict = self.parseParameterDict(
                context, algParameterDict, input_id=layer_id, fieldNameSet=fieldNameSet
            )
            currentDict[inputKey] = layer
            if (
                geographicBoundaryLyr is not None
                and geographicBoundaryKey is not None
                and geographicBoundaryKey != ""
            ):
                currentDict[geographicBoundaryKey] = geographicBoundaryLyr
            output = self.runProcessingAlg(
                algName,
                outputKey,
                currentDict,
                context=context,
                feedback=multiStepFeedback,
            )
            if output is None:
                continue
            outputLyr = (
                QgsProcessingUtils.mapLayerFromString(output, context)
                if isinstance(output, str)
                else output
            )
            if outputLyr.featureCount() == 0:
                continue
            if self.flagSink is None:
                self.prepareFlagSink(parameters, outputLyr, context)
            self.flagFeatures(
                outputLyr,
                algName,
                layerName,
                context,
                geographicBoundaryLyr=geographicBoundaryLyr,
            )
        if self.flag_id is None:
            _, self.flag_id = self.parameterAsSink(
                parameters,
                self.OUTPUT,
                context,
                self.flagFields,
                QgsWkbTypes.Point,
                QgsProject.instance().crs(),
            )
        gc.enable()
        gc.collect()
        return {self.OUTPUT: self.flag_id}

    def parseParameterDict(self, context, algParameterDict, input_id, fieldNameSet):
        currentDict = dict(algParameterDict)  # copy of the dict
        for k, v in currentDict.items():
            if not isinstance(v, list):
                continue
            s = set(v).intersection(fieldNameSet)
            if s != set():
                # field list
                currentDict[k] = list(s)
                continue
            if isinstance(v, str):
                if v == "":
                    continue
                if "," in v or "|" in v:
                    outputList = list(
                        filter(
                            lambda x: x != input_id,
                            AlgRunner().runStringCsvToLayerList(",".join(v), context),
                        )
                    )
                    if outputList == []:
                        continue
                    currentDict[k] = outputList[0]
            currentDict[k] = (
                list(
                    filter(
                        lambda x: x != input_id,
                        AlgRunner().runStringCsvToLayerList(",".join(v), context),
                    )
                )
                if len(v) > 0
                else []
            )
        return currentDict

    def loadAlgorithmParametersDict(self, parameters, context):
        rules_text = self.parameterAsString(parameters, self.PARAMETER_DICT, context)
        return json.loads(rules_text)

    def runProcessingAlg(self, algName, outputKey, parameters, context, feedback):
        output = processing.run(algName, parameters, context=context, feedback=feedback)
        return output[outputKey] if outputKey else None

    def flagFeatures(
        self, outputLyr, algName, inputLyrName, context, geographicBoundaryLyr=None
    ):
        lyrToHandle = (
            AlgRunner().runExtractByLocation(
                inputLyr=outputLyr,
                intersectLyr=geographicBoundaryLyr,
                context=context,
                predicate=[
                    AlgRunner.Intersects if self.mode == 1 else AlgRunner.Within
                ],
            )
            if geographicBoundaryLyr is not None and self.mode != 0
            else outputLyr
        )

        for feat in lyrToHandle.getFeatures():
            newFeat = QgsFeature(self.flagFields)
            for field in feat.fields():
                newFeat[field.name()] = feat[field.name()]
            newFeat["alg_name"] = algName
            newFeat["layer_name"] = inputLyrName
            newFeat.setGeometry(feat.geometry())
            self.flagSink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def prepareFlagSink(self, parameters, flagSource, context):
        for field in flagSource.fields():
            self.flagFields.append(field)
        (self.flagSink, self.flag_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            self.flagFields,
            flagSource.wkbType(),
            flagSource.sourceCrs(),
        )
        if self.flagSink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "batchrunalgorithmwithgeographicboundsconstraint"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Batch Run Algorithm With Geographic Bounds Constraint")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Model Helpers")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Model Helpers"

    def tr(self, string):
        return QCoreApplication.translate(
            "BatchRunAlgorithmWithGeographicBoundsConstraint", string
        )

    def createInstance(self):
        return BatchRunAlgorithmWithGeographicBoundsConstraint()
