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
                       QgsProcessingException, QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyGapsAndOverlapsInCoverageAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUTLAYERS = 'INPUTLAYERS'
    FRAMELAYER = 'FRAMELAYER'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Coverage Polygon Layers'),
                QgsProcessing.TypeVectorPolygon
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FRAMELAYER,
                self.tr('Frame Layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True
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
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUTLAYERS))
        frameLyr = self.parameterAsVectorLayer(parameters, self.FRAMELAYER, context)
        if frameLyr and frameLyr in inputLyrList:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.FRAMELAYER))
        isMulti = True
        for inputLyr in inputLyrList:
            isMulti &= QgsWkbTypes.isMultiType(int(inputLyr.wkbType()))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Polygon, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(inputLyrList, QgsWkbTypes.Polygon, onlySelected = onlySelected)
        lyr = self.overlayCoverage(coverage, context)
        if frameLyr:
            self.getGapsOfCoverageWithFrame(lyr, frameLyr, context)
        featureList, total = self.getIteratorAndFeatureCount(lyr) #only selected is not applied because we are using an inner layer, not the original ones
        geomDict = self.getGeomDict(featureList, isMulti, feedback, total)
        self.raiseFlags(geomDict, feedback)
        QgsProject.instance().removeMapLayer(lyr)
        return {self.FLAGS: self.flag_id}

    def overlayCoverage(self, coverage, context):
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        parameters = {
            'ainput':coverage,
            'atype':0,
            'binput':coverage,
            'btype':0,
            'operator':0,
            'snap':0,
            '-t':False,
            'output':output,
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
            'GRASS_MIN_AREA_PARAMETER':0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER':0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        x = processing.run('grass7:v.overlay', parameters, context = context)
        lyr = QgsProcessingUtils.mapLayerFromString(x['output'], context)
        return lyr
    
    def getGapsOfCoverageWithFrame(self, coverage, frameLyr, context):
        dissolveParameters = {
            'INPUT' : coverage,
            'FIELD':[],
            'OUTPUT':'memory:'
        }
        dissolveOutput = processing.run('native:dissolve', dissolveParameters, context = context)
        differenceParameters = {
            'INPUT' : frameLyr,
            'OVERLAY' : dissolveOutput['OUTPUT'],
            'OUTPUT':'memory:'
        }
        differenceOutput = processing.run('native:difference', differenceParameters, context = context)
        for feat in differenceOutput['OUTPUT'].getFeatures():
            self.flagFeature(feat.geometry(), self.tr('Gap in coverage with frame'))
    
    def getGeomDict(self, featureList, isMulti, feedback, total):
        geomDict = dict()
        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            if isMulti and not geom.isMultipart():
                geom.convertToMultiType()
            geomKey = geom.asWkb()
            if geomKey not in geomDict:
                geomDict[geomKey] = []
            geomDict[geomKey].append(feat)
            # # Update the progress bar
            attrList = feat.attributes()
            if attrList == len(attrList)*[None]:
                self.flagFeature(geom, self.tr('Gap in coverage layer.'))
            feedback.setProgress(int(current * total)) 
        return geomDict

    def raiseFlags(self, geomDict, feedback):
        for k, v in geomDict.items():
            if feedback.isCanceled():
                break
            if len(v) > 1:
                textList = []
                for feat in v:
                    textList += ['({0},{1})'.format(feat['a_featid'], feat['a_layer'])]
                flagText = self.tr('Overlapping features (id,layer): {0}').format(', '.join(set(textList)))
                self.flagFeature(v[0].geometry(), flagText) 

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifygapsandoverlaps'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Gaps and Overlaps in Coverage Layers')

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
        return QCoreApplication.translate('IdentifyGapsAndOverlapsInCoverageAlgorithm', string)

    def createInstance(self):
        return IdentifyGapsAndOverlapsInCoverageAlgorithm()
