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


class GeneralizeHighwaysAlgorithm(QgsProcessingAlgorithm):
    NETWORK_LAYER = "NETWORK_LAYER"
    MIN_LENGTH = "MIN_LENGTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    ESCALA = "ESCALA"
    AREA_MINIMA = "AREA_MINIMA"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NETWORK_LAYER,
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
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POINT_CONSTRAINT_LAYER_LIST,
                self.tr("Point constraint Layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_CONSTRAINT_LAYER_LIST,
                self.tr("Line constraint Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGON_CONSTRAINT_LAYER_LIST,
                self.tr("Polygon constraint Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.MIN_LENGTH,
                self.tr("Comprimento mínimo das estradas com pontas soltas"),
                minValue=0,
                defaultValue=0.001,
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
        return "generalizehighwaysalgorithm"

    def displayName(self):
        return self.tr("Generalizar Rodovias")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeHighwaysAlgorithm", string)

    def createInstance(self):
        return GeneralizeHighwaysAlgorithm()
