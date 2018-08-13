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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from .validationAlgorithm import ValidationAlgorithm

from PyQt5.QtCore import QCoreApplication
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
                       QgsProcessingUtils)

class IdentifyDanglesAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    LINEFILTERLAYERS = 'LINEFILTERLAYERS'
    POLYGONFILTERLAYERS = 'POLYGONFILTERLAYERS'
    TYPE = 'TYPE'
    IGNOREINNER = 'IGNOREINNER'
    FLAGS = 'FLAGS'
    

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
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
                self.tr('Search radius'),
                minValue=0,
                defaultValue=2
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.LINEFILTERLAYERS,
                self.tr('Linestring Filter Layers'),
                QgsProcessing.TypeVectorLine,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.POLYGONFILTERLAYERS,
                self.tr('Polygon Filter Layers'),
                QgsProcessing.TypeVectorPolygon,
                optional = True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.TYPE,
                self.tr('Ignore dangle on unsegmented lines')
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.IGNOREINNER,
                self.tr('Ignore search radius on inner layer search')
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

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        lineFilterLyrList = self.parameterAsLayerList(parameters, self.LINEFILTERLAYERS, context)
        polygonFilterLyrList = self.parameterAsLayerList(parameters, self.POLYGONFILTERLAYERS, context)
        ignoreNotSplit = self.parameterAsBool(parameters, self.TYPE, context)
        ignoreInner = self.parameterAsBool(parameters, self.IGNOREINNER, context)
        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)

        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr)
        endVerticesDict = self.buildInitialAndEndPointDict(featureList, 0.25*total, feedback)
        #search for dangles candidates
        pointList = self.searchDanglesOnPointDict(endVerticesDict, feedback, progressDelta=25)
        #build filter layer
        filterLayer = self.buildFilterLayer(lineFilterLyrList, polygonFilterLyrList, context, feedback, onlySelected=onlySelected)
        delta = 20 if not ignoreInner else 40
        #filter pointList with filterLayer
        if filterLayer:
            filteredPointList = self.filterPointListWithFilterLayer(pointList, filterLayer, searchRadius, feedback, progressDelta = delta)
        else:
            filteredPointList = pointList
            feedback.setProgress(feedback.progress()+delta)
        #filter with own layer
        if not ignoreInner: #True when looking for dangles on contour lines
            filteredPointList = self.filterPointListWithFilterLayer(filteredPointList, inputLyr, searchRadius, feedback, isRefLyr = True, ignoreNotSplit = ignoreNotSplit, progressDelta=20)
        #build flag list with filtered points
        if filteredPointList:
            currentValue = feedback.progress()
            currentTotal = 10/len(filteredPointList)
            for current, point in enumerate(filteredPointList):
                if feedback.isCanceled():
                    break
                self.flagFeature(QgsGeometry.fromPointXY(point), self.tr('Dangle on {0}').format(inputLyr.name()))
                feedback.setProgress(currentValue + int(current*currentTotal))      
        feedback.setProgress(100)
        return {self.FLAGS: self.flagSink}