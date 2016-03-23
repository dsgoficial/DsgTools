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
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            explodeIdDict = self.abstractDb.getExplodeCandidates() #list only classes with elements.
            #TODO: Do something
            for cl in explodeIdDict.keys():
                uri = self.abstractDb.getURI(cl)
                layer = QgsVectorLayer(uri.uri(), cl, 'postgres')
                if not layer.isValid():
                    QgsMessageLog.logMessage("Layer %s failed to load!" % cl)
                layer.startEditing()
                for id in explodeIdDict[cl]:
                    feat = layer.getFeatures(QgsFeatureRequest(id)).next()
                    count = 1
                    for part in feat.geometry().asGeometryCollection():
                        if count == 1:
                            feat.setGeometry(part)
                            layer.updateFeature(feat)
                        else:
                            newFeat = QgsFeature(feat)
                            newFeat.setGeometry(part)
                            layer.addFeature(newFeat)
                        count += 1
                layer.commitChanges()
            self.setStatus('All geometries are now single parted.\n', 1) #Finished
            QgsMessageLog.logMessage('All features are valid.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return
