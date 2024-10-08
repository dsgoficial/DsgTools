# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-03-21
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

import concurrent.futures

from itertools import chain
import os
from typing import Dict, List, Optional, Set
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools import graphHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsFeedback,
    QgsFeature,
    QgsVectorLayer,
    QgsProcessingParameterDistance,
)

from ...algRunner import AlgRunner
from ..ValidationAlgs.validationAlgorithm import ValidationAlgorithm


class FindSmallClosedLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    MIN_LENGTH = "MIN_LENGTH"
    METHOD = "METHOD"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterDistance(
                self.MIN_LENGTH,
                self.tr("Minimum size"),
                minValue=0,
                parentParameterName=self.INPUT,
                defaultValue=0.001,
            )
        )
        self.selectionIdDict = {
            1: Qgis.SelectBehavior.SetSelection,
            2: Qgis.SelectBehavior.AddToSelection,
            3: Qgis.SelectBehavior.IntersectSelection,
            4: Qgis.SelectBehavior.RemoveFromSelection,
        }
        self.method = [
            self.tr("Remove features from input layer"),
            self.tr("Modify current selection by creating new selection"),
            self.tr("Modify current selection by adding to current selection"),
            self.tr("Modify current selection by selecting within current selection"),
            self.tr("Modify current selection by removing from current selection"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD, self.tr("Method"), options=self.method, defaultValue=0
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # get the network handler
        self.algRunner = AlgRunner()
        self.layerHandler = LayerHandler()
        inputLayer = self.parameterAsLayer(parameters, self.INPUT, context)
        minLen = self.parameterAsDouble(parameters, self.MIN_LENGTH, context)
        method = self.parameterAsEnum(parameters, self.METHOD, context)

        nSteps = 6
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating local cache..."))
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Filtering small individual lines...")
        )
        smallIndividualLines = self.algRunner.runFilterExpression(
            localCache,
            expression=f"length($geometry)<{minLen}",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Dissolving small lines..."))
        dissolved = self.algRunner.runDissolve(
            inputLyr=smallIndividualLines,
            context=context,
            feedback=multiStepFeedback,
            # is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Filtering small dissolved lines..."))
        smallLines = self.algRunner.runFilterExpression(
            dissolved,
            expression=f"length($geometry)<{minLen}",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Filtering closed lines..."))
        closedLines = self.findClosedLines(smallLines)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Finding lines..."))
        lines = self.withinFeatures(localCache, closedLines)
        idsToRemove = {line["featid"] for line in lines}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.manageSelectedIdsUsingInputMethod(inputLayer, method, idsToRemove)
        return {}

    def findClosedLines(self, inputLyr) -> Set[QgsFeature]:
        closedLines = set()
        for feat in inputLyr.getFeatures():
            geom = feat.geometry()
            if geom.isMultipart():
                for part in geom.asMultiPolyline():
                    if part[0] == part[-1]:
                        closedLines.add(feat)
            else:
                line = geom.asPolyline()
                if line[0] == line[-1]:
                    closedLines.add(feat)
        return closedLines

    def withinFeatures(self, inputLyr, features) -> Set[QgsFeature]:
        featsWithin = set()
        for feature in features:
            geometry = feature.geometry()
            bbox = geometry.boundingBox()
            for feat in inputLyr.getFeatures(bbox):
                geom = feat.geometry()
                if geom.within(geometry):
                    featsWithin.add(feat)
        return featsWithin

    def manageSelectedIdsUsingInputMethod(
        self, inputLyr: QgsVectorLayer, method, idsToRemove
    ):
        if method != 0:
            inputLyr.selectByIds(list(idsToRemove), self.selectionIdDict[method])
            return {}
        inputLyr.startEditing()
        inputLyr.beginEditCommand(self.tr("Deleting features"))
        inputLyr.deleteFeatures(list(idsToRemove))
        inputLyr.endEditCommand()
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "findsmallclosedlinesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Find Small Closed Lines Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Generalization Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("FindSmallClosedLinesAlgorithm", string)

    def createInstance(self):
        return FindSmallClosedLinesAlgorithm()
