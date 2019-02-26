# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean)

class DeaggregatorAlgorithm(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addOutput(QgsProcessingOutputVectorLayer(
            self.INPUT,
            self.tr('Original layer updated')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        # (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
        #         context, source.fields(), source.wkbType(), source.sourceCrs())

        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)

        target = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        target.startEditing()
        target.beginEditCommand('Updating layer')
        provider = target.dataProvider()
        uri = QgsDataSourceUri(provider.dataSourceUri())
        keyColumn = uri.keyColumn()
        destType = target.geometryType()
        destIsMulti = QgsWkbTypes.isMultiType(target.wkbType())

        # Compute the number of steps to display within the progress bar and
        # get features from source
        if onlySelected:
            total = 100.0 / target.selectedFeatureCount() if target.selectedFeatureCount() else 0
            features = target.getSelectedFeatures()
        else:
            total = 100.0 / target.featureCount() if target.featureCount() else 0
            features = target.getFeatures()            

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            geom = feature.geometry()
            if not geom:
                target.deleteFeature(feature.id())
                # Update the progress bar
                feedback.setProgress(int(current * total))
                continue
            if geom.get().partCount() > 1:
                parts = geom.asGeometryCollection()
                for part in parts:
                    if destIsMulti:
                        part.convertToMultiType()
                addList = []
                for i in range(1,len(parts)):
                    if parts[i]:
                        newFeat = QgsFeature(feature)
                        newFeat.setGeometry(parts[i])
                        idx = newFeat.fieldNameIndex(keyColumn)
                        newFeat.setAttribute(idx,provider.defaultValue(idx))
                        addList.append(newFeat)
                feature.setGeometry(parts[0])
                target.updateFeature(feature)
                target.addFeatures(addList, QgsFeatureSink.FastInsert)             

            # Update the progress bar
            feedback.setProgress(int(current * total))

        target.endEditCommand()

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: target}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'deaggregategeometries'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Deaggregate Geometries')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools (Manipulation Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools (Manipulation Processes)'

    def tr(self, string):
        return QCoreApplication.translate('DeaggregatorAlgorithm', string)

    def createInstance(self):
        return DeaggregatorAlgorithm()
