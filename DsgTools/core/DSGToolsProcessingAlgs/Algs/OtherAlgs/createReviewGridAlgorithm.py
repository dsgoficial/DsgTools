# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-11
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
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
)
from qgis.PyQt.Qt import QVariant

from ...algRunner import AlgRunner


class CreateReviewGridAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    RELATED_TASK_ID = "RELATED_TASK_ID"
    X_GRID_SIZE = "X_GRID_SIZE"
    Y_GRID_SIZE = "Y_GRID_SIZE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input Polygon Layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.X_GRID_SIZE,
                self.tr("Grid size on x-axis"),
                defaultValue=0.005,
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.Y_GRID_SIZE,
                self.tr("Grid size on y-axis"),
                defaultValue=0.005,
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.RELATED_TASK_ID,
                self.tr("Related task id"),
                optional=True,
                type=QgsProcessingParameterNumber.Integer,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr("Created Review Grid")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        if inputSource is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        fields = self.getOutputFields()

        xGridSize = self.parameterAsDouble(parameters, self.X_GRID_SIZE, context)
        yGridSize = self.parameterAsDouble(parameters, self.Y_GRID_SIZE, context)
        (output_sink, output_sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            inputSource.sourceCrs(),
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        grid = algRunner.runCreateGrid(
            extent=inputSource.sourceExtent(),
            crs=inputSource.sourceCrs(),
            hSpacing=xGridSize,
            vSpacing=yGridSize,
            feedback=multiStepFeedback,
            context=context,
        )
        multiStepFeedback.setCurrentStep(1)
        algRunner.runCreateSpatialIndex(
            inputLyr=grid, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        filteredGrid = algRunner.runExtractByLocation(
            inputLyr=grid,
            intersectLyr=parameters[self.INPUT],
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(3)
        sortedFeatures = self.sortGridAndCreateOutputFetures(
            filteredGrid, fields, parameters, context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(4)
        list(
            map(
                lambda x: output_sink.addFeature(x, QgsFeatureSink.FastInsert),
                sortedFeatures,
            )
        )

        return {"OUTPUT": output_sink_id}

    def getOutputFields(self):
        fields = QgsFields()
        fields.append(QgsField("rank", QVariant.Int))
        fields.append(QgsField("visited", QVariant.Bool))
        fields.append(QgsField("atividade_id", QVariant.Int))
        return fields

    def sortGridAndCreateOutputFetures(
        self, grid, fields, parameters, context, feedback
    ):
        featList = [feat for feat in grid.getFeatures()]
        relatedTaskId = self.parameterAsInt(parameters, self.RELATED_TASK_ID, context)
        outputFeatList = []
        nSteps = len(featList)
        if nSteps == 0:
            return outputFeatList
        stepSize = 100 / nSteps
        for current, feat in enumerate(
            sorted(
                sorted(
                    featList,
                    key=lambda feat: feat.geometry().vertexAt(0).x(),
                    reverse=False,
                ),
                key=lambda feat: feat.geometry().vertexAt(0).y(),
                reverse=True,
            )
        ):
            if feedback.isCanceled():
                break
            newFeat = QgsFeature(fields)
            newFeat["visited"] = False
            newFeat["rank"] = current
            newFeat["atividade_id"] = relatedTaskId
            newFeat.setGeometry(feat.geometry())
            outputFeatList.append(newFeat)
            feedback.setProgress(current * stepSize)
        return outputFeatList

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "createreviewgridalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Create Review Grid")

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
        return QCoreApplication.translate("CreateReviewGridAlgorithm", string)

    def createInstance(self):
        return CreateReviewGridAlgorithm()
