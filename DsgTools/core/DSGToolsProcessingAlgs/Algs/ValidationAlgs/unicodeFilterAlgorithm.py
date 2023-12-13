# -*- coding: utf-8 -*-
from collections import defaultdict
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsCoordinateReferenceSystem,
    QgsProcessingParameterMultipleLayers,
    QgsFeatureRequest,
    QgsFeature,
    QgsProcessingParameterFile,
    QgsProcessingParameterVectorLayer,
    QgsProcessingMultiStepFeedback,
    QgsField,
    QgsFields,
    QgsWkbTypes,
    NULL,
)
from qgis import processing
from qgis.utils import iface
import csv
import concurrent.futures
import os


class UnicodeFilterAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYERS = "INPUT_LAYER_LIST"
    OUTPUT1 = "OUTPUT1"
    OUTPUT2 = "OUTPUT2"
    OUTPUT3 = "OUTPUT3"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                "INPUT_LAYER_LIST",
                self.tr("Selecionar camadas"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT1, self.tr("Flag - unicode não permitido (ponto)")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT2, self.tr("Flag - unicode não permitido (linha)")
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT3, self.tr("Flag - unicode não permitido (área)")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.setProgressText("Verificando unicodes...")
        layerList = self.parameterAsLayerList(parameters, "INPUT_LAYER_LIST", context)
        whitelist = self.getWhitelist(self.getCsvFilePath())
        flags = defaultdict(list)

        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)

        def checkUnicode(layer):
            featuresNotApproved = []
            for feature in layer.getFeatures():
                for attribute in feature.attributes():
                    if attribute == NULL:
                        continue
                    if not isinstance(attribute, str):
                        continue
                    for char in attribute:
                        if hex(ord(char))[2:].lower().rjust(4, "0") in whitelist:
                            continue
                        featuresNotApproved.append(feature)
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
            return layer.geometryType(), featuresNotApproved

        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count() - 1)
        futures = set()
        nSteps = len(layerList)
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        returnDict, sinkDict = self.getOutputDict(parameters, context, fields)
        if nSteps == 0:
            return returnDict
        stepSize = 100 / nSteps
        for step, layer in enumerate(layerList):
            if multiStepFeedback.isCanceled():
                break
            futures.add(pool.submit(checkUnicode, layer))
            multiStepFeedback.setProgress(step * stepSize)
        multiStepFeedback.setCurrentStep(1)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            geometryType, featList = future.result()
            flags[geometryType] += featList
            multiStepFeedback.setProgress(current * stepSize)

        multiStepFeedback.setCurrentStep(2)
        nFlags = len(flags)
        if nFlags == 0:
            return returnDict
        for current, (geometryType, flagList) in enumerate(flags.items()):
            if multiStepFeedback.isCanceled():
                return
            if len(flagList) == 0:
                continue
            for idx, feat in enumerate(flagList):
                newFeat = QgsFeature(fields)
                newFeat.setGeometry(feat.geometry())
                newFeat["id"] = idx
                sinkDict[geometryType].addFeature(newFeat, QgsFeatureSink.FastInsert)

        return returnDict

    def getOutputDict(self, parameters, context, fields):
        returnDict = dict()
        sinkDict = dict()
        point_sink, point_sink_id = self.createOutput(
            parameters, context, self.OUTPUT1, QgsWkbTypes.MultiPoint, fields
        )
        returnDict[self.OUTPUT1] = point_sink
        sinkDict[QgsWkbTypes.PointGeometry] = point_sink_id

        line_sink, line_sink_id = self.createOutput(
            parameters, context, self.OUTPUT2, QgsWkbTypes.MultiLineString, fields
        )
        returnDict[self.OUTPUT2] = line_sink
        sinkDict[QgsWkbTypes.LineGeometry] = line_sink_id

        polygon_sink, polygon_sink_id = self.createOutput(
            parameters, context, self.OUTPUT3, QgsWkbTypes.MultiPolygon, fields
        )
        returnDict[self.OUTPUT3] = polygon_sink_id
        sinkDict[QgsWkbTypes.PolygonGeometry] = polygon_sink

        return returnDict, sinkDict

    def createOutput(self, parameters, context, output, geomType, fields):
        CRSstr = iface.mapCanvas().mapSettings().destinationCrs().authid()
        CRS = QgsCoordinateReferenceSystem(CRSstr)
        # newField.append(QgsField('nome_da_camada', QVariant.String))
        (sink, newLayer) = self.parameterAsSink(
            parameters, output, context, fields, geomType, CRS
        )
        return sink, newLayer

    def getWhitelist(self, csvFilePath):
        whitelist = []
        with open(csvFilePath, newline="") as csvFile:
            table = csv.reader(csvFile, delimiter=",", quotechar='"')
            for row in table:
                whitelist.append(row[0].lower())
        return whitelist

    def getCsvFilePath(self):
        return os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__))),
            "data",
            "unicode-whitelist.csv",
        )

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return UnicodeFilterAlgorithm()

    def name(self):
        return "unicodefilter"

    def displayName(self):
        return self.tr("Identify Features With Invalid Unicode")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Attribute Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Attribute Handling"

    def shortHelpString(self):
        return self.tr(
            "O algoritmo identifica se existe algum atributo com um unicode que não está na whitelist"
        )
