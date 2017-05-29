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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, QgsDataSourceURI, QgsSpatialIndex, QgsField
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from PyQt4.QtCore import QVariant
import processing, binascii

class DissolvePolygonsWithCommonAttributesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Dissolve polygons with common attributes')
        
        if not self.instantiating:
            # getting tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['a'], withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Classes': classesWithElem, 'MaxDissolveArea': -1.0}

    def postProcess(self):
        """
        Gets the process that should be execute after this one
        """
        return self.tr('Deaggregate Geometries')
        
    def runProcessinAlg(self, layer):
        """
        Runs the actual grass process
        """
        alg = 'qgis:dissolve'
        uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        keyColumn = uri.keyColumn()
        #field.type() != 6 stands for virtual columns such as area_otf
        auxLayer = self.createUnifiedLayer([layer], None, attributeTupple = True)
        if self.parameters['MaxDissolveArea'] > 0:
            auxLayer = self.addDissolveField(auxLayer, self.parameters['MaxDissolveArea'])
        ret = processing.runalg(alg, auxLayer, False, 'tupple', None)
        if not ret:
            raise Exception(self.tr('Problem executing qgis:dissolve. Check your installed libs.\n'))
        #updating original layer
        outputLayer = processing.getObject(ret['OUTPUT'])
        QgsMapLayerRegistry.instance().removeMapLayer(auxLayer.id())
        self.splitUnifiedLayer(outputLayer, [layer])
        return outputLayer
    
    def addDissolveField(self, layer, tol):
        #add temp field
        idField = QgsField('d_id',QVariant.Int)
        layer.dataProvider().addAttributes([idField])
        layer.updateFields()
        #small feature list
        smallFeatureList = []
        bigFeatureList = []
        for feat in layer.getFeatures():
            feat['d_id'] = feat['featid']
            if feat.geometry().area() < float(tol):
                smallFeatureList.append(feat)
            else:
                bigFeatureList.append(feat)
        
        for bfeat in bigFeatureList:
            for sfeat in smallFeatureList:
                if sfeat['d_id'] == sfeat['featid'] and sfeat.geometry().intersects(bfeat.geometry()) and sfeat['tupple'] == bfeat['tupple']:
                    sfeat['d_id'] = bfeat['featid']
        idx = layer.fieldNameIndex('tupple')
        
        updateDict = dict()
        for feat in smallFeatureList + bigFeatureList:
            newValue = '{0},{1}'.format(feat['tupple'], feat['d_id'])
            updateDict[feat.id()] = {idx:newValue}
        layer.dataProvider().changeAttributeValues(updateDict)
        return layer
    
    def getCandidates(self, idx, bbox):
        return idx.intersects(bbox)

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            error = False
            classlist = []
            for classAndGeom in classesWithElem:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                lyr = self.loadLayerBeforeValidationProcess(cl)
                output = self.runProcessinAlg(lyr)

            if error:
                self.setStatus(self.tr('There are dissolve errors. Check log.'), 4) #Finished with errors
            else:
                self.setStatus(self.tr('Dissolve finished.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
