# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings
from qgis.core import (
    QgsProcessingAlgorithm,
)


class DsgToolsBaseSetParametersAlgorithm(QgsProcessingAlgorithm):

    def getValueFromQSettings(self, v):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        value = settings.value(v)
        settings.endGroup()
        return value

    def storeParametersInConfig(self, parameters):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        for key, value in parameters.items():
            settings.setValue(self.QSETTINGS_DICT[key], value)
        settings.endGroup()

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.storeParametersInConfig(parameters)

        return {}

    