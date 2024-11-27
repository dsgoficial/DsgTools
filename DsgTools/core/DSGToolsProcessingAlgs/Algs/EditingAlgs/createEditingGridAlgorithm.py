# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-04-25
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import processing, os, requests
from time import sleep
from qgis.PyQt.Qt import QVariant
from PyQt5.QtCore import QCoreApplication
from ....EditingTools.gridAndLabelCreator import GridAndLabelCreator
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsDataSourceUri,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingUtils,
    QgsSpatialIndex,
    QgsGeometry,
    QgsProcessingParameterField,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterExpression,
    QgsProcessingException,
    QgsProcessingParameterString,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterType,
    QgsProcessingParameterCrs,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsField,
    QgsFields,
)


class CreateEditingGridAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    ATTRIBUTE_INDEX = "ATTRIBUTE_INDEX"
    ATTRIBUTE_ID = "ATTRIBUTE_ID"
    ID_VALUE = "ID_VALUE"
    CROSSES_X = "CROSSES_X"
    CROSSES_Y = "CROSSES_Y"
    SPACING = "SPACING"
    MAP_SCALE = "MAP_SCALE"
    COLOR = "COLOR"
    FONT = "FONT"
    FONT_SIZE = "FONT_SIZE"
    FONT_LL = "FONT_LL"
    COLOR_LL = "COLOR_LL"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input Layer"), [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_INDEX,
                self.tr("INOM Field"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_ID,
                self.tr("ID Field"),
                None,
                "INPUT",
                QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ID_VALUE,
                self.tr("ID Field Value"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CROSSES_X,
                self.tr("Number of horizontal crosses"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=4,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CROSSES_Y,
                self.tr("Number of vertical crosses"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=4,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SPACING,
                self.tr("UTM Grid Spacing"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=4000,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAP_SCALE,
                self.tr("Map scale (in thousands)"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=25,
            )
        )

        colorParameter = ParameterColor(self.COLOR, description=self.tr("Color"))
        colorParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.colorWidgetWrapper.ColorWidgetWrapper"
            }
        )
        self.addParameter(colorParameter)

        fontParameter = ParameterFont(
            self.FONT, description=self.tr("Font of the label")
        )
        fontParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.fontWidgetWrapper.FontWidgetWrapper"
            }
        )
        self.addParameter(fontParameter)

        self.addParameter(
            QgsProcessingParameterNumber(
                self.FONT_SIZE,
                self.tr("Font Size"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1.5,
            )
        )

        fontParameter = ParameterFont(
            self.FONT_LL, description=self.tr("Font of the LatLong label")
        )
        fontParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.fontWidgetWrapper.FontWidgetWrapper"
            }
        )
        self.addParameter(fontParameter)

        colorParameter = ParameterColor(
            self.COLOR_LL, description=self.tr("Lat Long Color")
        )
        colorParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.colorWidgetWrapper.ColorWidgetWrapper"
            }
        )
        self.addParameter(colorParameter)

        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT, self.tr("Original layer with assigned styles")
            )
        )

    def parameterAsColor(self, parameters, name, context):
        return parameters[name]

    def parameterAsFont(self, parameters, name, context):
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        gridLayer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        attribute = self.parameterAsFields(parameters, self.ATTRIBUTE_INDEX, context)[0]
        id_attribute = self.parameterAsFields(parameters, self.ATTRIBUTE_ID, context)[0]
        id_value = self.parameterAsInt(parameters, self.ID_VALUE, context)
        spacing = self.parameterAsInt(parameters, self.SPACING, context)
        crossX = self.parameterAsInt(parameters, self.CROSSES_X, context)
        crossY = self.parameterAsInt(parameters, self.CROSSES_Y, context)
        color = self.parameterAsColor(parameters, self.COLOR, context)
        scale = self.parameterAsDouble(parameters, self.MAP_SCALE, context)
        fontSize = self.parameterAsDouble(parameters, self.FONT_SIZE, context)
        font = self.parameterAsFont(parameters, self.FONT, context)
        fontLL = self.parameterAsFont(parameters, self.FONT_LL, context)
        llcolor = self.parameterAsColor(parameters, self.COLOR_LL, context)

        gridGenerator = GridAndLabelCreator()
        gridCrs = gridLayer.crs().authid()
        srid = gridCrs.replace("EPSG:", "")
        gridGeometry = next(gridLayer.getFeatures()).geometry()
        gridOpts = {
                "crossX": crossX,
                "crossY": crossY,
                "fontSize": fontSize,
                "font": font,
                "fontLL": fontLL,
                "llcolor": llcolor,
                "linwidth_geo": 0.07,
                "linwidth_utm": 0.05,
                "linwidth_buffer_geo": 0,
                "linwidth_buffer_utm": 0,
                "geo_grid_color": llcolor,
                "utm_grid_color": color,
                "geo_grid_buffer_color": llcolor,
                "utm_grid_buffer_color": color,
                "masks_check": True,
            }
        gridGenerator.styleCreator(
            feature_geometry=gridGeometry,
            layer_bound=gridLayer,
            utmSRID=srid,
            id_attr="id",
            id_value=1,
            scale=scale,
            spacing=spacing,
            **gridOpts,
        )
        gridLayer.triggerRepaint()

        return {self.OUTPUT: gridLayer}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "createeditinggrid"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Create Editing Grid")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Cartographic Finishing Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Cartographic Finishing Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("CreateEditingGridAlgorithm", string)

    def createInstance(self):
        return CreateEditingGridAlgorithm()


class ParameterFontType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterFont(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.fontWidgetWrapper.FontWidgetWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", "Font Parameter")

    def id(self):
        return "font"

    def description(self):
        return QCoreApplication.translate("Processing", "Font parameter.")


class ParameterFont(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterFont(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "font"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()


class ParameterColorType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterColor(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.fontWidgetWrapper.ColorWidgetWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", "Color Parameter")

    def id(self):
        return "color"

    def description(self):
        return QCoreApplication.translate("Processing", "Color parameter.")


class ParameterColor(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterColor(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "color"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
