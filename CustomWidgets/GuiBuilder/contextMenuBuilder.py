# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-05-15
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
import os

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QColor, QMenu


class ContextMenuBuilder(QtCore.QObject):
    def __init__(self, parent = None):
        """Constructor."""
        super(ContextMenuBuilder, self).__init__(parent)
        self.parent = parent
    
    def createMenu(self, e, parentMenu, menuDict, genericAction, selectAll = False):
        pass
    
    def getCallback(self):
        pass
    
    def addMenu(self, parentMenu, newTitle):
        """
        Adds a new menu with title newTitle to parentMenu and returns the new menu
        """
        newMenu = QtGui.QMenu(title=title)
        parentMenu.addMenu(newMenu)
        return newMenu
    
    def addAction(self, menu, action):
        return menu.addAction(action)
    
