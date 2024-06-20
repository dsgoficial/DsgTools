# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-08-18
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                : matheus.silva@ime.eb.br
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

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QVariant
from processing.gui.wrappers import WidgetWrapper
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterString,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsFields,
    QgsProcessingParameterFeatureSink,
    QgsField,
    QgsProject,
    QgsWkbTypes,
)

from .validationAlgorithm import ValidationAlgorithm


class DetectChangesBetweenGroups(ValidationAlgorithm):
    ORIGINAL = "ORIGINAL"
    REVIEWED = "REVIEWED"
    BLACK_ATTRIBUTES = "BLACK_ATTRIBUTES"
    GROUP = "GROUP"
    POINT_FLAG = "POINT_FLAG"
    LINE_FLAG = "LINE_FLAG"
    POLYGON_FLAG = "POLYGON_FLAG"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            ParameterGroup(
                self.ORIGINAL,
                self.tr("Input group original"),
            )
        )

        self.addParameter(
            ParameterGroup(
                self.REVIEWED,
                self.tr("Input group reviewed"),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.BLACK_ATTRIBUTES,
                self.tr("Select the attributes to ignore"),
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GROUP,
                self.tr(
                    "Primary key attribute on input layers to group by (id, for example)"
                ),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAG, self.tr("{0} Point Flags").format(self.displayName())
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAG, self.tr("{0} Line Flags").format(self.displayName())
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAG,
                self.tr("{0} Polygon Flags").format(self.displayName()),
            )
        )

    def parameterAsGroup(self, parameters, name, context):
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        groupOriginal = self.parameterAsGroup(parameters, self.ORIGINAL, context)
        groupReviewed = self.parameterAsGroup(parameters, self.REVIEWED, context)
        strBlackAttributes = self.parameterAsString(
            parameters, self.BLACK_ATTRIBUTES, context
        )
        attributeGroup = self.parameterAsString(parameters, self.GROUP, context)

        if not groupOriginal or not groupReviewed:
            raise QgsProcessingException(
                "Must have a input group original and input review"
            )

        project = context.project()
        groupO = project.layerTreeRoot().findGroup(groupOriginal)
        groupR = project.layerTreeRoot().findGroup(groupReviewed)

        fields = self.fieldsFlag(attributeGroup)

        if not groupO or not groupR:
            raise QgsProcessingException(
                "Input group original and input review group not found"
            )

        dictLyrsOriginals, crs = self.dictNameLyrCrs(groupO)
        dictLyrsReviewed, crs = self.dictNameLyrCrs(groupR)

        point_flag_sink, point_flag_id = self.sinkLyr(
            parameters, self.POINT_FLAG, context, fields, QgsWkbTypes.Point, crs
        )
        line_flag_sink, line_flag_id = self.sinkLyr(
            parameters, self.LINE_FLAG, context, fields, QgsWkbTypes.LineString, crs
        )
        poly_flag_sink, poly_flag_id = self.sinkLyr(
            parameters, self.POLYGON_FLAG, context, fields, QgsWkbTypes.Polygon, crs
        )

        multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(dictLyrsOriginals), feedback
        )
        nSteps = len(dictLyrsOriginals)
        if nSteps == 0:
            return {
                self.POINT_FLAG: "",
                self.LINE_FLAG: "",
                self.POLYGON_FLAG: "",
            }

        for current, nameLyrOriginal in enumerate(dictLyrsOriginals):
            if multiStepFeedback.isCanceled():
                break
            multiStepFeedback.setCurrentStep(current)

            if nameLyrOriginal not in dictLyrsReviewed:
                raise QgsProcessingException(
                    "There is no correspondence of layers between the groups"
                )

            lyrOriginal = dictLyrsOriginals[nameLyrOriginal]
            lyrReviewed = dictLyrsReviewed[nameLyrOriginal]

            listWhiteAttributes = self.compareAttributes(
                strBlackAttributes, lyrOriginal
            )

            unchangedLyr, addedLyr, deletedLyr = algRunner.runDetectDatasetChanges(
                inputLayer=lyrOriginal,
                reviewedLayer=lyrReviewed,
                attributesList=listWhiteAttributes,
                matchComparation=0,
                context=context,
            )

            lyrPoint, lyrLine, lyrPolygon = self.typeOfLayer(addedLyr)

            # set of id feature in deleted layer
            setDelAddFeat = set()

            nStepsAddedLyr = addedLyr.featureCount()
            multiStep = QgsProcessingMultiStepFeedback(
                nStepsAddedLyr, multiStepFeedback
            )

            for current1, featureAdd in enumerate(addedLyr.getFeatures()):
                if multiStep.isCanceled():
                    break
                multiStep.setCurrentStep(current1)
                bothLyr = False
                differentAttribute = False
                differentGeometry = False
                nStepsDel = deletedLyr.featureCount()
                if nStepsDel == 0:
                    continue
                stepSize = 100 / nStepsDel
                for current2, featureDel in enumerate(deletedLyr.getFeatures()):
                    if multiStep.isCanceled():
                        break
                    if (
                        featureAdd[f"{attributeGroup}"]
                        != featureDel[f"{attributeGroup}"]
                    ):
                        continue
                    setDelAddFeat.add(featureDel[f"{attributeGroup}"])
                    flagMsg = ""
                    wktFeatAdd = self.geomWkt(featureAdd)
                    wktFeatDel = self.geomWkt(featureDel)
                    if wktFeatAdd != wktFeatDel:
                        flagMsg += "Different geometry, "
                        differentGeometry = True
                    for attribute in listWhiteAttributes:
                        if featureAdd[attribute] == featureDel[attribute]:
                            continue
                        flagMsg += f"{attribute}, "
                        differentAttribute = True
                    if not (differentAttribute or differentGeometry):
                        continue
                    flagMsg = flagMsg[: len(flagMsg) - 2] + " distinct attributes"
                    self.flagFeature(
                        nameLyrOriginal,
                        featureAdd,
                        flagMsg,
                        attributeGroup,
                        fields,
                        "Update",
                        point_flag_sink,
                        line_flag_sink,
                        poly_flag_sink,
                        lyrPoint,
                        lyrLine,
                        lyrPolygon,
                    )
                    bothLyr = True
                    multiStep.setProgress(current2 * stepSize)

                if not bothLyr:
                    self.flagFeature(
                        nameLyrOriginal,
                        featureAdd,
                        None,
                        attributeGroup,
                        fields,
                        "Added",
                        point_flag_sink,
                        line_flag_sink,
                        poly_flag_sink,
                        lyrPoint,
                        lyrLine,
                        lyrPolygon,
                    )

            for featureDel in deletedLyr.getFeatures():
                if featureDel[f"{attributeGroup}"] in setDelAddFeat:
                    continue
                self.flagFeature(
                    nameLyrOriginal,
                    featureDel,
                    None,
                    attributeGroup,
                    fields,
                    "Deleted",
                    point_flag_sink,
                    line_flag_sink,
                    poly_flag_sink,
                    lyrPoint,
                    lyrLine,
                    lyrPolygon,
                )

        return {
            self.POINT_FLAG: point_flag_id,
            self.LINE_FLAG: line_flag_id,
            self.POLYGON_FLAG: poly_flag_id,
        }

    def sinkLyr(self, parameters, flag, context, fields, wkbType, crs):
        (flag_sink, flag_id) = self.parameterAsSink(
            parameters,
            flag,
            context,
            fields,
            wkbType,
            crs,
        )
        return flag_sink, flag_id

    def geomWkt(self, feature):
        geomFeat = feature.geometry()
        wkt = geomFeat.asWkt()
        return wkt

    def flagFeature(
        self,
        nameLyr,
        feature,
        flagMsg,
        attributeGroup,
        fields,
        type_change,
        point_flag_sink,
        line_flag_sink,
        poly_flag_sink,
        lyrPoint,
        lyrLine,
        lyrPolygon,
    ):
        newFeat = QgsFeature(fields)
        geomFeatAdd = feature.geometry()
        newFeat.setGeometry(geomFeatAdd)
        newFeat[f"{attributeGroup}"] = feature[f"{attributeGroup}"]
        newFeat["name_layer"] = nameLyr
        newFeat["type_change"] = type_change
        newFeat["update"] = flagMsg
        if lyrPoint:
            point_flag_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        elif lyrLine:
            line_flag_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        elif lyrPolygon:
            poly_flag_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def fieldsFlag(self, attributeGroup):
        fields = QgsFields()
        fields.append(QgsField(f"{attributeGroup}", QVariant.String))
        fields.append(QgsField("name_layer", QVariant.String))
        fields.append(QgsField("type_change", QVariant.String))
        fields.append(QgsField("update", QVariant.String))
        return fields

    def compareAttributes(self, strBlackAttributes, lyrOriginal):
        listAttributes = list(lyrOriginal.attributeAliases())
        listBlackAttributes = strBlackAttributes.split(", ")
        listWhiteAttributes = [
            attribute
            for attribute in listAttributes
            if attribute not in listBlackAttributes
        ]
        return listWhiteAttributes

    def typeOfLayer(self, addedLyr):
        lyrPoint = addedLyr.geometryType() == QgsWkbTypes.PointGeometry
        lyrLine = addedLyr.geometryType() == QgsWkbTypes.LineGeometry
        lyrPolygon = addedLyr.geometryType() == QgsWkbTypes.PolygonGeometry
        return lyrPoint, lyrLine, lyrPolygon

    def dictNameLyrCrs(self, group):
        dictLyrs = dict()
        for layer in group.findLayers():
            lyr = layer.layer()
            dictLyrs[lyr.name()] = lyr
        crs = lyr.sourceCrs()
        return dictLyrs, crs

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "detectchangesbetweengroups"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Detect Changes Between Groups")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Dataset Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Dataset Processes"

    def tr(self, string):
        return QCoreApplication.translate("DetectChangesBetweenGroups", string)

    def createInstance(self):
        return DetectChangesBetweenGroups()


class GroupsWidgetWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(GroupsWidgetWrapper, self).__init__(*args, **kwargs)

    def getGroupNames(self):
        groupsList = [
            g.name() for g in QgsProject.instance().layerTreeRoot().findGroups()
        ]
        groupsList.insert(0, "")
        return groupsList

    def createWidget(self):
        self.widget = QtWidgets.QComboBox()
        self.widget.addItems(self.getGroupNames())
        self.widget.dialogType = self.dialogType
        return self.widget

    def parentLayerChanged(self, layer=None):
        pass

    def setLayer(self, layer):
        pass

    def setValue(self, value):
        pass

    def value(self):
        return self.widget.currentText()

    def postInitialize(self, wrappers):
        pass


class ParameterGroup(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterGroup(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "group"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.detectChangesGroupAlgorithm.GroupsWidgetWrapper"
        }

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
