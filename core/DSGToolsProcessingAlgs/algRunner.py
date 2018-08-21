# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-15
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import processing

from qgis.core import QgsProcessingUtils

class AlgRunner:
    Break, Snap, RmDangle, ChDangle, RmBridge, ChBridge, RmDupl, RmDac, BPol, Prune, RmArea, RmLine, RMSA = range(13)

    def generateGrassOutputAndError(self):
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        error = QgsProcessingUtils.generateTempFilename('error.shp')
        return output, error
    
    def getGrassReturn(self, outputDict, context, returnError = False):
        lyr = QgsProcessingUtils.mapLayerFromString(outputDict['output'], context)
        if returnError:
            errorLyr = QgsProcessingUtils.mapLayerFromString(outputDict['error'], context)
            return lyr, errorLyr
        else:
            return lyr

    def runDissolve(self, inputLyr, context, outputLyr = 'memory:', field = []):
        parameters = {
            'INPUT' : inputLyr,
            'FIELD': [],
            'OUTPUT': outputLyr
        }
        output = processing.run('native:dissolve', parameters, context = context)
        return output['OUTPUT']
    
    def runDonutHoleExtractor(self, inputLyr, context, donuthole = 'memory:', outershell = 'memory:' , selected = False):
        parameters = {
            'INPUT' : inputLyr,
            'SELECTED' : selected,
            'OUTERSHELL': outershell,
            'DONUTHOLE' : donuthole
        }
        output = processing.run('dsgtools:donutholeextractor', parameters, context = context)
        return output['OUTERSHELL'], output['DONUTHOLE']
    
    def runDeleteHoles(self, inputLyr, context, outputLyr='memory:', min_area=0):
        parameters = {
            'INPUT' : inputLyr,
            'MIN_AREA': min_area,
            'OUTPUT': outputLyr
        }
        output = processing.run('native:deleteholes', parameters, context = context)
        return output['OUTPUT']
    
    def runOverlay(self, lyrA, lyrB, context, snap=0, operator=0, minArea=0.0001):
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        parameters = {
            'ainput':lyrA,
            'atype':0,
            'binput':lyrB,
            'btype':0,
            'operator':operator,
            'snap':snap,
            '-t':False,
            'output':output,
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
            'GRASS_MIN_AREA_PARAMETER':minArea,
            'GRASS_OUTPUT_TYPE_PARAMETER':0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        outputDict = processing.run('grass7:v.overlay', parameters, context = context)
        return self.getGrassReturn(outputDict, context)
    
    def runClean(self, inputLyr, toolList, context, typeList=[0,1,2,3,4,5,6], returnError = False, useFollowup = True, snap = -1, minArea = 0.0001): 
        output, error = self.generateGrassOutputAndError()
        parameters = {
            'input':inputLyr,
            'type':typeList,
            'tool':toolList,
            'threshold':'-1', 
            '-b': False, 
            '-c': useFollowup, 
            'output' : output, 
            'error': error, 
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': snap,
            'GRASS_MIN_AREA_PARAMETER': minArea,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        outputDict = processing.run('grass7:v.clean', parameters, context = context)
        return self.getGrassReturn(outputDict, context, returnError=returnError)
    
    def runDouglasSimplification(self, inputLyr, threshold, context, snap=-1, minArea=0.0001, iterations=1, type=[0,1,2], returnError=False):
        output, error = self.generateGrassOutputAndError()
        parameters = {
            'input': inputLyr,
            'type':[0,1,2],
            'cats':'',
            'where':'',
            'method':0,
            'threshold':threshold,
            'look_ahead':7,
            'reduction':50,
            'slide':0.5,
            'angle_thresh':3,
            'degree_thresh':0,
            'closeness_thresh':0,
            'betweeness_thresh':0,
            'alpha':1,
            'beta':1,
            'iterations':iterations,
            '-t':False,
            '-l':True,
            'output':output,
            'error':error,
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER':snap,
            'GRASS_MIN_AREA_PARAMETER':minArea,
            'GRASS_OUTPUT_TYPE_PARAMETER':0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''}
        outputDict = processing.run("grass7:v.generalize", parameters, context=context)
        return self.getGrassReturn(outputDict, context, returnError=returnError)