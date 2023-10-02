# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-01-16
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

import concurrent.futures
import os
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingParameterNumber,
    QgsProcessingParameterField
)


class SmallHoleRemoverAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    DISSOLVE_OUTPUT = "DISSOLVE_OUTPUT"
    DISSOLVE_ATTRIBUTE_LIST = "DISSOLVE_ATTRIBUTE_LIST"
    MAX_HOLE_AREA_TO_ELIMINATE = "MAX_HOLE_AREA_TO_ELIMINATE"
    OUPUT = "OUPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DISSOLVE_OUTPUT, self.tr("Dissolve Output")
            )
        )


        self.addParameter(
            QgsProcessingParameterField(
                self.DISSOLVE_ATTRIBUTE_LIST,
                self.tr("Fields to consider on dissolve"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
                allowMultiple=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_HOLE_AREA_TO_ELIMINATE,
                self.tr("Max hole area to eliminate"),
                defaultValue=15625,
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUPUT, self.tr("Output"))
        )
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        maxHoleArea = self.parameterAsDouble(parameters, self.MAX_HOLE_AREA_TO_ELIMINATE, context)
        dissolveAttributeList = self.parameterAsFields(
            parameters, self.DISSOLVE_ATTRIBUTE_LIST, context
        )
        algRunner = AlgRunner()
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        dissolveOutput = self.parameterAsBool(parameters, self.DISSOLVE_OUTPUT, context)
        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUPUT,
            context,
            inputLyr.fields(),
            inputLyr.wkbType(),
            inputLyr.sourceCrs(),
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(10, feedback)

        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(self.tr("Building Cache"))
        cacheLyr = algRunner.runAddAutoIncrementalField(
            inputLyr=inputLyr if not onlySelected else \
                QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            context=context,
            feedback=multiStepFeedback
        )
        cacheDict = {feat["featid"]:feat for feat in cacheLyr.getFeatures()}
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.setProgressText(self.tr("Building Spatial Index"))
        algRunner.runCreateSpatialIndex(inputLyr=cacheLyr, context=context, feedback=multiStepFeedback)

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.setProgressText(self.tr("Point on surface layer"))
        pointOnSurfaceLyr = algRunner.runPointOnSurface(
            inputLyr=cacheLyr, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.setProgressText(self.tr("Building Spatial Index on point on surface layer"))
        algRunner.runCreateSpatialIndex(inputLyr=pointOnSurfaceLyr, context=context, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.setProgressText(self.tr("Extracting Donut Holes"))
        _, donutHole = algRunner.runDonutHoleExtractor(
            inputLyr=cacheLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(5)
        multiStepFeedback.setProgressText(self.tr("Submitting to thread"))
        nFeats = donutHole.featureCount()
        if nFeats == 0:
            return {self.OUPUT: output_sink_id}
        stepSize = 100 / nFeats
        futures = set()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        fieldNames = [field.name() for field in inputLyr.fields()]
        def compute(feat):
            outputList = []
            if multiStepFeedback.isCanceled():
                return outputList
            geom = feat.geometry()
            if geom.area() > maxHoleArea:
                return outputList
            bbox = geom.boundingBox()
            for newCandidate in cacheLyr.getFeatures(bbox):
                newCandidateGeom = newCandidate.geometry()
                if newCandidateGeom.equals(geom):
                    for fieldName in fieldNames:
                        newCandidate[fieldName] = feat[fieldName]
                    outputList.append(newCandidate)
                    return outputList
            for candidateFeat in pointOnSurfaceLyr.getFeatures(bbox):
                candidatePointGeom = candidateFeat.geometry()
                if not geom.intersects(candidatePointGeom):
                    continue
                candidateFeat = cacheDict[candidateFeat["featid"]]
                for fieldName in fieldNames:
                    candidateFeat[fieldName] = feat[fieldName]
                outputList.append(candidateFeat)
            return outputList

        cacheLyr.startEditing()
        cacheLyr.beginEditCommand("Updating holes")
        for current, feat in enumerate(donutHole.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(compute, feat))
            multiStepFeedback.setProgress(current * stepSize)

        multiStepFeedback.setCurrentStep(6)
        multiStepFeedback.setProgressText(self.tr("Evaluating Results"))
        cacheLyrDataProvider = cacheLyr.dataProvider()
        indexDict = {fieldName:cacheLyrDataProvider.fields().indexFromName(fieldName) for fieldName in fieldNames}
        def updateFunc(feat):
            featid = cacheDict[feat['featid']].id()
            cacheLyrDataProvider.changeAttributeValues({
                featid: { indexDict[fieldName]:feat[fieldName] for fieldName in fieldNames}
            })
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            results = future.result()
            if results == []:
                continue
            list(map(updateFunc, results))
            # for featToUpdate in future.result():
            # # for featToUpdate in compute(feat):
            #     cacheLyr.updateFeature(featToUpdate)
            multiStepFeedback.setProgress(current * stepSize)
        cacheLyr.endEditCommand()

        multiStepFeedback.setCurrentStep(7)
        if dissolveOutput:
            multiStepFeedback.setProgressText(self.tr("Dissolving Polygons"))
            mergedLyr = algRunner.runDissolve(
                inputLyr=cacheLyr,
                context=context,
                feedback=multiStepFeedback,
                field=dissolveAttributeList,
                is_child_algorithm=True
            )
            multiStepFeedback.setCurrentStep(8)
            mergedLyr = algRunner.runMultipartToSingleParts(
                inputLayer=mergedLyr,
                context=context,
                feedback=multiStepFeedback
            )
        else:
            mergedLyr = cacheLyr
        multiStepFeedback.setCurrentStep(9)
        nFeats = mergedLyr.featureCount()
        if nFeats == 0:
            return {self.OUPUT: output_sink_id}
        stepSize = 100 / nFeats
        multiStepFeedback.setProgressText(self.tr("Building Outputs"))
        for current, feat in enumerate(mergedLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            output_sink.addFeature(feat)
            multiStepFeedback.setProgress(current * stepSize)

        return {self.OUPUT: output_sink_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "smallholeremoveralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Small Hole Remover Algorithm")

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
        return QCoreApplication.translate("SmallHoleRemoverAlgorithm", string)

    def createInstance(self):
        return SmallHoleRemoverAlgorithm()
