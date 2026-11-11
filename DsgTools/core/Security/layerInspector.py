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

Inspeção das camadas ao carregar (CDCiber 2026, achados 4.3, 4.4 e 4.6.2).

Roda no `QgsProject.layersAdded`, que o QGIS emite durante a leitura do
projeto, antes de o operador abrir qualquer formulário:

- sinaliza símbolo SVG ou imagem com caminho remoto, inclusive pela
  propriedade data-defined (Name/File) com expressão que monta URL ou lê
  `env()`. A barreira de rede é a NetworkGuard; aqui é o aviso;
- formulário .ui remoto: troca o layout para o gerado pelo QGIS, salvo
  quando o destino está em `dsgtools/security/allowedHosts`;
- formulário .ui local: mede profundidade de aninhamento e tamanho com o
  expat em modo incremental (sem recursão e sem montar árvore). Acima do
  teto, com XML inválido ou com DOCTYPE, troca para o gerado. No QGIS 4.2.1
  um .ui com 4.000 níveis derruba o processo ao instanciar o
  QgsAttributeForm (estouro de pilha), então o .ui nunca é instanciado aqui.
"""
import os
import xml.parsers.expat

from qgis.core import (
    Qgis,
    QgsProject,
    QgsRasterFillSymbolLayer,
    QgsRasterLineSymbolLayer,
    QgsRasterMarkerSymbolLayer,
    QgsRenderContext,
    QgsSVGFillSymbolLayer,
    QgsSvgMarkerSymbolLayer,
    QgsSymbolLayer,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QUrl

from . import securitySettings as cfg

TAMANHO_BLOCO = 64 * 1024
GATILHOS_EXPRESSAO = ("://", "http", "ftp", "env(")


class _Recusa(Exception):
    pass


def avaliarFormularioUi(caminho, profundidadeMaxima=None, bytesMaximo=None):
    """
    Devolve (aceito, motivo). Lê o arquivo em blocos e para no primeiro
    elemento além do teto; nunca constrói o formulário.
    """
    tetoProf, tetoBytes = cfg.lerTetosUi()
    profundidadeMaxima = profundidadeMaxima or tetoProf
    bytesMaximo = bytesMaximo or tetoBytes
    try:
        tamanho = os.path.getsize(caminho)
    except OSError as e:
        return False, f"não foi possível ler o arquivo ({e.strerror})"
    if tamanho > bytesMaximo:
        return False, f"tamanho de {tamanho} bytes acima do teto de {bytesMaximo}"

    estado = {"prof": 0, "max": 0}

    def abre(nome, atributos):
        estado["prof"] += 1
        if estado["prof"] > estado["max"]:
            estado["max"] = estado["prof"]
        if estado["prof"] > profundidadeMaxima:
            raise _Recusa(f"aninhamento acima do teto de {profundidadeMaxima} níveis")

    def fecha(nome):
        estado["prof"] -= 1

    def doctype(*args):
        # O Qt Designer não grava DOCTYPE; recusar elimina expansão de entidade.
        raise _Recusa("DOCTYPE no formulário")

    leitor = xml.parsers.expat.ParserCreate()
    leitor.StartElementHandler = abre
    leitor.EndElementHandler = fecha
    leitor.StartDoctypeDeclHandler = doctype
    leitor.EntityDeclHandler = doctype
    try:
        with open(caminho, "rb") as arq:
            while True:
                bloco = arq.read(TAMANHO_BLOCO)
                if not bloco:
                    leitor.Parse(b"", True)
                    break
                leitor.Parse(bloco, False)
    except _Recusa as e:
        return False, str(e)
    except xml.parsers.expat.ExpatError as e:
        return False, f"XML inválido ({xml.parsers.expat.ErrorString(e.code)}, linha {e.lineno})"
    except OSError as e:
        return False, f"não foi possível ler o arquivo ({e.strerror})"
    return True, f"profundidade {estado['max']}, {tamanho} bytes"


def _caminhoLocal(texto):
    url = QUrl(texto)
    if url.isLocalFile():
        return url.toLocalFile()
    return texto


def _caminhosEstaticos(camada):
    if isinstance(camada, QgsSvgMarkerSymbolLayer):
        return [("SVG", camada.path())]
    if isinstance(camada, QgsSVGFillSymbolLayer):
        return [("SVG", camada.svgFilePath())]
    if isinstance(camada, QgsRasterFillSymbolLayer):
        return [("imagem", camada.imageFilePath())]
    if isinstance(camada, (QgsRasterMarkerSymbolLayer, QgsRasterLineSymbolLayer)):
        return [("imagem", camada.path())]
    return []


def _propriedadesDeCaminho(camada):
    """Expressões e valores estáticos das propriedades de arquivo da camada de símbolo."""
    achados = []
    props = camada.dataDefinedProperties()
    for chave in (QgsSymbolLayer.Property.Name, QgsSymbolLayer.Property.File):
        if not props.isActive(chave):
            continue
        p = props.property(chave)
        tipo = p.propertyType()
        if tipo == Qgis.PropertyType.Expression:
            achados.append(("expressão", p.expressionString()))
        elif tipo == Qgis.PropertyType.Static:
            achados.append(("valor fixo", str(p.staticValue())))
    return achados


def achadosDeSimbologia(camadaMapa):
    """Lista de textos, um por caminho remoto ou expressão suspeita na simbologia."""
    renderer = camadaMapa.renderer() if isinstance(camadaMapa, QgsVectorLayer) else None
    if renderer is None:
        return []
    achados = []
    pilha = list(renderer.symbols(QgsRenderContext()))
    vistos = 0
    while pilha and vistos < 10000:
        simbolo = pilha.pop()
        vistos += 1
        if simbolo is None:
            continue
        for camada in simbolo.symbolLayers():
            for rotulo, caminho in _caminhosEstaticos(camada):
                if _ehRemoto(caminho):
                    achados.append(f"{rotulo} remoto: {_semQuery(caminho)}")
            for rotulo, texto in _propriedadesDeCaminho(camada):
                minusc = (texto or "").lower()
                if rotulo == "valor fixo":
                    if _ehRemoto(texto):
                        achados.append(f"caminho data-defined remoto: {_semQuery(texto)}")
                elif any(g in minusc for g in GATILHOS_EXPRESSAO):
                    achados.append(f"caminho data-defined por expressão com URL ou env(): {texto[:200]}")
            sub = camada.subSymbol()
            if sub is not None:
                pilha.append(sub)
    return achados


def _ehRemoto(texto):
    return bool(texto) and QUrl(str(texto)).scheme().lower() in cfg.ESQUEMAS_REMOTOS


def _semQuery(texto):
    url = QUrl(str(texto))
    if url.scheme():
        return url.adjusted(QUrl.UrlFormattingOption.RemoveQuery).toString()[:200]
    return str(texto)[:200]


class LayerInspector:
    def __init__(self, iface=None, networkGuard=None):
        self.iface = iface
        self.networkGuard = networkGuard
        self._projeto = None
        self._conectadas = {}

    def install(self):
        if self._projeto is not None:
            return
        self._projeto = QgsProject.instance()
        self._projeto.layersAdded.connect(self.aoAdicionarCamadas)

    def uninstall(self):
        if self._projeto is None:
            return
        try:
            self._projeto.layersAdded.disconnect(self.aoAdicionarCamadas)
        except (TypeError, RuntimeError):
            pass
        for camadaId, (camada, slot) in list(self._conectadas.items()):
            try:
                camada.editFormConfigChanged.disconnect(slot)
            except (TypeError, RuntimeError):
                pass
        self._conectadas.clear()
        self._projeto = None

    def aoAdicionarCamadas(self, camadas):
        if not cfg.lerInspecaoLigada():
            return
        relatorio = []
        for camada in camadas:
            try:
                relatorio.extend(self.inspecionarCamada(camada))
                self._vigiarFormulario(camada)
            except Exception as e:
                cfg.log(f"falha ao inspecionar a camada {camada.name()}: {e!r}", Qgis.MessageLevel.Critical)
        self._avisar(relatorio)

    def _vigiarFormulario(self, camada):
        # Estilo carregado depois (QML) também pode trazer formulário.
        if not isinstance(camada, QgsVectorLayer) or camada.id() in self._conectadas:
            return

        def slot(c=camada):
            try:
                self._avisar(self.inspecionarFormulario(c))
            except Exception:
                pass

        camada.editFormConfigChanged.connect(slot)
        self._conectadas[camada.id()] = (camada, slot)
        camada.willBeDeleted.connect(lambda cid=camada.id(): self._conectadas.pop(cid, None))

    def inspecionarCamada(self, camada):
        """Devolve a lista de mensagens (já aplicando a troca de formulário)."""
        mensagens = []
        for achado in achadosDeSimbologia(camada):
            mensagens.append(f"camada '{camada.name()}': {achado}")
        mensagens.extend(self.inspecionarFormulario(camada))
        return mensagens

    def inspecionarFormulario(self, camada):
        if not isinstance(camada, QgsVectorLayer):
            return []
        config = camada.editFormConfig()
        if config.layout() != Qgis.AttributeFormLayout.UiFile:
            return []
        uiForm = config.uiForm()
        if not uiForm:
            return []
        if _ehRemoto(uiForm):
            if self.networkGuard is not None:
                self.networkGuard.registrarRecursoDeProjeto(uiForm)
            url = QUrl(str(uiForm))
            if cfg.hostPermitido(url.host(), url.port(), url.scheme().lower(), cfg.lerHostsPermitidos()):
                # Destino declarado confiável em allowedHosts: o formulário fica,
                # e a guarda de rede ainda barra o redirecionamento para fora.
                return []
            motivo = (
                f"formulário remoto ({_semQuery(uiForm)}), destino fora de {cfg.PREFIXO}allowedHosts"
            )
        else:
            caminho = _caminhoLocal(uiForm)
            if not os.path.exists(caminho):
                return []
            aceito, motivo = avaliarFormularioUi(caminho)
            if aceito:
                return []
            motivo = f"formulário {os.path.basename(caminho)}: {motivo}"
        config.setLayout(Qgis.AttributeFormLayout.AutoGenerated)
        camada.setEditFormConfig(config)
        return [f"camada '{camada.name()}': {motivo}; trocado para o formulário gerado pelo QGIS"]

    def _avisar(self, mensagens):
        if not mensagens:
            return
        for m in mensagens:
            cfg.log(m)
        if self.iface is not None:
            resumo = mensagens[0] if len(mensagens) == 1 else (
                f"{len(mensagens)} itens suspeitos nas camadas carregadas (SVG ou imagem remota, "
                "formulário remoto ou acima do teto). Detalhes no log."
            )
            try:
                self.iface.messageBar().pushMessage(cfg.TAG_LOG, resumo, Qgis.MessageLevel.Warning, 15)
            except Exception:
                pass
