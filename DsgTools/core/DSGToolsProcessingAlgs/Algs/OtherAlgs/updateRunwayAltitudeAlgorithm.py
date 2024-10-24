from typing import List
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsVectorLayer,
    QgsRasterLayer,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class UpdateRunwayAltitudeAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    ALTITUDE_FIELD = "ALTITUDE_FIELD"
    INPUT_DEM = "INPUT_DEM"
    DECIMALS = "DECIMALS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Input Layers"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.ALTITUDE_FIELD,
                self.tr("Altitude field name"),
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.DECIMALS,
                self.tr("Round to how many decimal places (-1 to not round)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=-1,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr("Input DEM"),
            )
        )

    def updateLyrs(
        self,
        inputLyrs: List[QgsVectorLayer],
        altitudeField,
        raster: QgsRasterLayer,
        decimals,
        context,
        feedback=None,
    ):
        layerIds = []
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(
                len(inputLyrs) * 2, feedback
            )
        else:
            multiStepFeedback = None
        for currentStep, original_lyr in enumerate(inputLyrs):
            if feedback is not None and feedback.isCanceled():
                break
            fields = original_lyr.fields()
            altitude = fields.indexFromName(altitudeField)
            lyr = self.algRunner.runAddAutoIncrementalField(
                inputLyr=original_lyr,
                context=context,
                feedback=multiStepFeedback,
                fieldName="AUTO",
            )
            multiStepFeedback.setCurrentStep(currentStep + 1)
            self.algRunner.runCreateSpatialIndex(
                inputLyr=lyr,
                context=context,
                feedback=multiStepFeedback,
                is_child_algorithm=True,
            )

            multiStepFeedback.setCurrentStep(currentStep + 2)

            data = {}
            for f in original_lyr.getFeatures():
                c = f.geometry().centroid().asPoint()
                value, success = raster.dataProvider().sample(c, 1)
                if decimals != -1:
                    value = round(value, decimals)
                if success:
                    data[f.id()] = {altitude: value}
            original_lyr.dataProvider().changeAttributeValues(data)
            layerIds.append(original_lyr.id())
        return layerIds

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Starting..."))
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        altitudeField = self.parameterAsString(parameters, self.ALTITUDE_FIELD, context)
        decimals = self.parameterAsInt(parameters, self.DECIMALS, context)
        raster = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        self.algRunner = AlgRunner()
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Updating field..."))
        layerIds = self.updateLyrs(
            inputLyrList, altitudeField, raster, decimals, context, multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Complete."))
        return {self.OUTPUT: layerIds}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "updaterunwayaltitudealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Update Runway Altitude")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Utils")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Utils"

    def tr(self, string):
        return QCoreApplication.translate("updateRunwayAltitudeAlgorithm", string)

    def createInstance(self):
        return UpdateRunwayAltitudeAlgorithm()
