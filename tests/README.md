# Testes do DSGTools

Há dois conjuntos, com finalidades e formas de execução diferentes.

## 1. Testes que rodam dentro do QGIS (esta pasta)

Precisam do PyQGIS, então o interpretador tem que ser o do QGIS. Use o
`run_local.py`, que inicializa o QGIS e o Processing, registra o provider do
DSGTools e devolve código de saída (`0` passou, `1` falhou):

```powershell
# Windows
& 'C:\Program Files\QGIS 4.0.0\bin\python-qgis.bat' tests/run_local.py tests.test_terrainHandler
```

```bash
# Linux/macOS
python3 tests/run_local.py tests.test_terrainHandler
```

Um segundo argumento filtra por trecho do nome do teste:

```powershell
& 'C:\Program Files\QGIS 4.0.0\bin\python-qgis.bat' tests/run_local.py tests.test_terrainHandler depression
```

O `run_local.py` descobre os testes com o `TestLoader` padrão, e não pela função
`run_all()` de cada módulo. Isso é proposital: `run_all()` descarta o resultado do
runner, então não há como saber se passou, e ele depende de `unittest.makeSuite`,
removido no Python 3.13 (que é o que o QGIS 4 traz em algumas plataformas).

## 2. Testes de execução por linha de comando (`dsgtools_cli/tests`)

Executam os algoritmos de verdade, headless, via `qgis_process`. Rodam no python
**do sistema** (só usam stdlib + subprocess) e são pulados se o `qgis_process` não
for encontrado:

```bash
pip install pytest
python -m pytest dsgtools_cli/tests -v
```

Veja [`dsgtools_cli/tests/README.md`](../dsgtools_cli/tests/README.md).

## Qual usar para o quê

| | dentro do QGIS (`run_local.py`) | por linha de comando (`dsgtools_cli/tests`) |
|---|---|---|
| Alvo | funções e classes isoladas | o algoritmo inteiro, de ponta a ponta |
| Velocidade | milissegundos | ~10 s por caso |
| Interpretador | python do QGIS | python do sistema |

Ambos valem: o primeiro cobre casos de borda difíceis de montar com dados reais
(empate de altura, banda em sela); o segundo prova que o algoritmo publicado
realmente produz as flags esperadas.

## Estado conhecido

Nem todo módulo aqui está saudável. Alguns testes congelaram enquanto o código
seguiu, e só voltaram a ser visíveis quando passaram a ser executados de novo:

- `test_graphHandler.py` — os 4 testes de `BuildAuxFlowGraphTestCase` falham desde
  2023-06-29 (`d5454020`), quando `buildAuxFlowGraph` passou a exigir `nodeIdDict` e
  atributos de aresta (`featid`, `inside_river`). Os grafos do teste são abstratos
  demais para o contrato atual, e os resultados esperados foram escritos antes de a
  ordenação por distância existir — restaurá-los exige rederivar as expectativas com
  conhecimento do domínio de drenagem, não apenas ajustar a chamada. Os outros 5
  testes do módulo passam.
- `test_rasterHandler.py` — 6 dos 8 testes falham com
  `Could not open raster: mock_raster.tif`. O mock de `QgsRasterLayer` devolve um
  nome de arquivo que `readAsNumpy` tenta abrir de verdade no GDAL; ou o mock passa a
  cobrir a leitura, ou o teste precisa de um raster real pequeno em disco.
- `test_postgisDb_refactor.py`: os 67 testes davam erro desde 2026-04-10
  (`4590dd0a`, migração de QSql para psycopg2), porque substituíam `QSqlDatabase` e
  `QSqlQuery`, que o `PostgisDb` não usa mais. Os mocks agora ficam na camada atual:
  o `PsycopgDbAdapter` é substituído por um `MagicMock` com spec, e cada consulta
  recebe um `MockCursor` pelo `db.cursor()`. As afirmações seguem o contrato atual:
  a exceção sobe com o erro do driver, sem o prefixo `Problem ...: ` da versão QSql;
  `implementationVersion` devolve `""` para NULL; e saíram os testes de
  `getAggregationAttributes` e `makeValueRelationDict`, removidos como código morto em
  `ac0a7e48`. Os 62 testes passam.
- Quebrados também na base `d6448e6f` (rodada de 2026-11-05 no QGIS 4.2.1), com as
  mesmas falhas:
  - `test_CustomButtonSetup`, `test_DsgToolsProcessingModel`, `test_ExternalFilesHandler`
    e `test_OtherAlgorithms` não carregam: importam módulos ou nomes que não existem
    mais (`CustomFeatureToolBox`, `DSGToolsProcessingAlgs.Models`, a classe
    `ExternalFilesHandler`, `DsgTools.tests.algorithmsTestBase`).
  - `test_ValidationAlgorithms`: 19 falhas e 2 erros, e o módulo grava nos GPKG de
    `testing_datasets/` e `expected_outputs/`; restaure-os com
    `git checkout -- tests/testing_datasets tests/expected_outputs` depois de rodá-lo.
  - `test_identifyGapsAndOverlapsEdgeXor`: os 5 testes de cobertura leem a camada de
    saída depois que o contexto do Processing a destruiu (`wrapped C/C++ object ...
    has been deleted`).
- Os demais módulos ainda usam `unittest.makeSuite` em `run_all()`. Não afeta o
  `run_local.py`, mas quebra em Python 3.13 por outros caminhos.

### O código de saída do `run_local.py`

Até 2026-11-05 o QGIS 4.2.1 caía na saída do runner no Windows (0xC0000374, heap
corrompido, ou 0xC0000409) depois de imprimir o veredito, mesmo com todos os testes
passando. A causa era haver duas `QgsApplication` no processo: o runner criava a
sua, e cada módulo que chama `qgis.testing.start_app()` no import criava outra,
porque o `start_app()` só enxerga a aplicação que ele próprio criou, e registrava um
segundo `exitQgis()` no `atexit`. Agora o runner cria a aplicação pelo próprio
`start_app(cleanup=False)`, os módulos recebem a mesma instância, e o runner faz o
único `exitQgis()`.

Consequências para quem lê o resultado:

- `0` é tudo passou e `1` é alguma falha ou erro. Qualquer outro código (negativo no
  Windows) é queda do processo e não vale como veredito; leia o `OK`/`FAILED` impresso
  e investigue a queda.
- Se um módulo criar uma `QgsApplication` por fora do `start_app()`, o runner avisa
  em stderr (`AVISO: há uma segunda QgsApplication`). A saída pode voltar a cair, e
  então vale o veredito impresso. Medido: a segunda aplicação sozinha, sem o
  `exitQgis()` extra no `atexit`, saiu com `0`; a queda apareceu com as duas
  finalizações.
- Os testes rodam num perfil descartável do QGIS, criado pelo `start_app()` na pasta
  temporária e apagado no fim, e não no perfil do usuário.

## Escrevendo testes de flags

Ao testar algoritmos de validação, prefira asseverar **quantidade de flags e o texto
do `reason`** a congelar a geometria de saída num arquivo golden. Flags são
diagnóstico; golden de geometria quebra a cada refactor sem indicar defeito, e foi o
que fez os testes do modelo de terreno apodrecerem por seis anos sem ninguém notar.

Atenção também ao early-return: `TerrainModel.validate()` para na primeira classe de
erro encontrada (curvas → bandas → depressão → ponto cotado). Um fixture com erro de
banda **nunca** chega a validar depressão, então cada fixture deve conter uma única
classe de erro.
