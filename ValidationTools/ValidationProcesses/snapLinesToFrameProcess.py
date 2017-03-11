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
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Snap Lines to Frame')
        
        # getting tables with elements
        classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['l'], withElements=True, getGeometryColumn=True)
        # creating a list of tuples (layer names, geometry columns)
        classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
        # adjusting process parameters
        self.parameters = {'Snap': 5.0, 'Classes': classesWithElem}

    def postProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Snap to Grid')
        
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            lines = self.parameters['Classes']
            if len(lines) == 0:
                self.setStatus(self.tr('Empty database.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('Empty database.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            tol = self.parameters['Snap']
            for classAndGeom in lines:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                processTableName, lyr = self.prepareExecution(cl, geometryColumn)
                frameTableName, frameLyr = self.prepareExecution('public.aux_moldura_a')

                #running the process in the temp table
                self.abstractDb.snapLinesToFrame([processTableName], frameTableName, tol)
                self.abstractDb.densifyFrame([processTableName], frameTableName, self.parameters['Snap Tolerance'])
                
                # finalization
                #TODO: Put try except to end process when error occur
                self.postProcessSteps(processTableName, lyr)
                self.postProcessSteps(frameTableName, frameLyr)
            msg = self.tr('All features snapped succesfully.')
            self.setStatus(msg, 1) #Finished
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0