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
  run <alg> [KEY=VALUE ...] Executa um algoritmo.
  doctor                    Diagnostica o ambiente (acha o qgis_process, etc).

Exemplos
--------
  python dsgtools_cli.py list
  python dsgtools_cli.py describe dsgtools:gridzonegenerator
  python dsgtools_cli.py run dsgtools:gridzonegenerator \\
      START_SCALE=2 STOP_SCALE=4 INDEX_TYPE=1 INDEX=SF-22-Y-D \\
      CRS=EPSG:31982 OUTPUT=grid.gpkg
  python dsgtools_cli.py run dsgtools:createframeswithconstraintalgorithm \\
      INPUT=area.gpkg STOP_SCALE=3 OUTPUT=frames.gpkg

O id do algoritmo pode ser passado com ou sem o prefixo "dsgtools:".
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROVIDER = "dsgtools"
HERE = Path(__file__).resolve().parent
ANNOTATIONS_PATH = HERE / "annotations.json"

_qgis_process_path = None  # cache (apenas resultados positivos)


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
# Comandos
# ---------------------------------------------------------------------------
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
    print(f"Algoritmos do DSGTools — {len(rows)} disponiveis:\n")
    for alg_id, info in rows:
        print(f"  {alg_id:<55} {info.get('name', '')}")
    print("\nUse `describe <id>` para ver os parametros, ou `run <id> KEY=VALUE ...` para executar.")
    return 0


def cmd_describe(args):
    data, code = _help_json(args.algorithm)
    if data is None:
        raise SystemExit(f"Falha ao descrever {args.algorithm} (exit {code}).")
    summary = _summarize_help(data)
    # Enriquece com o conhecimento de dominio curado, se houver para este id.
    extra = load_annotations().get(summary["id"], {})
    for key in ("description", "constraints", "example"):
        if key in extra:
            summary[key] = extra[key]
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


def cmd_run(args):
    inputs = _collect_inputs(args)
    payload = json.dumps({"inputs": inputs})
    code, out, err = call_qgis_process(["run", full_id(args.algorithm), "-"], stdin_text=payload)
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
    p_desc.set_defaults(func=cmd_describe)

    p_run = sub.add_parser("run", help="Executa um algoritmo.")
    p_run.add_argument("algorithm", help="Id do algoritmo (com ou sem 'dsgtools:').")
    p_run.add_argument("params_kv", nargs="*", metavar="KEY=VALUE", help="Parametros de entrada.")
    p_run.add_argument("--params", metavar="FILE", help="Arquivo JSON com os parametros.")
    p_run.add_argument("--stdin", action="store_true", help="Le os parametros (JSON) do stdin.")
    p_run.add_argument("--raw", action="store_true", help="Imprime o JSON cru do qgis_process.")
    p_run.set_defaults(func=cmd_run)

    p_doc = sub.add_parser("doctor", help="Diagnostica o ambiente.")
    p_doc.set_defaults(func=cmd_doctor)

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
