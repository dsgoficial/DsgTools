# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-12-26
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import json

from qgis.PyQt.Qt import QVariant
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterEnum,
    QgsFeatureSink,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsField,
    QgsWkbTypes,
)

from DsgTools.tests.test_ValidationAlgorithms import Tester
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler


class MultipleOutputUnitTestAlgorithm(QgsProcessingAlgorithm):
    __description__ = (
        """Runs unit tests for a set of DSGTools algorithms that"""
        """has single output - in-place modified or otherwise."""
    )
    AVAILABLE_ALGS = [
        "dsgtools:unbuildpolygonsalgorithm",
        "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm",
    ]
    INPUT_ALGS = "INPUT_ALGS"
    OUTPUT = "OUTPUT"

    def __init__(self):
        super(MultipleOutputUnitTestAlgorithm, self).__init__()

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_ALGS,
                self.tr("Algorithms to be tested"),
                options=self.AVAILABLE_ALGS,
                optional=False,
                allowMultiple=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr("DSGTools Multiple Output Algorithms Unit Tests")
            )
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised
        (e.g. must be ASCII). The name should be unique within each provider.
        Names should contain lowercase alphanumeric characters only and no
        spaces or other formatting characters.
        """
        return "multipleoutputunittest"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Multiple Output Algorithms Unit Test")

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
        return QCoreApplication.translate("MultipleOutputUnitTestAlgorithm", string)

    def createInstance(self):
        """
        Gets a new instance of algotithm object.
        """
        return MultipleOutputUnitTestAlgorithm()

    def getFields(self):
        """
        Gets all fields for output layer.
        """
        fields = QgsFields()
        fields.append(QgsField("algorithm", QVariant.String))
        fields.append(QgsField("tests_output", QVariant.String))
        fields.append(QgsField("status", QVariant.String))
        return fields

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algsOutput, dest_id = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            self.getFields(),
            QgsWkbTypes.NoGeometry,
            QgsCoordinateReferenceSystem("EPSG:4326"),
        )
        tester = Tester()
        featureHandler = FeatureHandler()
        fields = self.getFields()
        feats = set()
        algIndexes = self.parameterAsEnums(parameters, self.INPUT_ALGS, context)
        size = len(algIndexes)
        failCount = 0
        totalProgress = 100 / size if size else 0
        feedback.setProgress(0)
        for currentStep, algIdx in enumerate(algIndexes):
            if feedback.isCanceled():
                break
            alg = self.AVAILABLE_ALGS[algIdx]
            feedback.pushInfo(self.tr("Testing {alg}'s...").format(alg=alg))
            # decided not to pass feedback to not pollute this alg's log
            msg = tester.testAlg(
                alg,
                multipleOutputs=True,
                attributeBlackList=["path"],
                addControlKey=True,
                context=context,
            )  # , feedback=feedback, context=context)
            status = self.tr("Failed") if msg else self.tr("Passed")
            pushMethod = feedback.reportError if msg else feedback.pushDebugInfo
            failCount += 1 if msg else 0
            msg = msg or self.tr("All tests for {alg} are OK.").format(alg=alg)
            pushMethod("{msg}\n".format(msg=msg))
            feats.add(
                featureHandler.createFeatureFromLayer(
                    algsOutput,
                    attributes={
                        "algorithm": alg,
                        "tests_output": msg,
                        "status": status,
                    },
                    fields=fields,
                )
            )
            feedback.setProgress(currentStep * totalProgress)
        algsOutput.addFeatures(feats, QgsFeatureSink.FastInsert)
        if failCount:
            feedback.reportError(
                self.tr("{0} algorithms failed their unit tests.").format(failCount)
            )
        else:
            feedback.pushDebugInfo(self.tr("All algorithms passed their unit tests."))
        return {self.OUTPUT: dest_id}
