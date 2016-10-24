# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
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

class IdentifyInvalidGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Identify Invalid Geometries')

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName())
            invalidGeomRecordList = self.abstractDb.getInvalidGeomRecords() #list only classes with elements.
            if len(invalidGeomRecordList) > 0:
                numberOfInvGeom = self.addFlag(invalidGeomRecordList)
                for tuple in invalidGeomRecordList:
                    self.addClassesToBeDisplayedList(tuple[0])  
                msg = self.tr('{} features are invalid. Check flags.').format(numberOfInvGeom)
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            else:
                msg = self.tr('All features are valid.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0

