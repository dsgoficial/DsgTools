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
| `describe <id> [--json]` | Mostra os parâmetros do algoritmo, compacto (uma linha por parâmetro) + anotações. |
| `run <id> [KEY=VALUE ...]` | **Valida** e executa o algoritmo. Também aceita `--params arq.json` e `--stdin`. |
| `doctor [--fix]` | Diagnostica o ambiente (`qgis_process`, versão, **provider carregado**). |
| `cache [--clear]` | Mostra ou limpa o cache local do contrato dos algoritmos. |

O id pode ser passado **com ou sem** o prefixo `dsgtools:`.

Códigos de saída: `0` sucesso, `2` reprovado na validação local (nada foi executado),
qualquer outro é o código do próprio `qgis_process`.

> No `run`, as opções (`--dry-run`, `--no-check`, `--params`, ...) vão **depois** dos
> tokens `KEY=VALUE`. Limitação do `argparse` com positional de tamanho variável: uma
> opção no meio faz o resto virar "unrecognized arguments".

---

## Validação antes de executar

O `run` confere os parâmetros contra o contrato do próprio algoritmo **antes** de
executar, e quando reprova imprime o contrato dos parâmetros citados (não um ponteiro
para documentação):

- **nome de parâmetro que não existe**: o `qgis_process` *ignora em silêncio* a chave
  desconhecida, aplica o padrão do parâmetro que você queria setar, e o erro só aparece
  lá na frente disfarçado de erro de domínio. Este é o modo de falha que mais custa tempo;
- **parâmetro obrigatório ausente** (inclusive as saídas: o `qgis_process` não inventa
  destino temporário, ele aborta);
- **índice de enum fora da faixa**, ou o rótulo passado no lugar do índice
  (`START_SCALE=250k` responde "o índice de '250k' é 2").

```bash
# valida e mostra o que seria executado, sem executar
python dsgtools_cli.py run dsgtools:gridzonegenerator ... --dry-run

# escapes
python dsgtools_cli.py run <id> ... --no-check        # pula a validação
python dsgtools_cli.py run <id> ... --refresh-cache   # relê o contrato ao vivo
```

### Por que existe o cache (e quando limpá-lo)

Cada consulta ao `qgis_process` sobe o QGIS inteiro e custa **segundos**. Validar
buscando o contrato ao vivo dobraria o custo de todo `run`. Por isso o contrato
(`help --json`) fica em cache em disco, em `%TEMP%/dsgtools_cli_cache` (ou o que estiver
em `DSGTOOLS_CLI_CACHE`), invalidado por uma impressão digital barata do ambiente:
mtime/tamanho do executável do `qgis_process` e da pasta do plugin com o `metadata.txt`.

Medido nesta máquina (QGIS 4.0.0, Windows 11):

| | tempo |
|---|---|
| `run` sem validar (`--no-check`) | 3,08 s |
| `run` validado, cache frio | 5,66 s |
| `run` validado, cache quente | 2,99 s |
| `describe` cache frio / cache quente | 2,89 s / 0,12 s |

Ou seja: a validação ingênua custaria **+84%** em cada execução; com o cache o custo
fica dentro do ruído (**< 1%**).

A impressão digital **não** cobre a edição de um `.py` de algoritmo lá dentro (varrer a
árvore a cada `run` custaria mais do que economiza). Em desenvolvimento do plugin,
depois de mexer na assinatura de um algoritmo:

```bash
python dsgtools_cli.py cache --clear          # limpa tudo
python dsgtools_cli.py describe <id> --refresh-cache   # atualiza um
```

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

Na dúvida, comece pelo `doctor`: ele não se limita a achar o `qgis_process`, confere se o
provider `dsgtools` está **de fato carregado** e imprime o conserto exato.

- **`list` diz "Nenhum algoritmo do DSGTools disponível"** (antes: "0 disponíveis", sem
  erro nenhum e com stderr vazio) → o `qgis_process` mantém a **própria lista de plugins
  habilitados**, separada da do QGIS Desktop. Com o plugin ativo no Desktop e inativo
  aqui, o CLI fica inútil sem reclamar de nada. Conserto:

  ```bash
  python dsgtools_cli.py doctor --fix      # habilita no mesmo perfil que o CLI usa
  # equivalente na mão (precisa do MESMO perfil, veja abaixo):
  qgis_process plugins enable DsgTools
  qgis_process plugins                     # confere: '*' = provider carregado
  ```

  **Atenção ao perfil:** o `qgis_process` resolve o perfil legado (`QGIS/QGIS3`) por
  padrão, enquanto o CLI redireciona para o do QGIS 4 (`QGIS_CUSTOM_CONFIG_PATH`, veja
  "Como funciona por baixo"). Rodar o `enable` num terminal sem essa variável habilita o
  plugin **no perfil errado** e o CLI continua sem provider, sem sinal de que nada mudou.
  O `doctor --fix` usa o perfil certo por construção.
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
