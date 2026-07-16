# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import networkx as nx
from qgis.core import QgsFeature, QgsGeometry

from DsgTools.core.GeometricTools.terrainHandler import TerrainModel, TerrainSlice


def squareRing(xmin, ymin, xmax, ymax):
    """
    Builds a closed LineString geometry for the given bounding box.
    """
    return QgsGeometry.fromWkt(
        "LineString ({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1})".format(
            xmin, ymin, xmax, ymax
        )
    )


def squarePolygon(xmin, ymin, xmax, ymax):
    return QgsGeometry.fromWkt(
        "Polygon (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))".format(
            xmin, ymin, xmax, ymax
        )
    )


def ringWithHole(outer, inner):
    """
    Builds a polygon for the band between two nested squares.
    """
    outerPoly = squarePolygon(*outer)
    innerPoly = squarePolygon(*inner)
    return outerPoly.difference(innerPoly)


class TerrainModelStub(TerrainModel):
    """
    TerrainModel is a dataclass whose __post_init__ runs the whole contour
    preparation pipeline (merge, clip, polygonize...). These tests target the
    pure decision logic, so the instance is built without __post_init__ and the
    structures it would have produced are injected directly.
    """

    def __init__(
        self,
        contourElevationFieldName="cota",
        spotElevationFieldName="cota",
        threshold=10,
    ):
        self.nx = nx
        self.contourElevationFieldName = contourElevationFieldName
        self.spotElevationFieldName = spotElevationFieldName
        self.threshold = threshold
        self.depressionExpression = ''' "depressao" = 1 '''
        self.depressionIdSet = set()
        self.terrainGraph = nx.Graph()
        self.terrainSlicesDict = dict()
        self.contourFeatCache = dict()
        self.ringGeomCache = dict()

    def addContour(self, contourid, geom):
        feat = QgsFeature()
        feat.setGeometry(geom)
        self.contourFeatCache[contourid] = feat

    def addBand(self, polygonid, geom):
        feat = QgsFeature()
        feat.setGeometry(geom)
        self.terrainSlicesDict[polygonid] = TerrainSlice(
            polygonid=polygonid,
            polygonFeat=feat,
            contourElevationFieldName=self.contourElevationFieldName,
            threshold=self.threshold,
            contoursOnSlice=set(),
            contourIdField="contourid",
        )

    def addContourEdge(self, bandA, bandB, contourid, height, is_closed=True):
        self.terrainGraph.add_edge(
            bandA,
            bandB,
            contourid=contourid,
            height=height,
            is_closed=is_closed,
        )


class HilltopModelMixin:
    """
    A plain hill inside a map frame, built out of two nested closed contours:

        +-------------------------+  frame
        |   +-----------------+   |
        |   |   +---------+   |   |  contour 90  (ring id 90)
        |   |   |  cap    |   |   |  contour 100 (ring id 100)
        |   |   +---------+   |   |
        |   +-----------------+   |
        +-------------------------+

    band 1 = cap, inside contour 100 (terrain goes UP, 100 -> 110)
    band 2 = annulus between contours 100 and 90
    band 3 = outer region, outside contour 90 (terrain goes DOWN, 90 -> 80)
    """

    def buildHill(self):
        model = TerrainModelStub()
        model.addContour(100, squareRing(40, 40, 60, 60))
        model.addContour(90, squareRing(20, 20, 80, 80))
        model.addBand(1, squarePolygon(40, 40, 60, 60))
        model.addBand(2, ringWithHole((20, 20, 80, 80), (40, 40, 60, 60)))
        model.addBand(3, ringWithHole((0, 0, 100, 100), (20, 20, 80, 80)))
        model.addContourEdge(1, 2, contourid=100, height=100)
        model.addContourEdge(2, 3, contourid=90, height=90)
        return model


class DepressionModelMixin:
    """
    A closed depression inside a map frame:

    band 1 = pit, inside contour 90 (terrain goes DOWN, 90 -> 80)
    band 2 = annulus between contours 90 and 100
    band 3 = outer region, outside contour 100

    The terrain descends when moving inside BOTH rings (100 -> 90 -> pit), so
    both contours delimit the depression and both are expected to carry
    depressao = 1, not only the innermost one.
    """

    def buildDepression(self):
        model = TerrainModelStub()
        model.addContour(90, squareRing(40, 40, 60, 60))
        model.addContour(100, squareRing(20, 20, 80, 80))
        model.addBand(1, squarePolygon(40, 40, 60, 60))
        model.addBand(2, ringWithHole((20, 20, 80, 80), (40, 40, 60, 60)))
        model.addBand(3, ringWithHole((0, 0, 100, 100), (20, 20, 80, 80)))
        model.addContourEdge(1, 2, contourid=90, height=90)
        model.addContourEdge(2, 3, contourid=100, height=100)
        return model


class GetClosedCapContourIdTestCase(unittest.TestCase, HilltopModelMixin):
    def test_cap_band_is_recognized(self):
        model = self.buildHill()
        self.assertEqual(model.getClosedCapContourId(1), 100)

    def test_outer_band_is_not_a_cap(self):
        """
        Band 3 has degree 1 and its contour is closed, but it lies OUTSIDE the
        ring, so it must not be treated as the innermost band of a hilltop.
        """
        model = self.buildHill()
        self.assertIsNone(model.getClosedCapContourId(3))

    def test_intermediate_band_is_not_a_cap(self):
        model = self.buildHill()
        self.assertIsNone(model.getClosedCapContourId(2))

    def test_open_contour_is_not_a_cap(self):
        model = self.buildHill()
        model.terrainGraph[1][2]["is_closed"] = False
        self.assertIsNone(model.getClosedCapContourId(1))

    def test_band_missing_from_graph(self):
        model = self.buildHill()
        self.assertIsNone(model.getClosedCapContourId(42))


class IsDepressionContourTestCase(
    unittest.TestCase, HilltopModelMixin, DepressionModelMixin
):
    def test_hill_cap_contour_is_not_a_depression(self):
        model = self.buildHill()
        self.assertFalse(model.isDepressionContour(1, 2))

    def test_hill_outer_contour_is_not_a_depression(self):
        model = self.buildHill()
        self.assertFalse(model.isDepressionContour(2, 3))

    def test_depression_cap_contour_is_a_depression(self):
        model = self.buildDepression()
        self.assertTrue(model.isDepressionContour(1, 2))

    def test_depression_outer_contour_is_a_depression(self):
        model = self.buildDepression()
        self.assertTrue(model.isDepressionContour(2, 3))

    def test_open_contour_is_undetermined(self):
        model = self.buildHill()
        model.terrainGraph[2][3]["is_closed"] = False
        self.assertIsNone(model.isDepressionContour(2, 3))

    def test_equal_neighbour_heights_are_undetermined(self):
        """
        A ring wrapping another ring of the same height says nothing about which
        way the terrain runs.
        """
        model = self.buildHill()
        model.terrainGraph[1][2]["height"] = 90
        self.assertIsNone(model.isDepressionContour(2, 3))


class ValidateDepressionAttributionTestCase(
    unittest.TestCase, HilltopModelMixin, DepressionModelMixin
):
    def test_hill_correctly_attributed_yields_no_flag(self):
        model = self.buildHill()
        self.assertEqual(model.validateDepressionAttribution(), dict())

    def test_hill_outer_band_is_not_flagged_as_depression(self):
        """
        Regression: band 3 is outside contour 90 and all of its neighbour
        heights are higher, which used to be misread as a depression.
        """
        model = self.buildHill()
        flags = model.validateDepressionAttribution()
        self.assertNotIn(model.contourFeatCache[90].geometry().asWkb(), flags)

    def test_hill_cap_wrongly_marked_as_depression_is_flagged(self):
        model = self.buildHill()
        model.depressionIdSet = {100}
        flags = model.validateDepressionAttribution()
        self.assertEqual(len(flags), 1)
        self.assertIn("marked as depression", list(flags.values())[0])

    def test_depression_correctly_attributed_yields_no_flag(self):
        model = self.buildDepression()
        model.depressionIdSet = {90, 100}
        self.assertEqual(model.validateDepressionAttribution(), dict())

    def test_depression_not_marked_is_flagged(self):
        model = self.buildDepression()
        model.depressionIdSet = set()
        flags = model.validateDepressionAttribution()
        self.assertEqual(len(flags), 2)
        self.assertIn(model.contourFeatCache[90].geometry().asWkb(), flags)
        self.assertIn(model.contourFeatCache[100].geometry().asWkb(), flags)
        for message in flags.values():
            self.assertIn("not marked as depression", message)

    def test_outer_depression_contour_is_checked(self):
        """
        Only the innermost contour used to be validated, so a depression whose
        outer ring lost its attribute went unnoticed.
        """
        model = self.buildDepression()
        model.depressionIdSet = {90}
        flags = model.validateDepressionAttribution()
        self.assertEqual(len(flags), 1)
        self.assertIn(model.contourFeatCache[100].geometry().asWkb(), flags)
        self.assertIn("not marked as depression", list(flags.values())[0])

    def test_hill_nested_contour_wrongly_marked_is_flagged(self):
        """
        Contour 90 wraps contour 100, so the terrain ascends inside it: it is a
        hilltop contour and must not carry the depression attribute.
        """
        model = self.buildHill()
        model.depressionIdSet = {90}
        flags = model.validateDepressionAttribution()
        self.assertEqual(len(flags), 1)
        self.assertIn(model.contourFeatCache[90].geometry().asWkb(), flags)
        self.assertIn("marked as depression", list(flags.values())[0])


class SpotElevationRangeTestCase(
    unittest.TestCase, HilltopModelMixin, DepressionModelMixin
):
    """
    Band 1 of the hill is capped by contour 100, so a spot elevation inside it
    must be between 100 and 110. Band 1 of the depression is capped by contour
    90, so a spot elevation inside it must be between 80 and 90.
    """

    def test_spot_elevation_inside_hilltop_cap_is_accepted(self):
        model = self.buildHill()
        self.assertIsNone(model.getSpotElevationFlagText(1, 105, 100, 100))

    def test_spot_elevation_below_hilltop_cap_is_flagged(self):
        """
        Regression: 95 sits inside a cap closed by contour 100, so the terrain
        there is necessarily above 100. The permissive +/- threshold range used
        to accept it.
        """
        model = self.buildHill()
        text = model.getSpotElevationFlagText(1, 95, 100, 100)
        self.assertIsNotNone(text)
        self.assertIn("hilltop", text)

    def test_spot_elevation_above_hilltop_cap_range_is_flagged(self):
        model = self.buildHill()
        self.assertIsNotNone(model.getSpotElevationFlagText(1, 115, 100, 100))

    def test_spot_elevation_inside_depression_cap_is_accepted(self):
        model = self.buildDepression()
        model.depressionIdSet = {90}
        self.assertIsNone(model.getSpotElevationFlagText(1, 85, 90, 90))

    def test_spot_elevation_above_depression_cap_is_flagged(self):
        """
        95 inside a depression closed by contour 90 is below the terrain floor.
        """
        model = self.buildDepression()
        model.depressionIdSet = {90}
        text = model.getSpotElevationFlagText(1, 95, 90, 90)
        self.assertIsNotNone(text)
        self.assertIn("depression", text)

    def test_spot_elevation_on_regular_band_uses_bounding_contours(self):
        model = self.buildHill()
        self.assertIsNone(model.getSpotElevationFlagText(2, 95, 90, 100))
        self.assertIsNotNone(model.getSpotElevationFlagText(2, 105, 90, 100))
        self.assertIsNotNone(model.getSpotElevationFlagText(2, 85, 90, 100))

    def test_non_cap_band_with_equal_heights_keeps_permissive_range(self):
        """
        A saddle band bounded by two contours of the same height gives no clue
        about the terrain direction, so only the permissive range is checked.
        """
        model = self.buildHill()
        self.assertIsNone(model.getSpotElevationFlagText(3, 85, 90, 90))
        self.assertIsNone(model.getSpotElevationFlagText(3, 95, 90, 90))
        self.assertIsNotNone(model.getSpotElevationFlagText(3, 105, 90, 90))


def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    # unittest.makeSuite was removed on Python 3.13, which is what QGIS 4 ships
    loader = unittest.TestLoader()
    loader.testMethodPrefix = filterString
    suite = unittest.TestSuite()
    for testCase in (
        GetClosedCapContourIdTestCase,
        IsDepressionContourTestCase,
        ValidateDepressionAttributionTestCase,
        SpotElevationRangeTestCase,
    ):
        suite.addTests(loader.loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
