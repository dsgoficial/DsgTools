# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-08
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

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsGeometry,
    QgsFeatureRequest,
)

from .validationAlgorithm import ValidationAlgorithm


class IdentifySegmentErrorsBetweenLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    REFERENCE_LINE = "REFERENCE_LINE"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.REFERENCE_LINE, self.tr("Reference lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        referenceSource = self.parameterAsSource(parameters, self.REFERENCE_LINE, context)
        self.prepareFlagSink(parameters, inputSource, QgsWkbTypes.MultiPoint, context)
        nFeats = inputSource.featureCount()
        if inputSource is None or nFeats == 0:
            return {self.FLAGS: self.flag_id}
        stepSize = 100 / nFeats
        for current, feat in enumerate(inputSource.getFeatures()):
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            bbox = geom.boundingBox()
            vertexList = list(geom.vertices())
            originalDamVertexSet = set(map(lambda x: QgsGeometry(x), vertexList))
            roadVertexSet = set()
            request = QgsFeatureRequest(bbox)
            for candidateRoadFeat in referenceSource.getFeatures(request):
                candidateGeom = candidateRoadFeat.geometry()
                if not candidateGeom.intersects(geom) or candidateGeom.touches(geom):
                    continue
                intersectionGeom = geom.intersection(candidateGeom)
                intersectionSet = set(
                    map(lambda x: QgsGeometry(x), intersectionGeom.vertices())
                )
                if len(intersectionSet) == 1:
                    continue
                candidateGeomVertexSet = set(
                    map(lambda x: QgsGeometry(x), candidateGeom.vertices())
                )
                roadVertexSet = roadVertexSet.union(candidateGeomVertexSet)
            if roadVertexSet == set():
                continue
            damVertexSet = originalDamVertexSet - roadVertexSet
            if len(damVertexSet) == 0:
                continue
            if len(damVertexSet) == 1 and list(damVertexSet)[0] in [
                damVertexSet[0],
                damVertexSet[-1],
            ]:
                continue
            newVertexSet = originalDamVertexSet - damVertexSet
            if newVertexSet == set():
                continue
            firstVertex, *selectedVertexList = list(newVertexSet)
            for v in selectedVertexList:
                firstVertex = firstVertex.combine(v)
            self.flagFeature(
                flagGeom=firstVertex,
                flagText=self.tr(
                    "Invalid unshared vertexes on input line that intersects reference line"
                ),
            )
            feedback.setProgress(current * stepSize)
        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifysegmenterrorsbetweenlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Segment Errors Between Lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifySegmentErrorsBetweenLinesAlgorithm", string
        )

    def createInstance(self):
        return IdentifySegmentErrorsBetweenLinesAlgorithm()
