# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jossan
        email                :
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

from qgis.PyQt.QtCore import QCoreApplication, QMetaType
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsProcessingParameterFeatureSource,
    QgsGeometry,
    QgsLineString,
    QgsProcessingMultiStepFeedback,
    QgsWkbTypes,
    QgsFields,
    QgsField,
    QgsMultiLineString,
    QgsSpatialIndex,
)


class UnionFind:
    """Estrutura Union-Find (Disjoint Set Union) com compressão de caminho
    e union by rank para encontrar componentes conectados em tempo quase-linear.
    """

    __slots__ = ("parent", "rank")

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):
        # Compressão de caminho iterativa (evita recursão profunda)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


class Line2Multiline(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Select line layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            return {self.OUTPUT: None}

        fields = QgsFields()
        fields.append(QgsField("length", QMetaType.Type.Double))

        (sink, sink_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.MultiLineString,
            source.sourceCrs(),
        )

        total = source.featureCount()
        if total == 0:
            return {self.OUTPUT: sink_id}

        multi_feedback = QgsProcessingMultiStepFeedback(3, feedback)

        # -- Passo 1: carregar geometrias e construir índice espacial ----------
        multi_feedback.setCurrentStep(0)
        geometries = {}  # fid -> QgsGeometry
        spatial_index = QgsSpatialIndex()
        step_size = 100.0 / total

        for current, feat in enumerate(source.getFeatures()):
            if multi_feedback.isCanceled():
                return {self.OUTPUT: sink_id}
            fid = feat.id()
            geom = feat.geometry()
            if geom.isNull() or geom.isEmpty():
                continue
            geometries[fid] = geom
            spatial_index.addFeature(feat)
            multi_feedback.setProgress(current * step_size)

        # -- Passo 2: encontrar componentes conectados via Union-Find ---------
        multi_feedback.setCurrentStep(1)
        uf = UnionFind()
        fids = list(geometries.keys())
        n_geoms = len(fids)
        if n_geoms == 0:
            return {self.OUTPUT: sink_id}

        step_size = 100.0 / n_geoms
        for current, fid in enumerate(fids):
            if multi_feedback.isCanceled():
                return {self.OUTPUT: sink_id}
            uf.make_set(fid)
            geom = geometries[fid]
            bbox = geom.boundingBox()
            candidates = spatial_index.intersects(bbox)
            for cand_fid in candidates:
                if cand_fid == fid:
                    continue
                # Só faz union se realmente se tocam/intersectam
                if geom.touches(geometries[cand_fid]) or geom.intersects(
                    geometries[cand_fid]
                ):
                    uf.make_set(cand_fid)
                    uf.union(fid, cand_fid)
            multi_feedback.setProgress(current * step_size)

        # -- Passo 3: agrupar por componente e gerar multilinhas --------------
        multi_feedback.setCurrentStep(2)
        components = {}
        for fid in fids:
            root = uf.find(fid)
            if root not in components:
                components[root] = []
            components[root].append(fid)

        n_components = len(components)
        if n_components == 0:
            return {self.OUTPUT: sink_id}
        step_size = 100.0 / n_components

        for current, member_fids in enumerate(components.values()):
            if multi_feedback.isCanceled():
                return {self.OUTPUT: sink_id}

            mls = QgsMultiLineString()
            for fid in member_fids:
                geom = geometries[fid]
                # Suporta tanto geometrias simples quanto multi
                for part in geom.parts():
                    mls.addGeometry(part.clone())

            out_geom = QgsGeometry(mls)
            new_feat = QgsFeature(fields)
            new_feat.setGeometry(out_geom)
            new_feat["length"] = out_geom.length()
            sink.addFeature(new_feat, QgsFeatureSink.FastInsert)

            multi_feedback.setProgress(current * step_size)

        return {self.OUTPUT: sink_id}

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return Line2Multiline()

    def name(self):
        return "line2multiline"

    def displayName(self):
        return self.tr("Convert Line to Multiline")

    def group(self):
        return self.tr("Geometric Algorithms")

    def groupId(self):
        return "DSGTools - Geometric Algorithms"

    def shortHelpString(self):
        return self.tr("O algoritmo converte linhas que se tocam para multilinha")
