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
import os
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.processParametersDialog import ProcessParametersDialog

from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QMenu
from PyQt4.Qt import QObject

class ValidationManager(QObject):
    def __init__(self,postgisDb, iface):
        """
        Constructor
        """
        super(ValidationManager, self).__init__()
        self.processList = []
        self.postgisDb = postgisDb
        self.iface = iface
        self.processDict = dict()
        self.lastProcess = None
        self.lastParameters = None
        try:
            #creating validation structure
            self.postgisDb.checkAndCreateValidationStructure()
            self.postgisDb.checkAndCreatePostGISAddonsFunctions()
            #setting available processes
            self.setAvailableProcesses()
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            

    def setAvailableProcesses(self):
        """
        Sets all available processes.
        This method is a dynamic method that scans the processes folder for .py files.
        All .py files within the folder (minus the ignored ones) are listed as available processes
        """
        ignoredFiles = ['__init__.py', 'validationProcess.py', 'spatialRuleEnforcer.py']
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'ValidationProcesses')):
            files.sort()
            for file in files:
                if file in ignoredFiles or file.split('.')[-1] != 'py':
                    continue
                fileBaseName = file.split('.')[0]
                chars = list(fileBaseName)
                chars[0] = chars[0].upper()
                processClass = ''.join(chars)
                self.processList.append(processClass)
                self.processDict[self.instantiateProcessByName(processClass, True).processAlias] = processClass 
            
    def instantiateProcessByName(self, processName, instantiating):
        """
        This method instantiate a process by its name.
        The import is made dynamically using the __import__ function.
        The class to be import is obtained using the getattr function.
        The class instance is made using: klass(self.postgisDb, self.iface)
        """
        currProc = None
        for processClass in self.processList:
            if processClass == processName:
                chars = list(processClass)
                #adjusting first character case
                chars[0] = chars[0].lower()
                #making file name
                fileBaseName = ''.join(chars)
                #setting up the module to be imported
                mod = __import__('DsgTools.ValidationTools.ValidationProcesses.'+fileBaseName, fromlist=[processClass])
                #obtaining the class name
                klass = getattr(mod, processClass)
                #instantiating the class
                currProc = klass(self.postgisDb, self.iface, instantiating)
                return currProc
               
    def getProcessChain(self, processAlias):
        """
        Method to determine all processes that must be run
        This is a simple implementation, a recursive approach must be done if we want complex process graphs
        """
        currProc = self.instantiateProcessByName(self.processDict[processAlias], False)
        preProcessList, parameterDict = self.generateProcessObjects(currProc.preProcess(), currProc.parameters)
        postProcessList, parameterDict = self.generateProcessObjects(currProc.postProcess(), parameterDict)
        postProcessAlias = currProc.postProcess()
        localList = preProcessList + [currProc] + postProcessList
        return localList, parameterDict

    def generateProcessObjects(self, inputItem, inputParameterDict):
        """
        Returns currentList and parameterDict
        """
        localList = []
        if not inputParameterDict:
            parameterDict = dict()
        else:
            parameterDict = inputParameterDict
        if inputItem:
            if not isinstance(inputItem, list):
                processAliasList = [inputItem]
            else:
                processAliasList = inputItem
            for processAlias in processAliasList:
                process = self.instantiateProcessByName(self.processDict[processAlias], False)
                localList.append(process)
                if process.parameters:
                    parameterDict = dict(process.parameters, **parameterDict) #this is done this way not to overide process original classes
        return localList, parameterDict

    def runLastProcess(self):
        if self.lastProcess and self.lastParameters:
            return self.executeProcessV2(self.lastProcess, lastParameters = self.lastParameters)
        else:
            return -2
    
    def executeProcessV2(self, process, lastParameters = None):
        """
        Executes a process according to its chain
        """
        #checking for running processes
        try:
            runningProc = self.postgisDb.getRunningProc()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 0
        #if there is a running process we should stop
        QApplication.restoreOverrideCursor()
        if runningProc != None:
            if not QtGui.QMessageBox.question(self.iface.mainWindow(), self.tr('Question'),  self.tr('It seems that process {0} is already running. Would you like to ignore it and start another process?').format(process), QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                QgsMessageLog.logMessage(self.tr('Unable to run process {0}. Process {1} is already running.\n').format(process, runningProc), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 0
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #get process chain
        processChain, parameterDict = self.getProcessChain(process)
        #get parameters from dialog
        if not lastParameters:
            params = self.getParametersWithUi(processChain, parameterDict)
            if params == -1:
                return -1
            self.lastParameters = params
            self.lastProcess = process
        else:
            params = lastParameters
        #execute each process
        for process in processChain:
            QgsMessageLog.logMessage(self.tr('Process {0} Log:\n').format(process.getName()), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            process.setParameters(params)
            process.setDbUserName(self.postgisDb.getDatabaseParameters()[2])
            process.setProcessName(self.processDict[process.processAlias])
            ret = process.execute() #run bitch run!
            #status = currProc.getStatus() #must set status
            QgsMessageLog.logMessage(self.tr('Process {0} ran with status {1}\n').format(process.processAlias, process.getStatusMessage()), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            # process.logTotalTime()
            process.logProcess()        
            if ret == 0:
                return 0
        return 1
    
    def getParametersWithUi(self, processChain, parameterDict):
        """
        Builds interface
        """
        processText = ', '.join([process.processAlias for process in processChain])
        dlg = ProcessParametersDialog(None, parameterDict, None, self.tr('Process parameters setter for process(es) {0}').format(processText))
        if dlg.exec_() == 0:
            return -1
        # get parameters
        params = dlg.values
        return params

    def executeProcess(self, process):
        """
        Executes a process by its name
        processName: process name
        """
        #checking for running processes
        processName = self.processDict[process]
        runningProc = None
        try:
            runningProc = self.postgisDb.getRunningProc()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 0
            
        #if there is a running process we should stop
        QApplication.restoreOverrideCursor()
        if runningProc != None:
            if not QtGui.QMessageBox.question(self.iface.mainWindow(), self.tr('Question'),  self.tr('It seems that process {0} is already running. Would you like to ignore it and start another process?').format(process), QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                QgsMessageLog.logMessage(self.tr('Unable to run process {0}. Process {1} is already running.\n').format(process, runningProc), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 0
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        currProc = self.instantiateProcessByName(processName, False)
        #checking for existing pre process
        preProcessName = currProc.preProcess()
        if preProcessName:
            self.executeProcess(preProcessName)
        # setting parameters
        if currProc.parameters:
            dlg = ProcessParametersDialog(None, currProc.parameters, None, self.tr('Process parameters setter for process {0}').format(process))
            if dlg.exec_() == 0:
                return -1
            # get parameters
            params = dlg.values
            # adjusting the parameters in the process
            currProc.setParameters(params)
        #check status
        QgsMessageLog.logMessage('Process %s Log:\n' % currProc.getName(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        ret = currProc.execute() #run bitch run!
        #status = currProc.getStatus() #must set status
        QgsMessageLog.logMessage('Process ran with status %s\n' % currProc.getStatusMessage(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        currProc.logTotalTime()
        #checking for existing post process
        postProcessName = currProc.postProcess()
        if postProcessName:
            self.executeProcess(postProcessName)
        return ret
    
if __name__ == '__main__':
    from DsgTools.Factories.DbFactory.dbFactory import DbFactory
    abstractDb = DbFactory().createDbFactory('QPSQL')
    manager = ValidationManager(abstractDb)
    print manager
    pass
