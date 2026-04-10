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
from qgis.PyQt.QtCore import QCoreApplication
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

from ...algRunner import AlgRunner, runProcessing


class GeneralizeLandingStripAlgorithm(QgsProcessingAlgorithm):
    INPUT_POLYGON = "INPUT_POLYGON"
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
                self.INPUT_POLYGON,
                self.tr("Polygon Input Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Scale"),
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREAMINIMA,
                self.tr("Minimum Map Area (on chart)"),
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterDistance(
                self.LARGURAMINIMA,
                self.tr("Minimum Map Width (on chart)"),
                parentParameterName=self.INPUT_POLYGON,
            )
        )

        smooth_voronoi = QgsProcessingParameterNumber(
            self.SVORONOI,
            self.tr("Voronoi smoothing value"),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.1,
        )
        smooth_voronoi.setFlags(
            smooth_voronoi.flags() | QgsProcessingParameterDefinition.Flag.FlagAdvanced
        )
        self.addParameter(smooth_voronoi)

        smooth_simplify = QgsProcessingParameterNumber(
            self.SSIMPLIFY,
            self.tr("Simplify smoothing value"),
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0001,
        )
        smooth_simplify.setFlags(
            smooth_simplify.flags() | QgsProcessingParameterDefinition.Flag.FlagAdvanced
        )
        self.addParameter(smooth_simplify)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUTLINE, self.tr("Lines"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """

        polygonLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_POLYGON, context
        )
        polygonLayer.startEditing()
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

        (LineSink, LineSinkId) = self.parameterAsSink(
            parameters, self.OUTPUTLINE, context, fields, QgsWkbTypes.LineString, crs
        )

        fields = polygonLayer.fields()
        crs = polygonLayer.sourceCrs()

        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Starting 'id' assignment to layer features...")
        )
        ids = algRunner.runCreateFieldWithExpression(
            polygonLayer, "@id", "featid", context, fieldType=1
        )
        multiStepFeedback.setProgressText(
            self.tr("Feature 'id' assignment complete...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Starting pole of inaccessibility algorithm...")
        )

        verifyingCrs = ids.crs()

        if verifyingCrs.isGeographic():
            tolerancia = 0.001
        else:
            tolerancia = 100

        inacessibility_pole = algRunner.runPoleOfInaccessibility(
            ids, context, tolerance=tolerancia
        )
        multiStepFeedback.setProgressText(
            self.tr("Pole of inaccessibility algorithm complete...")
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Starting landing strip width determination...")
        )

        polygon_com_largura = algRunner.runJoinAttributesTable(
            ids, "featid", inacessibility_pole, "featid", context, 1, ["dist_pole"]
        )
        multiStepFeedback.setProgressText(
            self.tr("Landing strip width determination complete...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Starting landing strip selection...")
        )

        features_to_become_line = algRunner.runFilterExpression(
            polygon_com_largura,
            f"area($geometry) < {area_limite} or dist_pole < {largura_limite/2}",
            context,
        )
        multiStepFeedback.setProgressText(
            self.tr("Landing strip selection complete...")
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Starting line extraction from areas...")
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

        for featid in centerlinesDict:
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return {}
            ids_to_delete.append(featid)
            newFeat = QgsFeature(fields)
            feat = centerlinesDict[featid]
            newFeat.setGeometry(feat.geometry())
            fieldsFeat = [f.name() for f in feat.fields()]
            for field in fields:
                fieldName = field.name()
                if fieldName not in fieldsFeat:
                    continue
                newFeat[fieldName] = feat[fieldName]
            LineSink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        polygonLayer.startEditing()
        polygonLayer.beginEditCommand(self.tr("Delete polygons"))
        polygonLayer.deleteFeatures(ids_to_delete)
        polygonLayer.endEditCommand()

        return {self.OUTPUTLINE: LineSinkId}

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
            self.tr("Starting line extraction from areas...")
        )
        multiStepFeedback.setProgressText(
            self.tr("Applying Voronoi skeletonization...")
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
        orientedBBox = runProcessing(
            "native:orientedminimumboundingbox",
            {"INPUT": id2, "OUTPUT": "TEMPORARY_OUTPUT"},
            context=context,
        )["OUTPUT"]
        voronoi_result = algRunner.runSkeletonVoronoi(
            features_to_become_line, smooth_voronoi, -1, context
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Adjusting attribute table fields...")
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
            self.tr("Removing end vertices and applying smoothing...")
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
        return self.tr("Generalize Landing Strips")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeLandingStripAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "This algorithm receives a polygon layer with features corresponding to landing strips. \nIf the landing strip area is smaller than the minimum or its width is smaller than the minimum, the algorithm creates a center line to represent the landing strip and removes the polygon from the original polygon layer.\n The output layer contains the lines created corresponding to the respective landing strips. \nNote 1: The area and width parameters have measurement units corresponding to the input layer units. Thus, if the layer has a metric projection, the width and area values will be received by the algorithm in meters and square meters, respectively. \nNote 2: The default simplify smoothing value corresponds to a geographic projection (units in degrees). For a metric reference system, the smoothing value must be corrected by multiplying by a value in the order of magnitude of 10^5."
        )

    def createInstance(self):
        return GeneralizeLandingStripAlgorithm()
