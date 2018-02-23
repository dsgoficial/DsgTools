# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
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
from qgis.core import QgsMessageLog, QgsVectorLayer
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.DsgGeometrySnapper.dsgGeometrySnapper import DsgGeometrySnapper
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

from collections import OrderedDict

class RecursiveSnapParameters(list):
    def __init__(self):
        super(RecursiveSnapParameters, self).__init__()

class RecursiveSnapLayerOnLayerProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(RecursiveSnapLayerOnLayerProcess, self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Recursive Snap Layer on Layer')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a', 'l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            customInterface = RecursiveSnapParameters()
            for key in self.classesWithElemDict.keys():
                customInterface.append(key)
            # adjusting process parameters
            self.parameters = {'Snap': 5.0, 'Ordered Layers': customInterface, 'Only Selected':False}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            # refKey = self.parameters['Reference and Layers'][0]
            # classesWithElemKeys = self.parameters['Reference and Layers'][1]
            # if len(classesWithElemKeys) == 0:
            #     self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
            #     return 1

            # if not refKey:
            #     self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
            #     return 1

            # # preparing reference layer
            # refcl = self.classesWithElemDict[refKey]
            # reflyr = self.loadLayerBeforeValidationProcess(refcl)
            # snapper = DsgGeometrySnapper(reflyr)
            # snapper.featureSnapped.connect(self.updateProgress)
            # tol = self.parameters['Snap']
            # msg = ''
            # for key in classesWithElemKeys:
            #     # preparation
            #     clDict = self.classesWithElemDict[key]
            #     localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + clDict['tableName'], parent=self.iface.mapCanvas())
            #     localProgress.step()
            #     lyr = self.loadLayerBeforeValidationProcess(clDict)
            #     localProgress.step()

            #     # snapping lyr to reference
            #     if self.parameters['Only Selected']:
            #         featureList = lyr.selectedFeatures()
            #     else:
            #         featureList = lyr.getFeatures()
            #     features = [feature for feature in featureList]
            #     self.localProgress = ProgressWidget(1, len(features) - 1, self.tr('Processing features on ') + clDict['tableName'], parent=self.iface.mapCanvas())

            #     snappedFeatures = snapper.snapFeatures(features, tol)
            #     self.updateOriginalLayerV2(lyr, None, featureList=snappedFeatures)
            #     self.logLayerTime(clDict['lyrName'])

            #     localMsg = self.tr('All features from ') +clDict['lyrName']+ self.tr(' snapped to reference ') +refcl['tableName']+ self.tr(' succesfully.\n')
            #     QgsMessageLog.logMessage(localMsg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            #     msg += localMsg
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()