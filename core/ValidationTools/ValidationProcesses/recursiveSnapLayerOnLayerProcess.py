# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-23
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
from qgis.core import QgsMessageLog, QgsVectorLayer, Qgis
from qgis.analysis import QgsGeometrySnapper

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from .validationProcess import ValidationProcess

from collections import OrderedDict

class RecursiveSnapParameters(list):
    def __init__(self, x):
        super(RecursiveSnapParameters, self).__init__()
        self.values = x

class RecursiveSnapLayerOnLayerProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(RecursiveSnapLayerOnLayerProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Recursive Snap Layer on Layer')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            self.interfaceDict = dict()
            for key in list(self.classesWithElemDict.keys()):
                cat, lyr, geom = tuple(key.split(',')[0:3])
                interfaceKey = '{0}.{1} ({2})'.format(cat, lyr, geom)
                self.interfaceDict[interfaceKey] = key
            customInterface = RecursiveSnapParameters(list(self.interfaceDict.keys()))
            # adjusting process parameters
            self.parameters = {'Ordered Layers': customInterface, 'Only Selected':False}
    
    def loadAllLayersAndGetFeatures(self, keyList):
        pass

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        1. load all features and build structure
        2. Perform snap on each tree step (reference and all below rank)
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            snapList = self.parameters['Ordered Layers']
            if len(snapList) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            self.startTimeCount()
            for snapItem in snapList:
                #reference layer
                refcl = self.classesWithElemDict[self.interfaceDict[snapItem['referenceLayer']]]
                reflyr = self.loadLayerBeforeValidationProcess(refcl)
                snapper = QgsGeometrySnapper(reflyr)
                snapper.featureSnapped.connect(self.updateProgress)
                tol = snapItem['snap']
                msg = ''
                for key in snapItem['snapLayerList']:
                    # preparation
                    clDict = self.classesWithElemDict[self.interfaceDict[key]]
                    localProgress = ProgressWidget(0, 1, self.tr('Preparing snapping of {0} on {1}').format(clDict['tableName'], refcl['tableName']), parent=self.iface.mapCanvas())
                    localProgress.step()
                    lyr = self.loadLayerBeforeValidationProcess(clDict)
                    localProgress.step()

                    # snapping lyr to reference
                    if self.parameters['Only Selected']:
                        featureList = lyr.selectedFeatures()
                    else:
                        featureList = lyr.getFeatures()
                    features = [feature for feature in featureList]
                    self.localProgress = ProgressWidget(1, len(features) - 1, self.tr('Snapping features from {0} on {1} ').format(clDict['tableName'], refcl['tableName']), parent=self.iface.mapCanvas())

                    snappedFeatures = snapper.snapFeatures(features, tol, mode = QgsGeometrySnapper.PreferClosest)
                    self.updateOriginalLayerV2(lyr, None, featureList=snappedFeatures)
                    self.logLayerTime(clDict['lyrName'])

                    localMsg = self.tr('All features from ') +clDict['lyrName']+ self.tr(' snapped to reference ') +refcl['tableName']+ self.tr(' succesfully.\n')
                    QgsMessageLog.logMessage(localMsg, "DSG Tools Plugin", Qgis.Critical)
                    msg += localMsg
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()