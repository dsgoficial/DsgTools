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
        email                : uchoalzac@ime.eb.br
 ***************************************************************************/
"""
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDistance,
    QgsGeometry,
    QgsWkbTypes,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterDefinition,
    QgsProcessingMultiStepFeedback,
    QgsVectorLayer,
)
import processing

from ...algRunner import AlgRunner


class GeneralizeLandingStripAlgorithm(QgsProcessingAlgorithm):
    INPUT_POLYGONS = "INPUT_POLYGONS"
    INPUT_LINES = "INPUT_LINES"
    ESCALA = "ESCALA"
    AREAMINIMA = "AREAMINIMA"
    LARGURAMINIMA = "LARGURAMINIMA"
    SVORONOI = "SVORONOI"
    SSIMPLIFY = "SSIMPLIFY"
    OUTPUTLINE = "OUTPUTLINE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POLYGONS,
                self.tr("Camada de Entrada de Polígonos"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LINES,
                self.tr("Camada de Entrada de Linhas"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Escala"),
            )
        )

        param = QgsProcessingParameterNumber(
            self.AREAMINIMA,
            self.tr("Área Mínima no Mapa (na carta)"),
            type=QgsProcessingParameterNumber.Double,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)

        param = QgsProcessingParameterDistance(
            self.LARGURAMINIMA,
            self.tr("Largura mínima no Mapa (na carta)"),
            parentParameterName=self.INPUT_POLYGONS,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(param)

        smooth_voronoi = QgsProcessingParameterNumber(
            self.SVORONOI,
            self.tr("Valor da suavização voronoi"),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.1,
        )
        smooth_voronoi.setFlags(
            smooth_voronoi.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        self.addParameter(smooth_voronoi)

        smooth_simplify = QgsProcessingParameterNumber(
            self.SSIMPLIFY,
            self.tr("valor da suavização do 'simplify'"),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0001,
        )
        smooth_simplify.setFlags(
            smooth_simplify.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        self.addParameter(smooth_simplify)

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUTLINE, self.tr("Pista de Pouso areas que passaram para linha")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """

        polygonLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_POLYGONS, context
        )
        lineLayer = self.parameterAsVectorLayer(parameters, self.INPUT_LINES, context)
        algRunner = AlgRunner()

        escala = self.parameterAsInt(parameters, self.ESCALA, context)
        area_minima_mapa = self.parameterAsDouble(parameters, self.AREAMINIMA, context)
        largura_minima_mapa = self.parameterAsDouble(
            parameters, self.LARGURAMINIMA, context
        )

        area_limite = area_minima_mapa * (escala**2)
        largura_limite = largura_minima_mapa * (escala)

        smooth_voronoi = self.parameterAsDouble(parameters, self.SVORONOI, context)
        smooth_simplify = self.parameterAsDouble(parameters, self.SSIMPLIFY, context)

        crs = polygonLayer.crs()
        fields = polygonLayer.fields()

        (polygonSink, polygonSinkId) = self.parameterAsSink(
            parameters, self.OUTPUTLINE, context, fields, polygonLayer.wkbType(), crs
        )

        fields = polygonLayer.fields()
        crs = polygonLayer.sourceCrs()

        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando atribuição 'id' às feições da camada...")
        )
        polygonLayerWithIdFIeld = algRunner.runCreateFieldWithExpression(
            polygonLayer, "$id", "featid", context, fieldType=1
        )
        multiStepFeedback.setProgressText(
            self.tr("Atribuição de 'id' às feições da camada completa...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando algoritmo de polo de inacessibilidade...")
        )

        verifyingCrs = polygonLayerWithIdFIeld.crs()

        if verifyingCrs.isGeographic():
            tolerancia = 0.000001
        else:
            tolerancia = 1

        inacessibility_pole = algRunner.runPoleOfInaccessibility(
            polygonLayerWithIdFIeld, context, tolerance=tolerancia
        )
        multiStepFeedback.setProgressText(
            self.tr("algoritmo de polo de inacessibilidade completo...")
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando determinação da largura das pistas de pouso...")
        )

        polygon_com_largura = algRunner.runJoinAttributesTable(
            polygonLayerWithIdFIeld,
            "featid",
            inacessibility_pole,
            "featid",
            context,
            1,
            ["dist_pole"],
        )
        multiStepFeedback.setProgressText(
            self.tr("Determinação da largura das pistas de pouso completa...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando Seleção das pistas de pouso...")
        )

        features_to_become_line = algRunner.runFilterExpression(
            polygon_com_largura,
            f"area($geometry) < {area_limite} or dist_pole < {largura_limite/2}",
            context,
        )
        multiStepFeedback.setProgressText(
            self.tr("Seleção das pistas de pouso completo...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando obtenção das linhas a partir das áreas...")
        )

        centerlinesDict = self.getLinesFromArea(
            features_to_become_line,
            smooth_voronoi,
            smooth_simplify,
            context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        ids_to_delete = []
        lineFields = lineLayer.fields()
        lineLayer.startEditing()
        lineLayer.beginEditCommand(f"Adicionando { len(centerlinesDict) } linha(s)")

        for featid in centerlinesDict:
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return {}
            ids_to_delete.append(featid)
            newFeat = QgsFeature(lineFields)
            feat = centerlinesDict[featid]
            newFeat.setGeometry(feat.geometry())
            fieldsFeat = [f.name() for f in feat.fields()]
            for field in lineFields:
                fieldName = field.name()
                if fieldName not in fieldsFeat:
                    continue
                newFeat[fieldName] = feat[fieldName]
            lineLayer.addFeature(newFeat)

        lineLayer.endEditCommand()
        for featid in ids_to_delete:
            for feat in polygonLayerWithIdFIeld.getFeatures():
                if feat["featid"] != featid:
                    continue
                polygonSink.addFeature(feat, QgsFeatureSink.FastInsert)
        polygonLayer.startEditing()
        polygonLayer.beginEditCommand("Deletar os polígonos")
        polygonLayer.deleteFeatures(ids_to_delete)
        polygonLayer.endEditCommand()

        return {self.OUTPUTLINE: polygonSinkId}

    def getLinesFromArea(
        self,
        features_to_become_line: QgsVectorLayer,
        smooth_voronoi,
        smooth_simplify,
        context,
        feedback,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Iniciando obtenção das linhas a partir das áreas...")
        )
        multiStepFeedback.setProgressText(
            self.tr("Aplicando a esqueletização de voronoi...")
        )

        algRunner = AlgRunner()
        maiores_distancias = {}
        centerlinesDict = {}
        maiores_feicoes_id = {}
        if features_to_become_line.featureCount() == 0:
            return centerlinesDict
        idFieldForfeatures_to_become_line = "featid2"
        id2 = algRunner.runCreateFieldWithExpression(
            features_to_become_line,
            "$id",
            idFieldForfeatures_to_become_line,
            context,
            fieldType=1,
        )
        orientedBBox = processing.run(
            "native:orientedminimumboundingbox",
            {"INPUT": id2, "OUTPUT": "TEMPORARY_OUTPUT"},
        )["OUTPUT"]
        voronoi_result = algRunner.runSkeletonVoronoi(
            features_to_become_line, smooth_voronoi, -1, context
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Ajustando campos da tabela de atributos...")
        )
        # voronoi trunca nome dos atributos ate 10 caracteres, usamos join para recuperar os nomes originais
        line_with_fields = algRunner.runJoinAttributesTable(
            voronoi_result,
            "featid",
            features_to_become_line,
            "featid",
            context,
            0,
            [],
            discardNonMatching=True,
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Retirando vértices dos extremos e aplicando a suavização...")
        )
        line_with_height = algRunner.runJoinAttributesTable(
            line_with_fields, "featid", orientedBBox, "featid", context, 1, ["height"]
        )

        for feature in line_with_height.getFeatures():
            feature_id = feature["featid"]
            geom = feature.geometry()
            length = geom.length()

            if (
                feature_id not in maiores_distancias
                or length > maiores_distancias[feature_id]
            ):
                maiores_distancias[feature_id] = length
                centerlinesDict[feature_id] = feature
                maiores_feicoes_id[feature["id"]] = [feature, length]

            if multiStepFeedback.isCanceled():
                return

        for featId in centerlinesDict:
            feature = centerlinesDict[featId]
            geom = feature.geometry()
            vertices = geom.vertices()

            vertex_list = [v for v in vertices]
            new_geom = geom
            if len(vertex_list) > 3:
                vertex_list = vertex_list[3:-3]
            new_geom = QgsGeometry.fromPolyline(vertex_list)
            geom_simplified = new_geom.simplify(smooth_simplify)
            distance_to_extend = feature["height"] - geom_simplified.length()
            line_extended = geom_simplified.extendLine(
                distance_to_extend, distance_to_extend
            )
            featOriginal = features_to_become_line.getFeature(
                feature[idFieldForfeatures_to_become_line]
            )
            geomOriginal = featOriginal.geometry()
            intersection_result = line_extended.intersection(geomOriginal)
            new_geom = intersection_result
            feature.setGeometry(new_geom)

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        return centerlinesDict

    def name(self):
        return "generalizelandingstripalgorithm"

    def displayName(self):
        return self.tr("Generalizar Pistas de pouso")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeLandingStripAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "Este algoritmo recebe uma camada do tipo polígono com feições que correspondem a pistas de pouso. \nSe a área da pista de pouso for menor que a mínima ou sua largura for menor que a mínima, o algoritmo cria uma linha centra para representar a pista de pouso e elimina o polígono da camada de polígonos original.\n A camada de output são as linhas criadas correspondentes às respectivas pistas de pouso. \nObs.1: Os parâmetros de área e largura têm unidade de medida correspondente às unidades da camada de entrada. Assim, se a camada tem uma projeção métrica, os valores de largura e área serão recebidos pelo algoritmo em metros e metros quadrados, respectivamente. \nObs.2: O valor default da suavização do 'simplify' corresponde a uma projeção geográfica (unidades em graus). Para um sistema de referência métrico, valor de suavização deve ser corrigido, sendo multiplicado por um valor na ordem de grandeza de 10^5."
        )

    def createInstance(self):
        return GeneralizeLandingStripAlgorithm()
