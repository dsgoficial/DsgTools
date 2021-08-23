# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-06
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
import json

from qgis.core import (QgsEditorWidgetSetup, QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterString)
from qgis.PyQt.QtCore import QCoreApplication


class AssignValueMapToLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    VALUE_MAP_FILE = 'VALUE_MAP_FILE'
    VALUE_MAP = 'VALUE_MAP'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input Layers'),
                QgsProcessing.TypeVectorAnyGeometry
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.VALUE_MAP_FILE,
                description=self.tr('Json file with value maps'),
                defaultValue='.json'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.VALUE_MAP,
                description=self.tr('Json data'),
                multiLine=True,
                defaultValue='{}'
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Original layers with values mapped')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        inputLyrList = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )
        self.domainDict = self.loadMapFromParameters(parameters)
        listSize = len(inputLyrList)
        stepSize = 100/listSize if listSize else 0

        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            self.setDomainsAndRestrictions(lyr)
            feedback.setProgress(current * stepSize)

        return {self.OUTPUT: inputLyrList}

    def loadMapFromParameters(self, parameters):
        """
        Loads value map from json.
        :param parameters: dict with the parameters of the alg
        """
        rules_path = parameters[self.VALUE_MAP_FILE]
        rules_text = parameters[self.VALUE_MAP]
        if rules_path and rules_path != '.json':
            with open(rules_path, 'r') as f:
                rules_input = json.load(f)
        if rules_text and rules_text != '{}':
            rules_input = json.loads(rules_text)
        return rules_input

    def setDomainsAndRestrictions(self, lyr):
        """
        Adjusts the domain restriction to all attributes in the layer
        :param lyr:
        :param lyrName:
        :param domLayerDict:
        :return:
        """
        pkIdxList = lyr.primaryKeyAttributes()
        lyrName = lyr.name()
        self.multiColumnsDict = {}
        for i, field in enumerate(lyr.fields()):
            attrName = field.name()
            if attrName == 'id' or 'id_' in attrName or i in pkIdxList:
                formConfig = lyr.editFormConfig()
                formConfig.setReadOnly(i, True)
                lyr.setEditFormConfig(formConfig)
            elif lyrName in self.domainDict \
                and attrName in self.domainDict[lyrName]['columns'] \
                and 'values' in self.domainDict[lyrName]['columns'][attrName]:
                attrMetadataDict = self.domainDict[lyrName]['columns'][attrName]
                if lyrName in self.multiColumnsDict and \
                    attrName in self.multiColumnsDict[lyrName]:
                    #make filter
                    if 'constraintList' in attrMetadataDict \
                        and lyrName in self.domLayerDict \
                        and attrName in self.domLayerDict[lyrName]:
                        lyrFilter = '{0} in ({1})'.format(
                            attrMetadataDict['refPk'],
                            ','.join(
                                map(
                                    str,
                                    attrMetadataDict['constraintList']
                                )
                            )
                        )
                        editDict = {
                            'Layer': self.domLayerDict[lyrName][attrName].id(),
                            'Key': self.attrMetadataDict['refPk'],
                            'Value': self.attrMetadataDict['otherKey'],
                            'AllowMulti': True,
                            'AllowNull': self.attrMetadataDict['nullable'],
                            'FilterExpression': lyrFilter
                        }
                        widgetSetup = QgsEditorWidgetSetup(
                            'ValueRelation',
                            editDict
                        )
                        lyr.setEditorWidgetSetup(i, widgetSetup)
                else:
                    #filter value dict
                    valueDict = attrMetadataDict['values']
                    if 'constraintList' in attrMetadataDict and \
                        attrMetadataDict['constraintList'] != [] and \
                        attrMetadataDict['constraintList'] != list(valueDict.keys()):
                        valueRelationDict = {
                            v: str(k) for k, v in valueDict.items()
                            if str(k) in map(str, attrMetadataDict['constraintList'])
                        }
                    else:
                        valueRelationDict = {
                            v : str(k) for k, v in valueDict.items()
                        }
                    widgetSetup = QgsEditorWidgetSetup(
                        'ValueMap',
                        {'map':valueRelationDict}
                    )
                    lyr.setEditorWidgetSetup(i, widgetSetup)
        return lyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'assignvaluemaptolayersalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Assign Value Map to Layers')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        return QCoreApplication.translate(
            'AssignValueMapToLayersAlgorithm',
            string
        )

    def createInstance(self):
        return AssignValueMapToLayersAlgorithm()
