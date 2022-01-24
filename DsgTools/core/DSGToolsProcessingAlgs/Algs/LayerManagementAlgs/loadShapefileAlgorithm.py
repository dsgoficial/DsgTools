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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterFile, QgsProject, QgsVectorLayer,
                       QgsWkbTypes)
from qgis.utils import iface


class LoadShapefileAlgorithm(QgsProcessingAlgorithm):

    FOLDER_SHAPEFILES = 'FOLDER_SHAPEFILES'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER_SHAPEFILES,
                self.tr('Pasta com Shapefiles'),
                behavior = QgsProcessingParameterFile.Folder,
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Loaded layers')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        folderPath = self.parameterAsString(
            parameters,
            self.FOLDER_SHAPEFILES,
            context
        )
        output = []
        shapefileData = [ 
            {
                'name': fileName.split('.')[0],
                'path': os.path.join(folderPath, fileName)
            }
            for fileName in os.listdir(folderPath)
            if fileName.split('.')[1] == 'shp'
        ]
        shapefileData = sorted(shapefileData, key=lambda k: k['name']) 
        listSize = len(shapefileData)
        progressStep = 100/listSize if listSize else 0
        rootNode = QgsProject.instance().layerTreeRoot().addGroup('shapefiles')
        groups = {
            QgsWkbTypes.PointGeometry: self.createGroup('Ponto', rootNode),
            QgsWkbTypes.LineGeometry: self.createGroup('Linha', rootNode),
            QgsWkbTypes.PolygonGeometry: self.createGroup('Area', rootNode),
            
        }
        for step, data in enumerate(shapefileData):
            if feedback.isCanceled():
                break
            iface.mapCanvas().freeze(True)
            ml = QgsProject.instance().addMapLayer(
                QgsVectorLayer(data['path'], data['name'], 'ogr'), 
                addToLegend = False
            )
            groups[QgsWkbTypes.geometryType(ml.wkbType())].addLayer(ml)
            output.append(ml.id())
            iface.mapCanvas().freeze(False)
            feedback.setProgress(step*progressStep)
        self.removeEmptyGroups(list(groups.values()), rootNode)
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
        return 'loadshapefilealgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Loads a shapefile (.shp)')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        """
        Translates input string.
        """
        return QCoreApplication.translate('LoadShapefileAlgorithm', string)

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
