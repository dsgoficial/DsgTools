# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from PyQt5.QtCore import QCoreApplication, QVariant

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsVectorLayerUtils,
    QgsGeometry,
    QgsMultiPoint,
    QgsProcessingAlgorithm,
    QgsWkbTypes,
    QgsField,
    QgsFeature,
)


class ExtractMiddleVertexOnLineAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input Line Layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        if inputSource is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        outputFields = inputSource.fields()
        outputFields.append(QgsField("part_id", QVariant.Int))

        (output_sink, output_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            outputFields,
            QgsWkbTypes.Point,
            inputSource.sourceCrs(),
        )
        if output_sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        featCount = inputSource.featureCount()
        if featCount == 0:
            return {self.OUTPUT: output_dest_id}

        stepSize = 100 / featCount

        for current, feat in enumerate(inputSource.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                break
            geom = feat.geometry()
            if geom.isNull() or geom.isEmpty():
                continue
            for partId, part in enumerate(geom.asGeometryCollection()):
                if feedback is not None and feedback.isCanceled():
                    break
                vertexCount = len(list(part.vertices()))
                vertex = (
                    part.vertexAt(vertexCount // 2)
                    if vertexCount > 2
                    else part.vertexAt(0)
                )
                newFeat = QgsFeature(outputFields)
                newFeat.setAttributes(feat.attributes() + [partId])
                newFeat.setGeometry(QgsGeometry(vertex))
                output_sink.addFeature(newFeat)
            if feedback is not None:
                feedback.setProgress(current * stepSize)

        return {self.OUTPUT: output_dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "extractmiddlevertexonlinealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Extract Middle Vertex on Line")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ExtractMiddleVertexOnLineAlgorithm", string)

    def createInstance(self):
        return ExtractMiddleVertexOnLineAlgorithm()
