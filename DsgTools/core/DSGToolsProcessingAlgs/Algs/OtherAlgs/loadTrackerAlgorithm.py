# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-13
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

import re
from datetime import datetime

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)

from ...algRunner import AlgRunner


class LoadTrackerAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    OUTPUT_DB = "OUTPUT_DB"
    FIELD_MAP = "FIELD_MAP"
    ELEVATION_FIELD = "ELEVATION_FIELD"
    CREATION_FIELD = "CREATION_FIELD"
    TRACKID_FIELD = "TRACKID_FIELD"
    TRACKSEGID_FIELD = "TRACKSEGID_FIELD"
    TRACKSEGPOINTID_FIELD = "TRACKSEGPOINTID_FIELD"
    OPERATOR = "OPERATOR"
    PLATE = "PLATE"
    DATE = "DATE"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Track Layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ELEVATION_FIELD,
                self.tr("Elevation field"),
                type=QgsProcessingParameterField.Numeric,
                defaultValue="ele",
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CREATION_FIELD,
                self.tr("Date and time field"),
                type=QgsProcessingParameterField.DateTime,
                defaultValue="time",
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKID_FIELD,
                self.tr("Track id field"),
                type=QgsProcessingParameterField.Numeric,
                defaultValue="track_fid",
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKSEGID_FIELD,
                self.tr("Track seg id field"),
                type=QgsProcessingParameterField.Numeric,
                defaultValue="track_seg_id",
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKSEGPOINTID_FIELD,
                self.tr("Point seg id field"),
                type=QgsProcessingParameterField.Numeric,
                defaultValue="track_seg_point_id",
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
            )
        )

        todaydate = ValidationDate(
            self.DATE,
            description=self.tr("Current time and data(hh:mm YYYY-MM-DD);"),
            defaultValue=str(datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        self.addParameter(todaydate)

        operator = ValidationString(self.OPERATOR, description=self.tr("Operator name"))
        self.addParameter(operator)

        plate = ValidationPlate(self.PLATE, description=self.tr("License plate"))
        self.addParameter(plate)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OUTPUT_DB,
                self.tr("Output database Layer"),
                [QgsProcessing.TypeVectorPoint],
                defaultValue="aux_track_p",
            )
        )

    def makeFieldMap(
        self,
        operator: str,
        elevation,
        creation_time,
        trackid,
        tracksegid,
        tracksegpointid,
        todaydate,
        plate: str,
    ):
        fieldmap = [
            {
                "expression": "",
                "length": -1,
                "name": "id",
                "precision": 0,
                "sub_type": 0,
                "type": 10,
                "type_name": "text",
            },
            {
                "expression": f"'{operator}'",
                "length": -1,
                "name": "operador",
                "precision": 0,
                "sub_type": 0,
                "type": 10,
                "type_name": "text",
            },
            {
                "expression": f'to_date("{creation_time}")',
                "length": -1,
                "name": "data_track",
                "precision": 0,
                "sub_type": 0,
                "type": 14,
                "type_name": "date",
            },
            {
                "expression": "$x",
                "length": -1,
                "name": "x_ll",
                "precision": 0,
                "sub_type": 0,
                "type": 6,
                "type_name": "double precision",
            },
            {
                "expression": "$y",
                "length": -1,
                "name": "y_ll",
                "precision": 0,
                "sub_type": 0,
                "type": 6,
                "type_name": "double precision",
            },
            {
                "expression": f'"{trackid}"',
                "length": -1,
                "name": "track_id",
                "precision": 0,
                "sub_type": 0,
                "type": 10,
                "type_name": "text",
            },
            {
                "expression": f'"{tracksegid}"',
                "length": -1,
                "name": "track_segment",
                "precision": 0,
                "sub_type": 0,
                "type": 2,
                "type_name": "integer",
            },
            {
                "expression": f'"{tracksegpointid}"',
                "length": -1,
                "name": "track_segment_point_index",
                "precision": 0,
                "sub_type": 0,
                "type": 2,
                "type_name": "integer",
            },
            {
                "expression": f'"{elevation}"',
                "length": -1,
                "name": "elevation",
                "precision": 0,
                "sub_type": 0,
                "type": 6,
                "type_name": "double precision",
            },
            {
                "expression": f'"{creation_time}"',
                "length": -1,
                "name": "creation_time",
                "precision": 0,
                "sub_type": 0,
                "type": 16,
                "type_name": "datetime",
            },
            {
                "expression": f"to_datetime('{todaydate}')",
                "length": -1,
                "name": "data_importacao",
                "precision": 0,
                "sub_type": 0,
                "type": 16,
                "type_name": "datetime",
            },
            {
                "expression": f"'{plate}'",
                "length": -1,
                "name": "vtr",
                "precision": 0,
                "sub_type": 0,
                "type": 10,
                "type_name": "text",
            },
        ]
        return fieldmap

    def addFeatureAsPoint(self, inputLyr, outputLyr, feedback=None, targetCrs=None):
        features = inputLyr.getFeatures()
        outputLyr.beginEditCommand("Add features")
        total = 100.0 / inputLyr.featureCount() if inputLyr.featureCount() else 0
        inputCrs = inputLyr.crs()
        if targetCrs is not None:
            transform = QgsCoordinateTransform(
                inputCrs, targetCrs, QgsProject.instance()
            )
        outputDataProvider = outputLyr.dataProvider()
        featSet = set()
        for current, feat in enumerate(features):
            if feedback is not None and feedback.isCanceled():
                break
            outputfeature = QgsFeature()
            geom = feat.geometry()
            pointinput = geom.asPoint()
            point = QgsGeometry.fromPointXY(QgsPointXY(pointinput.x(), pointinput.y()))
            if targetCrs is not None:
                point.transform(transform)
            outputfeature.setGeometry(point)
            outputfeature.setAttributes(feat.attributes())
            featSet.add(outputfeature)
            if feedback is not None:
                feedback.setProgress(current * total)
        outputDataProvider.addFeatures(list(featSet))
        outputLyr.endEditCommand()

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Starting..."))
        algRunner = AlgRunner()
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        outputLyr = self.parameterAsVectorLayer(parameters, self.OUTPUT_DB, context)
        if outputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.OUTPUT_DB)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        operator = self.parameterAsString(parameters, self.OPERATOR, context)
        todaydate = self.parameterAsString(parameters, self.DATE, context)
        plate = self.parameterAsString(parameters, self.PLATE, context).upper()
        elevacao = self.parameterAsFields(parameters, self.ELEVATION_FIELD, context)[0]
        creation = self.parameterAsFields(parameters, self.CREATION_FIELD, context)[0]
        trackid = self.parameterAsFields(parameters, self.TRACKID_FIELD, context)[0]
        tracksegid = self.parameterAsFields(parameters, self.TRACKSEGID_FIELD, context)[
            0
        ]
        tracksegpointid = self.parameterAsFields(
            parameters, self.TRACKSEGPOINTID_FIELD, context
        )[0]
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Building FieldMap."))
        fieldmap = self.makeFieldMap(
            operator,
            elevacao,
            creation,
            trackid,
            tracksegid,
            tracksegpointid,
            todaydate,
            plate,
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Assinging fields."))
        tempLyr = algRunner.runRefactorFields(
            inputLayer=inputLyr,
            fieldmap=fieldmap,
            context=context,
            feedback=multiStepFeedback,
            onlySelected=onlySelected,
        )
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo("Updating database.")

        outputLyr.startEditing()
        self.addFeatureAsPoint(
            tempLyr, outputLyr, feedback=multiStepFeedback, targetCrs=outputLyr.crs()
        )
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo("Loading complete.")

        return {self.OUTPUT_DB: outputLyr}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "loadtrackeralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Load Tracker")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Other Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Other Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("LoadTrackerAlgorithm", string)

    def createInstance(self):
        return LoadTrackerAlgorithm()


class ValidationString(QgsProcessingParameterString):
    """
    Auxiliary class for pre validation on name.
    """

    # __init__ not necessary

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$", value):
            return True


class ValidationPlate(QgsProcessingParameterString):
    """
    Auxiliary class for pre validation on plate.
    """

    # __init__ not necessary

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def checkValueIsAcceptable(self, value, context=None):
        if re.match(r"([a-zA-Z]{3}-?\d[a-zA-Z0-9]\d{2})(?:$)", value):
            return True


class ValidationDate(QgsProcessingParameterString):
    """
    Auxiliary class for pre validation on dates.
    """

    # __init__ not necessary

    def __init__(self, name, description="", defaultValue=None):
        super().__init__(name, description, defaultValue)

    def checkValueIsAcceptable(self, value, context=None):
        if re.match(
            r"20\d\d-(?:0[1-9]|1[0-2])-(?:[0-2]\d|3[01]) (?:[01]\d|2[0-3]):[0-5]\d",
            value,
        ):
            return True
