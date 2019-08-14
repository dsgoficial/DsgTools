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
import uuid

import processing
from qgis.core import QgsProcessingUtils, QgsVectorLayer


class AlgRunner:
    Break, Snap, RmDangle, ChDangle, RmBridge, ChBridge, RmDupl, RmDac, BPol, Prune, RmArea, RmLine, RMSA = range(13)

    def generateGrassOutputAndError(self):
        uuid_value = str(uuid.uuid4()).replace('-','')
        output = QgsProcessingUtils.generateTempFilename('output_{uuid}.shp'.format(uuid=uuid_value))
        error = QgsProcessingUtils.generateTempFilename('error_{uuid}.shp'.format(uuid=uuid_value))
        return output, error
    
    def getGrassReturn(self, outputDict, context, returnError = False):
        lyr = QgsProcessingUtils.mapLayerFromString(outputDict['output'], context)
        if returnError:
            errorLyr = QgsProcessingUtils.mapLayerFromString(outputDict['error'], context)
            return lyr, errorLyr
        else:
            return lyr

    def runDissolve(self, inputLyr, context, feedback = None, outputLyr = 'memory:', field = None):
        field = [] if field is None else field
        parameters = {
            'INPUT' : inputLyr,
            'FIELD': field,
            'OUTPUT': outputLyr
        }
        output = processing.run('native:dissolve', parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runGrassDissolve(self, inputLyr, context, feedback=None, column=None, outputLyr=None, onFinish=None):
        """
        Runs dissolve from GRASS algorithm provider.
        :param inputLyr: (QgsVectorLayer) layer to be dissolved.
        :param context: (QgsProcessingContext) processing context.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        :param column: ()
        :param outputLyr: (str) URI to output layer.
        :param onFinish: (list-of-str) sequence of algs to be run after dissolve is executed, in execution order.
        :return: (QgsVectorLayer) dissolved (output) layer.
        """
        parameters = {
            'GRASS_MIN_AREA_PARAMETER' : 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER' : 0,
            'GRASS_REGION_PARAMETER' : None,
            'GRASS_SNAP_TOLERANCE_PARAMETER' : -1,
            'GRASS_VECTOR_DSCO' : '',
            'GRASS_VECTOR_EXPORT_NOCAT' : False,
            'GRASS_VECTOR_LCO' : '',
            'column' : column,
            'input' : inputLyr,
            'output' : outputLyr or QgsProcessingUtils.generateTempFilename('output.shp')
        }
        output = processing.run('grass7:v.dissolve', parameters, onFinish, feedback, context)
        return self.getGrassReturn(output, context)

    def runDonutHoleExtractor(self, inputLyr, context, feedback = None, donuthole = 'memory:', outershell = 'memory:' , selected = False):
        parameters = {
            'INPUT' : inputLyr,
            'SELECTED' : selected,
            'OUTERSHELL': outershell,
            'DONUTHOLE' : donuthole
        }
        output = processing.run('dsgtools:donutholeextractor', parameters, context = context, feedback = feedback)
        return output['OUTERSHELL'], output['DONUTHOLE']
    
    def runDeleteHoles(self, inputLyr, context, feedback = None, outputLyr='memory:', min_area=0):
        parameters = {
            'INPUT' : inputLyr,
            'MIN_AREA': min_area,
            'OUTPUT': outputLyr
        }
        output = processing.run('native:deleteholes', parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runOverlay(self, lyrA, lyrB, context, feedback = None, snap=0, operator=0, minArea=0.0001):
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
        outputDict = processing.run('grass7:v.overlay', parameters, context = context, feedback = feedback)
        return self.getGrassReturn(outputDict, context)
    
    def runClean(self, inputLyr, toolList, context, feedback=None, typeList=None, returnError = False, useFollowup = False, snap = -1, minArea = 0.0001): 
        typeList = [0,1,2,3,4,5,6] if typeList is None else typeList
        output, error = self.generateGrassOutputAndError()
        parameters = {
            'input':inputLyr,
            'type':typeList,
            'tool':toolList,
            '-b': False, 
            '-c': useFollowup, 
            'output' : output, 
            'error': error, 
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': snap,
            'GRASS_MIN_AREA_PARAMETER': minArea,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':'',
            'GRASS_VECTOR_EXPORT_NOCAT':False
            }
        outputDict = processing.run('grass7:v.clean', parameters, context = context, feedback = feedback)
        return self.getGrassReturn(outputDict, context, returnError=returnError)
    
    def runDsgToolsClean(self, inputLyr, context, feedback = None, onlySelected = False, snap = -1, minArea = 0.0001, flags = 'memory:'):
        parameters = {
            'INPUT' : inputLyr,
            'SELECTED' : onlySelected,
            'TOLERANCE': snap,
            'MINAREA': minArea,
            'FLAGS' : flags
        }
        output = processing.run('dsgtools:cleangeometries', parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runDouglasSimplification(self, inputLyr, threshold, context, feedback = None, snap=-1, minArea=0.0001, iterations=1, type=None, returnError=False):
        algType = [0,1,2] if type is None else type
        output, error = self.generateGrassOutputAndError()
        parameters = {
            'input': inputLyr,
            'type':algType,
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
        outputDict = processing.run("grass7:v.generalize", parameters, context=context, feedback=feedback)
        return self.getGrassReturn(outputDict, context, returnError=returnError)
    
    def runIdentifyDuplicatedGeometries(self, inputLyr, context, feedback = None, flagLyr = 'memory:', onlySelected = False):
        parameters = {
            'INPUT' : inputLyr,
            'SELECTED' : onlySelected,
            'FLAGS': flagLyr
        }
        output = processing.run('dsgtools:identifyduplicatedgeometries', parameters, context = context, feedback = feedback)
        return output['FLAGS']
    
    def runIdentifyDuplicatedFeatures(self, inputLyr, context, onlySelected=False, attributeBlackList=None, excludePrimaryKeys=True, ignoreVirtualFields=True, feedback = None, flagLyr = 'memory:'):
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        parameters = {
            'INPUT' : inputLyr,
            'SELECTED' : onlySelected,
            'FLAGS': flagLyr,
            'ATTRIBUTE_BLACK_LIST' : attributeBlackList,
            'IGNORE_VIRTUAL_FIELDS' : ignoreVirtualFields,
            'IGNORE_PK_FIELDS' : excludePrimaryKeys
        }
        output = processing.run('dsgtools:identifyduplicatedfeatures', parameters, context = context, feedback = feedback)
        return output['FLAGS']
    
    def runIdentifySmallLines(self, inputLyr, tol, context, feedback = None, flagLyr = 'memory:', onlySelected = False):
        parameters = {
            'INPUT' : inputLyr,
            'TOLERANCE' : tol,
            'SELECTED' : onlySelected,
            'FLAGS': flagLyr
        }
        output = processing.run('dsgtools:identifysmalllines', parameters, context = context, feedback = feedback)
        return output['FLAGS']

    def runIdentifySmallPolygons(self, inputLyr, tol, context, feedback = None, flagLyr = 'memory:', onlySelected = False):
        parameters = {
            'INPUT' : inputLyr,
            'TOLERANCE' : tol,
            'SELECTED' : onlySelected,
            'FLAGS': flagLyr
        }
        output = processing.run('dsgtools:identifysmallpolygons', parameters, context = context, feedback = feedback)
        return output['FLAGS']
    
    def runSnapGeometriesToLayer(self, inputLayer, referenceLayer, tol, context, feedback = None, behavior=0, outputLyr = 'memory:'):
        parameters = {
            'INPUT' : inputLayer,
            'REFERENCE_LAYER' : referenceLayer,
            'TOLERANCE' : tol,
            'BEHAVIOR' : behavior,
            'OUTPUT' : outputLyr
        }
        output = processing.run('qgis:snapgeometries', parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runSnapLayerOnLayer(self, inputLayer, referenceLayer, tol, context, onlySelected = False, feedback = None, behavior=0):
        parameters = {
            'INPUT' : inputLayer,
            'SELECTED' : onlySelected,
            'REFERENCE_LAYER' : referenceLayer,
            'TOLERANCE' : tol,
            'BEHAVIOR' : behavior
        }
        output = processing.run('dsgtools:snaplayeronlayer', parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runIdentifyDangles(self, inputLayer, searchRadius, context, feedback = None, onlySelected=False, lineFilter = None, polygonFilter = None, ignoreUnsegmented = False, ignoreInner = False, flagLyr = 'memory:'):
        lineFilter = [] if lineFilter is None else lineFilter
        polygonFilter = [] if polygonFilter is None else polygonFilter
        parameters = {
            'INPUT' : inputLayer,
            'SELECTED' : onlySelected,
            'TOLERANCE' : searchRadius,
            'LINEFILTERLAYERS' : lineFilter,
            'POLYGONFILTERLAYERS' : polygonFilter,
            'TYPE' : ignoreUnsegmented,
            'IGNOREINNER' : ignoreInner,
            'FLAGS' : flagLyr
        }
        output = processing.run('dsgtools:identifydangles', parameters, context = context, feedback = feedback)
        return output['FLAGS']
    
    def runSnapToGrid(self, inputLayer, tol, context, feedback = None, outputLyr = 'memory:'):
        parameters = {
            'INPUT':inputLayer,
            'HSPACING':tol,
            'VSPACING':tol,
            'ZSPACING':0,
            'MSPACING':0,
            'OUTPUT':outputLyr
        }
        output = processing.run("native:snappointstogrid", parameters, context=context, feedback=feedback)
        return output['OUTPUT']
    
    def runRemoveNull(self, inputLayer, context, feedback = None, outputLyr = 'memory:'):
        parameters = {
            'INPUT':inputLayer,
            'OUTPUT':outputLyr
        }
        output = processing.run("native:removenullgeometries", parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runClip(self, inputLayer, overlayLayer, context, feedback = None, outputLyr = 'memory:'):
        parameters = {
            'INPUT' : inputLayer,
            'OVERLAY' : overlayLayer,
            'OUTPUT' : outputLyr
        }
        output = processing.run("native:clip", parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runSymDiff(self, inputLayer, overlayLayer, context, feedback = None, outputLyr = 'memory:'):
        parameters = {
            'INPUT' : inputLayer,
            'OVERLAY' : overlayLayer,
            'OUTPUT' : outputLyr
        }
        output = processing.run("native:symmetricaldifference", parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runBoundary(self, inputLayer, context, feedback=None, outputLyr='memory:'):
        parameters = {
            'INPUT' : inputLayer,
            'OUTPUT' : outputLyr
        }
        output = processing.run("native:boundary", parameters, context=context, feedback=feedback)
        return output['OUTPUT']

    def runBuffer(self, inputLayer, distance, context, dissolve=False, endCapStyle=0, joinStyle=0, segments=5,\
                 mitterLimit=2, feedback = None, outputLyr = 'memory:'):
        parameters = {
            'INPUT' : inputLayer,
            'DISTANCE' : distance,
            'DISSOLVE' : dissolve, 
            'END_CAP_STYLE' : endCapStyle,
            'JOIN_STYLE' : endCapStyle,
            'SEGMENTS' : segments,
            'MITER_LIMIT' : mitterLimit,
            'OUTPUT' : outputLyr
        }
        output = processing.run("native:buffer", parameters, context = context, feedback = feedback)
        return output['OUTPUT']
    
    def runIntersection(self, inputLyr, context, inputFields=None, outputLyr='memory:', overlayLyr=None, overlayFields=None, feedback=None):
        inputFields = [] if inputFields is None else inputFields
        overlayFields = [] if overlayFields is None else overlayFields
        parameters = { 
            'INPUT' : inputLyr, 
            'INPUT_FIELDS' : inputFields, 
            'OUTPUT' : outputLyr,
            'OVERLAY' : overlayLyr,
            'OVERLAY_FIELDS' : overlayFields 
            }
        output = processing.run("native:intersection", parameters, context=context, feedback=feedback)
        return output['OUTPUT']
    
    def runFilterExpression(self, inputLyr, expression, context, outputLyr='memory:', feedback=None):
        parameters = {
            'EXPRESSION' : expression,
            'INPUT' : inputLyr,
            'OUTPUT' : outputLyr
            }
        output = processing.run("native:extractbyexpression", parameters, context=context, feedback=feedback)
        return output['OUTPUT']
