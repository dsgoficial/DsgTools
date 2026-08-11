# -*- coding: utf-8 -*-
"""
Testes de execução do `dsgtools:generalizecontourlines` via CLI.

Rodar:
    pip install pytest
    pytest dsgtools_cli/tests/test_contour_prep_algorithms.py -v

Os fixtures estão propositalmente em CRS geográfico (CRS84), que é o formato usual
do dado EDGV e o caso em que o filtro de tamanho mínimo media em graus e comparava
com um mínimo em metros, apagando toda curva fechada em silêncio.

Como nos testes de terreno, a asserção é sobre contagem e atributos, não sobre
geometria congelada em golden: a saída passa por NURBfit e Douglas-Peucker, cujo
traçado exato muda a cada ajuste de parâmetro sem que isso seja defeito.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
CLI_PY = CLI_DIR / "dsgtools_cli.py"
DATA = TESTS_DIR / "data" / "contour_prep"
FRAME = DATA / "frame.geojson"

_spec = importlib.util.spec_from_file_location("dsgtools_cli_under_test_contour", CLI_PY)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)

needs_qgis = pytest.mark.skipif(
    cli.find_qgis_process() is None,
    reason="qgis_process não encontrado (defina DSGTOOLS_QGIS_PROCESS para rodar os testes de execução)",
)

ALG = "dsgtools:generalizecontourlines"

SCALE_25K = 0
SCALE_50K = 1

# 12 mm de perímetro na escala: 300 m em 1:25.000, 600 m em 1:50.000.
MIN_PERIMETER = {SCALE_25K: 300, SCALE_50K: 600}


def runAlgGeometries(tmp_path, contours, scale, contourInterval=10):
    """Como runAlg, mas devolve as partes de cada geometria de saída."""
    data = _run(tmp_path, contours, scale, contourInterval)
    out = []
    for f in data.get("features", []):
        geom = f["geometry"]
        out.append(
            geom["coordinates"]
            if geom["type"] == "MultiLineString"
            else [geom["coordinates"]]
        )
    return out


def runAlg(tmp_path, contours, scale, contourInterval=10):
    """Executa o algoritmo via CLI e devolve a lista de propriedades de saída."""
    return [f["properties"] for f in _run(tmp_path, contours, scale, contourInterval).get("features", [])]


def _run(tmp_path, contours, scale, contourInterval=10):
    out = tmp_path / "out.geojson"
    params = tmp_path / "params.json"
    params.write_text(
        json.dumps(
            {
                "inputs": {
                    "INPUT": str(DATA / f"{contours}.geojson"),
                    "ELEVATION_ATTR": "cota",
                    "CONTOUR_INTERVAL": contourInterval,
                    "DEPRESSION_EXPRESSION": '"depressao" = 1',
                    "SCALE": scale,
                    "FRAME": str(FRAME),
                    "OUTPUT": str(out),
                }
            }
        ),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(CLI_PY), "run", ALG, "--params", str(params)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, f"CLI falhou (exit {proc.returncode}):\n{proc.stderr}"
    assert out.exists(), "arquivo de saída não foi criado"
    with open(out, encoding="utf-8-sig") as fh:
        return json.load(fh)


@needs_qgis
class TestGeneralizeContourLines:
    def test_curvas_fechadas_grandes_sobrevivem_em_crs_geografico(self, tmp_path):
        """
        Regressão: media-se o perímetro no CRS de origem, então um anel de ~14 km
        media 0,04 (graus), caía abaixo do mínimo em metros e era descartado. Toda
        curva fechada sumia da saída.

        Cada anel sai segmentado em dois arcos, daí quatro feições para dois anéis.
        """
        props = runAlg(tmp_path, "morro_aninhado", SCALE_25K)
        assert len(props) == 4
        assert sorted(p["cota"] for p in props) == [90, 90, 100, 100]

    def test_depressao_da_entrada_e_preservada(self, tmp_path):
        """
        Regressão: `depressao` era gravado fixo como 2, de modo que o preparador
        destruía a atribuição e o identifyterrainmodelerrorsalgorithm depois
        acusava toda depressão como não marcada.
        """
        props = runAlg(tmp_path, "depressao_aninhada", SCALE_25K)
        assert len(props) == 4
        assert all(p["depressao"] == 1 for p in props)

    def test_curva_nao_depressao_sai_como_nao_depressao(self, tmp_path):
        props = runAlg(tmp_path, "morro_aninhado", SCALE_25K)
        assert all(p["depressao"] == 2 for p in props)

    def test_anel_menor_que_12mm_na_escala_e_removido(self, tmp_path):
        """Perímetro de ~139 m, abaixo dos 300 m de 1:25.000."""
        assert runAlg(tmp_path, "anel_minusculo", SCALE_25K) == []

    def test_o_minimo_acompanha_a_escala(self, tmp_path):
        """
        Perímetro de ~487 m: acima dos 300 m de 1:25.000 e abaixo dos 600 m de
        1:50.000. O mesmo anel tem que sobreviver numa escala e sumir na outra.
        """
        assert len(runAlg(tmp_path, "anel_intermediario", SCALE_25K)) == 2
        assert runAlg(tmp_path, "anel_intermediario", SCALE_50K) == []

    def test_curva_mestra_e_marcada_a_cada_cinco(self, tmp_path):
        """
        Regressão: `indice` era gravado fixo como 2 e nenhuma curva saía como
        mestra. Com equidistância 10, a mestra é múltiplo de 50: a cota 100 é
        mestra e a 90 não.
        """
        props = {p["cota"]: p["indice"] for p in runAlg(tmp_path, "morro_aninhado", SCALE_25K)}
        assert props == {100: 1, 90: 2}

    def test_regra_da_mestra_acompanha_a_equidistancia(self, tmp_path):
        """Com equidistância 20, a mestra é múltiplo de 100: a 100 é, a 90 não."""
        props = {
            p["cota"]: p["indice"]
            for p in runAlg(tmp_path, "morro_aninhado", SCALE_25K, contourInterval=20)
        }
        assert props == {100: 1, 90: 2}

    def test_curva_fechada_sai_segmentada_em_dois_arcos_abertos(self, tmp_path):
        """
        Um anel começa e termina no mesmo ponto, o que é uma autointerseção: ao
        final ele é segmentado em dois arcos, e nenhuma feição de saída fecha.
        """
        geoms = runAlgGeometries(tmp_path, "anel_intermediario", SCALE_25K)
        assert len(geoms) == 2
        for parts in geoms:
            assert len(parts) == 1, "cada arco deve sair como feição de parte única"
            coords = parts[0]
            assert coords[0] != coords[-1], "o arco não pode fechar sobre si"

    def test_os_dois_arcos_recompoem_o_anel(self, tmp_path):
        """A segmentação não pode perder nem duplicar traçado."""
        geoms = runAlgGeometries(tmp_path, "anel_intermediario", SCALE_25K)
        first, second = (g[0] for g in geoms)
        # os arcos se encontram nas duas pontas
        assert first[-1] == second[0]
        assert second[-1] == first[0]

    def test_atributos_edgv_preenchidos(self, tmp_path):
        props = runAlg(tmp_path, "morro_aninhado", SCALE_25K)
        for p in props:
            assert p["id"]
            assert p["texto_edicao"] == str(p["cota"])
            assert p["visivel"] == 1
            assert p["dentro_massa_dagua"] == 2
