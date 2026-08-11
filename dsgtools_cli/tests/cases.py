# -*- coding: utf-8 -*-
"""
Definição única dos casos de execução usados TANTO pelos testes quanto pelo
regenerador de fixtures, para que parâmetros, nomes de golden e contagens não
divirjam silenciosamente entre os dois.
"""
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
CONSTRAINT_INPUT = DATA / "constraint_input.geojson"

# Fixture de ENTRADA do teste related-to-layer: é gerado, mas não é alvo de
# asserção direta. Precisa existir ANTES do caso 'createframeswithconstraint'.
INPUT_FIXTURE = {
    "name": "constraint_input",
    "args": [
        "dsgtools:gridzonegenerator",
        "START_SCALE=2", "STOP_SCALE=2", "INDEX_TYPE=1",
        "INDEX=SF-22-Y-D", "CRS=EPSG:31982",
    ],
    "golden": "constraint_input.geojson",
}

# Casos efetivamente testados: execução -> GeoJSON -> comparação com o golden.
TEST_CASES = [
    {
        "name": "gridzonegenerator",
        "args": [
            "dsgtools:gridzonegenerator",
            "START_SCALE=2", "STOP_SCALE=4", "INDEX_TYPE=1",
            "INDEX=SF-22-Y-D", "CRS=EPSG:31982",
        ],
        "golden": "gridzonegenerator_expected.geojson",
        "count": 24,
    },
    {
        "name": "createframeswithconstraint",
        "args": [
            "dsgtools:createframeswithconstraintalgorithm",
            f"INPUT={CONSTRAINT_INPUT}", "STOP_SCALE=3",
        ],
        "golden": "createframeswithconstraintalgorithm_expected.geojson",
        "count": 13,
    },
]

# Ordem importa: o input do related-to-layer precisa ser gerado primeiro.
ALL_FIXTURES = [INPUT_FIXTURE] + TEST_CASES
