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

import processing
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyOutOfBoundsAnglesInCoverageAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUTLAYERS = 'INPUTLAYERS'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Input layer'),
                QgsProcessing.TypeVectorLine
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Minimum angle'),
                minValue=0,
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )
    
    def runIdentifyOutOfBoundsAngles(self, lyr, onlySelected, tol, context):
        parameters = {
                'INPUT': lyr,
                'SELECTED' : onlySelected,
                'TOLERANCE' : tol,
                'FLAGS' : 'memory:'
            }
        output = processing.run('dsgtools:identifyoutofboundsangles', parameters, context = context)
        self.flagFeaturesFromProcessOutput(output)
    
    def cleanCoverage(self, coverage, context):
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        error = QgsProcessingUtils.generateTempFilename('error.shp')
        parameters = {
            'input':coverage,
            'type':[0,1,2,3,4,5,6],
            'tool':[0,6],
            'threshold':'-1', 
            '-b':False, 
            '-c':True, 
            'output' : output, 
            'error': error, 
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        x = processing.run('grass7:v.clean', parameters, context = context)
        lyr = QgsProcessingUtils.mapLayerFromString(x['output'], context)
        return lyr

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUTLAYERS))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Point, context)
        for lyr in inputLyrList:
            if feedback.isCanceled():
                break
            self.runIdentifyOutOfBoundsAngles(lyr, onlySelected, tol, context)
        epsg = inputLyrList[0].crs().authid().split(':')[-1]
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(inputLyrList, QgsWkbTypes.Point, epsg, onlySelected = onlySelected)
        cleanedCoverage = self.cleanCoverage(coverage, context)
        segmentDict = self.geometryHandler.getSegmentDict(cleanedCoverage)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        # featureList, total = self.getIteratorAndFeatureCount(inputLyr)           

        # for current, feat in enumerate(featureList):
        #     # Stop the algorithm if cancel button has been clicked
        #     if feedback.isCanceled():
        #         break
        #     outOfBoundsList = geometryHandler.getOutOfBoundsAngle(feat, tol)
        #     if outOfBoundsList:
        #         for item in outOfBoundsList:
        #             flagText = self.tr('Feature from layer {0} with id={1} has angle of value {2} degrees, which is lesser than the tolerance of {3} degrees.').format(inputLyr.name(), item['feat_id'], item['angle'], tol)
        #             self.flagFeature(item['geom'], flagText)      
        #     # Update the progress bar
        #     feedback.setProgress(int(current * total))

        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyoutofboundsanglesincoverage'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Out Of Bounds Angles in Coverage')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyOutOfBoundsAnglesInCoverageAlgorithm', string)

    def createInstance(self):
        return IdentifyOutOfBoundsAnglesInCoverageAlgorithm()
