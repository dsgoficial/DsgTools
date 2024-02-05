# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-x
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
from collections import Counter, defaultdict

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFile,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterString,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class RuleStatisticsAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    RULEFILE = "RULEFILE"
    RULEDATA = "RULEDATA"
    OUTPUT = "OUTPUT"
    UNUSUAL_ATTRIBUTES = "UNUSUAL_ATTRIBUTES"
    FLAGS = "FLAGS"

    def __init__(self):
        super(RuleStatisticsAlgorithm, self).__init__()

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS, "Camadas de entrada :"
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.RULEFILE,
                description='Arquivo ".json" com regras :',
                defaultValue=".json",
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.RULEDATA,
                description='Regras no formato "json" :',
                multiLine=True,
                defaultValue="{}",
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.UNUSUAL_ATTRIBUTES, self.tr("Atributos incomuns")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.algRunner = AlgRunner()
        layers_list = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        inputLyrNamesWithSchemaList = [
            f"{lyr.dataProvider().uri().schema()}.{lyr.dataProvider().uri().table()}"
            for lyr in layers_list
        ]
        input_data = self.load_rules_from_parameters(parameters)
        rows = self.buildRuleDict(input_data[0], inputLyrNamesWithSchemaList)
        fields = QgsFields()
        fields.append(QgsField("layer_name", QVariant.String))
        fields.append(QgsField("type", QVariant.String))
        fields.append(QgsField("number_of_errors", QVariant.Int))
        (flagSink, flag_id) = self.parameterAsSink(
            parameters,
            self.FLAGS,
            context,
            fields,
            geometryType=QgsWkbTypes.NoGeometry,
        )
        (unusualSink, unusual_output_id) = self.parameterAsSink(
            parameters,
            self.UNUSUAL_ATTRIBUTES,
            context,
            fields,
            geometryType=QgsWkbTypes.NoGeometry,
        )
        flagOutputDict = {
            "Atributo incomum": unusualSink,
            "Preencher atributo": flagSink,
            "Atributo incorreto": flagSink,
        }
        result = {}
        counterDict = defaultdict(Counter)
        for i, row in enumerate(rows):
            if not row["type"] in result:
                result[row["type"]] = []
            failed = self.check_rules_on_layers(
                row["attribute"],
                row["rule"],
                [
                    lyr
                    for lyr in layers_list
                    if f"{lyr.dataProvider().uri().schema()}.{lyr.dataProvider().uri().table()}"
                    in row["layers"]
                ],
            )
            counterDict[row["type"]].update(failed)
            result[row["type"]].append(failed)
        if not input_data:
            self.print_log(
                "Carregue um arquivos com as Regras ou insira as Regras!", feedback
            )
            return {
                self.OUTPUT: "",
                self.FLAGS: flag_id,
                self.UNUSUAL_ATTRIBUTES: unusual_output_id,
            }
        for counterType, lyrCounter in counterDict.items():
            for lyrName, lyrCount in lyrCounter.items():
                if lyrCount == 0:
                    continue
                newFeat = QgsFeature(fields)
                newFeat["layer_name"] = lyrName
                newFeat["type"] = counterType
                newFeat["number_of_errors"] = lyrCount
                sink = flagOutputDict.get(counterType, flagSink)
                sink.addFeature(newFeat)
        return {
            self.OUTPUT: self.format_output_result(result),
            self.FLAGS: flag_id,
            self.UNUSUAL_ATTRIBUTES: unusual_output_id,
        }

    def buildRuleDict(self, inputData, inputLyrNamesWithSchemaList):
        ruleDict = []
        styleDict = {
            style["tipo_estilo"]: {
                "corRgb": list(map(int, style["cor_rgb"].split(","))),
                "rank": idx,
            }
            for idx, style in enumerate(inputData["grupo_estilo"])
        }
        for rule in inputData["regras"]:
            lyrSet = self.getLayerNames(rule["camadas"], inputLyrNamesWithSchemaList)
            ruleDict.append(
                {
                    "type": rule["tipo_estilo"],
                    "name": rule["descricao"],
                    "rule": rule["regra"],
                    "attribute": rule["atributo"],
                    "layers": list(lyrSet),
                }
            )
        return ruleDict

    def getLayerNames(self, filterList, nameList):
        outputSet = set()
        wildCardFilterList = [
            filterItem for filterItem in filterList if "*" in filterItem
        ]
        for wildCardFilter in wildCardFilterList:
            outputSet = outputSet.union(set(fnmatch.filter(nameList, wildCardFilter)))
        outputSet = outputSet.union(
            set(name for name in nameList if name in filterList)
        )
        return outputSet

    def print_log(self, number, text, feedback):
        feedback.pushInfo(
            "{0}{1}LOG START - {2}{1}{0}\n\n".format("*" * 10, " " * 3, number + 1)
        )
        feedback.pushInfo(text)
        feedback.pushInfo(
            "{0}{1}LOG END - {2}{1}{0}\n\n".format("*" * 10, " " * 3, number + 1)
        )

    def load_rules_from_parameters(self, parameters):
        rules_input = []
        rules_path = parameters[self.RULEFILE]
        rules_text = parameters[self.RULEDATA]
        if rules_path and rules_path != ".json":
            with open(rules_path, "r") as f:
                rules_input.append(json.load(f))
        if rules_text and rules_text != "{}":
            rules_input.append(json.loads(rules_text))
        return rules_input

    def hasAttribute(self, attribute, lyr):
        return (
            len(
                [c for c in lyr.attributeTableConfig().columns() if c.name == attribute]
            )
            != 0
        )

    def check_rules_on_layers(self, attribute, rule, layers):
        failed = {}
        context = QgsProcessingContext()
        for lyr in layers:
            if not self.hasAttribute(attribute, lyr):
                continue
            outputLyr = self.algRunner.runFilterExpression(
                inputLyr=lyr,
                expression=rule,
                context=context,
            )
            count = outputLyr.featureCount()
            failed[lyr.name()] = count != 0
        return failed

    def format_output_result(self, result):
        html = ""
        for ruleName in sorted(result.keys()):
            row = "[REGRAS] : {0}\n\n".format(ruleName)
            html += row
            failedLayers = []
            for layers in result[ruleName]:
                for layerName in layers:
                    failed = layers[layerName]
                    if not failed:
                        continue
                    if layerName in failedLayers:
                        continue
                    failedLayers.append(layerName)
            rows = ""
            if failedLayers:
                for layerName in sorted(failedLayers):
                    rows += "{0}\n\n".format(layerName)
            else:
                rows = "As camadas passaram em todas as regras.\n\n"
            html += rows
        return html

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "rulestatistics"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Rule Statistics")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Attribute Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Attribute Handling"

    def tr(self, string):
        return QCoreApplication.translate("RuleStatisticsAlgorithm", string)

    def createInstance(self):
        return RuleStatisticsAlgorithm()
