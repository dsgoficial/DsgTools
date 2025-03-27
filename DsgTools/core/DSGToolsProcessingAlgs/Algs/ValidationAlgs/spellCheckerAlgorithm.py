import re

from PyQt5.QtCore import QCoreApplication
from qgis import core
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsProcessingException,
)
from qgis.PyQt.Qt import QVariant

from ..LayerManagementAlgs.spellChecker.spellCheckerCtrl import SpellCheckerCtrl


class SpellCheckerAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = "INPUT_LAYER"
    ATTRIBUTE_NAME = "ATTRIBUTE_NAME"
    PRIMARY_KEY_FIELD = "PRIMARY_KEY_FIELD"
    FLAGS = "FLAGS"

    def __init__(self):
        super(SpellCheckerAlgorithm, self).__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr("Layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ATTRIBUTE_NAME,
                self.tr("Attribute name"),
                type=QgsProcessingParameterField.String,
                parentLayerParameterName=self.INPUT_LAYER,
                allowMultiple=False,
                defaultValue="nome",
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.PRIMARY_KEY_FIELD,
                self.tr("Primary key field"),
                type=QgsProcessingParameterField.Any,
                parentLayerParameterName=self.INPUT_LAYER,
                allowMultiple=False,
                defaultValue="id",
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr(f"{self.displayName()} Flags")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        attributeName = self.parameterAsFields(
            parameters, self.ATTRIBUTE_NAME, context
        )[0]
        pkField = self.parameterAsFields(parameters, self.PRIMARY_KEY_FIELD, context)[0]

        fields = QgsFields()
        fields.append(QgsField("column_name", QVariant.String))
        fields.append(QgsField("number_of_errors", QVariant.Int))
        (flagSink, flag_id) = self.parameterAsSink(
            parameters,
            self.FLAGS,
            context,
            fields,
            geometryType=QgsWkbTypes.NoGeometry,
        )
        try:
            spellchecker = SpellCheckerCtrl("pt-BR")
        except:
            raise QgsProcessingException(
                self.tr(
                    'Error loading spellchecker files. Please go to the DSGTools menu and run "Download external data".'
                )
            )

        errorFieldName = "{}_erro".format(attributeName)

        layer.startEditing()
        attributeIndex = self.getAttributeIndex(attributeName, layer)
        if attributeIndex < 0 or pkField not in [f.name() for f in layer.fields()]:
            feedback.pushWarning("Attribute index not found")
            return {self.FLAGS: flag_id}
        fieldRelation = layer.fields().field(pkField)
        auxLayer = core.QgsAuxiliaryStorage().createAuxiliaryLayer(fieldRelation, layer)
        vdef = core.QgsPropertyDefinition(
            errorFieldName,
            core.QgsPropertyDefinition.DataType.DataTypeString,
            "",
            "",
            "",
        )
        auxLayer.addAuxiliaryField(vdef)
        layer.setAuxiliaryLayer(auxLayer)
        idx = layer.fields().indexOf("auxiliary_storage__{}".format(errorFieldName))
        layer.setFieldAlias(idx, errorFieldName)
        auxFields = auxLayer.fields()
        for feature in layer.getFeatures():
            if feedback.isCanceled():
                return {self.FLAGS: flag_id}
            attributeValue = feature[attributeIndex]
            if not attributeValue:
                continue
            attributeValue = "".join(
                e
                for e in attributeValue
                if not (e in [",", ";", "&", "."] or e.isdigit())
            )
            wordlist = re.split(" |/", attributeValue)
            wordlist = [w for w in wordlist if not w in ["-"]]
            wrongWords = [
                word for word in wordlist if not spellchecker.hasWord(word.lower())
            ]
            if len(wrongWords) == 0:
                continue
            auxFeature = QgsFeature(auxFields)
            auxFeature["ASPK"] = feature[pkField]
            auxFeature["_{}".format(errorFieldName)] = ";".join(wrongWords)
            auxLayer.addFeature(auxFeature)
        feedback.pushInfo(f"Field {errorFieldName} added/edited")
        nErrors = auxLayer.featureCount()
        if nErrors == 0:
            return {self.FLAGS: flag_id}
        flagFeat = QgsFeature(fields)
        flagFeat["column_name"] = attributeName
        flagFeat["number_of_errors"] = nErrors
        flagSink.addFeature(flagFeat)

        return {self.FLAGS: flag_id}

    def getAttributeIndex(self, attributeName, layer):
        if not layer.fields().indexOf(attributeName) < 0:
            return layer.fields().indexOf(attributeName)
        for attrName, attrAlias in list(layer.attributeAliases().items()):
            if not (attributeName in [attrName, attrAlias]):
                continue
            if layer.fields().indexOf(attrName) < 0:
                return layer.fields().indexOf(attrAlias)
            return layer.fields().indexOf(attrName)
        return -1

    def getFlagWkbType(self):
        return QgsWkbTypes.Point

    def getFlagFields(self):
        sinkFields = QgsFields()
        sinkFields.append(QgsField("erro", QVariant.String))
        sinkFields.append(QgsField("correcao", QVariant.String))
        sinkFields.append(QgsField("outras_opcoes", QVariant.String))
        return sinkFields

    def name(self):
        return "spellchecker"

    def displayName(self):
        return self.tr("Spell Check")

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

    def tr(self, string):
        return QCoreApplication.translate("SpellCheckerAlgorithm", string)

    def createInstance(self):
        return SpellCheckerAlgorithm()
