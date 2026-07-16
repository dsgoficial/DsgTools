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
- Os demais módulos ainda usam `unittest.makeSuite` em `run_all()`. Não afeta o
  `run_local.py`, mas quebra em Python 3.13 por outros caminhos.

## Escrevendo testes de flags

Ao testar algoritmos de validação, prefira asseverar **quantidade de flags e o texto
do `reason`** a congelar a geometria de saída num arquivo golden. Flags são
diagnóstico; golden de geometria quebra a cada refactor sem indicar defeito, e foi o
que fez os testes do modelo de terreno apodrecerem por seis anos sem ninguém notar.

Atenção também ao early-return: `TerrainModel.validate()` para na primeira classe de
erro encontrada (curvas → bandas → depressão → ponto cotado). Um fixture com erro de
banda **nunca** chega a validar depressão, então cada fixture deve conter uma única
classe de erro.
