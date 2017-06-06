# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-29
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
import processing, binascii

class TopologicalDouglasSimplificationProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Topological Douglas Peucker Simplification')
        
        if not self.instantiating:
            # getting tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['a', 'l'], withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Tolerance':1.0, 'Snap':1.0, 'MinArea':0.001 ,'Classes': classesWithElem}
        
    def runProcessinAlg(self, layer):
        """
        Runs the actual grass process
        """
        alg = 'grass7:v.generalize'

        #setting tools
        tools = 'break,rmsa,rmdangle'
        threshold = -1

        #getting table extent (bounding box)
        extent = layer.extent()
        (xmin, xmax, ymin, ymax) = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
        extent = '{0},{1},{2},{3}'.format(xmin, xmax, ymin, ymax)
        
        tol = self.parameters['Tolerance']
        snap = self.parameters['Snap']
        minArea = self.parameters['MinArea']
        
        ret = processing.runalg(alg, layer, 0, tol, 7, 50, 0.5, 3, 0, 0, 0, 1, 1, 1,False, True, extent, snap, minArea, 0, None)
        if not ret:
            raise Exception(self.tr('Problem executing grass7:v.generalize.simplify. Check your installed libs.\n'))
        
        #updating original layer
        outputLayer = processing.getObject(ret['output'])
        return outputLayer

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
                classlist.append(lyr)

            coverage = self.createUnifiedLayer(classlist)
            output = self.runProcessinAlg(coverage)
            self.splitUnifiedLayer(output, classlist)
            QgsMapLayerRegistry.instance().removeMapLayer(coverage.id())
            QgsMessageLog.logMessage(self.tr('Simplification done on the following layers: ') + ','.join([i.split(':')[0] for i in classesWithElem]) +'.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.setStatus(self.tr('Simplification process complete.'), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0
