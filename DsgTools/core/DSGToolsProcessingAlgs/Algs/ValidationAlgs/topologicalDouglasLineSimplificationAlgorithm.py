# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingException,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class TopologicalDouglasPeuckerLineSimplificationAlgorithm(ValidationAlgorithm):
    """
    Implements a Douglas Peucker algorithm to simplify lines taking into
    consideration the topological behavior for lines between layers.
    """

    INPUTLAYERS = "INPUTLAYERS"
    SELECTED = "SELECTED"
    SNAP = "SNAP"
    DOUGLASPARAMETER = "DOUGLASPARAMETER"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr("Linestring Layers"),
                QgsProcessing.TypeVectorLine,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DOUGLASPARAMETER,
                self.tr("Douglas Deucker threshold"),
                minValue=0,
                defaultValue=2,
                type=QgsProcessingParameterNumber.Double,
            )
        )
        param = QgsProcessingParameterNumber(
            self.SNAP,
            self.tr("Snap radius"),
            minValue=0,
            defaultValue=1,
            type=QgsProcessingParameterNumber.Double,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Bounds Layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
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
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList is None or inputLyrList == []:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUTLAYERS)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.SNAP, context)
        threshold = self.parameterAsDouble(parameters, self.DOUGLASPARAMETER, context)
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        self.prepareFlagSink(
            parameters, inputLyrList[0], QgsWkbTypes.MultiLineString, context
        )

        if geographicBoundsLyr is None:
            self.runTopologicalDouglasWithoutGeographicBounds(
                context,
                feedback,
                layerHandler,
                algRunner,
                inputLyrList,
                onlySelected,
                snap,
                threshold,
            )
        else:
            self.runTopologicalDouglasWithGeographicBounds(
                context,
                feedback,
                layerHandler,
                algRunner,
                inputLyrList,
                geographicBoundsLyr,
                onlySelected,
                snap,
                threshold,
            )

        return {self.FLAGS: self.flag_id}

    def runTopologicalDouglasWithoutGeographicBounds(
        self,
        context,
        feedback,
        layerHandler,
        algRunner,
        inputLyrList,
        onlySelected,
        snap,
        threshold,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Running clean..."))
        cleanedLyr, error = algRunner.runClean(
            coverage,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=1e-10,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(
            self.tr("Running douglas peucker on unified layer...")
        )
        simplifiedCoverage, error = algRunner.runDouglasSimplification(
            cleanedLyr,
            threshold,
            context,
            returnError=True,
            snap=snap,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr("Merging lines..."))
        merged = algRunner.runDissolve(
            inputLyr=simplifiedCoverage,
            context=context,
            field=["featid", "layer"],
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList,
            merged,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )

        multiStepFeedback.setCurrentStep(5)
        self.flagCoverageIssues(simplifiedCoverage, error, feedback)

    def runTopologicalDouglasWithGeographicBounds(
        self,
        context,
        feedback,
        layerHandler,
        algRunner,
        inputLyrList,
        geographicBoundsLyr,
        onlySelected,
        snap,
        threshold,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=QgsWkbTypes.MultiLineString,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Applying spatial constraint..."))
        (
            insideLyr,
            outsideLyr,
        ) = layerHandler.prepareAuxLayerForSpatialConstrainedAlgorithm(
            inputLyr=auxLyr,
            geographicBoundaryLyr=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running clean..."))
        cleanedLyr, error = algRunner.runClean(
            insideLyr,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=1e-10,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Running douglas peucker on unified layer...")
        )
        simplifiedCoverage, error = algRunner.runDouglasSimplification(
            cleanedLyr,
            threshold,
            context,
            returnError=True,
            snap=snap,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Merging lines..."))
        merged = algRunner.runDissolve(
            inputLyr=simplifiedCoverage,
            context=context,
            field=["featid", "layer"],
            feedback=multiStepFeedback,
        )

        renamedMerged = algRunner.runRenameField(
            inputLayer=merged,
            field="featid",
            newName="oldfeatid",
            context=context,
        )

        renamedOutsideLyr = algRunner.runRenameField(
            inputLayer=outsideLyr,
            field="featid",
            newName="oldfeatid",
            context=context,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Integrating results inside and outside geographic bounds...")
        )
        outputLyr = (
            layerHandler.integrateSpatialConstrainedAlgorithmOutputAndOutsideLayer(
                algOutputLyr=renamedMerged,
                outsideLyr=renamedOutsideLyr,
                tol=snap,
                context=context,
                feedback=multiStepFeedback,
                geographicBoundaryLyr=geographicBoundsLyr,
            )
        )
        renamedOutputLyr = algRunner.runRenameField(
            inputLayer=outputLyr,
            field="oldfeatid",
            newName="featid",
            context=context,
        )

        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList,
            renamedOutputLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )

        multiStepFeedback.setCurrentStep(5)
        self.flagCoverageIssues(simplifiedCoverage, error, feedback)

    def flagCoverageIssues(self, cleanedCoverage, error, feedback):
        """
        From lines, this method grabs its overlaps.
        """
        overlapDict = dict()
        for feat in cleanedCoverage.getFeatures():
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            geomKey = geom.asWkb()
            if geomKey not in overlapDict:
                overlapDict[geomKey] = []
            overlapDict[geomKey].append(feat)
        for geomKey, featList in overlapDict.items():
            if feedback.isCanceled():
                break
            if len(featList) > 1:
                txtList = []
                for i in featList:
                    txtList += ["{0} (id={1})".format(i["layer"], i["featid"])]
                txt = ", ".join(txtList)
                self.flagFeature(
                    featList[0].geometry(),
                    self.tr("Features from {0} overlap").format(txt),
                )
            elif len(featList) == 1:
                attrList = featList[0].attributes()
                if attrList == len(attrList) * [None]:
                    self.flagFeature(
                        featList[0].geometry(), self.tr("Gap in coverage.")
                    )

        if not error:
            return
        for feat in error.getFeatures():
            if feedback.isCanceled():
                break
            self.flagFeature(feat.geometry(), self.tr("Clean error on coverage."))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "topologicaldouglaspeuckerlinesimplification"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Topological Douglas Peucker Line Simplification")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Topological Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Topological Processes"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate(
            "TopologicalDouglasPeuckerLineSimplificationAlgorithm", string
        )

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return TopologicalDouglasPeuckerLineSimplificationAlgorithm()
