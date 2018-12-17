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
        email                : borba.philipe@eb.mil.br
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
from __future__ import print_function
import os
from qgis.core import QgsMessageLog, Qgis, QgsTask, QgsApplication
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.processParametersDialog import ProcessParametersDialog

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QMenu
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.Qt import QObject


class ValidationWorkflow(QgsTask):
    def __init__(self, description, flags):
        super(ValidationWorkflow, self).__init__(description, flags)

    def run(self):
        QgsMessageLog.logMessage(self.tr('Started task {}').format(self.description()))
        return True

class ValidationManager(QObject):
    def __init__(self, postgisDb, iface, application = None):
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
        self.taskManager = QgsApplication.taskManager() if not application else application.taskManager()
        self.workflowQueue = []
        self.algList = QgsApplication.processingRegistry().providerById('dsgtools').algorithms()
        try:
            #creating validation structure
            self.postgisDb.checkAndCreateValidationStructure()
            self.postgisDb.checkAndCreatePostGISAddonsFunctions()
            #setting available processes
            self.setAvailableProcesses()
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            
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
                processInstance = self.instantiateProcessByName(processClass, True)
                if processInstance:
                    self.processList.append({'category':processInstance.processCategory, 'alias':processInstance.processAlias, 'className':processClass })
                    self.processDict[processInstance.processAlias] = processClass 
        
    def instantiateProcessByName(self, processName, instantiating, withElements = True):
        """
        This method instantiate a process by its name.
        The import is made dynamically using the __import__ function.
        The class to be import is obtained using the getattr function.
        The class instance is made using: klass(self.postgisDb, self.iface)
        """
        currProc = None
        try:
            chars = list(processName)
            #adjusting first character case
            chars[0] = chars[0].lower()
            #making file name
            fileBaseName = ''.join(chars)
            #setting up the module to be imported
            mod = __import__('DsgTools.core.ValidationTools.ValidationProcesses.'+fileBaseName, fromlist=[processName])
            #obtaining the class name
            klass = getattr(mod, processName)
            #instantiating the class
            currProc = klass(self.postgisDb, self.iface, instantiating, withElements = withElements)
            return currProc
        except:
            return None
               
    def getProcessChain(self, processAlias, withElements = True):
        """
        Method to determine all processes that must be run
        This is a simple implementation, a recursive approach must be done if we want complex process graphs
        """
        currProc = self.instantiateProcessByName(self.processDict[processAlias], False, withElements = withElements)
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
        
    def getParams(self, process, lastParameters = None, restoreOverride = True, withElements = True):
        #get process chain
        processChain, parameterDict = self.getProcessChain(process, withElements = withElements)
        #get parameters from dialog
        if not lastParameters:
            params = self.getParametersWithUi(processChain, parameterDict, restoreOverride = restoreOverride, withElements = withElements)
            if params == -1:
                return -1
            self.lastParameters = params
            self.lastProcess = process
        else:
            params = lastParameters
        return params, processChain
    
    def executeProcessV2(self, process, lastParameters = None):
        """
        Executes a process according to its chain
        """
        #checking for running processes
        try:
            runningProc = self.postgisDb.getRunningProc()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            return 0
        #if there is a running process we should stop
        QApplication.restoreOverrideCursor()
        if runningProc != None:
            if not QMessageBox.question(self.iface.mainWindow(), self.tr('Question'),  self.tr('It seems that process {0} is already running. Would you like to ignore it and start another process?').format(process), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Ok:
                QgsMessageLog.logMessage(self.tr('Unable to run process {0}. Process {1} is already running.\n').format(process, runningProc), "DSG Tools Plugin", Qgis.Critical)
                return 0
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #get process chain
        processChain, parameterDict = self.getProcessChain(process)
        #get parameters from dialog
        if not lastParameters:
            if process != self.tr('Spatial Rule Checker'):
                params = self.getParametersWithUi(processChain, parameterDict)
                if params == -1:
                    return -1
            else:
                params = {}
            self.lastParameters = params
            self.lastProcess = process
        else:
            params = lastParameters
        #execute each process
        for process in processChain:
            QgsMessageLog.logMessage(self.tr('Process {0} Log:\n').format(process.getName()), "DSG Tools Plugin", Qgis.Critical)
            process.setParameters(params)
            process.setDbUserName(self.postgisDb.getDatabaseParameters()[2])
            process.setProcessName(self.processDict[process.processAlias])
            ret = process.execute()
            #status = currProc.getStatus() #must set status
            QgsMessageLog.logMessage(self.tr('Process {0} ran with status {1}\n').format(process.processAlias, process.getStatusMessage()), "DSG Tools Plugin", Qgis.Critical)
            # process.logTotalTime()
            # process.logProcess()
            if ret == 0:
                return 0
        return 1
    
    def addTaskToQeue(self, task, parameters):
        task.parameters = parameters
        self.workflowQueue.append(task)

    def runWorkflow(self):
        """
        Workflow is a set of dependent and serial tasks, each with its own parameters. 
        A workflowQueue is built and when this method is called, a QgsTask is built
        with dependencies, as follows:
            1 - The first task deppends on no other task;
            2 - When a taks is added to the workflow, it is added to the dependencies list;
            3 - For each task other than the first, it will depend on the task list;
        After the workflow is built, it is added to the taskManager

        """
        workflow = ValidationWorkflow(description = self.tr('Validation Workflow'))
        dependenciesList = []
        for task in self.workflowQueue:
            workflow.addSubTask(task, dependencies = dependenciesList, subTaskDependency = QgsTask.ParentDependsOnSubTask)
            if task not in dependenciesList:
                dependenciesList.append(task)
        self.taskManager.addTask(workflow)
