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

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

from PyQt5.QtCore import QCoreApplication
import processing
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterField,
                       QgsProcessingParameterBoolean,
                       QgsWkbTypes,
                       QgsProcessingUtils,
                       QgsProject)

class UpdateOriginalLayerAlgorithm(ValidationAlgorithm):
    ORIGINALLAYER = 'ORIGINALLAYER'
    PROCESSOUTPUTLAYER = 'PROCESSOUTPUTLAYER'
    CONTROLID = 'CONTROLID'
    KEEPFEATURES = 'KEEPFEATURES'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.ORIGINALLAYER,
                self.tr('Original Layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CONTROLID,
                self.tr('Control ID'),
                parentLayerParameterName=self.ORIGINALLAYER
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PROCESSOUTPUTLAYER,
                self.tr('Update Layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.KEEPFEATURES,
                self.tr('Keep features from input that are not in update layer')
            )
        )


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        originalLyr = self.parameterAsVectorLayer(parameters, self.ORIGINALLAYER, context)
        if originalLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.ORIGINALLAYER))

        processOutputLyr = self.parameterAsVectorLayer(parameters, self.PROCESSOUTPUTLAYER, context)
        if processOutputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PROCESSOUTPUTLAYER))
        
        controlId = self.parameterAsFields(parameters, self.CONTROLID, context)
        keepFeatures = self.parameterAsBool(parameters, self.KEEPFEATURES, context)

        layerHandler.updateOriginalLayer(originalLyr, processOutputLyr, field=str(controlId[0]), feedback=feedback, keepFeatures = keepFeatures)
        return {self.ORIGINALLAYER:originalLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'updatelayer'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Update Layer')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Other Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Other Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('UpdateOriginalLayerAlgorithm', string)

    def createInstance(self):
        return UpdateOriginalLayerAlgorithm()
