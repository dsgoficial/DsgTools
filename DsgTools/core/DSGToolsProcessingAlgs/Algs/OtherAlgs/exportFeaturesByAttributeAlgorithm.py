# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-11-06
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jean Michael Estevez Alvarez-  Brazilian Army
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
from qgis.core import (QgsProcessing,
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
                       QgsFeatureRequest)
from qgis import processing


class ExportFeaturesByAttributeAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OPERATOR = 'OPERATOR'
    VALUE = 'VALUE'
    OUTPUT = 'OUTPUT'

    OPERATORS = ['=',
                 '<>',
                 '>',
                 '>=',
                 '<',
                 '<=',
                 'begins with',
                 'contains',
                 'is null',
                 'is not null',
                 'does not contain'
                 ]
    STRING_OPERATORS = ['begins with', 'contains', 'does not contain']

    def createInstance(self):
        return ExportFeaturesByAttributeAlgorithm()

    def name(self):
        return 'exportfeaturesbyattribute'

    def displayName(self):
        return self.tr('Export Features by Attribute')


    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Utils")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Utils"
    
    def tr(self, string):
        return QCoreApplication.translate("Exports all features with a specified attribute value to a new layer", string
    )


    def shortHelpString(self):
        return self.tr("Exports all features with a specified attribute value to a new layer with the name of the input layer suffixed with '_Output'.")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                self.tr('Selection attribute'),
                parentLayerParameterName=self.INPUT
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATOR,
                self.tr('Operator'),
                options=self.OPERATORS,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.VALUE,
                self.tr('Value'),
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        fieldName = self.parameterAsString(parameters, self.FIELD, context)
        operator = self.OPERATORS[self.parameterAsEnum(parameters, self.OPERATOR, context)]
        value = self.parameterAsString(parameters, self.VALUE, context)

        if layer is None:
            feedback.pushInfo("Camada inválida ou não encontrada.")
            return {self.OUTPUT: None}

        if fieldName not in layer.fields().names():
            feedback.pushInfo(f"O atributo '{fieldName}' não foi encontrado na camada. Nenhuma exportação realizada.")
            return {self.OUTPUT: None}

        # Construindo a expressão de seleção
        field_ref = QgsExpression.quotedColumnRef(fieldName)
        if operator == 'is null':
            expression_string = f"{field_ref} IS NULL"
        elif operator == 'is not null':
            expression_string = f"{field_ref} IS NOT NULL"
        elif operator == 'begins with':
            expression_string = f"{field_ref} LIKE '{value}%'"
        elif operator == 'contains':
            expression_string = f"{field_ref} LIKE '%{value}%'"
        elif operator == 'does not contain':
            expression_string = f"{field_ref} NOT LIKE '%{value}%'"
        else:
            quoted_val = QgsExpression.quotedValue(value)
            expression_string = f"{field_ref} {operator} {quoted_val}"

        expression = QgsExpression(expression_string)
        if expression.hasParserError():
            feedback.pushInfo(f"Erro na expressão: {expression.parserErrorString()}")
            return {self.OUTPUT: None}

        # Configurando o sink para a camada de saída
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            layer.fields(),
            layer.wkbType(),
            layer.sourceCrs()
        )

        # Verificando se há features que correspondem ao filtro
        features = layer.getFeatures(QgsFeatureRequest(expression))
        matched_features = [f for f in features]
        if not matched_features:
            feedback.pushInfo("Nenhum recurso encontrado com o valor especificado.")
            return {self.OUTPUT: dest_id}

        # Adiciona as features que correspondem ao filtro no sink
        for feature in matched_features:
            if feedback.isCanceled():
                break
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

        feedback.pushInfo("Exportação concluída com sucesso.")
        return {self.OUTPUT: dest_id}
