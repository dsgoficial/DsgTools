# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-23
        git sha              : $Format:%H$
        copyright            : (C) 2019 by  Jossan Costa - Surveying Technician @ Brazilian Army
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
from qgis.PyQt.QtXml import QDomDocument

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterVectorLayer, 
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsProject)

from qgis.utils import iface

class ExportToMemoryLayer(QgsProcessingAlgorithm):
    INPUT = 'INPUT_LAYER'
    OUTPUT_NAME = 'OUTPUT_NAME'
    OUTPUT_QML_STYLE = 'OUTPUT_QML_STYLE'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Camada de entrada')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_NAME,
                self.tr('Nome da camada de saída'),
                optional=True,
                defaultValue='resultado'
            )
        )   
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_QML_STYLE,
                self.tr('Estilo da camada de saída'),
                multiLine = True,
                optional=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        geom_types = {
            0 : 'Point',
            1 : 'LineString',
            2 : 'Polygon',
        }
        outputLayerName = self.parameterAsString(parameters, self.OUTPUT_NAME, context)
        outputLayerStyle = self.parameterAsString(parameters, self.OUTPUT_QML_STYLE, context)
        temp = QgsVectorLayer(
            '{0}?crs={1}'.format(geom_types[layer.geometryType()], layer.crs().authid()), 
            "{0}".format(outputLayerName), 
            "memory"
        )
        doc = QDomDocument()
        doc.setContent(outputLayerStyle)
        temp.importNamedStyle(doc)
        temp_data = temp.dataProvider()
        temp_data.addAttributes(layer.dataProvider().fields().toList())
        temp.updateFields()
        temp_data.addFeatures([ feat for feat in layer.getFeatures() ])
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
        return self.tr('Export To Memory Layer (works only on models)')

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