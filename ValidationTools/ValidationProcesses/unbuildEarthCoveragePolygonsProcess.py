# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsField, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QGis
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from PyQt4.QtCore import QVariant
import processing, binascii
import json

#update imports
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class UnbuildEarthCoveragePolygonsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(UnbuildEarthCoveragePolygonsProcess,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Unbuild Earth Coverage Polygons')
        
    def cleanCentroidsAreas(self, coverageClassList):
        """
        Cleans all the previously created areas
        """
        for cl in coverageClassList:
            auxCentroidLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn = 'geom').uri(), cl, "postgres")
            featDict = dict()
            for feat in auxCentroidLyr.getFeatures():
                if feat['centroid']:
                    featDict[feat['id']] = QgsGeometry()
            auxCentroidLyr.dataProvider().changeGeometryValues(featDict)


    def getCandidates(self, idx, bbox):
        return idx.intersects(bbox)

    def prepareReclassification(self, cl, areaLyr, centroidLyr, relateDict):
        """
        area without centroid: destid = -1
        area with conflicted centroid: destid = 0
        """
        destIdx = areaLyr.fieldNameIndex('destid')
        for id in relateDict[cl].keys():
            numberOfCentroids = len(relateDict[cl][id])
            if numberOfCentroids == 1:
                if relateDict[cl][id][0]['cl'] == cl:
                    # perfect case - must be reclassified
                    areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id][0]['featid']}})
            elif numberOfCentroids == 0:
                # area without centroid - this must become a flag
                areaLyr.dataProvider().changeAttributeValues({id : {destIdx:-1000}})
            else:
                #first sweep: identify centroids with conflicted classes
                conflictedCentroids = [feat for feat in relateDict[cl][id] if feat['cl'] <> cl]
                conflictedChildCentroids = [feat['child'] for feat in relateDict[cl][id]]
                conflictedDict = dict()
                for conf in conflictedChildCentroids:
                    conflictedDict[conf] = 1
                if len(conflictedCentroids) > 0:
                    areaLyr.dataProvider().changeAttributeValues({id:{destIdx:-2000}})
                elif len(conflictedDict.keys())>1:
                    areaLyr.dataProvider().changeAttributeValues({id:{destIdx:-2000}})
                else:
                    sameClassCentroids = relateDict[cl][id]
                    #get original centroid layer
                    auxLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn='centroid').uri(), relateDict[cl][id][0][0], "postgres")
                    #get all field names
                    fieldNames = [field.name() for field in auxLyr.pendingFields()]
                    #we must not consider these fields
                    notAllowedFields = [name for name in fieldNames if (name in ['id', 'geom', 'centroid'] or 'id_' in name)]
                    #check by index is easier, therefore, this step
                    notAllowedIndexes = []
                    for notAllowedField in notAllowedFields:
                        notAllowedIndexes.append(auxLyr.fieldNameIndex(notAllowedField))
                        
                    #comparing centroid attributes
                    duplicated = True # aux variable
                    firstCentroid = [feat for feat in auxLyr.dataProvider().getFeatures(QgsFeatureRequest(relateDict[cl][id][0][1]))][0]
                    firstAttributes = firstCentroid.attributes()
                    for i in range(1, len(sameClassCentroids)):
                        centroid = [feat for feat in auxLyr.dataProvider().getFeatures(QgsFeatureRequest(sameClassCentroids[i][1]))][0]
                        attributes = centroid.attributes()
                        for j in range(len(attributes)):
                            if j not in notAllowedIndexes:
                                #in this case the attribute j is not equal, we must flag this out
                                if centroid[j] != firstCentroid[j]:
                                    duplicated = False
                                    break
                        break
                    if duplicated:
                        areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id][0]['featid']}})
                    else:
                        areaLyr.dataProvider().changeAttributeValues({id:{destIdx:-2000}})

    def createAuxStruct(self, epsg):
        """
        creates the memory area layer to store the polygonize return
        creates the memory point to store all the centroids 
        """
        try:
            areaLyr = QgsVectorLayer("MultiPolygon?crs=EPSG:%d" % epsg,"tempArea",'memory')
            idField = QgsField('cl',QVariant.String)
            destinationId = QgsField('destid',QVariant.Int)
            areaLyr.dataProvider().addAttributes([idField, destinationId])
            areaLyr.updateFields()
            centroidLyr = QgsVectorLayer("MultiPoint?crs=EPSG:%d" % epsg,'centroids','memory')
            classField = QgsField('cl',QVariant.String)
            idField = QgsField('featid',QVariant.Int)
            childField = QgsField('child',QVariant.String)
            centroidLyr.dataProvider().addAttributes([classField,idField, childField])
            centroidLyr.updateFields()
            return (areaLyr, centroidLyr)
        except Exception as e:
            raise e 

    def makeCentroid(self, lyr, centroidLyr):
        """
        Gets each polygon from lyr, calculates its centroid (inner point, not gravitational centroid) and stores it into the centroidLyr
        """
        pass

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            #TODO: check if frame is created
            
            #getting earth coverage configuration
            edgvVersion = self.abstractDb.getDatabaseVersion()
            propertyDict = self.abstractDb.getAllSettingsFromAdminDb('EarthCoverage')
            propertyName = propertyDict[edgvVersion][0]
            settingDict = json.loads(self.abstractDb.getSettingFromAdminDb('EarthCoverage', propertyName, edgvVersion))
            earthCoverageDict = settingDict['earthCoverageDict']
            self.frameLayer = settingDict['frameLayer']
            
            coverageClassList = earthCoverageDict.keys()
            if coverageClassList.__len__() == 0:
                self.setStatus(self.tr('Empty earth coverage!'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('Empty earth coverage!'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)                
                return
            
            self.cleanCentroidsAreas(coverageClassList)
            #making temp layers
            epsg = self.abstractDb.findEPSG()
            areaLyr, centroidLyr = self.createAuxStruct(epsg)
            
            #building centroid index
            self.populateCentroidLyr(coverageClassList, centroidLyr)
            centroidIdx = self.makeIndex(centroidLyr)
            
            relateDict = dict()
            for cl in coverageClassList:
                localProgress = ProgressWidget(0, 1, self.tr('Processing earth coverage on ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                #must gather all lines (including frame) to close areas
                lineLyr = self.defineQueryLayer(earthCoverageDict[cl])
                #close areas from lines
                self.runPolygonize(cl, areaLyr, lineLyr)
                self.relateAreasWithCentroids(cl, areaLyr, centroidLyr, relateDict, centroidIdx)
                # reclassifying areas
                self.prepareReclassification(cl, areaLyr, centroidLyr, relateDict)
                self.reclassifyAreasWithCentroids(coverageClassList, areaLyr, centroidLyr, relateDict)
                localProgress.step()
            self.raiseFlags(areaLyr)     
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
