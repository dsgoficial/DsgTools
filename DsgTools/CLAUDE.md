# CLAUDE.md - DsgTools

## Projeto

Plugin QGIS do Exército Brasileiro para produção cartográfica (DSG Tools).
Licença: GNU GPL v2. Repositório: https://github.com/dsgoficial/DsgTools

## Estrutura

```
DsgTools/
├── __init__.py          # Entry point (classFactory)
├── dsg_tools.py         # Classe principal DsgTools
├── metadata.txt         # Metadados do plugin QGIS
├── resources.py         # Recursos Qt compilados
├── core/                # Lógica de negócio
│   ├── DSGToolsProcessingAlgs/  # Algoritmos de processamento
│   ├── DbModels/        # Modelos de banco (PostGIS, SpatiaLite, Geopackage)
│   ├── DbTools/         # Utilitários de banco
│   ├── EditingTools/    # Ferramentas de edição
│   ├── Factories/       # Factory patterns (Db, Layer, Thread, SQL)
│   ├── GeometricTools/  # Operações geométricas
│   ├── LayerTools/      # Manipulação de camadas
│   ├── NetworkTools/    # Rede/topologia
│   ├── ServerManagementTools/
│   └── Utils/           # Utilitários gerais
├── gui/                 # Interface gráfica
│   ├── guiManager.py    # Orquestrador central de GUI
│   ├── CustomWidgets/   # Widgets reutilizáveis
│   ├── ProductionTools/ # Ferramentas de produção (MapTools, Toolbars)
│   ├── DatabaseTools/   # UI de gerenciamento de banco
│   ├── BDGExTools/      # Integração BDGEx
│   └── ...
├── Modules/             # Módulos legados (acquisitionMenu, qgis, utils)
├── i18n/                # Tradução PT-BR
└── icons/               # Ícones PNG/SVG
```

## Convenções de Código

- **Linguagem**: Python 3. Sem type hints obrigatórios.
- **Imports Qt**: Usar sempre `from qgis.PyQt` (nunca `from PyQt5` nem `from PyQt6` diretamente).
- **Estilo**: camelCase para métodos e variáveis (padrão Qt/QGIS, não PEP8 snake_case).
- **Commits**: Mensagens em português ou inglês, sem padrão rígido.
- **Sem testes unitários formais** no repo. Testes via Docker no CI.

## CI/CD

- `.github/workflows/test_plugin_on_qgis.yml` — Testes via Docker no push/PR para master.
- `.github/workflows/release.yml` — Deploy para repositório de plugins OSGeo via `qgis-plugin-ci`.
- Triggers: push to master, PR to master/dev, release publication.

## CHANGELOG

Arquivo: `CHANGELOG.md` na raiz do repo — fonte da verdade, escrito antes. O `changelog=` do `DsgTools/metadata.txt` é atualizado manualmente em seguida, replicando o mesmo conteúdo da versão que acabou de fechar (não das versões antigas, essas ficam como estão) no formato próprio do `metadata.txt` (ver seção Versionamento e Release abaixo).

- Formato do cabeçalho de versão: `## <versão> - <data ou "dev">`.
- Versão em desenvolvimento (ainda não lançada) leva `- dev` no lugar da data. Só vira `YYYY-MM-DD` no dia do release — troca `dev` pela data do lançamento naquele momento, não antes.
- Dentro de cada versão, até três subseções, nesta ordem, só as que tiverem conteúdo: `Novas Funcionalidades:`, `Melhorias:`, `Correções de bug:`.
- Cada item é um bullet `- Texto;` (termina em ponto e vírgula), em português, descrevendo o efeito pra quem usa o plugin (não a implementação).
- Itens novos são adicionados **sequencialmente ao final** da subseção correspondente da versão `dev` do topo, à medida que o trabalho vai sendo feito — não abre versão nova a cada commit/PR, só na hora de lançar.
- Ao lançar uma versão: troca o `- dev` pela data do release na entrada do topo, e abre uma nova `## <próxima versão> - dev` acima dela pros próximos commits (ver como calcular a próxima versão abaixo).
- Mudanças puramente internas (lint, formatação, refactor sem efeito observável, testes) não entram no changelog — só o que afeta quem usa o plugin.

## Versionamento e Release

Formato `X.Y.Z`. `Y` (segundo dígito) diz se é dev ou lançada; `Z` (terceiro dígito) é o contador de mudanças dentro do ciclo atual.

- **`Y` ímpar = versão de desenvolvimento** (ainda não lançada, branch `dev`). **`Y` par = versão lançada** (branch `master`, publicada no repositório OSGeo).
- **Toda alteração de funcionalidade — nova funcionalidade OU correção de bug — incrementa o terceiro dígito (`Z`) da versão dev atual.** Isso vale inclusive quando a correção de bug é sobre algo que já está na versão lançada (par): a correção entra pelo `dev` e incrementa o `Z` do dev corrente — não existe uma linha de patch separada na versão par (não se cria "5.2.1"; a correção vira parte do próximo "5.3.x - dev" e só chega a quem usa a versão lançada no próximo release).
  - Exemplo: dev está em `5.1.2`. Uma nova funcionalidade (ou correção de bug) é adicionada → passa a `5.1.3`.
- **Ao lançar (release)**: incrementa `Y` para o próximo par e zera `Z`. Exemplo: dev `5.1.2` (ou o `Z` que estiver corrente) lança como `5.2.0`.
  - Depois do lançamento, abre-se o próximo ciclo dev com `Y` ímpar seguinte e `Z=0` (no exemplo, `5.3.0 - dev`).
- Arquivos que carregam o número de versão e que devem ser mantidos em sincronia no commit de preparação do release:
  - `CHANGELOG.md` — cabeçalho da versão que está fechando (`- dev` → data) + abre o cabeçalho do próximo ciclo dev.
  - `DsgTools/metadata.txt` — campo `version=` e um novo bloco dentro de `changelog=`, no formato/indentação (tabs) já usado pelas versões anteriores, replicando o conteúdo do `CHANGELOG.md` dessa versão. Isso é só pra manter o arquivo legível/consistente pra quem olha o repo direto — o `qgis-plugin-ci` (rodado pelo `release.yml`) **regenera esse bloco sozinho a partir do `CHANGELOG.md`** (formato dele: indentação de 1 espaço, cabeçalho `Version X.Y.Z:`) toda vez que empacota, mas isso acontece só na cópia efêmera do runner de CI — nunca commita de volta no repo. Não precisa bater com o formato que o tooling gera.
  - `README.md` — tabela `branch|status|version`: linha `master` recebe a versão que acabou de ser lançada (par), linha `dev` recebe o próximo ciclo dev (ímpar, `Z=0`).
- Fluxo de release: commit de preparação (changelog + metadata + README) direto no `dev` → PR `dev` → `master`, título `Versão X.Y.Z`, corpo com o conteúdo do changelog dessa versão → merge → **publicar um GitHub Release com tag `X.Y.Z`** (é isso que dispara `.github/workflows/release.yml`; merge do PR sozinho não aciona nada).
- **Antes de publicar o GitHub Release**, vale rodar `qgis-plugin-ci package <versão> -c` localmente (não precisa de credenciais, só empacota, não sobe nada) pra pegar erro de empacotamento cedo. Já achamos dois assim, que ficaram anos escondidos atrás da falha de Python do CI (ver Armadilhas abaixo) — o `release.yml` só roda em `release: published`, então um erro aqui só aparece depois que a release já foi anunciada.

### Armadilhas conhecidas do `metadata.txt` para o `qgis-plugin-ci`

O parser de metadata do `qgis-plugin-ci` é ingênuo: só lê o texto que está na própria linha de cada chave (`chave=valor`), não entende continuação multi-linha do formato QGIS (que o `metadata.txt` usa e o QGIS Desktop entende normalmente). Chaves obrigatórias pra ele: `name`, `about`, `description`, `qgisMinimumVersion`, `tracker`, `repository`. Se qualquer uma virar multi-linha (só `about` corre esse risco hoje, é a única longa), ele aborta com `Mandatory key is missing in metadata: <chave>` — **sempre deixar a primeira frase na própria linha da chave** (o resto pode continuar multi-linha normalmente, o QGIS renderiza certo).

`DsgTools/resources_rc.py` não deve existir versionado — é artefato de build (`pyrcc5` a partir de `resources.qrc`) que o `qgis-plugin-ci package` gera sozinho a cada empacotamento e recusa sobrescrever se já existir arquivo versionado com esse nome exato. Fica no `.gitignore`, junto com `*.zip` da raiz (saída do `package`).

## Migração QGIS 4.0 (Branch `qgis4`)

A migração principal é Qt5 → Qt6. O QGIS 4.0 não quebra APIs além do Qt6.

### Regras de Migração

1. **Imports**: `from qgis.PyQt.QtWidgets import ...` (já correto na maioria dos arquivos)
2. **exec_()** → **exec()**: Em QDialog, QApplication, etc.
3. **Enums Qt6 devem ser fully qualified**:

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `Qt.UserRole` | `Qt.ItemDataRole.UserRole` |
| `Qt.Checked` | `Qt.CheckState.Checked` |
| `Qt.Unchecked` | `Qt.CheckState.Unchecked` |
| `Qt.ItemIsEnabled` | `Qt.ItemFlag.ItemIsEnabled` |
| `Qt.ItemIsSelectable` | `Qt.ItemFlag.ItemIsSelectable` |
| `Qt.ItemIsUserCheckable` | `Qt.ItemFlag.ItemIsUserCheckable` |
| `Qt.Horizontal` | `Qt.Orientation.Horizontal` |
| `Qt.Vertical` | `Qt.Orientation.Vertical` |
| `Qt.WaitCursor` | `Qt.CursorShape.WaitCursor` |
| `Qt.ArrowCursor` | `Qt.CursorShape.ArrowCursor` |
| `Qt.MatchExactly` | `Qt.MatchFlag.MatchExactly` |
| `Qt.DisplayRole` | `Qt.ItemDataRole.DisplayRole` |
| `Qt.EditRole` | `Qt.ItemDataRole.EditRole` |
| `Qt.DecorationRole` | `Qt.ItemDataRole.DecorationRole` |
| `Qt.ToolTipRole` | `Qt.ItemDataRole.ToolTipRole` |
| `Qt.AlignCenter` | `Qt.AlignmentFlag.AlignCenter` |
| `Qt.AlignLeft` | `Qt.AlignmentFlag.AlignLeft` |
| `Qt.AlignRight` | `Qt.AlignmentFlag.AlignRight` |
| `Qt.LeftButton` | `Qt.MouseButton.LeftButton` |
| `Qt.RightButton` | `Qt.MouseButton.RightButton` |
| `Qt.KeepAspectRatio` | `Qt.AspectRatioMode.KeepAspectRatio` |
| `Qt.SmoothTransformation` | `Qt.TransformationMode.SmoothTransformation` |
| `Qt.DescendingOrder` | `Qt.SortOrder.DescendingOrder` |
| `Qt.AscendingOrder` | `Qt.SortOrder.AscendingOrder` |
| `Qt.white` | `Qt.GlobalColor.white` |
| `Qt.red` | `Qt.GlobalColor.red` |
| `Qt.green` | `Qt.GlobalColor.green` |
| `Qt.black` | `Qt.GlobalColor.black` |
| `Qt.blue` | `Qt.GlobalColor.blue` |
| `Qt.yellow` | `Qt.GlobalColor.yellow` |
| `Qt.NoPen` | `Qt.PenStyle.NoPen` |
| `Qt.SolidLine` | `Qt.PenStyle.SolidLine` |
| `Qt.DashLine` | `Qt.PenStyle.DashLine` |
| `Qt.NoBrush` | `Qt.BrushStyle.NoBrush` |
| `Qt.SolidPattern` | `Qt.BrushStyle.SolidPattern` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QMessageBox.Yes` | `QMessageBox.StandardButton.Yes` |
| `QMessageBox.No` | `QMessageBox.StandardButton.No` |
| `QMessageBox.Ok` | `QMessageBox.StandardButton.Ok` |
| `QMessageBox.Cancel` | `QMessageBox.StandardButton.Cancel` |
| `QMessageBox.Warning` | `QMessageBox.Icon.Warning` |
| `QMessageBox.Information` | `QMessageBox.Icon.Information` |
| `QMessageBox.Critical` | `QMessageBox.Icon.Critical` |
| `QMessageBox.Question` | `QMessageBox.Icon.Question` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QDialogButtonBox.Ok` | `QDialogButtonBox.StandardButton.Ok` |
| `QDialogButtonBox.Cancel` | `QDialogButtonBox.StandardButton.Cancel` |
| `QDialogButtonBox.Apply` | `QDialogButtonBox.StandardButton.Apply` |
| `QDialogButtonBox.Close` | `QDialogButtonBox.StandardButton.Close` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QSizePolicy.Expanding` | `QSizePolicy.Policy.Expanding` |
| `QSizePolicy.Fixed` | `QSizePolicy.Policy.Fixed` |
| `QSizePolicy.Preferred` | `QSizePolicy.Policy.Preferred` |
| `QSizePolicy.Minimum` | `QSizePolicy.Policy.Minimum` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QFileDialog.ExistingFile` | `QFileDialog.FileMode.ExistingFile` |
| `QFileDialog.Directory` | `QFileDialog.FileMode.Directory` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `Qgis.Warning` | `Qgis.MessageLevel.Warning` |
| `Qgis.Critical` | `Qgis.MessageLevel.Critical` |
| `Qgis.Info` | `Qgis.MessageLevel.Info` |
| `Qgis.Success` | `Qgis.MessageLevel.Success` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QgsWkbTypes.PointGeometry` | `Qgis.GeometryType.Point` |
| `QgsWkbTypes.LineGeometry` | `Qgis.GeometryType.Line` |
| `QgsWkbTypes.PolygonGeometry` | `Qgis.GeometryType.Polygon` |
| `QgsWkbTypes.UnknownGeometry` | `Qgis.GeometryType.Unknown` |
| `QgsWkbTypes.NullGeometry` | `Qgis.GeometryType.Null` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QgsMapLayer.VectorLayer` | `Qgis.LayerType.Vector` |
| `QgsMapLayer.RasterLayer` | `Qgis.LayerType.Raster` |

| Antes (Qt5) | Depois (Qt6) |
|---|---|
| `QgsMapLayerProxyModel.VectorLayer` | `Qgis.LayerFilter.VectorLayer` |
| `QgsMapLayerProxyModel.RasterLayer` | `Qgis.LayerFilter.RasterLayer` |
| `QgsMapLayerProxyModel.NoGeometry` | `Qgis.LayerFilter.NoGeometry` |
| `QgsMapLayerProxyModel.HasGeometry` | `Qgis.LayerFilter.HasGeometry` |

### ATENTAR: NÃO migrar estes

- `QgsWkbTypes.Point`, `QgsWkbTypes.LineString`, `QgsWkbTypes.Polygon` etc. — são constantes WKB, NÃO enums Qt. Deixar como estão.
- `QgsProject.instance()` — remoção prevista apenas para QGIS 5.0.
- `QVariant.Type` — deprecado em 3.38 mas mínimo suportado é 3.22, manter por enquanto.

### Padrão de compatibilidade dual (Qt5 + Qt6)

Quando necessário manter compatibilidade com ambas versões:

```python
try:
    # Qt6 / QGIS 4
    from qgis.PyQt.QtCore import QEnum
except ImportError:
    pass  # Qt5 fallback
```

Para enums, preferir a forma fully qualified do Qt6 que já funciona no QGIS 3.40+.

## Comandos Úteis

```bash
# Verificar imports PyQt5 diretos (devem ser zero)
grep -r "from PyQt5\." --include="*.py" | wc -l

# Verificar exec_() remanescentes
grep -rn "\.exec_()" --include="*.py"

# Verificar enums não qualificados (exemplos)
grep -rn "Qt\.UserRole[^.]" --include="*.py"
grep -rn "QMessageBox\.Yes[^.]" --include="*.py"
grep -rn "Qgis\.Warning[^.]" --include="*.py"
```
