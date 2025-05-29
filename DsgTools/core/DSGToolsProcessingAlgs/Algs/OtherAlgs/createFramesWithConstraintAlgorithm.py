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
from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMapLayer,
    QgsWkbTypes,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingException,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsField,
    QgsFields,
    QgsProcessingParameterDefinition,
    QgsMapLayer,
    QgsVectorLayer,
    QgsGeometry,
    QgsFeature,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


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
            QgsProcessingParameterMapLayer(
                self.INPUT,
                self.tr("Input Layer (Vector or Raster)"),
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

        param = QgsProcessingParameterNumber(
            self.XSUBDIVISIONS,
            self.tr("Number of subdivisions on x-axis"),
            minValue=1,
            type=QgsProcessingParameterNumber.Integer,
            optional=True,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)

        self.addParameter(param)

        param = QgsProcessingParameterNumber(
            self.YSUBDIVISIONS,
            self.tr("Number of subdivisions on y-axis"),
            minValue=1,
            type=QgsProcessingParameterNumber.Integer,
            optional=True,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Created Frames"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        featureHandler = FeatureHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsLayer(parameters, self.INPUT, context)
        inputOld = inputLyr
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        # Verificar se é uma camada raster
        if inputLyr.type() == QgsMapLayer.RasterLayer:
            # Obter o extent do raster e convertê-lo em um polígono
            extent = inputLyr.extent()
            rasterGeom = QgsGeometry.fromRect(extent)

            # Criar uma camada temporária de polígono com esse extent
            fields = QgsFields()
            tempLayer = QgsVectorLayer(
                "Polygon?crs=" + inputLyr.crs().authid(), "temp", "memory"
            )
            provider = tempLayer.dataProvider()
            tempLayer.startEditing()
            feat = QgsFeature()
            feat.setGeometry(rasterGeom)
            provider.addFeature(feat)
            tempLayer.commitChanges()

            # Usar essa camada temporária como entrada
            inputLyr = tempLayer

        geomTypeLyr = (
            inputLyr.geometryType()
            if hasattr(inputLyr, "geometryType")
            else QgsWkbTypes.PolygonGeometry
        )
        if (
            geomTypeLyr == QgsWkbTypes.PointGeometry
            or geomTypeLyr == QgsWkbTypes.LineGeometry
        ):
            inputLyr = algRunner.runBuffer(
                inputLayer=inputLyr, distance=10 ** (-5), context=context
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

        default_x = 1
        default_y = 1

        if stopScale == 50:
            default_x = 2
            default_y = 2
        elif stopScale == 100:
            default_x = 4
            default_y = 4
        elif stopScale == 250:
            default_x = 12
            default_y = 8

        if xSubdivisions is None or xSubdivisions == 0:
            xSubdivisions = default_x
        if ySubdivisions is None or ySubdivisions == 0:
            ySubdivisions = default_y

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

        # Função de filtro para remover MI que não intersectam com a camada original
        def filterFunc(feat):
            if hasattr(inputOld, "type") and inputOld.type() == QgsMapLayer.RasterLayer:
                geom = feat.geometry()
                extent_geom = QgsGeometry.fromRect(inputOld.extent())
                return geom.intersects(extent_geom)
            else:
                geom = feat.geometry()
                bbox = geom.boundingBox()
                return any(
                    geom.intersects(f.geometry()) for f in inputOld.getFeatures(bbox)
                )

        # Se a entrada original for um polígono, não precisamos filtrar
        needsFiltering = True
        if hasattr(inputOld, "type"):
            if (
                inputOld.type() == QgsMapLayer.VectorLayer
                and inputOld.geometryType() == QgsWkbTypes.PolygonGeometry
            ):
                needsFiltering = False

        if needsFiltering:
            list(
                map(
                    lambda x: output_sink.addFeature(x, QgsFeatureSink.FastInsert),
                    filter(filterFunc, featureList),
                )
            )
        else:
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
        return self.tr("Grid Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Grid Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateFramesWithConstraintAlgorithm", string)

    def createInstance(self):
        return CreateFramesWithConstraintAlgorithm()
