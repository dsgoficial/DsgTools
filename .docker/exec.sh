#!/usr/bin/env bash

docker exec -t dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_ValidationAlgorithms"
docker exec -t dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_EnvironmentSetterAlgorithms"
docker exec -t dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_CustomButtonSetup"
docker exec -t dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_DsgToolsProcessingModel"
docker exec -t dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_OtherAlgorithms"
