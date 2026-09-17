# -*- coding: utf-8 -*-
"""
Contorno para redes em que a pilha do QGIS nao consegue resolver o proxy.

Em maquina com proxy configurado no sistema e os hosts do Exercito na lista
de excecao (ProxyOverride com *.eb.mil.br, no Windows), o QGIS entrega ao
socket um proxy nao resolvido e a conexao morre antes de abrir, com
"The proxy type is invalid for this operation". Medido no QGIS 4.2.1: um
QTcpSocket cru, conectando por nome a bdgex.eb.mil.br:443, falha; o mesmo
socket com setProxy(NoProxy) conecta; e um QNetworkAccessManager proprio,
no mesmo processo, baixa o GetCapabilities inteiro.

Nada aqui roda em maquina sadia. O gerente proprio so entra depois que o
caminho normal do QGIS ja falhou, e a fabrica de proxy so e instalada
depois que esse retry provou que a maquina tem o defeito.
"""

from qgis.core import Qgis, QgsNetworkAccessManager
from qgis.PyQt.QtCore import QEventLoop, QTimer, QUrl
from qgis.PyQt.QtNetwork import (
    QNetworkAccessManager,
    QNetworkProxy,
    QNetworkProxyFactory,
    QNetworkProxyQuery,
    QNetworkReply,
    QNetworkRequest,
)

from DsgTools.core.Utils.utils import MessageRaiser

BDGEX_HOSTS = ("bdgex.eb.mil.br",)


def resolveProxy(url):
    """Resolve o proxy da URL pela configuracao do sistema e devolve um proxy
    CONCRETO. DefaultProxy nao serve: e justamente ele que o motor de socket
    recusa."""
    proxies = QNetworkProxyFactory.proxyForQuery(QNetworkProxyQuery(QUrl(url)))
    for proxy in proxies:
        if proxy.type() != QNetworkProxy.ProxyType.DefaultProxy:
            return proxy
    return QNetworkProxy(QNetworkProxy.ProxyType.NoProxy)


def fetchWithOwnManager(url, timeout=30000):
    """Baixa a URL com um QNetworkAccessManager proprio e proxy resolvido a
    mao. Devolve (corpo, mensagem_de_erro)."""
    manager = QNetworkAccessManager()
    manager.setProxy(resolveProxy(url))
    request = QNetworkRequest(QUrl(url))
    request.setRawHeader(b"User-Agent", b"Magic Browser")
    request.setAttribute(
        QNetworkRequest.Attribute.RedirectPolicyAttribute,
        QNetworkRequest.RedirectPolicy.NoLessSafeRedirectPolicy,
    )
    reply = manager.get(request)
    loop = QEventLoop()
    reply.finished.connect(loop.quit)
    QTimer.singleShot(timeout, loop.quit)
    # Sem entrada do usuário: o laço roda na thread da interface, e clique
    # reentrante aqui dispara a mesma ação de novo.
    loop.exec(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
    if reply.error() != QNetworkReply.NetworkError.NoError:
        return b"", reply.errorString()
    return bytes(reply.readAll()), ""


class BDGExProxyFactory(QNetworkProxyFactory):
    """Fabrica escopada aos hosts do BDGEx, instalada so em maquina que ja
    demonstrou o defeito. Fora desses hosts devolve lista vazia, e o QGIS
    segue o caminho normal dele."""

    def queryProxy(self, query=QNetworkProxyQuery()):
        host = query.url().host() or query.peerHostName()
        if not any(
            host == known or host.endswith("." + known) for known in BDGEX_HOSTS
        ):
            return []
        proxies = QNetworkProxyFactory.systemProxyForQuery(query)
        concrete = [
            proxy
            for proxy in proxies
            if proxy.type() != QNetworkProxy.ProxyType.DefaultProxy
        ]
        return concrete or [QNetworkProxy(QNetworkProxy.ProxyType.NoProxy)]


_installedFactory = None


def installProxyFactoryOnce():
    """Instala a fabrica no gerente de rede do QGIS, uma vez por sessao.

    ATENCAO, medido e nao explicado: com a fabrica na lista, a camada WMS do
    BDGEx passa a carregar e a desenhar (4 de 4 falhas sem ela, 2 de 2
    sucessos com ela, cache limpo a cada rodada). Mas queryProxy nunca e
    chamada, e uma fabrica que devolve proxy podre funciona igual, entao o
    efeito vem de inserir, nao do conteudo. Por isso so instalamos depois de
    constatar a falha, nunca por padrao.
    """
    global _installedFactory
    if _installedFactory is not None:
        return _installedFactory
    _installedFactory = BDGExProxyFactory()
    QgsNetworkAccessManager.instance().insertProxyFactory(_installedFactory)
    MessageRaiser().logMessage(
        "BDGEx: pilha de rede do QGIS nao resolveu o proxy desta maquina. "
        "Contorno instalado para os hosts do BDGEx.",
        Qgis.MessageLevel.Warning,
    )
    return _installedFactory


def removeProxyFactory():
    global _installedFactory
    if _installedFactory is None:
        return
    QgsNetworkAccessManager.instance().removeProxyFactory(_installedFactory)
    _installedFactory = None
