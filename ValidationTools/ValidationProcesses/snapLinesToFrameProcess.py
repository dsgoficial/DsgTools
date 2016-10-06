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
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class SnapLinesToFrameProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Snap Lines to Frame Process')
        self.parameters = {'Snap': 5.0}

    def postProcess(self):
        '''
        Gets the process that should be execute after this one
        '''
        return 'SnapToGridProcess'

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            classesWithGeom = self.abstractDb.getOrphanGeomTablesWithElements()
            if len(classesWithElem) == 0:
                self.setStatus('Empty database.', 1) #Finished
                QgsMessageLog.logMessage('Empty database.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            lines = []
            for cl in classesWithGeom:
                if cl[-1] == 'l':
                    lines.append(cl)
            tol = self.parameters['Snap']
            for cl in lines:
                # preparation
                processTableName, lyr = self.prepareExecution(cl)
                #running the process in the temp table
                self.abstractDb.snapLinesToFrame([processTableName], tol)
                self.abstractDb.densifyFrame([processTableName])
                # finalization
                self.postProcessSteps(processTableName, lyr)
            self.setStatus('All features snapped succesfully.', 1) #Finished
            QgsMessageLog.logMessage('All features snapped succesfully.', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0