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
from PyQt5.QtCore import QCoreApplication
from qgis.core import QgsProcessingParameterString

from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.dsgtoolsBaseSetParametersAlgorithm import \
    DsgToolsBaseSetParametersAlgorithm


class GenericSelectionToolParametersAlgorithm(DsgToolsBaseSetParametersAlgorithm):
    VALUE_LIST = "VALUE_LIST"

    QSETTINGS_DICT = {
        "VALUE_LIST": "valueList",
    }

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.VALUE_LIST,
                self.tr("Black list for Generic Selection Tool (values must be separated by ;)"),
                multiLine=False,
                defaultValue="aux_grid_revisao_a;Created Review Grid;grid;moldura",
            )
        )

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "genericselectiontoolparametersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Generic Selection Tool Parameters")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Environment Setters")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Environment Setters"

    def tr(self, string):
        return QCoreApplication.translate("GenericSelectionToolParametersAlgorithm", string)

    def createInstance(self):
        return GenericSelectionToolParametersAlgorithm()
