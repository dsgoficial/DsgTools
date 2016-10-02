# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-06-22
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
from qgis.core import QgsMessageLog, QgsVectorLayer
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SnapToGridProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.parameters = {'Snap': 0.001}

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            classesWithElem = self.abstractDb.listClassesWithElementsFromDatabase()
            if len(classesWithElem) == 0:
                self.setStatus('Empty database.\n', 1) #Finished
                QgsMessageLog.logMessage('Empty database.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            #getting parameters
            tol = self.parameters['Snap']
            srid = self.abstractDb.findEPSG()
            for cl in classesWithElem:
                # preparation
                processTableName, lyr = self.prepareExecution(cl)
                #running the process in the temp table
                self.abstractDb.snapToGrid([processTableName], tol, srid)
                # finalization
                self.postProcessSteps(processTableName, lyr)
                #setting status
                self.setStatus('All features from {} snapped succesfully.\n'.format(cl), 1) #Finished
                QgsMessageLog.logMessage('All features from {} snapped succesfully.\n'.format(cl), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            #returning success
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            #returning error
            return 0