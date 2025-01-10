# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-01-06
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import json
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingParameterDefinition,
    QgsProcessingParameterType,
)

class ParameterDbConversionType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterDbConversion(name)  # mudar

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.dbConversionWrapper.DbConversionWrapper"
        }  # mudar

    def name(self):
        return QCoreApplication.translate("Processing", "Database Conversion Maps")

    def id(self):
        return "db_conversion_maps"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "A list of database conversion maps. Used in the Convert Database algorithm.",
        )


class ParameterDbConversion(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterDbConversion(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "db_conversion_maps"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return json.dumps(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
