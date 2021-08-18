#!/usr/bin/env bash

docker exec -it dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_ValidationAlgorithms"
docker exec -it dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_EnvironmentSetterAlgorithms"
docker exec -it dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_CustomButtonSetup"
docker exec -it dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_DsgToolsProcessingModel"
docker exec -it dsgtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_OtherAlgorithms"