# -*- coding: utf-8 -*-
"""
Contorno para redes em que a pilha do QGIS nao consegue resolver o proxy.

Em maquina com proxy configurado no sistema e o proxy do QGIS em branco, o
QGIS nao alcanca NENHUM host que o sistema manda contatar diretamente. Nao e
um problema do BDGEx nem deste plugin: medido no QGIS 4.2.1, com um
QTcpSocket cru, os sete hosts que o sistema manda ir direto falham todos com
"The proxy type is invalid for this operation" e nem abrem o socket, e os
dois que devem passar pelo proxy chegam la e so falham em autenticacao. So o
loopback escapa, porque o Qt o trata a parte.

O que sustenta a explicacao: o socket nasce com DefaultProxy, o Qt escolhe o
motor de socket direto por causa da resposta NoProxy, e na hora de conectar o
DefaultProxy vira o applicationProxy, que e o proxy do sistema; o motor
direto so aceita NoProxy ou DefaultProxy e recusa pelo tipo. A mensagem vem
da tabela de erros do QNativeSocketEngine. As duas unicas alavancas que
consertam sao justamente as que mexem nesse valor.

Com setProxy(NoProxy) o mesmo socket conecta, e um QNetworkAccessManager
proprio, no mesmo processo, baixa o GetCapabilities inteiro (41.563 bytes).

ALCANCE. Isto resgata apenas o GetCapabilities, que e o que monta o menu do
BDGEx. O desenho da camada acontece na thread de renderizacao, dentro do
provedor WMS, fora do alcance do plugin, e la o defeito continua: a camada
entra sem erro nenhum e a tela fica em branco. A unica alavanca medida que
conserta o desenho e o applicationProxy, que vale para o processo inteiro e
ainda desliga o usesSystemConfiguration do Qt, mandando TODO host direto: um
plugin nao pode assumir isso sem arriscar tirar o proxy do QGIS todo.

A correcao esta do lado da configuracao, e cobre tela, WFS e os hosts
internos de uma vez: preencher o proxy em Configuracoes, Opcoes, Rede. Serve
tanto rotear o BDGEx pelo proxy quanto preencher o proxy e por o host do
BDGEx em "Excluir URLs" para ele ir direto; as duas foram medidas
desenhando. O que nao funciona e deixar o proxy do QGIS em branco. E isso que
avisamos ao usuario quando o retry entra em acao.
"""

from qgis.core import Qgis
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

_proxyAdviceShown = False


def resolveProxy(url):
    """Resolve o proxy da URL pela configuracao do sistema e devolve um proxy
    CONCRETO. DefaultProxy nao serve: e justamente ele que, substituido pelo
    applicationProxy, faz o motor de socket direto recusar a conexao."""
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
    # Sem entrada do usuario: o laco roda na thread da interface, e clique
    # reentrante aqui dispara a mesma acao de novo.
    loop.exec(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
    if reply.error() != QNetworkReply.NetworkError.NoError:
        return b"", reply.errorString()
    return bytes(reply.readAll()), ""


def adviseProxyConfiguration(tr):
    """Avisa, uma vez por sessao, que a maquina precisa do proxy preenchido
    nas Opcoes do QGIS. Sem isso as camadas entram sem erro e nao desenham,
    porque o provedor WMS renderiza em outra thread e o plugin nao alcanca."""
    global _proxyAdviceShown
    MessageRaiser().logMessage(
        tr(
            "BDGEx: the QGIS network stack could not resolve the proxy on this "
            "machine, so GetCapabilities was retried with a private network "
            "manager. On this machine QGIS cannot reach any host the system "
            "tells it to contact directly, BDGEx included. Layer rendering "
            "runs in the WMS provider, outside the plugin, and will stay blank "
            "until the proxy is configured under Settings > Options > Network: "
            "either route BDGEx through the proxy, or fill the proxy in and "
            "add the BDGEx host to Exclude URLs so it goes direct. Both work; "
            "leaving the proxy blank there does not."
        ),
        Qgis.MessageLevel.Warning,
    )
    if _proxyAdviceShown:
        return
    _proxyAdviceShown = True
    try:
        MessageRaiser().raiseIfaceMessage(
            tr("BDGEx layers (DSGTools)"),
            tr(
                "This machine's network settings prevent QGIS from reaching "
                "BDGEx. The menu was loaded, but layers will not draw until "
                "the proxy is configured under Settings > Options > Network, "
                "either routing BDGEx through the proxy or excluding the "
                "BDGEx host there so it goes direct."
            ),
            Qgis.MessageLevel.Warning,
            10,
        )
    except Exception:
        # Sem interface (qgis_process, dsgtools_cli) nao ha barra de
        # mensagens, e o aviso ja foi para o log. O retry deu certo, entao
        # nao e aqui que a chamada pode morrer.
        pass
