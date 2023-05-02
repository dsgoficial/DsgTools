# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-28
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


from PyQt5.QtCore import QCoreApplication, QRegExp
from qgis.core import (QgsGeometry, QgsProcessing,
                       QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString, Qgis)
from qgis.PyQt.QtGui import QRegExpValidator

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler


class ValidationString(QgsProcessingParameterString):
    """
    Auxiliary class for pre validation on measurer's names.
    """

    # __init__ not necessary

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        regex = QRegExp("[FfTt012\*]{9}")
        acceptable = QRegExpValidator.Acceptable
        return (
            isinstance(value, str)
            and QRegExpValidator(regex).validate(value, 9)[0] == acceptable
        )


class SelectByDE9IMAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    INTERSECT = "INTERSECT"
    DE9IM = "DE9IM"
    METHOD = "METHOD"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Select features from"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INTERSECT,
                self.tr("By comparing features from"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        param = ValidationString(self.DE9IM, description=self.tr("DE9IM"))
        self.addParameter(param)
        self.method = [
            self.tr("creating new selection"),
            self.tr("adding to current selection"),
            self.tr("selecting within current selection"),
            self.tr("removing from current selection"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD, self.tr("Modify current selection by"), options=self.method, defaultValue=0
            )
        )
        self.selectionIdDict = {
            0: Qgis.SelectBehavior.SetSelection,
            1: Qgis.SelectBehavior.AddToSelection,
            2: Qgis.SelectBehavior.IntersectSelection,
            3: Qgis.SelectBehavior.RemoveFromSelection,
        }

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        source = self.parameterAsSource(parameters, self.INPUT, context)
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        intersectSource = self.parameterAsSource(parameters, self.INTERSECT, context)
        method = self.parameterAsEnum(parameters, self.METHOD, context)
        de9im = self.parameterAsString(parameters, self.DE9IM, context)
        nFeats = intersectSource.featureCount()
        if nFeats == 0:
            return {}
        if de9im == "FF1FF0102":
            self.algRunner.runSelectByLocation(
                inputLyr=parameters[self.INPUT],
                intersectLyr=parameters[self.INTERSECT],
                context=context,
                feedback=feedback,
                predicate=[2],
                method=self.selectionIdDict[method],
                is_child_algorithm=True,
            )
            return
        nSteps = 4
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        lyrWithId = self.algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT],
            expression="$id",
            fieldType=1,
            fieldName="featid",
            feedback=multiStepFeedback,
            context=context,
            is_child_algorithm=False,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            lyrWithId,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        selectedLyr = self.algRunner.runExtractByLocation(
            inputLyr=lyrWithId,
            intersectLyr=parameters[self.INTERSECT],
            context=context,
            feedback=multiStepFeedback,
            predicate=[2] if de9im == "FF1FF0102" else [0],
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nFeats = selectedLyr.featureCount()
        if nFeats == 0:
            return {}
        selectedSet = set()
        stepSize = 100 / nFeats

        def compute(feat):
            returnSet = set()
            geom = feat.geometry()
            bbox = geom.boundingBox()
            engine = QgsGeometry.createGeometryEngine(geom.constGet())
            engine.prepareGeometry()
            for f in selectedLyr.getFeatures(bbox):
                if multiStepFeedback.isCanceled():
                    return {}
                intersectGeom = f.geometry()
                if intersectGeom.isEmpty() or intersectGeom.isNull():
                    continue
                if engine.relatePattern(intersectGeom.constGet(), de9im):
                    returnSet.add(f["featid"])
            return returnSet

        for current, feat in enumerate(intersectSource.getFeatures()):
            if multiStepFeedback.isCanceled():
                return {}
            selectedSet.update(compute(feat))
            multiStepFeedback.setProgress(current * stepSize)
        layer.selectByIds(list(selectedSet), self.selectionIdDict[method])

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "selectbyde9im"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Select features by DE9IM")

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
        return "DSGTools: Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("SelectByDE9IMAlgorithm", string)

    def createInstance(self):
        return SelectByDE9IMAlgorithm()
