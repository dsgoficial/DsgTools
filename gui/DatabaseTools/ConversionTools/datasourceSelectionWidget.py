# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-05
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.PyQt import QtWidgets, uic

from DsgTools.gui.CustomWidgets.ConnectionWidgets.ServerConnectionWidgets.exploreServerWidget import ExploreServerWidget
from DsgTools.gui.DatabaseTools.ConversionTools.inputWizardPage import InputWizardPage

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceSelectionWidget.ui'))

class DatasourceSelectionWidget(QtWidgets.QWizard, FORM_CLASS):
    def __init__(self, manager, parentMenu, parent=None):
        """
        """
        super(DatasourceSelectionWidget, self).__init__()
        self.setupUi(self)
        self.manager = manager
        self.parentMenu = parentMenu
        self.parentButton = None
        self.sequenceDict = {'InputPage':1, 'OutputPage':2, 'MappingPage':3}
        self.setPage(self.sequenceDict['InputPage'], InputWizardPage(parent=parent))

    def initGui(self):
        """
        Instantiate GUI for user, including button shortcut (if necessary) and tool insertion on DSGTools tab on QGIS. 
        """
        callback = lambda : self.exec_() 
        self.manager.addTool(
            text=self.tr('Convert Databases'),
            callback=callback,
            parentMenu=self.parentMenu,
            icon='install.png',
            parentButton=self.parentButton,
            defaultButton=False
        )

    def unload(self):
        """
        Unloads GUI.
        """
        pass