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
  SVG/imagem em prancha. Sempre recurso de projeto;
- URL que o projeto lê (QgsPathResolver.setPathPreprocessor, que roda na
  leitura do projeto e do estilo): formulário .ui remoto, que chega SEM
  iniciador, e figura de prancha de caminho fixo, que chega com o
  iniciador `QgsNetworkContentFetcher`;
- salto de redirecionamento: o salto chega com o iniciador
  `QgsNetworkContentFetcher`, igual ao de qualquer outro uso da classe.
  A guarda acompanha a resposta de cada busca de recurso que deixou
  passar (QgsNetworkAccessManager.setReplyPreprocessor) e registra o
  destino do 3xx; só o salto registrado é recurso;
- figura e quadro HTML de prancha com endereço por expressão: a URL não
  passa pelo QgsPathResolver. Com o projeto aberto, a requisição
  `QgsNetworkContentFetcher` da thread principal é comparada com o
  caminho avaliado dos itens das pranchas. Durante a LEITURA do projeto a
  prancha ainda não está no gerenciador (a figura é buscada antes do
  `layoutAdded`), então do `cleared` ao `readProject` toda requisição
  `QgsNetworkContentFetcher` da thread principal é tratada como recurso.

Fora desses casos o `QgsNetworkContentFetcher` NÃO é filtrado: é a mesma
classe que busca a imagem do feed de notícias, a checagem de versão do
QGIS e o conteúdo de plugins de terceiros. Os demais iniciadores
(QgsWmsCapabilitiesDownload, QgsWmsTiledImageDownloadHandler,
QgsWmsImageDownloadHandler, QgsBaseNetworkRequest do WFS,
QgsNewsFeedParser...) e o tráfego sem iniciador que o projeto não aponta
(tiles XYZ, QgsBlockingNetworkRequest, plugins) nunca são filtrados.

Limite conhecido: figura de prancha cuja expressão muda a cada avaliação
(`rand()`, `now()`) só é barrada na leitura do projeto; depois dela o
endereço avaliado já não coincide com o da requisição.
"""
import functools
import threading

from qgis.core import (
    Qgis,
    QgsLayoutItemHtml,
    QgsLayoutItemPicture,
    QgsLayoutObject,
    QgsNetworkAccessManager,
    QgsNetworkRequestParameters,
    QgsPathResolver,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication, QObject, QThread, QTimer, QUrl, pyqtSignal, pyqtSlot
from qgis.PyQt.QtNetwork import QNetworkRequest

from . import securitySettings as cfg

# QNetworkRequest.Attribute não tem membro para o atributo do QGIS (User + 3000).
ATRIBUTO_INICIADOR = QNetworkRequest.Attribute(
    int(QgsNetworkRequestParameters.RequestAttributes.AttributeInitiatorClass.value)
)
# Marca, na própria requisição, a busca de recurso que a guarda deixou passar:
# é por ela que o pré-processador de resposta sabe qual resposta acompanhar.
ATRIBUTO_RECURSO = QNetworkRequest.Attribute(int(QNetworkRequest.Attribute.User.value) + 7461)
PREFIXOS_INICIADOR_RECURSO = ("QgsAbstractContentCache",)
INICIADOR_BUSCADOR = "QgsNetworkContentFetcher"
URL_BLOQUEADA = "bloqueado:"
LIMITE_REGISTRO = 5000
ESPERA_JANELA_MS = 50


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
        self.idResposta = None
        self.idCaminho = None
        self.modo = cfg.PADRAO_MODO
        self.permitidos = []
        self._trava = threading.Lock()
        self._urlsDeProjeto = set()
        self._saltos = set()
        self._hostsAvisados = set()
        self._urlsLogadas = set()
        self.bloqueios = 0
        self._notificador = None
        self._projeto = None
        self._threadPrincipal = None
        self._lendoProjeto = False
        self._nivelLaco = 0
        self._ifaceLigada = False

    # ciclo de vida -------------------------------------------------------
    def install(self):
        if self.idRequisicao is not None:
            return
        self.recarregarConfiguracao()
        self._notificador = _Notificador(self.iface)
        app = QCoreApplication.instance()
        self._threadPrincipal = app.thread() if app is not None else QThread.currentThread()
        self.idRequisicao = QgsNetworkAccessManager.setRequestPreprocessor(self._preprocessarRequisicao)
        self.idResposta = QgsNetworkAccessManager.setReplyPreprocessor(self._preprocessarResposta)
        self.idCaminho = QgsPathResolver.setPathPreprocessor(self._registrarCaminho)
        self._projeto = QgsProject.instance()
        self._projeto.cleared.connect(self._aoLimparProjeto)
        self._projeto.readProject.connect(self._aoTerminarLeitura)
        if self.iface is not None:
            try:
                self.iface.newProjectCreated.connect(self._aoTerminarLeitura)
                self._ifaceLigada = True
            except Exception:
                self._ifaceLigada = False

    def uninstall(self):
        if self.idRequisicao is not None:
            QgsNetworkAccessManager.removeRequestPreprocessor(self.idRequisicao)
            self.idRequisicao = None
        if self.idResposta is not None:
            QgsNetworkAccessManager.removeReplyPreprocessor(self.idResposta)
            self.idResposta = None
        if self.idCaminho is not None:
            QgsPathResolver.removePathPreprocessor(self.idCaminho)
            self.idCaminho = None
        if self._projeto is not None:
            for sinal, slot in (
                (self._projeto.cleared, self._aoLimparProjeto),
                (self._projeto.readProject, self._aoTerminarLeitura),
            ):
                try:
                    sinal.disconnect(slot)
                except (TypeError, RuntimeError):
                    pass
            self._projeto = None
        if self._ifaceLigada:
            try:
                self.iface.newProjectCreated.disconnect(self._aoTerminarLeitura)
            except (TypeError, RuntimeError, AttributeError):
                pass
            self._ifaceLigada = False
        self._lendoProjeto = False
        self._notificador = None

    def recarregarConfiguracao(self):
        """Relê modo e destinos permitidos (também a cada projeto novo)."""
        modo, permitidos = cfg.lerModo(), cfg.lerHostsPermitidos()
        with self._trava:
            self.modo, self.permitidos = modo, permitidos

    # janela de leitura do projeto ----------------------------------------
    def _aoLimparProjeto(self):
        """
        O `cleared` abre a leitura de um projeto (QgsProject.read limpa antes
        de ler). A janela fecha no `readProject`, no `newProjectCreated` ou,
        se nenhum dos dois vier (projeto limpo sem leitura, leitura que
        falhou), quando o controle volta ao laço de eventos de onde o
        `clear()` foi chamado.
        """
        with self._trava:
            self._urlsDeProjeto.clear()
            self._saltos.clear()
            self._hostsAvisados.clear()
            self._urlsLogadas.clear()
            self._lendoProjeto = True
        self.recarregarConfiguracao()
        try:
            self._nivelLaco = QThread.currentThread().loopLevel()
            QTimer.singleShot(0, self._fecharJanelaSeOciosa)
        except Exception:
            self._lendoProjeto = False

    def _fecharJanelaSeOciosa(self):
        if not self._lendoProjeto or self.idRequisicao is None:
            return
        # Laço aninhado (a busca da figura de prancha abre um): a leitura
        # ainda está em curso.
        if QThread.currentThread().loopLevel() > self._nivelLaco:
            QTimer.singleShot(ESPERA_JANELA_MS, self._fecharJanelaSeOciosa)
            return
        self._lendoProjeto = False

    def _aoTerminarLeitura(self, *args):
        self._lendoProjeto = False

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
        iniciador = str(iniciador) if iniciador else ""
        if iniciador.startswith(PREFIXOS_INICIADOR_RECURSO):
            return True
        if iniciador and iniciador != INICIADOR_BUSCADOR:
            return False
        chave = chaveUrl(url)
        with self._trava:
            if chave in self._urlsDeProjeto:
                return True
            if not iniciador:
                return False
            if chave in self._saltos:
                return True
        if QThread.currentThread() != self._threadPrincipal:
            return False
        return self._lendoProjeto or self._ehFonteDePrancha(chave)

    def _ehFonteDePrancha(self, chave):
        """
        A URL é o endereço avaliado de uma figura ou de um quadro HTML de
        prancha do projeto aberto? Só na thread principal, de onde a prancha
        busca a figura (QgsLayoutItemPicture.loadRemotePicture).
        """
        try:
            for prancha in QgsProject.instance().layoutManager().layouts():
                for item in prancha.items():
                    if not isinstance(item, QgsLayoutItemPicture):
                        continue
                    caminho = item.evaluatedPath()
                    if ehRemoto(caminho) and chaveUrl(caminho) == chave:
                        return True
                for quadro in prancha.multiFrames():
                    if not isinstance(quadro, QgsLayoutItemHtml):
                        continue
                    if quadro.contentMode() != QgsLayoutItemHtml.ContentMode.Url:
                        continue
                    endereco = quadro.url().toString()
                    props = quadro.dataDefinedProperties()
                    if props.isActive(QgsLayoutObject.DataDefinedProperty.SourceUrl):
                        endereco, _ = props.valueAsString(
                            QgsLayoutObject.DataDefinedProperty.SourceUrl,
                            quadro.createExpressionContext(),
                            endereco,
                        )
                    endereco = (endereco or "").strip()
                    if ehRemoto(endereco) and chaveUrl(endereco) == chave:
                        return True
        except Exception as e:
            cfg.log(f"falha ao conferir as pranchas do projeto: {e!r}", Qgis.MessageLevel.Critical)
        return False

    def _preprocessarRequisicao(self, requisicao):
        try:
            if self.modo == cfg.MODO_DESLIGADO or not self.ehRecursoDeProjeto(requisicao):
                return ""
            url = requisicao.url()
            if cfg.hostPermitido(url.host(), url.port(), url.scheme().lower(), self.permitidos):
                requisicao.setAttribute(ATRIBUTO_RECURSO, True)
                return ""
            bloquear = self.modo == cfg.MODO_BLOQUEAR
            if bloquear:
                requisicao.setUrl(QUrl(URL_BLOQUEADA))
            else:
                requisicao.setAttribute(ATRIBUTO_RECURSO, True)
            self._relatar(url, requisicao.attribute(ATRIBUTO_INICIADOR), bloquear)
        except Exception as e:
            cfg.log(f"falha no filtro de rede: {e!r}", Qgis.MessageLevel.Critical)
        return ""

    # salto de redirecionamento -------------------------------------------
    def _preprocessarResposta(self, requisicao, resposta):
        """
        Acompanha a resposta da busca de recurso que passou: o destino de um
        3xx só é conhecido no fim dela, e o salto sai da mesma thread logo
        depois (a conexão daqui é anterior à do QgsNetworkContentFetcher,
        então roda antes).
        """
        try:
            if resposta is None or not requisicao.attribute(ATRIBUTO_RECURSO):
                return
            resposta.finished.connect(functools.partial(self._registrarSalto, resposta))
        except Exception as e:
            cfg.log(f"falha ao acompanhar a resposta: {e!r}", Qgis.MessageLevel.Critical)

    def _registrarSalto(self, resposta):
        try:
            alvo = resposta.attribute(QNetworkRequest.Attribute.RedirectionTargetAttribute)
            if alvo is None:
                return
            alvo = alvo if isinstance(alvo, QUrl) else QUrl(str(alvo))
            if alvo.isRelative():
                alvo = resposta.url().resolved(alvo)
            if alvo.scheme().lower() not in cfg.ESQUEMAS_REMOTOS:
                return
            with self._trava:
                if len(self._saltos) < LIMITE_REGISTRO:
                    self._saltos.add(chaveUrl(alvo))
        except Exception as e:
            cfg.log(f"falha ao registrar o redirecionamento: {e!r}", Qgis.MessageLevel.Critical)

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
