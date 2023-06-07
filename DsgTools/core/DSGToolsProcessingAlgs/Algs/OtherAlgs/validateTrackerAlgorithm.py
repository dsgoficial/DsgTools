from PyQt5.QtCore import QCoreApplication, QVariant
from datetime import datetime
import concurrent.futures
import os
import re
from ...algRunner import AlgRunner
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsGeometry,
    QgsProject,
    QgsProcessingException,
    QgsCoordinateTransform,
    QgsPointXY,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
)

class ValidateTrackerAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    ELEVATION_FIELD = 'ELEVATION_FIELD'
    CREATION_FIELD = 'CREATION_FIELD'
    TRACKID_FIELD = 'TRACKID_FIELD'
    TRACKSEGID_FIELD = 'TRACKSEGID_FIELD'
    TRACKSEGPOINTID_FIELD = 'TRACKSEGPOINTID_FIELD'
    TOLERANCE = 'TOLERANCE'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input Track Layer"),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Max difference between today and tracker (days)"),
                minValue=0,
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ELEVATION_FIELD,
                self.tr('Elevation field'), 
                type=QgsProcessingParameterField.Numeric, 
                defaultValue='ele',
                parentLayerParameterName=self.INPUT,
                allowMultiple=False
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CREATION_FIELD,
                self.tr('Date and time field'), 
                type=QgsProcessingParameterField.DateTime, 
                defaultValue='time',
                parentLayerParameterName=self.INPUT,
                allowMultiple=False
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKID_FIELD,
                self.tr('Track id field'), 
                type=QgsProcessingParameterField.Numeric, 
                defaultValue='track_fid',
                parentLayerParameterName=self.INPUT,
                allowMultiple=False
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKSEGID_FIELD,
                self.tr('Track seg id field'), 
                type=QgsProcessingParameterField.Numeric, 
                defaultValue='track_seg_id',
                parentLayerParameterName=self.INPUT,
                allowMultiple=False
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.TRACKSEGPOINTID_FIELD,
                self.tr('Point seg id field'), 
                type=QgsProcessingParameterField.Numeric, 
                defaultValue='track_seg_point_id',
                parentLayerParameterName=self.INPUT,
                allowMultiple=False
            )
        )


    def validateFieldType(self, inputLyr, elevation, creation_time, trackid, tracksegid, tracksegpointid, feedback=None):
        dictExpectedType = {elevation: QVariant.Double, creation_time: QVariant.DateTime, trackid: QVariant.Int, tracksegid: QVariant.Int, tracksegpointid: QVariant.Int}
        fields = inputLyr.fields()
        dictActualType = {elevation: fields.at(fields.indexFromName(elevation)).type(), creation_time: fields.at(fields.indexFromName(creation_time)).type(), trackid: fields.at(fields.indexFromName(trackid)).type(), tracksegid: fields.at(fields.indexFromName(tracksegid)).type(), tracksegpointid: fields.at(fields.indexFromName(tracksegpointid)).type()}
        dictDiff = {}
        for key in dictExpectedType.keys():
            if not dictExpectedType[key]==dictActualType[key]:
                dictDiff[key] = self.tr(f"Expected value for {key} type was {dictExpectedType[key]} but {dictActualType[key]} was given instead")
        return dictDiff
    
    def validateDate(self, inputLyr, creation_time, toleranceDays):
        features = inputLyr.getFeatures()
        diffDaysBiggerThanTolerance = 0

        timenow  =datetime.now().timestamp()
        for feat in features:
            try:
                if str(feat[creation_time].value()) == 'NULL':
                    continue
            except AttributeError:
                pass
            diff_t = timenow - feat[creation_time].toTime_t()
            diff_d = diff_t/(3600*24)
            if abs(diff_d)>toleranceDays:
                diffDaysBiggerThanTolerance+=1
        return diffDaysBiggerThanTolerance
    
    def diffBiggerThan1Day(self, inputLyr, creation_time):
        idx=inputLyr.fields().indexFromName(creation_time)
        max = inputLyr.maximumValue(idx).toTime_t()
        min = inputLyr.minimumValue(idx).toTime_t()
        if (max-min)/(3600*24)>1:
            return True
        return False

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Starting..."))
        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        toleranceDays = self.parameterAsInt(parameters, self.TOLERANCE, context)
        elevacao = self.parameterAsFields(parameters, self.ELEVATION_FIELD, context)[0]
        creation = self.parameterAsFields(parameters, self.CREATION_FIELD, context)[0]
        trackid = self.parameterAsFields(parameters, self.TRACKID_FIELD, context)[0]
        tracksegid = self.parameterAsFields(parameters, self.TRACKSEGID_FIELD, context)[0]
        tracksegpointid = self.parameterAsFields(parameters, self.TRACKSEGPOINTID_FIELD, context)[0]
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Checking field type."))
        dictDiffFieldType = self.validateFieldType(inputLyr, elevacao, creation, trackid, tracksegid, tracksegpointid)
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Checking date (today and tracker)."))
        diffDaysBiggerThanTolerance = self.validateDate(inputLyr, creation, toleranceDays)
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo("Checking dates (tracker).")
        diffBiggerThan1Day = self.diffBiggerThan1Day(inputLyr, creation)
        errorMessage = ""
        if dictDiffFieldType:
            for message in dictDiffFieldType.values():
                errorMessage+=message+'\n'
        if diffDaysBiggerThanTolerance:
            errorMessage+=self.tr(f"{diffDaysBiggerThanTolerance} features found at least {toleranceDays}-day difference from today\n")
        if diffBiggerThan1Day:
            errorMessage+=self.tr(f"Latest date more than 24 hours after earlier date")
        if (not dictDiffFieldType) and (not diffDaysBiggerThanTolerance) and (not diffBiggerThan1Day):
            errorMessage+=self.tr("No inconsistencies found")
        multiStepFeedback.setCurrentStep(4)
        multiStepFeedback.pushInfo("Loading complete.")
       
        return {self.OUTPUT:errorMessage}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "validatetrackeralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Validate Tracker")

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
        return QCoreApplication.translate("validateTrackerAlgorithm", string)

    def createInstance(self):
        return ValidateTrackerAlgorithm()