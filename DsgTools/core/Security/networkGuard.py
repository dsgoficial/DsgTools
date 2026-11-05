# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Guarda de rede para recursos de projeto (CDCiber 2026, achados 4.3 e 4.4).

Abrir um projeto de terceiro faz o QGIS buscar na rede o SVG, a imagem e o
formulário .ui que o projeto aponta, e a URL pode carregar o valor de
`env()`. A guarda instala um pré-processador no QgsNetworkAccessManager,
que vê o endereço FINAL de cada requisição (depois da expressão e de cada
salto de redirecionamento), e barra só as buscas de recurso de projeto cujo
destino não está em `dsgtools/security/allowedHosts`.

Como a busca é classificada (medido no QGIS 4.2.1):

- atributo AttributeInitiatorClass `QgsAbstractContentCache<SVG>` ou
  `QgsAbstractContentCache<Image>`: símbolo SVG, imagem raster de símbolo,
  SVG/imagem em prancha;
- `QgsNetworkContentFetcher`: figura de prancha e TODO salto de
  redirecionamento das buscas acima (o salto troca o iniciador);
- sem iniciador: o formulário .ui remoto (QgsNetworkContentFetcherRegistry)
  chega assim, junto com o tráfego legítimo de provedor (tiles XYZ pelo
  QgsTileDownloadManager), do QgsBlockingNetworkRequest e dos plugins. Para
  separar, a guarda registra os caminhos remotos que o projeto lê
  (QgsPathResolver.setPathPreprocessor, que roda ANTES da busca do .ui) e
  trata como recurso só a requisição sem iniciador cuja URL é exatamente
  uma delas, ou cujo caminho termina em `.ui`.

Os demais iniciadores (QgsWmsCapabilitiesDownload,
QgsWmsTiledImageDownloadHandler, QgsWmsImageDownloadHandler,
QgsBaseNetworkRequest do WFS, QgsNewsFeedParser...) nunca são filtrados.
"""
import threading

from qgis.core import Qgis, QgsNetworkAccessManager, QgsNetworkRequestParameters, QgsPathResolver, QgsProject
from qgis.PyQt.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from qgis.PyQt.QtNetwork import QNetworkRequest

from . import securitySettings as cfg

# QNetworkRequest.Attribute não tem membro para o atributo do QGIS (User + 3000).
ATRIBUTO_INICIADOR = QNetworkRequest.Attribute(
    int(QgsNetworkRequestParameters.RequestAttributes.AttributeInitiatorClass.value)
)
PREFIXOS_INICIADOR_RECURSO = ("QgsAbstractContentCache",)
INICIADORES_RECURSO = ("QgsNetworkContentFetcher",)
URL_BLOQUEADA = "bloqueado:"
LIMITE_REGISTRO = 5000


def chaveUrl(url):
    """Forma canônica para comparar o caminho lido do projeto com a URL da requisição."""
    if not isinstance(url, QUrl):
        url = QUrl(str(url))
    return bytes(url.adjusted(QUrl.UrlFormattingOption.RemoveFragment).toEncoded()).decode("ascii", "replace")


def ehRemoto(texto):
    if not texto:
        return False
    return QUrl(str(texto)).scheme().lower() in cfg.ESQUEMAS_REMOTOS


class _Notificador(QObject):
    """Vive na thread principal; o sinal vindo de thread de rede chega enfileirado."""

    pedido = pyqtSignal(str, str)

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.pedido.connect(self._mostrar)

    @pyqtSlot(str, str)
    def _mostrar(self, titulo, texto):
        if self.iface is None:
            return
        try:
            self.iface.messageBar().pushMessage(titulo, texto, Qgis.MessageLevel.Warning, 15)
        except Exception:
            pass


class NetworkGuard:
    def __init__(self, iface=None):
        self.iface = iface
        self.idRequisicao = None
        self.idCaminho = None
        self.modo = cfg.PADRAO_MODO
        self.permitidos = []
        self._trava = threading.Lock()
        self._urlsDeProjeto = set()
        self._hostsAvisados = set()
        self._urlsLogadas = set()
        self.bloqueios = 0
        self._notificador = None
        self._projeto = None

    # ciclo de vida -------------------------------------------------------
    def install(self):
        if self.idRequisicao is not None:
            return
        self.recarregarConfiguracao()
        self._notificador = _Notificador(self.iface)
        self.idRequisicao = QgsNetworkAccessManager.setRequestPreprocessor(self._preprocessarRequisicao)
        self.idCaminho = QgsPathResolver.setPathPreprocessor(self._registrarCaminho)
        self._projeto = QgsProject.instance()
        self._projeto.cleared.connect(self._aoLimparProjeto)

    def uninstall(self):
        if self.idRequisicao is not None:
            QgsNetworkAccessManager.removeRequestPreprocessor(self.idRequisicao)
            self.idRequisicao = None
        if self.idCaminho is not None:
            QgsPathResolver.removePathPreprocessor(self.idCaminho)
            self.idCaminho = None
        if self._projeto is not None:
            try:
                self._projeto.cleared.disconnect(self._aoLimparProjeto)
            except (TypeError, RuntimeError):
                pass
            self._projeto = None
        self._notificador = None

    def recarregarConfiguracao(self):
        """Relê modo e destinos permitidos (também a cada projeto novo)."""
        modo, permitidos = cfg.lerModo(), cfg.lerHostsPermitidos()
        with self._trava:
            self.modo, self.permitidos = modo, permitidos

    def _aoLimparProjeto(self):
        with self._trava:
            self._urlsDeProjeto.clear()
            self._hostsAvisados.clear()
            self._urlsLogadas.clear()
        self.recarregarConfiguracao()

    # registro dos caminhos remotos que o projeto lê ----------------------
    def registrarRecursoDeProjeto(self, caminho):
        if not ehRemoto(caminho):
            return
        with self._trava:
            if len(self._urlsDeProjeto) < LIMITE_REGISTRO:
                self._urlsDeProjeto.add(chaveUrl(caminho))

    def _registrarCaminho(self, caminho):
        try:
            if self.modo != cfg.MODO_DESLIGADO:
                self.registrarRecursoDeProjeto(caminho)
        except Exception:
            pass
        return caminho

    # classificação e filtro ----------------------------------------------
    def ehRecursoDeProjeto(self, requisicao):
        url = requisicao.url()
        if url.scheme().lower() not in cfg.ESQUEMAS_REMOTOS:
            return False
        iniciador = requisicao.attribute(ATRIBUTO_INICIADOR)
        if iniciador:
            iniciador = str(iniciador)
            return iniciador in INICIADORES_RECURSO or iniciador.startswith(PREFIXOS_INICIADOR_RECURSO)
        if url.path().lower().endswith(".ui"):
            return True
        with self._trava:
            return chaveUrl(url) in self._urlsDeProjeto

    def _preprocessarRequisicao(self, requisicao):
        try:
            if self.modo == cfg.MODO_DESLIGADO or not self.ehRecursoDeProjeto(requisicao):
                return ""
            url = requisicao.url()
            if cfg.hostPermitido(url.host(), url.port(), url.scheme().lower(), self.permitidos):
                return ""
            bloquear = self.modo == cfg.MODO_BLOQUEAR
            if bloquear:
                requisicao.setUrl(QUrl(URL_BLOQUEADA))
            self._relatar(url, requisicao.attribute(ATRIBUTO_INICIADOR), bloquear)
        except Exception as e:
            cfg.log(f"falha no filtro de rede: {e!r}", Qgis.MessageLevel.Critical)
        return ""

    def _relatar(self, url, iniciador, bloqueado):
        host = url.host()
        porta = f":{url.port()}" if url.port() > 0 else ""
        # Sem a query: é nela que a expressão costuma pôr o valor de env().
        curta = f"{url.scheme()}://{host}{porta}{url.path()}"[:160]
        with self._trava:
            if bloqueado:
                self.bloqueios += 1
            novoUrl = curta not in self._urlsLogadas and len(self._urlsLogadas) < LIMITE_REGISTRO
            if novoUrl:
                self._urlsLogadas.add(curta)
            novoHost = host not in self._hostsAvisados
            self._hostsAvisados.add(host)
        acao = "bloqueada" if bloqueado else "permitida (modo warn)"
        if novoUrl:
            cfg.log(
                f"busca de recurso de projeto {acao}: {curta} "
                f"(iniciador: {iniciador or 'sem iniciador'}); destino fora de "
                f"{cfg.PREFIXO}allowedHosts"
            )
        if novoHost and self._notificador is not None:
            texto = (
                f"busca de recurso de projeto (SVG, imagem ou formulário) {acao} "
                f"para {host}{porta}. Se o destino for confiável, inclua-o em "
                f"{cfg.PREFIXO}allowedHosts. Detalhes no log."
            )
            self._notificador.pedido.emit(cfg.TAG_LOG, texto)
