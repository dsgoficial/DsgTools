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

from collections import defaultdict

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyDuplicatedGeometriesAlgorithm(ValidationAlgorithm):
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
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry ]
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

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        isMulti = QgsWkbTypes.isMultiType(int(inputLyr.wkbType()))
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr, onlySelected=onlySelected)
        geomDict = defaultdict(set)
        featureList = list(featureList)
        for idx1, f1 in enumerate(featureList):
            geomDict[f1.geometry()].add(f1)
            for idx2, f2 in enumerate(featureList):
                if feedback.isCanceled():
                    break
                if idx2 <= idx1 or not f1.geometry().isGeosEqual(f2.geometry()):
                    feedback.setProgress(int(idx1 * total + idx2))
                    continue
                for geom in geomDict:
                    if geom.isGeosEqual(f1.geometry()) or geom.isGeosEqual(f2.geometry()):
                        geomDict[geom] |= {f1, f2}
                        break
                else:
                    geomDict[f1.geometry()].add(f2)
                feedback.setProgress(int(idx1 * total + idx2))
        for k, v in geomDict.items():
            if feedback.isCanceled():
                break
            if len(v) > 1:
                idStrList = ','.join( map(str, [i.id() for i in v] ) )
                flagText = self.tr('Features from layer {0} with ids=({1}) have duplicated geometries.')\
                            .format(inputLyr.name(), idStrList)
                self.flagFeature(v.pop().geometry(), flagText)      

        return {self.FLAGS: self.flag_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyduplicatedgeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Duplicated Geometries')

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
        return QCoreApplication.translate('IdentifyDuplicatedGeometriesAlgorithm', string)

    def createInstance(self):
        return IdentifyDuplicatedGeometriesAlgorithm()
