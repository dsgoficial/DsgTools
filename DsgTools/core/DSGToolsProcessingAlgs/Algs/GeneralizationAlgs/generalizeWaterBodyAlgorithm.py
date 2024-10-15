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
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsFeatureSink,
    QgsFeature,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsVectorLayer,
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
    MIN_WATER_BODY_AREA = "MIN_WATER_BODY_AREA"
    ISLAND = "ISLAND"
    MIN_ISLAND_AREA = "MIN_ISLAND_AREA"
    DRAINAGE_SECTION = "DRAINAGE_SECTION"
    DRAINAGE_FIELD = "DRAINAGE_FIELD"
    DRAINAGE_FIELD_VALUE = "DRAINAGE_FIELD_VALUE"
    MIN_DRAINAGE_SECTION_WIDTH = "MIN_DRAINAGE_SECTION_WIDTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    OUTPUT_HOLE = "OUTPUT_HOLE"
    OUTPUT_LINE = "OUTPUT_LINE"
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
                self.tr("Island (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_ISLAND_AREA,
                self.tr("Minimum island area tolerance in square millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=4,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.DRAINAGE_SECTION,
                self.tr("Drainage section (line layer)"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.DRAINAGE_FIELD,
                self.tr('Select field from Drainage Section'),
                parentLayerParameterName=self.DRAINAGE_SECTION,
                type=QgsProcessingParameterField.Any
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.DRAINAGE_FIELD_VALUE,
                self.tr('Value to set for field (outside polygon)'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_DRAINAGE_SECTION_WIDTH,
                self.tr("Drainage section width tolerance in millimeters"),
                QgsProcessingParameterNumber.Double,
                minValue=0.1,
                defaultValue=10,
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
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_HOLE,
                self.tr("Output Layer (Polygon)"),
                type=QgsProcessing.TypeVectorPolygon
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LINE,
                self.tr("Output Layer (Line)"),
                type=QgsProcessing.TypeVectorLine
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
        min_island_area = self.parameterAsDouble(parameters, self.MIN_ISLAND_AREA, context)
        drainage_section_layer = self.parameterAsVectorLayer(parameters, self.DRAINAGE_SECTION, context)
        drainage_field = self.parameterAsString(parameters, 'DRAINAGE_FIELD', context)
        drainage_field_value = self.parameterAsString(parameters, 'DRAINAGE_FIELD_VALUE', context)
        min_drainage_section_width = self.parameterAsDouble(parameters, self.MIN_DRAINAGE_SECTION_WIDTH, context)
        geographicBoundsLayer = self.parameterAsLayer(parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context)
        pointLayerList = self.parameterAsLayerList(parameters, self.POINT_CONSTRAINT_LAYER_LIST, context)
        lineLayerList = self.parameterAsLayerList(parameters, self.LINE_CONSTRAINT_LAYER_LIST, context)
        polygonLayerList = self.parameterAsLayerList(parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context)

        if water_body_layer is None or island_layer is None or drainage_section_layer is None:
            feedback.reportError('Layers not defined correctly.')
            return {}

        if water_body_layer.crs().isGeographic():
            min_water_body_width_tolerance = (min_water_body_width * scale) / (10**5)
        else:
            min_water_body_width_tolerance = (min_water_body_width * scale)

        min_water_body_area_tolerance = (min_water_body_area * (scale ** 2))
        min_island_area_tolerance = (min_island_area * (scale ** 2))

        if drainage_section_layer.crs().isGeographic():
            min_drainage_section_width_tolerance = (min_drainage_section_width * (scale)) / (10**5)
        else:
            min_drainage_section_width_tolerance = (min_drainage_section_width * (scale))
        
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
        '''
        smallFeaturesLyr, localCache = localCache#filtrado
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

        feedback.pushInfo('Filtering features')
        filtered_bodywater = algRunner.runFilterExpression(
            inputLyr=localBodyWaterCache,
            expression=f"""$area >= {min_water_body_area*15625}""",
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Features filtered by area successfully.')

        unified_layer = algRunner.runMergeVectorLayers(
            [filtered_waterbodystretch,filtered_bodywater],
            context=context,
            feedback=multi_step_feedback,
        )
        
        feedback.pushInfo('Finding holes on geometry...')
        _, hole = algRunner.runDonutHoleExtractor(
            inputLyr=unified_layer,
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Holes successfully saved...')

        filtered_hole = algRunner.runFilterExpression(
            inputLyr=hole,
            expression=f"""$area < {min_water_body_area_tolerance}""",
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
            expression=f"""$area >= {min_island_area_tolerance}""",
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
            expression=f"""$area < {min_island_area_tolerance}""",
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
        feedback.pushInfo('Transformation done.')

        drainage_section_layer.startEditing()
        drainage_section_layer.beginEditCommand(self.tr('Drainage section field updating for features outside water body.'))
        water_body_index = QgsSpatialIndex(water_body_layer.getFeatures())
        for drainage_feature in drainage_section_layer.getFeatures():
            drainage_geom = drainage_feature.geometry()
            intersects = False
            for water_body_id in water_body_index.intersects(drainage_geom.boundingBox()):
                water_body_feature = water_body_layer.getFeature(water_body_id)
                if water_body_feature.geometry().intersects(drainage_geom):
                    intersects = True
                    break
            if not intersects:
                drainage_feature.setAttribute(drainage_field, drainage_field_value)
                drainage_section_layer.updateFeature(drainage_feature)
        drainage_section_layer.endEditCommand()
        feedback.pushInfo('Drainage section field updated for features outside water body.')

        feedback.pushInfo('Editing Drainage sections.')
        algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(inputLayer=drainage_section_layer, context=context, min_length=min_drainage_section_width_tolerance, bounds_layer=geographicBoundsLayer, spatial_partition=True, pointlyr_list=pointLayerList, linelyr_list=lineLayerList, polygonlyr_list=polygonLayerList, method = 0)
        feedback.pushInfo('Drainage sections edition finished')

        feedback.pushInfo('Finding Small Islands.')
        drainage_inside_polygon = algRunner.runFilterExpression(
            inputLyr=drainage_section_layer,
            expression=f"""{drainage_field} != {drainage_field_value}""",
            context=context,
            feedback=multi_step_feedback,
        )
        feedback.pushInfo('Small Islands identified.')

        
        feedback.pushInfo('Eliminating secundary stretchs.')
        drainage_poligonized = algRunner.runPolygonize(inputLyr=drainage_inside_polygon, context=context,feedback=multi_step_feedback, )
        algRunner.runCreateSpatialIndex(inputLyr=drainage_poligonized, context=context, feedback=multi_step_feedback, is_child_algorithm=True)
        drainage_poligonized_filtered = algRunner.runExtractByLocation(inputLyr=drainage_poligonized, intersectLyr=filtered_hole, predicate=[1], context=context,feedback=multi_step_feedback)
        drainage_poligonized_autoincremet = algRunner.runAddAutoIncrementalField(inputLyr=drainage_poligonized_filtered, context=context,feedback=multi_step_feedback)
        drainage_filtered_line = algRunner.runPolygonsToLines( inputLyr=drainage_poligonized_autoincremet, context=context,feedback=multi_step_feedback)
        feedback.pushInfo('Secundary streths successfully eliminated.')
        

        feedback.pushInfo('Generating output layer.')
        filtered_hole_fields = filtered_hole.fields()
        point_island_fields = pointIsland.fields()
        hole_output_sink, hole_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_HOLE, context, filtered_hole_fields, QgsWkbTypes.Polygon, filtered_hole.crs()
        )
        line_output_sink, line_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_LINE, context, filtered_hole_fields, QgsWkbTypes.LineString, filtered_hole.crs()
        )
        island_fields = island_layer.fields()
        island_output_sink, island_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_SMALL_ISLAND, context, island_fields, QgsWkbTypes.Point, island_layer.crs()
        )
        for feat in drainage_poligonized_autoincremet.getFeatures():
            newPolygon = QgsFeature(drainage_poligonized_autoincremet.fields())
            newPolygon.setGeometry(feat.geometry())
            for field in feat.fields():
                newPolygon.setAttribute(field.name(), feat[field.name()])
            hole_output_sink.addFeature(newPolygon, QgsFeatureSink.FastInsert)
        for feat in drainage_filtered_line.getFeatures():
            newLine = QgsFeature(drainage_filtered_line.fields())
            newLine.setGeometry(feat.geometry())
            for field in feat.fields():
                newLine.setAttribute(field.name(), feat[field.name()])
            line_output_sink.addFeature(newLine, QgsFeatureSink.FastInsert)
        for feat in pointIsland.getFeatures():
            newPoint = QgsFeature(point_island_fields)
            newPoint.setGeometry(feat.geometry())
            for field in feat.fields():
                newPoint.setAttribute(field.name(), feat[field.name()])
            island_output_sink.addFeature(newPoint, QgsFeatureSink.FastInsert)

        feedback.pushInfo('Returning output layer.')
        return {self.OUTPUT_HOLE: hole_output_id, self.OUTPUT_SMALL_ISLAND: island_output_id, self.OUTPUT_LINE:line_output_id}

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
