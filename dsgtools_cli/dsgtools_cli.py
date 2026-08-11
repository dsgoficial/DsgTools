#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dsgtools-cli — executa algoritmos de Processing do DSGTools por linha de comando,
de forma headless, encapsulando o utilitario oficial `qgis_process` do QGIS.

Permite descobrir quais algoritmos o DSGTools expoe, inspecionar os parametros de
cada um e executa-los passando os valores, sem abrir o QGIS Desktop. Util tanto para
uso manual quanto em automacoes/scripts.

A fonte da verdade e sempre o proprio `qgis_process` (consultado ao vivo): a lista e
os parametros estao sempre corretos e escalam para centenas de algoritmos sem nenhum
catalogo pre-gerado. O arquivo opcional `annotations.json` apenas enriquece algoritmos
especificos com conhecimento de dominio (regras e exemplos) que nao da para extrair
automaticamente do `qgis_process`.

Comandos
--------
  list                      Lista os algoritmos do DSGTools.
  describe <alg>            Mostra os parametros de um algoritmo (resumo + anotacoes).
  run <alg> [KEY=VALUE ...] Valida e executa um algoritmo.
  doctor                    Diagnostica o ambiente (qgis_process, provider carregado).
  cache                     Mostra ou limpa o cache local do contrato dos algoritmos.

Antes de executar, o `run` valida os parametros contra o contrato do proprio
algoritmo (nome inexistente, obrigatorio ausente, indice de enum fora da faixa) e,
quando reprova, imprime o contrato dos parametros citados. O contrato vem de uma
chamada ao qgis_process, que e cara (segundos), entao fica em cache em disco,
invalidado pela impressao digital do ambiente (ver `cache`). Escapes: `--no-check`
pula a validacao e `--refresh-cache` forca reler o contrato ao vivo.

Exemplos
--------
  python dsgtools_cli.py list
  python dsgtools_cli.py describe dsgtools:gridzonegenerator
  python dsgtools_cli.py run dsgtools:gridzonegenerator \\
      START_SCALE=2 STOP_SCALE=4 INDEX_TYPE=1 INDEX=SF-22-Y-D \\
      CRS=EPSG:31982 OUTPUT=grid.gpkg
  python dsgtools_cli.py run dsgtools:createframeswithconstraintalgorithm \\
      INPUT=area.gpkg STOP_SCALE=3 OUTPUT=frames.gpkg --dry-run

O id do algoritmo pode ser passado com ou sem o prefixo "dsgtools:".

Codigos de saida: 0 sucesso, 2 reprovado na validacao local (nada foi executado),
qualquer outro e o codigo do proprio qgis_process.
"""
import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

PROVIDER = "dsgtools"
HERE = Path(__file__).resolve().parent
ANNOTATIONS_PATH = HERE / "annotations.json"
# O pacote do plugin que o QGIS carrega vive ao lado deste CLI, no mesmo repo.
PLUGIN_DIR = HERE.parent / "DsgTools"
# Muda quando o FORMATO do arquivo de cache muda, para invalidar entradas antigas
# sem precisar limpar o cache na mao.
CACHE_FORMAT = 1
WIDTH = 92

_qgis_process_path = None  # cache (apenas resultados positivos)
_fingerprint = None  # cache em memoria (o stat e barato, mas o run chama varias vezes)


# ---------------------------------------------------------------------------
# qgis_process
# ---------------------------------------------------------------------------
def _version_key(path):
    """Chave de ordenacao por versao extraida do caminho, p.ex. 'QGIS 3.40.0' deve
    vir DEPOIS de 'QGIS 3.8' (a ordenacao lexicografica de string erraria isso)."""
    return tuple(int(n) for n in re.findall(r"\d+", path)[:4])


def find_qgis_process():
    """Retorna o caminho do executavel/bat do qgis_process, ou None.

    Memoiza apenas resultados positivos: se nao encontrar, volta a procurar na
    proxima chamada (evita cachear um None permanente — relevante para uso como
    modulo/testes que definem DSGTOOLS_QGIS_PROCESS depois do import).
    """
    global _qgis_process_path
    if _qgis_process_path is not None:
        return _qgis_process_path

    # 1. Override explicito
    env = os.environ.get("DSGTOOLS_QGIS_PROCESS")
    if env and Path(env).exists():
        _qgis_process_path = env
        return env

    # 2. PATH
    for name in ("qgis_process", "qgis_process.bin", "qgis_process-qgis.bat"):
        found = shutil.which(name)
        if found:
            _qgis_process_path = found
            return found

    # 3. Locais de instalacao mais comuns
    candidates = []
    if sys.platform.startswith("win"):
        program_dirs = {
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramW6432", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        }
        for pf in filter(None, program_dirs):
            candidates += glob.glob(os.path.join(pf, "QGIS *", "bin", "qgis_process-qgis.bat"))
        for root in (r"C:\OSGeo4W", r"C:\OSGeo4W64"):
            candidates += glob.glob(os.path.join(root, "bin", "qgis_process*.bat"))
    elif sys.platform == "darwin":
        candidates += glob.glob("/Applications/QGIS*.app/Contents/MacOS/bin/qgis_process")
    else:
        candidates += ["/usr/bin/qgis_process", "/usr/local/bin/qgis_process"]
        candidates += glob.glob("/usr/lib/qgis/qgis_process*")

    # Prefere a versao mais nova (por numero de versao real, nao lexicografico).
    for path in sorted(set(candidates), key=_version_key, reverse=True):
        if Path(path).exists():
            _qgis_process_path = path
            return path
    return None


def _build_command(qgis_process, args):
    """Monta o comando, tratando .bat/.cmd no Windows via cmd /c."""
    if os.name == "nt" and qgis_process.lower().endswith((".bat", ".cmd")):
        return ["cmd", "/c", qgis_process, *args]
    return [qgis_process, *args]


def _qgis4_config_path():
    """Diretorio de configuracao do QGIS 4 (que contem 'profiles'), se existir.

    O qgis_process 4.0 ainda resolve o perfil legado QGIS/QGIS3 por padrao,
    enquanto o QGIS 4 Desktop usa QGIS/QGIS4 — sem redirecionar via
    QGIS_CUSTOM_CONFIG_PATH, o plugin instalado no perfil real fica invisivel
    para o qgis_process (lista vazia / provider nao carregado).
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA", "")
        cand = os.path.join(base, "QGIS", "QGIS4")
    elif sys.platform == "darwin":
        cand = os.path.expanduser("~/Library/Application Support/QGIS/QGIS4")
    else:
        cand = os.path.expanduser("~/.local/share/QGIS/QGIS4")
    return cand if os.path.isdir(os.path.join(cand, "profiles")) else None


def call_qgis_process(args, stdin_text=None):
    """Executa o qgis_process e retorna (returncode, stdout, stderr)."""
    qgis_process = find_qgis_process()
    if qgis_process is None:
        raise SystemExit(
            "ERRO: nao encontrei o 'qgis_process'.\n"
            "  - Garanta que o QGIS 4.0+ esta instalado, ou\n"
            "  - Aponte a variavel de ambiente DSGTOOLS_QGIS_PROCESS para o\n"
            "    caminho do qgis_process (ex.: \"C:\\\\Program Files\\\\QGIS 4.0.0\\\\bin\\\\qgis_process-qgis.bat\").\n"
            "  Rode `dsgtools_cli.py doctor` para diagnosticar."
        )

    env = dict(os.environ)
    # Necessario para rodar sem servidor grafico (headless / servidores).
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    # Aponta o qgis_process para o perfil do QGIS 4 (ver _qgis4_config_path).
    if "QGIS_CUSTOM_CONFIG_PATH" not in env:
        cfg = _qgis4_config_path()
        if cfg:
            env["QGIS_CUSTOM_CONFIG_PATH"] = cfg

    proc = subprocess.run(
        _build_command(qgis_process, args),
        input=stdin_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _parse_json_stdout(stdout):
    """qgis_process imprime o JSON no stdout; o stderr leva ruido de outros plugins."""
    stdout = stdout.strip()
    if not stdout:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def full_id(alg):
    """Normaliza para 'dsgtools:nome'."""
    alg = alg.strip()
    return alg if ":" in alg else f"{PROVIDER}:{alg}"


def _help_json(alg):
    """Retorna (help_parseado, returncode) de `qgis_process help <id> --json`."""
    code, out, _err = call_qgis_process(["help", full_id(alg), "--json"])
    return _parse_json_stdout(out), code


def load_annotations():
    """Conhecimento de dominio opcional (regras/exemplos) por id de algoritmo."""
    if not ANNOTATIONS_PATH.exists():
        return {}
    with open(ANNOTATIONS_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _summarize_help(data):
    """Reduz a saida verbosa do `qgis_process help --json` a um resumo util."""
    details = data.get("algorithm_details", {})
    params = []
    for name, p in sorted(data.get("parameters", {}).items()):
        item = {
            "name": name,
            "type": p.get("raw_definition", {}).get("parameter_type", p.get("type", {}).get("id")),
            "description": p.get("description"),
            "required": not p.get("optional", False),
            "advanced": p.get("is_advanced", False),
            "is_output": p.get("is_destination", False),
            "default": p.get("default_value"),
        }
        if "available_options" in p:
            item["options"] = p["available_options"]
            item["note"] = "passe o indice numerico da opcao (ex.: 2)"
        params.append(item)
    outputs = [
        {"name": k, "type": v.get("type"), "description": v.get("description")}
        for k, v in data.get("outputs", {}).items()
    ]
    return {
        "id": details.get("id"),
        "display_name": details.get("name"),
        "group": details.get("group"),
        "parameters": params,
        "outputs": outputs,
    }


# ---------------------------------------------------------------------------
# Cache do contrato (help --json) em disco
#
# Uma chamada ao qgis_process custa segundos (o QGIS inteiro sobe a cada vez),
# entao validar o `run` contra o contrato ao vivo dobraria o custo de toda
# execucao. O contrato so muda quando o QGIS ou o plugin mudam, logo cabe em
# cache com uma impressao digital barata (stat, sem ler arquivo).
# ---------------------------------------------------------------------------
def _stat_token(path):
    """Assinatura barata de um caminho: mtime + tamanho, ou '-' se nao existir."""
    try:
        st = os.stat(path)
    except OSError:
        return "-"
    return f"{st.st_mtime_ns}.{st.st_size}"


def env_fingerprint():
    """Impressao digital do ambiente que produz o contrato.

    Cobre o executavel do qgis_process (troca de versao do QGIS) e a pasta do
    plugin com o metadata.txt (troca de versao/instalacao do DSGTools). NAO cobre
    a edicao de um .py de algoritmo la dentro, porque varrer a arvore a cada `run`
    custaria mais do que economiza: em desenvolvimento do plugin, use
    `--refresh-cache` ou `cache --clear` depois de mexer na assinatura de um
    algoritmo.
    """
    global _fingerprint
    if _fingerprint is not None:
        return _fingerprint
    qp = find_qgis_process() or "-"
    parts = [
        str(CACHE_FORMAT),
        qp,
        _stat_token(qp),
        str(PLUGIN_DIR),
        _stat_token(PLUGIN_DIR),
        _stat_token(PLUGIN_DIR / "metadata.txt"),
    ]
    _fingerprint = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return _fingerprint


def cache_dir():
    """Pasta do cache; DSGTOOLS_CLI_CACHE permite isolar (testes, CI, read-only tmp)."""
    override = os.environ.get("DSGTOOLS_CLI_CACHE")
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / "dsgtools_cli_cache"


def _cache_file(alg):
    # O id tem ':', que nao e nome de arquivo valido no Windows.
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", full_id(alg))
    return cache_dir() / f"{safe}.json"


def cache_read(alg):
    """Contrato em cache e ainda valido, ou None."""
    try:
        with open(_cache_file(alg), encoding="utf-8") as fh:
            entry = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None
    if entry.get("fingerprint") != env_fingerprint():
        return None
    return entry.get("help")


def cache_write(alg, data):
    """Grava o contrato. Falha de escrita nunca derruba o comando: o cache e
    otimizacao, e um /tmp somente-leitura nao pode impedir de rodar o algoritmo."""
    path = _cache_file(alg)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Escrita atomica: dois `run` simultaneos nao podem deixar um JSON pela metade.
        tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(
                {"fingerprint": env_fingerprint(), "algorithm": full_id(alg), "help": data},
                fh,
                ensure_ascii=False,
            )
        os.replace(tmp, path)
    except OSError:
        pass


def help_json_cached(alg, refresh=False):
    """Contrato do algoritmo. Retorna (help, returncode, veio_do_cache)."""
    if not refresh:
        cached = cache_read(alg)
        if cached is not None:
            return cached, 0, True
    data, code = _help_json(alg)
    if data is not None:
        cache_write(alg, data)
    return data, code, False


# ---------------------------------------------------------------------------
# Contrato: formatacao legivel e validacao local
# ---------------------------------------------------------------------------
def _param_type(param):
    return (
        param.get("raw_definition", {}).get("parameter_type")
        or param.get("type", {}).get("id")
        or "?"
    )


def _param_marks(param):
    marks = ["opcional" if param.get("optional", False) else "obrigatorio"]
    if param.get("is_destination"):
        marks.append("saida")
    if param.get("is_advanced"):
        marks.append("avancado")
    return ",".join(marks)


def _options_line(param):
    """'0=MI/MIR  1=INOM' para enum por indice, ou os rotulos aceitos quando o
    enum usa string estatica. None se o parametro nao for enumerado."""
    options = param.get("available_options")
    if not options:
        return None
    if param.get("raw_definition", {}).get("uses_static_strings"):
        return "valores: " + "  ".join(str(v) for v in options.values())
    pairs = "  ".join(f"{k}={v}" for k, v in sorted(options.items(), key=_option_sort_key))
    return f"opcoes (passe o indice): {pairs}"


def _option_sort_key(item):
    key = item[0]
    return (int(key), "") if str(key).lstrip("-").isdigit() else (0, str(key))


def format_param(name, param, indent="  "):
    """Uma linha por parametro (mais continuacoes para padrao e opcoes)."""
    head = f"{indent}{name:<26} {_param_type(param):<10} {_param_marks(param):<22}"
    desc = param.get("description") or ""
    lines = [f"{head} {desc}".rstrip()]
    default = param.get("default_value")
    if default is not None:
        lines.append(f"{indent}      padrao: {json.dumps(default, ensure_ascii=False)}")
    options = _options_line(param)
    if options:
        lines += textwrap.wrap(
            options,
            width=WIDTH,
            initial_indent=indent + "      ",
            subsequent_indent=indent + "              ",
        )
    return "\n".join(lines)


def _param_sort_key(item):
    """Obrigatorios de entrada primeiro, depois as saidas obrigatorias, depois os
    opcionais: e a ordem em que um chamador precisa decidir o que passar."""
    name, param = item
    return (bool(param.get("optional", False)), bool(param.get("is_destination")), name)


def _enum_indices(value):
    """Indices de um valor de enum ('1', 1, '1,3', [1, 3]) ou None se nao for indice."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return [value]
    if isinstance(value, (list, tuple)):
        items = value
    elif isinstance(value, str):
        items = value.split(",")
    else:
        return None
    out = []
    for item in items:
        text = str(item).strip()
        if not re.fullmatch(r"-?\d+", text):
            return None
        out.append(int(text))
    return out or None


def validate_inputs(inputs, help_data):
    """Confere os parametros contra o contrato do algoritmo, sem executar nada.

    Devolve uma lista de {"message", "params"}. So checa o que da para afirmar com
    certeza a partir do contrato; um enum de string estatica, por exemplo, fica de
    fora, porque reprovar por engano e pior do que deixar o qgis_process reclamar.
    """
    params = help_data.get("parameters", {})
    errors = []

    # 1. Nome que nao existe. E o modo de falha mais traicoeiro: o qgis_process
    # IGNORA a chave desconhecida em silencio, aplica o padrao do parametro que o
    # chamador queria setar e o erro so aparece la na frente, com outra cara.
    for key in inputs:
        if key in params:
            continue
        close = difflib.get_close_matches(key, list(params), n=2, cutoff=0.6)
        message = f"parametro inexistente: {key}"
        if close:
            message += f" (talvez: {', '.join(close)})"
        errors.append({"message": message, "params": close})

    # 2. Obrigatorio ausente. Vale tambem para saidas (sink/fileDestination): o
    # qgis_process nao inventa destino temporario, ele aborta.
    for name, param in sorted(params.items(), key=_param_sort_key):
        if param.get("optional", False):
            continue
        if name not in inputs or inputs[name] is None:
            errors.append({"message": f"parametro obrigatorio ausente: {name}", "params": [name]})

    # 3. Enum por indice: fora da faixa, ou rotulo passado no lugar do indice.
    for name, value in inputs.items():
        param = params.get(name)
        if not param:
            continue
        options = param.get("available_options")
        if not options or param.get("raw_definition", {}).get("uses_static_strings"):
            continue
        valid = {int(k) for k in options if str(k).lstrip("-").isdigit()}
        indices = _enum_indices(value)
        if indices is None:
            label = {str(v).lower(): k for k, v in options.items()}.get(str(value).lower())
            message = f"{name}: valor {value!r} nao e indice de opcao"
            if label is not None:
                message += f" (o indice de {value!r} e {label})"
            errors.append({"message": message, "params": [name]})
            continue
        fora = [i for i in indices if i not in valid]
        if fora:
            errors.append(
                {
                    "message": f"{name}: indice {', '.join(map(str, fora))} fora da faixa",
                    "params": [name],
                }
            )
    return errors


def format_validation_errors(alg, errors, help_data):
    """Mensagem de reprovacao: o contrato dos parametros citados vem JUNTO, para
    o chamador poder corrigir sem uma segunda chamada (que custaria segundos)."""
    params = help_data.get("parameters", {})
    out = [f"ERRO: {len(errors)} problema(s) de validacao em {alg} (nada foi executado).", ""]
    for n, err in enumerate(errors, 1):
        out.append(f"  [{n}] {err['message']}")
        for name in err.get("params") or []:
            if name in params:
                out.append(format_param(name, params[name], indent="      "))
    known = ", ".join(sorted(params))
    out.append("")
    out += textwrap.wrap(
        f"Parametros de {alg}: {known}",
        width=WIDTH,
        initial_indent="  ",
        subsequent_indent="    ",
    )
    out.append(f"  Contrato completo: describe {alg}")
    out.append("  Para pular esta checagem: --no-check")
    return "\n".join(out) + "\n"


def render_describe(help_data, annotation):
    """Saida compacta do describe: uma linha por parametro, mais o que so a prosa
    curada sabe (regra de dominio e exemplo)."""
    details = help_data.get("algorithm_details", {})
    params = help_data.get("parameters", {})
    alg = details.get("id") or "?"
    out = [f"{alg}  |  {details.get('name', '')}  |  grupo: {details.get('group', '')}"]

    if annotation.get("description"):
        out += ["", textwrap.fill(annotation["description"], width=WIDTH)]

    required = sum(1 for p in params.values() if not p.get("optional", False))
    out += ["", f"Parametros ({required} obrigatorio(s), {len(params) - required} opcional(is)):"]
    for name, param in sorted(params.items(), key=_param_sort_key):
        out.append(format_param(name, param))

    # So as saidas que NAO sao parametro (a saida-destino ja saiu acima, marcada
    # como 'saida'; repeti-la aqui seria dizer duas vezes a mesma coisa).
    extras = {k: v for k, v in help_data.get("outputs", {}).items() if k not in params}
    if extras:
        out += ["", "Saidas adicionais (nao sao parametro):"]
        for name, info in sorted(extras.items()):
            out.append(f"  {name:<26} {info.get('type', ''):<16} {info.get('description', '')}".rstrip())

    rules = annotation.get("constraints") or []
    if rules:
        out += ["", "Regras (curadas):"]
        for rule in rules:
            out += textwrap.wrap(rule, width=WIDTH, initial_indent="  - ", subsequent_indent="    ")

    example = annotation.get("example")
    if example:
        out += ["", "Exemplo:", f"  python dsgtools_cli.py run {alg} {_example_args(example)}"]
    return "\n".join(out)


def _example_args(example):
    """Transforma o exemplo curado ({'KEY': valor}) em tokens KEY=VALUE prontos."""
    tokens = []
    for key, value in example.items():
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        tokens.append(f'"{key}={text}"' if " " in text else f"{key}={text}")
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------
def _quote(path):
    return f'"{path}"' if " " in str(path) else str(path)


def _print_enable_fix(qp):
    """Imprime o conserto do plugin desabilitado.

    O comando so vale se rodar no MESMO perfil que este CLI usa: o qgis_process
    resolve o perfil legado (QGIS3) por padrao, enquanto o CLI redireciona para o
    perfil do QGIS 4. Rodar o enable sem essa variavel habilita o plugin no perfil
    errado e o CLI continua sem provider, sem sinal nenhum de que nada mudou.
    """
    cfg = os.environ.get("QGIS_CUSTOM_CONFIG_PATH") or _qgis4_config_path()
    print(f"    conserto: {_quote(qp)} plugins enable DsgTools")
    if cfg:
        setter = f'set QGIS_CUSTOM_CONFIG_PATH={cfg}' if os.name == "nt" \
            else f'export QGIS_CUSTOM_CONFIG_PATH="{cfg}"'
        print(f"              (antes, no mesmo terminal: {setter})")
    print("    ou, ja no perfil certo: python dsgtools_cli.py doctor --fix")


def _check_provider(qp, fix=False):
    """Confere se o provider dsgtools esta carregado NO qgis_process e, quando nao
    esta, devolve o conserto exato.

    Este e o modo de falha real: o qgis_process mantem a propria lista de plugins
    habilitados, separada da do QGIS Desktop. Com o plugin ativo no Desktop e
    inativo aqui, `list` retorna zero algoritmos com exit 0 e stderr vazio, ou
    seja, o CLI fica inutil sem reclamar de nada.
    """
    problems = []
    code, out, err = call_qgis_process(["plugins", "--json"])
    plugins = (_parse_json_stdout(out) or {}).get("plugins")
    if plugins is None:
        print(f"  plugins         : nao consegui ler (exit {code})")
        if err.strip():
            print(f"    stderr: {err.strip().splitlines()[0]}")
        problems.append("nao foi possivel consultar os plugins do qgis_process")
        return problems
    entry = plugins.get("DsgTools")
    if entry is None:
        print(f"  plugin DsgTools : NAO INSTALADO no perfil visto pelo qgis_process")
        print(f"    plugins vistos: {', '.join(sorted(plugins)) or '(nenhum)'}")
        print(f"    conserto: instale/aponte o plugin no perfil (ver QGIS_CUSTOM_CONFIG_PATH acima);")
        print(f"              em desenvolvimento, um link de {PLUGIN_DIR} para <perfil>/python/plugins.")
        problems.append("plugin DsgTools ausente")
        return problems
    if not entry.get("loaded"):
        print("  plugin DsgTools : instalado, mas NAO habilitado para o qgis_process")
        print("    (o qgis_process tem lista de plugins propria, independente do QGIS Desktop)")
        _print_enable_fix(qp)
        if not fix:
            problems.append("plugin DsgTools nao habilitado no qgis_process")
            return problems
        print("    --fix: habilitando agora...")
        code, _out, err = call_qgis_process(["plugins", "enable", "DsgTools"])
        if code != 0:
            print(f"    falhou (exit {code}): {err.strip().splitlines()[:1]}")
            problems.append("nao consegui habilitar o plugin")
            return problems
        print("    habilitado.")
    else:
        print("  plugin DsgTools : habilitado e carregado")

    code, out, err = call_qgis_process(["list", "--json"])
    algs = (_parse_json_stdout(out) or {}).get("providers", {}).get(PROVIDER, {}).get("algorithms", {})
    if not algs:
        print(f"  provider {PROVIDER}: CARREGOU 0 ALGORITMOS (exit {code})")
        print("    o plugin subiu mas nao registrou o provider: quase sempre um erro de import.")
        print(f"    conserto: rode {_quote(qp)} list e leia o stderr, que traz o traceback.")
        if err.strip():
            print(f"    stderr (1a linha): {err.strip().splitlines()[0]}")
        problems.append("provider carregou 0 algoritmos")
    else:
        print(f"  provider {PROVIDER}: {len(algs)} algoritmos")
    return problems


def cmd_doctor(args):
    qp = find_qgis_process()
    print("dsgtools-cli doctor")
    print("-------------------")
    print(f"  qgis_process    : {qp or 'NAO ENCONTRADO'}")
    print(f"  annotations.json: {'ok' if ANNOTATIONS_PATH.exists() else 'ausente (opcional)'}")
    print(f"  QT_QPA_PLATFORM (sera definido como) : "
          f"{os.environ.get('QT_QPA_PLATFORM', 'offscreen')}")
    cfg = os.environ.get("QGIS_CUSTOM_CONFIG_PATH") or _qgis4_config_path()
    print(f"  QGIS_CUSTOM_CONFIG_PATH (sera definido como) : {cfg or '(padrao do qgis_process)'}")
    if qp is None:
        print("\n  Defina DSGTOOLS_QGIS_PROCESS apontando para o qgis_process.")
        return 1
    code, out, err = call_qgis_process(["--version"])
    first = (out or err).strip().splitlines()
    print(f"  versao          : {first[0] if first else '??'} (exit {code})")
    print(f"  cache do contrato: {cache_dir()} ({_cache_counts()[0]} entrada(s) validas)")

    problems = _check_provider(qp, fix=args.fix)
    if problems:
        print("\n  RESULTADO: o CLI NAO vai funcionar. " + "; ".join(problems) + ".")
        return 1
    print("\n  RESULTADO: ambiente ok.")
    return 0


def _cache_counts():
    """(validas, obsoletas) no cache, sem falhar se a pasta nem existir."""
    valid = stale = 0
    try:
        files = sorted(cache_dir().glob("*.json"))
    except OSError:
        return 0, 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                entry = json.load(fh)
        except (OSError, json.JSONDecodeError):
            stale += 1
            continue
        if entry.get("fingerprint") == env_fingerprint():
            valid += 1
        else:
            stale += 1
    return valid, stale


def cmd_cache(args):
    directory = cache_dir()
    if args.clear:
        removed = 0
        for path in directory.glob("*.json"):
            try:
                path.unlink()
                removed += 1
            except OSError:
                pass
        print(f"Cache limpo: {removed} entrada(s) removida(s) de {directory}")
        return 0
    valid, stale = _cache_counts()
    print(f"Cache do contrato (help --json) dos algoritmos")
    print(f"  pasta           : {directory}")
    print(f"  existe          : {'sim' if directory.is_dir() else 'nao (sera criada no 1o uso)'}")
    print(f"  impressao digital: {env_fingerprint()}")
    print(f"  entradas        : {valid} validas, {stale} obsoletas")
    print("\nLimpar: cache --clear   |   Atualizar um algoritmo: describe <alg> --refresh-cache")
    return 0


def cmd_list(args):
    code, out, _err = call_qgis_process(["list", "--json"])
    data = _parse_json_stdout(out)
    if data is None:
        raise SystemExit(f"Falha ao listar (exit {code}).")
    algs = data.get("providers", {}).get(PROVIDER, {}).get("algorithms", {})
    rows = sorted(algs.items())
    if args.json:
        print(json.dumps({"algorithms": [k for k, _ in rows]}, indent=2, ensure_ascii=False))
        return 0
    if not rows:
        # Zero algoritmos com exit 0 e o sintoma de provider nao carregado, nao de
        # um plugin sem algoritmos: aponta o diagnostico em vez de calar.
        print("Nenhum algoritmo do DSGTools disponivel (o provider nao carregou).")
        print("Rode `dsgtools_cli.py doctor` para ver o conserto exato.")
        return 1
    print(f"Algoritmos do DSGTools — {len(rows)} disponiveis:\n")
    for alg_id, info in rows:
        print(f"  {alg_id:<55} {info.get('name', '')}")
    print("\nUse `describe <id>` para ver os parametros, ou `run <id> KEY=VALUE ...` para executar.")
    return 0


def cmd_describe(args):
    data, code, _cached = help_json_cached(args.algorithm, refresh=args.refresh_cache)
    if data is None:
        raise SystemExit(f"Falha ao descrever {args.algorithm} (exit {code}).")
    annotation = load_annotations().get(data.get("algorithm_details", {}).get("id"), {})
    if not args.json:
        print(render_describe(data, annotation))
        return 0
    summary = _summarize_help(data)
    # Enriquece com o conhecimento de dominio curado, se houver para este id.
    for key in ("description", "constraints", "example"):
        if key in annotation:
            summary[key] = annotation[key]
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


_INT_RE = re.compile(r"^-?[1-9][0-9]*$|^0$")
_FLOAT_RE = re.compile(r"^-?[0-9]+\.[0-9]+$")


def _coerce(value):
    """Converte tokens 'KEY=VALUE' em numero apenas quando e seguro; senao, string.

    So coage inteiros "limpos" (sem zero a esquerda, sem '_', sem 'inf'/'nan', sem
    notacao exponencial ou hex) e floats decimais simples — assim nao corrompe
    strings numericas como '007', '1_000', 'inf' ou identificadores. Para forcar
    um valor numerico a permanecer string, use --params/--stdin (o JSON preserva os tipos).
    """
    if _INT_RE.match(value):
        return int(value)
    if _FLOAT_RE.match(value):
        return float(value)
    return value


def _unwrap_inputs(data):
    """Aceita {"inputs": {...}} ou {...} diretamente; exige um objeto JSON (dict)."""
    if not isinstance(data, dict):
        raise SystemExit("JSON de parametros invalido: esperado um objeto JSON.")
    if "inputs" in data:
        inner = data["inputs"]
        if not isinstance(inner, dict):
            raise SystemExit('JSON de parametros invalido: a chave "inputs" deve ser um objeto.')
        return inner
    return data


def _load_json_file(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise SystemExit(f"Arquivo de parametros nao encontrado: {path}")
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Falha ao ler JSON de '{path}': {exc}")


def _collect_inputs(args):
    inputs = {}
    if args.params:
        inputs.update(_unwrap_inputs(_load_json_file(args.params)))
    if args.stdin:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Falha ao ler JSON do stdin: {exc}")
        inputs.update(_unwrap_inputs(data))
    for token in args.params_kv:
        if "=" not in token:
            raise SystemExit(f"Parametro invalido '{token}'. Use KEY=VALUE.")
        key, value = token.split("=", 1)
        inputs[key.strip()] = _coerce(value)
    return inputs


def render_dry_run(alg, inputs, help_data):
    """Mostra exatamente o que seria executado, sem executar."""
    payload = json.dumps({"inputs": inputs}, ensure_ascii=False)
    out = [
        f"[dry-run] {alg} (nada foi executado)",
        f"  comando : qgis_process run {alg} -   (parametros pelo stdin)",
        f"  binario : {find_qgis_process() or 'NAO ENCONTRADO'}",
        "  stdin   : " + payload,
        "",
        f"  Parametros ({len(inputs)}):",
    ]
    params = (help_data or {}).get("parameters", {})
    for key in sorted(inputs):
        value = json.dumps(inputs[key], ensure_ascii=False)
        rotulo = ""
        param = params.get(key)
        if param and param.get("available_options"):
            # Traduz o indice de volta ao rotulo: e a checagem que o chamador
            # nao tem como fazer de cabeca, e o erro silencioso mais comum.
            rotulo = param["available_options"].get(str(inputs[key]), "")
            rotulo = f"   -> {rotulo}" if rotulo else ""
        out.append(f"    {key:<26} = {value}{rotulo}")
    if params:
        omitidos = [n for n, p in params.items() if n not in inputs]
        if omitidos:
            out.append(f"  Omitidos (opcionais): {', '.join(sorted(omitidos))}")
        out.append("  Validacao: ok")
    else:
        out.append("  Validacao: NAO conferida (sem contrato disponivel)")
    return "\n".join(out)


def cmd_run(args):
    inputs = _collect_inputs(args)
    alg = full_id(args.algorithm)

    # Valida ANTES de gastar a execucao. O contrato sai do cache em disco, entao o
    # custo tipico e de milissegundos, nao de uma segunda subida do QGIS.
    help_data = None
    if not args.no_check:
        help_data, code, _cached = help_json_cached(alg, refresh=args.refresh_cache)
        if help_data is None:
            # Sem contrato nao da para validar. Abortar aqui esconderia o erro real
            # do qgis_process, entao avisa e segue: a validacao e rede, nao portao.
            print(
                f"AVISO: nao consegui obter o contrato de {alg} (exit {code}); "
                "seguindo sem validar. Se repetir, rode `dsgtools_cli.py doctor`.",
                file=sys.stderr,
            )
        else:
            errors = validate_inputs(inputs, help_data)
            if errors:
                sys.stderr.write(format_validation_errors(alg, errors, help_data))
                return 2

    if args.dry_run:
        print(render_dry_run(alg, inputs, help_data))
        return 0

    payload = json.dumps({"inputs": inputs})
    code, out, err = call_qgis_process(["run", alg, "-"], stdin_text=payload)
    data = _parse_json_stdout(out)

    if args.raw or data is None:
        if out:
            print(out)
        if err.strip():
            sys.stderr.write(err)
        return code

    # O returncode do qgis_process e a fonte da verdade de sucesso/falha.
    results = data.get("results")
    if results is not None:
        print(json.dumps({"results": results, "inputs": inputs}, indent=2, ensure_ascii=False))
        if code == 0:
            for key, value in results.items():
                print(f"\n[OK] {key} -> {value}", file=sys.stderr)
    else:
        # Sucesso sem 'results' (ex.: algoritmos de efeito colateral) tambem e valido.
        print(json.dumps(data, indent=2, ensure_ascii=False))
    if err.strip():
        sys.stderr.write(err)
    return code


def build_parser():
    parser = argparse.ArgumentParser(
        prog="dsgtools_cli.py",
        description="Executa algoritmos de Processing do DSGTools por linha de comando (headless).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="Lista os algoritmos disponiveis.")
    p_list.add_argument("--json", action="store_true", help="Saida em JSON.")
    p_list.set_defaults(func=cmd_list)

    p_desc = sub.add_parser("describe", help="Mostra os parametros de um algoritmo.")
    p_desc.add_argument("algorithm", help="Id do algoritmo (com ou sem 'dsgtools:').")
    p_desc.add_argument("--json", action="store_true", help="Saida em JSON (para encadear).")
    p_desc.add_argument("--refresh-cache", action="store_true",
                        help="Rele o contrato ao vivo, ignorando o cache.")
    p_desc.set_defaults(func=cmd_describe)

    p_run = sub.add_parser("run", help="Valida e executa um algoritmo.")
    p_run.add_argument("algorithm", help="Id do algoritmo (com ou sem 'dsgtools:').")
    p_run.add_argument("params_kv", nargs="*", metavar="KEY=VALUE", help="Parametros de entrada.")
    p_run.add_argument("--params", metavar="FILE", help="Arquivo JSON com os parametros.")
    p_run.add_argument("--stdin", action="store_true", help="Le os parametros (JSON) do stdin.")
    p_run.add_argument("--raw", action="store_true", help="Imprime o JSON cru do qgis_process.")
    p_run.add_argument("--dry-run", action="store_true",
                       help="Valida e mostra o que seria executado, sem executar.")
    p_run.add_argument("--no-check", action="store_true",
                       help="Pula a validacao local dos parametros.")
    p_run.add_argument("--refresh-cache", action="store_true",
                       help="Rele o contrato ao vivo antes de validar.")
    p_run.set_defaults(func=cmd_run)

    p_doc = sub.add_parser("doctor", help="Diagnostica o ambiente.")
    p_doc.add_argument("--fix", action="store_true",
                       help="Habilita o plugin no qgis_process quando for esse o problema.")
    p_doc.set_defaults(func=cmd_doctor)

    p_cache = sub.add_parser("cache", help="Mostra ou limpa o cache do contrato.")
    p_cache.add_argument("--clear", action="store_true", help="Apaga as entradas do cache.")
    p_cache.set_defaults(func=cmd_cache)

    return parser


def main(argv=None):
    # Garante saída UTF-8 (descrições/constraints podem ter acentos) independentemente
    # da codificação padrão do console/plataforma.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
