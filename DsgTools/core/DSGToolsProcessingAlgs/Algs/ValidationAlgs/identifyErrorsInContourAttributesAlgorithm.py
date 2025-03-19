# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-31
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

from collections import defaultdict
from typing import Any, Dict, Set
from PyQt5.QtCore import QCoreApplication

import concurrent.futures
import os
from itertools import product, chain
from qgis.core import (
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsFeature,
    QgsProcessingParameterField,
    QgsProcessingParameterExpression,
    QgsProcessingParameterString,
    QgsVectorLayer,
    QgsFeedback,
    QgsProcessingParameterEnum,
    QgsWkbTypes,
    QgsFeatureRequest,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools import graphHandler


class IdentifyErrorsInContourAttributesAlgorithm(ValidationAlgorithm):
    INPUT_CONTOURS = "INPUT_CONTOURS"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    MASTER_CONTOUR_EXPRESSION = "MASTER_CONTOUR_EXPRESSION"
    SCALE = "SCALE"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_CONTOURS,
                self.tr("Input Contours layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="elemnat_curva_nivel_l",
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CONTOUR_ATTR,
                self.tr("Contour value field"),
                "cota",
                "INPUT_CONTOURS",
                QgsProcessingParameterField.Any,
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.MASTER_CONTOUR_EXPRESSION,
                self.tr("Master contours expression"),
                """"indice" = 1""",
                self.INPUT_CONTOURS,
            )
        )
        self.scales = [
            "1:25.000",
            "1:50.000",
            "1:100.000",
            "1:250.000",
        ]
        self.equidistances = {
            0: 10,
            1: 20,
            2: 40,
            3: 100,
        }
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE, self.tr("Scale"), options=self.scales, defaultValue=0
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
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT_CONTOURS, context)
        scale = self.parameterAsEnum(parameters, self.SCALE, context)
        equidistance = self.equidistances[scale]
        heightFieldName = self.parameterAsFields(parameters, self.CONTOUR_ATTR, context)[0]
        masterContourExpression = self.parameterAsExpression(
            parameters, self.MASTER_CONTOUR_EXPRESSION, context
        )
        masterContourExpression = masterContourExpression if masterContourExpression != "" else None
        if masterContourExpression is None:
            raise QgsProcessingException("invalid expression")
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.LineString, context, addFeatId=True)
        request = QgsFeatureRequest()
        request.setFilterExpression(expression=f"""{masterContourExpression} and ("{heightFieldName}" % (5*{equidistance}) = 0)""")
        masterContoursWithCorrectIndexValueSet = set(
            f.id() for f in inputLyr.getFeatures(request)
        )
        request = QgsFeatureRequest()
        request.setFilterExpression(expression=f"""not({masterContourExpression}) and ("{heightFieldName}" % (5*{equidistance}) != 0)""")
        normalContoursWithCorrectIndexValueSet = set(
            f.id() for f in inputLyr.getFeatures(request)
        )
        nFeats = inputLyr.featureCount()
        if nFeats == 0:
            return {self.FLAGS: self.flag_id}
        stepSize = 100/nFeats
        for current, feat in enumerate(inputLyr.getFeatures()):
            if feedback.isCanceled():
                break
            feedback.setProgress(current * stepSize)
            if feat.id() in masterContoursWithCorrectIndexValueSet or feat.id() in normalContoursWithCorrectIndexValueSet:
                continue
            self.flagFeature(
                flagGeom=feat.geometry(),
                flagText=self.tr(f"Contour with height {feat[heightFieldName]} has invalid index"),
                featid=feat.id(),
            )
        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyerrorsincontourattributesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Errors In Contour Attributes Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Terrain Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Terrain Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyErrorsInContourAttributesAlgorithm", string
        )

    def createInstance(self):
        return IdentifyErrorsInContourAttributesAlgorithm()
