# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-30
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Isaac Uchoa - Cartographic Engineer @ Brazilian Army
        email                : uchoalzac@eb.br
 ***************************************************************************/
"""
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
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
    LAT_LENGTH = "LAT_LENGTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    ESCALA = "ESCALA"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NETWORK_LAYER,
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
                self.tr("Comprimento mínimo para o segmento paralelo ser eliminado"),
                minValue=0,
                defaultValue=0.005,
                parentParameterName=self.NETWORK_LAYER
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.LAT_LENGTH,
                self.tr("Distância lateral mínima para o segmento ser eliminado"),
                minValue=0,
                defaultValue=0.0005,
                parentParameterName=self.NETWORK_LAYER
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Rodovias Paralelas"),
                QgsProcessing.TypeVectorPolygon
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(8, feedback)
        multiStepFeedback.setCurrentStep(currentStep)

        algRunner = AlgRunner()

        lineLayer = self.parameterAsVectorLayer(parameters, self.NETWORK_LAYER, context)
        lineLayerList = self.parameterAsLayerList(parameters, self.LINE_CONSTRAINT_LAYER_LIST, context)
        pointLayerList = self.parameterAsLayerList(parameters, self.POINT_CONSTRAINT_LAYER_LIST, context)
        polygonLayerList = self.parameterAsLayerList(parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context)
        
        fields = lineLayer.fields()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.LineString,
            lineLayer.sourceCrs()
        )

        bufferDistance = self.parameterAsDouble(parameters, self.LAT_LENGTH, context)
        escala = self.parameterAsDouble(parameters, self.ESCALA, context)
        minLength = self.parameterAsDouble(parameters, self.MIN_LENGTH, context)
        geographicBoundsLayer = self.parameterAsLayer(parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context)

        compMinimo = minLength * escala

        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Retirando pontas soltas")) 
        algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(inputLayer=lineLayer, context=context, min_length=compMinimo, bounds_layer=geographicBoundsLayer, spatial_partition=True, pointlyr_list=pointLayerList, linelyr_list=lineLayerList, polygonlyr_list=polygonLayerList, method = 0)
        
        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("criando ids")) 
        lineLayerWithID = algRunner.runCreateFieldWithExpression(lineLayer, '$id', 'featid', context, fieldType=1)
        featLengthField = "featlength"
        multiStepFeedback.setProgressText(self.tr(f"criando novo atributo '{featLengthField}'")) 
        lineLayerWithField = algRunner.runCreateFieldWithExpression(lineLayerWithID, 'length($geometry)', featLengthField, context, fieldType=0)
        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("criando buffers")) 
        buffer = algRunner.runBuffer(lineLayerWithField, distance=bufferDistance, context=context, endCapStyle=1, joinStyle=0, segments=5, mitterLimit=2)
       
        intersection_buffer_vias = algRunner.runIntersection(lineLayerWithField, context, overlayLyr=buffer)

        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("calculando interseções")) 

        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("filtrando feições")) 
        extracted = algRunner.runFilterExpression(intersection_buffer_vias, 'featid!=featid_2', context)
        
        intersection_vias_extracted = algRunner.runIntersection(lineLayerWithField, context, overlayLyr=extracted)
 
        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("filtrando rodovias paralelas com comprimento acima do mínimo")) 
        extractedCompMin = algRunner.runFilterExpression(intersection_vias_extracted, f'length($geometry) > {compMinimo}', context)
        addedIds = {feature['featid'] for feature in extractedCompMin.getFeatures()}

        currentStep+=1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("adicionando rodovias paralelas ao sink")) 
        for featId in addedIds:
            feat = lineLayer.getFeature(featId)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Retornando"))
        
        return {self.OUTPUT: dest_id}

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

    def shortHelpString(self):
        return self.tr(
            "Este processing recebe como input a camada de vias de deslocamento (linha) e entrega como output as linhas paralelas que satisfazem aos parâmetros de comprimento e distância lateral mínimos estabelecidos no input do processing."
        )
    
    def createInstance(self):
        return GeneralizeHighwaysAlgorithm()
