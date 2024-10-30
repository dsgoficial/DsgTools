# -*- coding: utf-8 -*-
"""
/***************************************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-01
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jaime Guilherme - Cartographic Engineer @ Brazilian Army
        email                : jaime.breda@ime.eb.br
 ***************************************************************************************************/

 /***************************************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************************************/
"""

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterNumber,
    QgsSpatialIndex,
    QgsProcessingParameterDistance,
    QgsProcessingParameterString,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class GeneralizeContourLineAlgorithm(QgsProcessingAlgorithm):
    
    CONTOUR_LINE = "CONTOUR_LINE"
    SCALE = "SCALE"
    QUOTA_FIELD = "QUOTA_FIELD"
    INDEX_FIELD = "INDEX_FIELD"
    INDEX_FIELD_VALUE = "INDEX_FIELD_VALUE"
    SMALL_CLOSED_LINES_VALUE = "SMALL_CLOSED_LINES_VALUE"
    WATER_BODY = "WATER_BODY"
    WATER_BODY_INSIDE_FIELD = "WATER_BODY_INSIDE_FIELD"
    WATER_BODY_INSIDE_FIELD_VALUE = "WATER_BODY_INSIDE_FIELD_VALUE"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.CONTOUR_LINE,
                self.tr("Contour line layer"),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE,
                self.tr("Scale"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.QUOTA_FIELD,
                self.tr('Select Quota field'),
                parentLayerParameterName=self.CONTOUR_LINE,
                type=QgsProcessingParameterField.Any
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.INDEX_FIELD,
                self.tr('Select Index field'),
                parentLayerParameterName=self.CONTOUR_LINE,
                type=QgsProcessingParameterField.Any
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.INDEX_FIELD_VALUE,
                self.tr('Index normal quota value')
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.SMALL_CLOSED_LINES_VALUE, self.tr('Closed lines tolerance'),
                parentParameterName=self.CONTOUR_LINE,
                minValue=0,
                defaultValue=0.0001
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY,
                self.tr("Water body layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.WATER_BODY_INSIDE_FIELD,
                self.tr('Inside Water Body field from Contour Line'),
                parentLayerParameterName=self.CONTOUR_LINE,
                type=QgsProcessingParameterField.Any,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.WATER_BODY_INSIDE_FIELD_VALUE,
                self.tr('Value related to Not inside water body'),
                optional=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        contour_line_layer = self.parameterAsVectorLayer(parameters, self.CONTOUR_LINE, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        quota_field = self.parameterAsString(parameters, self.QUOTA_FIELD, context)
        index_field = self.parameterAsString(parameters, self.INDEX_FIELD, context)
        index_field_value = self.parameterAsString(parameters, self.INDEX_FIELD_VALUE, context)
        small_closed_lines_value = self.parameterAsDouble(parameters, self.SMALL_CLOSED_LINES_VALUE, context)
        water_body_layer = self.parameterAsVectorLayer(parameters, self.WATER_BODY, context)
        water_body_inside_field = self.parameterAsString(parameters, self.WATER_BODY_INSIDE_FIELD, context)
        water_body_inside_field_value = self.parameterAsString(parameters, self.WATER_BODY_INSIDE_FIELD_VALUE, context)

        equidist = scale/2.5
        small_closed_lines_tol = small_closed_lines_value * scale
        optional_step = water_body_layer is not None and water_body_inside_field is not None and water_body_inside_field_value is not None

        algRunner = AlgRunner()

        steps = 5
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        if contour_line_layer is None:
            feedback.reportError('Layer not defined correctly.')
            return {}
        if water_body_inside_field is not None and water_body_inside_field!='':
            field_index = contour_line_layer.fields().indexFromName(water_body_inside_field)
            if field_index == -1:
                multiStepFeedback.pushInfo(
                    self.tr(f"The field {water_body_inside_field} does not exist in layer {contour_line_layer.name()}!")
                )
                return {}

        multiStepFeedback.setProgressText(self.tr("Removing small closed lines."))
        algRunner.runFindSmallClosedLinesAlgorithm(
            inputLayer=contour_line_layer,
            min_length=small_closed_lines_tol,
            method=0,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        cacheCountourLyr = algRunner.runCreateFieldWithExpression(
            contour_line_layer,
            '$id',
            'featid',
            fieldType=1,
            context=context,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering by quota."))
        filteredContourLines = algRunner.runFilterExpression(
            inputLyr=cacheCountourLyr,
            expression=f"""{quota_field} % {equidist} = 0""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        idsToRemove = [feat["featid"] for feat in filteredContourLines.getFeatures()]

        contour_line_layer.startEditing()
        contour_line_layer.beginEditCommand(self.tr('Updating contour lines.'))
        contour_line_layer.deleteFeatures(idsToRemove)
        for feature in contour_line_layer.getFeatures():
            if feature[quota_field] % (equidist * 5) != 0:
                feature[index_field] = index_field_value
            contour_line_layer.updateFeature(feature)
        contour_line_layer.endEditCommand()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        if optional_step:
            contour_line_layer.startEditing()
            contour_line_layer.beginEditCommand(self.tr("Update Outside Water Body Field"))
            spatial_index = QgsSpatialIndex(water_body_layer.getFeatures())
            for contour_feature in contour_line_layer.getFeatures():
                intersects_water_body = any(
                    contour_feature.geometry().intersects(water_body.geometry())
                    for water_body in water_body_layer.getFeatures(spatial_index.intersects(contour_feature.geometry().boundingBox()))
                )
                if not intersects_water_body:
                    contour_feature[water_body_inside_field] = water_body_inside_field_value
                    contour_line_layer.updateFeature(contour_feature)
            contour_line_layer.endEditCommand()

        return {}

    def name(self):
        return "generalizecontourlinealgorithm"

    def displayName(self):
        return self.tr("Generalize Contour Line Algorithm")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"
    
    def shortHelpString(self):
        return self.tr(
            "Generaliza curvas de nível.\nScale: Escolha a escala desejada. Exemplo: '50' para 50k.\nSelect Quota field: Escolha a coluna da layer Countour Line relacionada com a Cota.\nSelect Index field: Escolha a coluna da layer Countour Line relacionada ao atributo de curva mestra.\nIndex normal quota value: Insira o valor relacionado às cotas normais para alterar o atributo de curva mestra.\nClosed lines tolerance: Escolha o valor mínimo de tolerância para suprimir curvas fechadas pequenas. Exemplo: '0,0001' para 10mm.\nInside Water Body field from Contour Line: Escolha a coluna referente a dentro de massa d'água na camada de curva de nível.\nValue related to Not inside water body: Insira o valor relacionado ao campo anterior referente ao que NÃO está dentro de massa d'água."
        )


    def tr(self, string):
        return QCoreApplication.translate("GeneralizeContourLineAlgorithm", string)

    def createInstance(self):
        return GeneralizeContourLineAlgorithm()
