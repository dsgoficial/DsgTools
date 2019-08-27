# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, 
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsProject)

class ExportToMemoryLayer(QgsProcessingAlgorithm):
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        feats = [ feat for feat in layer.getFeatures() ]
        geom_types = {
            0 : 'Point',
            1 : 'LineString',
            2 : 'Polygon',
        }
        temp = QgsVectorLayer(
            '{0}?crs={1}'.format(geom_types[layer.geometryType()], layer.crs().authid()), 
            "result", 
            "memory"
        )
        temp_data = temp.dataProvider()
        attr = layer.dataProvider().fields().toList()
        temp_data.addAttributes(attr)
        temp.updateFields()
        temp_data.addFeatures(feats)
        QgsProject().instance().addMapLayer(temp)
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'exportToMemoryLayer'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Export To Memory Layer')

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
        return QCoreApplication.translate('ExportToMemoryLayer', string)

    def createInstance(self):
        return ExportToMemoryLayer()