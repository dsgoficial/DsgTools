# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-26
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Pedro Martins - Cartographic Engineer @ Brazilian Army
                               (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army

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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProject,
    QgsMapLayer,
    Qgis,
)
from qgis import processing
from qgis.utils import iface


class RemoveEmptyLayers(QgsProcessingAlgorithm):
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        "pass"

    def processAlgorithm(self, parameters, context, feedback):
        outputLayers = []

        listSize = len(QgsProject.instance().mapLayers())
        progressStep = 100 / listSize if listSize else 0

        toBeRemoved = []
        step = 0
        feedback.setProgressText(self.tr("Removing layers..."))

        for key, layer in QgsProject.instance().mapLayers().items():
            if feedback.isCanceled():
                return {self.OUTPUT: outputLayers}
            if layer.type() == QgsMapLayer.VectorLayer and layer.featureCount() == 0:
                outputLayers.append(layer.name())
                toBeRemoved.append(layer.id())
            step += 1
            feedback.setProgress(step * progressStep)
        if toBeRemoved:
            QgsProject.instance().removeMapLayers(toBeRemoved)
        iface.messageBar().pushMessage(
            self.tr("Executed."),
            self.tr("Empty layers removed."),
            level=Qgis.Success,
            duration=5,
        )

        return {self.OUTPUT: outputLayers}

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return RemoveEmptyLayers()

    def name(self):
        return "remove_empty_layers"

    def displayName(self):
        return self.tr("Remove Empty Layers")

    def group(self):
        return self.tr("Layer Management Algorithms")

    def groupId(self):
        return "DSGTools - Layer Management Algorithms"

    def shortHelpString(self):
        return self.tr(
            "The processing algorithm removes empty layers from the project."
        )
