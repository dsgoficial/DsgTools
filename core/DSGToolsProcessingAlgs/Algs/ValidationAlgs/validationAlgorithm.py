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
                       QgsFields)

class ValidationAlgorithm(QgsProcessingAlgorithm):
    """
    Processing algorithm with handy stuff for other algs.
    """
    def getIteratorAndFeatureCount(self, lyr, onlySelected = False):
        """
        Gets the iterator and feature count from lyr.
        """
        if onlySelected:
            total = 100.0 / lyr.selectedFeatureCount() if lyr.selectedFeatureCount() else 0
            iterator = lyr.getSelectedFeatures()
        else:
            total = 100.0 / lyr.featureCount() if lyr.featureCount() else 0
            iterator = lyr.getFeatures()
        return iterator, total
    
    def prepareFlagSink(self, parameters, source, wkbType, context):
        flagFields = self.getFlagFields()
        (self.flagSink, self.dest_id) = self.parameterAsSink(parameters, self.FLAGS,
                context, flagFields, wkbType, source.sourceCrs())
        if self.flagSink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.FLAGS))
    
    def getFlagFields(self):
        fields = QgsFields()
        fields.append(QgsField('reason',QVariant.String))
        return fields
    
    def flagFeature(self, flagGeom, flagText):
        """
        Creates and adds to flagSink a new flag with the reason.
        :param flagGeom: (QgsGeometry) geometry of the flag;
        :param flagText: (string) Text of the flag
        """
        newFeat = QgsFeature(self.getFlagFields())
        newFeat['reason'] = flagText
        newFeat.setGeometry(flagGeom)
        self.flagSink.addFeature(newFeat, QgsFeatureSink.FastInsert)
    
    def getFlagsFromOutput(self, output):
        if 'FLAGS' not in output:
            return []
        return [i for i in output['FLAGS'].getFeatures()]
    
    def flagFeaturesFromProcessOutput(self, output):
        if 'FLAGS' in output:
            for feat in output['FLAGS'].getFeatures():
                self.flagSink.addFeature(feat, QgsFeatureSink.FastInsert)