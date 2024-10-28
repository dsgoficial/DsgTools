# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : diniz.felipe@eb.mil.br
 ***************************************************************************/
"""
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingParameterExpression, 
    QgsProcessingMultiStepFeedback,
)

from ...algRunner import AlgRunner
class GeneralizeEdificationsAlgorithm(QgsProcessingAlgorithm):
    INPUT_POLYGON = "INPUT_POLYGON"
    INPUT_POINT = "INPUT_POINT"
    ESCALA = "ESCALA"
    AREAMINIMA = "AREAMINIMA"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    OUTPUTPOINT = "OUTPUTPOINT"
    OUTPUTPOLYGON = "OUTPUTPOLYGON"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POLYGON,
                self.tr("Camada de Entrada de Polígonos"),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POINT,
                self.tr("Camada de Entrada de Pontos"),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Escala"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=50000
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREAMINIMA,
                self.tr("Área Mínima no Mapa (mm²)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.FILTER_EXPRESSION,
                self.tr("Filter expression for input"),
                None,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUTPOINT, self.tr("Output Point Layer")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUTPOLYGON, self.tr("Output Polygon Layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(currentStep)

        polygonLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POLYGON, context)
        pointLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POINT, context)
        algRunner = AlgRunner()
        localCache = algRunner.runCreateFieldWithExpression(
            inputLyr=pointLayer,
            expression="@id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=None,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        escala = self.parameterAsInt(parameters, self.ESCALA, context)
        area_minima_mapa = self.parameterAsDouble(parameters, self.AREAMINIMA, context)

        area_limite = ((area_minima_mapa / 1000) ** 2) * (escala ** 2)

        fields = polygonLayer.fields()
        crs = polygonLayer.sourceCrs()

        (pointSink, pointSinkId) = self.parameterAsSink(
            parameters, self.OUTPUTPOINT, context, fields, QgsWkbTypes.Point, crs
        )

        (polygonSink, polygonSinkId) = self.parameterAsSink(
            parameters, self.OUTPUTPOLYGON, context, fields, QgsWkbTypes.Polygon, crs
        )
        
        filterExpression = self.parameterAsExpression(parameters, self.FILTER_EXPRESSION, context)
        pointLayer.startEditing()

        expression = f"$area < {area_limite}"
        polygonLayer.selectByExpression(expression)

        selected_features = polygonLayer.selectedFeatures()

        for feature in selected_features:
            if multiStepFeedback.isCanceled():
                return
            geom = feature.geometry()
            centroid = geom.centroid().asPoint()
            
            pointFeature = QgsFeature(fields)
            pointFeature.setGeometry(QgsGeometry.fromPointXY(centroid))
            pointFeature.setAttributes(feature.attributes())
            pointSink.addFeature(pointFeature, QgsFeatureSink.FastInsert)

            pointLayer.addFeature(pointFeature)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        polygonLayer.deleteSelectedFeatures()

        remaining_features = polygonLayer.getFeatures()
        for feature in remaining_features:
            if multiStepFeedback.isCanceled():
                return
            polygonSink.addFeature(feature, QgsFeatureSink.FastInsert)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        return {self.OUTPUTPOINT: pointSinkId, self.OUTPUTPOLYGON: polygonSinkId}

    def name(self):
        return "generalizeedificationsalgorithm"

    def displayName(self):
        return self.tr("Generalizar Edificações")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeEdificationsAlgorithm", string)

    def createInstance(self):
        return GeneralizeEdificationsAlgorithm()
