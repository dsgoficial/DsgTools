# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-03-21
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
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProject,
    QgsPointXY,
    QgsProcessingParameterFeatureSource,
)

from qgis.PyQt.Qt import QVariant

from qgis.PyQt.QtCore import (
    QCoreApplication,
    QVariant
)


class CreateGridAlongLineAlgorithm(QgsProcessingAlgorithm):
    
    INPUT_LAYER = "INPUT_LAYER"
    PAPER_SIZE = "PAGE_SIZE"
    SCALE = "SCALE"
    OVERLAP = 'OVERLAP'
    START = 'START'
    MARGINS_TOP = 'MARGINS_TOP'
    MARGINS_BOTTOM = 'MARGINS_BOTTOM'
    MARGINS_LEFT = 'MARGINS_LEFT'
    MARGINS_RIGHT = 'MARGINS_RIGHT'
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_LAYER,
                self.tr("Insira a camada de linha"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE,
                self.tr('Escala'),
                options=['1:1000', '1:2000', '1:5000', '1:10000'],
                defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.PAPER_SIZE,
                self.tr('Tamanho da Folha'),
                options=['A4', 'A3'], 
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP,
                self.tr('Sobreposição (%)'),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                maxValue=100,
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.START,
                self.tr('Start from begin (m)'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=50
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MARGINS_TOP,
                'Margem Superior (mm)',
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MARGINS_BOTTOM,
                'Margem Inferior (mm)',
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MARGINS_LEFT,
                'Margem Esquerda (mm)',
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MARGINS_RIGHT,
                'Margem Direita (mm)',
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Camada de Molduras',
                QgsProcessing.TypeVectorPolygon))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsSource(parameters, self.INPUT_LAYER, context)
        scale = self.parameterAsEnum(parameters, self.SCALE, context)
        paper_size = self.parameterAsEnum(parameters, self.PAPER_SIZE, context)
        margins_top = self.parameterAsDouble(parameters, self.MARGINS_TOP, context)
        margins_bottom = self.parameterAsDouble(parameters, self.MARGINS_BOTTOM, context)
        margins_left = self.parameterAsDouble(parameters, self.MARGINS_LEFT, context)
        margins_right = self.parameterAsDouble(parameters, self.MARGINS_RIGHT, context)
        overlap = self.parameterAsDouble(parameters, self.OVERLAP, context)
        start = self.parameterAsDouble(parameters, self.START, context)

        fields = QgsFields()
        fields.append(QgsField("ord", QVariant.Int))
        fields.append(QgsField("id", QVariant.Int))  # ID da feição de linha

        #Tamanho da folha
        if paper_size == 0: proportion = (297, 210) # proporção do a4 Altura/largura
        else: proportion = (420, 297) # proporção do a3

        #Tamanho da escala - 0-1000, 1-2000, 3-5000, 4-10000
        escalas = {
            0: 1,
            1: 2,
            2: 5,
            3: 10,
        }
        escala = escalas[scale]

        #Definição da largura e tamanho no terreno
        height = (proportion[1] - ((margins_left + margins_right))) * escala
        width = (proportion[0] - ((margins_bottom + margins_top))) * escala

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            source.sourceCrs(),
        )

        self.calcula_grid(source, sink, start, width, height, overlap, feedback)

        return {"OUTPUT": dest_id}
    
    def calcula_grid(self, source, sink, start, width, height, overlap, feedback):
        r = 1
        nFeatures = source.featureCount()
        if nFeatures == 0:
            return
        stepSize = 100/nFeatures
        for current, feature in enumerate(source.getFeatures()):
            if feedback.isCanceled():
                break
            geom = feature.geometry()
            line_id = feature.id()
            extended_geom = QgsGeometry.extendLine(geom, start, overlap)
            curs = 0
            geomlength = geom.length()
            numpages = geomlength / width #Divisão do comprimento da feição pela altura da folha
            step = 1.0 / numpages
            stepnudge = (1.0 - (overlap/100)) * step

            while curs <= 1:
                startpoint = extended_geom.interpolate(curs*geomlength)
                # interpolate returns no geometry when > 1
                forward = (curs+step)
                if forward > 1:
                    forward = 1
                endpoint = extended_geom.interpolate(forward*geomlength)
                x_start = startpoint.asPoint().x()
                y_start = startpoint.asPoint().y()
                geom = self.createPolygon(x_start, y_start, startpoint, endpoint, height, width)
                curs = curs + stepnudge
                new_feat = self.createFeature(r, line_id, geom)
                sink.addFeature(new_feat, QgsFeatureSink.FastInsert)
                r += 1

            feedback.setProgress(current * stepSize)
    
    def createPolygon(self, x_start, y_start, startpoint, endpoint, height, width):
        page_polygon = QgsGeometry().fromWkt(
                    f'POLYGON((0 0, 0 {height},{width} {height}, {width} 0, 0 0))'
                )
        page_polygon.translate(0, - height/2)
        azimuth = startpoint.asPoint().azimuth(endpoint.asPoint())
        currangle = (azimuth+270) % 360
        page_polygon.rotate(currangle, QgsPointXY(0, 0))
        page_polygon.translate(x_start, y_start)
        page_polygon.asPolygon()
        return page_polygon

    def createFeature(self, r, line_id, geom):
        new_feat = QgsFeature()
        new_feat.setAttributes([r, line_id])
        new_feat.setGeometry(geom)
        return new_feat

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "creategridalonglinealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Create Grid Along Line")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Grid Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Grid Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateGridAlongLineAlgorithm", string)

    def createInstance(self):
        return CreateGridAlongLineAlgorithm()
