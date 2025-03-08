# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-11-06
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jean Michael Estevez Alvarez - Brazilian Army
        email                : jeanalvarez@id.uff.br
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

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsExpression,
    QgsFeatureSink,
    QgsVectorLayer,
    QgsFeatureRequest,
)
from qgis import processing

from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class ExportFeaturesByAttributeAlgorithm(QgsProcessingAlgorithm):
    """Algorithm to export features based on attribute filtering."""

    INPUT = "INPUT"
    FIELD = "FIELD"
    OPERATOR = "OPERATOR"
    VALUE = "VALUE"
    OUTPUT = "OUTPUT"

    OPERATORS = [
        "=",
        "<>",
        ">",
        ">=",
        "<",
        "<=",
        "begins with",
        "contains",
        "is null",
        "is not null",
        "does not contain",
    ]
    STRING_OPERATORS = ["begins with", "contains", "does not contain"]

    def initAlgorithm(self, config=None):
        """Initializes algorithm parameters."""
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input layer"), [QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                self.tr("Selection attribute"),
                parentLayerParameterName=self.INPUT,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATOR,
                self.tr("Operator"),
                options=self.OPERATORS,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(self.VALUE, self.tr("Value"), optional=True)
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """Processes the algorithm."""
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        fieldName = self.parameterAsString(parameters, self.FIELD, context)
        operator = self.OPERATORS[
            self.parameterAsEnum(parameters, self.OPERATOR, context)
        ]
        value = self.parameterAsString(parameters, self.VALUE, context)

        fields = layer.fields() if layer else QgsFields()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            layer.wkbType() if layer else QgsWkbTypes.NoGeometry,
            layer.sourceCrs() if layer else None,
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        if layer is None:
            raise QgsProcessingException("Camada inválida ou não encontrada.")

        if fieldName not in layer.fields().names():
            feedback.pushInfo(
                f"O atributo '{fieldName}' não foi encontrado na camada. Nenhuma exportação realizada."
            )
            return {self.OUTPUT: dest_id}

        field_ref = QgsExpression.quotedColumnRef(fieldName)
        if operator == "is null":
            expression_string = f"{field_ref} IS NULL"
        elif operator == "is not null":
            expression_string = f"{field_ref} IS NOT NULL"
        elif operator == "begins with":
            expression_string = f"{field_ref} LIKE '{value}%'"
        elif operator == "contains":
            expression_string = f"{field_ref} LIKE '%{value}%'"
        elif operator == "does not contain":
            expression_string = f"{field_ref} NOT LIKE '%{value}%'"
        else:
            quoted_val = QgsExpression.quotedValue(value)
            expression_string = f"{field_ref} {operator} {quoted_val}"

        expression = QgsExpression(expression_string)
        if expression.hasParserError():
            raise QgsProcessingException(
                f"Erro na expressão: {expression.parserErrorString()}"
            )

        features = layer.getFeatures(QgsFeatureRequest(expression))
        matched_features = [f for f in features]

        nFeatures = len(matched_features)
        if nFeatures == 0:
            feedback.pushInfo("Nenhum recurso encontrado com o valor especificado.")
            return {self.OUTPUT: dest_id}

        stepSize = 100 / nFeatures

        for current, feature in enumerate(matched_features):
            if feedback.isCanceled():
                break
            sink.addFeature(feature, QgsFeatureSink.FastInsert)
            feedback.setProgress(int((current / nFeatures) * 100))

        feedback.pushInfo("Exportação concluída com sucesso.")
        return {self.OUTPUT: dest_id}

    def name(self):
        return "exportfeaturesbyattribute"

    def displayName(self):
        return self.tr("Export Features by Attribute")

    def group(self):
        return self.tr("Utils")

    def groupId(self):
        return "DSGTools - Utils"

    def tr(self, string):
        return QCoreApplication.translate("ExportFeaturesByAttribute", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def createInstance(self):
        return ExportFeaturesByAttributeAlgorithm()
