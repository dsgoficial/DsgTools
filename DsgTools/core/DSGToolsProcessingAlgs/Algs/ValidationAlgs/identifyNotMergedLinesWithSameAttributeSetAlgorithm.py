# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-19
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import itertools
import concurrent.futures
import os
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterField
)


class IdentifyNotMergedLinesWithSameAttributeSetAlgorithm(ValidationAlgorithm):
    INPUT_LINES = "INPUT_LINES"
    SELECTED = 'SELECTED'
    ATTRIBUTE_BLACK_LIST = 'ATTRIBUTE_BLACK_LIST'
    IGNORE_VIRTUAL_FIELDS = 'IGNORE_VIRTUAL_FIELDS'
    IGNORE_PK_FIELDS = 'IGNORE_PK_FIELDS'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LINES,
                self.tr("Input lines"),
                QgsProcessing.TypeVectorLine,
                optional=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_BLACK_LIST, 
                self.tr('Fields to ignore'),
                None, 
                'INPUT', 
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_VIRTUAL_FIELDS,
                self.tr('Ignore virtual fields'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNORE_PK_FIELDS,
                self.tr('Ignore primary key fields'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr('Geographic Boundary (this layer only filters the output dangles)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
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
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        pointFilterLyrList = self.parameterAsLayerList(
            parameters, self.POINTFILTERLAYERS, context) 
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.LINEFILTERLAYERS, context)
        polygonFilterLyrList = self.parameterAsLayerList(
            parameters, self.POLYGONFILTERLAYERS, context)
        
        return {
            "FLAGS": self.flag_id
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifynotmergedlineswithsameattributeset"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Not Merged Lines With Same Attribute Set")

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
            "IdentifyNotMergedLinesWithSameAttributeSetAlgorithm", string
        )

    def createInstance(self):
        return IdentifyNotMergedLinesWithSameAttributeSetAlgorithm()
