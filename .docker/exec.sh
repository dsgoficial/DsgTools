#!/usr/bin/env bash

docker exec -t dsgtools-testing-env sh -c "
  export PYTHONPATH=/usr/share/qgis/python:/usr/share/qgis/python/plugins:/usr/lib/python3/dist-packages:/tests_directory
  export QT_QPA_PLATFORM=offscreen
  cd /tests_directory && python3 -m pytest tests/ -v
"
