# -*- coding: utf-8 -*-
import os
import sys

import pytest

# Ensure DsgTools repo root is importable as 'DsgTools.*'
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# QGIS Python plugins path (processing, etc.)
_QGIS_PLUGINS = "/usr/share/qgis/python/plugins"
if _QGIS_PLUGINS not in sys.path:
    sys.path.insert(0, _QGIS_PLUGINS)


def pytest_addoption(parser):
    parser.addoption(
        "--regen",
        action="store_true",
        default=False,
        help="Regenerate expected output files instead of comparing against them.",
    )


@pytest.fixture(scope="session")
def regen_expected(request):
    """True when --regen flag is passed; makes tests save actual outputs as new expected."""
    return request.config.getoption("--regen")


@pytest.fixture(scope="session", autouse=True)
def _set_regen_flag(request):
    """Propagate --regen flag into the Tester class before any test runs."""
    from tests.test_ValidationAlgorithms import Tester
    Tester.REGEN = request.config.getoption("--regen")


@pytest.fixture(scope="session", autouse=True)
def _register_dsgtools_provider(qgis_app, qgis_processing):
    """Register the DSGTools processing provider for all tests.

    Uses pytest-qgis fixtures (qgis_app, qgis_processing) so QGIS and the
    native algorithms are already initialised before we add our provider.
    This fixture is test-infrastructure only — it must never be imported by
    the plugin codebase itself.
    """
    from qgis.core import QgsApplication
    from DsgTools.core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import (
        DSGToolsProcessingAlgorithmProvider,
    )

    provider = DSGToolsProcessingAlgorithmProvider()
    QgsApplication.processingRegistry().addProvider(provider)

    yield

    QgsApplication.processingRegistry().removeProvider(provider)
