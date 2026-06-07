# -*- coding: utf-8 -*-
"""
Testes do dsgtools-cli.

Três níveis:
- Unitários (sempre rodam, sem QGIS): funções puras de parsing/coerção do CLI.
- Annotations (estrutura sempre; correspondência com o provider precisa de QGIS):
  garantem que annotations.json não derive em relação aos algoritmos reais.
- Integração (pulados se o qgis_process não for encontrado): executam de fato os
  algoritmos de grade via linha de comando, salvam o resultado em GeoJSON e o
  comparam com os arquivos "golden" em tests/data/.

Rodar:
    pip install pytest
    pytest dsgtools_cli/tests -v

Regenerar os golden (após uma mudança INTENCIONAL de comportamento):
    python dsgtools_cli/tests/regenerate_fixtures.py
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

# --------------------------------------------------------------------------
# Carrega o módulo do CLI por caminho (a pasta e o arquivo têm o mesmo nome,
# então importlib evita ambiguidade de import). E disponibiliza cases.py.
# --------------------------------------------------------------------------
TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
CLI_PY = CLI_DIR / "dsgtools_cli.py"
ANNOTATIONS = CLI_DIR / "annotations.json"

sys.path.insert(0, str(TESTS_DIR))
from cases import DATA, TEST_CASES  # noqa: E402

_spec = importlib.util.spec_from_file_location("dsgtools_cli_under_test", CLI_PY)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)

HAS_QGIS = cli.find_qgis_process() is not None
needs_qgis = pytest.mark.skipif(
    not HAS_QGIS,
    reason="qgis_process não encontrado (defina DSGTOOLS_QGIS_PROCESS para rodar os testes de execução)",
)


# --------------------------------------------------------------------------
# Comparação de GeoJSON — invariante a ordem das feições, ordem/winding/vértice
# inicial dos anéis e ordem das partes do MultiPolygon (compara o multiset de
# vértices arredondados por feição), e a -0.0 vs 0.0 e int vs float.
# --------------------------------------------------------------------------
def _positions(coords, ndigits):
    """Extrai recursivamente todas as posições [x, y(, z)], arredondadas; -0.0 -> 0.0."""
    if (
        isinstance(coords, list)
        and coords
        and all(isinstance(c, (int, float)) for c in coords)
    ):
        return [tuple(round(float(c), ndigits) + 0.0 for c in coords)]
    out = []
    if isinstance(coords, list):
        for c in coords:
            out.extend(_positions(c, ndigits))
    return out


def _signature(geojson_path, ndigits=3):
    """Forma canônica e comparável de um GeoJSON."""
    with open(geojson_path, encoding="utf-8-sig") as fh:
        data = json.load(fh)
    feats = []
    for feature in data.get("features", []):
        props = feature.get("properties") or {}
        geom = feature.get("geometry") or {}
        pts = tuple(sorted(_positions(geom.get("coordinates"), ndigits)))
        feats.append((props.get("inom"), props.get("mi"), geom.get("type"), pts))
    return sorted(feats)


def _run_cli(args, out_path):
    """Executa o CLI de verdade (subprocess) gravando a saída em out_path."""
    cmd = [sys.executable, str(CLI_PY), "run", *args, f"OUTPUT={out_path}"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert proc.returncode == 0, f"CLI falhou (exit {proc.returncode}):\n{proc.stderr}"
    assert out_path.exists(), "arquivo de saída não foi criado"
    return out_path


# --------------------------------------------------------------------------
# Testes unitários (sem QGIS)
# --------------------------------------------------------------------------
def test_full_id_normaliza_prefixo():
    assert cli.full_id("gridzonegenerator") == "dsgtools:gridzonegenerator"
    assert cli.full_id("dsgtools:gridzonegenerator") == "dsgtools:gridzonegenerator"
    assert cli.full_id("  gridzonegenerator  ") == "dsgtools:gridzonegenerator"
    assert cli.full_id("native:buffer") == "native:buffer"


def test_coerce_tipos():
    assert cli._coerce("2") == 2 and isinstance(cli._coerce("2"), int)
    assert cli._coerce("0") == 0
    assert cli._coerce("-3") == -3
    assert cli._coerce("2.5") == 2.5 and isinstance(cli._coerce("2.5"), float)
    # strings que NÃO devem virar número (corrige coerção perigosa)
    assert cli._coerce("EPSG:31982") == "EPSG:31982"
    assert cli._coerce("SF-22-Y-D") == "SF-22-Y-D"
    assert cli._coerce("007") == "007"      # zero à esquerda preservado
    assert cli._coerce("1_000") == "1_000"  # underscore não coage
    assert cli._coerce("inf") == "inf"
    assert cli._coerce("nan") == "nan"
    assert cli._coerce("1e3") == "1e3"
    assert cli._coerce("") == ""


def test_unwrap_inputs():
    assert cli._unwrap_inputs({"inputs": {"A": 1}}) == {"A": 1}
    assert cli._unwrap_inputs({"A": 1}) == {"A": 1}
    with pytest.raises(SystemExit):
        cli._unwrap_inputs([1, 2, 3])
    with pytest.raises(SystemExit):
        cli._unwrap_inputs({"inputs": [1, 2]})


def test_parse_json_stdout():
    assert cli._parse_json_stdout('{"a": 1}') == {"a": 1}
    assert cli._parse_json_stdout("   ") is None
    assert cli._parse_json_stdout("traceback de outro plugin") is None


def test_version_key_ordena_por_versao():
    paths = [r"C:\QGIS 3.8\bin\x", r"C:\QGIS 3.40\bin\x", r"C:\QGIS 4.0.0\bin\x"]
    newest = sorted(paths, key=cli._version_key, reverse=True)[0]
    assert "4.0.0" in newest
    # 3.40 deve ser mais novo que 3.8 (lexicográfico erraria)
    assert cli._version_key(r"C:\QGIS 3.40\x") > cli._version_key(r"C:\QGIS 3.8\x")


def test_summarize_help_resume_parametros():
    help_data = {
        "algorithm_details": {"id": "dsgtools:foo", "name": "Foo", "group": "Bar"},
        "parameters": {
            "SCALE": {
                "description": "Escala",
                "optional": False,
                "raw_definition": {"parameter_type": "enum"},
                "available_options": {"0": "1000k", "1": "500k"},
            }
        },
        "outputs": {"OUTPUT": {"type": "outputVector", "description": "Saída"}},
    }
    summary = cli._summarize_help(help_data)
    assert summary["id"] == "dsgtools:foo"
    assert summary["display_name"] == "Foo"
    param = summary["parameters"][0]
    assert param["name"] == "SCALE"
    assert param["type"] == "enum"
    assert param["required"] is True
    assert param["options"] == {"0": "1000k", "1": "500k"}
    assert summary["outputs"][0]["name"] == "OUTPUT"


# --------------------------------------------------------------------------
# Annotations: estrutura (sempre) e correspondência com o provider (precisa QGIS)
# --------------------------------------------------------------------------
def _load_annotations():
    with open(ANNOTATIONS, encoding="utf-8") as fh:
        ann = json.load(fh)
    return {k: v for k, v in ann.items() if not k.startswith("_")}


def test_annotations_estrutura():
    entries = _load_annotations()
    assert entries, "annotations.json vazio"
    for alg_id, entry in entries.items():
        assert alg_id.startswith("dsgtools:"), f"id sem prefixo: {alg_id}"
        assert isinstance(entry.get("description"), str) and entry["description"], alg_id
        if "constraints" in entry:
            assert isinstance(entry["constraints"], list), alg_id
        if "example" in entry:
            assert isinstance(entry["example"], dict), alg_id


@needs_qgis
def test_annotations_ids_existem_no_provider():
    # Guarda contra deriva: toda chave anotada deve ser um algoritmo real do provider.
    code, out, _err = cli.call_qgis_process(["list", "--json"])
    data = cli._parse_json_stdout(out)
    assert data is not None, f"falha ao listar (exit {code})"
    live = set(data.get("providers", {}).get("dsgtools", {}).get("algorithms", {}))
    assert live, "provider dsgtools não retornou algoritmos"
    extra = sorted(set(_load_annotations()) - live)
    assert not extra, f"annotations.json tem ids inexistentes no provider: {extra}"


# --------------------------------------------------------------------------
# Testes de integração (execução real → GeoJSON → comparação com o golden)
# --------------------------------------------------------------------------
@needs_qgis
@pytest.mark.parametrize("case", TEST_CASES, ids=[c["name"] for c in TEST_CASES])
def test_execucao_compara_geojson(tmp_path, case):
    out = _run_cli(case["args"], tmp_path / f"{case['name']}.geojson")
    expected = _signature(DATA / case["golden"])
    actual = _signature(out)
    assert len(actual) == case["count"], f"esperado {case['count']} feições, veio {len(actual)}"
    assert actual == expected
