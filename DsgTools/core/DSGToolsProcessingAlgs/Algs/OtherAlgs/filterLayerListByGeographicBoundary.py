# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-05
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from itertools import chain
from typing import Any, Dict
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsWkbTypes,
    QgsProcessingParameterVectorLayer,
    QgsProject,
    QgsProcessingContext,
    QgsCoordinateReferenceSystem,
    QgsProcessingMultiStepFeedback,
    QgsFeatureSink,
    QgsFields,
)


class FilterLayerListByGeographicBoundary(QgsProcessingAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    POINT_OUTPUT = "POINT_OUTPUT"
    LINE_OUTPUT = "LINE_OUTPUT"
    POLYGON_OUTPUT = "POLYGON_OUTPUT"

    def __init__(self):
        super(FilterLayerListByGeographicBoundary, self).__init__()

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Input Layers"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_OUTPUT,
                self.tr("Merged Point layer with features that intersect the geographic boundary"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_OUTPUT,
                self.tr("Merged line layer with features that intersect the geographic boundary"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_OUTPUT,
                self.tr("Merged polygon layer with features that intersect the geographic boundary"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        geographicBoundaryLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        algRunner = AlgRunner()
        listSize = len(inputLyrList)
        crs = QgsProject.instance().crs() if listSize == 0 else inputLyrList[0].crs()
        fieldList = [field for field in chain.from_iterable(i.fields() for i in inputLyrList)]
        fieldDict = {
            field.name(): field for field in fieldList
        }
        self.fields = QgsFields([fieldDict[f.name()] for f in fieldList])

        self.buildOutputSinks(
            parameters,
            context,
            outputCrs=crs,
        )
        if listSize == 0:
            return {
                self.POINT_OUTPUT: self.point_flag_id,
                self.LINE_OUTPUT: self.line_flag_id,
                self.POLYGON_OUTPUT: self.poly_flag_id,
            }
        stepSize = 100 / listSize if listSize else 0
        geometryDict = {
            QgsWkbTypes.PointGeometry: [],
            QgsWkbTypes.LineGeometry: [],
            QgsWkbTypes.PolygonGeometry: [],
        }
        
        if geographicBoundaryLyr is not None and not geographicBoundaryLyr.hasSpatialIndex():
            algRunner.runCreateSpatialIndex(geographicBoundaryLyr, context, is_child_algorithm=True)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2*listSize, feedback)
        currentStep = 0
        for current, lyr in enumerate(inputLyrList):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(currentStep)
            if geographicBoundaryLyr is None or geographicBoundaryLyr.featureCount() == 0:
                geometryDict[lyr.geometryType()].append(lyr.id())
                feedback.setProgress(current * stepSize)
                continue
            if not lyr.hasSpatialIndex():
                algRunner.runCreateSpatialIndex(lyr, context, is_child_algorithm=True)
            intersectionLyrId = algRunner.runExtractByLocation(
                inputLyr=lyr,
                intersectLyr=geographicBoundaryLyr,
                predicate=AlgRunner.Intersects,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )
            geometryDict[lyr.geometryType()].append(intersectionLyrId)
            currentStep += 1

        for current, (geomType, inputList) in enumerate(geometryDict.items()):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(currentStep)
            if len(inputList) == 0:
                continue
            merged = algRunner.runMergeVectorLayers(inputList=inputList, context=context, feedback=multiStepFeedback, crs=crs)
            list(
                map(
                    lambda x: self.flagSinkDict[geomType].addFeature(
                        x, QgsFeatureSink.FastInsert
                    ),
                    merged.getFeatures(),
                )
            )
            currentStep += 1
        
        return {
            self.POINT_OUTPUT: self.point_flag_id,
            self.LINE_OUTPUT: self.line_flag_id,
            self.POLYGON_OUTPUT: self.poly_flag_id,
        }
    
    def buildOutputSinks(self, parameters: Dict[str, Any], context: QgsProcessingContext, outputCrs: QgsCoordinateReferenceSystem) -> None:
        self.point_flag_sink, self.point_flag_id = self.parameterAsSink(
            parameters,
            self.POINT_OUTPUT,
            context,
            self.fields,
            QgsWkbTypes.Point,
            outputCrs,
        )
        self.line_flag_sink, self.line_flag_id = self.parameterAsSink(
            parameters,
            self.LINE_OUTPUT,
            context,
            self.fields,
            QgsWkbTypes.LineString,
            outputCrs,
        )
        self.poly_flag_sink, self.poly_flag_id = self.parameterAsSink(
            parameters,
            self.POLYGON_OUTPUT,
            context,
            self.fields,
            QgsWkbTypes.Polygon,
            outputCrs,
        )
        self.flagSinkDict = {
            QgsWkbTypes.PointGeometry: self.point_flag_sink,
            QgsWkbTypes.LineGeometry: self.line_flag_sink,
            QgsWkbTypes.PolygonGeometry: self.poly_flag_sink,
        }

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "filterlayerlistbygeographicboundary"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Filter layer list by geographic boundary")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Model Helpers")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Model Helpers"

    def tr(self, string):
        return QCoreApplication.translate("FilterLayerListByGeographicBoundary", string)

    def createInstance(self):
        return FilterLayerListByGeographicBoundary()
