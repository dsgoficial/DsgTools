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

from __future__ import absolute_import
from builtins import object
import os.path
import sys

from qgis.PyQt.QtCore import QObject, Qt

from .AttributeTools.code_list import CodeList
from .FieldToolBox.field_toolbox import FieldToolbox
from .ValidationToolbox.validation_toolbox import ValidationToolbox
from .ContourTool.calc_contour import CalcContour
from .ComplexTools.complexWindow import ComplexWindow

class ToolBoxesGuiManager(QObject):

    def __init__(self, manager, iface, parentMenu = None, toolbar = None, stackButton = None):
        """Constructor.
        """
        super(ToolBoxesGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.stackButton = stackButton
        self.iconBasePath = ':/plugins/DsgTools/icons/'
    
    def initGui(self):
        self.validationToolbox = ValidationToolbox(self.iface)
        self.validationToolbox.addTool(self.manager, self.showValidationToolbox, self.parentMenu, self.iconBasePath, self.stackButton)
        self.fieldToolbox = FieldToolbox(self.iface)
        self.fieldToolbox.addTool(self.manager, self.showFieldToolbox, self.parentMenu, self.iconBasePath, self.stackButton)
        self.calcContour = CalcContour(self.iface)
        self.calcContour.addTool(self.manager, self.showCalcContourToolbox, self.parentMenu, self.iconBasePath, self.stackButton)
        self.codeList = CodeList(self.iface)
        self.codeList.addTool(self.manager, self.showCodeList, self.parentMenu, self.iconBasePath, self.stackButton)
        self.complexWindow = ComplexWindow(self.iface)
        self.complexWindow.addTool(self.manager, self.showComplexDock, self.parentMenu, self.iconBasePath, self.stackButton)
    
    def unload(self):
        pass

    def showCodeList(self):
        """
        Shows the Code list Dock
        """
        if self.codeList:
            self.iface.removeDockWidget(self.codeList)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.codeList)

    def showFieldToolbox(self):
        """
        Shows the reclassification tool box dock
        """
        if self.fieldToolbox:
            self.iface.removeDockWidget(self.fieldToolbox)
        else:
            self.fieldToolbox = FieldToolbox(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.fieldToolbox)

    def showValidationToolbox(self):
        """
        Shows the Validation Dock
        """
        if self.validationToolbox:
            self.iface.removeDockWidget(self.validationToolbox)
        else:
            self.validationToolbox = ValidationToolbox(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.validationToolbox)

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
