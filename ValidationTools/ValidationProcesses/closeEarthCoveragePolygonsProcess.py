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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsField, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, QGis
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from PyQt4.QtCore import QVariant
import processing, binascii
import json

#update imports
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class CloseEarthCoveragePolygonsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Close Earth Coverage Polygons')
        
    def preProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Snap Lines to Frame')
        
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
    
    def processFlags(self, areaLyr):
        """
        Gets flags candidates and filters those who are within other flags
        areaLayers: list of layers with possible flags
        """
        
        feats = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = -1000 or destid = -2000')))]
        idx = QgsSpatialIndex()
        updateDict = dict()
        destIdx = areaLyr.fieldNameIndex('destid')
        for feat1 in feats:
            for feat2 in feats:
                if feat2['destid'] <> -1000:
                    continue 
                if feat1.id() <> feat2.id() and not feat1.geometry().equals(feat2.geometry()):
                    combine = feat1.geometry().combine(feat2.geometry())
                    if feat2.geometry().equals(combine):
                        updateDict[feat2.id()] = {destIdx:None}
        areaLyr.dataProvider().changeAttributeValues(updateDict)
        pass
        
    def defineQueryLayer(self, delimiterList):
        """
        Defines a query layer composed by all features from earthCoverage lines and also by frame
        """
        epsg = self.abstractDb.findEPSG()
        
        # temp layer
        lineLyr = QgsVectorLayer("multilinestring?crs=EPSG:%d" % epsg,"tempLine",'memory')
        for delimiter in delimiterList:
            # loading/getting each line layer
            lyr = self.loadLayerBeforeValidationProcess(delimiter)
            featureList = []
            for feat in lyr.getFeatures():
                featureList.append(feat)
            lineLyr.dataProvider().addFeatures(featureList)

        # loading/getting the frame layer
        frame = self.loadLayerBeforeValidationProcess(self.frameLayer)
        for feat in frame.getFeatures():
            newFeat = QgsFeature(lineLyr.pendingFields())
            newGeom = QgsGeometry.fromPolyline(feat.geometry().asMultiPolygon()[0][0])
            newFeat.setGeometry(newGeom)
            lineLyr.dataProvider().addFeatures([newFeat])
        return lineLyr
        
    def runPolygonize(self, cl, areaLyr, lineLyr):
        """
        runs polygonize to generate coverage areas.
        store the polygonize return in the memory area layer with the following attributes:
        cl - original area class
        """
        QgsMapLayerRegistry.instance().addMapLayer(lineLyr)
        ret = processing.runalg('qgis:polygonize', lineLyr, False, True, None)
        if not ret:
            raise Exception(self.tr('Problem executing qgis:polygonize. Check your installed libs.\n'))
        #updating original layer
        outputLayer = processing.getObject(ret['OUTPUT'])
        addList = []
        for feat in outputLayer.getFeatures():
            newFeat = QgsFeature(areaLyr.pendingFields())
            newFeat['cl'] = cl
            area = feat.geometry()
            area.convertToMultiType()
            newFeat.setGeometry(area)
            addList.append(newFeat)
        areaLyr.dataProvider().addFeatures(addList)
        #removing from registry
        QgsMapLayerRegistry.instance().removeMapLayer(lineLyr.id())
        
    def raiseFlags(self, areaLyr):
        """
        run difference to determine holes in the coverage
        """
        frame = self.loadLayerBeforeValidationProcess(self.frameLayer)
        frameFeat = frame.getFeatures().next()
        
        #getting all geometries
        geoms = [i.geometryAndOwnership() for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid >= 0')))]
        
        #combining them
        combined = geoms[0]
        for geom in geoms:
            combined = combined.combine(geom)
        
        #getting earth coverage hole
        hole = frameFeat.geometry().difference(combined)
        hole = hole.buffer(0.1, 5)
        
        #making the flags
        flagTupleList = []
        areasWithConflictedCentroids = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = -2000')))]
        for feat in areasWithConflictedCentroids:
            if feat.geometry().within(hole):
                #After detecting that feat is indeed a flag (area with conflicted centroids), combines it with the rest of earth coverage
                combined = combined.combine(feat.geometry())
                flagTupleList.append((feat['cl'], -1, self.tr('Area with conflicted centroid.'), binascii.hexlify(feat.geometry().asWkb()), 'geom'))
        
        destIdx = areaLyr.fieldNameIndex('destid')
        notFlagDict = dict()
        
        #create a buffer to check which flags are within, if they are, these are not flags 
        earthCoveragePolygonsAndAreasWithoutCentroid = combined.buffer(0.1,5)
        for feat in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = -1000'))):
            if feat.geometry().within(earthCoveragePolygonsAndAreasWithoutCentroid):
                notFlagDict[feat.id()] = {destIdx:None}
        areaLyr.dataProvider().changeAttributeValues(notFlagDict)
        areasWithoutCentroids = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = -1000')))]
        for feat in areasWithoutCentroids:
                flagTupleList.append((feat['cl'], -1, self.tr('Area without centroid.'), binascii.hexlify(feat.geometry().asWkb()), 'geom'))
        #finishing the raise flags step
        if len(flagTupleList) > 0:
            self.addFlag(flagTupleList)
            msg = self.tr('Process finished with problems. Check flags.')
            self.setStatus(msg, 4) #Finished with flags
        else:
            msg = self.tr('There are no area building errors.')
            self.setStatus(msg, 1)     
    
    def relateAreasWithCentroids(self, cl, areaLyr, centroidLyr, relateDict, centroidIdx):
        """
        Alters a input dict that relates each area with a centroid feature list. This list might be empty.
        """
        relateDict[cl] = dict()
        for areaFeat in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("cl = '%s'" % cl))):
            areaId = areaFeat.id()
            relateDict[cl][areaId] = []
            bbox = areaFeat.geometry().boundingBox()
            candidates = self.getCandidates(centroidIdx, bbox)
            for candidate in candidates:
                feat = [i for i in centroidLyr.dataProvider().getFeatures(QgsFeatureRequest(candidate))][0]
                if feat.geometry().within(areaFeat.geometry()):
                    relateDict[cl][areaId].append(feat)

    def makeIndex(self, centroidLyr):
        """
        creates a spatial index for the centroid layer
        """
        centroidIdx = QgsSpatialIndex()
        for feat in centroidLyr.getFeatures():
            centroidIdx.insertFeature(feat)
        return centroidIdx

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
    
    def reclassifyAreasWithCentroids(self, coverageClassList, areaLyr, centroidLyr, relateDict):
        """
        Reclassifies areas with centroids
        """
        lyrDict = dict()
        for cl in coverageClassList:
            lyr = QgsVectorLayer(self.abstractDb.getURI(cl, False).uri(), cl, "postgres")
            classFeats = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("cl = '%s'" % cl)))]
            reclassFeats = []
            for i in classFeats:
                if i['destid'] > 0:
                    reclassFeats.append(i)
            reclassDict = dict()
            deleteList = []
            for feat in reclassFeats:
                reclassDict[feat['destid']]=feat.geometry()
            lyr.dataProvider().changeGeometryValues(reclassDict)

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
    
    def populateCentroidLyr(self, coverageClassList, centroidLyr):
        """
        stores all the centroids defined in the earth covarage
        in a memory point layer with the following attributes:
        featid - centroid feature id
        cl - centroid original class name
        """
        for cl in coverageClassList:
            auxCentroidLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn = 'centroid').uri(), cl, "postgres")
            newFeatList = []
            for feat in auxCentroidLyr.getFeatures():
                newFeat = QgsFeature(centroidLyr.pendingFields())
                newFeat['featid'] = feat.id()
                newFeat['cl'] = cl
                newFeat['child'] = self.abstractDb.getWhoAmI(cl,feat.id()) 
                if feat.geometry():
                    newFeat.setGeometry(feat.geometry())
                    newFeatList.append(newFeat)
            centroidLyr.dataProvider().addFeatures(newFeatList)

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
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
            self.endTimeCount()    
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
