# -*- coding: utf-8 -*-
"""
Executa um módulo de teste dentro do ambiente do QGIS, sem Docker e sem instalar
nada.

Uso (o interpretador precisa ser o do QGIS, que já traz PyQGIS configurado):

    # Windows
    & 'C:\\Program Files\\QGIS 4.0.0\\bin\\python-qgis.bat' tests/run_local.py tests.test_terrainHandler

    # Linux/macOS
    python3 tests/run_local.py tests.test_terrainHandler

    # apenas os testes cujo nome contém um trecho
    ... tests/run_local.py tests.test_terrainHandler depression

Os testes são descobertos com o TestLoader padrão, e não pela função `run_all()`
de cada módulo: assim o resultado é observável e vira código de saída (0 = passou,
1 = falhou), o que `run_all()` não permite porque descarta o resultado do runner.

Testes que executam Processing (`processing.run`) dependem do provider do DSGTools
registrado, o que é feito aqui. Já a execução dos algoritmos por linha de comando
tem caminho próprio: veja `dsgtools_cli/`.
"""
import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def qgisPrefixPath():
    """
    Descobre o prefixo do QGIS pelo ambiente e, se preciso, pelo próprio pacote.
    """
    prefix = os.environ.get("QGIS_PREFIX_PATH")
    if prefix:
        return prefix
    import qgis

    # <prefix>/python/qgis/__init__.py
    return str(Path(qgis.__file__).resolve().parents[2])


def filterSuite(suite, pattern):
    """
    Achata a suíte e mantém apenas os testes cujo id contém `pattern`.
    """
    selected = unittest.TestSuite()
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            selected.addTests(filterSuite(test, pattern))
        elif pattern in test.id():
            selected.addTest(test)
    return selected


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    moduleName = sys.argv[1]
    pattern = sys.argv[2] if len(sys.argv) > 2 else None

    sys.path.insert(0, str(REPO_ROOT))

    from qgis.core import QgsApplication

    QgsApplication.setPrefixPath(qgisPrefixPath(), True)
    app = QgsApplication([], False)
    app.initQgis()
    try:
        sys.path.append(os.path.join(app.prefixPath(), "python", "plugins"))
        from processing.core.Processing import Processing

        Processing.initialize()

        from DsgTools.core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import (
            DSGToolsProcessingAlgorithmProvider,
        )

        # sem o provider registrado, `processing.run("dsgtools:...")` não encontra
        # os algoritmos e os testes falham com "Algorithm not found"
        provider = DSGToolsProcessingAlgorithmProvider()
        QgsApplication.processingRegistry().addProvider(provider)

        module = __import__(moduleName, fromlist=["__name__"])
        suite = unittest.TestLoader().loadTestsFromModule(module)
        if pattern is not None:
            suite = filterSuite(suite, pattern)
        if suite.countTestCases() == 0:
            print(f"nenhum teste encontrado em {moduleName}" + (f" para {pattern!r}" if pattern else ""))
            return 1
        result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
        return 0 if result.wasSuccessful() else 1
    finally:
        app.exitQgis()


if __name__ == "__main__":
    sys.exit(main())
