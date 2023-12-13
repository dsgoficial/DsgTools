# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-26
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
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsDataSourceUri,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsGeometry,
    QgsProcessingParameterField,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterExpression,
    QgsProcessingException,
    QgsProcessingParameterString,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterType,
    QgsProcessingParameterCrs,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsField,
    QgsFields,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterExtent,
)


class AssignBoundingBoxFilterToLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    BB_FILTER = "BB_FILTER"
    BEHAVIOR = "BEHAVIOR"
    OUTPUT = "OUTPUT"
    AndMode, OrMode, ReplaceMode = list(range(3))

    def initAlgorithm(self, config):
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
            QgsProcessingParameterExtent(self.BB_FILTER, self.tr("Filter"))
        )

        self.modes = [
            self.tr("Append to existing filter with AND clause"),
            self.tr("Append to existing filter with OR clause"),
            self.tr("Replace filter"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.BEHAVIOR, self.tr("Behavior"), options=self.modes, defaultValue=0
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT, self.tr("Original layers with assigned styles")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        boundingBoxGeometry = self.parameterAsExtentGeometry(
            parameters, self.BB_FILTER, context
        )
        behavior = self.parameterAsEnum(parameters, self.BEHAVIOR, context)
        progressStep = 100 / len(inputLyrList) if len(inputLyrList) else 0
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            if lyr.dataProvider().name() != "postgres":
                feedback.pushInfo(
                    self.tr(
                        "Operation only defined for postgres provider. Layer {layer} will be skipped."
                    )
                )
                continue
            bboxClause = self.buildSpatialClause(lyr, boundingBoxGeometry)
            if bboxClause == "":
                continue
            filterExpression = self.adaptFilter(lyr, bboxClause, behavior)
            lyr.setSubsetString(filterExpression)
            feedback.setProgress(current * progressStep)

        return {self.OUTPUT: inputLyrList}

    def adaptFilter(self, lyr, bboxClause, behavior):
        """
        Adapts filter according to the selected mode
        """
        originalFilter = lyr.subsetString()
        if (
            behavior == AssignBoundingBoxFilterToLayersAlgorithm.ReplaceMode
            or originalFilter == ""
        ):
            return bboxClause
        clause = (
            " AND "
            if behavior == AssignBoundingBoxFilterToLayersAlgorithm.AndMode
            else " OR "
        )
        return clause.join([originalFilter, bboxClause])

    def buildSpatialClause(self, lyr, boundingBoxGeometry):
        geometryColumn = QgsDataSourceUri(
            lyr.dataProvider().dataSourceUri()
        ).geometryColumn()
        if geometryColumn == "":
            return ""
        epsg = lyr.crs().authid().replace("EPSG:", "SRID=")
        GeometryHandler().reprojectFeature(boundingBoxGeometry, lyr.crs())
        geomEwkt = " ; ".join([epsg, boundingBoxGeometry.asWkt()])
        return """ST_INTERSECTS({geom}, ST_GEOMFROMEWKT('{ewkt}'))""".format(
            geom=geometryColumn, ewkt=geomEwkt
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "assignboundingboxfiltertolayers"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Assign Bounding Box Filter to Layers")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Layer Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Layer Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate(
            "AssignBoundingBoxFilterToLayersAlgorithm", string
        )

    def createInstance(self):
        return AssignBoundingBoxFilterToLayersAlgorithm()
