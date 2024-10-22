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
    QgsFields
)
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class GeneralizeWaterBodyAlgorithm(QgsProcessingAlgorithm):
    
    WATER_BODY = "WATER_BODY"
    EXPRESSION = "EXPRESSION"
    SCALE = "SCALE"
    MIN_WATER_BODY_WIDTH = "MIN_WATER_BODY_WIDTH"
    MIN_WATER_BODY_AREA = "MIN_WATER_BODY_AREA"
    ISLAND = "ISLAND"
    ISLAND_POINT = "ISLAND_POINT"
    MIN_ISLAND_AREA = "MIN_ISLAND_AREA"
    DRAINAGE_SECTION = "DRAINAGE_SECTION"
    DRAINAGE_FIELD = "DRAINAGE_FIELD"
    DRAINAGE_FIELD_VALUE = "DRAINAGE_FIELD_VALUE"
    DRAINAGE_FIELD_VALUE_SECUNDARY = "DRAINAGE_FIELD_VALUE_SECUNDARY"
    MIN_DRAINAGE_SECTION_WIDTH = "MIN_DRAINAGE_SECTION_WIDTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    POINT_CONSTRAINT_LAYER_LIST = "POINT_CONSTRAINT_LAYER_LIST"
    LINE_CONSTRAINT_LAYER_LIST = "LINE_CONSTRAINT_LAYER_LIST"
    POLYGON_CONSTRAINT_LAYER_LIST = "POLYGON_CONSTRAINT_LAYER_LIST"
    BARRAGE = "BARRAGE"
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
            QgsProcessingParameterVectorLayer(
                self.ISLAND_POINT,
                self.tr("Island (point layer)"),
                [QgsProcessing.TypeVectorPoint],
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
                self.tr('Value to set for outside polygon'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=1
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DRAINAGE_FIELD_VALUE_SECUNDARY,
                self.tr('Value to set for secundary stretches'),
                QgsProcessingParameterNumber.Integer,
                defaultValue=3
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
            QgsProcessingParameterVectorLayer(
                self.BARRAGE,
                self.tr("Barrage (line layer)"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POLYGON,
                self.tr("Output Line"),
                type=QgsProcessing.TypeVectorPolygon
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """
        water_body_layer = self.parameterAsVectorLayer(parameters, self.WATER_BODY, context)
        expression = self.parameterAsString(parameters, self.EXPRESSION, context)
        scale = self.parameterAsDouble(parameters, self.SCALE, context)
        min_water_body_width = self.parameterAsDouble(parameters, self.MIN_WATER_BODY_WIDTH, context)
        island_layer = self.parameterAsVectorLayer(parameters, self.ISLAND, context)
        island_point_layer = self.parameterAsVectorLayer(parameters, self.ISLAND_POINT, context)
        min_water_body_area = self.parameterAsDouble(parameters, self.MIN_WATER_BODY_AREA, context)
        min_island_area = self.parameterAsDouble(parameters, self.MIN_ISLAND_AREA, context)
        drainage_section_layer = self.parameterAsVectorLayer(parameters, self.DRAINAGE_SECTION, context)
        drainage_field = self.parameterAsString(parameters, self.DRAINAGE_FIELD, context)
        drainage_field_value = self.parameterAsString(parameters, self.DRAINAGE_FIELD_VALUE, context)
        drainage_field_value_secundary = self.parameterAsString(parameters, self.DRAINAGE_FIELD_VALUE_SECUNDARY, context)
        min_drainage_section_width = self.parameterAsDouble(parameters, self.MIN_DRAINAGE_SECTION_WIDTH, context)
        geographicBoundsLayer = self.parameterAsLayer(parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context)
        barrage_layer = self.parameterAsVectorLayer(parameters, self.BARRAGE, context)
        pointLayerList = self.parameterAsLayerList(parameters, self.POINT_CONSTRAINT_LAYER_LIST, context)
        lineLayerList = self.parameterAsLayerList(parameters, self.LINE_CONSTRAINT_LAYER_LIST, context)
        polygonLayerList = self.parameterAsLayerList(parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context)

        if water_body_layer is None or island_layer is None or island_point_layer is None or drainage_section_layer is None:
            feedback.reportError('Layers not defined correctly.')
            return {}

        if water_body_layer.crs().isGeographic():
            min_water_body_width_tolerance = (min_water_body_width * scale) / (10**5)
        else:
            min_water_body_width_tolerance = (min_water_body_width * scale)

        min_water_body_area_tolerance = (min_water_body_area * (scale ** 2))
        min_island_area_tolerance = (min_island_area * (scale ** 2)) * 10 #Remover *10 depois

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

        steps = 45
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        localWaterBodyCache = algRunner.runCreateFieldWithExpression(
            water_body_layer,
            '@id',
            'featid',
            fieldType=1,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [water_body_layer],
            geomType=water_body_layer.wkbType(),
            onlySelected= False,
            feedback=multiStepFeedback
        )
        localIslandCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [island_layer],
            geomType=island_layer.wkbType(),
            onlySelected= False,
            feedback=multiStepFeedback
        )
        localBarrageCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [barrage_layer],
            geomType=barrage_layer.wkbType(),
            onlySelected= False,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering flow types from water bodies..."))
        rivers= algRunner.runFilterExpression(
            inputLyr=localWaterBodyCache,
            expression=expression,
            context=context,
            feedback=multiStepFeedback,
            outputLyr="memory:",
        ) 
        riversIdsTuple = (str(river["featid"]) for river in rivers.getFeatures())
        riversIdsStr = ','.join(riversIdsTuple)
        filterRiversIdsExpression = f'featid in ({riversIdsStr})'

        localRiversCache, localWaterCache = algRunner.runFilterExpressionWithFailOutput(
            inputLyr=localInputLayerCache,
            expression=filterRiversIdsExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying dissolve..."))
        dissolve = algRunner.runDissolve(localRiversCache, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Dissolve successfully applied."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying negative buffer to remove thin parts..."))
        buffer_neg = algRunner.runBuffer(dissolve, distance=-min_water_body_width_tolerance / 2.0, context=context, dissolve=True, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Negative buffer generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart..."))
        singlepart = algRunner.runMultipartToSingleParts(buffer_neg, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Singlepart generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Removing null geometries manually..."))
        removenull = algRunner.runRemoveNull(singlepart, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Null geometries removed successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying positive buffer to restore to initial state..."))
        buffer_pos = algRunner.runBuffer(removenull, distance=min_water_body_width_tolerance / 2.0, context=context, dissolve=True, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Positive buffer generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # single part pois resultado do buffer dissolvido é sempre multipart (pior para spatialIndex)
        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart..."))
        buffer_pos_single = algRunner.runMultipartToSingleParts(buffer_pos, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Singlepart generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying difference between original and buffer."))
        difference_original = algRunner.runDifference(inputLyr=localRiversCache, overlayLyr=buffer_pos_single, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Difference generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering features."))
        filtered_difference = algRunner.runFilterExpression(
            inputLyr=difference_original,
            expression=f"""$area >= {min_water_body_area*15625}""",
            context=context,
            feedback=multiStepFeedback,
        )
        filtered_bodywater = algRunner.runFilterExpression(
            inputLyr=localWaterCache,
            expression=f"""$area >= {min_water_body_area*15625}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Features filtered by area successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Applying difference between original and holes filtered."))
        waterbodystretch = algRunner.runDifference(inputLyr=localRiversCache, overlayLyr=filtered_difference, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Difference generated successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering features."))
        filtered_waterbodystretch = algRunner.runFilterExpression(
            inputLyr=waterbodystretch,
            expression=f"""$area >= {min_water_body_area*15625}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Features filtered by area successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Merging features."))
        unified_layer = algRunner.runMergeVectorLayers(
            [filtered_waterbodystretch,filtered_bodywater],
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Features successfully merged."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Finding holes on geometry."))
        _, hole = algRunner.runDonutHoleExtractor(
            inputLyr=unified_layer,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Holes successfully saved."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering holes."))
        filtered_hole = algRunner.runFilterExpression(
            inputLyr=hole,
            expression=f"""$area < {min_water_body_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Holes filtered."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Editing water bodies."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [water_body_layer],
            unified_layer,
            feedback=multiStepFeedback,
            onlySelected= False,
        )
        multiStepFeedback.setProgressText(self.tr("Water bodies edition finished."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering Island."))
        filtered_island = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""$area >= {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Island filtered successfully."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Editing islands."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [island_layer],
            filtered_island,
            feedback=multiStepFeedback,
            onlySelected= False,
        )
        multiStepFeedback.setProgressText(self.tr("Islands edition finished."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Transforming Small Islands into points."))
        smallIsland = algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""$area < {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Points successfully generated."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        pointIsland = algRunner.runPoleOfInaccessibility(
            inputLyr=smallIsland,
            tolerance=toleranceIsland,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        island_point_layer.startEditing()
        island_point_layer.beginEditCommand(self.tr('Updating Islant Point Layer.'))
        for feat in pointIsland.getFeatures():
            newFeat = self.createNewFeature(island_point_layer.fields(), feat)
            island_point_layer.addFeature(newFeat)
        island_point_layer.endEditCommand()
        multiStepFeedback.setProgressText(self.tr("Transformation done."))

        multiStepFeedback.setProgressText(self.tr("Obtaining empty spaces."))
        waterbody_empty_space = algRunner.runDifference(inputLyr=localInputLayerCache, overlayLyr=unified_layer, context=context,feedback=multiStepFeedback)
        island_empty_space = algRunner.runDifference(inputLyr=localIslandCache, overlayLyr=filtered_island, context=context,feedback=multiStepFeedback)
        empty_spaces_merged = algRunner.runMergeVectorLayers(inputList=[waterbody_empty_space, island_empty_space], context=context, feedback=multiStepFeedback)
        multiStepFeedback.setProgressText(self.tr("Empty spaces successfully obtained."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
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
        multiStepFeedback.setProgressText(self.tr("Drainage section field updated for features outside water body."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Editing Drainage sections."))
        algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(inputLayer=drainage_section_layer, context=context, min_length=min_drainage_section_width_tolerance, bounds_layer=geographicBoundsLayer, spatial_partition=True, pointlyr_list=pointLayerList, linelyr_list=lineLayerList, polygonlyr_list=polygonLayerList, method = 0)
        localDrainageCache = algRunner.runCreateFieldWithExpression(
            drainage_section_layer,
            '@id',
            'featid',
            fieldType=1,
            context=context
        )
        multiStepFeedback.setProgressText(self.tr("Drainage sections edition finished."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Filtering Drainages."))
        drainage_inside_polygon = algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" != {drainage_field_value}""",
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setProgressText(self.tr("Filtering done."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Eliminating secundary stretchs."))
        drainage_poligonized = algRunner.runPolygonize(
            inputLyr=drainage_inside_polygon,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        algRunner.runCreateSpatialIndex(
            inputLyr=drainage_poligonized,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        drainage_poligonized_filtered = algRunner.runExtractByLocation(
            inputLyr=drainage_poligonized,
            intersectLyr=filtered_hole,
            predicate=[1],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        drainage_poligonized_autoincremet = algRunner.runAddAutoIncrementalField(
            inputLyr=drainage_poligonized_filtered,
            fieldName="auto",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        drainage_filtered_line = algRunner.runPolygonsToLines(
            inputLyr=drainage_poligonized_autoincremet,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        secondary_stretches_filtered = algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" = {drainage_field_value_secundary}""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        algRunner.runCreateSpatialIndex(
            inputLyr=secondary_stretches_filtered,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
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
        
        statistic = algRunner.runStatisticsByCategories(
            inputLyr=secondary_stretches_filtered_inside,
            categoriesFieldName=["auto"],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        extract = algRunner.runFilterExpression(
            inputLyr=statistic,
            expression=f""" "count" = 1""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        attributesUnion = algRunner.runJoinAttributesTable(
            layerA=secondary_stretches_filtered_inside,
            fieldA="auto",
            layerB=extract,
            fieldB="auto",
            method=0,
            discardNonMatching=True,
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setProgressText(self.tr("Secundary streths successfully eliminated."))
        #auto nao null -> extractbyexpression -> saida 1 = auto nao null, saida 2 =auto null
        # saida 1 -> metodo de check de exclusao -> extractbylocation disjoints com elemen_viario -> saida 3 (excluir por nao tocar)
        # for na saida 3 para pegar ids (feat id??) e jogar no deleteFeatures
        # saida 1 - saida 3 -> saida 4 (flag de secundario nao excluido por metodo de check de exlusao "secundario nao excluido por intersectar elemento viario")
        # saida 2 -> flag por mais de um secundario formando ilha excluída
        #idstodelete = []
        # drainage_section_layer.deleteFeatures(idstodelete)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        extract_not_null = algRunner.runFilterExpression(
            inputLyr=attributesUnion,
            expression=f""" "auto" IS NOT NULL""",
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
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
            drainage_section_layer.startEditing()
            drainage_section_layer.beginEditCommand(self.tr('Removing secondary stretches from drainage section layer.'))
            drainage_section_layer.deleteFeatures(idsToRemove)
            drainage_section_layer.endEditCommand()
        multiStepFeedback.setProgressText(self.tr("Secondary stretches removed from drainage section layer, excluding those intersecting with line constraints."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering barrage."))
        barrage_intersect = algRunner.runExtractByLocation(
                inputLyr=localBarrageCache,
                intersectLyr=water_body_layer,
                predicate=[0],
                context=context,
                feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [barrage_layer],
            barrage_intersect,
            feedback=multiStepFeedback,
            onlySelected= False
        )
        multiStepFeedback.setProgressText(self.tr("All Barrages filtered."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Generating output layer."))
        polygon_fields = empty_spaces_merged.fields()
        polygon_output_sink, polygon_output_id = self.parameterAsSink(
            parameters, self.OUTPUT_POLYGON, context, polygon_fields, QgsWkbTypes.Polygon, empty_spaces_merged.crs()
        )
        self.sink_dict = {
            empty_spaces_merged.id(): polygon_output_sink,
        }
        lyrList = [empty_spaces_merged]
        
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

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeWaterBodyAlgorithm", string)

    def createInstance(self):
        return GeneralizeWaterBodyAlgorithm()
