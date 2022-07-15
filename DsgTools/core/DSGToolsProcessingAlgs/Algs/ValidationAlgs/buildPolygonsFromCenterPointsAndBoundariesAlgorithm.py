# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
import processing
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingUtils,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class BuildPolygonsFromCenterPointsAndBoundariesAlgorithm(ValidationAlgorithm):
    INPUT_CENTER_POINTS = "INPUT_CENTER_POINTS"
    SELECTED = "SELECTED"
    ATTRIBUTE_BLACK_LIST = "ATTRIBUTE_BLACK_LIST"
    BOUNDARY_LINE_LAYER = "BOUNDARY_LINE_LAYER"
    CONSTRAINT_LINE_LAYERS = "CONSTRAINT_LINE_LAYERS"
    CONSTRAINT_POLYGON_LAYERS = "CONSTRAINT_POLYGON_LAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    SUPPRESS_AREA_WITHOUT_CENTROID_FLAG = "SUPPRESS_AREA_WITHOUT_CENTROID_FLAG"
    CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS = (
        "CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS"
    )
    MERGE_OUTPUT_POLYGONS = "MERGE_OUTPUT_POLYGONS"
    OUTPUT_POLYGONS = "OUTPUT_POLYGONS"
    INVALID_POLYGON_LOCATION = "INVALID_POLYGON_LOCATION"
    UNUSED_BOUNDARY_LINES = "UNUSED_BOUNDARY_LINES"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_CENTER_POINTS,
                self.tr("Center Point Layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST,
                self.tr("Fields to ignore"),
                None,
                "INPUT_CENTER_POINTS",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.BOUNDARY_LINE_LAYER,
                self.tr("Line Boundary"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_LINE_LAYERS,
                self.tr("Line Constraint Layers"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_POLYGON_LAYERS,
                self.tr("Polygon Constraint Layers"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.MERGE_OUTPUT_POLYGONS,
                self.tr("Merge output polygons with same attribute set"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS,
                self.tr("Check output polygons for invalid geometries"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SUPPRESS_AREA_WITHOUT_CENTROID_FLAG,
                self.tr("Suppress area without center point flag"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POLYGONS, self.tr("Output Polygons")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.INVALID_POLYGON_LOCATION,
                self.tr("Invalid Polygon Location Flags from {0}").format(
                    self.displayName()
                ),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.UNUSED_BOUNDARY_LINES,
                self.tr("Unused Boundary Flags from {0}").format(self.displayName()),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("Polygon Flags from {0}").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputCenterPointLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_CENTER_POINTS, context
        )
        if inputCenterPointLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT_CENTER_POINTS)
            )
        boundaryLineLyr = self.parameterAsVectorLayer(
            parameters, self.BOUNDARY_LINE_LAYER, context
        )
        constraintLineLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_LINE_LAYERS, context
        )
        if boundaryLineLyr is None and constraintLineLyrList == []:
            raise QgsProcessingException(
                self.tr('There must be at least one boundary layer or one constraint line list.')
            )
        constraintPolygonLyrList = self.parameterAsLayerList(
            parameters, self.CONSTRAINT_POLYGON_LAYERS, context
        )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        attributeBlackList = self.parameterAsFields(
            parameters, self.ATTRIBUTE_BLACK_LIST, context
        )
        fields = layerHandler.getFieldsFromAttributeBlackList(
            inputCenterPointLyr, attributeBlackList
        )
        (output_polygon_sink, output_polygon_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_POLYGONS,
            context,
            fields,
            QgsWkbTypes.Polygon,
            inputCenterPointLyr.sourceCrs(),
        )
        suppressPolygonWithoutCenterPointFlag = self.parameterAsBool(
            parameters, self.SUPPRESS_AREA_WITHOUT_CENTROID_FLAG, context
        )
        checkInvalidOnOutput = self.parameterAsBool(
            parameters, self.CHECK_INVALID_GEOMETRIES_ON_OUTPUT_POLYGONS, context
        )
        mergeOutput = self.parameterAsBool(
            parameters, self.MERGE_OUTPUT_POLYGONS, context
        )

        self.prepareFlagSink(
            parameters, inputCenterPointLyr, QgsWkbTypes.Polygon, context
        )
        (
            unused_boundary_flag_sink,
            unused_boundary_flag_sink_id,
        ) = self.parameterAsSink(
            parameters,
            self.UNUSED_BOUNDARY_LINES,
            context,
            boundaryLineLyr.fields() if boundaryLineLyr is not None else QgsFields(),
            QgsWkbTypes.LineString,
            boundaryLineLyr.sourceCrs() if boundaryLineLyr is not None else inputCenterPointLyr.sourceCrs(),
        )
        nSteps = (
            3 + (mergeOutput + 1) + checkInvalidOnOutput
        )  # boolean sum, if true, sums 1 to each term
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        polygonFeatList, flagDict = self.computePolygonsFromCenterPointAndBoundaries(
            context,
            layerHandler,
            algRunner,
            inputCenterPointLyr,
            boundaryLineLyr,
            constraintLineLyrList,
            constraintPolygonLyrList,
            onlySelected,
            geographicBoundaryLyr,
            attributeBlackList,
            suppressPolygonWithoutCenterPointFlag,
            multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        invalid_polygon_sink, invalid_polygon_sink_id = self.prepareInvalidPolygonFlags(
            parameters, context, inputCenterPointLyr
        )
        currentStep += 1
        sink, sink_id = QgsProcessingUtils.createFeatureSink(
            'memory:', context, fields, QgsWkbTypes.Polygon, inputCenterPointLyr.sourceCrs())
        sink.addFeatures(polygonFeatList, QgsFeatureSink.FastInsert)

        if mergeOutput:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Dissolving output..."))
            dissolvedLyr = algRunner.runDissolve(
                sink_id, context, feedback=multiStepFeedback, field=[field.name() for field in fields]
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            dissolvedLyr = algRunner.runMultipartToSingleParts(
                dissolvedLyr, context=context, feedback=multiStepFeedback
            )
            polygonFeatList = [feat for feat in dissolvedLyr.getFeatures()]
            currentStep += 1
        self.writeOutputPolygons(
            output_polygon_sink, multiStepFeedback, polygonFeatList, flagDict
        )
        currentStep += 1
        if checkInvalidOnOutput:
            multiStepFeedback.setCurrentStep(currentStep)
            self.checkInvalidOnOutput(
                layerHandler,
                inputCenterPointLyr,
                multiStepFeedback,
                polygonFeatList,
                invalid_polygon_sink,
            )
            currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.checkUnusedBoundariesAndWriteOutput(
            context,
            boundaryLineLyr,
            output_polygon_sink_id,
            unused_boundary_flag_sink,
            multiStepFeedback,
        )

        return {
            self.OUTPUT_POLYGONS: output_polygon_sink_id,
            self.FLAGS: self.flag_id,
            self.INVALID_POLYGON_LOCATION: invalid_polygon_sink_id,
            self.UNUSED_BOUNDARY_LINES: unused_boundary_flag_sink_id,
        }

    def checkUnusedBoundariesAndWriteOutput(
        self,
        context,
        boundaryLineLyr,
        output_polygon_sink_id,
        unused_boundary_flag_sink,
        multiStepFeedback,
    ):
        if boundaryLineLyr is None:
            return
        multiStepFeedback.setProgressText(self.tr("Checking unused boundaries..."))
        flags = self.checkUnusedBoundaries(
            boundaryLineLyr=boundaryLineLyr,
            output_polygon_sink_id=output_polygon_sink_id,
            feedback=multiStepFeedback,
            context=context,
        )
        unused_boundary_flag_sink.addFeatures(
            boundaryLineLyr.getFeatures(list(flags.keys())), QgsFeatureSink.FastInsert
        )

    def checkInvalidOnOutput(
        self,
        layerHandler,
        inputCenterPointLyr,
        feedback,
        polygonFeatList,
        invalid_polygon_sink,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setProgressText(
            self.tr("Checking for invalid geometries on output polygons...")
        )
        multiStepFeedback.setCurrentStep(0)
        invalidGeomFlagDict, _ = layerHandler.identifyInvalidGeometries(
            polygonFeatList,
            len(polygonFeatList),
            inputCenterPointLyr,
            ignoreClosed=False,
            fixInput=False,
            parameterDict=None,
            geometryType=None,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        flagLambda = lambda x: self.flagFeature(
            flagGeom=x[1]["geom"], flagText=x[1]["reason"], sink=invalid_polygon_sink
        )
        list(map(flagLambda, invalidGeomFlagDict.items()))

    def prepareInvalidPolygonFlags(self, parameters, context, inputCenterPointLyr):
        (invalid_polygon_sink, invalid_polygon_sink_id) = self.parameterAsSink(
            parameters,
            self.INVALID_POLYGON_LOCATION,
            context,
            self.getFlagFields(),
            QgsWkbTypes.Point,
            inputCenterPointLyr.sourceCrs(),
        )

        return invalid_polygon_sink, invalid_polygon_sink_id

    def writeOutputPolygons(
        self, output_polygon_sink, multiStepFeedback, polygonFeatList, flagDict
    ):
        multiStepFeedback.setProgressText(self.tr("Writing output..."))
        output_polygon_sink.addFeatures(polygonFeatList, QgsFeatureSink.FastInsert)
        nItems = len(flagDict)
        for current, (flagGeom, flagText) in enumerate(flagDict.items()):
            if multiStepFeedback.isCanceled():
                break
            self.flagFeature(flagGeom, flagText, fromWkb=True)
            multiStepFeedback.setProgress(current * 100 / nItems)

    def computePolygonsFromCenterPointAndBoundaries(
        self,
        context,
        layerHandler,
        algRunner,
        inputCenterPointLyr,
        boundaryLineLyr,
        constraintLineLyrList,
        constraintPolygonLyrList,
        onlySelected,
        geographicBoundaryLyr,
        attributeBlackList,
        suppressPolygonWithoutCenterPointFlag,
        multiStepFeedback,
    ):
        multiStepFeedback.pushInfo(
            self.tr("Starting {0}...").format(self.displayName())
        )
        multiStepFeedback.setProgressText(
            self.tr("Computing polygons from center points and boundaries...")
        )
        (
            polygonFeatList,
            flagDict,
        ) = layerHandler.getPolygonsFromCenterPointsAndBoundaries(
            inputCenterPointLyr,
            geographicBoundaryLyr=geographicBoundaryLyr,
            constraintLineLyrList=constraintLineLyrList + [boundaryLineLyr] if boundaryLineLyr is not None else constraintLineLyrList,
            constraintPolygonLyrList=constraintPolygonLyrList,
            onlySelected=onlySelected,
            suppressPolygonWithoutCenterPointFlag=suppressPolygonWithoutCenterPointFlag,
            context=context,
            feedback=multiStepFeedback,
            attributeBlackList=attributeBlackList,
            algRunner=algRunner,
        )

        return polygonFeatList, flagDict

    def checkUnusedBoundaries(
        self, boundaryLineLyr, output_polygon_sink_id, feedback=None, context=None
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        lyr = processing.run(
            "native:addautoincrementalfield",
            parameters={
                "INPUT": output_polygon_sink_id,
                "FIELD_NAME": "featid",
                "START": 1,
                "GROUP_FIELDS": [],
                "SORT_EXPRESSION": "",
                "SORT_ASCENDING": True,
                "SORT_NULLS_FIRST": False,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
            context=context,
            feedback=multiStepFeedback,
        )["OUTPUT"]
        processing.run(
            "native:createspatialindex", {"INPUT": lyr}, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        return SpatialRelationsHandler().checkDE9IM(
            layerA=boundaryLineLyr,
            layerB=lyr,
            mask="*1*******",
            cardinality="1..*",
            feedback=multiStepFeedback,
            ctx=context,
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "buildpolygonsfromcenterpointsandboundariesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Build Polygons From Center Points and Boundaries")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Manipulation Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Manipulation Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "BuildPolygonsFromCenterPointsAndBoundariesAlgorithm", string
        )

    def createInstance(self):
        return BuildPolygonsFromCenterPointsAndBoundariesAlgorithm()
