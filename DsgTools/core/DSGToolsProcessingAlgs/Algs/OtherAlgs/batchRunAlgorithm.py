# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-10-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsDataSourceUri,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterString,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterMultipleLayers,
    QgsWkbTypes,
    QgsProcessingUtils,
    QgsProject,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsVectorLayerUtils,
    QgsProcessingMultiStepFeedback,
    QgsFields,
    QgsField,
)


class BatchRunAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    INPUT_LAYER_PARAMETER_NAME = "INPUT_LAYER_PARAMETER_NAME"
    ALG_NAME = "ALG_NAME"
    PARAMETER_DICT = "PARAMETER_DICT"
    OUTPUT_LAYER_PARAMETER_NAME = "OUTPUT_LAYER_PARAMETER_NAME"
    OUTPUT = "OUTPUT"

    def __init__(self):
        super(BatchRunAlgorithm, self).__init__()
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
                defaultValue="FLAGS",
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
        layerCsv = self.parameterAsString(parameters, self.INPUTLAYERS, context)
        algParameterDict = self.loadAlgorithmParametersDict(
            parameters, context, feedback
        )
        algName = self.parameterAsString(parameters, self.ALG_NAME, context)
        inputKey = self.parameterAsString(
            parameters, self.INPUT_LAYER_PARAMETER_NAME, context
        )
        outputKey = self.parameterAsString(
            parameters, self.OUTPUT_LAYER_PARAMETER_NAME, context
        )
        layerNameList = layerCsv.split(",")
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
            return {"OUTPUT": flag_id}
        layerList = AlgRunner().runStringCsvToLayerList(layerCsv, context)
        nSteps = len(layerList)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        for idx, layer_id in enumerate(layerList):
            layer = QgsProcessingUtils.mapLayerFromString(layer_id, context)
            layerName = layer.name()
            multiStepFeedback.setCurrentStep(idx)
            multiStepFeedback.pushInfo(
                self.tr(
                    "Step {idx}/{total}: Running algorithm {algName} on {layerName}"
                ).format(idx=idx, total=nSteps, algName=algName, layerName=layerName)
            )
            if layer is None:
                multiStepFeedback.pushInfo(
                    self.tr("Layer {layerName} not found. Skipping step.").format(
                        layerName=layerName
                    )
                )
                continue

            currentDict = dict(algParameterDict)  # copy of the dict
            currentDict[inputKey] = layerName
            output = self.runProcessingAlg(
                algName,
                outputKey,
                currentDict,
                context=context,
                feedback=multiStepFeedback,
            )
            outputLyr = (
                QgsProcessingUtils.mapLayerFromString(output, context)
                if isinstance(output, str)
                else output
            )
            if outputLyr is None:
                continue
            if self.flagSink is None:
                self.prepareFlagSink(parameters, outputLyr, context)
            self.flagFeatures(outputLyr, algName, layerName, context)
        if self.flag_id is None:
            _, self.flag_id = self.parameterAsSink(
                parameters,
                self.OUTPUT,
                context,
                self.flagFields,
                QgsWkbTypes.Point,
                QgsProject.instance().crs(),
            )
        return {self.OUTPUT: self.flag_id}

    def loadAlgorithmParametersDict(self, parameters, context, feedback):
        rules_text = self.parameterAsString(parameters, self.PARAMETER_DICT, context)
        feedback.pushInfo(rules_text)
        return json.loads(rules_text)

    def runProcessingAlg(self, algName, outputKey, parameters, context, feedback):
        output = processing.run(algName, parameters, context=context, feedback=feedback)
        return output[outputKey] if outputKey else None

    def flagFeatures(self, outputLyr, algName, inputLyrName, context):
        for feat in outputLyr.getFeatures():
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
        return "batchrunalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Batch Run Algorithm")

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
        return QCoreApplication.translate("BatchRunAlgorithm", string)

    def createInstance(self):
        return BatchRunAlgorithm()
