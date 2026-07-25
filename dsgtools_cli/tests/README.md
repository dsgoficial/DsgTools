# Testes do dsgtools-cli

Dois níveis de teste em `test_grid_algorithms.py`:

1. **Unitários** (sempre rodam, não precisam de QGIS) — funções puras do CLI:
   `full_id`, `_coerce`, `_unwrap_inputs`, `_parse_json_stdout`, `_summarize_help`.

2. **Integração** (pulados se o `qgis_process` não for encontrado) — executam de fato
   os algoritmos de grade via linha de comando, salvam o resultado em **GeoJSON** e
   comparam, feição a feição, com os arquivos *golden* em [`data/`](data):
   - `dsgtools:gridzonegenerator` → 24 molduras (250k → 50k)
   - `dsgtools:createframeswithconstraintalgorithm` → 13 molduras (a partir de
     `data/constraint_input.geojson` → 100k)

A comparação é robusta: normaliza o GeoJSON para `(inom, mi, tipo, coords arredondadas
a 3 casas)` e compara como conjunto ordenado — ignora ordem das feições e ruído de
precisão sub-milimétrico (o CRS dos golden é métrico, EPSG:31982).

Além desses, `test_cli_contract.py` cobre (**sem QGIS**, com o contrato injetado como
fixture no formato real do `help --json`) as camadas que ficam entre o chamador e o
`qgis_process`:

- **validação local** dos parâmetros do `run` (nome inexistente, obrigatório ausente,
  índice de enum fora da faixa, rótulo no lugar do índice) e a mensagem de erro, que
  precisa carregar o contrato dos parâmetros citados;
- **cache do contrato** em disco (roundtrip, invalidação pela impressão digital, arquivo
  corrompido, pasta impossível de escrever, e a asserção central: a 2ª consulta não sobe
  o QGIS de novo);
- **`describe` compacto** (uma linha por parâmetro, opções, prosa curada, exemplo pronto
  para colar) e o **`--dry-run`**.

É de propósito que não precisem de QGIS: a validação existe justamente para poupar a
chamada cara, então testá-la não pode custar essa chamada (a suíte inteira roda em ~0,1 s).

## Rodar

```bash
pip install pytest
pytest dsgtools_cli/tests -v
```

Se o `qgis_process` não estiver no PATH, aponte-o:

```bash
# Windows
set DSGTOOLS_QGIS_PROCESS=C:\Program Files\QGIS 4.0.0\bin\qgis_process-qgis.bat
```

Sem QGIS, os testes de execução são **pulados** (skip) e só os unitários rodam — útil
para CI sem QGIS.

## Golden / fixtures

Os arquivos em `data/` são a referência. Regenere-os **apenas após uma mudança
intencional** de comportamento dos algoritmos:

```bash
python dsgtools_cli/tests/regenerate_fixtures.py
```

| Arquivo | O que é |
|---|---|
| `gridzonegenerator_expected.geojson` | saída esperada do Generate Systematic Grid (24 feições) |
| `constraint_input.geojson` | entrada do teste related-to-layer (1 moldura 250k) |
| `createframeswithconstraintalgorithm_expected.geojson` | saída esperada do related-to-layer (13 feições) |
