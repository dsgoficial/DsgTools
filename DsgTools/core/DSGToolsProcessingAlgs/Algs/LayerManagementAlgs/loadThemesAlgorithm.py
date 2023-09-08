# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-13
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jossan
        email                : -
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
import os

from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsDataSourceUri,
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterExpression,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProject,
    QgsProcessingParameterFile
)
from qgis.utils import iface
from qgis import gui, core
import json

class LoadThemesAlgorithm(QgsProcessingAlgorithm):
    FILE = "FILE"
    TEXT = "TEXT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.FILE, self.tr("Input json file"), defaultValue=".json"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.TEXT,
                description=self.tr("Input json text"),
                multiLine=True,
                defaultValue="[]",
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT, self.tr("Original layers id with default field value")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.

        """
        inputJSONFile = self.parameterAsFile(parameters, self.FILE, context)
        inputJSONData = json.loads(
            self.parameterAsString(parameters, self.TEXT, context)
        )
        if os.path.exists(inputJSONFile):
            self.loadThemes(inputJSONFile)
        elif len(inputJSONData) > 0:
            self.loadThemes(inputJSONData)
        return {self.OUTPUT: []}

    def loadThemes(self, themes):
        for theme in themes:
            themeLayers = [ '{}.{}'.format(l['schema'], l['camada']) for l in theme['camadas'] ]
            root = core.QgsProject().instance().layerTreeRoot().clone()
            for rLayer in root.findLayers():
                rLayer.setItemVisibilityChecked(False)
                rLayerName = '{}.{}'.format(
                    rLayer.layer().dataProvider().uri().schema(),
                    rLayer.layer().dataProvider().uri().table()
                )
                if not(rLayerName in themeLayers):
                    continue
                rLayer.setItemVisibilityChecked(True)
            model = core.QgsLayerTreeModel(root)
            themeCollection = core.QgsProject.instance().mapThemeCollection()
            themeCollection.insert(theme['nome'], core.QgsMapThemeCollection.createThemeFromCurrentState(root, model))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "loadthemes"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Load Themes")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Layer Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Layer Management Algorithms"

    def tr(self, string):
        """
        Translates input string.
        """
        return QCoreApplication.translate("LoadThemesAlgorithm", string)

    def createInstance(self):
        """
        Creates an instance of this class
        """
        return LoadThemesAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
