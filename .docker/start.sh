#!/usr/bin/env bash

docker-compose up -d --build
echo 'Wait 10 seconds'
sleep 10
echo 'Installation of the plugin'
docker exec -t dsgtools-testing-env sh -c "qgis_setup.sh"
docker exec -t dsgtools-testing-env sh -c "rm -f  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools"
docker exec -t dsgtools-testing-env sh -c "ln -s /tests_directory/ /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools"
docker exec -t dsgtools-testing-env sh -c "apt update && apt install -y libqt5sql5-psql libqt5sql5-sqlite"
docker exec -t dsgtools-testing-env sh -c "pip3 install numpy networkx"
echo 'Containers are running'
