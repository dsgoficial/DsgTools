from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterString,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterRasterLayer,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class UpdateRunwayAltitudeAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    ALTITUDE_FIELD = 'ALTITUDE_FIELD'
    INPUT_DEM = 'INPUT_DEM'
    OUTPUT = 'OUTPUT'

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
                self.tr('Altitude field name'),
                defaultValue='altitude'
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr("Input DEM"),
            )
        )
    
    def updateLyrs(self, inputLyrs, altitudeField, raster, context, feedback=None):
        layerIds = []
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(
                len(inputLyrs)*2, feedback
            )
        else:
            multiStepFeedback = None
        for currentStep, original_lyr in enumerate(inputLyrs):
            if feedback is not None and feedback.isCanceled():
                break
            fields = original_lyr.fields()
            altitude = fields.indexFromName(altitudeField)
            orig_lyr = self.algRunner.runAddAutoIncrementalField(
            inputLyr=original_lyr,
            context=context,
            feedback=multiStepFeedback,
            fieldName="AUTO",
        )
            multiStepFeedback.setCurrentStep(currentStep+1)
            self.algRunner.runCreateSpatialIndex(
                inputLyr=orig_lyr,
                context=context,
                feedback=multiStepFeedback,
            )

            multiStepFeedback.setCurrentStep(currentStep+2)
            lyr = self.algRunner.runJoinAttributesByLocation(
                inputLyr=orig_lyr,
                joinLyr=orig_lyr,
                context=context,
                feedback=multiStepFeedback,
            )
            data={}
            for f in lyr.getFeatures():
                c = f.geometry().centroid().asPoint()
                value, success = raster.dataProvider().sample(c, 1)
                if success:
                    data[f.id()]={altitude:value}
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
        raster = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        self.algRunner = AlgRunner()
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Updating field..."))
        layerIds = self.updateLyrs(inputLyrList, altitudeField, raster, context, multiStepFeedback)
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Complete."))
        return {self.OUTPUT:layerIds}

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
        return QCoreApplication.translate("updateRunwayAltitudeAlgorithm", string)

    def createInstance(self):
        return UpdateRunwayAltitudeAlgorithm()