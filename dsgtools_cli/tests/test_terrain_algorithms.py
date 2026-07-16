# -*- coding: utf-8 -*-
"""
Testes de execução do `dsgtools:identifyterrainmodelerrorsalgorithm` via CLI.

Rodar:
    pip install pytest
    pytest dsgtools_cli/tests/test_terrain_algorithms.py -v

Ao contrário dos testes de grade, aqui NÃO se compara GeoJSON golden: a asserção é
sobre a quantidade de flags por sink e sobre o texto do `reason`. Flags são
diagnósticos, não geometria de saída — congelar a geometria produz um golden que
quebra a cada refactor sem indicar defeito algum.

Um ponto de projeto que os fixtures precisam respeitar: `TerrainModel.validate()`
faz early-return em cascata (curvas -> bandas -> depressão -> ponto cotado), então
**cada fixture exercita uma única classe de erro**. Um fixture com um erro de banda
nunca chega a validar depressão. Por isso cada modelo de terreno abaixo é válido em
tudo, exceto no ponto que o caso quer testar.
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
DATA = TESTS_DIR / "data" / "terrain"
BOUNDS = DATA / "bounds.geojson"

_spec = importlib.util.spec_from_file_location("dsgtools_cli_under_test_terrain", CLI_PY)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)

needs_qgis = pytest.mark.skipif(
    cli.find_qgis_process() is None,
    reason="qgis_process não encontrado (defina DSGTOOLS_QGIS_PROCESS para rodar os testes de execução)",
)

ALG = "dsgtools:identifyterrainmodelerrorsalgorithm"

# (nome, camada de curvas, camada de pontos cotados ou None, flags esperadas)
# As flags esperadas são {sink: [trecho esperado no reason, ...]}; sink omitido = vazio.
TERRAIN_CASES = [
    (
        "depressao_ok",
        "depressao_ok",
        None,
        {},
    ),
    (
        "depressao_nao_marcada",
        "depressao_nao_marcada",
        None,
        {"LINE_FLAGS": ["is not marked as depression"]},
    ),
    (
        "morro_ok",
        "morro_ok",
        None,
        {},
    ),
    (
        "morro_marcado_como_depressao",
        "morro_marcado_dep",
        None,
        {"LINE_FLAGS": ["is marked as depression"]},
    ),
    (
        "cota_no_topo_dentro_da_faixa",
        "morro_ok",
        "cota_topo_ok",
        {},
    ),
    (
        "cota_no_topo_abaixo_da_faixa",
        "morro_ok",
        "cota_topo_abaixo",
        {"POINT_FLAGS": ["hilltop"]},
    ),
    (
        "cota_no_fundo_dentro_da_faixa",
        "depressao_ok",
        "cota_fundo_ok",
        {},
    ),
    (
        "cota_no_fundo_acima_da_faixa",
        "depressao_ok",
        "cota_fundo_acima",
        {"POINT_FLAGS": ["valley/depression"]},
    ),
]

SINKS = ("POINT_FLAGS", "LINE_FLAGS", "POLYGON_FLAGS")


def _run_terrain(tmp_path, contours, spot_elevation):
    """Executa o algoritmo via CLI e devolve {sink: [reason, ...]}."""
    outputs = {sink: tmp_path / f"{sink.lower()}.geojson" for sink in SINKS}
    inputs = {
        "INPUT": str(DATA / f"{contours}.geojson"),
        "CONTOUR_ATTR": "cota",
        "CONTOUR_INTERVAL": 10,
        "DEPRESSION_EXPRESSION": '"depressao" = 1',
        "GEOGRAPHIC_BOUNDS": str(BOUNDS),
        "SELECTED": False,
        "GROUP_BY_SPATIAL_PARTITION": False,
        **{sink: str(path) for sink, path in outputs.items()},
    }
    if spot_elevation is not None:
        inputs["INPUT_ELEVATION_POINTS"] = str(DATA / f"{spot_elevation}.geojson")
        inputs["ELEVATION_POINT_ATTR"] = "cota"

    params = tmp_path / "params.json"
    params.write_text(json.dumps({"inputs": inputs}), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(CLI_PY), "run", ALG, "--params", str(params)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, f"CLI falhou (exit {proc.returncode}):\n{proc.stderr}"

    found = {}
    for sink, path in outputs.items():
        assert path.exists(), f"sink {sink} não foi criado"
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
        found[sink] = [f["properties"].get("reason") for f in data.get("features", [])]
    return found


@needs_qgis
@pytest.mark.parametrize(
    "name,contours,spot_elevation,expected",
    TERRAIN_CASES,
    ids=[c[0] for c in TERRAIN_CASES],
)
def test_terrain_flags(tmp_path, name, contours, spot_elevation, expected):
    found = _run_terrain(tmp_path, contours, spot_elevation)
    for sink in SINKS:
        wanted = expected.get(sink, [])
        got = found[sink]
        assert len(got) == len(wanted), f"{sink}: esperado {len(wanted)} flag(s), veio {got}"
        for fragment, reason in zip(wanted, got):
            assert fragment in reason, f"{sink}: esperava conter {fragment!r}, veio {reason!r}"
