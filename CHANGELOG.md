# CHANGELOG

## [4.2](https://github.com/dsgoficial/DsgTools/releases/tag/v4.2)

New algorithms and a Refactor to DSGTools feature extraction tool.

### New algorithms:

- Enforce Attribute Rules;
- Identify Polygon Sliver;

### Enhancements:

- Enforce Spatial Rules has improved to accept rules using the DE-9IM mask;
- Build Polygons From Center Points has now a spatial relationship check;

### Bug fixes:

- Topological Clean deleting features;
- Run Remote FME Workspace listing workspaces;
- Build Polygons From Center Points and Boundaries API compatibility;
- Remove obsolete pg_constraint.consrc column for PostgreSQL 12+;
- BDGEx WFS connection fixes;
- Using Reshape Freehand at polygons don't cause a crash anymore

The full changelog at https://github.com/dsgoficial/DsgTools/wiki/Changelog-4.2
## [4.1](https://github.com/dsgoficial/DsgTools/releases/tag/v4.1)

New algorithms and a Refactor to DSGTools feature extraction tool.

### New features:

- DSGTools Feature Classification is now renamed to DSGTools Custom Feature Tool Box and was completely remodeled;
- A few bug fixes and UX improvements;
- Added a few new algorithms, such as Enforce spatial rules, Identify Terrain, Identify Angles in Invalid Range and a couple more.

Check out the full changelog at https://github.com/dsgoficial/DsgTools/wiki/Changelog-4.1

## [4.0](https://github.com/dsgoficial/DsgTools/releases/tag/4.0)

### New Features:
- DSGTools now have a Processing Provider Called DSGToolsAlgorithm. Algorithms were grouped by types such as Data Quality, Quality Assurance, Editing Algorithms and Layer Management Algorithms. It has 61 algorithms, as follows:
                 ```   'Deaggregate Geometries', 'Identify Small Polygons', 'Identify Small Lines', 'Identify Duplicated Geometries', 'Identify Out Of Bounds Angles', 'Identify Out Of Bounds Angles in Coverage', 'Identify Overlaps', 'Identify Gaps and Overlaps in Coverage Layers', 'Identify Dangles', 'Identify Gaps', 'Donut Hole Extractor', 'Update Layer', 'Topological Clean Polygons', 'Topological Douglas Peucker Simplification', 'Remove Duplicated Geometries', 'Remove Small Lines', 'Remove Small Polygons', 'Clean Geometries', 'Merge lines with same attribute set', 'Topological Clean Linestrings', 'Snap layer on layer', 'Line on line overlayer', 'Dissolve polygons with same attribute set', 'Snap to grid and update', 'Remove empty and update', 'Convert layer to layer', 'Overlay Elements With Areas', 'Create Drainage Network Nodes', 'Verify Drainage Network Directioning', 'Identify Duplicated Features', 'Adjust Network Connectivity', 'Remove Duplicated Features', 'Hierarchical Snap layer on layer', 'Identify Duplicated Polygons Between Layers', 'Identify Duplicated Lines Between Layers', 'Identify Duplicated Points Between Layers', 'Run Remote FME Workspace', 'Generate Systematic Grid', 'Run File Inventory', 'Raise Flags', 'Identify And Fix Invalid Geometries', 'Create Editing Grid', 'Assign Filter to Layers', 'Assign Bounding Box Filter to Layers', 'Assign Measure Column to Layers', 'Group Layers', 'Topological adjustment of the connectivity of lines', 'Calculate RMS and Percentile 90 of Layer', 'Rule Statistics', 'Match and Apply QML Styles to Layers', 'Apply Styles from Database to Layers', 'Export To Memory Layer', 'Assign Custom Form and Format Rules to Layers', 'Assign Value Map to Layers', 'Load Layers From Postgis', 'Load Non-Spatial Layers From PostgreSQL', 'Assign Aliases to Layers', 'Build Joins on Layers', 'Batch Run Algorithm', 'String CSV to Layer List Algorithm', 'Identify Wrong Building Angles' ```
- New Quality Assurance Toolbox that allows users to stop between executions of models if there are flags raised in a flag layer;
- New Quality Assurance Toolbar that allows users to change between installed models and run them using a single hotkey;
- New Toggle Layers Visibility Tool that allows users to toggle layers visibylity using a hotkey;
- New Toggle Layers' Label Visibility Tool that allows users to toggle layers' label visibility using a hotkey;
- New BDGEx (Brazilian SDI) layers, such as: Digital Surface Models, Artificial SAR Imagery and Multi-scale mosaics;
                
### Enhancements:
- Database Conversion Tool has been updated with new UX and new features such as 1:n conversion, m:n conversion and geoprocessing features such as clip before conversion;
- Inspect Features now can zoom to a % of the bounding box of the feature;
- Option to set active layer to the feature inspector;
- Performance improvements on Quality Assurance algorithms (previously called validation algorithms) ;
- Style swap in the style  toolbar is now generic (works with any style stored into PostgreSQL database);
##Changes:
- Bug fixes;
- Dropped support for EDGV FTer_2a_Ed (DSGTools no longer creates this model, but feature loading is still supported);
- Bug fixes on EDGV 3.0 model;

## [3.2](https://github.com/dsgoficial/DsgTools/releases/tag/v3.2)

### New Features
- New raster toolbar with band tooltips, dynamic histogram and band value capture;
- New flip line tool;
- New free hand acquisition tool;
- New validation process: Drainage Network Directioning Processes;
- New validation process: Identify out of bounds angles in coverage;

### Enhancements
- Generic Selection Tool: New rubberband on features, new context menu and better performance;
- Right Angle digitizing tool: Better rubberband, real time segment length and real time polygon check;
- New options menu to customize tools.

[Visual changelog (just in portuguese)](https://github.com/dsgoficial/DsgTools/wiki/Changelog-3.2)


## [3.1.2](https://github.com/dsgoficial/DsgTools/releases/tag/v3.2)

### Bug fixes:
- Bug fix on Generic Selection Tool
- Bug fix on loading EDGV FTer_2a_Ed databases with custom check constraints
- Bug fix on Validation Processes
- Bug fix on Field Toolbox