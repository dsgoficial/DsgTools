# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from PyQt4.QtCore import Qt
from DsgTools.DsgToolsOp.MilitaryTools.MilitarySimbologyTools.militarySimbologyDock import MilitarySimbologyDock

class ToolLoader:
    def __init__(self, parentMenu, parent, icon_path):
        self.parentMenu = parentMenu
        self.parent = parent
        self.icon_path = icon_path
    
    def loadTools(self):
        toolList = []
        action = self.parent.add_action(
            self.icon_path,
            text='Military Simbology',
            callback=self.loadMilitarySimbologyDock,
            parent=self.parentMenu,
            add_to_menu=False,
            add_to_toolbar=False)
        self.parentMenu.addAction(action)
        toolList.append(action) #sempre adicione o action na tool list, para cada tool

        return toolList

    
    def loadMilitarySimbologyDock(self):
        """
        Shows the Military Simbology Dock
        """
        if self.parent:
            if self.parent.militaryDock:
                self.parent.iface.removeDockWidget(self.parent.militaryDock)
            else:
                self.parent.militaryDock = MilitarySimbologyDock(self.parent.iface)
            self.parent.iface.addDockWidget(Qt.LeftDockWidgetArea, self.parent.militaryDock)
    
    def uninstallDsgToolsOp(self):
        """
        Uninstall dsgtoolsop
        """
        self.opInstaller.uninstallDsgToolsOp(self.iface)