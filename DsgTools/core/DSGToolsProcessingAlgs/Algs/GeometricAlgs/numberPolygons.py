# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-19
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Edson Tadeu - Cartographic Engineer @ Brazilian Army
        email                : tadeu.edson@eb.mil.br
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

from qgis.core import (QgsFeatureSink,
                        QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterField,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink,
                       QgsProject,
                       QgsFeatureRequest,
                       QgsProcessingUtils,
                       QgsVectorLayer,
                       QgsField,
                       QgsFeature)
from qgis.PyQt.QtCore import QVariant, QCoreApplication
import processing

class NumberPolygonsAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    ATTRIBUTE_NAME = 'ATTRIBUTE_NAME'
    OUTPUT_LAYER = 'OUTPUT_LAYER'
    DIRECTION = 'DIRECTION'

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr('Insira a camada de polígonos'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DIRECTION,
                self.tr('Indique a direção de numeração:'),
                options = ['Do Norte para o Sul, do Oeste para o Leste',
                            'Do Norte para o Sul, do Leste para o Oeste',
                            'Do Sul para o Norte, do Leste para o Oeste',
                            'Do Sul para o Norte, do Oeste para o Leste'],
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.ATTRIBUTE_NAME,
                self.tr('Insira o nome do atributo de ordenamento'),
                defaultValue = 'ord'
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LAYER,
                self.tr('Numbered Polygons')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        direction = self.parameterAsEnum(parameters, self.DIRECTION, context)
        attr_name = self.parameterAsString(parameters, self.ATTRIBUTE_NAME, context)

        total = 100.0 / layer.featureCount() if layer.featureCount() else 0

        if not layer:
            raise QgsProcessingException('Invalid input layer')

        fields = layer.fields()
        fields.append(QgsField(attr_name, QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(parameters,
                                                self.OUTPUT_LAYER,
                                                context,
                                                fields,
                                                layer.wkbType(),
                                                layer.sourceCrs())

        features = list(layer.getFeatures())
       
        # Ordenação do Norte para o Sul e do Oeste para o Leste
        if direction == 0:
            features.sort(key=lambda f: (-f.geometry().centroid().asPoint().y(), f.geometry().centroid().asPoint().x()))

        # Ordenação do Norte para o Sul e do Leste para o Oeste
        elif direction == 1:
            features.sort(key=lambda f: (-f.geometry().centroid().asPoint().y(), -f.geometry().centroid().asPoint().x()))

        # Ordenação do Sul para o Norte e do Leste para o Oeste
        elif direction == 2:
            features.sort(key=lambda f: (f.geometry().centroid().asPoint().y(), -f.geometry().centroid().asPoint().x()))

        # Ordenação do Sul para o Norte e do Oeste para o Leste
        elif direction == 3:
            features.sort(key=lambda f: (f.geometry().centroid().asPoint().y(), f.geometry().centroid().asPoint().x()))
        
        feedback.setProgressText('Numerando os polígonos conforme direção dada...\n')

        for i, feature in enumerate(features, start=1):
            new_feature = QgsFeature(fields)
            new_feature.setGeometry(feature.geometry())
            new_feature.setAttributes(feature.attributes() + [i])
            sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
            feedback.setProgress(int(i * total))
        
        """
        centroides = processing.run("native:centroids", 
                                    {'INPUT': layer,
                                    'ALL_PARTS':False,
                                    'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
        centroides.setName("Centroides")
        QgsProject.instance().addMapLayer(centroides)
        """

        return {self.OUTPUT_LAYER: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "numberpolygons"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Number Polygons")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("NumberPolygonsAlgorithm", string)

    def createInstance(self):
        return NumberPolygonsAlgorithm()