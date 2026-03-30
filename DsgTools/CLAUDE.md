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
