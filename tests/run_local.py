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

Uma única QgsApplication por processo. A aplicação é criada por
`qgis.testing.start_app()`, o mesmo que os módulos de teste chamam ao serem
importados. O `start_app()` só reconhece a aplicação que ele próprio criou (guarda
na global `QGISAPP` do `qgis.testing`, não consulta `QgsApplication.instance()`),
então, se o runner criasse a sua com `QgsApplication([], False)`, cada módulo que
chama `start_app()` criaria uma segunda, com `initQgis()` de novo e um
`exitQgis()` registrado no `atexit`. O Qt admite um só objeto de aplicação, e as
duas finalizações sobre o mesmo estado global corrompem o heap na saída
(0xC0000374 e 0xC0000409 no Windows), depois do veredito impresso, o que fazia o
código de saída mentir mesmo com todos os testes passando.
"""
import os
import shutil
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
    from qgis.testing import start_app

    QgsApplication.setPrefixPath(qgisPrefixPath(), True)
    # cleanup=False: quem finaliza é o `finally` abaixo, uma vez só; com True o
    # start_app registraria outro exitQgis() no atexit
    app = start_app(cleanup=False)
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
        if QgsApplication.instance() is not app:
            # algum import criou outra QgsApplication por fora do start_app(); a
            # saída pode cair, e então o veredito impresso é o que vale
            print(
                "AVISO: há uma segunda QgsApplication no processo; o código de saída "
                "pode não refletir o veredito",
                file=sys.stderr,
            )
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
        # o perfil descartável que o start_app() criou na pasta temporária
        perfil = os.environ.get("QGIS_CUSTOM_CONFIG_PATH")
        if perfil and Path(perfil).name.startswith("QGIS-PythonTestConfigPath-"):
            shutil.rmtree(perfil, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
