from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsDataSourceUri,
    QgsRasterLayer,
    QgsProcessingParameterMultipleLayers,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

from qgis.PyQt.QtWidgets import (
    QLineEdit
)

from processing.gui.wrappers import WidgetWrapper

class UpdateRunwayAltitudeAlgorithm(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    SERVER_IP = 'SERVER_IP'
    PORT = 'PORT'
    DB_NAME = 'DB_NAME'
    SCHEMA_NAME = 'SCHEMA_NAME'
    TABLE_NAME = 'TABLE_NAME'
    USER = 'USER'
    PASSWORD = 'PASSWORD'
    GEOMETRY_COLUMN = 'GEOMETRY_COLUMN'
    INPUT_LAYERS = 'INPUT_LAYERS'
    ALTITUDE_FIELD = 'ALTITUDE_FIELD'

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
            QgsProcessingParameterString(
                self.SERVER_IP,
                self.tr('Server Address')
            )
        )
        

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PORT,
                self.tr('Port')
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.DB_NAME,
                self.tr('Database name'),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.SCHEMA_NAME,
                self.tr('Schema name'),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.TABLE_NAME,
                self.tr('Table name'),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GEOMETRY_COLUMN,
                self.tr('Geometry column name'),
                defaultValue='rast'
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.USER,
                self.tr('User'),
            )
        )

        password = QgsProcessingParameterString(
            self.PASSWORD,
            self.tr('Password'),
        )
        password.setMetadata({
            'widget_wrapper':{'class':PasswordWrapper}
        })
        self.addParameter(password)
    
    def updateLyrs(self, inputLyrs, altitudeField, raster, context, feedback=None):
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

            

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("Starting..."))
        server_ip = self.parameterAsString(parameters, self.SERVER_IP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        db_name = self.parameterAsString(parameters, self.DB_NAME, context)
        schema_name = self.parameterAsString(parameters, self.SCHEMA_NAME, context)
        table_name = self.parameterAsString(parameters, self.TABLE_NAME, context)
        geometry_column = self.parameterAsString(parameters, self.GEOMETRY_COLUMN, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        altitudeField = self.parameterAsString(parameters, self.ALTITUDE_FIELD, context)
        self.algRunner = AlgRunner()
        uriRaster = QgsDataSourceUri()
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Connecting..."))
        uriRaster.setConnection(server_ip, str(port), db_name, user, password, sslmode=QgsDataSourceUri.SslDisable)
        uriRaster.setDataSource(schema_name, table_name, geometry_column)
        raster = QgsRasterLayer(uriRaster.uri(), providerType="postgresraster")
        multiStepFeedback.setCurrentStep(2)
        multiStepFeedback.pushInfo(self.tr("Updating field..."))
        self.updateLyrs(inputLyrList, altitudeField, raster, context, multiStepFeedback)
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr("Complete."))
        errorMessage = ""
        return {self.OUTPUT:errorMessage}

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
    
class PasswordWrapper(WidgetWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = args[0]

    def createWidget(self):
        self._lineEdit = QLineEdit()
        self._lineEdit.setEchoMode(QLineEdit.Password)
        return self._lineEdit

    def value(self):
        return self._lineEdit.text()