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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsProject, Qgis
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

from collections import OrderedDict

from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcesses

class IdentifyGapsAndOverlapsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyGapsAndOverlapsProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Earth Coverage Gaps and Overlaps')

        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            # adjusting process parameters
            self.parameters = {'Reference and Layers': OrderedDict({'referenceDictList':{}, 'layersDictList':interfaceDict})}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        try:
            self.startTimeCount()
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            refKey, classesKeys = self.parameters['Reference and Layers']
            if len(classesKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1

            if not refKey:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                return 1

            # preparing reference layer
            refDict = self.classesWithElemDict[refKey]
            refcl = """{0}.{1}""".format(refDict['tableSchema'], refDict['tableName'])
            reflyr = self.loadLayerBeforeValidationProcess(refDict)

            # gathering all coverage layers
            classlist = []
            for key in classesKeys:
                self.startTimeCount()
                # preparation
                cl = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl['tableName'], parent=self.iface.mapCanvas())
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
            result = self.abstractDb.getGapsAndOverlapsRecords(refcl, refDict['geom'])
            localProgress.step()

            #storing flags
            recordFlagList = []
            if len(result) > 0:
                for r in result:
                    featId, reason, geom = r
                    recordFlagList.append(('validation.coverage_temp', featId, reason, geom, 'geom'))

            #removing the coverage layer
            try:
                QgsProject.instance().removeMapLayer(coverage.id())
            except:
                QgsMessageLog.logMessage(self.tr('Error while trying to remove coverage layer.'), "DSG Tools Plugin", Qgis.Critical)
            
            # storing flags
            if len(recordFlagList) > 0:
                numberOfProblems = self.addFlag(recordFlagList)
                msg = self.tr('There are {} gaps or overlaps in the coverage layer. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('The coverage has no gaps or overlaps.')
                self.setStatus(msg, 1) #Finished

            # dropping temp table
            self.abstractDb.dropTempTable('validation.coverage_temp')
            self.logLayerTime('coverage')


            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()