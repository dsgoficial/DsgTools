# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton / Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho / @eb.mil.br
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

from pathlib import Path

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterFile,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.utils import iface


class LoadShapefileAlgorithm(QgsProcessingAlgorithm):

    FOLDER_SHAPEFILES = "FOLDER_SHAPEFILES"
    OUTPUT = "OUTPUT"

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER_SHAPEFILES,
                self.tr("Pasta com Shapefiles"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(self.OUTPUT, self.tr("Loaded layers"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        folderPath = self.parameterAsString(parameters, self.FOLDER_SHAPEFILES, context)
        folder_pathlib_obj = Path(folderPath)
        output = []
        file_iter = folder_pathlib_obj.glob('*/*.shp') \
            if len(list(folder_pathlib_obj.glob('*/*.shp'))) > 0 \
            else folder_pathlib_obj.glob('*.shp')
        shapefileData = [
            {"name": p.stem, "path": p, "parent_folder": p.parent.stem}
            for p in file_iter
        ]
        shapefileData = sorted(shapefileData, key=lambda k: (k["parent_folder"], k["name"]))
        groupDict = dict()
        rootNodeList = []
        parentFolderSet = set(i["parent_folder"] for i in shapefileData)
        listSize = len(shapefileData)
        progressStep = 100 / listSize if listSize else 0
        for rootNodeName in sorted(parentFolderSet):
            rootNode = QgsProject.instance().layerTreeRoot().addGroup(rootNodeName)
            rootNodeList.append(rootNode)
            groupDict[rootNodeName] = {
                QgsWkbTypes.PointGeometry: self.createGroup("Ponto", rootNode),
                QgsWkbTypes.LineGeometry: self.createGroup("Linha", rootNode),
                QgsWkbTypes.PolygonGeometry: self.createGroup("Area", rootNode),
            }
        for step, data in enumerate(shapefileData):
            if feedback.isCanceled():
                break
            iface.mapCanvas().freeze(True)
            ml = QgsProject.instance().addMapLayer(
                QgsVectorLayer(str(data["path"]), data["name"], "ogr"), addToLegend=False
            )
            groupDict[data["parent_folder"]][QgsWkbTypes.geometryType(ml.wkbType())].addLayer(ml)
            output.append(ml.id())
            iface.mapCanvas().freeze(False)
            feedback.setProgress(step * progressStep)
        for rootNode in rootNodeList:
            self.removeEmptyGroups(list(groupDict[rootNode.name()].values()), rootNode)
        return {self.OUTPUT: output}

    def createGroup(self, groupName, rootNode):
        return rootNode.addGroup(groupName)

    def removeEmptyGroups(self, groups, rootNode):
        for group in groups:
            if group.findLayers():
                continue
            rootNode.removeChildNode(group)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "loadshapefilealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Loads a shapefile (.shp)")

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
        return "DSGTools - Layer Management Algorithms"

    def tr(self, string):
        """
        Translates input string.
        """
        return QCoreApplication.translate("LoadShapefileAlgorithm", string)

    def createInstance(self):
        """
        Creates an instance of this class
        """
        return LoadShapefileAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
    
    def shortHelpString(self):
        return self.tr("This algorithm loads shapefiles from folders. If a folder with subfolders is selected, one extra node is created for each subfolder")
