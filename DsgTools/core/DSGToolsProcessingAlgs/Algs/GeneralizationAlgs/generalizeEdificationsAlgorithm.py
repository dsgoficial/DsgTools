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
import concurrent.futures
import os
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsVectorLayer,
    QgsProcessingParameterDistance,
    QgsProcessingParameterExpression, 
    QgsWkbTypes, 
    QgsFeatureRequest, 
    QgsFeatureSink, 
    QgsProcessingParameterFeatureSink,
    QgsGeometry, 
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsProcessingFeedback
)
from qgis.PyQt.QtCore import QVariant
import processing

from ...algRunner import AlgRunner
class GeneralizeEdificationsAlgorithm(QgsProcessingAlgorithm):
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    INPUT_POINT = "INPUT_POINT"
    TOL = "TOL"
    OUTPUT = "OUTPUT"
    
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POINT,
                self.tr("Camada de Entrada de Pontos"),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                name = self.FILTER_EXPRESSION,
                description = self.tr("Expressão de filtro correspondente às edificações de baixa prioridade"),
                defaultValue = None,
                parentLayerParameterName = self.INPUT_POINT,
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterDistance(
                self.TOL,
                self.tr("Tolerancia"),
                parentParameterName=self.INPUT_POINT
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Edificações não eliminadas (alta prioridade próximas)"),
                QgsProcessing.TypeVectorPoint
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Implementação do processo com camadas de saída e atualização direta das camadas de entrada.
        """
        tolerancia = self.parameterAsDouble(parameters, self.TOL, context)
        pointLayer = self.parameterAsVectorLayer(parameters, self.INPUT_POINT, context)
        filter_expression = self.parameterAsExpression(parameters, self.FILTER_EXPRESSION, context)

        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building id dict"))
        
        algRunner = AlgRunner()
        pointLayerWithIDs = algRunner.runCreateFieldWithExpression(pointLayer, '@id', 'featid', context, fieldType=1)
        algRunner.runCreateSpatialIndex(
            inputLyr=pointLayerWithIDs,
            context=context,
        )
        dictPointIdFeat = {point['featid']:point for point in pointLayerWithIDs.getFeatures()}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Passando de multipart para singlepart..."))
        singlepart = algRunner.runMultipartToSingleParts(pointLayerWithIDs, context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Multipart para Singlepart completo..."))

        multiStepFeedback.setProgressText(self.tr("Clusterizando..."))
        clusterizado = algRunner.runDBScanClustering(singlepart, 2, tolerancia, context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Clusterização completa..."))

        multiStepFeedback.setProgressText(self.tr("Filtrando pontos..."))
        filtered_points, non_filtered_points = algRunner.runFilterExpressionWithFailOutput(clusterizado, filter_expression, context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Filtragem completa..."))

        multiStepFeedback.setProgressText(self.tr("Criando buffers a partir dos pontos..."))
        non_filtered_buffers = algRunner.runBuffer(non_filtered_points, tolerancia, context) #alta prioridade
        filtered_buffers = algRunner.runBuffer(filtered_points, tolerancia, context) #baixa prioridade
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Criação de buffers concluída..."))

        dictCluster = self.makeDictCluster(clusterizado, filtered_points, non_filtered_points, filtered_buffers, non_filtered_buffers, feedback=multiStepFeedback)
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
       

        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count())
        futures = set()
        def compute(cluster):
            currentStep = 0
            multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Preparando para rodar em paralelo..."))
            idsToFlagCompute = set()
            IDsToDeleteCompute = set()
            featsToSink = set()
            filtered_points, non_filtered_points, filtered_buffers, non_filtered_buffers = cluster[0], cluster[1],cluster[2], cluster[3]
            #1: alta prioridade - alta prioridade

            for point in non_filtered_points:
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    return
                pointGeom = point.geometry()
                geomEngine = QgsGeometry.createGeometryEngine(pointGeom.constGet())
                geomEngine.prepareGeometry()
                point_id = point['featid']
                for buffer in non_filtered_buffers:
                    bufferGeom = buffer.geometry()
                    buffer_id = buffer['featid']
                    if point_id==buffer_id or point_id in idsToFlagCompute:
                        continue
                    if not geomEngine.intersects(bufferGeom.constGet()):
                        continue
                    bufferPoint = dictPointIdFeat[buffer_id]
                    featsToSink.add(dictPointIdFeat[point_id])
                    idsToFlagCompute.add(point_id)
                    featsToSink.add(bufferPoint)
                    idsToFlagCompute.add(buffer_id)
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Análise 'alta prioridade - alta prioridade' completa..."))

            multiStepFeedback.setProgressText(self.tr("Iniciando criação de dicionários..."))
            intersections_dict = {}
            for point in filtered_points:
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    return
                pointGeom = point.geometry()
                geomEngine = QgsGeometry.createGeometryEngine(pointGeom.constGet())
                geomEngine.prepareGeometry()
                point_id = point['featid']
                if point_id in IDsToDeleteCompute:
                    continue
                #2: baixa prioridade -  alta prioridade

                for buffer in non_filtered_buffers:
                    bufferGeom = buffer.geometry()
                    if not geomEngine.intersects(bufferGeom.constGet()):
                        continue
                    IDsToDeleteCompute.add(point_id)
            
                #3: baixa prioridade - baixa prioridade (dict)
                if point_id not in intersections_dict:
                    intersections_dict[point_id] = []
                for buffer in filtered_buffers:
                    bufferGeom = buffer.geometry()
                    geomEngine = QgsGeometry.createGeometryEngine(bufferGeom.constGet())
                    geomEngine.prepareGeometry()
                    buffer_id = buffer['featid'] 
                    if point_id == buffer_id or point_id in IDsToDeleteCompute or buffer_id in IDsToDeleteCompute:
                        continue
                    if not geomEngine.intersects(bufferGeom.constGet()):
                        continue
                    intersections_dict[point_id].append(buffer_id)
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Criação de dicionários completa..."))
            #3: baixa prioridade - baixa prioridade
            maxIntersections=1
            if not intersections_dict:
                return idsToFlagCompute, IDsToDeleteCompute, featsToSink
            while maxIntersections>0:
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    return
                maxIntersections = max(map(len, intersections_dict.values()))
                chave_maxima = min(s for s in intersections_dict if len(intersections_dict[s]) == maxIntersections)
                
                if chave_maxima in IDsToDeleteCompute:
                    continue
                IDsToDeleteCompute.add(chave_maxima)

                for id_ponto in intersections_dict[chave_maxima]:
                    if not chave_maxima in intersections_dict[id_ponto]:
                        continue
                    intersections_dict[id_ponto].remove(chave_maxima)
                del intersections_dict[chave_maxima]
            return idsToFlagCompute, IDsToDeleteCompute, featsToSink
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Chamando a função 'compute' para rodar em paralelo..."))
        for cluster in dictCluster.values():
            futures.add(pool.submit(compute, cluster))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Processo em paralelo completo..."))

        multiStepFeedback.setProgressText(self.tr("Adicionando feições ao sink..."))
        fields = pointLayer.fields()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Point,
            pointLayer.sourceCrs()
        )
        idsToFlag = set()
        idsToDelete = set()
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                return
            idsToFlagResult, IDsToDeleteResult, featsToSink = future.result()
            idsToFlag = idsToFlag.union(idsToFlagResult)
            idsToDelete = idsToDelete.union(IDsToDeleteResult)
            for feat in featsToSink:
                fieldsFeat = [f.name() for f in feat.fields()]
                newFeat = QgsFeature(fields)
                for field in fields:
                    fieldName = field.name()
                    if fieldName not in fieldsFeat:
                        continue
                    newFeat[fieldName] = feat[fieldName]
                newFeat.setGeometry(feat.geometry())
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        multiStepFeedback.setProgressText(self.tr("Adição de feições ao Sink completa..."))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Deletando feições selecionadas..."))
        pointLayer.startEditing() 
        pointLayer.beginEditCommand(self.tr("Deleting features"))
        pointLayer.deleteFeatures(list(idsToDelete))   
        pointLayer.endEditCommand()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Feições deletadas..."))
        return {self.OUTPUT: dest_id}
    
    def makeDictCluster(self, clusterLayer: QgsVectorLayer, filteredPoints: QgsVectorLayer, nonFilteredPoints: QgsVectorLayer, filteredBuffers: QgsVectorLayer, nonFilteredBuffers: QgsVectorLayer, feedback: QgsProcessingFeedback = None):
        dictCluster = dict()
        for cluster in clusterLayer.getFeatures():
            if feedback is not None and feedback.isCanceled():
                return dictCluster
            clusterID = cluster["CLUSTER_ID"]
            
            filteredPointList = []
            nonFilteredPointList = []
            filteredBufferList = []
            nonFilteredBufferList = []
            
            request = QgsFeatureRequest()
            request.setFilterExpression(f"CLUSTER_ID = {clusterID}")
            if clusterID not in dictCluster:
                dictCluster[clusterID] = []

            for filtered_points_feat in filteredPoints.getFeatures(request):
                filteredPointList.append(filtered_points_feat)
                if feedback is not None and feedback.isCanceled():
                    return dictCluster
            dictCluster[clusterID].append(filteredPointList)
            
            for non_filtered_points_feat in nonFilteredPoints.getFeatures(request):
                nonFilteredPointList.append(non_filtered_points_feat)
                if feedback is not None and feedback.isCanceled():
                    return dictCluster
            dictCluster[clusterID].append(nonFilteredPointList)
            
            for filtered_buffers_feat in filteredBuffers.getFeatures(request):
                filteredBufferList.append(filtered_buffers_feat)
                if feedback is not None and feedback.isCanceled():
                    return dictCluster
            dictCluster[clusterID].append(filteredBufferList)
            
            for non_filtered_buffers_feat in nonFilteredBuffers.getFeatures(request):
                nonFilteredBufferList.append(non_filtered_buffers_feat)
                if feedback is not None and feedback.isCanceled():
                    return dictCluster
            dictCluster[clusterID].append(nonFilteredBufferList)
        return dictCluster

    def name(self):
        return "generalizeedificationsareaalgorithm"

    def displayName(self):
        return self.tr("Generalizar Edificações")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeEdificationsAlgorithm", string)
    
    def shortHelpString(self):
        return self.tr(
            "Dentre outros inputs, este algoritmo recebe uma expressão, que será utilizada para distinguir as feições de baixa prioridade (as que satisfazem à expressão). A partindo daí, o processing executa os seguintes passos: \n1.Eliminar genéricas próximas de edificações específicas;\n2. Eliminar edificações próximas de mesmo tipo;"
        )

    def createInstance(self):
        return GeneralizeEdificationsAlgorithm()
