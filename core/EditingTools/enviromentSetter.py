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
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

class EnviromentSetter:
    def __init__(self, iface, parent=None):
        self.layerFactory = LayerLoaderFactory()
        self.iface = iface
    
    def setEnviroment(self, parameterDict):
        """
        :param parameterDict (dict): dictionary with parameters to set de Editing Enviroment.
        parameterDict = {
            'abstractDb' : database,
            'layerList': [list of layer names, ordered by exibition],
            'stylePath' : path of the style
        }
        """
        #Step 1: Load layers
        layerLoader = self.layerFactory.makeLoader(self.iface, parameterDict['abstractDb'])
        loadedLayerDict = layerLoader.loadedLayers(
            inputList=parameterDict['layerList'],
            stylePath=parameterDict['stylePath'],
            loadEditingStructure=True
        )
        self.setLayerOrdering(loadedLayerDict, parameterDict['layerList'])
    
    def createGrid(self, extents):
        """
        :param extents: [xmin, ymin, xmax, ymax]
        Creates the grid of 
        }
        """
        pass
    
    def setWorkArea(self, extents):
        """
        :param extents: [xmin, ymin, xmax, ymax]
        """
        pass
    
    def setLayerOrdering(self, vectorLayerList, layerOrder):
        """
        :param vectorLayerList: list of QgsVectorLayers,
        :param layerOrder: order of each layer
        """
        pass