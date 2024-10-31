# -*- coding: utf-8 -*-
"""
/***************************************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-01
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jaime Guilherme - Cartographic Engineer @ Brazilian Army
        email                : jaime.breda@ime.eb.br
 ***************************************************************************************************/

 /***************************************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************************************/
"""
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsWkbTypes,
    QgsFeature,
    QgsFields,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeUtils import GeneralizeUtils

class GeneralizeInundaAlgorithm(QgsProcessingAlgorithm):
    
    INUNDA = "INUNDA"
    SCALE = "SCALE"
    MIN_INUNDA_WIDTH = "MIN_INUNDA_WIDTH"
    MIN_INUNDA_AREA = "MIN_INUNDA_AREA"
    MAX_INUNDA_HOLE_AREA = "MAX_INUNDA_HOLE_AREA"
    OUTPUT_POLYGON = "OUTPUT_POLYGON"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INUNDA,
                self.tr("Inunda (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE,
                self.tr("Scale"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_INUNDA_WIDTH, self.tr("Minimum inunda width tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(param
        )
        param = QgsProcessingParameterDistance(
            self.MIN_INUNDA_AREA, self.tr("Minimum inunda area tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(param
        )
        param = QgsProcessingParameterDistance(
            self.MAX_INUNDA_HOLE_AREA, self.tr("nMaximum inunda hole area tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(param
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POLYGON,
                self.tr("Output Removed Polygons"),
                type=QgsProcessing.TypeVectorPolygon
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        
        inunda_layer = self.parameterAsVectorLayer(parameters, self.INUNDA, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_inunda_width = self.parameterAsDouble(parameters, self.MIN_INUNDA_WIDTH, context)
        min_inunda_area = self.parameterAsDouble(parameters, self.MIN_INUNDA_AREA, context)
        max_inunda_hole_area = self.parameterAsDouble(parameters, self.MAX_INUNDA_HOLE_AREA, context)
        

        if inunda_layer is None:
            feedback.reportError('Layer not defined correctly.')
            return {}

        min_inunda_width_tolerance = min_inunda_width*scale
        min_inunda_area_tolerance = min_inunda_area*(scale**2)
        max_inunda_hole_area_tolerance = max_inunda_hole_area*(scale**2)

        layerHandler = LayerHandler()
        generalizeUtils = GeneralizeUtils()
        algRunner = AlgRunner()
        

        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inunda_layer],
            geomType=inunda_layer.wkbType(),
        )

        steps = 12
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying strangle."))
        strangled_inunda = generalizeUtils.runStrangle(layer=localInputLayerCache, length_tol=min_inunda_width_tolerance, context=context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        filteredSmallHolesInunda = algRunner.runSmallHoleRemoverAlgorithm(
            inputLayer=strangled_inunda,
            max_hole_area=max_inunda_hole_area_tolerance,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        filteredSmallInunda = algRunner.runFilterExpression(
            inputLyr=filteredSmallHolesInunda,
            expression=f"""area($geometry) >= {min_inunda_area_tolerance} """,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Editing inunda."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inunda_layer],
            filteredSmallInunda,
            feedback=multiStepFeedback,
            onlySelected= False,
        )
        
        inunda_removed = algRunner.runDifference(
            inputLyr=localInputLayerCache,
            overlayLyr=filteredSmallInunda,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Generating output layer."))
        polygon_fields = QgsFields()

        polygon_output_sink, polygon_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_POLYGON, context, polygon_fields, QgsWkbTypes.Polygon, inunda_removed.crs()
        )
        for feature in inunda_removed.getFeatures():
            new_feature = QgsFeature(polygon_fields)
            new_feature.setGeometry(feature.geometry())
            polygon_output_sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        self.sink_dict = {
            inunda_removed.id(): polygon_output_sink,
        }
        lyrList = [inunda_removed]
        
        multiStepFeedback.setProgressText(self.tr("Adding to sink."))
        for lyr in lyrList:
            self.iterateAndAddToSink(lyr, feedback)
        multiStepFeedback.setProgressText(self.tr("Returning output layer."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        return {self.OUTPUT_POLYGON:polygon_output_id}
    
    def iterateAndAddToSink(self, lyr, feedback=None):
        sink = self.sink_dict.get(lyr.id(), None)
        if sink is None:
            return
        nFeatures = lyr.featureCount()
        if nFeatures == 0:
            return
        stepSize = 100/nFeatures
        for current, feat in enumerate(lyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                return
            newFeat = self.createNewFeature(lyr.fields(), feat)
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            if feedback is not None:
                feedback.setProgress(current * stepSize)

    def createNewFeature(self, fields:QgsFields, feat:QgsFeature)->QgsFeature:
        fieldsFeat = [f.name() for f in feat.fields()]
        newFeat = QgsFeature(fields)
        newFeat.setGeometry(feat.geometry())
        for field in fields:
            fieldName = field.name()
            if fieldName not in fieldsFeat:
                continue
            newFeat[fieldName]=feat[fieldName]
        return newFeat
    
    def name(self):
        return "generalizeinundaalgorithm"

    def displayName(self):
        return self.tr("Generalize Inunda Algorithm")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"
    
    def shortHelpString(self):
        return self.tr(
            "Generaliza inundação.\nScale: Escolha a escala desejada. Exemplo: '50000' para 50k.\nMinimum inunda width tolerance: Escolha o comprimento mínimo da inundação em graus. Exemplo: '0,000000008' para 0,8mm.\nMinimum inunda area tolerance: Escolha a área mínima da inundaçãoem graus quadrados. Exemplo: '0,0000000000000025' para 25mm².\nMaximum inunda home area tolerance: Escolha a área máxima dos buracos em graus quadrados. Exemplo: '0,0000000000000004' para 4mm²."
        )


    def tr(self, string):
        return QCoreApplication.translate("GeneralizeInundaAlgorithm", string)

    def createInstance(self):
        return GeneralizeInundaAlgorithm()
