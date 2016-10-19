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
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Deaggregate Geometries')

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            explodeIdDict = self.abstractDb.getExplodeCandidates() #list only classes with elements.
            if len(explodeIdDict.keys()) == 0:
                self.setStatus(self.tr('There are no multi parted geometries.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('There are no multi parted geometries.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            for cl in explodeIdDict.keys():
                #creating vector layer
                schema, layer_name = self.abstractDb.getTableSchema(cl)
                layer = self.layerLoader.load([layer_name],uniqueLoad=True)[layer_name]
                provider = layer.dataProvider()
                if not layer.isValid():
                    QgsMessageLog.logMessage(self.tr("Layer {0} failed to load!").format(cl))
                layer.startEditing()
                for id in explodeIdDict[cl]:
                    layer.startEditing()
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
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
