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

import numpy as np
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsField, QgsFields

from DsgTools.core.GeometricTools.affine import Affine
from DsgTools.core.GeometricTools.rasterHandler import (
    createFeatureWithPixelValueFromPixelCoordinates,
    findNearbyNonMultiplePixel,
    maskContourIntervalMultiples,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.extractElevationPoints import (
    ExtractElevationPoints,
)

INTERVAL = 10


def cotaFields():
    fields = QgsFields()
    fields.append(QgsField("cota", QVariant.Int))
    return fields


def identityTransform():
    return Affine(1.0, 0.0, 0.0, 0.0, -1.0, 0.0)


class FindNearbyNonMultiplePixelTestCase(unittest.TestCase):
    """
    Um ponto cotado nunca pode ter o valor de uma curva de nível, então um pixel
    que caia num múltiplo da equidistância é deslocado para o vizinho não múltiplo
    mais próximo. Quando não existe vizinho utilizável, a resposta correta é "não
    há ponto a gerar aqui", e não o múltiplo original.
    """

    def test_pixel_que_nao_e_multiplo_fica_onde_esta(self):
        npRaster = np.full((11, 11), 104.0)
        self.assertEqual(findNearbyNonMultiplePixel((5, 5), npRaster, INTERVAL), (5, 5))

    def test_desloca_para_vizinho_nao_multiplo(self):
        npRaster = np.full((11, 11), 100.0)
        npRaster[5, 6] = 104.0
        coords = findNearbyNonMultiplePixel((5, 5), npRaster, INTERVAL)
        self.assertEqual(coords, (5, 6))
        self.assertNotEqual(int(npRaster[coords]) % INTERVAL, 0)

    def test_plato_plano_em_cota_redonda_nao_gera_ponto(self):
        """
        Regressão: devolvia o próprio pixel múltiplo, gerando a cota proibida.
        """
        npRaster = np.full((11, 11), 100.0)
        self.assertIsNone(findNearbyNonMultiplePixel((5, 5), npRaster, INTERVAL))

    def test_nao_multiplo_fora_do_raio_de_busca_nao_gera_ponto(self):
        npRaster = np.full((31, 31), 100.0)
        npRaster[0, 0] = 105.0
        self.assertIsNone(findNearbyNonMultiplePixel((15, 15), npRaster, INTERVAL))

    def test_intervalo_zero_desliga_a_regra(self):
        npRaster = np.full((11, 11), 100.0)
        self.assertEqual(findNearbyNonMultiplePixel((5, 5), npRaster, 0), (5, 5))


class CreateFeatureWithPixelValueTestCase(unittest.TestCase):
    def test_feicao_descartada_quando_nao_ha_pixel_valido(self):
        npRaster = np.full((11, 11), 100.0)
        feat = createFeatureWithPixelValueFromPixelCoordinates(
            (5, 5),
            "cota",
            cotaFields(),
            npRaster,
            identityTransform(),
            contourHeightInterval=INTERVAL,
        )
        self.assertIsNone(feat)

    def test_feicao_criada_no_vizinho_valido(self):
        npRaster = np.full((11, 11), 100.0)
        npRaster[5, 6] = 104.0
        feat = createFeatureWithPixelValueFromPixelCoordinates(
            (5, 5),
            "cota",
            cotaFields(),
            npRaster,
            identityTransform(),
            contourHeightInterval=INTERVAL,
        )
        self.assertIsNotNone(feat)
        self.assertEqual(feat["cota"], 104)


class MaskContourIntervalMultiplesTestCase(unittest.TestCase):
    def test_multiplos_viram_nan(self):
        npRaster = np.array([[100.0, 103.0], [107.0, 110.0]])
        out = maskContourIntervalMultiples(npRaster, INTERVAL)
        self.assertTrue(np.isnan(out[0, 0]))
        self.assertTrue(np.isnan(out[1, 1]))
        self.assertEqual(out[0, 1], 103.0)
        self.assertEqual(out[1, 0], 107.0)

    def test_intervalo_zero_devolve_intacto(self):
        npRaster = np.array([[100.0, 110.0]])
        out = maskContourIntervalMultiples(npRaster, 0)
        self.assertTrue(np.array_equal(out, npRaster))


class DropContourIntervalMultiplesTestCase(unittest.TestCase):
    """
    Rede final antes da única escrita no sink: mesmo que uma proteção a montante
    deixe passar (a máscara desiste quando todo pixel é múltiplo), a saída não pode
    conter cota múltipla da equidistância.
    """

    def setUp(self):
        self.alg = ExtractElevationPoints()
        self.fields = cotaFields()

    def featList(self, cotas):
        out = []
        for cota in cotas:
            feat = QgsFeature(self.fields)
            feat["cota"] = cota
            out.append(feat)
        return out

    def test_descarta_multiplos_e_mantem_o_resto(self):
        kept = self.alg.dropContourIntervalMultiples(
            self.featList([100, 105, 110, 97, 120]), INTERVAL
        )
        self.assertEqual([f["cota"] for f in kept], [105, 97])

    def test_nada_a_descartar(self):
        kept = self.alg.dropContourIntervalMultiples(
            self.featList([101, 105, 109]), INTERVAL
        )
        self.assertEqual([f["cota"] for f in kept], [101, 105, 109])

    def test_todos_multiplos_resulta_em_lista_vazia(self):
        kept = self.alg.dropContourIntervalMultiples(
            self.featList([100, 110, 120]), INTERVAL
        )
        self.assertEqual(kept, [])

    def test_intervalo_zero_nao_descarta(self):
        kept = self.alg.dropContourIntervalMultiples(self.featList([100, 110]), 0)
        self.assertEqual([f["cota"] for f in kept], [100, 110])

    def test_cota_nula_nao_quebra(self):
        kept = self.alg.dropContourIntervalMultiples(
            self.featList([None, 105]), INTERVAL
        )
        self.assertEqual([f["cota"] for f in kept], [None, 105])


def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    loader = unittest.TestLoader()
    loader.testMethodPrefix = filterString
    suite = unittest.TestSuite()
    for testCase in (
        FindNearbyNonMultiplePixelTestCase,
        CreateFeatureWithPixelValueTestCase,
        MaskContourIntervalMultiplesTestCase,
        DropContourIntervalMultiplesTestCase,
    ):
        suite.addTests(loader.loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
