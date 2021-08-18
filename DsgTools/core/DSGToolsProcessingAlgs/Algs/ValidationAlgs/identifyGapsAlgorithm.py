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

import processing
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsWkbTypes)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyGapsAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input Polygon Layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    
    def getGapLyr(self, inputLyr, context, multiStepFeedback, onlySelected = False):
        algRunner = AlgRunner()
        multiStepFeedback.setCurrentStep(0)
        dissolvedLyr = algRunner.runDissolve(inputLyr, context, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(1)
        deletedHolesLyr = algRunner.runDeleteHoles(dissolvedLyr, context, feedback=multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        gapLyr = algRunner.runOverlay(deletedHolesLyr, deletedHolesLyr, context, feedback=multiStepFeedback)
        return gapLyr

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        isMulti = QgsWkbTypes.isMultiType(int(inputLyr.wkbType()))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Polygon, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback) 
        lyr = self.getGapLyr(inputLyr, context, multiStepFeedback, onlySelected=onlySelected)
        featureList, total = self.getIteratorAndFeatureCount(lyr) #only selected is not applied because we are using an inner layer, not the original ones
        QgsProject.instance().removeMapLayer(lyr)
        geomDict = dict()

        multiStepFeedback.setCurrentStep(3)
        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            attrList = feat.attributes()
            if attrList == len(attrList)*[None]:
                geom = feat.geometry()
                self.flagFeature(geom, self.tr('Gap in layer {0}.').format(inputLyr.name()))
            # # Update the progress bar
            multiStepFeedback.setProgress(current * total)
        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifygaps'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Gaps')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyGapsAlgorithm', string)

    def createInstance(self):
        return IdentifyGapsAlgorithm()
