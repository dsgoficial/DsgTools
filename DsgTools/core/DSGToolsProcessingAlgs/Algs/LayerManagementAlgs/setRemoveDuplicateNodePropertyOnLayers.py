# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-22
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
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingOutputMultipleLayers)

class SetRemoveDuplicateNodePropertyOnLayers(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    OUTPUT = 'OUTPUT'
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input Layers'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Original layers with measure column')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            lyr.geometryOptions().setRemoveDuplicateNodes(True)
            feedback.setProgress(current * stepSize)

        return {self.OUTPUT: [lyr.id() for lyr in inputLyrList]}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'setremoveduplicatenodepropertyonlayers'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Set Remove Duplicate Node Property On Layers')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('SetRemoveDuplicateNodePropertyOnLayers', string)

    def createInstance(self):
        return SetRemoveDuplicateNodePropertyOnLayers()
