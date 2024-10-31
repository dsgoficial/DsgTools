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
    QgsProcessingParameterNumber,
    QgsFields,
    QgsProcessingParameterDistance,
    QgsProcessingParameterString,
)
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeUtils import (
    GeneralizeUtils,
)


class GeneralizeWaterBodyAlgorithm(QgsProcessingAlgorithm):

    WATERBODY = "WATERBODY"
    EXPRESSION = "EXPRESSION"
    SCALE = "SCALE"
    MIN_WATERBODY_WIDTH = "MIN_WATERBODY_WIDTH"
    MIN_WATERBODY_AREA = "MIN_WATERBODY_AREA"
    MAX_WATERBODY_HOLE_AREA = "MAX_WATERBODY_HOLE_AREA"
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
    OUTPUT_WATERBODY = "OUTPUT_WATERBODY"
    OUTPUT_DRAINAGE_LINE = "OUTPUT_DRAINAGE_LINE"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATERBODY,
                self.tr("Water body (polygon layer)"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION,
                self.tr("Flow types expression"),
                parentLayerParameterName=self.WATERBODY,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE,
                self.tr("Scale"),
                type=QgsProcessingParameterNumber.Integer,
                minValue=0,
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_WATERBODY_WIDTH,
            self.tr("Minimum waterbody width tolerance"),
            parentParameterName=self.WATERBODY,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 12}})
        self.addParameter(param)
        param = QgsProcessingParameterDistance(
            self.MIN_WATERBODY_AREA,
            self.tr("Minimum waterbody area tolerance"),
            parentParameterName=self.WATERBODY,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)
        param = QgsProcessingParameterDistance(
            self.MAX_WATERBODY_HOLE_AREA,
            self.tr("Maximum waterbody hole area to remove tolerance"),
            parentParameterName=self.WATERBODY,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)
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
            self.MIN_ISLAND_AREA,
            self.tr("Minimum island area tolerance"),
            parentParameterName=self.ISLAND,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.DRAINAGE_LINES,
                self.tr("Drainage lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        param = QgsProcessingParameterDistance(
            self.MIN_DRAINAGE_LINES_WIDTH,
            self.tr("Minimum drainage line width tolerance"),
            parentParameterName=self.DRAINAGE_LINES,
            minValue=0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 20}})
        self.addParameter(param)
        self.addParameter(
            QgsProcessingParameterField(
                self.DRAINAGE_FIELD,
                self.tr(
                    "Select field from Drainage Lines to classify outside polygons"
                ),
                parentLayerParameterName=self.DRAINAGE_LINES,
                type=QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DRAINAGE_FIELD_VALUE,
                self.tr("Value for outside polygon"),
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DRAINAGE_FIELD_VALUE_SECUNDARY,
                self.tr("Value for secundary drainage lines (inside polygons)"),
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
                self.OUTPUT_WATERBODY,
                self.tr("Output Removed Waterbody"),
                type=QgsProcessing.TypeVectorPolygon,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_DRAINAGE_LINE,
                self.tr("Output Removed Draiage Line"),
                type=QgsProcessing.TypeVectorLine,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Processing logic.
        """

        waterbody_layer = self.parameterAsVectorLayer(
            parameters, self.WATERBODY, context
        )
        filterRiversExpression = self.parameterAsExpression(
            parameters, self.EXPRESSION, context
        )
        scale = self.parameterAsInt(parameters, self.SCALE, context)
        min_waterbody_width = self.parameterAsDouble(
            parameters, self.MIN_WATERBODY_WIDTH, context
        )
        min_waterbody_area = self.parameterAsDouble(
            parameters, self.MIN_WATERBODY_AREA, context
        )
        max_waterbody_hole_area = self.parameterAsDouble(
            parameters, self.MAX_WATERBODY_HOLE_AREA, context
        )
        island_layer = self.parameterAsVectorLayer(parameters, self.ISLAND, context)
        island_point_layer = self.parameterAsVectorLayer(
            parameters, self.ISLAND_POINT, context
        )
        min_island_area = self.parameterAsDouble(
            parameters, self.MIN_ISLAND_AREA, context
        )
        min_drainage_lines_width = self.parameterAsDouble(
            parameters, self.MIN_DRAINAGE_LINES_WIDTH, context
        )
        drainage_lines_layer = self.parameterAsVectorLayer(
            parameters, self.DRAINAGE_LINES, context
        )
        drainage_field = self.parameterAsString(
            parameters, self.DRAINAGE_FIELD, context
        )
        drainage_field_value = self.parameterAsString(
            parameters, self.DRAINAGE_FIELD_VALUE, context
        )
        drainage_field_value_secundary = self.parameterAsString(
            parameters, self.DRAINAGE_FIELD_VALUE_SECUNDARY, context
        )
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        dam_layer = self.parameterAsVectorLayer(parameters, self.DAM, context)
        pointLayerList = self.parameterAsLayerList(
            parameters, self.POINT_CONSTRAINT_LAYER_LIST, context
        )
        lineLayerList = self.parameterAsLayerList(
            parameters, self.LINE_CONSTRAINT_LAYER_LIST, context
        )
        polygonLayerList = self.parameterAsLayerList(
            parameters, self.POLYGON_CONSTRAINT_LAYER_LIST, context
        )

        if (
            waterbody_layer is None
            or island_layer is None
            or island_point_layer is None
            or drainage_lines_layer is None
        ):
            feedback.reportError("Layers not defined correctly.")
            return {}

        min_waterbody_width_tolerance = min_waterbody_width * scale
        min_waterbody_area_tolerance = min_waterbody_area * (scale) ** 2
        max_waterbody_hole_area_tolerance = max_waterbody_hole_area * (scale) ** 2
        min_island_area_tolerance = min_island_area * (scale) ** 2
        min_drainage_ines_width_tolerance = min_drainage_lines_width

        self.algRunner = AlgRunner()
        layerHandler = LayerHandler()
        generalizeUtils = GeneralizeUtils()

        steps = 50
        multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        localWaterBodyCache = self.algRunner.runCreateFieldWithExpression(
            waterbody_layer,
            "$id",
            "featid",
            fieldType=1,
            context=context,
        )
        localInputLayerCache = layerHandler.createAndPopulateUnifiedVectorLayer(
            [waterbody_layer],
            geomType=waterbody_layer.wkbType(),
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

        multiStepFeedback.setProgressText(
            self.tr("Filtering flow types from water bodies.")
        )
        rivers = self.algRunner.runFilterExpression(
            inputLyr=localWaterBodyCache,
            expression=filterRiversExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        riversIdsTuple = (str(river["featid"]) for river in rivers.getFeatures())
        riversIdsStr = ",".join(riversIdsTuple)

        multiStepFeedback.setProgressText(self.tr("Separating rivers from bodywaters."))
        (
            localRiversCache,
            localWaterCache,
        ) = self.algRunner.runFilterExpressionWithFailOutput(
            inputLyr=localInputLayerCache,
            expression=f"featid in ({riversIdsStr})",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying strangle."))
        waterbodystretch = generalizeUtils.runStrangle(
            layer=localRiversCache,
            length_tol=min_waterbody_width_tolerance,
            area_tol=min_waterbody_area_tolerance,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Merging features."))
        unified_layer = self.algRunner.runMergeVectorLayers(
            [waterbodystretch, localWaterCache],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Transforming multipart geometries into singlepart.")
        )
        unified_single = self.algRunner.runMultipartToSingleParts(
            unified_layer, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Finding holes on geometry."))
        removed_hole = self.algRunner.runSmallHoleRemoverAlgorithm(
            inputLayer=unified_single,
            max_hole_area=max_waterbody_hole_area_tolerance,
            context=context,
            feedback=multiStepFeedback,
        ) 
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)


        multiStepFeedback.setProgressText(self.tr("Filtering waterbody."))
        filtered_waterbody = self.algRunner.runFilterExpression(
            inputLyr=removed_hole,
            expression=f"""area($geometry) >= {min_waterbody_area_tolerance} """,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Editing waterbodies."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [waterbody_layer],
            filtered_waterbody,
            feedback=multiStepFeedback,
            onlySelected=False,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Obtaining empty spaces."))
        waterbody_empty_space = self.algRunner.runDifference(
            inputLyr=localInputLayerCache,
            overlayLyr=filtered_waterbody,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Empty spaces multipart to singlepart.")
        )
        empty_spaces = self.algRunner.runMultipartToSingleParts(
            waterbody_empty_space, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # ISLAND

        multiStepFeedback.setProgressText(self.tr("Filtering Island."))
        filtered_island = self.algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""area($geometry) >= {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Creating spatial index."))
        self.algRunner.runCreateSpatialIndex(
            inputLyr=filtered_island, context=context, feedback=multiStepFeedback
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

        multiStepFeedback.setProgressText(
            self.tr("Transforming Small Islands into points.")
        )
        smallIsland = self.algRunner.runFilterExpression(
            inputLyr=localIslandCache,
            expression=f"""area($geometry) < {min_island_area_tolerance}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        toleranceIsland = 1 / (10**5) if island_layer.crs().isGeographic() else 1
        multiStepFeedback.setProgressText(self.tr("Generating island points."))
        pointIsland = self.algRunner.runPoleOfInaccessibility(
            inputLyr=smallIsland,
            tolerance=toleranceIsland,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Updating Island Point Layer."))

        island_point_layer.startEditing()
        island_point_layer.beginEditCommand(self.tr("Updating."))
        for feat in pointIsland.getFeatures():
            newFeat = self.createNewFeature(island_point_layer.fields(), feat)
            island_point_layer.addFeature(newFeat)
        island_point_layer.endEditCommand()

        # DRAINAGE LINE

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Drainage lines field updating for features outside water body.")
        )
        drainage_lines_layer.startEditing()
        drainage_lines_layer.beginEditCommand(
            self.tr("updating.")
        )
        idsOutsideWaterbody = self.getDrainageOutsideWaterbody(
            waterbody_layer, drainage_lines_layer, context, feedback=multiStepFeedback
        )
        drainage_field_index = drainage_lines_layer.fields().indexFromName(
            drainage_field
        )
        for id in idsOutsideWaterbody:
            drainage_lines_layer.changeAttributeValue(
                id, drainage_field_index, drainage_field_value
            )
        drainage_lines_layer.endEditCommand()

        multiStepFeedback.setProgressText(self.tr("Editing Drainage sections."))
        self.algRunner.runGeneralizeNetworkEdgesFromLengthAlgorithm(
            inputLayer=drainage_lines_layer,
            context=context,
            min_length=min_drainage_ines_width_tolerance,
            bounds_layer=geographicBoundsLayer,
            spatial_partition=True,
            pointlyr_list=pointLayerList,
            linelyr_list=lineLayerList,
            polygonlyr_list=polygonLayerList,
            method=0,
        )
        localDrainageCache = self.algRunner.runCreateFieldWithExpression(
            drainage_lines_layer, "$id", "featid", fieldType=1, context=context
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Filtering Drainages."))
        drainage_inside_polygon = self.algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" != {drainage_field_value}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: polygonizing.")
        )
        drainage_poligonized = self.algRunner.runPolygonize(
            inputLyr=drainage_inside_polygon,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: creating spatial index.")
        )
        self.algRunner.runCreateSpatialIndex(
            inputLyr=drainage_poligonized, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: extracting by location.")
        )
        drainage_poligonized_filtered = self.algRunner.runExtractByLocation(
            inputLyr=drainage_poligonized,
            intersectLyr=empty_spaces,
            predicate=[1],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: incrementing fields.")
        )
        drainage_poligonized_autoincremet = self.algRunner.runAddAutoIncrementalField(
            inputLyr=drainage_poligonized_filtered,
            fieldName="auto",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: polygons to lines.")
        )
        drainage_filtered_line = self.algRunner.runPolygonsToLines(
            inputLyr=drainage_poligonized_autoincremet,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: filtering by type of field.")
        )
        secondary_stretches_filtered = self.algRunner.runFilterExpression(
            inputLyr=localDrainageCache,
            expression=f""" "{drainage_field}" = {drainage_field_value_secundary}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: creating spatial index.")
        )
        self.algRunner.runCreateSpatialIndex(
            inputLyr=secondary_stretches_filtered,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: joining attributes by location.")
        )
        secondary_stretches_filtered_inside = (
            self.algRunner.runJoinAttributesByLocation(
                inputLyr=secondary_stretches_filtered,
                joinLyr=drainage_filtered_line,
                predicateList=[0],
                discardNonMatching=True,
                method=0,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr(
                "Eliminating secundary stretchs: generating statistics by categories."
            )
        )
        statistic = self.algRunner.runStatisticsByCategories(
            inputLyr=secondary_stretches_filtered_inside,
            categoriesFieldName=["auto"],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: filtering by field value.")
        )
        extract = self.algRunner.runFilterExpression(
            inputLyr=statistic,
            expression=f""" "count" = 1""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr(
                "Eliminating secundary stretchs: joining attributes inside the table."
            )
        )
        attributesUnion = self.algRunner.runJoinAttributesTable(
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
        extract_not_null = self.algRunner.runFilterExpression(
            inputLyr=attributesUnion,
            expression=f""" "auto" IS NOT NULL""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(
            self.tr("Eliminating secundary stretchs: creating spatial index.")
        )
        self.algRunner.runCreateSpatialIndex(
            inputLyr=extract_not_null, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        layersToCombine = []
        # trechos de drenagem secundários nao serão removidos se intersectar linhas para manter fluxo
        for lineLayer in lineLayerList:
            extract_not_null_location = self.algRunner.runExtractByLocation(
                inputLyr=extract_not_null,
                intersectLyr=lineLayer,
                predicate=[2],
                context=context,
                feedback=multiStepFeedback,
            )
            layersToCombine.append(extract_not_null_location)
        combined_layer = self.algRunner.runMergeVectorLayers(
            inputList=layersToCombine, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        idsToRemove = [feat["featid"] for feat in combined_layer.getFeatures()]
        if idsToRemove:
            drainage_lines_layer.startEditing()
            drainage_lines_layer.beginEditCommand(
                self.tr("Removing secondary stretches from drainage lines layer.")
            )
            drainage_lines_layer.deleteFeatures(idsToRemove)
            drainage_lines_layer.endEditCommand()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        # DAM

        multiStepFeedback.setProgressText(self.tr("Filtering dam."))
        dam_intersect = self.algRunner.runExtractByLocation(
            inputLyr=localBarrageCache,
            intersectLyr=waterbody_layer,
            predicate=[0],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Updating dam layer."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            [dam_layer], dam_intersect, feedback=multiStepFeedback, onlySelected=False
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Generating output layer."))
        waterbody_fields = QgsFields()
        drainage_line_fields = QgsFields()
        waterbody_fields.append(QgsField("layer", QVariant.String))

        waterbody_output_sink, waterbody_output_id = self.parameterAsSink(
            parameters,
            self.OUTPUT_WATERBODY,
            context,
            waterbody_fields,
            QgsWkbTypes.Polygon,
            empty_spaces.crs(),
        )
        drainage_line_output_sink, drainage_line_output_id = self.parameterAsSink(
            parameters,
            self.OUTPUT_DRAINAGE_LINE,
            context,
            drainage_line_fields,
            QgsWkbTypes.LineString,
            combined_layer.crs(),
        )
        for feature in empty_spaces.getFeatures():
            new_feature = QgsFeature(waterbody_fields)
            new_feature.setGeometry(feature.geometry())
            new_feature.setAttribute("layer", feature["layer"])
            waterbody_output_sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        for feature in combined_layer.getFeatures():
            new_feature = QgsFeature(drainage_line_fields)
            new_feature.setGeometry(feature.geometry())
            drainage_line_output_sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        self.sink_dict = {
            empty_spaces.id(): waterbody_output_sink,
            combined_layer.id(): drainage_line_output_sink,
        }
        lyrList = [empty_spaces, combined_layer]

        multiStepFeedback.setProgressText(self.tr("Adding to sink."))
        for lyr in lyrList:
            self.iterateAndAddToSink(lyr, feedback)
        multiStepFeedback.setProgressText(self.tr("Returning output layer."))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        return {self.OUTPUT_WATERBODY: waterbody_output_id, self.OUTPUT_DRAINAGE_LINE: drainage_line_output_id}

    def getDrainageOutsideWaterbody(
        self, waterbody_layer, drainage_lines_layer, context, feedback=None
    ):
        auxFieldName = "newfeatid"
        cacheLayer = self.algRunner.runCreateFieldWithExpression(
            inputLyr=drainage_lines_layer,
            expression="$id",
            fieldName=auxFieldName,
            fieldType=1,
            context=context,
            feedback=feedback,
        )
        ids = {feat[auxFieldName] for feat in cacheLayer.getFeatures()}
        drainagesInsideWaterbody = self.algRunner.runExtractByLocation(
            inputLyr=cacheLayer,
            intersectLyr=waterbody_layer,
            predicate=[6],
            context=context,
            feedback=feedback,
        )
        idsInsideWaterbody = {
            feat[auxFieldName] for feat in drainagesInsideWaterbody.getFeatures()
        }
        idsOutsideWaterbody = ids - idsInsideWaterbody
        return idsOutsideWaterbody

    def iterateAndAddToSink(self, lyr, feedback=None):
        sink = self.sink_dict.get(lyr.id(), None)
        if sink is None:
            return
        nFeatures = lyr.featureCount()
        if nFeatures == 0:
            return
        stepSize = 100 / nFeatures
        for current, feat in enumerate(lyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                return
            newFeat = self.createNewFeature(lyr.fields(), feat)
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            if feedback is not None:
                feedback.setProgress(current * stepSize)

    def createNewFeature(self, fields: QgsFields, feat: QgsFeature) -> QgsFeature:
        fieldsFeat = [f.name() for f in feat.fields()]
        newFeat = QgsFeature(fields)
        newFeat.setGeometry(feat.geometry())
        for field in fields:
            fieldName = field.name()
            if fieldName not in fieldsFeat:
                continue
            newFeat[fieldName] = feat[fieldName]
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
            """Generaliza massas d'água, ilhas, trechos de drenagem e barragens.\n
            Flow types expression: Escolha os números relacionados aos rios que possuem fluxo na tabela de atributos. Exemplo: 'tipo in (1,2,9,10)'.\n
            Scale: Escolha a escala desejada. Exemplo: '50000' para 50k.\n
            Minimum waterbody width tolerance: Escolha o comprimento mínimo da massa d'água em graus na carta. Exemplo: '8e-9' para 0,8mm (considerando 1 grau = 10^5m).\n
            Minimum waterbody area tolerance: Escolha a área mínima da massa d'água em graus quadrados na carta. Exemplo: '2.5e-15' para 25mm² (considerando 1 grau = 10^5m).\n
            Maximum inunda home area tolerance: Escolha a área máxima dos buracos a serem removidos em graus quadrados. Exemplo: '4e-16' para 4mm² (considerando 1 grau = 10^5m).\n
            Minimum island area tolerance: Escolha a área mínima da ilha em graus quadrados na carta. Exemplo: '2.5e-15' para 25mm² (considerando 1 grau = 10^5m).\n
            Minimum drainage line size tolerance: Escolha o comprimento mínimo do trecho de drenagem em graus. Exemplo: '8e-9' para 0,8mm. (considerando 1 grau = 10^5m)\n
            Select field from Drainage Lines to classify outside polygons: Escolha a coluna da tabela de atributos relacionada à situação da linha de drenagem dentro do polígono para alterá-la para fora do polígono.\n
            Value for outside polygon: Escolha o valor numérico relacionado à coluna escolhida anteriormente que se refere aos elementos fora do polígono.\n
            Value for secondary lines (inside polygons): Escolha o valor relacionado à coluna escolhida anteriormente que se refere aos elementos dentro dos polígonos (linhas de drenagem secundárias).\n
            Line constraint layers é parâmetro para o Generalize Network Edges With Length e trechos secundários não são removidos caso intersectem essas linhas.
            Point constraint layers, Polygon constraint layers, Reference layer, mesmos parâmetros para o Generalize Network Edges With Length.\n"""
        )

    def tr(self, string):
        return QCoreApplication.translate("GeneralizeWaterBodyAlgorithm", string)

    def createInstance(self):
        return GeneralizeWaterBodyAlgorithm()
