# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-07-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QColor, QFont
from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsProject,
    QgsWkbTypes,
    QgsGeometry,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsExpression,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterType,
    QgsProcessingParameterDefinition,
)
from qgis.PyQt.QtWidgets import QMessageBox

from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class IdentifyCloseFeaturesAlgorithm(ValidationAlgorithm):
    """
    Algorithm for applying user-defined attribute rules to
    verify the filling of database attributes.
    """

    DISTANCE_BETWEEN_LAYERS = "DISTANCE_BETWEEN_LAYERS"
    SELECTED = "SELECTED"
    FLAGS = "FLAGS"

    # def __init__(self):
    #     """
    #     Constructor.
    #     """
    #     super().__init__()
    #     self.valAlg = ValidationAlgorithm()
    #     self.flagFields = self.valAlg.getFlagFields()
    #     self.font = QFont()
    #     self.font.setBold(True)
    #     self.conditionalStyle = QgsConditionalStyle()

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        minimumDistanceParameter = ParameterDistanceBetweenLayers(
            self.DISTANCE_BETWEEN_LAYERS,
            description=self.tr("Minimum distance between layers"),
        )
        minimumDistanceParameter.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.distanceBetweenLayersWrapper.DistanceBetweenLayersWrapper"
            }
        )
        self.addParameter(minimumDistanceParameter)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.FLAGS, self.tr("Flags"))
        )

    def parameterAsMinimumDistanceBetweenLayers(self, parameters, name, context):
        """
        Adds data from wrapper to algorithm parameters.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters;
        :param name: parameter Name;
        :param context: (QgsProcessingContext) context in which
            processing was run;
        :return: (dict) parameters dictionary.
        """
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        :param parameters: (QgsProcessingParameter) a set of algorithm
            parameters.
        :param context: (QgsProcessingContext) context in which
            processing was run.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        :return: (dict) filled flag layers.
        """

        minimumDistances = self.parameterAsMinimumDistanceBetweenLayers(
            parameters, self.DISTANCE_BETWEEN_LAYERS, context
        )
        self.prepareFlagSink(parameters, None, QgsWkbTypes.MultiLineString, context)
        if not minimumDistances:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.DISTANCE_BETWEEN_LAYERS)
            )
        algRunner = AlgRunner()
        layersList = [] 
        for row in minimumDistances:
            distance = row['distance']
            layerApre = row['layerA']
            layerA = algRunner.runCreateFieldWithExpression(
                layerApre,
                expression="$id",
                fieldName="feat_id",
                context=context
            )
            algRunner.runCreateSpatialIndex(
                inputLyr=layerA,
                context=context
            )
            layerAbuffered = algRunner.runBuffer(
                inputLayer=layerA,
                distance = distance,
                context=context,
            )
            algRunner.runCreateSpatialIndex(
                inputLyr=layerAbuffered,
                context=context
            )
            layerBpre = row['layerB']
            layerB = algRunner.runCreateFieldWithExpression(
                layerBpre,
                expression="$id",
                fieldName="feat_id",
                context=context
            )
            algRunner.runCreateSpatialIndex(
                inputLyr=layerB,
                context=context
            )
            layersList.append([layerAbuffered, layerA, layerB, distance])
        for layers in layersList:
            layerAbuffered, layerA, layerB, distance = layers
            joinedLayer = algRunner.runJoinAttributesByLocation(
                inputLyr=layerAbuffered,
                joinLyr=layerB,
                context=context,
                predicateList=[0]
            )
            for feat in joinedLayer.getFeatures():
                expression = QgsExpression(f'"feat_id"={feat["feat_id"]}')
                request = QgsFeatureRequest(expression)
                featA = next(layerA.getFeatures(request))
                pointA = featA.geometry().asPoint()
                expression = QgsExpression(f'"feat_id"={feat["feat_id_2"]}')
                request = QgsFeatureRequest(expression)
                featB = next(layerB.getFeatures(request))
                pointB = featB.geometry().asPoint()
                geom = QgsGeometry().fromPolylineXY([pointA, pointB])
                flagText = f'distance smaller than {distance}'
                self.flagFeature(geom, flagText)

        

        # onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        # crs = QgsProject.instance().crs()
        # pointFlags, ptId = self.parameterAsSink(
        #     parameters,
        #     self.POINT_FLAGS,
        #     context,
        #     self.flagFields,
        #     QgsWkbTypes.Point,
        #     crs,
        # )

        # if not pointFlags:
        #     raise QgsProcessingException(
        #         self.invalidSourceError(parameters, self.POINT_FLAGS)
        #     )

        # lineFlags, lId = self.parameterAsSink(
        #     parameters,
        #     self.LINE_FLAGS,
        #     context,
        #     self.flagFields,
        #     QgsWkbTypes.LineString,
        #     crs,
        # )

        # if not lineFlags:
        #     raise QgsProcessingException(
        #         self.invalidSourceError(parameters, self.LINE_FLAGS)
        #     )

        # polygonFlags, polId = self.parameterAsSink(
        #     parameters,
        #     self.POLYGON_FLAGS,
        #     context,
        #     self.flagFields,
        #     QgsWkbTypes.Polygon,
        #     crs,
        # )

        # if not polygonFlags:
        #     raise QgsProcessingException(
        #         self.invalidSourceError(parameters, self.POLYGON_FLAGS)
        #     )

        # failedFeatures = self.applyAttrRules(rules, onlySelected)

        # self.flagsFromFailedList(
        #     failedFeatures, pointFlags, lineFlags, polygonFlags, feedback
        # )
        return {self.FLAGS: self.flag_id}

    def applyAttrRules(self, attrRulesMap, onlySelected):
        """
        Filters a layer or a set of selected features as from conditional rules,
        and the result is added to a list in a dictionary.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param onlySelected: (boolean) indicates whether the attribute rules
            should be applied exclusively on selected features of each
            verified layer;
        :return: (dict) modified attrRulesMap with filtered features.
        """
        proj = QgsProject.instance()

        for ruleOrder, ruleParam in attrRulesMap.items():
            if onlySelected:
                lyr = proj.mapLayersByName(ruleParam["layerField"][0])[0]
                request = QgsFeatureRequest().setFilterExpression(
                    ruleParam["expression"]
                )
                selectedFeatures = lyr.getSelectedFeatures(request)
                ruleParam["features"] = [feature for feature in selectedFeatures]
            else:
                lyr = proj.mapLayersByName(ruleParam["layerField"][0])[0]
                ruleParam["features"] = [
                    feature for feature in lyr.getFeatures(ruleParam["expression"])
                ]
            self.applyConditionalStyle(
                proj.mapLayersByName(ruleParam["layerField"][0])[0], ruleParam
            )
        return attrRulesMap

    def flagsFromFailedList(self, attrRulesMap, ptLayer, lLayer, polLayer, feedback):
        """
        Creates new features from a failed conditional rules dictionary.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param ptLayer: (QgsVectorLayer) output point vector layer;
        :param lLayer: (QgsVectorLayer) output line vector layer;
        :param polLayer: (QgsVectorLayer) output polygon vector layer;
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component;
        :return: (tuple-of-QgsVectorLayer) filled flag layers.
        """
        layerMap = {
            QgsWkbTypes.PointGeometry: ptLayer,
            QgsWkbTypes.LineGeometry: lLayer,
            QgsWkbTypes.PolygonGeometry: polLayer,
        }

        for ruleParam in attrRulesMap.values():
            flagText = "{name}".format(name=ruleParam["description"])
            for flag in ruleParam["features"]:
                geom = flag.geometry()
                newFeature = QgsFeature(self.flagFields)
                newFeature["reason"] = flagText
                newFeature.setGeometry(geom)
                layerMap[geom.type()].addFeature(newFeature, QgsFeatureSink.FastInsert)
        self.logResult(attrRulesMap, feedback)
        return (ptLayer, lLayer, polLayer)

    def applyConditionalStyle(self, lyr, values):
        """
        Applies a conditional style for each wrong attribute
        in the attribute table.
        :param lyr: (QgsVectorLayer) vector layer;
        :param values: (dict) dictionary with conditional rules.
        """
        self.conditionalStyle.setRule(values["expression"])
        self.conditionalStyle.setFont(self.font)
        self.conditionalStyle.setTextColor(QColor(255, 255, 255))

        for field in lyr.fields():
            if field.name() in values["layerField"]:
                if isinstance(values["color"], (list, tuple)):
                    self.conditionalStyle.setBackgroundColor(
                        QColor(
                            values["color"][0], values["color"][1], values["color"][2]
                        )
                    )
                else:
                    self.conditionalStyle.setBackgroundColor(QColor(values["color"]))

                lyr.conditionalStyles().setFieldStyles(
                    field.name(), [self.conditionalStyle]
                )

    def logResult(self, attrRulesMap, feedback):
        """
        Creates a statistics text log from each layer and your
        respectively wrong attribute.
        :param attrRulesMap: (dict) dictionary with conditional rules;
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking
                         component.
        """
        feedback.pushInfo("{0} {1} {0}\n".format("===" * 5, self.tr("LOG START")))

        for ruleParam in attrRulesMap.values():
            if len(ruleParam["features"]) > 0:
                row = self.tr("[RULE]") + ": {0} - {1}\n{2}: {3} {4}\n".format(
                    ruleParam["layerField"][1],
                    ruleParam["errorType"],
                    ruleParam["layerField"][0],
                    len(ruleParam["features"]),
                    self.tr("features")
                    if len(ruleParam["features"]) > 1
                    else self.tr("feature"),
                )
                feedback.pushInfo(row)
            else:
                pass

        feedback.pushInfo("{0} {1} {0}\n".format("===" * 5, self.tr("LOG END")))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyclosefeaturesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Close Features")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("IdentifyCloseFeaturesAlgorithm", string)

    def createInstance(self):
        """
        Must return a new copy of your algorithm.
        """
        return IdentifyCloseFeaturesAlgorithm()


class ParameterDistanceBetweenLayersType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterDistanceBetweenLayers(name)

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.distanceBetweenLayersWrapper.DistanceBetweenLayersWrapper"
        }

    def name(self):
        return QCoreApplication.translate("Processing", self.tr("Distance Between Layers"))

    def id(self):
        return "distance_between_layers"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            self.tr("Check minimum acceptable distance between features of chosen layers."),
        )


class ParameterDistanceBetweenLayers(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterDistanceBetweenLayers(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "distance_between_layers"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
