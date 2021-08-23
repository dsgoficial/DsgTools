#!/usr/bin/env bash

docker-compose exec -t qgis sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_ValidationAlgorithms \
                                            && qgis_testrunner.sh tests.test_EnvironmentSetterAlgorithms \
                                            && qgis_testrunner.sh tests.test_CustomButtonSetup && \ 
                                            qgis_testrunner.sh tests.test_DsgToolsProcessingModel && \
                                            qgis_testrunner.sh tests.test_OtherAlgorithms"