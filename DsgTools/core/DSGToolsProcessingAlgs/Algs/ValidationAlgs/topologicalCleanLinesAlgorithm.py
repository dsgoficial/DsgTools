# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
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
from collections import defaultdict
from PyQt5.QtCore import QCoreApplication

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsProject,
    QgsSpatialIndex,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .topologicalCleanAlgorithm import TopologicalCleanAlgorithm


class TopologicalCleanLinesAlgorithm(TopologicalCleanAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    MINAREA = "MINAREA"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        snapParam = QgsProcessingParameterNumber(
            self.TOLERANCE,
            self.tr("Snap radius"),
            minValue=0,
            defaultValue=1,
            type=QgsProcessingParameterNumber.Double,
        )
        snapParam.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(snapParam)

        areaParam = QgsProcessingParameterNumber(
            self.MINAREA,
            self.tr("Minimum area"),
            minValue=0,
            defaultValue=1e-8,
            type=QgsProcessingParameterNumber.Double,
        )
        areaParam.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(areaParam)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Bounds Layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )
    
    def flagCoverageIssues(self, cleanedCoverage, error, feedback):
        overlapDict = defaultdict(list)
        for current, feat in enumerate(cleanedCoverage.getFeatures()):
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            geomKey = geom.asWkb()
            overlapDict[geomKey].append(feat)
        for geomKey, featList in overlapDict.items():
            if feedback.isCanceled():
                break
            if len(featList) == 0:
                continue
            elif len(featList) == 1:
                attrList = featList[0].attributes()
                if attrList == len(attrList) * [None]:
                    self.flagFeature(
                        featList[0].geometry(), self.tr("Gap in coverage.")
                    )
                continue
            groupByLayerDict = defaultdict(list)
            for f in featList:
                groupByLayerDict[f["layer"]].append(f["featid"])
            for fl in groupByLayerDict.values():
                if len(fl) == 1:
                    continue
                txtList = []
                for i in fl:
                    txtList += ["{0} (id={1})".format(i["layer"], i["featid"])]
                txt = ", ".join(txtList)
                self.flagFeature(
                    fl[0].geometry(),
                    self.tr("Features from {0} overlap").format(txt),
                )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "topologicalcleanlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Topological Clean Linestrings")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Topological Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Topological Processes"

    def tr(self, string):
        return QCoreApplication.translate("TopologicalCleanLinesAlgorithm", string)

    def createInstance(self):
        return TopologicalCleanLinesAlgorithm()
