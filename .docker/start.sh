#!/usr/bin/env bash

docker-compose up -d --build
echo 'Wait 10 seconds'
sleep 10
echo 'Installation of the plugin'
docker exec -t dsgtools-testing-env sh -c "qgis_setup.sh DsgTools && \
                                             rm -f  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools && \
                                             ln -s /tests_directory/ /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools && \
                                             apt update && apt install -y libqt5sql5-psql libqt5sql5-sqlite"
echo 'Containers are running'