# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
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
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class TopologicalCleanAlgorithm(ValidationAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    MINAREA = "MINAREA"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr("Polygon Layers"),
                QgsProcessing.TypeVectorPolygon,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        snapParam = QgsProcessingParameterNumber(
            self.TOLERANCE,
            self.tr("Snap radius"),
            minValue=0,
            defaultValue=1,
            type=QgsProcessingParameterNumber.Double,
        )
        snapParam.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(snapParam)

        areaParam = QgsProcessingParameterNumber(
            self.MINAREA,
            self.tr("Minimum area"),
            minValue=0,
            defaultValue=1e-8,
            type=QgsProcessingParameterNumber.Double,
        )
        areaParam.setMetadata({"widget_wrapper": {"decimals": 16}})
        self.addParameter(areaParam)

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
        for layer in inputLyrList:
            if layer.featureCount() > 0:
                geomType = next(layer.getFeatures()).geometry().wkbType()
                break
        else:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUTLAYERS),
                self.tr("Provided layers have no features in it."),
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        minArea = self.parameterAsDouble(parameters, self.MINAREA, context)
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        if geomType == QgsWkbTypes.PolygonGeometry and geographicBoundsLyr is not None:
            raise NotImplementedError(self.tr("Spatial restriction not implemented yet for polygon layers"))
        self.prepareFlagSink(parameters, inputLyrList[0], geomType, context)

        if geographicBoundsLyr is None:
            self.topologicalCleanWithoutGeographicBounds(context, feedback, layerHandler, algRunner, inputLyrList, geomType, onlySelected, snap, minArea)
        else:
            self.topologicalCleanWithGeographicBounds(context, feedback, layerHandler, algRunner, inputLyrList, geographicBoundsLyr, geomType, onlySelected, snap, minArea)

        return {self.INPUTLAYERS: inputLyrList, self.FLAGS: self.flagSink}

    def topologicalCleanWithoutGeographicBounds(self, context, feedback, layerHandler, algRunner, inputLyrList, geomType, onlySelected, snap, minArea):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        # in order to check the topology of all layers as a whole, all features
        # are handled as if they formed a single layer
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=geomType,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Running clean on unified layer..."))
        cleanedCoverage, error = algRunner.runClean(
            coverage,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=minArea,
            feedback=multiStepFeedback,
        )

        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, cleanedCoverage, feedback=multiStepFeedback
        )
        self.flagCoverageIssues(cleanedCoverage, error, feedback)

    def topologicalCleanWithGeographicBounds(self, context, feedback, layerHandler, algRunner, inputLyrList, geographicBoundsLyr, geomType, onlySelected, snap, minArea):
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Building unified layer..."))
        # in order to check the topology of all layers as a whole, all features
        # are handled as if they formed a single layer
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=geomType,
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        renamedAuxLyr = algRunner.runRenameField(
            inputLayer=auxLyr,
            field="featid",
            newName="oldfeatid",
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Applying spatial constraint..."))
        (
            insideLyr,
            outsideLyr,
        ) = layerHandler.prepareAuxLayerForSpatialConstrainedAlgorithm(
            inputLyr=renamedAuxLyr,
            geographicBoundaryLyr=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Running clean on unified layer..."))
        cleanedCoverage, error = algRunner.runClean(
            insideLyr,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=minArea,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(
            self.tr("Integrating results inside and outside geographic bounds...")
        )
        outputLyr = (
            layerHandler.integrateSpatialConstrainedAlgorithmOutputAndOutsideLayer(
                algOutputLyr=cleanedCoverage,
                outsideLyr=outsideLyr,
                tol=snap,
                context=context,
                feedback=multiStepFeedback,
            )
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        renamedOutputLyr = algRunner.runRenameField(
            inputLayer=outputLyr,
            field="oldfeatid",
            newName="featid",
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            inputLyrList, renamedOutputLyr, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if error.featureCount() == 0:
            return
        cleanedCoverage = algRunner.runRenameField(
            inputLayer=cleanedCoverage,
            field="oldfeatid",
            newName="featid",
            context=context,
            feedback=multiStepFeedback,
        )
        self.flagCoverageIssues(cleanedCoverage, error, feedback)
    
    def flagCoverageIssues(self, cleanedCoverage, error, feedback):
        overlapDict = dict()
        for current, feat in enumerate(cleanedCoverage.getFeatures()):
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

        if error:
            for feat in error.getFeatures():
                if feedback.isCanceled():
                    break
                self.flagFeature(
                    feat.geometry(), self.tr("Clean error on unified layer.")
                )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "topologicalclean"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Topological Clean Polygons")

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
        return QCoreApplication.translate("TopologicalCleanAlgorithm", string)

    def createInstance(self):
        return TopologicalCleanAlgorithm()
