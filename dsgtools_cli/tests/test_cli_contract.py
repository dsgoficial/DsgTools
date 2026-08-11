# -*- coding: utf-8 -*-
"""
Testes das camadas que ficam ENTRE o chamador e o qgis_process: validação local
dos parâmetros, cache do contrato em disco e formatação compacta do `describe`.

Nenhum destes precisa de QGIS: o contrato é injetado como fixture, exatamente no
formato que o `qgis_process help --json` devolve (capturado de
`dsgtools:gridzonegenerator` no QGIS 4.0.0). É de propósito: a validação existe
para poupar a chamada cara, então testá-la não pode custar essa chamada.

Rodar:
    pytest dsgtools_cli/tests/test_cli_contract.py -v
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CLI_DIR = TESTS_DIR.parent
CLI_PY = CLI_DIR / "dsgtools_cli.py"

_spec = importlib.util.spec_from_file_location("dsgtools_cli_under_test_contract", CLI_PY)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)


# --------------------------------------------------------------------------
# Contrato de exemplo (formato real do `help --json`)
# --------------------------------------------------------------------------
def _param(ptype, optional=False, **extra):
    param = {
        "description": extra.pop("description", ""),
        "optional": optional,
        "is_advanced": extra.pop("is_advanced", False),
        "is_destination": extra.pop("is_destination", False),
        "default_value": extra.pop("default_value", None),
        "raw_definition": {"parameter_type": ptype, **extra.pop("raw_definition", {})},
    }
    param.update(extra)
    return param


HELP = {
    "algorithm_details": {
        "id": "dsgtools:gridzonegenerator",
        "name": "Generate Systematic Grid",
        "group": "Grid Algorithms",
    },
    "parameters": {
        "CRS": _param("crs", description="CRS"),
        "INDEX": _param("string", description="Index (comma-separated for multiple)"),
        "INDEX_TYPE": _param(
            "enum",
            description="Index type",
            default_value=0,
            available_options={"0": "MI/MIR", "1": "INOM"},
        ),
        "START_SCALE": _param(
            "enum",
            description="Base scale",
            default_value=0,
            available_options={"0": "1000k", "1": "500k", "2": "250k", "3": "100k", "4": "50k"},
        ),
        "OUTPUT": _param("sink", description="Created Frames", is_destination=True),
        "XSUBDIVISIONS": _param(
            "number", optional=True, is_advanced=True, description="Subdivisions on x"
        ),
    },
    "outputs": {"OUTPUT": {"type": "outputVector", "description": "Created Frames"}},
}

VALIDO = {
    "CRS": "EPSG:31982",
    "INDEX": "SF-22-Y-D",
    "INDEX_TYPE": 1,
    "START_SCALE": 2,
    "OUTPUT": "grid.gpkg",
}


def _mensagens(inputs, help_data=HELP):
    return [e["message"] for e in cli.validate_inputs(inputs, help_data)]


# --------------------------------------------------------------------------
# Validação local
# --------------------------------------------------------------------------
def test_entrada_valida_nao_gera_erro():
    assert cli.validate_inputs(VALIDO, HELP) == []


def test_opcional_omitido_nao_e_erro():
    assert "XSUBDIVISIONS" not in " ".join(_mensagens(VALIDO))


def test_obrigatorio_ausente_e_apontado():
    inputs = {k: v for k, v in VALIDO.items() if k != "CRS"}
    assert _mensagens(inputs) == ["parametro obrigatorio ausente: CRS"]


def test_saida_obrigatoria_ausente_e_apontada():
    """O qgis_process não inventa destino temporário: sem OUTPUT ele aborta."""
    inputs = {k: v for k, v in VALIDO.items() if k != "OUTPUT"}
    assert _mensagens(inputs) == ["parametro obrigatorio ausente: OUTPUT"]


def test_valor_none_conta_como_ausente():
    inputs = dict(VALIDO, CRS=None)
    assert _mensagens(inputs) == ["parametro obrigatorio ausente: CRS"]


def test_booleano_false_nao_conta_como_ausente():
    """Regressão: um teste de presença por falsidade reprovaria SELECTED=False."""
    help_data = {"parameters": {"SELECTED": _param("boolean")}}
    assert cli.validate_inputs({"SELECTED": False}, help_data) == []


def test_nome_inexistente_e_apontado_com_sugestao():
    """
    É o modo de falha mais traiçoeiro: o qgis_process IGNORA a chave desconhecida
    em silêncio, o parâmetro pretendido fica no padrão e o erro só aparece depois,
    disfarçado de erro de domínio.
    """
    inputs = dict(VALIDO)
    inputs["INDEXTYPE"] = inputs.pop("INDEX_TYPE")
    mensagens = _mensagens(inputs)
    assert any(m.startswith("parametro inexistente: INDEXTYPE") for m in mensagens)
    assert any("INDEX_TYPE" in m for m in mensagens)


def test_indice_de_enum_fora_da_faixa():
    assert _mensagens(dict(VALIDO, START_SCALE=99)) == ["START_SCALE: indice 99 fora da faixa"]


def test_rotulo_no_lugar_do_indice_devolve_o_indice_certo():
    mensagens = _mensagens(dict(VALIDO, START_SCALE="250k"))
    assert len(mensagens) == 1
    assert "nao e indice de opcao" in mensagens[0]
    assert "e 2" in mensagens[0]


def test_enum_aceita_lista_de_indices():
    assert cli.validate_inputs(dict(VALIDO, START_SCALE="2,4"), HELP) == []
    assert _mensagens(dict(VALIDO, START_SCALE="2,44")) == ["START_SCALE: indice 44 fora da faixa"]


def test_enum_de_string_estatica_nao_e_validado_por_indice():
    """
    Com uses_static_strings o valor É o rótulo, não o índice. Validar como índice
    reprovaria a chamada correta, e um falso positivo é pior que deixar o
    qgis_process reclamar.
    """
    help_data = {
        "parameters": {
            "MODE": _param(
                "enum",
                available_options={"0": "rapido", "1": "preciso"},
                raw_definition={"uses_static_strings": True},
            )
        }
    }
    assert cli.validate_inputs({"MODE": "preciso"}, help_data) == []


def test_enum_indices_normaliza_formatos():
    assert cli._enum_indices(3) == [3]
    assert cli._enum_indices("3") == [3]
    assert cli._enum_indices(" 1 , 3 ") == [1, 3]
    assert cli._enum_indices([1, 3]) == [1, 3]
    assert cli._enum_indices("50k") is None
    assert cli._enum_indices(True) is None  # bool é int em Python; não é índice


def test_varios_erros_saem_juntos():
    """Uma rodada de validação tem que render a lista inteira, não o primeiro erro."""
    mensagens = _mensagens({"START_SCALE": 99, "TIPO": 1})
    assert len(mensagens) == 6  # 4 obrigatórios ausentes + nome inexistente + enum


# --------------------------------------------------------------------------
# Mensagem de erro: o contrato vem junto
# --------------------------------------------------------------------------
def test_erro_imprime_o_contrato_dos_parametros_citados():
    """O chamador tem que conseguir corrigir sem uma segunda chamada (que custa segundos)."""
    inputs = dict(VALIDO, START_SCALE=99)
    texto = cli.format_validation_errors("dsgtools:gridzonegenerator", cli.validate_inputs(inputs, HELP), HELP)
    assert "START_SCALE" in texto
    assert "Base scale" in texto
    assert "0=1000k" in texto and "4=50k" in texto  # as opções válidas, não um ponteiro
    assert "--no-check" in texto


def test_erro_lista_os_parametros_validos():
    inputs = dict(VALIDO, FOO=1)
    texto = cli.format_validation_errors("dsgtools:x", cli.validate_inputs(inputs, HELP), HELP)
    for name in HELP["parameters"]:
        assert name in texto


def test_format_param_marca_obrigatorio_saida_e_avancado():
    linha = cli.format_param("OUTPUT", HELP["parameters"]["OUTPUT"])
    assert "obrigatorio" in linha and "saida" in linha and "sink" in linha
    linha = cli.format_param("XSUBDIVISIONS", HELP["parameters"]["XSUBDIVISIONS"])
    assert "opcional" in linha and "avancado" in linha


# --------------------------------------------------------------------------
# describe compacto
# --------------------------------------------------------------------------
ANOTACAO = {
    "description": "Gera a moldura sistemática a partir de um índice.",
    "constraints": ["STOP_SCALE não pode ser mais grossa que START_SCALE."],
    "example": {"START_SCALE": 2, "INDEX": "SF-22-Y-D", "OUTPUT": "grid.gpkg"},
}


def test_describe_compacto_nao_e_json():
    texto = cli.render_describe(HELP, {})
    with pytest.raises(json.JSONDecodeError):
        json.loads(texto)


def test_describe_compacto_da_uma_linha_por_parametro():
    cabecas = [linha.split()[0] for linha in cli.render_describe(HELP, {}).splitlines() if linha.strip()]
    for name in HELP["parameters"]:
        assert cabecas.count(name) == 1, f"{name} apareceu {cabecas.count(name)} vez(es)"


def test_describe_compacto_traz_tipo_obrigatoriedade_e_opcoes():
    texto = cli.render_describe(HELP, {})
    assert "dsgtools:gridzonegenerator" in texto
    assert "crs" in texto and "enum" in texto
    assert "0=MI/MIR" in texto and "1=INOM" in texto


def test_describe_compacto_traz_a_prosa_curada():
    texto = cli.render_describe(HELP, ANOTACAO)
    assert "moldura sistemática" in texto
    assert "mais grossa que START_SCALE" in texto


def test_describe_compacto_vira_linha_de_comando_pronta():
    texto = cli.render_describe(HELP, ANOTACAO)
    assert "run dsgtools:gridzonegenerator START_SCALE=2 INDEX=SF-22-Y-D OUTPUT=grid.gpkg" in texto


def test_exemplo_com_espaco_sai_entre_aspas():
    assert cli._example_args({"INPUT": "c:/dados de campo.gpkg"}) == '"INPUT=c:/dados de campo.gpkg"'


# --------------------------------------------------------------------------
# Cache do contrato
# --------------------------------------------------------------------------
@pytest.fixture
def cache_isolado(tmp_path, monkeypatch):
    """Cache numa pasta descartável, com a impressão digital memoizada zerada."""
    monkeypatch.setenv("DSGTOOLS_CLI_CACHE", str(tmp_path / "cache"))
    monkeypatch.setattr(cli, "_fingerprint", None)
    yield tmp_path / "cache"
    cli._fingerprint = None


def test_cache_grava_e_le(cache_isolado):
    cli.cache_write("gridzonegenerator", HELP)
    assert cli.cache_read("gridzonegenerator") == HELP
    assert cli.cache_read("outroalgoritmo") is None


def test_cache_nome_de_arquivo_sem_dois_pontos(cache_isolado):
    """':' não é caractere válido em nome de arquivo no Windows."""
    cli.cache_write("dsgtools:gridzonegenerator", HELP)
    arquivos = list(cache_isolado.glob("*.json"))
    assert len(arquivos) == 1
    assert ":" not in arquivos[0].name


def test_cache_invalida_quando_a_impressao_digital_muda(cache_isolado):
    cli.cache_write("gridzonegenerator", HELP)
    cli._fingerprint = "outra-coisa"
    assert cli.cache_read("gridzonegenerator") is None


def test_cache_ignora_arquivo_corrompido(cache_isolado):
    """Cache é otimização: um JSON pela metade não pode derrubar o comando."""
    cli.cache_write("gridzonegenerator", HELP)
    alvo = next(cache_isolado.glob("*.json"))
    alvo.write_text("{isso nao e json", encoding="utf-8")
    assert cli.cache_read("gridzonegenerator") is None


def test_cache_write_nao_estoura_com_pasta_impossivel(monkeypatch, tmp_path):
    """/tmp somente-leitura não pode impedir de rodar o algoritmo."""
    arquivo = tmp_path / "arquivo"
    arquivo.write_text("x", encoding="utf-8")
    monkeypatch.setenv("DSGTOOLS_CLI_CACHE", str(arquivo / "sub"))
    monkeypatch.setattr(cli, "_fingerprint", "fixa")
    cli.cache_write("gridzonegenerator", HELP)  # não deve levantar
    cli._fingerprint = None


def test_help_json_cached_so_chama_o_qgis_uma_vez(cache_isolado, monkeypatch):
    """O ganho inteiro do cache: a 2ª chamada não sobe o QGIS de novo."""
    chamadas = []

    def _fake(alg):
        chamadas.append(alg)
        return HELP, 0

    monkeypatch.setattr(cli, "_help_json", _fake)
    primeiro = cli.help_json_cached("gridzonegenerator")
    segundo = cli.help_json_cached("gridzonegenerator")
    assert primeiro == (HELP, 0, False)
    assert segundo == (HELP, 0, True)
    assert len(chamadas) == 1


def test_refresh_cache_ignora_o_cache(cache_isolado, monkeypatch):
    chamadas = []
    monkeypatch.setattr(cli, "_help_json", lambda alg: (chamadas.append(alg), (HELP, 0))[1])
    cli.help_json_cached("gridzonegenerator")
    cli.help_json_cached("gridzonegenerator", refresh=True)
    assert len(chamadas) == 2


def test_falha_do_help_nao_vai_para_o_cache(cache_isolado, monkeypatch):
    """Cachear um contrato vazio congelaria o ambiente quebrado."""
    monkeypatch.setattr(cli, "_help_json", lambda alg: (None, 1))
    assert cli.help_json_cached("gridzonegenerator") == (None, 1, False)
    assert cli.cache_read("gridzonegenerator") is None


# --------------------------------------------------------------------------
# dry-run
# --------------------------------------------------------------------------
def test_dry_run_mostra_o_payload_e_traduz_o_enum():
    texto = cli.render_dry_run("dsgtools:gridzonegenerator", VALIDO, HELP)
    assert '"INDEX_TYPE": 1' in texto  # o payload exato que iria para o stdin
    assert "-> INOM" in texto          # o rótulo por trás do índice
    assert "XSUBDIVISIONS" in texto    # o que ficou de fora
    assert "nada foi executado" in texto


def test_dry_run_sem_contrato_avisa_que_nao_validou():
    texto = cli.render_dry_run("dsgtools:x", VALIDO, None)
    assert "NAO conferida" in texto


# --------------------------------------------------------------------------
# Fim a fim, pelo main() (sem QGIS: o contrato vem monkeypatchado)
# --------------------------------------------------------------------------
def test_run_reprovado_devolve_2_e_nao_executa(cache_isolado, monkeypatch, capsys):
    monkeypatch.setattr(cli, "_help_json", lambda alg: (HELP, 0))
    monkeypatch.setattr(
        cli,
        "call_qgis_process",
        lambda *a, **k: pytest.fail("nao pode executar com parametro invalido"),
    )
    assert cli.main(["run", "gridzonegenerator", "START_SCALE=99"]) == 2
    assert "fora da faixa" in capsys.readouterr().err


def test_no_check_pula_a_validacao(cache_isolado, monkeypatch):
    monkeypatch.setattr(cli, "_help_json", lambda alg: pytest.fail("--no-check nao pode buscar contrato"))
    monkeypatch.setattr(cli, "call_qgis_process", lambda *a, **k: (0, '{"results": {}}', ""))
    assert cli.main(["run", "gridzonegenerator", "START_SCALE=99", "--no-check"]) == 0


def test_dry_run_nao_chama_o_qgis(cache_isolado, monkeypatch, capsys):
    monkeypatch.setattr(cli, "_help_json", lambda alg: (HELP, 0))
    monkeypatch.setattr(
        cli, "call_qgis_process", lambda *a, **k: pytest.fail("dry-run nao pode executar")
    )
    assert cli.main(["run", "gridzonegenerator", *[f"{k}={v}" for k, v in VALIDO.items()], "--dry-run"]) == 0
    assert "[dry-run]" in capsys.readouterr().out


def test_run_sem_contrato_avisa_e_segue(cache_isolado, monkeypatch, capsys):
    """A validação é rede, não portão: sem contrato, o erro real do qgis_process
    tem que continuar aparecendo, em vez de ser mascarado por um erro nosso."""
    monkeypatch.setattr(cli, "_help_json", lambda alg: (None, 1))
    monkeypatch.setattr(cli, "call_qgis_process", lambda *a, **k: (1, "", "Algorithm not found!"))
    assert cli.main(["run", "gridzonegenerator"]) == 1
    err = capsys.readouterr().err
    assert "AVISO" in err and "Algorithm not found!" in err
