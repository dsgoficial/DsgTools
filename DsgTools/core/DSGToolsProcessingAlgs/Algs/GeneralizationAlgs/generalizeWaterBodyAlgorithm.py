# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-11-27
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
 ***************************************************************************/

 /***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsFeatureSink,
    QgsFeature,
    QgsProcessingMultiStepFeedback
)
import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class GeneralizeWaterBodyAlgorithm(QgsProcessingAlgorithm):
    WATER_BODY = "WATER_BODY"
    SCALE = "SCALE"
    MIN_WIDTH_MM = "MIN_WIDTH_MM"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY,
                self.tr("Water body (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE,
                self.tr("Scale (e.g., 50 for 50k)"),
                minValue=1,
                defaultValue=50,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_WIDTH_MM,
                self.tr("Minimum width in millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=0.8,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_WIDTH_MM,
                self.tr("Minimum width in millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=0.8,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Output Layer (Polygon)"),
                type=QgsProcessing.TypeVectorPolygon
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        water_body_layer = self.parameterAsVectorLayer(parameters, self.WATER_BODY, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_width_mm = self.parameterAsDouble(parameters, self.MIN_WIDTH_MM, context)

        if water_body_layer is None:
            return {}

        fields = water_body_layer.fields()
        output_sink, output_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields, water_body_layer.wkbType(), water_body_layer.crs()
        )

        if water_body_layer.crs().isGeographic():
            min_width = (min_width_mm * scale) / 100000
        else:
            min_width = (min_width_mm * scale)

        algRunner = AlgRunner()

        steps = 8
        multi_step_feedback = QgsProcessingMultiStepFeedback(steps, feedback)

        multi_step_feedback.setCurrentStep(0)
        feedback.pushInfo('Applying negative buffer to remove thin parts...')
        buffer_neg = algRunner.runBuffer(water_body_layer, distance=-min_width / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
        if not buffer_neg:
            feedback.reportError('Negative buffer was not generated correctly.')
            return {}
        feedback.pushInfo('Negative buffer generated successfully.')

        multi_step_feedback.setCurrentStep(1)
        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        singlepart = algRunner.runMultipartToSingleParts(buffer_neg, context=context, feedback=multi_step_feedback)
        if not singlepart:
            feedback.reportError('singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        multi_step_feedback.setCurrentStep(2)
        feedback.pushInfo('Removing null geometries manually...')
        removenull = algRunner.runRemoveNull(singlepart, context=context, feedback=multi_step_feedback)
        if not removenull:
            feedback.reportError('Null geometries not removed.')
            return {}
        feedback.pushInfo('Null geometries removed successfully.')

        multi_step_feedback.setCurrentStep(3)
        feedback.pushInfo('Removing duplicate vertices...')
        cleaned_duplicates = algRunner.runRemoveDuplicatedGeometries(removenull, context=context, feedback=multi_step_feedback)
        if not cleaned_duplicates:
            feedback.reportError('Removing duplicate vertices failed.')
            return {}
        feedback.pushInfo('Duplicate vertices removed successfully.')

        multi_step_feedback.setCurrentStep(4)
        feedback.pushInfo('Applying positive buffer to restore valid parts...')
        buffer_pos = algRunner.runBuffer(cleaned_duplicates, distance=min_width / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
        if not buffer_pos:
            feedback.reportError('Positive buffer was not generated correctly.')
            return {}
        
        multi_step_feedback.setCurrentStep(5)
        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        newsinglepart = algRunner.runMultipartToSingleParts(buffer_pos, context=context, feedback=multi_step_feedback)
        if not newsinglepart:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        multi_step_feedback.setCurrentStep(6)
        feedback.pushInfo('Taking the difference between original water body and the newest one...')
        difference = algRunner.runDifference(water_body_layer, newsinglepart, context=context, feedback=multi_step_feedback)
        if not difference:
            feedback.reportError('Difference was not possible to take.')
            return {}
        feedback.pushInfo('Difference successfully taken.')

        multi_step_feedback.setCurrentStep(7)
        feedback.pushInfo('Generating output layer.')
        for feat in difference.getFeatures():
            newFeat = QgsFeature(fields)
            geomFeatAdd = feat.geometry()
            newFeat.setGeometry(geomFeatAdd)
            for field in feat.fields():
                newFeat[field.name()] = feat[field.name()]
            output_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

        multi_step_feedback.setCurrentStep(8)
        feedback.pushInfo('Returning output layer.')
        return {self.OUTPUT: output_id}

    def name(self):
        return "generalizewaterbodyalgorithm"

    def displayName(self):
        return self.tr("Generalize Water Body Algorithm")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeWaterBodyAlgorithm", string)

    def createInstance(self):
        return GeneralizeWaterBodyAlgorithm()
