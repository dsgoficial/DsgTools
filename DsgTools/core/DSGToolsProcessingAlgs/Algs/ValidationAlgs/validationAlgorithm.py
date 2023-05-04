# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsGeometry, QgsFeature, QgsField, QgsProcessingAlgorithm

from qgis.core import (
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsFeature,
    QgsFields,
    QgsProcessingException,
    QgsProject,
)


class ValidationAlgorithm(QgsProcessingAlgorithm):
    """
    Processing algorithm with handy stuff for other algs.
    """

    def getIteratorAndFeatureCount(self, lyr, onlySelected=False):
        """
        Gets the iterator and feature count from lyr.
        """
        try:
            if onlySelected:
                total = (
                    100.0 / lyr.selectedFeatureCount()
                    if lyr.selectedFeatureCount()
                    else 0
                )
                iterator = lyr.getSelectedFeatures()
            else:
                total = 100.0 / lyr.featureCount() if lyr.featureCount() else 0
                iterator = lyr.getFeatures()
            return iterator, total
        except:
            return [], 0

    def prepareFlagSink(self, parameters, source, wkbType, context, addFeatId=False):
        (self.flagSink, self.flag_id) = self.prepareAndReturnFlagSink(
            parameters, source, wkbType, context, self.FLAGS, addFeatId=addFeatId
        )

    def prepareAndReturnFlagSink(
        self, parameters, source, wkbType, context, UI_FIELD, addFeatId=False
    ):
        flagFields = self.getFlagFields(addFeatId=addFeatId)
        (flagSink, flag_id) = self.parameterAsSink(
            parameters,
            UI_FIELD,
            context,
            flagFields,
            wkbType,
            source.sourceCrs() if source is not None else QgsProject.instance().crs(),
        )
        if flagSink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, UI_FIELD))
        return (flagSink, flag_id)

    def getFlagFields(self, addFeatId=False):
        fields = QgsFields()
        fields.append(QgsField("reason", QVariant.String))
        if addFeatId:
            fields.append(QgsField("featid", QVariant.String))
        return fields

    def flagFeature(self, flagGeom, flagText, featid=None, fromWkb=False, sink=None):
        """
        Creates and adds to flagSink a new flag with the reason.
        :param flagGeom: (QgsGeometry) geometry of the flag;
        :param flagText: (string) Text of the flag
        """
        flagSink = self.flagSink if sink is None else sink
        newFeat = QgsFeature(self.getFlagFields(addFeatId=featid is not None))
        newFeat["reason"] = flagText
        if featid is not None:
            newFeat["featid"] = featid
        if fromWkb:
            geom = QgsGeometry()
            geom.fromWkb(flagGeom)
            newFeat.setGeometry(geom)
        else:
            newFeat.setGeometry(flagGeom)
        flagSink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def getFlagsFromOutput(self, output):
        if "FLAGS" not in output:
            return []
        return [i for i in output["FLAGS"].getFeatures()]

    def flagFeaturesFromProcessOutput(self, output):
        if "FLAGS" in output:
            for feat in output["FLAGS"].getFeatures():
                self.flagSink.addFeature(feat, QgsFeatureSink.FastInsert)
