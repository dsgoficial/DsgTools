# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton / Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho / @eb.mil.br
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

from qgis.PyQt.QtCore import (QCoreApplication, QVariant)
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterNumber,
                       QgsCoordinateReferenceSystem,
                       QgsGeometry,
                       QgsField,
                       QgsFeature,
                       QgsFields,
                       QgsProcessingParameterMultipleLayers
                       )
from qgis.utils import iface

from .validationAlgorithm import ValidationAlgorithm


class IdentifySmallHolesAlgorithm(ValidationAlgorithm):

    INPUT_LAYER_LIST = 'INPUT_LAYER_LIST'
    MAX_HOLE_SIZE = 'MAX_HOLE_SIZE'
    OUTPUT = 'OUTPUT'


    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                'INPUT_LAYER_LIST',
                self.tr('Input layer(s)'),
                QgsProcessing.TypeVectorPolygon
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                'MAX_HOLE_SIZE',
                self.tr('Tolerance'), 
                type=QgsProcessingParameterNumber.Double, 
                minValue=0)
            )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Flags')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):      
        feedback.setProgressText(self.tr('Searching holes smaller than tolerance'))
        layerList = self.parameterAsLayerList(parameters,'INPUT_LAYER_LIST', context)
        maxSize = self.parameterAsDouble (parameters,'MAX_HOLE_SIZE', context) 
        CRSstr = iface.mapCanvas().mapSettings().destinationCrs().authid()
        CRS = QgsCoordinateReferenceSystem(CRSstr)
        smallRings = []
        listSize = len(layerList)
        progressStep = 100/listSize if listSize else 0
        step = 0
        for step,layer in enumerate(layerList):
            if feedback.isCanceled():
                return {self.OUTPUT: smallRings}
            for feature in layer.getFeatures():
                if not feature.hasGeometry():
                    continue
                for poly in feature.geometry().asMultiPolygon():
                    onlyrings = poly[1:]
                    for ring in onlyrings:
                        newRing = QgsGeometry.fromPolygonXY([ring])
                        print(newRing.area())
                        if newRing.area()<maxSize:
                            smallRings.append(newRing)
            feedback.setProgress( step * progressStep )
        
        if len(smallRings) == 0:
            flagLayer = self.tr(f'Holes smaller than {str(maxSize)} were not found')
            return{self.OUTPUT: flagLayer}
        flagLayer = self.outputLayer(parameters, context, smallRings, CRS, 6)
        return{self.OUTPUT: flagLayer}

    def outputLayer(self, parameters, context, smallRings, CRS, geomType):
        newField = QgsFields()
        newField.append(QgsField('area', QVariant.Double))
        features = smallRings
        (sink, newLayer) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            newField,
            geomType,
            CRS
        )
        for feature in features:
            newFeat = QgsFeature()
            newFeat.setGeometry(feature)
            newFeat.setFields(newField)
            newFeat['area'] = feature.area()
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        
        return newLayer

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifysmallholesalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify small holes')

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
        return QCoreApplication.translate('IdentifySmallHolesAlgorithm', string)

    def createInstance(self):
        return IdentifySmallHolesAlgorithm()
