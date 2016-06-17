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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsField, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from PyQt4.QtCore import QVariant
import processing, binascii
import json

#update imports

class CloseEarthCoveragePolygonsProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
    
    def defineQueryLayer(self, delimiterList):
        '''
        Defines a query layer composed by all features from earthCoverage lines and also by frame
        '''
        #TODO: add frame
        epsg = self.abstractDb.findEPSG()
        lineLyr = QgsVectorLayer("multilinestring?crs=EPSG:%d" % epsg,"tempLine",'memory')
        for delimiter in delimiterList:
            lyr = QgsVectorLayer(self.abstractDb.getURI(delimiter, False).uri(), delimiter, "postgres")
            featureList = []
            for feat in lyr.getFeatures():
                featureList.append(feat)
            lineLyr.dataProvider().addFeatures(featureList)
        frame = QgsVectorLayer(self.abstractDb.getURI('public.aux_moldura_a', False).uri(), 'public.aux_moldura_a', "postgres")
        for feat in frame.getFeatures():
            newFeat = QgsFeature(lineLyr.pendingFields())
            newGeom = QgsGeometry.fromPolyline(feat.geometry().asMultiPolygon()[0][0])
            newFeat.setGeometry(newGeom)
            lineLyr.dataProvider().addFeatures([newFeat])
        return lineLyr
        
    def runPolygonize(self, cl, areaLyr, lineLyr):
        alg = 'qgis:polygonize'
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
    
    def relateAreasWithCentroids(self, cl, areaLyr, centroidLyr, relateDict):
        '''
        Alters a input dict that relates each area with a centroid feature list. This list might be empty.
        '''
        #after all checks, reclassifies areas
        centroidIdx = QgsSpatialIndex()
        for feat in centroidLyr.getFeatures():
            centroidIdx.insertFeature(feat)
        relateDict[cl] = dict()
        for areaFeat in areaLyr.getFeatures():
            areaId = areaFeat.id()
            relateDict[cl][areaId] = []
            bbox = areaFeat.geometry().boundingBox()
            candidates = self.getCandidates(centroidIdx, bbox)
            for candidate in candidates:
                feat = [i for i in centroidLyr.dataProvider().getFeatures(QgsFeatureRequest(candidate))][0]
                if feat.geometry().within(areaFeat.geometry()):
                    relateDict[cl][areaId].append(feat)

    def getCandidates(self, idx, bbox):
        return idx.intersects(bbox)

    def prepareReclassification(self, cl, areaLyr, centroidLyr, relateDict):
        '''
        area without centroid: destid = -1
        area with conflicted centroid: destid = 0
        '''
        destIdx = areaLyr.fieldNameIndex('destid')
        for id in relateDict[cl].keys():
            numberOfCentroids = len(relateDict[cl][id])
            if numberOfCentroids == 1 and relateDict[cl][id][0]['cl'] == cl:
                areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id][0]['featid']}})
            elif numberOfCentroids == 1 and relateDict[cl][id][0]['cl'] != cl:
                # this happens when there is only one centroid but its class is different
                continue
            elif numberOfCentroids == 0:
                areaLyr.dataProvider().changeAttributeValues({id : {destIdx:-1}})
            else:
                conflictedCentroids = []
                #first sweep: identify centroids with conflicted classes
                for feat in relateDict[cl][id]:
                    if feat['cl'] <> cl:
                        conflictedCentroids.append(feat)
                if len(conflictedCentroids) > 0:
                    f = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(id))][0]
                    if f['cl'] == cl:
                        areaLyr.dataProvider().changeAttributeValues({id:{destIdx:0}})
                else:
                #second sweep: if there are no conflicted attributes, it tests if all centroids have the same set of attributes
                    #get original centroids
                    auxLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn='centroid').uri(), relateDict[cl][id][0][0], "postgres")
                    originalFeat = [i for i in auxLyr.dataProvider().getFeatures(QgsFeatureRequest(relateDict[cl][id][0][1]))][0]
                    fieldNames = [field.name() for field in auxLyr.pendingFields()]
                    notAllowedFields = []
                    for i in fieldNames:
                        if i in ['id', 'geom', 'centroid'] or 'id_' in i:
                            notAllowedFields.append(auxLyr.fieldNameIndex(i)) 
                    attributes = originalFeat.attributes()
                    duplicated = True
                    for centr in relateDict[cl][id][1::]:
                        #compairs attributes if one set of attribute is different from another, for breaks and sets duplicates = False
                        innerLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn='centroid').uri(), centr[0], "postgres")
                        c = [i for i in innerLyr.dataProvider().getFeatures(QgsFeatureRequest(centr[1]))][0]
                        if duplicated:
                            featAttr = c.attributes()
                            for i in range(len(attributes)):
                                if i not in notAllowedFields and attributes[i] <> featAttr[i]:
                                    duplicated = False
                                    break
                        else:
                            break
                    if duplicated:
                        areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id][0]['featid']}})
    
    def reclassifyAreasWithCentroids(self, coverageClassList, areaLyr, centroidLyr, relateDict):
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
#                 deleteList.append(feat.id())
            lyr.dataProvider().changeGeometryValues(reclassDict)

    def createAuxStruct(self, epsg):
        try:
            areaLyr = QgsVectorLayer("MultiPolygon?crs=EPSG:%d" % epsg,"tempArea",'memory')
            idField = QgsField('cl',QVariant.String)
            destinationId = QgsField('destid',QVariant.Int)
            areaLyr.dataProvider().addAttributes([idField, destinationId])
            areaLyr.updateFields()
            centroidLyr = QgsVectorLayer("MultiPoint?crs=EPSG:%d" % epsg,'centroids','memory')
            classField = QgsField('cl',QVariant.String)
            idField = QgsField('featid',QVariant.Int)
            centroidLyr.dataProvider().addAttributes([classField,idField])
            centroidLyr.updateFields()
            return (areaLyr, centroidLyr)
        except Exception as e:
            raise e 
    
    def populateCentroidLyr(self, coverageClassList, centroidLyr):
        for cl in coverageClassList:
            auxCentroidLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn = 'centroid').uri(), cl, "postgres")
            newFeatList = []
            for feat in auxCentroidLyr.getFeatures():
                newFeat = QgsFeature(centroidLyr.pendingFields())
                newFeat['featid'] = feat.id()
                newFeat['cl'] = cl
                newFeat.setGeometry(feat.geometry())
                newFeatList.append(newFeat)
            centroidLyr.dataProvider().addFeatures(newFeatList)

    def raiseFlags(self, areaLyr):
        flagTupleList = []
        areasWithoutCentroids = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = 0')))]
        reclassifiedAreas = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid > 0')))]
        spatialIndex = QgsSpatialIndex()
        for feat in reclassifiedAreas:
            spatialIndex.insertFeature(feat)
        for feat in areasWithoutCentroids:
#             candidates = self.getCandidates(spatialIndex, feat.geometry().boundingBox())
#             candidateList = []
#             for f in reclassifiedAreas:
#                 if f.id() in candidates:
#                     candidateList.append(f)
            isFlag = True
#             for c in candidateList:
#                 if feat.geometry().within(c.geometry()) or feat.geometry().overlaps(c.geometry()) or c.geometry().within(feat.geometry()) or c.geometry().overlaps(feat.geometry()):
#                     if feat['cl'] <> c['cl']:
#                         isFlag = False
#                         break
 
            if isFlag:
                flagTupleList.append((feat['cl'],-1,'Area without centroid.',binascii.hexlify(feat.geometry().asWkb())))
        
        areasWithConflictedCentroids = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('destid = -1')))]
        for feat in areasWithConflictedCentroids:
            candidates = self.getCandidates(spatialIndex, feat.geometry().boundingBox())
            candidateList = []
            for f in reclassifiedAreas:
                if f.id() in candidates:
                    candidateList.append(f)
            isFlag = True
            for c in candidateList:
                if isFlag:
                    if feat.geometry().within(c.geometry()) or feat.geometry().overlaps(c.geometry()) or c.geometry().within(feat.geometry()) or c.geometry().overlaps(feat.geometry()):
                        if feat['cl'] <> c['cl']:
                            isFlag = False
                else:
                    break
            if isFlag:
#                 flagTupleList.append((feat['cl'],-1,'Area without centroid.',binascii.hexlify(feat.geometry().asWkb())))
                flagTupleList.append((feat['cl'],-1,'Area with conflicted centroid.',binascii.hexlify(feat.geometry().asWkb())))
        
        if len(flagTupleList) > 0:
            self.addFlag(flagTupleList)
            self.setStatus('Process finished with problems. Check flags.\n', 4) #Finished with flags
            QgsMessageLog.logMessage('Process finished with problems. Check flags.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        else:
            self.setStatus('There are no area building errors.\n', 1)
            QgsMessageLog.logMessage('There are no area building errors.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            #TODO: check if frame is created
            dadsWithGeom = self.abstractDb.getOrphanGeomTablesWithElements()
            earthCoverageDict = json.loads(self.abstractDb.getEarthCoverageDict())
            if len(earthCoverageDict.keys()) == 0:
                self.setStatus('Earth coverage not defined!\n', 1)
                QgsMessageLog.logMessage('Earth coverage not defined!\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return
            coverageClassList = []
            for cl in dadsWithGeom:
                if cl in earthCoverageDict.keys():
                    coverageClassList.append(cl)
            if coverageClassList.__len__() == 0:
                self.setStatus('Empty earth coverage!\n', 1) #Finished
                QgsMessageLog.logMessage('Empty earth coverage!\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)                
                return
            epsg = self.abstractDb.findEPSG()
            areaLyr, centroidLyr = self.createAuxStruct(epsg)
            self.populateCentroidLyr(coverageClassList, centroidLyr)
            relateDict = dict()
            for cl in coverageClassList:
                #must gather all lines (including frame) to close areas
                lineLyr = self.defineQueryLayer(earthCoverageDict[cl])
                #close areas from lines
                self.runPolygonize(cl, areaLyr, lineLyr)
                self.relateAreasWithCentroids(cl, areaLyr, centroidLyr, relateDict)
                self.prepareReclassification(cl, areaLyr, centroidLyr, relateDict)
            self.reclassifyAreasWithCentroids(coverageClassList, areaLyr, centroidLyr, relateDict)
            self.raiseFlags(areaLyr)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

        