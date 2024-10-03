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
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsProcessingMultiStepFeedback
)
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
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
        area_tolerancia = 3.16*10**(-8)

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
        layerHandler = LayerHandler()

        steps = 1
        multi_step_feedback = QgsProcessingMultiStepFeedback(steps, feedback)

        localCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [water_body_layer],
            geomType=water_body_layer.wkbType(),
            onlySelected= False,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Applying dissolve...')
        dissolve = algRunner.runDissolve(localCache, context=context, feedback=multi_step_feedback)
        if not dissolve:
            feedback.reportError('Error on dissolve process.')
            return {}
        feedback.pushInfo('Dissolve successfully applied.')

        feedback.pushInfo('Applying negative buffer to remove thin parts...')
        buffer_neg = algRunner.runBuffer(dissolve, distance=-min_width / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
        if not buffer_neg:
            feedback.reportError('Negative buffer was not generated correctly.')
            return {}
        feedback.pushInfo('Negative buffer generated successfully.')

        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        singlepart = algRunner.runMultipartToSingleParts(buffer_neg, context=context, feedback=multi_step_feedback)
        if not singlepart:
            feedback.reportError('singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Removing null geometries manually...')
        removenull = algRunner.runRemoveNull(singlepart, context=context, feedback=multi_step_feedback)
        if not removenull:
            feedback.reportError('Null geometries not removed.')
            return {}
        feedback.pushInfo('Null geometries removed successfully.')

        feedback.pushInfo('Removing duplicate vertices...')
        cleaned_duplicates = algRunner.runRemoveDuplicatedGeometries(removenull, context=context, feedback=multi_step_feedback)
        if not cleaned_duplicates:
            feedback.reportError('Removing duplicate vertices failed.')
            return {}
        feedback.pushInfo('Duplicate vertices removed successfully.')

        feedback.pushInfo('Applying positive buffer to restore to initial state...')
        buffer_pos = algRunner.runBuffer(cleaned_duplicates, distance=min_width / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
        if not buffer_pos:
            feedback.reportError('Positive buffer was not generated correctly.')
            return {}
        
        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        newsinglepart = algRunner.runMultipartToSingleParts(buffer_pos, context=context, feedback=multi_step_feedback)
        if not newsinglepart:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Taking the difference between original water body and the newest one...')
        difference = algRunner.runDifference(localCache, newsinglepart, context=context, feedback=multi_step_feedback)
        if not difference:
            feedback.reportError('Difference was not possible to take.')
            return {}
        feedback.pushInfo('Difference successfully taken.')

        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        newnewsinglepart = algRunner.runMultipartToSingleParts(difference, context=context, feedback=multi_step_feedback)
        if not newnewsinglepart:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Filtering geometries by area...')
        filtered_features = []
        for feat in newnewsinglepart.getFeatures():
            geom = feat.geometry()
            if geom.area() >= area_tolerancia:
                filtered_features.append(feat)
        filtered_holes = QgsVectorLayer("Polygon", "filtered_geometry", "memory")
        filtered_holes.setCrs(newnewsinglepart.crs())
        filtered_holes.dataProvider().addFeatures(filtered_features)
        
        feedback.pushInfo('Taking the difference between original water body and the newest one...')
        newdifference = algRunner.runDifference(localCache, filtered_holes, context=context, feedback=multi_step_feedback)
        if not newdifference:
            feedback.reportError(self.tr('Difference was not possible to take.'))
            return {}
        feedback.pushInfo('Difference successfully taken.')

        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        newnewnewsinglepart = algRunner.runMultipartToSingleParts(newdifference, context=context, feedback=multi_step_feedback)
        if not newnewnewsinglepart:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Editing water bodies')
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [water_body_layer],
            newnewnewsinglepart,
            feedback=multi_step_feedback,
            onlySelected= False,
        )
        feedback.pushInfo('Water bodies edition finished')

        feedback.pushInfo('Generating output layer.')
        for feat in filtered_holes.getFeatures():
            newFeat = QgsFeature(fields)
            geomFeatAdd = feat.geometry()
            newFeat.setGeometry(geomFeatAdd)
            for field in feat.fields():
                newFeat[field.name()] = feat[field.name()]
            output_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

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
