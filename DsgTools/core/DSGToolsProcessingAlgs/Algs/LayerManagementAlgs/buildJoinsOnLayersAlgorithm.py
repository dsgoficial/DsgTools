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

from qgis.core import (
    QgsDataSourceUri,
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterExpression,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProject,
    QgsRelation,
    QgsVectorLayerJoinInfo,
)
from qgis.utils import iface


class BuildJoinsOnLayersAlgorithm(QgsProcessingAlgorithm):
    """
    Algorithm to join layers according to its relations.
    INPUT_LAYERS: list of QgsVectorLayer
    START_EDITING: starts edition of related layer if true
    OUTPUT: list of outputs
    """

    INPUT_LAYERS = "INPUT_LAYERS"
    START_EDITING = "START_EDITING"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS, self.tr("Input Layers"), QgsProcessing.TypeVector
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.START_EDITING, self.tr("Start Editing"), defaultValue=True
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT, self.tr("Original reorganized layers")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        startEditing = self.parameterAsBoolean(parameters, self.START_EDITING, context)
        listSize = len(inputLyrList)
        progressStep = 100 / listSize if listSize else 0
        relationManager = QgsProject.instance().relationManager()
        for current, relation in enumerate(
            relationManager.discoverRelations([], inputLyrList)
        ):
            if feedback.isCanceled():
                break
            if relation.strength() != QgsRelation.Association:
                continue
            originalLyr = relation.referencingLayer()
            joinnedLyr = relation.referencedLayer()
            originalLyrFieldName, joinLyrFieldName = [
                (k, v) for k, v in relation.fieldPairs().items()
            ][0]
            self.buildJoin(
                originalLyr,
                originalLyrFieldName,
                joinnedLyr,
                joinLyrFieldName,
                startEdit=startEditing,
            )
            feedback.setProgress(current * progressStep)
        return {self.OUTPUT: [i.id() for i in inputLyrList]}

    def buildJoin(
        self,
        originalLyr,
        originalLyrFieldName,
        joinnedLyr,
        joinLyrFieldName,
        startEdit=False,
    ):
        """
        Builds a join bewteen lyr and joinnedLyr.
        :param originalLyr: QgsVectorLayer original layer;
        :param originalLyrFieldName: (str) name of the field;
        :param joinnedLyr: QgsVectorLayer lyr to be joinned to originalLayer;
        :param joinLyrFieldName: (str) name of the join field name (usually primary key of joinnedLyr)
        """
        joinObject = QgsVectorLayerJoinInfo()
        joinObject.setJoinFieldName(joinLyrFieldName)
        joinObject.setTargetFieldName(originalLyrFieldName)
        if startEdit:
            joinnedLyr.startEditing()
        joinObject.setJoinLayer(joinnedLyr)
        # joinObject.setJoinFieldNamesSubset([])
        joinObject.setUpsertOnEdit(True)  # set to enable edit on original lyr
        joinObject.setCascadedDelete(True)
        joinObject.setDynamicFormEnabled(True)
        joinObject.setEditable(True)
        joinObject.setUsingMemoryCache(True)
        originalLyr.addJoin(joinObject)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "buildjoinsonlayersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Build Joins on Layers")

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
        return QCoreApplication.translate("BuildJoinsOnLayersAlgorithm", string)

    def createInstance(self):
        """
        Creates an instance of this class
        """
        return BuildJoinsOnLayersAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
