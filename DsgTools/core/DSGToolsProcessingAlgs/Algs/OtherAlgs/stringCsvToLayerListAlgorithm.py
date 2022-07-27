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
from qgis.core import (QgsMapLayer, QgsProcessingAlgorithm,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterString,
                       QgsProcessingUtils,
                       QgsProject)


class StringCsvToLayerListAlgorithm(QgsProcessingAlgorithm):
    INPUTLAYERS = 'INPUTLAYERS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUTLAYERS,
                self.tr('Comma separated Input Layer Names')
            )
        )
       
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Multiple layer list')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerCsv = self.parameterAsString(
            parameters,
            self.INPUTLAYERS,
            context
        )
        layerNameList = layerCsv.split(',')
        if not len(layerNameList):
            return {self.OUTPUT : None}
        layerSet = set()
        layerNamesToLoadSet = self.getLayerNameSetToLoad(layerNameList)
        progressStep = 100/len(layerNamesToLoadSet)
        for idx, layerName in enumerate(layerNamesToLoadSet):
            if feedback.isCanceled():
                break
            lyr = QgsProcessingUtils.mapLayerFromString(layerName, context)
            if lyr is None:
                continue
            layerSet.add(lyr.id())
            feedback.setProgress(idx * progressStep)

        return { self.OUTPUT : list(layerSet)}

    def getLayerNameSetToLoad(self, layerNameList):
        loadedLayerNamesSet = set(
            l.name() for l in QgsProject.instance().mapLayers().values() \
            if l.type() == QgsMapLayer.VectorLayer
        )
        wildCardFilterList = [fi for fi in layerNameList if "*" in fi]
        wildCardLayersSet = set()
        for wildCardFilter in wildCardFilterList:
            wildCardLayersSet = wildCardLayersSet.union(
                set(fnmatch.filter(loadedLayerNamesSet, wildCardFilter))
            )
        layerNamesToLoadSet = set(layerNameList) - set(wildCardFilterList) | wildCardLayersSet
        return layerNamesToLoadSet

    def name(self):
        """
        Here is where the processing itself takes place.
        """
        return 'stringcsvtolayerlistalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('String CSV to Layer List Algorithm')

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
        return QCoreApplication.translate('StringCsvToLayerListAlgorithm', string)

    def createInstance(self):
        return StringCsvToLayerListAlgorithm()
