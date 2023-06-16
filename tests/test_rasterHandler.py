# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import sys
import unittest
from unittest.mock import MagicMock
from osgeo import gdal, ogr
from osgeo.gdal import Dataset
from qgis.core import (
    QgsFields,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPoint,
)
import numpy as np

from DsgTools.core.GeometricTools import rasterHandler
from DsgTools.core.GeometricTools.affine import Affine


class TestRasterHandler(unittest.TestCase):
    def setUp(self):
        # Create a mock QgsRasterLayer
        self.mockRasterLayer = MagicMock(spec=QgsRasterLayer)
        self.mockRasterDataProvider = MagicMock()
        self.mockRasterDataProvider.dataSourceUri.return_value = "mock_raster.tif"
        self.mockRasterLayer.dataProvider.return_value = self.mockRasterDataProvider

        # Create a mock Dataset
        self.mockDataset = MagicMock(spec=Dataset)

        # Create a mock QgsVectorLayer
        self.mockVectorLayer = MagicMock(spec=QgsVectorLayer)
        self.mockVectorLayer.featureCount.return_value = 2

        # Create mock GeoTransform values
        self.mockGeoTransform = (0, 1, 0, 0, 0, -1)

        # Create mock numpy array
        self.mockNumpyArray = np.array([[1, 2], [3, 4]])

    def tearDown(self):
        pass

    def test_readAsNumpy(self):
        ds, npArray = rasterHandler.readAsNumpy(self.mockRasterLayer)
        self.assertEqual(ds, self.mockDataset)
        self.assertTrue(np.array_equal(npArray, self.mockNumpyArray))

    def test_getCoordinateTransform(self):
        transform = rasterHandler.getCoordinateTransform(self.mockDataset)
        self.assertEqual(transform, Affine.from_gdal(*self.mockGeoTransform))

    def test_getMaxCoordinatesFromNpArray(self):
        maxCoords = rasterHandler.getMaxCoordinatesFromNpArray(self.mockNumpyArray)
        expectedCoords = np.array([[1, 1]])
        self.assertTrue(np.array_equal(maxCoords, expectedCoords))

    def test_getMinCoordinatesFromNpArray(self):
        minCoords = rasterHandler.getMinCoordinatesFromNpArray(self.mockNumpyArray)
        expectedCoords = np.array([[0, 0]])
        self.assertTrue(np.array_equal(minCoords, expectedCoords))

    def test_createFeatureWithPixelValueFromPixelCoordinates(self):
        pixelCoordinates = (0.5, 0.5)
        fieldName = "value"
        fields = QgsFields()
        npRaster = self.mockNumpyArray
        transform = Affine.from_gdal(*self.mockGeoTransform)
        feat = rasterHandler.createFeatureWithPixelValueFromPixelCoordinates(
            pixelCoordinates, fieldName, fields, npRaster, transform
        )
        expectedGeom = QgsGeometry(QgsPoint(0.5, -0.5))
        expectedFeat = QgsFeature(fields)
        expectedFeat.setGeometry(expectedGeom)
        expectedFeat[fieldName] = 1
        self.assertEqual(feat, expectedFeat)

    def test_createFeatureListWithPixelValuesFromPixelCoordinatesArray(self):
        pixelCoordinates = np.array([[0.5, 0.5], [1.5, 1.5]])
        fieldName = "value"
        fields = QgsFields()
        npRaster = self.mockNumpyArray
        transform = Affine.from_gdal(*self.mockGeoTransform)
        featList = (
            rasterHandler.createFeatureListWithPixelValuesFromPixelCoordinatesArray(
                pixelCoordinates, fieldName, fields, npRaster, transform
            )
        )
        expectedGeom1 = QgsGeometry(QgsPoint(0.5, -0.5))
        expectedFeat1 = QgsFeature(fields)
        expectedFeat1.setGeometry(expectedGeom1)
        expectedFeat1[fieldName] = 1
        expectedGeom2 = QgsGeometry(QgsPoint(1.5, -1.5))
        expectedFeat2 = QgsFeature(fields)
        expectedFeat2.setGeometry(expectedGeom2)
        expectedFeat2[fieldName] = 4
        self.assertEqual(len(featList), 2)
        self.assertEqual(featList[0], expectedFeat1)
        self.assertEqual(featList[1], expectedFeat2)

    def test_createFeatureWithPixelValueFromTerrainCoordinates(self):
        terrainCoordinates = (0.5, -0.5)
        fieldName = "value"
        fields = QgsFields()
        npRaster = self.mockNumpyArray
        transform = Affine.from_gdal(*self.mockGeoTransform)
        feat = rasterHandler.createFeatureWithPixelValueFromTerrainCoordinates(
            terrainCoordinates, fieldName, fields, npRaster, transform
        )
        expectedGeom = QgsGeometry(QgsPoint(0.5, -0.5))
        expectedFeat = QgsFeature(fields)
        expectedFeat.setGeometry(expectedGeom)
        expectedFeat[fieldName] = 1
        self.assertEqual(feat, expectedFeat)

    def test_buildNumpyNodataMask(self):
        mockRasterLayer = MagicMock(spec=QgsRasterLayer)
        mockRasterLayer.rasterUnitsPerPixelX.return_value = 1
        mockRasterLayer.rasterUnitsPerPixelY.return_value = 1
        mockRasterLayer.extent.return_value.toRectF.return_value.getCoords.return_value = (
            0,
            0,
            2,
            2,
        )
        mockVectorLayer = MagicMock(spec=QgsVectorLayer)
        mockVectorLayer.featureCount.return_value = 2
        npRaster = rasterHandler.buildNumpyNodataMask(mockRasterLayer, mockVectorLayer)
        expectedNpRaster = np.array([[np.nan, np.nan], [np.nan, np.nan]])
        self.assertTrue(np.array_equal(npRaster, expectedNpRaster))


def run_all():
    """Default function that is called by the runner if nothing else is specified"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestRasterHandler, "test"))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
