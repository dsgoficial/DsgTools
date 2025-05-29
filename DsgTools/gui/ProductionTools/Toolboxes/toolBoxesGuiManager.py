# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


from builtins import object
import os.path
import sys
import json

from qgis.PyQt.QtCore import QObject, Qt
from qgis.core import QgsProject, QgsExpressionContextUtils

from .AttributeTools.code_list import CodeList
from DsgTools.Modules.acquisitionMenu.controllers.acquisitionMenuCtrl import (
    AcquisitionMenuCtrl,
)
from .ContourTool.calc_contour import CalcContour
from .ComplexTools.complexWindow import ComplexWindow
from .WorkflowToolBox.workflowDockWidget import (
    WorkflowDockWidget,
)
from .MultiLayersCentroidsFlagTool.multiLayersCentroidsFlagTool import (
    MultiLayersCentroidsFlagDockWidget,
)


class ToolBoxesGuiManager(QObject):
    def __init__(
        self,
        manager,
        iface,
        parentMenu=None,
        toolbar=None,
        stackButton=None,
        acquisitionMenuCtrl=None,
    ):
        """Constructor."""
        super(ToolBoxesGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.stackButton = stackButton
        self.iconBasePath = ":/plugins/DsgTools/icons/"

        self.acquisitionMenuCtrl = (
            AcquisitionMenuCtrl()
            if acquisitionMenuCtrl is None
            else acquisitionMenuCtrl
        )

        # Connect to project signals for state management
        QgsProject.instance().projectSaved.connect(self.saveStateOnProject)
        self.iface.projectRead.connect(self.loadStateFromProject)

    def initGui(self):
        self.workflowToolBox = None
        self.addTool(
            self.showWorkflowToolBox,
            "validationtools.png",
            self.tr("Workflow Toolbox"),
            parentButton=self.stackButton,
            setDefaultAction=True,
        )

        self.addTool(
            self.acquisitionMenuCtrl.openMenuEditor,
            "customFeatureToolBox.png",
            self.tr("Custom Feature Tool"),
            parentButton=self.stackButton,
        )

        self.addTool(
            self.acquisitionMenuCtrl.clickReclassfyMode,
            "customFeatureToolBox.png",
            self.tr("Reclassify Mode"),
            withShortcut=True,
        )

        self.multiLayersCentroidsFlagToolBox = None
        self.addTool(
            self.showMultiLayersCentroidsFlagTool,
            "flags_centroids.png",
            self.tr("Inspect Multiple Layers Centroid Flags Toolbox"),
            parentButton=self.stackButton,
            setDefaultAction=False,
        )

        self.calcContour = None
        self.addTool(
            self.showCalcContourToolbox,
            "calccontour.png",
            self.tr("Assign Contour Values"),
        )
        self.codeList = None
        self.addTool(
            self.showCodeList,
            "codelist.png",
            self.tr("View Code List Codes and Values"),
        )
        self.complexWindow = None
        self.addTool(
            self.showComplexDock, "complex.png", self.tr("Build Complex Structures")
        )

        # Load state for current project
        self.loadStateFromProject()

    def addTool(
        self,
        callback,
        iconBaseName,
        text,
        setDefaultAction=False,
        parentButton=None,
        withShortcut=False,
    ):
        action = self.manager.add_action(
            os.path.join(self.iconBasePath, iconBaseName),
            text=text,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=withShortcut,
            parentMenu=self.parentMenu,
            parentButton=parentButton,
        )
        if setDefaultAction:
            self.stackButton.setDefaultAction(action)
        return action

    def unload(self):
        # Disconnect project signals
        try:
            QgsProject.instance().projectSaved.disconnect(self.saveStateOnProject)
            self.iface.projectRead.disconnect(self.loadStateFromProject)
        except:
            pass

        self.acquisitionMenuCtrl.unloadPlugin()

        # Unload MultiLayersCentroidsFlagDockWidget
        if self.multiLayersCentroidsFlagToolBox:
            self.multiLayersCentroidsFlagToolBox.unload()
            self.iface.removeDockWidget(self.multiLayersCentroidsFlagToolBox)
            del self.multiLayersCentroidsFlagToolBox

    def showCodeList(self):
        """
        Shows the Code list Dock
        """
        if self.codeList:
            self.iface.removeDockWidget(self.codeList)
        else:
            self.codeList = CodeList(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.codeList)

    def showCustomFeatureToolbox(self):
        """
        Shows the reclassification tool box dock
        """
        """ if self.cfToolbox:
            self.iface.removeDockWidget(self.cfToolbox)
        else:
            self.cfToolbox = CustomFeatureTool()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.cfToolbox) """
        pass

    def refreshWorkflowToolBoxObject(self):
        if self.workflowToolBox is not None:
            self.iface.removeDockWidget(self.workflowToolBox)
            del self.workflowToolBox
        self.workflowToolBox = WorkflowDockWidget(self.iface)
        return self.workflowToolBox

    def showWorkflowToolBox(self):
        """
        Shows/Hides the Quality Assurance Dock on main window.
        """
        if self.workflowToolBox:
            self.iface.removeDockWidget(self.workflowToolBox)
        else:
            self.workflowToolBox = WorkflowDockWidget(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.workflowToolBox)

    def showMultiLayersCentroidsFlagTool(self):
        if self.multiLayersCentroidsFlagToolBox is not None:
            self.iface.removeDockWidget(self.multiLayersCentroidsFlagToolBox)
        else:
            self.multiLayersCentroidsFlagToolBox = MultiLayersCentroidsFlagDockWidget(
                self.iface
            )
        self.iface.addDockWidget(
            Qt.RightDockWidgetArea, self.multiLayersCentroidsFlagToolBox
        )

    def showCalcContourToolbox(self):
        """
        Shows contour calculation dock.
        """
        if self.calcContour:
            self.iface.removeDockWidget(self.calcContour)
        else:
            self.calcContour = CalcContour(self.iface)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.calcContour)

    def showComplexDock(self):
        """
        Shows the Manage Complex features Dock
        """
        if self.complexWindow:
            self.iface.removeDockWidget(self.complexWindow)
        else:
            self.complexWindow = ComplexWindow(self.iface)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.complexWindow)

    def saveStateOnProject(self):
        """
        Saves the state of all toolboxes to the project.
        """
        currentProject = QgsProject.instance()
        toolStateDict = dict()

        # Save MultiLayersCentroidsFlagDockWidget state if it exists
        if self.multiLayersCentroidsFlagToolBox:
            toolStateDict[
                "MultiLayersCentroidsFlagDockWidget"
            ] = self.multiLayersCentroidsFlagToolBox.getToolState()

        # Save states for other toolboxes if needed in the future
        # if self.someOtherToolBox:
        #     toolStateDict["SomeOtherToolBox"] = self.someOtherToolBox.getToolState()

        # Store the state in project variables
        QgsExpressionContextUtils.setProjectVariable(
            currentProject,
            "dsgtools_toolboxes_state",
            json.dumps(toolStateDict),
        )

    def loadStateFromProject(self):
        """
        Loads the state of all toolboxes from the project.
        """
        state = json.loads(
            QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable(
                "dsgtools_toolboxes_state"
            )
            or "{}"
        )

        if state == {}:
            return

        # Load MultiLayersCentroidsFlagDockWidget state if it exists in the saved state
        if (
            "MultiLayersCentroidsFlagDockWidget" in state
            and self.multiLayersCentroidsFlagToolBox
        ):
            self.multiLayersCentroidsFlagToolBox.setToolState(
                state["MultiLayersCentroidsFlagDockWidget"]
            )

        # Load states for other toolboxes if needed in the future
        # if "SomeOtherToolBox" in state and self.someOtherToolBox:
        #     self.someOtherToolBox.setToolState(state["SomeOtherToolBox"])
