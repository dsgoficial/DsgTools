# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import range
from qgis.core import QgsVectorLayer,QgsDataSourceUri, QgsMessageLog, QgsFeature, QgsFeatureRequest, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess


class DeaggregateGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False, withElements = True):
        """
        Constructor
        """
        super(DeaggregateGeometriesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'manipulation'
        self.processAlias = self.tr('Deaggregate Geometries')

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            for key in classesWithElem:
                self.startTimeCount()
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['lyrName'], parent=self.iface.mapCanvas())
                localProgress.step()
                localProgress.step()

                lyr.startEditing()
                provider = lyr.dataProvider()
                uri = QgsDataSourceUri(provider.dataSourceUri())
                keyColumn = uri.keyColumn()

                if self.parameters['Only Selected']:
                    featureList = lyr.selectedFeatures()
                    size = len(featureList)
                else:
                    featureList = lyr.getFeatures()
                    size = len(lyr.allFeatureIds())

                localProgress = ProgressWidget(1, size, self.tr('Running process on ') + classAndGeom['lyrName'], parent=self.iface.mapCanvas())
                for feat in featureList:
                    geom = feat.geometry()
                    if not geom:
                        #insert deletion
                        lyr.deleteFeature(feat.id())
                        localProgress.step()
                        continue
                    if geom.get().partCount() > 1:
                        parts = geom.asGeometryCollection()
                        for part in parts:
                            part.convertToMultiType()
                        addList = []
                        for i in range(1,len(parts)):
                            if parts[i]:
                                newFeat = QgsFeature(feat)
                                newFeat.setGeometry(parts[i])
                                idx = newFeat.fieldNameIndex(keyColumn)
                                newFeat.setAttribute(idx,provider.defaultValue(idx))
                                addList.append(newFeat)
                        feat.setGeometry(parts[0])
                        lyr.updateFeature(feat)
                        lyr.addFeatures(addList)
                    localProgress.step()
                self.logLayerTime(classAndGeom['lyrName'])

            msg = self.tr('All geometries are now single parted.')
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0