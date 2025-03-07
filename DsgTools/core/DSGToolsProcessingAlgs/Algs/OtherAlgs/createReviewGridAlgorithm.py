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
    UNIT_WORK_ID = "UNIT_WORK_ID"
    STEP_ID = "STEP_ID"
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

        # Parâmetros avançados
        paramRelatedTask = QgsProcessingParameterNumber(
            self.RELATED_TASK_ID,
            self.tr("Related task id"),
            optional=True,
            type=QgsProcessingParameterNumber.Integer,
        )
        paramRelatedTask.setFlags(
            paramRelatedTask.flags() | QgsProcessingParameterNumber.FlagAdvanced
        )
        self.addParameter(paramRelatedTask)

        paramUnitWork = QgsProcessingParameterNumber(
            self.UNIT_WORK_ID,
            self.tr("Work unit id"),
            optional=True,
            type=QgsProcessingParameterNumber.Integer,
        )
        paramUnitWork.setFlags(
            paramUnitWork.flags() | QgsProcessingParameterNumber.FlagAdvanced
        )
        self.addParameter(paramUnitWork)

        paramStep = QgsProcessingParameterNumber(
            self.STEP_ID,
            self.tr("Step id"),
            optional=True,
            type=QgsProcessingParameterNumber.Integer,
        )
        paramStep.setFlags(
            paramStep.flags() | QgsProcessingParameterNumber.FlagAdvanced
        )
        self.addParameter(paramStep)

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
            inputLyr=grid,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
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
        fields.append(QgsField("unidade_trabalho_id", QVariant.Int))
        fields.append(QgsField("etapa_id", QVariant.Int))
        fields.append(QgsField("data_atualizacao", QVariant.DateTime))
        return fields

    def sortGridAndCreateOutputFetures(
        self, grid, fields, parameters, context, feedback
    ):
        featList = [feat for feat in grid.getFeatures()]
        relatedTaskId = self.parameterAsInt(parameters, self.RELATED_TASK_ID, context)
        unitWorkId = self.parameterAsInt(parameters, self.UNIT_WORK_ID, context)
        stepId = self.parameterAsInt(parameters, self.STEP_ID, context)
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
            if relatedTaskId is not None:
                newFeat["atividade_id"] = relatedTaskId
            if unitWorkId is not None:
                newFeat["unidade_trabalho_id"] = unitWorkId
            if stepId is not None:
                newFeat["etapa_id"] = stepId
            newFeat.setGeometry(feat.geometry())
            outputFeatList.append(newFeat)
            feedback.setProgress(current * stepSize)
        return outputFeatList

    def name(self):
        return "createreviewgridalgorithm"

    def displayName(self):
        return self.tr("Create Review Grid")

    def group(self):
        return self.tr("Grid Algorithms")

    def groupId(self):
        return "DSGTools - Grid Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateReviewGridAlgorithm", string)

    def createInstance(self):
        return CreateReviewGridAlgorithm()
