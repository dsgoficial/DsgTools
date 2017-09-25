# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsMapLayerRegistry
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.DsgGeometrySnapper.dsgGeometrySnapper import DsgGeometrySnapper
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class IdentifyGapsAndOverlapsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Identify Gaps and Overlaps')
        
        if not self.instantiating:
            # getting tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Reference and Layers': ([], classesWithElem)}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
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

            # gathering all coverage layers
            classlist = []
            for classAndGeom in classesWithElem:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(cl)
                classlist.append(lyr)
                localProgress.step()

            # creating the unified layer
            coverage = self.createUnifiedLayer(classlist)

            # creating the temporary coverage layer on postgis
            self.abstractDb.createAndPopulateCoverageTempTable(coverage)

            # running the process
            localProgress = ProgressWidget(0, 1, self.tr('Running process for coverage_temp'), parent=self.iface.mapCanvas())
            localProgress.step()
            result = self.abstractDb.getGapsAndOverlapsRecords(refcl, refGeometryColumn)
            localProgress.step()

            #storing flags
            recordFlagList = []
            if len(result) > 0:
                for r in result:
                    featId, reason, geom = r
                    recordFlagList.append(('validation.coverage_temp', featId, reason, geom, 'geom'))

            #removing the coverage layer
            try:
                QgsMapLayerRegistry.instance().removeMapLayer(coverage.id())
            except:
                QgsMessageLog.logMessage(self.tr('Error while trying to remove coverage layer.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            
            # storing flags
            if len(recordFlagList) > 0:
                numberOfProblems = self.addFlag(recordFlagList)
                msg = self.tr('There are {} gaps or overlaps in the coverage layer. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('The coverage has no gaps or overlaps.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)

            # dropping temp table
            self.abstractDb.dropTempTable('validation.coverage_temp')

            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()