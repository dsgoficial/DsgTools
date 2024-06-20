# -*- coding: utf-8 -*-
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

from itertools import islice
from collections import deque
import os
from typing import Optional

import numpy as np
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
import concurrent.futures

from qgis.core import (
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
)
from qgis.PyQt.QtCore import QCoreApplication


class SetLineOrientation(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    ORIENTATION = "ORIENTATION"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input"), [QgsProcessing.TypeVectorLine]
            )
        )

        self.modes = [
            self.tr("Clockwise"),
            self.tr("Counterclockwise"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.ORIENTATION,
                self.tr("Orientation"),
                options=self.modes,
                defaultValue=0,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        orientation = self.parameterAsEnum(parameters, self.ORIENTATION, context)
        ccw = orientation == 1
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        nFeats = inputSource.featureCount()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            inputSource.fields(),
            inputSource.wkbType(),
            inputSource.sourceCrs(),
        )
        self.algRunner = AlgRunner()
        if nFeats == 0:
            return {"OUTPUT": dest_id}
        stepSize = 100 / nFeats
        featDict = dict()
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)

        def compute(feat):
            if not should_flip(feat.geometry(), ccw=ccw):
                return None
            return feat

        for current, feat in enumerate(inputSource.getFeatures()):
            if multiStepFeedback.isCanceled():
                return {"OUTPUT": dest_id}
            futures.add(pool.submit(compute, feat))
            multiStepFeedback.setProgress(current * stepSize)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                return {"OUTPUT": dest_id}
            feat = future.result()
            if feat is None:
                continue
            featDict[feat.id()] = feat
            multiStepFeedback.setProgress(current * stepSize)
        if featDict == dict():
            sink.addFeatures(inputSource.getFeatures())
            return {"OUTPUT": dest_id}
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        cacheLyr = self.algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        expression = f"{tuple(featDict.keys())}".replace(",)", ")")
        selectedFeatures = self.algRunner.runFilterExpression(
            inputLyr=cacheLyr,
            expression=f"featid in {expression}",
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        flippedFeatures = self.algRunner.runReverseLineDirection(
            inputLayer=selectedFeatures, context=context, feedback=multiStepFeedback
        )
        flippedDict = {feat["featid"]: feat for feat in flippedFeatures.getFeatures()}
        if len(flippedFeatures) == 0:
            return {"OUTPUT": dest_id}
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)

        for current, feat in enumerate(inputSource.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            featToAdd = feat if feat.id() not in flippedDict else flippedDict[feat.id()]
            sink.addFeature(featToAdd)
            multiStepFeedback.setProgress(current * stepSize)

        return {"OUTPUT": dest_id}

    def tr(self, string):
        return QCoreApplication.translate("SetLineOrientation", string)

    def createInstance(self):
        return SetLineOrientation()

    def name(self):
        return "setlineorientation"

    def displayName(self):
        return self.tr("Set Line Orientation")

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

    def shortHelpString(self):
        return self.tr("The algorithm sets the line orientation")


def should_flip(geom: QgsGeometry, ccw: Optional[bool] = True) -> bool:
    vertexList = list(geom.vertices())
    if vertexList[0] == vertexList[-1]:
        vertexList.pop(-1)
    if len(vertexList) == 2:
        p0, p1 = vertexList
        a = [p0.x(), p0.y(), 0]
        b = [p1.x(), p1.y(), 0]
        prod = np.cross(a, b)
        return prod[-1] > 0 if ccw else prod[-1] < 0
    z = 0
    for p0, p1, p2 in sliding_window_iter(vertexList, 3):
        a = [p1.x() - p0.x(), p1.y() - p0.y(), 0]
        b = [p2.x() - p1.x(), p2.y() - p1.y(), 0]
        z += np.sign(np.cross(a, b)[-1])
    return z > 0 if not ccw else z < 0


def sliding_window_iter(iterable, size):
    """..."""
    iterable = iter(iterable)
    window = deque(islice(iterable, size), maxlen=size)
    for item in iterable:
        yield tuple(window)
        window.append(item)
    if window:
        # needed because if iterable was already empty before the `for`,
        # then the window would be yielded twice.
        yield tuple(window)
