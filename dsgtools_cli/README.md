# DSGTools — execução de Processings por linha de comando (headless)

Esta pasta permite **rodar algoritmos de Processing do DSGTools fora do QGIS**, por
linha de comando, de forma headless — para uso manual ou em automações/scripts.

Tudo é construído sobre o utilitário **oficial `qgis_process`** que vem com o QGIS.
O `dsgtools_cli.py` é uma camada fina que: localiza o `qgis_process`, configura o
ambiente headless, e descobre/executa os algoritmos **consultando o `qgis_process` ao
vivo**. Não há catálogo pré-gerado: a lista e os parâmetros vêm sempre da fonte da
verdade, então estão sempre corretos e escalam para as centenas de algoritmos do
plugin sem manutenção manual.

---

## Onde está a lista de algoritmos e como rodar

```
python dsgtools_cli.py list                              # todos os algoritmos
python dsgtools_cli.py describe dsgtools:gridzonegenerator   # parâmetros de um
python dsgtools_cli.py run dsgtools:gridzonegenerator ...    # executar
```

- **O CLI:** [`dsgtools_cli.py`](dsgtools_cli.py)
- **Conhecimento de domínio curado** (regras, exemplos), opcional: [`annotations.json`](annotations.json)
  — enriquece a saída de `describe` para algoritmos específicos.

---

## Requisitos

- **QGIS 4.0+** instalado (traz o `qgis_process`).
- **Python 3** (qualquer um; o CLI usa só a biblioteca padrão).
- O plugin **DSGTools instalado/habilitado** no perfil do QGIS
  (em desenvolvimento, normalmente um symlink do repo para a pasta de plugins do perfil).

O CLI acha o `qgis_process` sozinho no Windows/Linux/macOS. Se não achar, aponte a
variável de ambiente:

```
# Windows
set DSGTOOLS_QGIS_PROCESS=C:\Program Files\QGIS 4.0.0\bin\qgis_process-qgis.bat
# Linux/macOS
export DSGTOOLS_QGIS_PROCESS=/usr/bin/qgis_process
```

Verifique o ambiente a qualquer momento:

```
python dsgtools_cli.py doctor
```

---

## Comandos

| Comando | O que faz |
|---|---|
| `list [--json]` | Lista os algoritmos do DSGTools (consulta o `qgis_process`). |
| `describe <id>` | Mostra os parâmetros do algoritmo (resumo do `qgis_process` + anotações). |
| `run <id> [KEY=VALUE ...]` | Executa o algoritmo. Também aceita `--params arq.json` e `--stdin`. |
| `doctor` | Diagnostica o ambiente (acha o `qgis_process`, versão). |

O id pode ser passado **com ou sem** o prefixo `dsgtools:`.

---

## Passando parâmetros

Três formas equivalentes (use a que preferir):

```bash
# a) tokens KEY=VALUE
python dsgtools_cli.py run dsgtools:gridzonegenerator START_SCALE=2 STOP_SCALE=4 \
    INDEX_TYPE=1 INDEX=SF-22-Y-D CRS=EPSG:31982 OUTPUT=grid.gpkg

# b) arquivo JSON
python dsgtools_cli.py run dsgtools:gridzonegenerator --params params.json

# c) JSON via stdin (pipe)
type params.json | python dsgtools_cli.py run dsgtools:gridzonegenerator --stdin
```

Formato do `params.json`:

```json
{ "inputs": { "START_SCALE": 2, "STOP_SCALE": 4, "INDEX_TYPE": 1,
              "INDEX": "SF-22-Y-D", "CRS": "EPSG:31982", "OUTPUT": "grid.gpkg" } }
```

**Regras importantes de tipos:**
- **Enum** (ex.: `START_SCALE`, `STOP_SCALE`, `INDEX_TYPE`): passe o **índice numérico**
  da opção. Veja o mapa índice→rótulo no `describe`. Ex.: `STOP_SCALE=4` = `50k`.
- **Número**: numérico. **String/CRS**: texto (ex.: `CRS=EPSG:31982`).
- Em `KEY=VALUE`, valores que parecem número viram número automaticamente; o resto vira string.

---

## Os dois algoritmos de grade (validados)

### `dsgtools:gridzonegenerator` — Generate Systematic Grid
Gera a moldura sistemática a partir de um índice (MI/MIR ou INOM).

```bash
python dsgtools_cli.py run dsgtools:gridzonegenerator \
    START_SCALE=2 STOP_SCALE=4 INDEX_TYPE=1 INDEX=SF-22-Y-D \
    CRS=EPSG:31982 OUTPUT=grid_50k.gpkg
```
- `START_SCALE` = escala do índice informado; `STOP_SCALE` = escala desejada (mais detalhada).
- `INDEX_TYPE=0` (MI/MIR) só vale para 250k e abaixo; para 1000k/500k use `INDEX_TYPE=1` (INOM).
- `INDEX` aceita múltiplos separados por vírgula.

### `dsgtools:createframeswithconstraintalgorithm` — Generate Systematic Grid Related to Layer
Gera a moldura que recobre/intersecta uma camada (vetor ou raster).

```bash
python dsgtools_cli.py run dsgtools:createframeswithconstraintalgorithm \
    INPUT=area.gpkg STOP_SCALE=3 OUTPUT=frames_100k.gpkg
```
- O CRS da saída é herdado da camada de entrada.

---

## Como funciona por baixo

1. O plugin DSGTools declara `hasProcessingProvider=yes` no `metadata.txt`, então o
   `qgis_process` o reconhece.
2. O plugin expõe `initProcessing()` e seu `__init__`/`unload` são seguros quando
   `iface is None` — necessário porque, em headless, o QGIS instancia o plugin **sem GUI**
   e chama `initProcessing()` (nunca `initGui()`).
3. O CLI define `QT_QPA_PLATFORM=offscreen` e usa o `qgis_process`:
   `list --json` / `help <id> --json` para descobrir e `run dsgtools:<id> -` enviando
   `{"inputs": {...}}` via stdin para executar.

---

## Solução de problemas

- **"não encontrei o qgis_process"** → defina `DSGTOOLS_QGIS_PROCESS` (veja Requisitos) e rode `doctor`.
- **Tracebacks de outro plugin no stderr** (ex.: `latlontools` → `Qt has no attribute Unchecked`):
  é um bug *daquele* plugin, não do DSGTools. O `qgis_process` continua e o JSON do DSGTools sai
  limpo no **stdout** (o CLI lê só o stdout). Para silenciar, desabilite o plugin problemático:
  `qgis_process plugins disable latlontools`.
- **Aviso `MULTIPOLYGON inserted into layer of type POLYGON`** → benigno; as molduras são geradas.
- **Servidor sem display (Linux headless)** → o CLI já define `QT_QPA_PLATFORM=offscreen`.

---

## Adicionar mais algoritmos

Nada a fazer no código: **todos** os algoritmos do provider `dsgtools:` já aparecem em
`list`, têm parâmetros em `describe` e rodam via `run`. Só verifique que o algoritmo
roda headless (sem GUI / sem tipos de parâmetro customizados que exijam interface).

Opcionalmente, para enriquecer um algoritmo com regras de negócio e um exemplo no
`describe`, adicione um bloco em [`annotations.json`](annotations.json) usando o id do
algoritmo como chave (`description`, `constraints`, `example`).
