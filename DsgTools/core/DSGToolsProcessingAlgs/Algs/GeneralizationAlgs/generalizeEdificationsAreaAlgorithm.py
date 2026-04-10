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
from qgis.PyQt.QtCore import QCoreApplication
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
)

from ...algRunner import AlgRunner


class GeneralizeEdificationsAreaAlgorithm(QgsProcessingAlgorithm):
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
                self.tr("Polygon Input Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POINT,
                self.tr("Point Input Layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ESCALA,
                self.tr("Scale"),
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREAMINIMA,
                self.tr("Minimum Map Area (degrees squared on chart)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUTPOLYGON, self.tr("Area buildings converted to points")
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
        area_minima_mapa = self.parameterAsDouble(parameters, self.AREAMINIMA, context)
        algRunner = AlgRunner()

        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        ids = algRunner.runCreateFieldWithExpression(
            polygonLayer, "@id", "featid", context, fieldType=1
        )

        area_limite = area_minima_mapa * (escala**2)
        fields = polygonLayer.fields()
        crs = ids.sourceCrs()

        (polygonSink, polygonSinkId) = self.parameterAsSink(
            parameters, self.OUTPUTPOLYGON, context, fields, QgsWkbTypes.Polygon, crs
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Selecting features with area smaller than the established minimum...")
        )

        selected_features = algRunner.runFilterExpression(
            ids, f"area($geometry) < {area_limite}", context
        )
        pointLayer.startEditing()
        pointLayer.beginEditCommand(
            self.tr("Adding points to the original point layer")
        )
        idsToDelete = []
        for feature in selected_features.getFeatures():
            polygonSink.addFeature(feature, QgsFeatureSink.FastInsert)
            idsToDelete.append(feature["featid"])
            if multiStepFeedback.isCanceled():
                return
            geom = feature.geometry()
            centroid = geom.centroid()

            pointFeature = QgsFeature(fields)
            pointFeature.setGeometry(centroid)

            fieldsFeat = [f.name() for f in feature.fields()]
            for field in fields:
                fieldName = field.name()
                if fieldName not in fieldsFeat:
                    continue
                pointFeature[fieldName] = feature[fieldName]
            pointLayer.addFeature(pointFeature)

        pointLayer.endEditCommand()

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr(
                "Deleting polygons with area smaller than the minimum from the input layer..."
            )
        )

        polygonLayer.startEditing()
        polygonLayer.beginEditCommand(
            self.tr("Delete polygons with area smaller than the limit from the input polygon layer")
        )
        polygonLayer.deleteFeatures(idsToDelete)
        polygonLayer.endEditCommand()

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Algorithm complete..."))
        return {self.OUTPUTPOLYGON: polygonSinkId}

    def name(self):
        return "generalizeedificationsareaalgorithm"

    def displayName(self):
        return self.tr("Generalize Buildings - Area")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeEdificationsAreaAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "This algorithm receives a point layer and a polygon layer as inputs. Polygon features with an area smaller than the established minimum will be removed from the original layer and a point corresponding to the centroid of each polygon will be inserted into the point layer. Additionally, an output layer contains the polygon features that were removed from the original layer. Note: The area values to be entered as input are relative to the map area (which will be corrected by the scale), in the metric system of the input layers."
        )

    def createInstance(self):
        return GeneralizeEdificationsAreaAlgorithm()
