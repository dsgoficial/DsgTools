# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-13
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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
import processing, os, requests
from time import sleep
from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QSettings
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProcessingParameterField,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterExpression,
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType)

class SetFreeHandToolParametersAlgorithm(QgsProcessingAlgorithm):
    FREE_HAND_TOLERANCE = 'FREE_HAND_TOLERANCE'
    FREE_HAND_SMOOTH_ITERATIONS = 'FREE_HAND_SMOOTH_ITERATIONS'
    FREE_HAND_SMOOTH_OFFSET = 'FREE_HAND_SMOOTH_OFFSET'
    ALG_ITERATIONS = 'ALG_ITERATIONS'
    UNDO_POINTS = 'UNDO_POINTS'

    QSETTINGS_DICT = {
        'FREE_HAND_TOLERANCE' : 'freeHandTolerance',
        'FREE_HAND_SMOOTH_ITERATIONS' : 'freeHandSmoothIterations',
        'FREE_HAND_SMOOTH_OFFSET' : 'freeHandSmoothOffset',
        'ALG_ITERATIONS' : 'algIterations',
        'UNDO_POINTS' : 'undoPoints'
    }

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FREE_HAND_TOLERANCE,
                self.tr('Free hand tolerance'),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=2
            )
        )
    
    def getValueFromQSettings(self, v):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        value = settings.value(v)
        settings.endGroup()
        return value
    
    def storeParametersInConfig(self, parameters):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        for key, value in parameters.items():
            settings.setValue(self.QSETTINGS_DICT[key], value)
        settings.endGroup()

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'setfreehandtoolparametersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Set Free Hand Tool Parameters')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Environment Setters')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Environment Setters'

    def tr(self, string):
        return QCoreApplication.translate('SetFreeHandToolParametersAlgorithm', string)

    def createInstance(self):
        return SetFreeHandToolParametersAlgorithm()
