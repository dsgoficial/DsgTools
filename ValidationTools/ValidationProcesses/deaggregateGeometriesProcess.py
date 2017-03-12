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

class DeaggregateGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Deaggregate Geometries')
        
        # getting tables with elements
        classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, getGeometryColumn=True)
        # creating a list of tuples (layer names, geometry columns)
        classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
        # adjusting process parameters
        self.parameters = {'Classes': classesWithElem}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())

            for classAndGeom in self.parameters['Classes']:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                processTableName, lyr = self.prepareExecution(cl, geometryColumn)
                    
                # getting multi geometries ids
                multiIds = self.abstractDb.getExplodeCandidates(processTableName)

                # actual deaggregation
                provider = lyr.dataProvider()
                lyr.startEditing()
                for id in multiIds:
                    feat = layer.getFeatures(QgsFeatureRequest(id)).next()
                    parts = feat.geometry().asGeometryCollection()
                    for part in parts:
                        part.convertToMultiType()
                    addList = []
                    for i in range(1,len(parts)):
                        newFeat = QgsFeature(feat)
                        newFeat.setGeometry(parts[i])
                        idx = newFeat.fieldNameIndex('id')
                        newFeat.setAttribute(idx,provider.defaultValue(idx))
                        addList.append(newFeat)
                    feat.setGeometry(parts[0])
                    layer.updateFeature(feat)
                    layer.addFeatures(addList,True)
            msg = self.tr('All geometries are now single parted.')
            self.setStatus(msg, 1) #Finished
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
