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

Configuração da proteção contra recursos remotos de projeto (avaliação de
segurança do CDCiber, 2026, achados 4.3, 4.4 e 4.6.2).

Chaves em QgsSettings, sob `dsgtools/security/`:

- `resourceMode`: `block` (padrão), `warn` ou `off`. Vale para as buscas de
  rede de RECURSO DE PROJETO (SVG, imagem, formulário .ui, figura de
  prancha); o tráfego dos provedores de dados nunca é filtrado.
- `allowedHosts`: lista de destinos permitidos para recurso de projeto,
  cada um `host` (qualquer porta), `host:porta` ou `.dominio` (o domínio e
  os subdomínios). Padrão: vazia.
- `inspectLayers`: inspeção das camadas ao carregar (padrão: true).
- `uiMaxDepth`: profundidade máxima de aninhamento de elementos no .ui
  local (padrão: 256).
- `uiMaxBytes`: tamanho máximo do .ui local em bytes (padrão: 5 MiB).
"""
from qgis.core import Qgis, QgsMessageLog, QgsSettings

TAG_LOG = "DSGTools Segurança"
PREFIXO = "dsgtools/security/"

MODO_BLOQUEAR = "block"
MODO_AVISAR = "warn"
MODO_DESLIGADO = "off"
MODOS = (MODO_BLOQUEAR, MODO_AVISAR, MODO_DESLIGADO)

PADRAO_MODO = MODO_BLOQUEAR
PADRAO_UI_PROFUNDIDADE = 256
PADRAO_UI_BYTES = 5 * 1024 * 1024

# Esquemas que saem para a rede pelo QgsNetworkAccessManager.
ESQUEMAS_REMOTOS = ("http", "https", "ftp")
PORTA_PADRAO = {"http": 80, "https": 443, "ftp": 21}


def log(mensagem, nivel=Qgis.MessageLevel.Warning):
    QgsMessageLog.logMessage(mensagem, TAG_LOG, nivel)


def _texto(valor):
    if valor is None:
        return ""
    return str(valor).strip()


def lerModo(settings=None):
    s = settings or QgsSettings()
    modo = _texto(s.value(PREFIXO + "resourceMode", PADRAO_MODO)).lower()
    if modo not in MODOS:
        # Valor desconhecido não pode desligar a proteção.
        log(f"modo '{modo}' desconhecido em {PREFIXO}resourceMode; usando '{PADRAO_MODO}'")
        modo = PADRAO_MODO
    return modo


def lerHostsPermitidos(settings=None):
    """Lista normalizada (minúsculas, sem vazios). Aceita lista ou texto separado por vírgula."""
    s = settings or QgsSettings()
    valor = s.value(PREFIXO + "allowedHosts", [])
    if valor is None:
        itens = []
    elif isinstance(valor, (list, tuple)):
        itens = [str(v) for v in valor]
    else:
        itens = str(valor).replace(";", ",").split(",")
    return [i.strip().lower() for i in itens if i and i.strip()]


def _bool(valor, padrao):
    if valor is None:
        return padrao
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().lower() not in ("0", "false", "no", "nao", "não", "off", "")


def _int(valor, padrao):
    try:
        n = int(valor)
        return n if n > 0 else padrao
    except (TypeError, ValueError):
        return padrao


def lerInspecaoLigada(settings=None):
    s = settings or QgsSettings()
    return _bool(s.value(PREFIXO + "inspectLayers", True), True)


def lerTetosUi(settings=None):
    s = settings or QgsSettings()
    return (
        _int(s.value(PREFIXO + "uiMaxDepth", PADRAO_UI_PROFUNDIDADE), PADRAO_UI_PROFUNDIDADE),
        _int(s.value(PREFIXO + "uiMaxBytes", PADRAO_UI_BYTES), PADRAO_UI_BYTES),
    )


def hostPermitido(host, porta, esquema, permitidos):
    """
    `permitidos` vem de lerHostsPermitidos. `host` sem porta casa qualquer
    porta; `host:porta` casa só a porta (a padrão do esquema quando a URL não
    traz porta); `.dominio` casa o domínio e os subdomínios.
    """
    host = (host or "").lower().strip("[]")
    if not host:
        return False
    if porta is None or porta < 0:
        porta = PORTA_PADRAO.get(esquema, -1)
    for item in permitidos:
        if item.startswith("*."):
            item = item[1:]
        if item.startswith("."):
            if host == item[1:] or host.endswith(item):
                return True
            continue
        alvo, portaItem = item, None
        if item.startswith("["):
            # IPv6: [::1] ou [::1]:8080
            fecha = item.find("]")
            alvo = item[1:fecha]
            resto = item[fecha + 1:]
            if resto.startswith(":") and resto[1:].isdigit():
                portaItem = int(resto[1:])
        elif item.count(":") == 1:
            alvo, p = item.split(":")
            if p.isdigit():
                portaItem = int(p)
        if alvo == host and (portaItem is None or portaItem == porta):
            return True
    return False
