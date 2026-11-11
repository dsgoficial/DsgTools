# -*- coding: utf-8 -*-
"""
Compatibility shim for QGIS 3.x (PyQt5).

PyQt5's uic.loadUiType() turns every ``<include location="resources.qrc"/>``
found in a .ui file into a top-level ``import resources_rc`` (the plugin dir
is appended to sys.path in dsg_tools.py). Several hand-compiled *_ui.py files
also import it directly. The real compiled resources live in resources.py, so
this module only makes sure they are registered.

This file must stay small and tracked: resources.qrc was renamed to
resources.qrc.src so qgis-plugin-ci no longer generates resources_rc.py at
package time. PyQt6's uic (QGIS 4 / DsgTools 5) ignores <resources>, which is
why this shim is not needed on the dev branch.
"""
from DsgTools import resources  # noqa: F401
