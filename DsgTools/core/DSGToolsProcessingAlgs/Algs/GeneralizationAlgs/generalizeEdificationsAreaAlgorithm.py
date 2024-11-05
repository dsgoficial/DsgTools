# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-22
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
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsGeometry,
)

from ...algRunner import AlgRunner


class GeneralizeEdificationsAreaAlgorithm(QgsProcessingAlgorithm):
    INPUT_POLYGON = "INPUT_POLYGON"
    INPUT_POINT = "INPUT_POINT"
    ESCALA = "ESCALA"
    AREA_MINIMA = "AREA_MINIMA"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    OUTPUT_POINT = "OUTPUT_POINT"
    OUTPUT_POLYGON = "OUTPUT_POLYGON"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POLYGON,
                self.tr("Camada de Entrada de Polígonos"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POINT,
                self.tr("Camada de Entrada de Pontos"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Escala"),
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        param = QgsProcessingParameterNumber(
            self.AREA_MINIMA,
            self.tr("Área Mínima no Mapa (graus² na carta)"),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=1,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POLYGON,
                self.tr("Edificações áreas transformadas em pontos"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """

        polygonLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_POLYGON, context
        )
        pointLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POINT, context)
        escala = self.parameterAsInt(parameters, self.ESCALA, context)
        area_minima_mapa = self.parameterAsDouble(parameters, self.AREA_MINIMA, context)
        algRunner = AlgRunner()

        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        polygonLayerWithFeatId = algRunner.runCreateFieldWithExpression(
            polygonLayer, "$id", "featid", context, fieldType=1
        )

        area_limite = area_minima_mapa * (escala**2)
        fields = polygonLayer.fields()
        crs = polygonLayerWithFeatId.sourceCrs()

        (polygonSink, polygonSinkId) = self.parameterAsSink(
            parameters, self.OUTPUT_POLYGON, context, fields, QgsWkbTypes.Polygon, crs
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Selecionando feições com area menor que o mínimo estabelecido...")
        )

        selected_features = algRunner.runFilterExpression(
            polygonLayerWithFeatId, f"area($geometry) < {area_limite}", context
        )
        multiStepFeedback.pushInfo(
            f"{selected_features.featureCount()} feição(ões) selecionados"
        )
        centroids = algRunner.runCentroids(selected_features, context)
        pointLayer.startEditing()
        pointLayer.beginEditCommand("Adicionando os pontos na camada de pontos")
        idsToDelete = []
        pointFields = pointLayer.fields()
        for feature in centroids.getFeatures():
            if multiStepFeedback.isCanceled():
                return
            geom = feature.geometry()
            pointFeature = QgsFeature(pointFields)
            pointFeature.setGeometry(geom)

            fieldsFeat = [f.name() for f in feature.fields()]
            for field in fields:
                fieldName = field.name()
                if fieldName not in fieldsFeat:
                    continue
                pointFeature[fieldName] = feature[fieldName]
            pointLayer.addFeature(pointFeature)

        pointLayer.endEditCommand()
        for feature in selected_features.getFeatures():
            idsToDelete.append(feature["featid"])
            polygonSink.addFeature(feature, QgsFeatureSink.FastInsert)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr(
                f"Deletando da camada de input os polígonos com área menor que o mínimo... {len(idsToDelete)} feição(ões)"
            )
        )
        if len(idsToDelete) > 0:
            polygonLayer.startEditing()
            polygonLayer.beginEditCommand(
                "Deletar da camada de polígonos de input os polígonos com área menor que a área limite"
            )
            polygonLayer.deleteFeatures(idsToDelete)
            polygonLayer.endEditCommand()

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Algoritmo completo..."))
        return {self.OUTPUT_POLYGON: polygonSinkId}

    def name(self):
        return "generalizeedificationsareaalgorithm"

    def displayName(self):
        return self.tr("Generalizar Edificações - Area")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeEdificationsAreaAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "Este algoritmo recebe uma camada do tipo ponto e uma do tipo polígono como inputs. As feições do tipo polígono que tiverem uma área menor que o mínimo estabecido serão excluídas da camada original e um ponto correspondente ao centroide de cada um desses polígonos será inserido na camada de pontos. Além disso, uma camada de output contém as feições do tipo polígono que foram excluídas da camada original. Obs.: Os valores de área a ser inseridos no input são relativos à área no mapa(que será corrigida pela escala), no sistema métrico das camadas inseridas."
        )

    def createInstance(self):
        return GeneralizeEdificationsAreaAlgorithm()
