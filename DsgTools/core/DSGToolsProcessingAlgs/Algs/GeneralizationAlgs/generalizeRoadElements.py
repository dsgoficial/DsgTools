# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-31
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
    QgsWkbTypes,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingMultiStepFeedback,
)

from ...algRunner import AlgRunner
class GeneralizeRoadElementsAlgorithm(QgsProcessingAlgorithm):
    INPUT_VIARIO = "INPUT_VIARIO"
    INPUT_DRENAGEM = "INPUT_DRENAGEM"
    INPUT_DESLOCAMENTO = "INPUT_DESLOCAMENTO"
    INPUT_MASSA_DAGUA = "INPUT_MASSA_DAGUA"
    INPUT_FERROVIA = "INPUT_FERROVIA"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_VIARIO,
                self.tr("Camada de elementos viários"),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_DRENAGEM,
                self.tr("Camada de trecho de drenagem"),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_DESLOCAMENTO,
                self.tr("Camada de vias de Deslocamento"),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_MASSA_DAGUA,
                self.tr("Camada de Massa d'água"),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_FERROVIA,
                self.tr("Input Camada Ferrovias"),
                [QgsProcessing.TypeVectorLine]
            )
        ) 
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Elementos deletados"),
                QgsProcessing.TypeVectorLine
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        multiStepFeedback.setCurrentStep(currentStep)

        algRunner = AlgRunner()

        deslocamentoLayer = self.parameterAsVectorLayer(parameters, self.INPUT_DESLOCAMENTO, context)
        viarioLayer = self.parameterAsVectorLayer(parameters, self.INPUT_VIARIO, context)
        drenagemLayer = self.parameterAsVectorLayer(parameters, self.INPUT_DRENAGEM, context)
        massadaguaLayer = self.parameterAsVectorLayer(parameters, self.INPUT_MASSA_DAGUA, context)
        ferroviaLayer = self.parameterAsVectorLayer(parameters, self.INPUT_FERROVIA, context)
                
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("IDs na camada de elementos viários..."))
        viarioLayerWithIds = algRunner.runCreateFieldWithExpression(viarioLayer, '$id', 'featid', context, fieldType = 1)
        
        fields = viarioLayerWithIds.fields()
        (sink_viario, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.LineString,
            viarioLayer.sourceCrs()
        )

        idsViario = set()
        
        for feature in viarioLayerWithIds.getFeatures():
            idsViario.add(feature['featid'])
        
        intersectaHidro = set()
        intersectaVias = set()

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("interseção com trechos de drenagem"))
        intersectionDrenagem = algRunner.runExtractByLocation(viarioLayerWithIds, drenagemLayer, context)
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("interseção massa dagua"))
        intersectionMassaDagua = algRunner.runExtractByLocation(viarioLayerWithIds, massadaguaLayer, context)
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("interseção com ferrovias"))
        intersectionFerrovia = algRunner.runExtractByLocation(viarioLayerWithIds, ferroviaLayer, context)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("interseção com vias de deslocamento"))
        intersectionViaDeslocamento = algRunner.runExtractByLocation(viarioLayerWithIds, deslocamentoLayer, context)
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Inserindo os IDs no conjuntos"))
        for feature in intersectionMassaDagua.getFeatures():
            intersectaHidro.add(feature['featid'])
        for feature in intersectionDrenagem.getFeatures():
            intersectaHidro.add(feature['featid'])
        for feature in intersectionViaDeslocamento.getFeatures():
            intersectaVias.add(feature['featid'])
        for feature in intersectionFerrovia.getFeatures():
            intersectaVias.add(feature['featid'])

        idsToDelete1 = idsViario - intersectaHidro 
        idsToDelete2 = idsViario - intersectaVias

        for id in list(set(list(idsToDelete1) + list(idsToDelete2))):  
            new_feature = QgsFeature(viarioLayer.getFeature(id))
            sink_viario.addFeature(new_feature, QgsFeatureSink.FastInsert)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Deletando os IDs selecionados"))
        viarioLayer.startEditing()
        viarioLayer.beginEditCommand("Deletando ids selecionados")
        viarioLayer.deleteFeatures(list(idsToDelete1))        
        viarioLayer.deleteFeatures(list(idsToDelete2))
        viarioLayer.endEditCommand()
     
        return {self.OUTPUT: dest_id}

    def name(self):
        return "generalizeroadelelementsalgorithm"

    def displayName(self):
        return self.tr("Generalizar Elementos viários")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeRoadElementsAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            "Este processing verifica se o elemento viário possui interseção com uma via de deslocamento e com um trecho de drenagem. Se uma das duas condições não for atendida, o elemento viário será deletado da camada de input. Além disso, o algoritmo apresenta um output que apresenta os elementos viários deletados."
        )
    
    def createInstance(self):
        return GeneralizeRoadElementsAlgorithm()
