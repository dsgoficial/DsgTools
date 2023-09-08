# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid
from ...algRunner import AlgRunner
import processing, os, requests
from time import sleep
from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication
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
)


class CreateFramesWithConstraintAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    STOP_SCALE = "STOP_SCALE"
    XSUBDIVISIONS = "XSUBDIVISIONS"
    YSUBDIVISIONS = "YSUBDIVISIONS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.scales = [
            "1000k",
            "500k",
            "250k",
            "100k",
            "50k",
            "25k",
            "10k",
            "5k",
            "2k",
            "1k",
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.STOP_SCALE,
                self.tr("Desired scale"),
                options=self.scales,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.XSUBDIVISIONS,
                self.tr("Number of subdivisions on x-axis"),
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.YSUBDIVISIONS,
                self.tr("Number of subdivisions on y-axis"),
                defaultValue=1,
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Created Frames"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        featureHandler = FeatureHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        stopScaleIdx = self.parameterAsEnum(parameters, self.STOP_SCALE, context)
        stopScale = self.scales[stopScaleIdx]
        stopScale = int(stopScale.replace("k", ""))
        fields = QgsFields()
        fields.append(QgsField("inom", QVariant.String))
        fields.append(QgsField("mi", QVariant.String))
        crs = inputLyr.crs()
        xSubdivisions = self.parameterAsInt(parameters, self.XSUBDIVISIONS, context)
        ySubdivisions = self.parameterAsInt(parameters, self.YSUBDIVISIONS, context)
        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields, QgsWkbTypes.Polygon, crs
        )
        featureList = []
        coordinateTransformer = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(crs.geographicCrsAuthId()),
            crs,
            QgsProject.instance(),
        )
        featureHandler.getSystematicGridFeaturesWithConstraint(
            featureList,
            inputLyr,
            stopScale,
            coordinateTransformer,
            fields,
            xSubdivisions=xSubdivisions,
            ySubdivisions=ySubdivisions,
            feedback=feedback,
        )
        list(
            map(
                lambda x: output_sink.addFeature(x, QgsFeatureSink.FastInsert),
                featureList,
            )
        )

        return {"OUTPUT": output_sink_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "createframeswithconstraintalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Generate Systematic Grid Related to Layer")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Other Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Other Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateFramesWithConstraintAlgorithm", string)

    def createInstance(self):
        return CreateFramesWithConstraintAlgorithm()
