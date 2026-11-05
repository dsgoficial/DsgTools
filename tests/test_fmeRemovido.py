# -*- coding: utf-8 -*-
"""
Retirada da integração com o FME (avaliação de segurança do CDCiber, 2026,
achado 4.2: verificação TLS desligada por padrão e credencial de proxy).

Confere que o provider carrega sem os dois algoritmos e sem o tipo de
parâmetro do FME Manager, e que nenhum módulo do plugin ainda chama o
Requests com a verificação de certificado desligada.
"""
import re
import unittest
from pathlib import Path

from qgis.core import QgsApplication
from qgis.testing import start_app

start_app()

from DsgTools.core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import (  # noqa: E402
    DSGToolsProcessingAlgorithmProvider,
)

RAIZ_PLUGIN = Path(__file__).resolve().parent.parent / "DsgTools"


class TestFmeRemovido(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # O run_local.py já registra o provider; só cria um se rodar avulso.
        registro = QgsApplication.processingRegistry()
        cls.provider = registro.providerById("dsgtools")
        cls.criado_aqui = cls.provider is None
        if cls.criado_aqui:
            cls.provider = DSGToolsProcessingAlgorithmProvider()
            registro.addProvider(cls.provider)

    @classmethod
    def tearDownClass(cls):
        if cls.criado_aqui:
            QgsApplication.processingRegistry().removeProvider(cls.provider)

    def test_algoritmos_fme_fora_do_provider(self):
        nomes = {alg.name() for alg in self.provider.algorithms()}
        self.assertTrue(nomes, "o provider não carregou nenhum algoritmo")
        self.assertNotIn("runremotefme", nomes)
        self.assertNotIn("runfmesap", nomes)

    def test_tipo_de_parametro_fme_fora_do_registro(self):
        tipos = {t.id() for t in QgsApplication.processingRegistry().parameterTypes()}
        self.assertFalse([t for t in tipos if "fme" in t.lower()], tipos)

    def test_nenhum_verify_desligado_no_plugin(self):
        padrao = re.compile(r"verify\s*=\s*(False|useSsl)")
        achados = [
            str(p.relative_to(RAIZ_PLUGIN))
            for p in RAIZ_PLUGIN.rglob("*.py")
            if padrao.search(p.read_text(encoding="utf-8", errors="ignore"))
        ]
        self.assertEqual(achados, [])


if __name__ == "__main__":
    unittest.main()
