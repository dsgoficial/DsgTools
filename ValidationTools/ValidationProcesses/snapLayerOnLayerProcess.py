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

from collections import deque

class SnapLayerOnLayerProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Snap Layer on Layer')
        
        if not self.instantiating:
            # getting tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Snap': 5.0, 'Reference and Layers': deque([], classesWithElem)}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            refWithElem = self.parameters['Reference and Layers'][0]
            classesWithElem = self.parameters['Reference and Layers'][1]
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1

            if not refWithElem:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('One reference must be selected! Stopping.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1

            # preparing reference layer
            refcl, refGeometryColumn = refWithElem.split(':')
            reflyr = self.loadLayerBeforeValidationProcess(refcl)
            snapper = DsgGeometrySnapper(reflyr)
            snapper.featureSnapped.connect(self.updateProgress)

            tol = self.parameters['Snap']
            msg = ''
            for classAndGeom in classesWithElem:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(cl)
                localProgress.step()

                # snapping lyr to reference
                features = [feature for feature in lyr.getFeatures()]
                self.localProgress = ProgressWidget(1, len(features) - 1, self.tr('Processing features on ') + cl, parent=self.iface.mapCanvas())

                snappedFeatures = snapper.snapFeatures(features, tol)
                self.updateOriginalLayer(lyr, None, featureList=snappedFeatures)

                localMsg = self.tr('All features from ') +cl+ self.tr(' snapped to reference ') +refcl+ self.tr(' succesfully.\n')
                QgsMessageLog.logMessage(localMsg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                msg += localMsg
            self.setStatus(msg, 1) #Finished
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()