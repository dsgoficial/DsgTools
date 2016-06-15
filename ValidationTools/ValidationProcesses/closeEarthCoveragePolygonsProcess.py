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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex
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
            candidates = self.getCentroidCandidates(centroidIdx, bbox)
            for candidate in candidates:
                feat = [i for i in centroidLyr.dataProvider().getFeatures(QgsFeatureRequest(candidate))][0]
                if feat.geometry().within(areaFeat.geometry()):
                    relateDict[cl][areaId].append(feat)

    def getCentroidCandidates(self, idx, bbox):
        return idx.intersects(bbox)

    def prepareReclassification(self, cl, areaLyr, centroidLyr, relateDict):
        '''
        Comentar essa porra
        '''
        destIdx = areaLyr.fieldNameIndex('destid')
        for id in relateDict[cl].keys():
            numberOfCentroids = len(relateDict[cl][id])
            if numberOfCentroids == 1 and relateDict[cl][id]['cl'] == cl:
                areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id].id()}})
            elif numberOfCentroids == 0:
                areaLyr.dataProvider().changeAttributeValues({id : {destIdx:-1}})
            else:
                conflictedCentroids = []
                #first sweep: identify centroids with conflicted classes
                for feat in relateDict[cl][id]:
                    if feat['cl'] <> cl:
                        conflictedCentroids.append(feat)
                if len(conflictedCentroids) > 0:
                    changeDict = dict()
                    for c in conflictedCentroids:
                        changeDict[c.id()] = {destIdx:0}
                    areaLyr.dataProvider().changeAttributeValues(changeDict)
                else:
                #second sweep: if there are no conflicted attributes, it tests if all centroids have the same set of attributes
                    fieldNames = [field.name() for field in centroidLyr.pendingFields()]
                    notAllowedFields = []
                    for i in fieldNames:
                        if i in ['id', 'geom', 'centroid'] or 'id_' in i:
                            notAllowedFields.append(centroidLyr.fieldNameIndex(i)) 
                    attributes = relateDict[cl][id][0].attributes()
                    duplicated = True
                    for c in relateDict[cl][id][1::]:
                        #compairs attributes if one set of attribute is different from another, for breaks and sets duplicates = False
                        if duplicated:
                            featAttr = c.attributes()
                            for i in range(attributes):
                                if i not in notAllowedFields and attributes[i] <> featAttr[i]:
                                    duplicated = False
                                    break
                        else:
                            break
                    if duplicated:
                        areaLyr.dataProvider().changeAttributeValues({id : {destIdx:relateDict[cl][id][0].id()}})
    
    def reclassifyAreasWithCentroids(self, coverageClassList, areaLyr, centroidLyr, relateDict):
        lyrDict = dict()
        for cl in coverageClassList:
            lyr = QgsVectorLayer(self.abstractDb.getURI(cl, False).uri(), cl, "postgres")
            reclassFeats = areaLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression('cl = %s and destid > 0' % cl)))
            reclassDict = dict()
            deleteList = []
            for feat in reclassFeats:
                reclassDict[feat['destid']]=feat.geometry()
                deleteList.append(feat.id())
            lyr.dataProvider().changeGeometryValues(reclassDict)
            areaLyr.dataProvider().deleteFeatures(deleteList)
    
    def postProcessFlags(self, coverageClassList, areaLyr, centroidLyr):
        for cl in coverageClassList:
            centroidCheckList = []
            for i in coverageClassList:
                if i <> cl:
                    centroidCheckList.append(i)
            problemCandidates = [i for i in flags.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("process_name = '%s' and layer = '%s' and reason = '%s'" % (self.getName(), cl, self.tr('Area without centroid.')) )))]
            eraseIdList = []
            for candidate in problemCandidates:
                for centroidName in centroidCheckList:
                    lyr = QgsVectorLayer(self.abstractDb.getURI(centroidName, False).uri(), centroidName, "postgres")
                    earthCoverageAreasFeatList = [i for i in lyr.getFeatures()]
                    for c in earthCoverageAreasFeatList:
                        if c.geometry() and candidate.geometry():
                            if candidate.geometry().within(c.geometry()) or candidate.geometry().contains(c.geometry()) or candidate.geometry().overlaps(c.geometry()) or c.geometry().contains(candidate.geometry()) or c.geometry().overlaps(candidate.geometry()):
                                if candidate.id() not in eraseIdList:
                                    eraseIdList.append(candidate.id())
                            
            flags.dataProvider().deleteFeatures(eraseIdList)

    def createAuxStruct(self, epsg):
        try:
            areaLyr = QgsVectorLayer("MultiPolygon?crs=EPSG:%d" % epsg,"tempArea",'memory')
            idField = QgsField('cl',QVariant.String)
            destinationId = QgsField('destId',QVariant.Id)
            areaLyr.dataProvider().addAttributes([idField])
            areaLyr.updateFields()
            centroidLyr = QgsVectorLayer("MultiPoint?crs=EPSG:%d" % epsg,'centroids','memory')
            classField = QgsField('cl',QVariant.String)
            idField = QgsField('featid',QVariant.Int)
            centroidLyr.dataProvider().addAttributes([classField,idField])
            centroidLyr.updateFields()
            return (areaLyr, centroidLyr)
        except Exception as e:
            raise e 
    
    def createAuxCentroidLyr(self, coverageClassList):
        for cl in coverageClassList:
            auxCentroidLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn = 'centroid').uri(), cl, "postgres")
            newFeatList = []
            for feat in auxCentroidLyr.getFeatures():
                newFeat = QgsFeature(centroidLyr.pendingFields())
                newFeat['featid'] = feat.id()
                newFeat['cl'] = cl
                newFeat.setGeometry(feat.geometry())
                newFeatList.append(newFeat)
            auxCentroidLyr.dataProvider().addFeatures(newFeatList)
        return auxCentroidLyr

    def raiseFlags(self, areaLyr):
        flagTupleList = []
        areasWithoutCentroids = areaLyr.dataProvider.getFeatures(QgsFeatureRequest(QgsExpression('destid = 0')))
        for feat in areasWithoutCentroids:
            tuppleList.append((feat['cl'],-1,'Area without centroid.',binascii.hexlify(feat.geometry().asWkb())))
        areasWithConflictedCentroids = areaLyr.dataProvider.getFeatures(QgsFeatureRequest(QgsExpression('destid = -1')))
        for feat in areasWithConflictedCentroids:
            flagTupleList.append((feat['cl'],-1,'Area with conflicted centroid.',binascii.hexlify(feat.geometry().asWkb())))
        self.addFlag(flagTupleList)

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
            auxCentroidLyr = self.createAuxCentroidLyr(coverageClassList)
            relateDict = dict()
            for cl in coverageClassList:
                #must gather all lines (including frame) to close areas
                lineLyr = self.defineQueryLayer(earthCoverageDict[cl])
                #close areas from lines
                self.runPolygonize(cl, areaLyr, lineLyr)
                self.relateAreasWithCentroids(cl, areaLyr, auxCentroidLyr, relateDict)
                self.prepareReclassification(cl, areaLyr, centroidLyr, relateDict)
            self.reclassifyAreasWithCentroids(coverageClassList, areaLyr, centroidLyr, relateDict)
            self.raiseFlags(areaLyr)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return

        