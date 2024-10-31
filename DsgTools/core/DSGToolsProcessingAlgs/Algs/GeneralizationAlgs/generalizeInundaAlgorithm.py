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
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterDistance,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeUtils import GeneralizeUtils

class GeneralizeInundaAlgorithm(QgsProcessingAlgorithm):
    
    INUNDA = "INUNDA"
    SCALE = "SCALE"
    MIN_INUNDA_WIDTH = "MIN_INUNDA_WIDTH"
    MIN_INUNDA_AREA = "MIN_INUNDA_AREA"
    MIN_INUNDA_HOLE_AREA = "MIN_INUNDA_HOLE_AREA"

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
            QgsProcessingParameterDistance(
                self.SCALE,
                self.tr("Scale"),
                parentParameterName=self.INUNDA,
                minValue=0,
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_INUNDA_WIDTH, self.tr("Minimum inunda width tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        param = QgsProcessingParameterDistance(
            self.MIN_INUNDA_AREA, self.tr("Minimum inunda area tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        param = QgsProcessingParameterDistance(
            self.MIN_INUNDA_HOLE_AREA, self.tr("Minimum inunda hole area tolerance"),
            parentParameterName=self.INUNDA,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        
        inunda_layer = self.parameterAsVectorLayer(parameters, self.INUNDA, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_inunda_width = self.parameterAsDouble(parameters, self.MIN_INUNDA_WIDTH, context)
        min_inunda_area = self.parameterAsDouble(parameters, self.MIN_INUNDA_AREA, context)
        min_inunda_hole_area = self.parameterAsDouble(parameters, self.MIN_INUNDA_HOLE_AREA, context)
        

        if inunda_layer is None:
            feedback.reportError('Layer not defined correctly.')
            return {}

        min_inunda_width_tolerance = min_inunda_width*scale
        min_inunda_area_tolerance = min_inunda_area*(scale**2)
        min_inunda_hole_area_tolerance = min_inunda_hole_area*(scale**2)

        layerHandler = LayerHandler()
        generalizeUtils = GeneralizeUtils()
        algRunner = AlgRunner()
        

        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inunda_layer],
            geomType=inunda_layer.wkbType(),
        )
        print(localInputLayerCache.featureCount())

        steps = 12
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying strangle."))
        strangled_inunda = generalizeUtils.runStrangle(layer=localInputLayerCache, length_tol=min_inunda_width_tolerance, area_tol=min_inunda_area_tolerance, context=context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        filteredSmallInunda = algRunner.runSmallHoleRemoverAlgorithm(
            inputLayer=strangled_inunda,
            max_hole_area=min_inunda_hole_area_tolerance,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        filteredSmallHolesInunda = algRunner.runFilterExpression(
            inputLyr=filteredSmallInunda,
            expression=f"""area($geometry) >= {min_inunda_area_tolerance} """,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Editing inunda."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [inunda_layer],
            filteredSmallHolesInunda,
            feedback=multiStepFeedback,
            onlySelected= False,
        )
    
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
            "Generaliza inundação.\nScale: Escolha a escala desejada. Exemplo: '50' para 50k.\nMinimum inunda width tolerance: Escolha o comprimento mínimo da inundação em graus. Exemplo: '0,000008' para 0,8mm.\nMinimum inunda area tolerance: Escolha a área mínima da inundaçãoem graus quadrados. Exemplo: '0,0000000004' para 4mm²."
        )


    def tr(self, string):
        return QCoreApplication.translate("GeneralizeInundaAlgorithm", string)

    def createInstance(self):
        return GeneralizeInundaAlgorithm()
