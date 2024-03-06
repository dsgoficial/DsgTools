# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-03-06
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from collections import defaultdict
import itertools
import json
import os

import concurrent.futures
from osgeo import gdal, ogr
import numpy as np
import numpy.ma as ma

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools import rasterHandler

from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingException,
    QgsProcessingParameterDistance,
    QgsProcessingMultiStepFeedback,
    QgsProcessingFeatureSourceDefinition,
    QgsGeometry,
    QgsProcessingParameterString,
    QgsProcessingParameterNumber,
    QgsProcessingParameterExpression,
    QgsFeatureRequest,
    QgsProcessingContext,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
)


class ReclassifyAdjacentPixelsToNearestNeighborAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    VALUES = "VALUES"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr("Input Single Band Image"),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.VALUES,
                self.tr("Comma separated values")
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT, self.tr("Output Raster")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python scipy library. Please install this library and try again."
                )
            )
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        valueStr = self.parameterAsString(parameters, self.VALUES, context)
        valueList = list(map(int, valueStr.split(",")))
        outputRaster = self.parameterAsOutputLayer(
            parameters, self.OUTPUT, context
        )
        nValues = len(valueList)
        if nValues == 0:
            return {self.OUTPUT: outputRaster} 
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Reading input numpy array"))

        ds = gdal.Open(str(inputRaster.source()))
        npRaster = np.array(ds.GetRasterBand(1).ReadAsArray(), dtype=np.int8)
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Masking values"))
        stepSize = 100/nValues
        for current, v in enumerate(valueList):
            if multiStepFeedback.isCanceled():
                return {self.OUTPUT: outputRaster}
            npRaster = ma.masked_array(npRaster, npRaster==v, dtype=np.int8)
            multiStepFeedback.setProgress(current * stepSize)
        
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Computing grid"))
        x, y =np.mgrid[0:npRaster.shape[0],0:npRaster.shape[1]]

        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr("Evaluating grid values"))
        xygood = np.array((x[~npRaster.mask],y[~npRaster.mask])).T
        xybad = np.array((x[npRaster.mask],y[npRaster.mask])).T

        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo(self.tr("Building output masked numpy array"))
        npRaster[npRaster.mask] = npRaster[~npRaster.mask][KDTree(xygood).query(xybad)[1]]

        multiStepFeedback.setCurrentStep(5)
        multiStepFeedback.pushInfo(self.tr("Writing output"))
        rasterHandler.writeOutputRaster(outputRaster, npRaster, ds)

        return {self.OUTPUT: outputRaster}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "reclassifyadjacentpixelstonearestneighboralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Reclassify Adjacent Pixels to Nearest Neighbor Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Generalization Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ReclassifyAdjacentPixelsToNearestNeighborAlgorithm", string)

    def createInstance(self):
        return ReclassifyAdjacentPixelsToNearestNeighborAlgorithm()
