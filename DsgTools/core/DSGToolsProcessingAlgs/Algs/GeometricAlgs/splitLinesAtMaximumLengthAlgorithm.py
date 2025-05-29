# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-24
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsGeometry,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingException,
    QgsDistanceArea,
    QgsPoint,
    QgsPointXY,
    QgsProcessingMultiStepFeedback,
    QgsProcessingContext,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class SplitLinesAtMaximumLengthAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm splits lines based on a maximum length threshold.
    Special handling for closed lines shorter than the threshold - these are split into two parts.
    """

    # Constants used to refer to parameters and outputs
    INPUT = "INPUT"
    MAX_LENGTH = "MAX_LENGTH"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input line layer"), [QgsProcessing.TypeVectorLine]
            )
        )
        param = QgsProcessingParameterDistance(
            self.MAX_LENGTH,
            self.tr("Maximum length"),
            minValue=0,
            parentParameterName=self.INPUT,
            defaultValue=0.001,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Split lines"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()

        source = self.parameterAsSource(parameters, self.INPUT, context)
        max_length = self.parameterAsDouble(parameters, self.MAX_LENGTH, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs(),
        )

        multiStepFeedback = QgsProcessingMultiStepFeedback(10, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        feedback.pushInfo("Extracting closed lines...")
        closed_lines, open_lines = algRunner.runFilterExpressionWithFailOutput(
            inputLyr=parameters[self.INPUT],
            expression="is_closed($geometry)",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        sinkLambda = lambda x: sink.addFeature(x, QgsFeatureSink.FastInsert)

        if open_lines.featureCount() > 0:
            feedback.pushInfo(f"Processing {open_lines.featureCount()} open lines...")
            split_open_lines = algRunner.runSplitLinesByLength(
                inputLayer=open_lines,
                length=max_length,
                context=context,
                feedback=feedback,
            )
            list(map(sinkLambda, split_open_lines.getFeatures()))
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)

        # Process closed lines
        if closed_lines.featureCount() > 0:
            multiStepFeedback.pushInfo(
                f"Processing {closed_lines.featureCount()} closed lines..."
            )

            # Process closed lines one by one to determine length correctly
            total = (
                100.0 / closed_lines.featureCount()
                if closed_lines.featureCount()
                else 0
            )
            localContext = QgsProcessingContext()
            for current, feature in enumerate(closed_lines.getFeatures()):
                if multiStepFeedback.isCanceled():
                    break

                multiStepFeedback.setProgress(int(current * total))
                geom = feature.geometry()
                line_length = geom.length()
                if line_length > max_length:
                    temp_layer = algRunner.runFilterExpression(
                        inputLyr=closed_lines,
                        expression=f"$id = {feature.id()}",
                        context=localContext,
                    )

                    split_result = algRunner.runSplitLinesByLength(
                        inputLayer=temp_layer,
                        length=max_length,
                        context=localContext,
                    )

                    list(map(sinkLambda, split_result.getFeatures()))
                else:
                    vertices = (
                        geom.asMultiPolyline()[0]
                        if geom.isMultipart()
                        else geom.asPolyline()
                    )
                    if len(vertices) < 4:
                        sink.addFeature(feature, QgsFeatureSink.FastInsert)
                        continue

                    # Split at approximately midway point
                    mid_idx = len(vertices) // 2

                    # Create two segments
                    part1 = vertices[: mid_idx + 1]  # First half including midpoint
                    part2 = vertices[
                        mid_idx:
                    ]  # Second half including midpoint (to end/start)

                    # Create features for each part
                    feat1 = QgsFeature(feature.fields())
                    feat1.setAttributes(feature.attributes())
                    feat1.setGeometry(QgsGeometry.fromPolylineXY(part1))
                    sink.addFeature(feat1, QgsFeatureSink.FastInsert)

                    feat2 = QgsFeature(feature.fields())
                    feat2.setAttributes(feature.attributes())
                    feat2.setGeometry(QgsGeometry.fromPolylineXY(part2))
                    sink.addFeature(feat2, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return SplitLinesAtMaximumLengthAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return "splitlinesatmaximumlengthalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr("Split Lines with Maximum Length, splitting closed lines")

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
        """
        Returns a short helper string for the algorithm.
        """
        return self.tr(
            """This algorithm splits lines based on maximum length.
        If the line is closed (a ring) and shorter than the maximum length, it will be split in half.
        If the line is closed and longer than the maximum length, or if the line is open,
        it will be split into parts no longer than the maximum length.
        All calculations are performed in the source CRS units."""
        )
