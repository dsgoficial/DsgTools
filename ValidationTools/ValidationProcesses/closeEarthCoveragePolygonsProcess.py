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
import processing, binascii
import json

class CloseEarthCoveragePolygonsProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)
    
    def defineQueryLayer(self, delimiterList):
        '''
        Defines a query layer composed by all features from earthCoverage lines
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
        return lineLyr
        
    def runPolygonize(self, lineLyr):
        alg = 'qgis:polygonize'
        QgsMapLayerRegistry.instance().addMapLayer(lineLyr)
        ret = processing.runalg('qgis:polygonize', lineLyr, False, True, None)
        if not ret:
            raise Exception(self.tr('Problem executing qgis:polygonize. Check your installed libs.\n'))
        #updating original layer
        outputLayer = processing.getObject(ret['OUTPUT'])
        #removing from registry
        QgsMapLayerRegistry.instance().removeMapLayer(lineLyr.id())
        return outputLayer
    
    def relateAreasWithCentroids(self, areaLyr, centroidLyr):
        '''
        Returns a dict that relates each area with a centroid list. This list might be empty.
        '''
        #after all checks, reclassifies areas
        centroidIdx = QgsSpatialIndex()
        for feat in centroidLyr.getFeatures():
            centroidIdx.insertFeature(feat)
        relateDict = dict()
        for areaFeat in areaLyr.getFeatures():
            areaId = areaFeat.id()
            relateDict[areaId] = []
            bbox = areaFeat.geometry().boundingBox()
            candidates = self.getCentroidCandidates(centroidIdx, centroidLyr, bbox)
            for candidate in candidates:
                relateDict[areaId].append(candidate)
        return relateDict

    def getCentroidCandidates(self, idx, layer, bbox):
        return idx.intersects(bbox)

    def reclassifyAreasWithCentroids(self, areaLyr, centroidLyr, relateDict):
        flagTupleList = []
        for id in relateDict.keys():
            numberOfCentroids = len(relateDict[id])
            if numberOfCentroids == 1:
                centroidFeature = [i for i in centroidLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("id=%d"%relateDict[id][0])))][0]
                areaFeature = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(id))][0]
                centroidFeature['geom'] = binascii.hexlify(areaFeature.geometry().asWkb())
            elif numberOfCentroids == 0:
                feature = [i for i in areaLyr.dataProvider().getFeatures(QgsFeatureRequest(id))][0]
                flagTupleList.append((centroidLyr.name(),-1, self.tr('Area without centroid.'), binascii.hexlify(feature.geometry().asWkb()) ))
            else:
                idList = ','.join(map(str,relateDict[id]))
                features = [i for i in centroidLyr.dataProvider().getFeatures(QgsFeatureRequest(QgsExpression("id=%d"%relateDict[id][0])))]
                attributes = features[0].attributes()
                duplicated = True
                for i in range(1,len(features)):
                    candidateFeat = features[i]
                    if candidateFeat.attributes() != attributes:
                        flagTupleList.append( (centroidLyr.name(), candidateFeat['id'], self.tr('Area with conflicted centroids.'), binascii.hexlify(candidateFeat.geometry().asWkb()) ) )
                        duplicated = False
                if duplicated:
                    flagTupleList.append( (centroidLyr.name(), candidateFeat['id'], self.tr('Area with multiple centroids with same attributes.'), binascii.hexlify(candidateFeat.geometry().asWkb()) ) )
        return flagTupleList
        
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
            for cl in coverageClassList:
                centroidLyr = QgsVectorLayer(self.abstractDb.getURI(cl, False, geomColumn = 'centroid').uri(), cl, "postgres")
                #must gather all lines (including frame) to close areas
                lineLyr = self.defineQueryLayer(earthCoverageDict[cl])
                #close areas from lines
                areaLyr = self.runPolygonize(lineLyr)
                #relate elements
                relateDict = self.relateAreasWithCentroids(areaLyr, centroidLyr)
                #reclassify
                flagTuppleList = self.reclassifyAreasWithCentroids(areaLyr, centroidLyr, relateDict)
                
                if len(flagTuppleList) > 0:
                    numberOfProblems = self.addFlag(flagTuppleList)
                    self.setStatus('%s feature(s) of class '+cl+' with problems. Check flags.\n' % numberOfProblems, 4) #Finished with flags
                    QgsMessageLog.logMessage('%s feature(s) of class '+cl+' with problems. Check flags.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                else:
                    self.setStatus('There are no area building errors on '+cl+'.\n', 1) #Finished
                    QgsMessageLog.logMessage('There are no area building errors on '+cl+'.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return
