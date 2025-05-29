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
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDistance,
    QgsWkbTypes,
    QgsProcessingParameterMultipleLayers,
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
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA, self.tr("Escala"), type=QgsProcessingParameterNumber.Double
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.AREA_MINIMA,
                self.tr("Área mínima para rotatórias na carta"),
                parentParameterName=self.NETWORK_LAYER,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(currentStep)

        algRunner = AlgRunner()

        lineLayer = self.parameterAsVectorLayer(parameters, self.NETWORK_LAYER, context)
        lineLayerList = self.parameterAsLayerList(
            parameters, self.LINE_CONSTRAINT_LAYER_LIST, context
        )
        pointLayerList = self.parameterAsLayerList(
            parameters, self.POINT_CONSTRAINT_LAYER_LIST, context
        )
        polygonLayerList = self.parameterAsLayerList(
            parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context
        )

        escala = self.parameterAsDouble(parameters, self.ESCALA, context)
        minLength = self.parameterAsDouble(parameters, self.MIN_LENGTH, context)
        minArea = self.parameterAsDouble(parameters, self.AREA_MINIMA, context)
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        multiStepFeedback.setProgressText(self.tr("Calculando tamanhos"))
        areaminima = minArea * (escala**2)
        compMinimo = minLength * escala

        multiStepFeedback.setProgressText(self.tr("Generalizando"))
        algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(
            inputLayer=lineLayer,
            context=context,
            min_length=compMinimo,
            bounds_layer=geographicBoundsLayer,
            spatial_partition=True,
            pointlyr_list=pointLayerList,
            linelyr_list=lineLayerList,
            polygonlyr_list=polygonLayerList,
            method=0,
        )

        lineLayerWithID = algRunner.runCreateFieldWithExpression(
            lineLayer, "$id", "featid", context
        )

        polygonized = algRunner.runPolygonize(lineLayerWithID, context, keepFields=True)

        areasPequenas = algRunner.runFilterExpression(
            polygonized, f"area($geometry) < {areaminima}", context
        )
        idsAreasPequenas = []

        for feature in areasPequenas.getFeatures():
            idsAreasPequenas.append(feature["featid"])

        print(idsAreasPequenas)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Retornando"))

        return {}

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

    def createInstance(self):
        return GeneralizeRoundaboutsAlgorithm()
