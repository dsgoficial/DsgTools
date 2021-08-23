# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os
from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.Qt import QVariant
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
                       QgsProcessingParameterType,
                       QgsProcessingParameterCrs,
                       QgsCoordinateTransform,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsField,
                       QgsFields,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterString)

class MatchAndApplyQmlStylesToLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    QML_FOLDER = 'QML_FOLDER'
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

        self.addParameter(
            QgsProcessingParameterFile(
                self.QML_FOLDER,
                self.tr('Input QML Folder'),
                behavior = QgsProcessingParameterFile.Folder
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

        This process matches the layer name to the qml name.
        """
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        inputDirectory = self.parameterAsFile(
            parameters,
            self.QML_FOLDER,
            context
        )
        listSize = len(inputLyrList)
        progressStep = 100/listSize if listSize else 0
        notSuccessfulList = []
        qmlDict = self.buildQmlDict(inputDirectory)
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            if lyr.name() in qmlDict:
                lyr.loadNamedStyle(qmlDict[lyr.name()], True)
                lyr.triggerRepaint()
            feedback.setProgress(current*progressStep)

        return {self.OUTPUT: [i.id() for i in inputLyrList]}
    
    def buildQmlDict(self, inputDir):
        """
        Builds a dict with the format 
        {'fileName':'filePath'}
        """
        qmlDict = dict()
        for fileNameWithExtension in os.listdir(inputDir):
            if '.qml' not in fileNameWithExtension:
                continue
            fileName = fileNameWithExtension.split('.')[0]
            qmlDict[fileName] = os.path.join(inputDir, fileNameWithExtension)
        return qmlDict


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'matchandapplyqmlstylestolayersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Match and Apply QML Styles to Layers')

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
        return QCoreApplication.translate('MatchAndApplyQmlStylesToLayersAlgorithm', string)

    def createInstance(self):
        return MatchAndApplyQmlStylesToLayersAlgorithm()