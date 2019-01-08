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
        self.modelList = self.getModels()
        try:
            #creating validation structure
            self.postgisDb.checkAndCreateValidationStructure()
            #setting available processes
        except Exception as e:
            QMessageBox.critical(None, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
    
    def getModels(self):
        modelProvider = QgsApplication.processingRegistry().providerById('model')
        modelList = [model for model in modelProvider.algorithms() if model.group().lower() == 'dsgtools']
        return modelList
    
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
