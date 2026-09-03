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

import os
import shutil
import sys
import tempfile
import unittest

import numpy as np
from osgeo import gdal
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFeature, QgsField, QgsFields, QgsGeometry, QgsPointXY

from DsgTools.core.GeometricTools.affine import Affine
from DsgTools.core.GeometricTools.rasterHandler import (
    createFeatureWithPixelValueFromPixelCoordinates,
    createMaxPointFeatFromRasterLayer,
    createMaxPointFeatListFromRasterLayer,
    createMinPointFeatFromRasterLayer,
    findNearbyNonMultiplePixel,
    maskContourIntervalMultiples,
    readAsNumpy,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.extractElevationPoints import (
    ExtractElevationPoints,
)

INTERVAL = 10


NODATA = -9999

# o mesmo mapa que o algoritmo monta no processAlgorithm
DEFAULT_ATTR_MAP = {
    "cota_mais_alta": 2,
    "cota_comprovada": 2,
    "ancora_horizontal": 1,
    "ancora_vertical": 1,
    "suprimir_simbologia": 2,
    "visivel": 1,
}


def cotaFields():
    fields = QgsFields()
    fields.append(QgsField("cota", QVariant.Int))
    return fields


def edgvFields():
    """Os sete campos que o algoritmo escreve no sink."""
    fields = QgsFields()
    fields.append(QgsField("cota", QVariant.Int))
    for name in DEFAULT_ATTR_MAP:
        fields.append(QgsField(name, QVariant.Int))
    return fields


def writeRaster(path, array, nodata=None):
    """Grava um GeoTIFF de uma banda, com o nodata declarado na banda."""
    rows, cols = array.shape
    ds = gdal.GetDriverByName("GTiff").Create(path, cols, rows, 1, gdal.GDT_Float32)
    ds.SetGeoTransform((0.0, 1.0, 0.0, float(rows), 0.0, -1.0))
    band = ds.GetRasterBand(1)
    if nodata is not None:
        band.SetNoDataValue(float(nodata))
    band.WriteArray(array)
    band.FlushCache()
    ds = None
    return path


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


class RasterNodataTestCase(unittest.TestCase):
    """
    O algoritmo recorta o MDE com `nodata=-9999`, e o candidato menor que a célula
    do MDE devolve um recorte sem pixel válido. O sentinela entrava como altitude:
    no máximo só quando a janela inteira era vazia, mas no mínimo sempre que
    houvesse UM pixel sem dado, porque -9999 ganha de qualquer cota real.
    """

    def setUp(self):
        self.tmpDir = tempfile.mkdtemp(prefix="dsgtools_nodata_")
        self.fields = edgvFields()

    def tearDown(self):
        shutil.rmtree(self.tmpDir, ignore_errors=True)

    def raster(self, name, array, nodata=NODATA):
        return writeRaster(
            os.path.join(self.tmpDir, name), np.array(array, dtype=float), nodata
        )

    def test_nodata_declarado_na_banda_vira_nan(self):
        path = self.raster("misto.tif", [[10.0, NODATA], [12.0, 11.0]])
        _ds, npRaster = readAsNumpy(path)
        self.assertEqual(int(np.isnan(npRaster).sum()), 1)
        self.assertEqual(float(np.nanmax(npRaster)), 12.0)
        self.assertEqual(float(np.nanmin(npRaster)), 10.0)

    def test_dtype_inteiro_pedido_pelo_chamador_e_respeitado(self):
        """
        O reclassifyGroupsOfPixels pede int16 e faz aritmética de classe: NaN não
        cabe em inteiro, então ali nada é mascarado.
        """
        path = self.raster("classes.tif", [[1.0, NODATA], [2.0, 3.0]])
        _ds, npRaster = readAsNumpy(path, dtype=np.int16)
        self.assertEqual(npRaster.dtype, np.int16)
        self.assertEqual(int(npRaster.min()), NODATA)

    def test_janela_sem_pixel_valido_nao_gera_ponto(self):
        """Regressão: devolvia uma feição com cota -9999."""
        path = self.raster("vazio.tif", [[NODATA, NODATA], [NODATA, NODATA]])
        self.assertIsNone(
            createMaxPointFeatFromRasterLayer(
                inputRaster=path, fields=self.fields, fieldName="cota"
            )
        )
        self.assertIsNone(
            createMinPointFeatFromRasterLayer(
                inputRaster=path, fields=self.fields, fieldName="cota"
            )
        )
        self.assertEqual(
            createMaxPointFeatListFromRasterLayer(
                inputRaster=path, fields=self.fields, fieldName="cota"
            ),
            [],
        )

    def test_o_minimo_ignora_o_nodata_e_pega_a_cota_real(self):
        """
        Regressão: bastava UM pixel sem dado na janela para o mínimo (o caso da
        depressão) sair -9999.
        """
        path = self.raster("com_buraco.tif", [[10.0, NODATA], [12.0, 11.0]])
        feat = createMinPointFeatFromRasterLayer(
            inputRaster=path, fields=self.fields, fieldName="cota"
        )
        self.assertIsNotNone(feat)
        self.assertEqual(feat["cota"], 10)

    def test_o_maximo_ignora_o_nodata(self):
        path = self.raster("com_buraco2.tif", [[10.0, NODATA], [12.0, 11.0]])
        feat = createMaxPointFeatFromRasterLayer(
            inputRaster=path, fields=self.fields, fieldName="cota"
        )
        self.assertIsNotNone(feat)
        self.assertEqual(feat["cota"], 12)

    def test_lista_de_maximos_carimba_os_atributos_padrao(self):
        """
        É o mecanismo do defeito da área plana: sem o defaultAtributeMap, os seis
        atributos saem NULL, e foi assim que 24 pontos foram parar na carta.
        """
        path = self.raster("plana.tif", [[10.0, 11.0], [12.0, 11.0]])
        semMapa = createMaxPointFeatListFromRasterLayer(
            inputRaster=path, fields=self.fields, fieldName="cota"
        )
        self.assertTrue(semMapa)
        for attr in DEFAULT_ATTR_MAP:
            self.assertFalse(
                bool(semMapa[0][attr]), f"{attr} deveria vir vazio sem o mapa"
            )
        comMapa = createMaxPointFeatListFromRasterLayer(
            inputRaster=path,
            fields=self.fields,
            fieldName="cota",
            defaultAtributeMap=dict(DEFAULT_ATTR_MAP),
        )
        self.assertTrue(comMapa)
        for attr, value in DEFAULT_ATTR_MAP.items():
            self.assertEqual(comMapa[0][attr], value)


class DropNodataElevationsTestCase(unittest.TestCase):
    """
    Rede final antes da única escrita no sink: nenhuma cota pode sair valendo o
    sentinela de sem-dado do recorte.
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

    def test_descarta_o_sentinela_e_mantem_o_resto(self):
        kept = self.alg.dropNodataElevations(self.featList([105, NODATA, 97]))
        self.assertEqual([f["cota"] for f in kept], [105, 97])

    def test_nada_a_descartar(self):
        kept = self.alg.dropNodataElevations(self.featList([105, 97]))
        self.assertEqual([f["cota"] for f in kept], [105, 97])

    def test_cota_nula_nao_quebra(self):
        kept = self.alg.dropNodataElevations(self.featList([None, 105]))
        self.assertEqual([f["cota"] for f in kept], [None, 105])

    def test_cota_negativa_legitima_nao_e_descartada(self):
        """Depressão abaixo do nível do mar existe; só o sentinela sai."""
        kept = self.alg.dropNodataElevations(self.featList([-3, NODATA]))
        self.assertEqual([f["cota"] for f in kept], [-3])


class DropPointsOutsideBoundaryTestCase(unittest.TestCase):
    """
    As grades são montadas sobre o extent() da moldura em lon/lat, e a moldura é
    retângulo em UTM, não em lon/lat: as células de canto sobram para fora.
    """

    def setUp(self):
        self.alg = ExtractElevationPoints()
        self.fields = cotaFields()
        self.boundary = QgsGeometry.fromWkt("Polygon ((0 0, 10 0, 10 10, 0 10, 0 0))")

    def pointFeat(self, x, y):
        feat = QgsFeature(self.fields)
        feat["cota"] = 100
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
        return feat

    def test_ponto_fora_da_moldura_e_descartado(self):
        kept = self.alg.dropPointsOutsideBoundary(
            [self.pointFeat(5, 5), self.pointFeat(11, 5), self.pointFeat(-0.5, 5)],
            self.boundary,
        )
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0].geometry().asPoint(), QgsPointXY(5, 5))

    def test_ponto_na_borda_fica(self):
        kept = self.alg.dropPointsOutsideBoundary(
            [self.pointFeat(10, 5)], self.boundary
        )
        self.assertEqual(len(kept), 1)

    def test_moldura_vazia_nao_descarta_nada(self):
        kept = self.alg.dropPointsOutsideBoundary(
            [self.pointFeat(100, 100)], QgsGeometry()
        )
        self.assertEqual(len(kept), 1)

    def test_extent_nao_serve_de_criterio(self):
        """
        O ponto está DENTRO do extent do polígono e FORA do polígono. É o caso do
        canto da moldura reprojetada, e o filtro por extent o aprovaria.
        """
        boundary = QgsGeometry.fromWkt("Polygon ((0 0, 10 0, 10 10, 0 0))")
        pointInsideExtent = self.pointFeat(1, 9)
        self.assertTrue(boundary.boundingBox().contains(QgsPointXY(1, 9)))
        kept = self.alg.dropPointsOutsideBoundary([pointInsideExtent], boundary)
        self.assertEqual(kept, [])


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
        RasterNodataTestCase,
        DropNodataElevationsTestCase,
        DropPointsOutsideBoundaryTestCase,
    ):
        suite.addTests(loader.loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
