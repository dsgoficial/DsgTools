# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BuildMergedDataWithFieldRefactorAlgorithm
                                 A QGIS plugin
 Build merged data with field refactor
                              -------------------
        begin                : 2025-08-27
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

import random
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingException,
    QgsProcessingParameterType,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterCrs,
    QgsProcessingParameterString,
    QgsFields,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsSymbol,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsVectorLayer,
    QgsProcessingUtils,
)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class BuildMergedDataWithFieldRefactorAlgorithm(ValidationAlgorithm):
    LAYERS_CONFIG = "LAYERS_CONFIG"
    OUTPUT_CRS = "OUTPUT_CRS"
    FIELD_NAME = "FIELD_NAME"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        layersConfigSetter = ParameterLayersConfig(
            self.LAYERS_CONFIG, description=self.tr("Layers configuration")
        )
        layersConfigSetter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.buildMergedDataWrapper.BuildMergedDataWrapper"
            }
        )
        self.addParameter(layersConfigSetter)

        self.addParameter(
            QgsProcessingParameterCrs(
                self.OUTPUT_CRS,
                self.tr("Output CRS"),
                defaultValue=QgsProject.instance().crs(),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.FIELD_NAME, self.tr("Output field name"), defaultValue="tipo"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Merged output"))
        )

    def parameterAsLayersConfig(self, parameters, name, context):
        return parameters[name]

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return "buildmergeddatawithfieldrefactor"

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr("Build Merged Data with Field Refactor")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr("Data Management Tools")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return "DSGTools - Data Management Tools"

    def tr(self, string):
        return QCoreApplication.translate(
            "BuildMergedDataWithFieldRefactorAlgorithm", string
        )

    def createInstance(self):
        return BuildMergedDataWithFieldRefactorAlgorithm()

    def generateRandomColor(self):
        """
        Generates a random color for symbolization
        """
        return QColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def applyCategorizedStyle(self, layer, classNameField):
        """
        Applies categorized symbology to the output layer based on class_name field
        """
        if not isinstance(layer, QgsVectorLayer):
            return

        try:
            # Get unique values from class_name field
            unique_values = layer.uniqueValues(
                layer.fields().indexFromName(classNameField)
            )

            # Create categories
            categories = []
            for value in unique_values:
                # Create symbol based on geometry type
                if layer.geometryType() == QgsWkbTypes.PointGeometry:
                    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
                elif layer.geometryType() == QgsWkbTypes.LineGeometry:
                    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
                else:  # Polygon
                    symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)

                # Set random color
                color = self.generateRandomColor()
                symbol.setColor(color)

                # Create category
                category = QgsRendererCategory(value, symbol, str(value))
                categories.append(category)

            # Create and apply categorized renderer
            renderer = QgsCategorizedSymbolRenderer(classNameField, categories)
            layer.setRenderer(renderer)
            layer.triggerRepaint()

        except Exception as e:
            # If styling fails, continue without styling
            pass

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layersConfig = self.parameterAsLayersConfig(
            parameters, self.LAYERS_CONFIG, context
        )
        outputCrs = self.parameterAsCrs(parameters, self.OUTPUT_CRS, context)
        fieldName = self.parameterAsString(parameters, self.FIELD_NAME, context)

        if not layersConfig:
            raise QgsProcessingException(self.tr("No layers configuration provided"))

        if not fieldName:
            fieldName = "tipo"

        algRunner = AlgRunner()
        processedLayers = []

        feedback.setProgressText(self.tr("Processing individual layers..."))
        proj = QgsProject.instance()

        for i, config in enumerate(layersConfig):
            if feedback.isCanceled():
                break

            layerName = config.get("layer")
            layer = proj.mapLayersByName(layerName)[0] if layerName else None
            expression = config.get("expression", "").strip()
            classIndex = config.get("classIndex", 0)
            className = config.get("className", "").strip()

            if not layer:
                continue

            feedback.setProgress(int((i / len(layersConfig)) * 70))
            feedback.setProgressText(
                self.tr(f"Processing layer {i+1} of {len(layersConfig)}...")
            )

            currentLayer = layer

            # Apply filter if expression is provided
            if expression:
                feedback.setProgressText(
                    self.tr(f"Applying filter to layer {layer.name()}...")
                )
                try:
                    currentLayer = algRunner.runFilterExpression(
                        inputLyr=layer,
                        expression=expression,
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=True,
                    )
                except Exception as e:
                    feedback.pushWarning(
                        self.tr(
                            f"Failed to apply filter to layer {layer.name()}: {str(e)}"
                        )
                    )
                    continue

            # Add class index field
            feedback.setProgressText(self.tr(f"Adding field '{fieldName}' to layer..."))
            try:
                layerWithField = algRunner.runCreateFieldWithExpression(
                    inputLyr=currentLayer,
                    expression=str(classIndex),
                    fieldName=fieldName,
                    context=context,
                    fieldType=1,  # Integer
                    fieldLength=10,
                    fieldPrecision=0,
                    feedback=feedback,
                    is_child_algorithm=True,
                )
            except Exception as e:
                feedback.pushWarning(
                    self.tr(
                        f"Failed to add field {fieldName} to layer {layer.name()}: {str(e)}"
                    )
                )
                continue

            # Add class name field
            feedback.setProgressText(self.tr("Adding field 'class_name' to layer..."))
            try:
                finalLayer = algRunner.runCreateFieldWithExpression(
                    inputLyr=layerWithField,
                    expression=f"'{className}'",
                    fieldName="class_name",
                    context=context,
                    fieldType=2,  # String
                    fieldLength=255,
                    fieldPrecision=0,
                    feedback=feedback,
                    is_child_algorithm=True,
                )
                processedLayers.append(finalLayer)
            except Exception as e:
                feedback.pushWarning(
                    self.tr(
                        f"Failed to add class_name field to layer {layer.name()}: {str(e)}"
                    )
                )
                continue

        if not processedLayers:
            raise QgsProcessingException(
                self.tr("No layers were successfully processed")
            )

        feedback.setProgress(70)
        feedback.setProgressText(self.tr("Merging layers..."))

        # Merge all processed layers
        try:
            mergedLayer = algRunner.runMergeVectorLayers(
                inputList=processedLayers,
                context=context,
                crs=outputCrs,
                feedback=feedback,
            )
        except Exception as e:
            raise QgsProcessingException(self.tr(f"Failed to merge layers: {str(e)}"))

        feedback.setProgress(85)
        feedback.setProgressText(self.tr("Writing output..."))

        # Create output sink with all fields from merged layer
        fields = QgsFields()
        for field in mergedLayer.fields():
            if field.name() not in [fieldName, "class_name"]:
                continue
            fields.append(field)
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields, mergedLayer.wkbType(), outputCrs
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Copy features to output
        total = mergedLayer.featureCount()
        for current, feature in enumerate(mergedLayer.getFeatures()):
            if feedback.isCanceled():
                break
            newFeature = QgsFeature(fields)
            newFeature.setGeometry(feature.geometry())
            for field in fields:
                newFeature.setAttribute(field.name(), feature[field.name()])
            sink.addFeature(newFeature, QgsFeatureSink.FastInsert)
            feedback.setProgress(85 + int((current / total) * 10))

        feedback.setProgress(95)
        feedback.setProgressText(self.tr("Applying categorized style..."))

        # Apply categorized style to output layer
        try:
            outputLayer = QgsProcessingUtils.mapLayerFromString(dest_id, context)
            if outputLayer:
                self.applyCategorizedStyle(outputLayer, "class_name")
        except Exception as e:
            feedback.pushWarning(self.tr(f"Failed to apply style: {str(e)}"))

        feedback.setProgress(100)
        feedback.setProgressText(self.tr("Process completed successfully"))

        return {self.OUTPUT: dest_id}


class ParameterLayersConfigType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterLayersConfig(name)

    def metadata(self):
        return {"widget_wrapper": "BuildMergedDataWrapper.BuildMergedDataWrapper"}

    def name(self):
        return QCoreApplication.translate("Processing", "Layers Configuration")

    def id(self):
        return "layers_config_type"

    def description(self):
        return QCoreApplication.translate(
            "Processing", "Configuration for layers with class index."
        )


class ParameterLayersConfig(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterLayersConfig(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "layers_config"

    def checkValueIsAcceptable(self, value, context=None):
        return value is not None

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
