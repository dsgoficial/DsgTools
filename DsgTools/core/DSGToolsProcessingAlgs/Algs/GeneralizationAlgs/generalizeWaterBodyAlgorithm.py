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
    QgsProcessingParameterMultipleLayers,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsWkbTypes,
    QgsProcessingParameterFeatureSink,
    QgsFeatureSink,
    QgsFeature,
    QgsVectorLayer,
    QgsProcessingMultiStepFeedback,
    QgsFeatureRequest,
)
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class GeneralizeWaterBodyAlgorithm(QgsProcessingAlgorithm):
    WATER_BODY = "WATER_BODY"
    #RIVERS_WITH_FLOW = "RIVERS_WITH_FLOW"
    #RIVERS_WITHOUT_FLOW = "RIVERS_WITHOUT_FLOW"
    EXPRESSION = "EXPRESSION"
    SCALE = "SCALE"
    MIN_WATER_BODY_WIDTH = "MIN_WATER_BODY_WIDTH"
    ISLAND = "ISLAND"
    MIN_WATER_BODY_AREA = "MIN_WATER_BODY_AREA"
    OUTPUT_SMALL_WATER_BODY = "OUTPUT_SMALL_WATER_BODY"
    OUTPUT_SMALL_ISLAND = "OUTPUT_SMALL_ISLAND"

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
        '''
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.RIVERS_WITH_FLOW,
                self.tr("Select rivers with flow (multiple line layers)"),
                layerType=QgsProcessing.TypeVectorLine
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.RIVERS_WITHOUT_FLOW,
                self.tr("Select rivers without flow (multiple line layers)"),
                layerType=QgsProcessing.TypeVectorLine
            )
        )
        '''
        self.addParameter(
            QgsProcessingParameterString(
                self.EXPRESSION,
                self.tr("Flow types expression"),
                defaultValue="tipo in (1,2,9,10)",
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
                self.MIN_WATER_BODY_WIDTH,
                self.tr("Minimum body water width tolerance in millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=0.8,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_WATER_BODY_AREA,
                self.tr("Minimum body water area tolerance in square millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=4,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.ISLAND,
                self.tr("Island Elemnat (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_SMALL_WATER_BODY,
                self.tr("Output Layer (Polygon)"),
                type=QgsProcessing.TypeVectorPolygon
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_SMALL_ISLAND,
                self.tr("Output Small Island (Point)"),
                type=QgsProcessing.TypeVectorPoint
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        water_body_layer = self.parameterAsVectorLayer(parameters, self.WATER_BODY, context)
        #river_with_flow = self.parameterAsLayerList(parameters, self.RIVERS_WITH_FLOW, context)
        #river_no_flow = self.parameterAsLayerList(parameters, self.RIVERS_WITHOUT_FLOW, context)
        expression = self.parameterAsString(parameters, self.EXPRESSION, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_water_body_width = self.parameterAsDouble(parameters, self.MIN_WATER_BODY_WIDTH, context)
        island_layer = self.parameterAsVectorLayer(parameters, self.ISLAND, context)
        min_water_body_area = self.parameterAsDouble(parameters, self.MIN_WATER_BODY_AREA, context)

        if water_body_layer is None or island_layer is None:
            return {}

        water_body_fields = water_body_layer.fields()
        water_body_output_sink, waterbody_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_SMALL_WATER_BODY, context, water_body_fields, water_body_layer.wkbType(), water_body_layer.crs()
        )
        island_fields = island_layer.fields()
        island_output_sink, island_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_SMALL_ISLAND, context, island_fields, QgsWkbTypes.Point, island_layer.crs()
        )
        dict_water_body_featid_feat = {feat.id():feat for feat in water_body_layer.getFeatures()}

        if water_body_layer.crs().isGeographic():
            min_water_body_width_tolerance = (min_water_body_width * scale) / (10**5)
        else:
            min_water_body_width_tolerance = (min_water_body_width * scale)
        min_water_body_area_tolerance = (min_water_body_area * (scale ** 2))
        
        if island_layer.crs().isGeographic():
            toleranceIsland = 1 / (10**5)
        else:
            toleranceIsland = 1

        algRunner = AlgRunner()
        layerHandler = LayerHandler()

        steps = 1
        multi_step_feedback = QgsProcessingMultiStepFeedback(steps, feedback)
        localWaterBodyCache = algRunner.runCreateFieldWithExpression(
            water_body_layer,
            '@id',
            'featid',
            context
        )
        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [water_body_layer],
            geomType=water_body_layer.wkbType(),
            onlySelected= False,
            feedback=multi_step_feedback,
        )
        localIslandCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [island_layer],
            geomType=island_layer.wkbType(),
            onlySelected= False,
            feedback=multi_step_feedback,
        )
        '''smallFeaturesLyr, localCache = localCache#filtrado
        idsToRemove = [feat["featid"] for feat in smallFeaturesLyr.getFeatures()]
        if idsToRemove:
            water_body_layer.startEditing()
            water_body_layer.deleteFeatures(idsToRemove)
        '''
        feedback.pushInfo("Filtering flow types from water bodies...")
        rivers= algRunner.runFilterExpression(
            inputLyr=localWaterBodyCache,
            expression=expression,
            context=context,
            feedback=multi_step_feedback,
            outputLyr="memory:",
        ) 
        riversIdsTuple = (str(int(river["featid"])) for river in rivers.getFeatures())
        riversIdsStr = ','.join(riversIdsTuple)
        filterRiversIdsExpression = f'featid in ({riversIdsStr})'

        localRiversCache, localBodyWaterCache = algRunner.runFilterExpressionWithFailOutput(
            inputLyr=localInputLayerCache,
            expression=filterRiversIdsExpression,
            context=context,
            feedback=multi_step_feedback,
        ) 

        feedback.pushInfo('Applying dissolve...')
        dissolve = algRunner.runDissolve(localRiversCache, context=context, feedback=multi_step_feedback)
        if not dissolve:
            feedback.reportError('Error on dissolve process.')
            return {}
        feedback.pushInfo('Dissolve successfully applied.')

        feedback.pushInfo('Applying negative buffer to remove thin parts...')
        buffer_neg = algRunner.runBuffer(dissolve, distance=-min_water_body_width_tolerance / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
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

        feedback.pushInfo('Applying positive buffer to restore to initial state...')
        buffer_pos = algRunner.runBuffer(removenull, distance=min_water_body_width_tolerance / 2.0, context=context, dissolve=True, feedback=multi_step_feedback)
        if not buffer_pos:
            feedback.reportError('Positive buffer was not generated correctly.')
            return {}
        
        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        # single part pois resultado do buffer dissolvido é sempre multipart (pior para spatialIndex)
        filtered_waterbodystretch = algRunner.runMultipartToSingleParts(buffer_pos, context=context, feedback=multi_step_feedback)
        if not filtered_waterbodystretch:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Taking the difference between original water body and the newest one...')
        holes = algRunner.runDifference(localInputLayerCache, filtered_waterbodystretch, context=context, feedback=multi_step_feedback)
        if not holes:
            feedback.reportError('Difference was not possible to take.')
            return {}
        feedback.pushInfo('Difference successfully taken.')

        feedback.pushInfo('Transforming multipart geometries into singlepart...')
        singlepartholes = algRunner.runMultipartToSingleParts(holes, context=context, feedback=multi_step_feedback)
        if not singlepartholes:
            feedback.reportError('Singlepart was not generated.')
            return {}
        feedback.pushInfo('Singlepart generated successfully.')

        feedback.pushInfo('Filtering features')
        filtered_bodywater = algRunner.runFilterExpression(
            inputLyr=localBodyWaterCache,
            expression=f"""$area >= {min_water_body_area*15625}""",
            context=context,
            feedback=multi_step_feedback,
        )
        filtered_holes = algRunner.runFilterExpression(
            inputLyr=singlepartholes,
            expression=f"""$area >= {min_water_body_area_tolerance}""",
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Features filtered by area successfully.')

        unified_layer = algRunner.runMergeVectorLayers(
            [filtered_waterbodystretch,filtered_bodywater],
            context=context,
            feedback=multi_step_feedback,
        )

        feedback.pushInfo('Editing water bodies')
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [water_body_layer],
            unified_layer,
            feedback=multi_step_feedback,
            onlySelected= False,
        )
        feedback.pushInfo('Water bodies edition finished')

        feedback.pushInfo('Island filtering.')
        filtered_island = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""$area >= {min_water_body_area_tolerance}""",
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Island filtered successfully.')

        feedback.pushInfo('Editing islands.')
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [island_layer],
            filtered_island,
            feedback=multi_step_feedback,
            onlySelected= False,
        )
        feedback.pushInfo('Islands edition finished')

        feedback.pushInfo('Finding Small Islands.')
        smallIsland = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""$area < {min_water_body_area_tolerance}""",
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Small Islands identified.')

        feedback.pushInfo('Transforming Small Islands into points.')
        pointIsland = algRunner.runPoleOfInaccessibility(
            inputLyr=smallIsland,
            tolerance=toleranceIsland,
            context=context,
            feedback=multi_step_feedback,
        )
        point_island_fields = pointIsland.fields()
        feedback.pushInfo('Transformation done.')

        feedback.pushInfo('Generating output layer.')
        for feat in filtered_holes.getFeatures():
            newFeat = QgsFeature(water_body_fields)
            geomFeatAdd = feat.geometry()
            newFeat.setGeometry(geomFeatAdd)
            water_body_feat = dict_water_body_featid_feat[feat["featid"]]
            for field in water_body_fields:
                newFeat.setAttribute(field.name(), water_body_feat[field.name()])
            water_body_output_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        for feat in pointIsland.getFeatures():
            newPoint = QgsFeature(point_island_fields)
            newPoint.setGeometry(feat.geometry())
            for field in feat.fields():
                newPoint.setAttribute(field.name(), feat[field.name()])
            island_output_sink.addFeature(newPoint, QgsFeatureSink.FastInsert)

        feedback.pushInfo('Returning output layer.')
        return {self.OUTPUT_SMALL_WATER_BODY: waterbody_output_id, self.OUTPUT_SMALL_ISLAND: island_output_id}

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
