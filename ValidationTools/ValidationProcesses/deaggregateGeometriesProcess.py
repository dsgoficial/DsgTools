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
        email                : borba@dsg.eb.mil.br
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
from qgis.core import QgsVectorLayer,QgsDataSourceURI, QgsMessageLog, QgsFeature, QgsFeatureRequest
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class DeaggregateGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Deaggregate Geometries')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['lyrName'], parent=self.iface.mapCanvas())
                localProgress.step()
                localProgress.step()

                allIds = lyr.allFeatureIds()
                localProgress = ProgressWidget(1, len(allIds) - 1, self.tr('Running process on ') + classAndGeom['lyrName'], parent=self.iface.mapCanvas())
                lyr.startEditing()
                provider = lyr.dataProvider()
                uri = QgsDataSourceURI(provider.dataSourceUri())
                keyColumn = uri.keyColumn()
                for feat in lyr.getFeatures():
                    geom = feat.geometry()
                    if not geom:
                        #insert deletion
                        lyr.deleteFeature(feat.id())
                        localProgress.step()
                        continue
                    if geom.geometry().partCount() > 1:
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
                        lyr.addFeatures(addList,True)
                    localProgress.step()
                localProgress.step()
            msg = self.tr('All geometries are now single parted.')
            self.setStatus(msg, 1) #Finished
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
