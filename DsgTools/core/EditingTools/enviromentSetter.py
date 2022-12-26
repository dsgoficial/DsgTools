# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-02-27
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
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import (
    LayerLoaderFactory,
)
from qgis.core import QgsProject


class EnviromentSetter:
    def __init__(self, iface):
        self.layerFactory = LayerLoaderFactory()
        self.iface = iface

    def setEnviroment(self, parameterDict):
        """
        :param parameterDict (dict): dictionary with parameters
        to set de Editing Enviroment.
        parameterDict = {
            'abstractDb' : database,
            'layerList': [list of layer names, ordered by exibition],
            'stylePath' : path of the style,
            'framePolygon' : polygon of the working area
        }
        """
        # Step 1: Load layers
        layerLoader = self.layerFactory.makeLoader(
            iface=self.iface, abstractDb=parameterDict["abstractDb"]
        )
        loadedLayerDict = layerLoader.loadedLayers(
            inputList=parameterDict["layerList"],
            stylePath=parameterDict["stylePath"],
            loadEditingStructure=True,
        )
        self.setLayerOrdering(
            vectorLayerDict=loadedLayerDict, layerOrder=parameterDict["layerList"]
        )
        self.createGrid(parameterDict["workingAreaPolygon"])
        self.setWorkArea(parameterDict["workingAreaPolygon"])

    def createGrid(self, workingAreaPolygon):
        """
        :param extents: [xmin, ymin, xmax, ymax]
        Creates the grid of workingAreaPolygon
        }
        """
        pass

    def setWorkArea(self, workingAreaPolygon):
        """
        :param extents: [xmin, ymin, xmax, ymax]
        """
        pass

    def setLayerOrdering(self, vectorLayerDict, layerOrder):
        """
        :param vectorLayerDict: dict of QgsVectorLayers,
        :param layerOrder: ordered list with the names of each layer
        """
        root = QgsProject.instance().layerTreeRoot()
        order = root.customLayerOrder()
        count = 0
        for layer_name in layerOrder:
            if layer_name in vectorLayerDict:
                order.insert(count, vectorLayerDict[layer_name])
                count += 1
        root.setCustomLayerOrder(order)
        root.setHasCustomLayerOrder(True)
