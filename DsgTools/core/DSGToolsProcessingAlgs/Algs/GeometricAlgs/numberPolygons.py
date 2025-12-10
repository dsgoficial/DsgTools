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
"""

from qgis.core import (
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsField,
    QgsFeature,
)
from qgis.PyQt.QtCore import QVariant, QCoreApplication


class NumberPolygonsAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = "INPUT_LAYER"
    ATTRIBUTE_NAME = "ATTRIBUTE_NAME"
    OUTPUT_LAYER = "OUTPUT_LAYER"
    DIRECTION = "DIRECTION"
    GROUP_BY_FIELD = "GROUP_BY_FIELD"  # Novo parâmetro

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr("Insira a camada de polígonos"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DIRECTION,
                self.tr("Indique a direção de numeração:"),
                options=[
                    "Do Norte para o Sul, do Oeste para o Leste",
                    "Do Norte para o Sul, do Leste para o Oeste",
                    "Do Sul para o Norte, do Leste para o Oeste",
                    "Do Sul para o Norte, do Oeste para o Leste",
                ],
                defaultValue=0,
            )
        )
        
        # Novo parâmetro opcional de agrupamento
        self.addParameter(
            QgsProcessingParameterField(
                self.GROUP_BY_FIELD,
                self.tr("Campo para agrupar (opcional)"),
                parentLayerParameterName=self.INPUT_LAYER,
                optional=True,
                allowMultiple=False,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.ATTRIBUTE_NAME,
                self.tr("Insira o nome do atributo de ordenamento"),
                defaultValue="ord",
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LAYER, self.tr("Numbered Polygons")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        direction = self.parameterAsEnum(parameters, self.DIRECTION, context)
        attr_name = self.parameterAsString(parameters, self.ATTRIBUTE_NAME, context)
        group_by_field = self.parameterAsString(parameters, self.GROUP_BY_FIELD, context)

        if not layer:
            raise QgsProcessingException("Invalid input layer")

        # Validar campo de agrupamento se fornecido
        if group_by_field:
            field_index = layer.fields().indexFromName(group_by_field)
            if field_index == -1:
                raise QgsProcessingException(f"Campo '{group_by_field}' não encontrado")
            feedback.pushInfo(f"Ordenando por campo: {group_by_field}")

        fields = layer.fields()
        fields.append(QgsField(attr_name, QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_LAYER,
            context,
            fields,
            layer.wkbType(),
            layer.sourceCrs(),
        )

        features = list(layer.getFeatures())
        
        # Ordenar features considerando grupo (se houver) e direção
        sorted_features = self._sort_features(features, direction, group_by_field)
        
        total = 100.0 / len(sorted_features) if sorted_features else 0
        feedback.setProgressText("Numerando os polígonos conforme direção dada...\n")

        for i, feature in enumerate(sorted_features, start=1):
            new_feature = QgsFeature(fields)
            new_feature.setGeometry(feature.geometry())
            new_feature.setAttributes(feature.attributes() + [i])
            sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
            feedback.setProgress(int(i * total))

        return {self.OUTPUT_LAYER: dest_id}

    def _sort_features(self, features, direction, group_by_field=None):
        """
        Ordena uma lista de features baseado na direção especificada
        e opcionalmente por um campo de agrupamento
        """
        # Ordenação do Norte para o Sul e do Oeste para o Leste
        if direction == 0:
            if group_by_field:
                features.sort(
                    key=lambda f: (
                        f.attribute(group_by_field),
                        -f.geometry().centroid().asPoint().y(),
                        f.geometry().centroid().asPoint().x(),
                    )
                )
            else:
                features.sort(
                    key=lambda f: (
                        -f.geometry().centroid().asPoint().y(),
                        f.geometry().centroid().asPoint().x(),
                    )
                )

        # Ordenação do Norte para o Sul e do Leste para o Oeste
        elif direction == 1:
            if group_by_field:
                features.sort(
                    key=lambda f: (
                        f.attribute(group_by_field),
                        -f.geometry().centroid().asPoint().y(),
                        -f.geometry().centroid().asPoint().x(),
                    )
                )
            else:
                features.sort(
                    key=lambda f: (
                        -f.geometry().centroid().asPoint().y(),
                        -f.geometry().centroid().asPoint().x(),
                    )
                )

        # Ordenação do Sul para o Norte e do Leste para o Oeste
        elif direction == 2:
            if group_by_field:
                features.sort(
                    key=lambda f: (
                        f.attribute(group_by_field),
                        f.geometry().centroid().asPoint().y(),
                        -f.geometry().centroid().asPoint().x(),
                    )
                )
            else:
                features.sort(
                    key=lambda f: (
                    f.geometry().centroid().asPoint().y(),
                    -f.geometry().centroid().asPoint().x(),
                )
            )

        # Ordenação do Sul para o Norte e do Oeste para o Leste
        elif direction == 3:
            if group_by_field:
                features.sort(
                    key=lambda f: (
                        f.attribute(group_by_field),
                        f.geometry().centroid().asPoint().y(),
                        f.geometry().centroid().asPoint().x(),
                    )
                )
            else:
                features.sort(
                    key=lambda f: (
                        f.geometry().centroid().asPoint().y(),
                        f.geometry().centroid().asPoint().x(),
                    )
                )
        
        return features

    def name(self):
        return "numberpolygons"

    def displayName(self):
        return self.tr("Number Polygons")

    def group(self):
        return self.tr("Geometric Algorithms")

    def groupId(self):
        return "DSGTools - Geometric Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("NumberPolygonsAlgorithm", string)

    def createInstance(self):
        return NumberPolygonsAlgorithm()
