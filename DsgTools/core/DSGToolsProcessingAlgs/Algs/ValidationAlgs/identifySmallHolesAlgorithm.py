# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton / Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho / @eb.mil.br
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

# from qgis.PyQt.QtCore import (QCoreApplication, QVariant)
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsCoordinateReferenceSystem,
    QgsGeometry,
    QgsField,
    QgsFeature,
    QgsFields,
    QgsProcessingParameterMultipleLayers,
    QgsWkbTypes,
)
from qgis.utils import iface

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifySmallHolesAlgorithm(ValidationAlgorithm):

    INPUT_LAYER_LIST = "INPUT_LAYER_LIST"
    MAX_HOLE_SIZE = "MAX_HOLE_SIZE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                "INPUT_LAYER_LIST",
                self.tr("Input layer(s)"),
                QgsProcessing.TypeVectorPolygon,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                "MAX_HOLE_SIZE",
                self.tr("Tolerance"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Flags"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.setProgressText(self.tr("Searching holes smaller than tolerance"))
        layerList = self.parameterAsLayerList(
            parameters, self.INPUT_LAYER_LIST, context
        )
        maxSize = self.parameterAsDouble(parameters, self.MAX_HOLE_SIZE, context)
        crsStr = iface.mapCanvas().mapSettings().destinationCrs().authid()
        crs = QgsCoordinateReferenceSystem(crsStr)
        smallRings = []
        listSize = len(layerList)
        progressStep = 100 / listSize if listSize else 0
        step = 0
        newField = QgsFields()
        newField.append(QgsField("area", QVariant.Double))
        (self.sink, self.sink_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, newField, QgsWkbTypes.MultiPolygon, crs
        )
        for step, layer in enumerate(layerList):
            if feedback.isCanceled():
                break
            for feature in layer.getFeatures():
                if not feature.hasGeometry():
                    continue
                for poly in feature.geometry().asMultiPolygon():
                    onlyrings = poly[1:]
                    for ring in onlyrings:
                        newRing = QgsGeometry.fromPolygonXY([ring])
                        if newRing.area() < maxSize:
                            smallRings.append(newRing)
            feedback.setProgress(step * progressStep)

        if len(smallRings) == 0:
            feedback.pushInfo(
                self.tr(f"Holes smaller than {str(maxSize)} were not found")
            )
            return {self.OUTPUT: self.sink_id}
        self.outputLayer(smallRings, newField)
        return {self.OUTPUT: self.sink_id}

    def outputLayer(self, smallRings, newField):
        features = smallRings
        for feature in features:
            newFeat = QgsFeature()
            newFeat.setGeometry(feature)
            newFeat.setFields(newField)
            newFeat["area"] = feature.area()
            self.sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifysmallholes"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Small Holes")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Small Object Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Small Object Handling"

    def tr(self, string):
        return QCoreApplication.translate("IdentifySmallHolesAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifySmallHolesAlgorithm()
