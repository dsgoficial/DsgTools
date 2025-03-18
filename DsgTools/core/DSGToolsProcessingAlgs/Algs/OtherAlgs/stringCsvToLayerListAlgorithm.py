# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-10-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import fnmatch
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsMapLayer,
    QgsProcessingAlgorithm,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterString,
    QgsProcessingUtils,
    QgsProject,
    QgsVectorLayer,
)


class StringCsvToLayerListAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = "INPUTLAYERS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUTLAYERS, self.tr("Comma separated Input Layer Names")
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT, self.tr("Multiple layer list")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerCsv = self.parameterAsString(parameters, self.INPUTLAYERS, context)
        layerNameList = [i.strip() for i in layerCsv.split(",")] if layerCsv != "" else []
        if not len(layerNameList):
            return {self.OUTPUT: []}
        layerSet = set()
        layerNamesToLoadSet = self.getLayerNameSetToLoad(layerNameList)
        progressStep = 100 / len(layerNamesToLoadSet)
        for idx, layerName in enumerate(layerNamesToLoadSet):
            if feedback.isCanceled():
                break
            lyr = QgsProcessingUtils.mapLayerFromString(layerName, context)
            if lyr is None:
                continue
            if lyr.readOnly() or not isinstance(lyr, QgsVectorLayer):
                continue
            layerSet.add(lyr.id())
            feedback.setProgress(idx * progressStep)

        return {self.OUTPUT: [lyr for lyr in layerSet]}

    def getLayerNameSetToLoad(self, layerNameList):
        loadedLayerDict = {
            l.name(): l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsMapLayer.VectorLayer
        }
        loadedLayerNamesSet = set(loadedLayerDict.keys())
        wildCardFilterList = [fi for fi in layerNameList if "*" in fi]
        wildCardLayersSet = set()
        for wildCardFilter in wildCardFilterList:
            wildCardLayersSet = wildCardLayersSet.union(
                set(fnmatch.filter(loadedLayerNamesSet, wildCardFilter))
            )
        layerNamesToLoadSet = (
            set(layerNameList) - set(wildCardFilterList) | wildCardLayersSet
        )
        for pipeString in filter(lambda x: "|" in x, layerNameList):
            nameList = pipeString.split("|")
            for name in nameList:
                matched = list(
                    filter(
                        lambda x: name in x[0] and x[1].featureCount() > 0,
                        loadedLayerDict.items(),
                    )
                )
                if len(matched) == 0:
                    continue
                layerNamesToLoadSet.add(matched[0][0])
                break

        return layerNamesToLoadSet

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return "stringcsvtolayerlistalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("String CSV to Layer List Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Model Helpers")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Model Helpers"

    def tr(self, string):
        return QCoreApplication.translate("StringCsvToLayerListAlgorithm", string)

    def createInstance(self):
        return StringCsvToLayerListAlgorithm()
