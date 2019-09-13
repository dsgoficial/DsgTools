# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-26
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
import os

from PyQt5.QtCore import QCoreApplication

from qgis.core import (QgsDataSourceUri, QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProject)
class GroupLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    CATEGORY_TOKEN = 'CATEGORY_TOKEN'
    CATEGORY_TOKEN_INDEX = 'CATEGORY_TOKEN_INDEX'
    OUTPUT = 'OUTPUT'
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input Layers'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.CATEGORY_TOKEN,
                self.tr('Category Token'),
                defaultValue='_'
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CATEGORY_TOKEN_INDEX,
                self.tr('Category token index'),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=0
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Original reorganized layers')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        categoryToken = self.parameterAsString(
            parameters,
            self.CATEGORY_TOKEN,
            context
        )
        categoryTokenIndex = self.parameterAsInt(
            parameters,
            self.CATEGORY_TOKEN_INDEX,
            context
        )
        listSize = len(inputLyrList)
        progressStep = 100/listSize if listSize else 0
        rootNode = QgsProject.instance().layerTreeRoot()
        rootNodeSet = set()
        inputLyrList.sort(key=lambda x: (x.geometryType(), x.name()))
        geometryNodeDict = {
            0 : self.tr('Point'),
            1 : self.tr('Line'),
            2 : self.tr('Polygon')
        }
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            rootDatabaseNode = self.getLayerRootNode(lyr, rootNode)
            rootNodeSet.add(rootDatabaseNode)
            geometryNode = self.createGroup(
                geometryNodeDict[lyr.geometryType()],
                rootDatabaseNode
            )
            categoryNode = self.getLayerCategoryNode(
                lyr,
                geometryNode,
                categoryToken,
                categoryTokenIndex
            )
            lyrNode = rootNode.findLayer(lyr.id())
            myClone = lyrNode.clone()
            categoryNode.addChildNode(myClone)
            rootNode.removeChildNode(lyrNode) # not thread safe, must set flag to FlagNoThreading
            feedback.setProgress(current*progressStep)

        return {self.OUTPUT: inputLyrList}
    
    def getLayerRootNode(self, lyr, rootNode):
        uriText = lyr.dataProvider().dataSourceUri()
        candidateUri = QgsDataSourceUri(uriText)
        rootNodeName = candidateUri.database()
        if not rootNodeName:
            rootNodeName = self.getRootNodeName(uriText)
        #creates database root
        return self.createGroup(rootNodeName, rootNode)
    
    def getRootNodeName(self, uriText):
        if 'memory?' in uriText:
            rootNodeName = 'memory'
        elif 'dbname' in uriText:
            rootNodeName = uriText.replace('dbname=','').split(' ')[0]
        elif '|' in uriText:
            rootNodeName = os.path.dirname(uriText.split(' ')[0].split('|')[0])
        else:
            rootNodeName = 'unrecognised_format'
        return rootNodeName

    def getLayerCategoryNode(self, lyr, rootNode, categoryToken, categoryTokenIndex):
        categorySplit = lyr.name().split(categoryToken)
        categoryText = categorySplit[categoryTokenIndex] if categoryTokenIndex <= len(categorySplit) else 0
        return self.createGroup(categoryText, rootNode)

    def createGroup(self, groupName, rootNode):
        groupNode = rootNode.findGroup(groupName)
        if groupNode:
            return groupNode
        else:
            return rootNode.addGroup(groupName)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'grouplayers'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Group Layers')

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
        return QCoreApplication.translate('GroupLayersAlgorithm', string)

    def createInstance(self):
        return GroupLayersAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode method
        from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
