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
# mudar o cabeçalho
# short helpstring
# setProgressText
# indice espacial antes de operacoes geometricas
# nao usar $area para ficar tudo no sistema da camada
# nao deixar tamanho hardcoded
import os
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsFeatureSink,
    QgsFeature,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsField,
    QgsFields,
    QgsProcessingParameterDistance,
    QgsProcessingParameterString,
)
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class GeneralizeWaterBodyAlgorithm(QgsProcessingAlgorithm):
    
    WATER_BODY = "WATER_BODY"
    EXPRESSION = "EXPRESSION"
    SCALE = "SCALE"
    MIN_WATERBODY_WIDTH = "MIN_WATERBODY_WIDTH"
    MIN_WATERBODY_AREA = "MIN_WATERBODY_AREA"
    ISLAND = "ISLAND"
    ISLAND_POINT = "ISLAND_POINT"
    MIN_ISLAND_AREA = "MIN_ISLAND_AREA"
    DRAINAGE_LINES = "DRAINAGE_LINES"
    DRAINAGE_FIELD = "DRAINAGE_FIELD"
    DRAINAGE_FIELD_VALUE = "DRAINAGE_FIELD_VALUE"
    DRAINAGE_FIELD_VALUE_SECUNDARY = "DRAINAGE_FIELD_VALUE_SECUNDARY"
    MIN_DRAINAGE_LINES_WIDTH = "MIN_DRAINAGE_LINES_WIDTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    DAM = "DAM"
    OUTPUT_POLYGON = "OUTPUT_POLYGON"

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
            QgsProcessingParameterExpression(
                self.EXPRESSION,
                self.tr("Flow types expression"),
                parentLayerParameterName=self.WATER_BODY
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.SCALE,
                self.tr("Scale"),
                parentParameterName=self.WATER_BODY,
                minValue=0,
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_WATERBODY_WIDTH, self.tr("Minimum waterbody width tolerance"),
            parentParameterName=self.WATER_BODY,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        param = QgsProcessingParameterDistance(
            self.MIN_WATERBODY_AREA, self.tr("Minimum waterbody area tolerance"),
            parentParameterName=self.WATER_BODY,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.ISLAND,
                self.tr("Island (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.ISLAND_POINT,
                self.tr("Island (point layer)"),
                [QgsProcessing.TypeVectorPoint],
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_ISLAND_AREA, self.tr("Minimum island area tolerance"),
            parentParameterName=self.ISLAND,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.DRAINAGE_LINES,
                self.tr("Drainage lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_DRAINAGE_LINES_WIDTH, self.tr("Minimum drainage line width tolerance"),
            parentParameterName=self.DRAINAGE_LINES,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 10}})
        self.addParameter(param
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.DRAINAGE_FIELD,
                self.tr('Select field from Drainage Lines to classify outside polygons'),
                parentLayerParameterName=self.DRAINAGE_LINES,
                type=QgsProcessingParameterField.Any
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DRAINAGE_FIELD_VALUE,
                self.tr('Value for outside polygon'),
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DRAINAGE_FIELD_VALUE_SECUNDARY,
                self.tr('Value for secundary drainage lines (inside polygons)'),
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
                self.tr("Point constraint layers"),
                QgsProcessing.TypeVectorPoint,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINE_CONSTRAINT_LAYER_LIST,
                self.tr("Line constraint layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGON_CONSTRAINT_LAYER_LIST,
                self.tr("Polygon constraint layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.DAM,
                self.tr("Dam lines"),
                [QgsProcessing.TypeVectorLine],
            )
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
        
        water_body_layer = self.parameterAsVectorLayer(parameters, self.WATER_BODY, context)
        filterRiversExpression = self.parameterAsExpression(parameters, self.EXPRESSION, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_waterbody_width = self.parameterAsDouble(parameters, self.MIN_WATERBODY_WIDTH, context)
        min_waterbody_area = self.parameterAsDouble(parameters, self.MIN_WATERBODY_AREA, context)
        island_layer = self.parameterAsVectorLayer(parameters, self.ISLAND, context)
        island_point_layer = self.parameterAsVectorLayer(parameters, self.ISLAND_POINT, context)
        min_island_area = self.parameterAsDouble(parameters, self.MIN_ISLAND_AREA, context)
        min_drainage_lines_width = self.parameterAsDouble(parameters, self.MIN_DRAINAGE_LINES_WIDTH, context)
        drainage_lines_layer = self.parameterAsVectorLayer(parameters, self.DRAINAGE_LINES, context)
        drainage_field = self.parameterAsString(parameters, self.DRAINAGE_FIELD, context)
        drainage_field_value = self.parameterAsString(parameters, self.DRAINAGE_FIELD_VALUE, context)
        drainage_field_value_secundary = self.parameterAsString(parameters, self.DRAINAGE_FIELD_VALUE_SECUNDARY, context)
        geographicBoundsLayer = self.parameterAsLayer(parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context)
        dam_layer = self.parameterAsVectorLayer(parameters, self.DAM, context)
        pointLayerList = self.parameterAsLayerList(parameters, self.POINT_CONSTRAINT_LAYER_LIST, context)
        lineLayerList = self.parameterAsLayerList(parameters, self.LINE_CONSTRAINT_LAYER_LIST, context)
        polygonLayerList = self.parameterAsLayerList(parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context)

        if water_body_layer is None or island_layer is None or island_point_layer is None or drainage_lines_layer is None:
            feedback.reportError('Layers not defined correctly.')
            return {}

        min_water_body_width_tolerance = min_waterbody_width*scale
        min_water_body_area_tolerance = min_waterbody_area*(scale)**2
        min_island_area_tolerance = min_island_area*(scale)**2
        min_drainage_ines_width_tolerance = min_drainage_lines_width

        algRunner = AlgRunner()
        layerHandler = LayerHandler()

        steps = 53
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        localWaterBodyCache = algRunner.runCreateFieldWithExpression(
            water_body_layer,
            '$id',
            'featid',
            fieldType=1,
            context=context,
        )
        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [water_body_layer],
            geomType=water_body_layer.wkbType(),
        )
        localIslandCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [island_layer],
            geomType=island_layer.wkbType(),
        )
        localBarrageCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [dam_layer],
            geomType=dam_layer.wkbType(),
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # WATERBODY

        multiStepFeedback.setProgressText(self.tr("Filtering flow types from water bodies."))
        rivers= algRunner.runFilterExpression(
            inputLyr=localWaterBodyCache,
            expression=filterRiversExpression,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        riversIdsTuple = (str(river["featid"]) for river in rivers.getFeatures())
        riversIdsStr = ','.join(riversIdsTuple)

        multiStepFeedback.setProgressText(self.tr("Separating rivers from bodywaters."))
        localRiversCache, localWaterCache = algRunner.runFilterExpressionWithFailOutput(
            inputLyr=localInputLayerCache,
            expression=f'featid in ({riversIdsStr})',
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying dissolve."))
        dissolve = algRunner.runDissolve(localRiversCache,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying negative buffer to remove thin parts."))
        buffer_neg = algRunner.runBuffer(dissolve,
            distance=-min_water_body_width_tolerance / 2.0,
            context=context,
            dissolve=True,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        singlepart = algRunner.runMultipartToSingleParts(buffer_neg,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Removing null geometries."))
        removenull = algRunner.runRemoveNull(singlepart,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying positive buffer."))
        buffer_pos = algRunner.runBuffer(removenull,
            distance=min_water_body_width_tolerance / 2.0,
            context=context,
            dissolve=True,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # single part pois resultado do buffer dissolvido é sempre multipart (pior para spatialIndex)
        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        buffer_pos_single = algRunner.runMultipartToSingleParts(buffer_pos,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying difference between original and buffer."))
        difference_original = algRunner.runDifference(inputLyr=localRiversCache,
            overlayLyr=buffer_pos_single,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        new_singlepart = algRunner.runMultipartToSingleParts(difference_original,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Removing small holes."))
        filtered_difference = algRunner.runFilterExpression(
            inputLyr=new_singlepart,
            expression=f"""area($geometry) >= {min_water_body_area_tolerance} """,
            context=context,
            feedback=multiStepFeedback,
        )        
        multiStepFeedback.setProgressText(self.tr("Applying difference between original and holes filtered."))
        waterbodystretch = algRunner.runDifference(inputLyr=localRiversCache, overlayLyr=filtered_difference, context=context, feedback=multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Merging features."))
        unified_layer = algRunner.runMergeVectorLayers(
            [waterbodystretch,localWaterCache],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        unified_single = algRunner.runMultipartToSingleParts(unified_layer,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering waterbody."))
        filtered_waterbody = algRunner.runFilterExpression(
            inputLyr=unified_single,
            expression=f"""area($geometry) >= {min_water_body_area_tolerance} """,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Finding holes on geometry."))
        _, hole = algRunner.runDonutHoleExtractor(
            inputLyr=filtered_waterbody,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Getting holes."))
        filtered_hole = algRunner.runFilterExpression(
            inputLyr=hole,
            expression=f"""area($geometry) >= {min_water_body_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Editing waterbodies."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [water_body_layer],
            filtered_waterbody,
            feedback=multiStepFeedback,
            onlySelected= False,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # ISLAND
        
        multiStepFeedback.setProgressText(self.tr("Filtering Island."))
        filtered_island = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""area($geometry) >= {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=filtered_island,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Editing islands."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [island_layer],
            filtered_island,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Transforming Small Islands into points."))
        smallIsland = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""area($geometry) < {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        toleranceIsland = 1 / (10**5) if island_layer.crs().isGeographic() else 1
        multiStepFeedback.setProgressText(self.tr("Generating island points."))
        pointIsland = algRunner.runPoleOfInaccessibility(
            inputLyr=smallIsland,
            tolerance=toleranceIsland,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        island_point_layer.startEditing()
        island_point_layer.beginEditCommand(self.tr('Updating Island Point Layer.'))
        for feat in pointIsland.getFeatures():
            newFeat = self.createNewFeature(island_point_layer.fields(), feat)
            island_point_layer.addFeature(newFeat)
        island_point_layer.endEditCommand()

        multiStepFeedback.setProgressText(self.tr("Obtaining empty spaces."))
        waterbody_empty_space = algRunner.runDifference(
            inputLyr=localInputLayerCache,
            overlayLyr=filtered_waterbody,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=waterbody_empty_space,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Extracting waterbody from island."))
        extracted_waterbody_to_island = algRunner.runExtractByLocation(
            inputLyr=waterbody_empty_space,
            intersectLyr=filtered_island,
            predicate=[0],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=extracted_waterbody_to_island,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Joining Attributes."))
        joined_waterbody_to_island = algRunner.runJoinAttributesByLocation(
            inputLyr=extracted_waterbody_to_island,
            joinLyr=filtered_island,
            predicateList=[0],
            context=context,
            method=0,
            discardNonMatching=True,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Getting waterbodies empty spaces."))
        filtered_waterbody_empty_space = algRunner.runDifference(
            inputLyr=waterbody_empty_space,
            overlayLyr=joined_waterbody_to_island,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Getting islands empty spaces."))
        island_empty_space = algRunner.runDifference(
            inputLyr=localIslandCache,
            overlayLyr=filtered_island,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Merging features."))
        empty_spaces_merged = algRunner.runMergeVectorLayers(
            inputList=[filtered_waterbody_empty_space, island_empty_space],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Empty spaces multipart to singlepart."))
        empty_spaces = algRunner.runMultipartToSingleParts(empty_spaces_merged,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # DRAINAGE LINE
        
        drainage_lines_layer.startEditing()
        drainage_lines_layer.beginEditCommand(self.tr('Drainage lines field updating for features outside water body.'))
        water_body_index = QgsSpatialIndex(water_body_layer.getFeatures())
        for drainage_feature in drainage_lines_layer.getFeatures():
            drainage_geom = drainage_feature.geometry()
            contained = False
            for water_body_id in water_body_index.intersects(drainage_geom.boundingBox()):
                water_body_feature = water_body_layer.getFeature(water_body_id)
                if water_body_feature.geometry().contains(drainage_geom):
                    contained = True
                    break
            if not contained:
                drainage_feature.setAttribute(drainage_field, drainage_field_value)
                drainage_lines_layer.updateFeature(drainage_feature)
        drainage_lines_layer.endEditCommand()
        
        multiStepFeedback.setProgressText(self.tr("Editing Drainage sections."))
        algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(inputLayer=drainage_lines_layer, context=context, min_length=min_drainage_ines_width_tolerance, bounds_layer=geographicBoundsLayer, spatial_partition=True, pointlyr_list=pointLayerList, linelyr_list=lineLayerList, polygonlyr_list=polygonLayerList, method = 0)
        localDrainageCache = algRunner.runCreateFieldWithExpression(
            drainage_lines_layer,
            '$id',
            'featid',
            fieldType=1,
            context=context
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering Drainages."))
        drainage_inside_polygon = algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" != {drainage_field_value}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: polygonizing."))
        drainage_poligonized = algRunner.runPolygonize(
            inputLyr=drainage_inside_polygon,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=drainage_poligonized,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: extracting by location."))
        drainage_poligonized_filtered = algRunner.runExtractByLocation(
            inputLyr=drainage_poligonized,
            intersectLyr=filtered_hole,
            predicate=[1],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: incrementing fields."))
        drainage_poligonized_autoincremet = algRunner.runAddAutoIncrementalField(
            inputLyr=drainage_poligonized_filtered,
            fieldName="auto",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: polygons to lines."))
        drainage_filtered_line = algRunner.runPolygonsToLines(
            inputLyr=drainage_poligonized_autoincremet,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: filtering by type of field."))
        secondary_stretches_filtered = algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" = {drainage_field_value_secundary}""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=secondary_stretches_filtered,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: joining attributes by location."))
        secondary_stretches_filtered_inside = algRunner.runJoinAttributesByLocation(
            inputLyr=secondary_stretches_filtered,
            joinLyr=drainage_filtered_line,
            predicateList=[0],
            discardNonMatching=True,
            method = 0,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: generating statistics by categories."))
        statistic = algRunner.runStatisticsByCategories(
            inputLyr=secondary_stretches_filtered_inside,
            categoriesFieldName=["auto"],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: filtering by field value."))
        extract = algRunner.runFilterExpression(
            inputLyr=statistic,
            expression=f""" "count" = 1""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: joining attributes inside the table."))
        attributesUnion = algRunner.runJoinAttributesTable(
            layerA=secondary_stretches_filtered_inside,
            fieldA="auto",
            layerB=extract,
            fieldB="auto",
            method=0,
            discardNonMatching=True,
            context=context,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering by field."))
        extract_not_null = algRunner.runFilterExpression(
            inputLyr=attributesUnion,
            expression=f""" "auto" IS NOT NULL""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs: creating spatial index."))
        algRunner.runCreateSpatialIndex(
            inputLyr=extract_not_null,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        for lineLayer in lineLayerList:
            extract_not_null_location = algRunner.runExtractByLocation(
                inputLyr=extract_not_null,
                intersectLyr=lineLayer,
                predicate=[2],
                context=context,
                feedback=multiStepFeedback
            )
            if extract_not_null_location:
                if 'combined_layer' not in locals():
                    combined_layer = extract_not_null_location
                else:
                    combined_layer = algRunner.runMergeVectorLayers(
                        inputList=[combined_layer, extract_not_null_location],
                        context=context,
                        feedback=multiStepFeedback
                    )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        idsToRemove = [feat["featid"] for feat in combined_layer.getFeatures()]
        if idsToRemove:
            drainage_lines_layer.startEditing()
            drainage_lines_layer.beginEditCommand(self.tr('Removing secondary stretches from drainage lines layer.'))
            drainage_lines_layer.deleteFeatures(idsToRemove)
            drainage_lines_layer.endEditCommand()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # DAM

        multiStepFeedback.setProgressText(self.tr("Filtering dam."))
        dam_intersect = algRunner.runExtractByLocation(
                inputLyr=localBarrageCache,
                intersectLyr=water_body_layer,
                predicate=[0],
                context=context,
                feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Updating dam layer."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [dam_layer],
            dam_intersect,
            feedback=multiStepFeedback,
            onlySelected= False
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Generating output layer."))
        polygon_fields = QgsFields()
        polygon_fields.append(QgsField("layer", QVariant.String))

        polygon_output_sink, polygon_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_POLYGON, context, polygon_fields, QgsWkbTypes.Polygon, empty_spaces.crs()
        )
        for feature in empty_spaces.getFeatures():
            new_feature = QgsFeature(polygon_fields)
            new_feature.setGeometry(feature.geometry())
            new_feature.setAttribute("layer", feature["layer"])
            polygon_output_sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        self.sink_dict = {
            empty_spaces.id(): polygon_output_sink,
        }
        lyrList = [empty_spaces]
        
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
        return "generalizewaterbodyalgorithm"

    def displayName(self):
        return self.tr("Generalize Water Body Algorithm")

    def group(self):
        return self.tr("Generalization Algorithms")

    def groupId(self):
        return "DSGTools - Generalization Algorithms"
    
    def shortHelpString(self):
        return self.tr(
            "Generaliza massas d'água, ilhas, trechos de drenagem e barragens.\nFlow types expression: Escolha os números relacionados aos rios que possuem fluxo na tabela de atributos. Exemplo: 'tipo in (1,2,9,10)'.\nScale: Escolha a escala desejada. Exemplo: '50' para 50k.\nMinimum waterbody width tolerance: Escolha o comprimento mínimo da massa d'água em graus. Exemplo: '0,000008' para 0,8mm.\nMinimum waterbody area tolerance: Escolha a área mínima da massa d'água em graus quadrados. Exemplo: '0,0000000004' para 4mm².\nMinimum island area tolerance: Escolha a área mínima da ilha em graus quadrados. Exemplo: '0,0000000004' para 4mm².\nMinimum drainage line width tolerance: Escolha o comprimento mínimo do trecho de drenagem em graus. Exemplo: '0,000008' para 0,8mm.\nSelect field from Drainage Lines to classify outside polygons: Escolha a coluna da tabela de atributos relacionada à situação da linha de drenagem dentro do polígono para alterá-la para fora do polígono.\nValue for outside polygon: Escolha ovalor númerico úmero relacionado à coluna escolhida anteriormente que se refere aos elementos fora do polígono.\nValue for secondary lines (inside polygons): Escolha o valor relacionado à coluna escolhida anteriormente que se refere aos elementos dentro dos polígonos (linhas de drenagem secundárias).\nReference layer: Escolha a camada de referência para o plugin Generalize Network Edges With Length.\nPoint constraint layers: Escolha as camadas relacionadas à restrição de pontos para o plugin Generalize Network Edges With Length.\nLine constraint layers: Escolha as camadas relacionadas à restrição de linhas para o plugin Generalize Network Edges With Length.\nPolygon constraint layers: Escolha as camadas relacionadas à restrição de polígonos para o plugin Generalize Network Edges With Length."
        )


    def tr(self, string):
        return QCoreApplication.translate("GeneralizeWaterBodyAlgorithm", string)

    def createInstance(self):
        return GeneralizeWaterBodyAlgorithm()
