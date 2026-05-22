#!/usr/bin/env bash
# Local test runner — sets up the QGIS Python environment and delegates to pytest.
# Usage:
#   ./run_tests.sh                          # run all tests
#   ./run_tests.sh tests/test_graphHandler.py
#   ./run_tests.sh -k test_identifydangles  # run a single test by name
#   ./run_tests.sh -x                       # stop on first failure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYTHONPATH="\
/usr/share/qgis/python:\
/usr/share/qgis/python/plugins:\
/usr/lib/python3/dist-packages:\
${SCRIPT_DIR}"

export QT_QPA_PLATFORM=offscreen

python3 -m pytest "$@"
