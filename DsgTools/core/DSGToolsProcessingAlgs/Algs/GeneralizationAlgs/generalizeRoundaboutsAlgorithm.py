# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Isaac Uchoa - Cartographic Engineer @ Brazilian Army
        email                : uchoalzac@eb.br
 ***************************************************************************/
"""
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeature,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDistance,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingMultiStepFeedback,
)

from ...algRunner import AlgRunner
class GeneralizeRoundaboutsAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = "INPUT_LAYER"
    ESCALA = "ESCALA"
    AREA_MINIMA = "AREA_MINIMA"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr("Camada de rodovias"),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Escala"),
                type=QgsProcessingParameterNumber.Double
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.AREA_MINIMA,
                self.tr("Área mínima para rotatórias na carta"),
                parentParameterName=self.INPUT_LAYER
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Rotatórias"),
                QgsProcessing.TypeVectorPolygon
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(currentStep)

        algRunner = AlgRunner()

        lineLayer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
       
        escala = self.parameterAsDouble(parameters, self.ESCALA, context)
        minArea = self.parameterAsDouble(parameters, self.AREA_MINIMA, context)
        fields = lineLayer.fields()
        
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            lineLayer.sourceCrs()
        )
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Calculando tamanhos"))    
        areaminima = minArea * (escala**2)
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Generalizando"))

        lineLayerWithID = algRunner.runCreateFieldWithExpression(lineLayer, '$id', 'featid', context)
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Aplicando o polygonized"))  
        polygonized = algRunner.runPolygonize(lineLayerWithID, context, keepFields=True)

        areasPequenas = algRunner.runFilterExpression(polygonized, f'area($geometry) < {areaminima}', context)
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Adicionando os polígonos de área pequena ao sink"))
        for feature in areasPequenas.getFeatures():
            feat = QgsFeature(feature)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Retornando"))
        
        return {self.OUTPUT: dest_id}

    def name(self):
        return "generalizeroundaboutsalgorithm"

    def displayName(self):
        return self.tr("Generalizar Rotatórias")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeRoundaboutsAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "Este processing recebe uma camada de linhas e retorna como output, os polígonos de área pequena limitados pelas linhas."
        )
    
    def createInstance(self):
        return GeneralizeRoundaboutsAlgorithm()
