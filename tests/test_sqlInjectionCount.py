# -*- coding: utf-8 -*-
"""
Testes do achado 4.1 da avaliação de segurança do CDCiber (2026): composição
insegura de SQL em getElementCountFromLayer() e getElementCountFromLayerV2().

Duas camadas de teste:

1. Gerador (sempre roda): a consulta sai como psycopg2.sql.Composed e o nome
   recebido vira UM identificador inteiro, por mais SQL que traga dentro.

2. Banco (roda só com um PostgreSQL descartável configurado): o nome malicioso
   passa pelos consumidores reais do PostgisDb (countElements e
   getLayersWithElementsV2) conectados com uma conta de operador, que só tem
   SELECT, INSERT, UPDATE e DELETE na tabela, como o usuário temporário do SAP.
   O efeito procurado é o comando injetado apagar as feições. No código antigo
   o DELETE executa; no corrigido o nome inteiro vira identificador, a consulta
   falha por tabela inexistente e nada é apagado.

   Variáveis de ambiente (o banco é criado e destruído pelo teste):
     DSGTOOLS_TEST_PG_HOST, DSGTOOLS_TEST_PG_PORT, DSGTOOLS_TEST_PG_DB,
     DSGTOOLS_TEST_PG_USER, DSGTOOLS_TEST_PG_PASSWORD (conta administrativa
     do banco descartável, usada só para montar e desmontar o cenário).
"""
import os
import secrets
import unittest

import psycopg2
from psycopg2 import sql as pgsql

from qgis.testing import start_app

start_app()

from DsgTools.core.Factories.SqlFactory.postgisSqlGenerator import (  # noqa: E402
    PostGISSqlGenerator,
)
from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb  # noqa: E402

# A entrada da seção 4.1.4 do relatório, com sufixo _a para passar no filtro
# de primitiva do countElements.
NOME_V1 = "cb.veg_a; DELETE FROM cb.veg_a; --_a"
# Contra a V2, o nome fecha a aspa e o parêntese das aspas fixas do format().
NOME_V2 = 'veg_a" ) as a; DELETE FROM cb.veg_a; --'


def _identificadores(composed):
    """Coleta as strings de todo Identifier dentro de um Composed."""
    achados = []
    for parte in getattr(composed, "seq", [composed]):
        if isinstance(parte, pgsql.Identifier):
            achados.extend(parte.strings)
        elif isinstance(parte, pgsql.Composed):
            achados.extend(_identificadores(parte))
    return achados


class TestGeradorContagem(unittest.TestCase):
    def setUp(self):
        self.gen = PostGISSqlGenerator()

    def test_v1_devolve_composed(self):
        self.assertIsInstance(self.gen.getElementCountFromLayer("cb.veg_a"), pgsql.Composed)

    def test_v1_nome_malicioso_vira_um_identificador(self):
        ids = _identificadores(self.gen.getElementCountFromLayer(NOME_V1))
        self.assertEqual(ids, ["cb", "veg_a; DELETE FROM cb.veg_a; --_a"])

    def test_v1_sem_schema(self):
        self.assertEqual(_identificadores(self.gen.getElementCountFromLayer("veg_a")), ["veg_a"])

    def test_v2_nome_malicioso_vira_um_identificador(self):
        for heranca in (False, True):
            ids = _identificadores(self.gen.getElementCountFromLayerV2("cb", NOME_V2, heranca))
            self.assertEqual(ids, ["cb", NOME_V2])

    def test_v2_only_so_sem_heranca(self):
        sem = self.gen.getElementCountFromLayerV2("cb", "veg_a", False)
        com = self.gen.getElementCountFromLayerV2("cb", "veg_a", True)
        self.assertIn(pgsql.SQL("ONLY "), sem.seq)
        self.assertNotIn(pgsql.SQL("ONLY "), com.seq)


def _config():
    chaves = ["HOST", "PORT", "DB", "USER", "PASSWORD"]
    valores = {c: os.environ.get("DSGTOOLS_TEST_PG_" + c) for c in chaves}
    return valores if all(valores.values()) else None


@unittest.skipIf(_config() is None, "sem PostgreSQL descartável (DSGTOOLS_TEST_PG_*)")
class TestConsumidoresNoBanco(unittest.TestCase):
    FEICOES = 3

    @classmethod
    def setUpClass(cls):
        cfg = _config()
        cls.cfg = cfg
        cls.operador = "operador_teste_41"
        cls.senha_operador = secrets.token_hex(16)
        admin = psycopg2.connect(
            host=cfg["HOST"], port=cfg["PORT"], dbname=cfg["DB"],
            user=cfg["USER"], password=cfg["PASSWORD"],
        )
        admin.autocommit = True
        with admin.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS cb CASCADE")
            cur.execute(pgsql.SQL("DROP ROLE IF EXISTS {}").format(pgsql.Identifier(cls.operador)))
            cur.execute("CREATE SCHEMA cb")
            cur.execute("CREATE TABLE cb.veg_a (id serial PRIMARY KEY, nome text)")
            cur.execute("CREATE TABLE cb.hid_l (id serial PRIMARY KEY, nome text)")
            cur.execute("INSERT INTO cb.veg_a (nome) SELECT 'v' || g FROM generate_series(1, %s) g", (cls.FEICOES,))
            cur.execute("INSERT INTO cb.hid_l (nome) VALUES ('rio')")
            cur.execute(
                pgsql.SQL("CREATE ROLE {} LOGIN PASSWORD %s").format(pgsql.Identifier(cls.operador)),
                (cls.senha_operador,),
            )
            cur.execute(pgsql.SQL("GRANT USAGE ON SCHEMA cb TO {}").format(pgsql.Identifier(cls.operador)))
            cur.execute(
                pgsql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE ON cb.veg_a, cb.hid_l TO {}").format(
                    pgsql.Identifier(cls.operador)
                )
            )
        cls.admin = admin

    @classmethod
    def tearDownClass(cls):
        with cls.admin.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS cb CASCADE")
            cur.execute(pgsql.SQL("DROP ROLE IF EXISTS {}").format(pgsql.Identifier(cls.operador)))
        cls.admin.close()

    def setUp(self):
        self.db = PostgisDb()
        ok = self.db.testCredentials(
            self.cfg["HOST"], self.cfg["PORT"], self.cfg["DB"], self.operador, self.senha_operador
        )
        self.assertTrue(ok, "a conta de operador não conectou")

    def tearDown(self):
        self.db.closeDatabase()

    def _feicoes_vistas_pelo_operador(self):
        # Mesma conexão e mesma transação do consumidor: um DELETE injetado e
        # não confirmado aparece aqui, e é isso que se quer medir.
        try:
            return self.db._fetch_one("SELECT count(*) FROM cb.veg_a")[0]
        except Exception:
            self.db.db.rollback()
            return self.db._fetch_one("SELECT count(*) FROM cb.veg_a")[0]

    def test_countElements_nao_executa_comando_injetado(self):
        with self.assertRaises(Exception):
            self.db.countElements([NOME_V1])
        self.assertEqual(self._feicoes_vistas_pelo_operador(), self.FEICOES)

    def test_getLayersWithElementsV2_nao_executa_comando_injetado(self):
        camadas = [
            {"tableSchema": "cb", "tableName": NOME_V2},
            {"tableSchema": "cb", "tableName": "hid_l"},
        ]
        resultado = self.db.getLayersWithElementsV2(camadas)
        self.assertEqual(self._feicoes_vistas_pelo_operador(), self.FEICOES)
        # A tabela legítima depois da maliciosa ainda é contada (rollback do erro).
        self.assertEqual(resultado, ["hid_l"])

    def test_contagem_legitima(self):
        self.assertEqual(self.db.countElements(["cb.veg_a"]), [["cb.veg_a", self.FEICOES]])
        self.assertEqual(
            self.db.getLayersWithElementsV2([{"tableSchema": "cb", "tableName": "veg_a"}]),
            ["veg_a"],
        )


if __name__ == "__main__":
    unittest.main()
