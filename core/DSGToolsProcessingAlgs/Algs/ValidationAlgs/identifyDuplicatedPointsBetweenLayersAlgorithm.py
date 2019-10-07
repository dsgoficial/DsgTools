# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-06-08
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

from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyDuplicatedPointsBetweenLayersAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUTLAYERS = 'INPUTLAYERS'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Point Layers'),
                QgsProcessing.TypeVectorPoint
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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUTLAYERS))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Point, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        geomDict = dict()
        multiStepFeedback = QgsProcessingMultiStepFeedback(len(inputLyrList)+1, feedback)
        for currentLyrIdx, lyr in enumerate(inputLyrList):
            multiStepFeedback.setCurrentStep(currentLyrIdx)
            featIterator, total = self.getIteratorAndFeatureCount(lyr, onlySelected=onlySelected)
            size = 100/total if total else 0
            lyrName = lyr.name()      
            for current, feat in enumerate(featIterator):
                # Stop the algorithm if cancel button has been clicked
                if multiStepFeedback.isCanceled():
                    break
                geom = feat.geometry()
                geomKey = geom.asWkb()
                if geomKey not in geomDict:
                    geomDict[geomKey] = []
                geomDict[geomKey].append({'feat':feat, 'layerName':lyrName})
                # # Update the progress bar
                multiStepFeedback.setProgress(current * size)
        for v in geomDict.values():
            if multiStepFeedback.isCanceled():
                break
            if len(v) > 1:
                flagStrList = ['{lyrName} (id={id})'.format(lyrName=featDict['layerName'], id=featDict['feat'].id()) for featDict in v]
                flagStr = ', '.join(flagStrList)
                flagText = self.tr('Features from coverage with same geometry: {0}.').format(flagStr)
                self.flagFeature(v[0]['feat'].geometry(), flagText)

        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyduplicatedpointsoncoverage'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Duplicated Points Between Layers')

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
        return QCoreApplication.translate('IdentifyDuplicatedPointsBetweenLayersAlgorithm', string)

    def createInstance(self):
        return IdentifyDuplicatedPointsBetweenLayersAlgorithm()
