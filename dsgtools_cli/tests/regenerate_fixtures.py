#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera os arquivos "golden" usados pelos testes de integração, executando os
algoritmos via dsgtools_cli e salvando o resultado em GeoJSON em data/.

Os casos (parâmetros, nomes de golden) vêm de cases.py — a MESMA fonte usada
pelos testes — para que nunca divirjam.

Use SOMENTE após uma mudança INTENCIONAL de comportamento dos algoritmos.

    python dsgtools_cli/tests/regenerate_fixtures.py
"""
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
CLI_PY = TESTS_DIR.parent / "dsgtools_cli.py"

sys.path.insert(0, str(TESTS_DIR))
from cases import ALL_FIXTURES, DATA  # noqa: E402


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    # Ordem importa: o input do related-to-layer é gerado antes do caso que o usa.
    for fixture in ALL_FIXTURES:
        final = DATA / fixture["golden"]
        tmp = final.with_suffix(final.suffix + ".tmp")
        if tmp.exists():
            tmp.unlink()
        cmd = [sys.executable, str(CLI_PY), "run", *fixture["args"], f"OUTPUT={tmp}"]
        print(f"== {fixture['name']} ==")
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode != 0 or not tmp.exists():
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            raise SystemExit(f"falha ao gerar {fixture['golden']} (exit {proc.returncode})")
        # Só substitui o golden após sucesso (escrita atômica): nunca deixa o repo
        # com um golden apagado se a geração falhar no meio.
        tmp.replace(final)
        print(f"   -> {final}")
    print("OK: golden regenerados.")


if __name__ == "__main__":
    main()
