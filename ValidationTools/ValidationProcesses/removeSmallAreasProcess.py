# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-04-06
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

class RemoveSmallAreasProcess(ValidationProcess):
    def __init__(self, postgisDb):
        super(self.__class__,self).__init__(postgisDb)

    def execute(self):
        #abstract method. MUST be reimplemented.
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifySmallAreasProcess')
            numberOfProblems = 0
            for cl in flagsDict.keys():
                numberOfProblems += self.abstractDb.removeFeatures(cl,flagsDict[cl])
            self.setStatus('%s features were removed.\n' % numberOfProblems, 1) #Finished with flags
            QgsMessageLog.logMessage('%s features were changed.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return