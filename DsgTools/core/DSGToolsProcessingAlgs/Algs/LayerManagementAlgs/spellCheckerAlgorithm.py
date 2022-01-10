import re

from PyQt5.QtCore import QCoreApplication
from qgis import core
from qgis.core import (QgsFeature, QgsField, QgsFields, QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterString,
                       QgsProcessingParameterVectorLayer, QgsWkbTypes, QgsProcessingException,)
from qgis.PyQt.Qt import QVariant

from .spellChecker.spellCheckerCtrl import SpellCheckerCtrl

class SpellCheckerAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    ATTRIBUTE_NAME = 'ATTRIBUTE_NAME'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super(SpellCheckerAlgorithm, self).__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr('Layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.ATTRIBUTE_NAME,
                description =  self.tr('Attribute name'),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Flags')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_LAYER,
            context
        )
        attributeName = self.parameterAsFile(
            parameters,
            self.ATTRIBUTE_NAME,
            context
        )
        try:
            spellchecker = SpellCheckerCtrl('pt-BR')
        except:
            raise QgsProcessingException(self.tr('Error loading spellchecker files. Please go to the DSGTools menu and run "Download external data".'))
        
        errorFieldName = '{}_erro'.format(attributeName)
        fieldRelation = core.QgsField('id', QVariant.Double)
        layer.startEditing()
        attributeIndex = self.getAttributeIndex(attributeName, layer)
        if attributeIndex < 0:
            return {self.OUTPUT: ''}
        auxLayer = core.QgsAuxiliaryStorage().createAuxiliaryLayer(fieldRelation, layer)
        vdef = core.QgsPropertyDefinition(
            errorFieldName,
            core.QgsPropertyDefinition.DataType.DataTypeString,
            "",
            "",
            ""
        )
        auxLayer.addAuxiliaryField(vdef)
        layer.setAuxiliaryLayer(auxLayer)
        idx = layer.fields().indexOf('auxiliary_storage__{}'.format(errorFieldName))
        layer.setFieldAlias(idx, errorFieldName)
        auxFields = auxLayer.fields()
        for feature in layer.getFeatures():
            if feedback.isCanceled():
                return {self.OUTPUT: ''}
            attributeValue = feature[attributeIndex]
            if not attributeValue:
                continue
            attributeValue = ''.join(e for e in attributeValue if not(e in [',', ';', '&', '.'] or e.isdigit()))
            wordlist = re.split(' |/', attributeValue)
            wordlist = [ w for w in wordlist if not w in ['-'] ]
            wrongWords = [ word for word in wordlist if not spellchecker.hasWord(word.lower())]
            if len(wrongWords) == 0:
                continue
            auxFeature = QgsFeature(auxFields)
            auxFeature['ASPK'] = feature['id']
            auxFeature['_{}'.format(errorFieldName)] = ';'.join(wrongWords)
            auxLayer.addFeature(auxFeature)
        return {self.OUTPUT: ''}

    def getAttributeIndex(self, attributeName, layer):
        for attrName, attrAlias  in list(layer.attributeAliases().items()):
            if not(attributeName in [attrName, attrAlias]):
                continue
            if layer.fields().indexOf(attrName) < 0:
                return layer.fields().indexOf(attrAlias)
            return layer.fields().indexOf(attrName) 
        return -1

    def getFlagWkbType(self):
        return QgsWkbTypes.Point

    def getFlagFields(self):
        sinkFields = QgsFields()
        sinkFields.append(QgsField('erro', QVariant.String))
        sinkFields.append(QgsField('correcao', QVariant.String))
        sinkFields.append(QgsField('outras_opcoes', QVariant.String))
        return sinkFields

    def name(self):
        return 'spellchecker'

    def displayName(self):
        return self.tr('Spell check')

    def group(self):
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('SpellCheckerAlgorithm', string)

    def createInstance(self):
        return SpellCheckerAlgorithm()
