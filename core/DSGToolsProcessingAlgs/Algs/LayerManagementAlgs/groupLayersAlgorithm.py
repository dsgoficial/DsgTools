# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba -
                                    Cartographic Engineer @ Brazilian Army
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

from qgis.core import (QgsDataSourceUri, QgsExpression, QgsExpressionContext,
                       QgsExpressionContextUtils, QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString, QgsProject)
from qgis.utils import iface


class GroupLayersAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm to group layers according to primitive, dataset and a category.
    INPUT_LAYERS: list of QgsVectorLayer
    CATEGORY_TOKEN: token used to split layer name
    CATEGORY_TOKEN_INDEX: index of the split list
    OUTPUT: list of outputs
    """
    INPUT_LAYERS = 'INPUT_LAYERS'
    CATEGORY_EXPRESSION = 'CATEGORY_EXPRESSION'
    OUTPUT = 'OUTPUT'
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input Layers'),
                QgsProcessing.TypeVector
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.CATEGORY_EXPRESSION,
                self.tr('Expression used to find out the category'),
                defaultValue="regexp_substr(@layer_name ,'([^_]+)')"
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
        categoryExpression = self.parameterAsExpression(
            parameters,
            self.CATEGORY_EXPRESSION,
            context
        ) 
        listSize = len(inputLyrList)
        progressStep = 100/listSize if listSize else 0
        rootNode = QgsProject.instance().layerTreeRoot()
        inputLyrList.sort(key=lambda x: (x.geometryType(), x.name()))
        geometryNodeDict = {
            0 : self.tr('Point'),
            1 : self.tr('Line'),
            2 : self.tr('Polygon'),
            4 : self.tr('Non spatial')
        }
        iface.mapCanvas().freeze(True)
        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            rootDatabaseNode = self.getLayerRootNode(lyr, rootNode)
            geometryNode = self.createGroup(
                geometryNodeDict[lyr.geometryType()],
                rootDatabaseNode
            )
            categoryNode = self.getLayerCategoryNode(
                lyr,
                geometryNode,
                categoryExpression
            )
            lyrNode = rootNode.findLayer(lyr.id())
            myClone = lyrNode.clone()
            categoryNode.addChildNode(myClone)
            # not thread safe, must set flag to FlagNoThreading
            rootNode.removeChildNode(lyrNode)
            feedback.setProgress(current*progressStep)
        iface.mapCanvas().freeze(False)
        return {self.OUTPUT: [i.id() for i in inputLyrList]}

    def getLayerRootNode(self, lyr, rootNode):
        """
        Finds the database name of the layer and creates (if not exists)
        a node with the found name.
        lyr: (QgsVectorLayer)
        rootNode: (node item)
        """
        uriText = lyr.dataProvider().dataSourceUri()
        candidateUri = QgsDataSourceUri(uriText)
        rootNodeName = candidateUri.database()
        if not rootNodeName:
            rootNodeName = self.getRootNodeName(uriText)
        #creates database root
        return self.createGroup(rootNodeName, rootNode)

    def getRootNodeName(self, uriText):
        """
        Gets root node name from uri according to provider type.
        """
        if 'memory?' in uriText:
            rootNodeName = 'memory'
        elif 'dbname' in uriText:
            rootNodeName = uriText.replace('dbname=', '').split(' ')[0]
        elif '|' in uriText:
            rootNodeName = os.path.dirname(uriText.split(' ')[0].split('|')[0])
        else:
            rootNodeName = 'unrecognised_format'
        return rootNodeName

    def getLayerCategoryNode(self, lyr, rootNode, categoryExpression):
        """
        Finds category node based on category expression
        and creates it (if not exists a node)
        """
        exp = QgsExpression(categoryExpression)
        context = QgsExpressionContext()
        context.appendScopes(
            QgsExpressionContextUtils.globalProjectLayerScopes(lyr)
        )
        if exp.hasParserError():
            raise Exception(exp.parserErrorString())
        if exp.hasEvalError():
            raise ValueError(exp.evalErrorString())
        categoryText = exp.evaluate(context)
        return self.createGroup(categoryText, rootNode)

    def createGroup(self, groupName, rootNode):
        """
        Create group with the name groupName and parent rootNode.
        """
        groupNode = rootNode.findGroup(groupName)
        return groupNode if groupNode else rootNode.addGroup(groupName)

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
        """
        Translates input string.
        """
        return QCoreApplication.translate('GroupLayersAlgorithm', string)

    def createInstance(self):
        """
        Creates an instance of this class
        """
        return GroupLayersAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
