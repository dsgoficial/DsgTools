# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-28
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
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class CleanGeometriesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    MINAREA = "MINAREA"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        param = QgsProcessingParameterDistance(
            self.TOLERANCE,
            self.tr("Snap Radius"),
            parentParameterName=self.INPUT,
            defaultValue=1.0,
        )
        param.setMetadata({"widget_wrapper": {"decimals": 8}})
        self.addParameter(param)

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
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Cleaned original layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        algRunner = AlgRunner()

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        if inputLyr.featureCount() == 0:
            feedback.pushWarning(self.tr("Empty input"))
            return {self.FLAGS: self.flag_id}
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        snap = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        # if snap < 0 and snap != -1:
        #     raise QgsProcessingException(self.invalidParameterError(parameters, self.TOLERANCE))
        minArea = self.parameterAsDouble(parameters, self.MINAREA, context)
        geographicBoundsLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )
        if (
            inputLyr.wkbType() == QgsWkbTypes.PolygonGeometry
            and geographicBoundsLyr is not None
        ):
            raise NotImplementedError(
                self.tr("Spatial restriction not implemented yet for polygon layers")
            )
        if geographicBoundsLyr is None:
            self.cleanGeometries(
                context,
                feedback,
                layerHandler,
                algRunner,
                inputLyr.clone(),
                onlySelected,
                snap,
                minArea,
            )
        else:
            self.cleanGeometriesInsideGeographicBoundary(
                context,
                feedback,
                layerHandler,
                algRunner,
                inputLyr.clone(),
                onlySelected,
                snap,
                minArea,
                geographicBoundsLyr,
            )

        return {self.FLAGS: self.flag_id}

    def cleanGeometries(
        self,
        context,
        feedback,
        layerHandler,
        algRunner,
        inputLyr,
        onlySelected,
        snap,
        minArea,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer..."))
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            [inputLyr],
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Running clean..."))
        cleanedLyr, error = algRunner.runClean(
            auxLyr,
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
            [inputLyr],
            cleanedLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        self.flagIssues(cleanedLyr, error, feedback)

    def cleanGeometriesInsideGeographicBoundary(
        self,
        context,
        feedback,
        layerHandler,
        algRunner,
        inputLyr,
        onlySelected,
        snap,
        minArea,
        geographicBoundsLyr,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Populating temp layer..."))
        inputLyrList = [inputLyr]
        auxLyr = layerHandler.createAndPopulateUnifiedVectorLayer(
            inputLyrList,
            geomType=inputLyr.wkbType(),
            onlySelected=onlySelected,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(1)
        (
            insideLyr,
            outsideLyr,
        ) = layerHandler.prepareAuxLayerForSpatialConstrainedAlgorithm(
            inputLyr=auxLyr,
            geographicBoundaryLyr=geographicBoundsLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Running clean..."))
        cleanedLyr, error = algRunner.runClean(
            insideLyr,
            [algRunner.RMSA, algRunner.Break, algRunner.RmDupl, algRunner.RmDangle],
            context,
            returnError=True,
            snap=snap,
            minArea=minArea,
            feedback=multiStepFeedback,
        )
        cleanedLyr = algRunner.runRenameField(
            inputLayer=cleanedLyr,
            field="featid",
            newName="oldfeatid",
            context=context,
        )
        outsideLyr = algRunner.runRenameField(
            inputLayer=outsideLyr,
            field="featid",
            newName="oldfeatid",
            context=context,
        )
        multiStepFeedback.setCurrentStep(3)
        outputLyr = (
            layerHandler.integrateSpatialConstrainedAlgorithmOutputAndOutsideLayer(
                algOutputLyr=cleanedLyr,
                outsideLyr=outsideLyr,
                tol=snap,
                context=context,
                feedback=multiStepFeedback,
                geographicBoundaryLyr=geographicBoundsLyr,
            )
        )
        outputLyr = algRunner.runRenameField(
            inputLayer=outputLyr,
            field="oldfeatid",
            newName="featid",
            context=context,
        )
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Updating original layer..."))
        layerList = [inputLyr.clone()]
        layerHandler.updateOriginalLayersFromUnifiedLayer(
            layerList,
            outputLyr,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        self.flagIssues(cleanedLyr, error, feedback)

    def flagIssues(self, cleanedLyr, error, feedback):
        overlapDict = dict()
        for feat in cleanedLyr.getFeatures():
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
                    txtList += (
                        [f"""{i["layer"]} (id={i["featid"]})"""]
                        if "featid" in i.attributeMap()
                        else [f"""{i["layer"]} (id={i["oldfeatid"]})"""]
                    )
                txt = ", ".join(txtList)
                self.flagFeature(
                    featList[0].geometry(),
                    self.tr("Features from {0} overlap").format(txt),
                )
            elif len(featList) == 1:
                attrList = featList[0].attributes()
                if attrList == len(attrList) * [None]:
                    self.flagFeature(featList[0].geometry(), self.tr("Gap in layer."))

        if error:
            for feat in error.getFeatures():
                if feedback.isCanceled():
                    break
                self.flagFeature(feat.geometry(), self.tr("Clean error on layer."))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "cleangeometries"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Clean Geometries")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Snap Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Snap Processes"

    def tr(self, string):
        return QCoreApplication.translate("CleanGeometriesAlgorithm", string)

    def createInstance(self):
        return CleanGeometriesAlgorithm()
