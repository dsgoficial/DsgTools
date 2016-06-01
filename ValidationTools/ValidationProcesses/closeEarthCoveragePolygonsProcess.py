# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
import processing, binascii
import json

class CloseEarthCoveragePolygonsProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
        self.parameters = {'Snap': 1.0, 'MinArea':0.001}
    
    def defineQueryLayer(self, key, earthCoverageDict):
        #Defines a query layer composed by all features from earthCoverage
        lyr = None
        return lyr
        
    def runProcessinAlg(self, key):
        alg = 'qgis:polygonize'
        
        #creating vector layer
        input = QgsVectorLayer(self.abstractDb.getURI(cl, False).uri(), cl, "postgres")
        crs = input.crs()
        epsg = self.abstractDb.findEPSG()
        crs.createFromId(epsg)
        input.setCrs(crs)
        
        #Adding to registry
        QgsMapLayerRegistry.instance().addMapLayer(input)
        
        #setting tools
        tools = 'break,rmsa,rmdangle'
        threshold = -1
        #change parameters
        ret = processing.runalg(alg, input, tools, threshold, extent, snap, minArea, None, None)

        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        #getting error flags
        errorLayer = processing.getObject(ret['error'])
        #removing from registry
        QgsMapLayerRegistry.instance().removeMapLayer(input.id())
        return self.getProcessingErrors(errorLayer)
    
    def reclassifyAreasWithCentroids(self,areaLyr):
        #after all checks, reclassifies areas
        pass

    def detectConflicts(self, areaLyr):
        #Conflicts are centroids of different set of attributes which reclassify the same area.
        #This method outputs flags with the geometry of the problem and the id of the conflict
#         numberOfProblems = self.addFlag(recordList)
        pass
    
    def detectDuplicatedCentroids(self, areaLyr):
        #returns a dict with the ids of duplicated centroids with the same set of attributes and wich reclassifies the same area
        pass
    
    def detectAreaWithoutCentroid(self, areaLyr):
        #areas
        pass
    
    def getProcessingErrors(self, layer):
        recordList = []
        for feature in layer.getFeatures():
            recordList.append((feature['id'], binascii.hexlify(feature.geometry().asWkb())))
        return recordList
        
    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithGeom = self.abstractDb.getOrphanGeomTablesWithElements()
            if classesWithGeom.__len__() == 0:
                self.setStatus('Empty database!\n', 1) #Finished
                QgsMessageLog.logMessage('Empty database!\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)                
                return
            for cl in classesWithGeom:
                if cl[-1]  in ['a']:
                    result = self.runProcessinAlg(cl)
                    if len(result) > 0:
                        recordList = []
                        for tupple in result:
                            recordList.append((cl,tupple[0],'Cleaning error.',tupple[1]))
                            self.addClassesToBeDisplayedList(cl) 
                        numberOfProblems = self.addFlag(recordList)
                        self.setStatus('%s feature(s) of class '+cl+' with cleaning errors. Check flags.\n' % numberOfProblems, 4) #Finished with flags
                        QgsMessageLog.logMessage('%s feature(s) of class '+cl+' with cleaning errors. Check flags.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                    else:
                        self.setStatus('There are no cleaning errors on '+cl+'.\n', 1) #Finished
                        QgsMessageLog.logMessage('There are no cleaning errors on '+cl+'.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return
