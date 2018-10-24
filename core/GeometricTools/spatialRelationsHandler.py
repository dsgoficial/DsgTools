# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-05-01
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
from __future__ import absolute_import
from builtins import range
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, \
                      QgsCoordinateTransform, QgsWkbTypes, edit, QgsCoordinateReferenceSystem, QgsProject, \
                      QgsProcessingMultiStepFeedback
from qgis.PyQt.Qt import QObject, QVariant
from qgis.analysis import QgsGeometrySnapper, QgsInternalGeometrySnapper

from .featureHandler import FeatureHandler
from .geometryHandler import GeometryHandler

class SpatialRelationsHandler(QObject):
    def __init__(self, iface = None, parent = None):
        super(SpatialRelationsHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.featureHandler = FeatureHandler(iface)
        self.geometryHandler = GeometryHandler(iface)
    
    def relateDrainagesWithContours(self, drainageLyr, contourLyr, frameLinesLyr, threshold, topologyRadius, feedback=None):
        """
        Checks the conformity between directed drainages and contours.
        :param drainageLyr: QgsVectorLayer (line) with drainage lines
        :param contourLyr: QgsVectorLayer (line) with contour lines
        :param frameLinesLyrLyr: QgsVectorLayer (line) with frame lines
        :param threshold: (int) equidistance between contour lines
        :param threshold: (float) topology radius
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(self.tr('Building drainage spatial index...'))
        drainageSpatialIdx, drainageIdDict = self.featureHandler.buildSpatialIndexAndIdDict
        (
            inputLyr=drainageLyr,
            feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(self.tr('Building contour spatial index...'))
        contourSpatialIdx, contourIdDict = self.featureHandler.buildSpatialIndexAndIdDict
        (
            inputLyr=contourLyr,
            feedback=multiStepFeedback
        )