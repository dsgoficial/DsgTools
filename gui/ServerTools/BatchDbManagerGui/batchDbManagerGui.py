# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-11-06
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

from qgis.PyQt.QtCore import QObject

from DsgTools.gui.ServerTools.batchDbManager import BatchDbManager

class BatchDbManagerGui(QObject):
    
    def __init__(self, manager, parentMenu):
        """
        Class constructor.
        :param iface: (QgsInterface) interface to be used to send commands to QGIS
                      at runtime.
        :param parent: (QWidget) widget parent to this interface dialog.
        """
        super(BatchDbManagerGui, self).__init__()
        self.manager = manager
        self.parentMenu = parentMenu
        self.batchDbManager = BatchDbManager()

    def initGui(self):
        """
        Sets server tools to DSGTools/QGIS interface.
        """
        icon_path = ':/plugins/DsgTools/icons/server.png'
        action = self.manager.addTool(
            text=self.tr('Manage Databases from Server'),
            callback=self.openBatchDbManager,
            parentMenu=self.parentMenu,
            icon='server.png'
            )

    def openBatchDbManager(self):
        """
        Opens dialog.
        """
        self.batchDbManager.show()
        result = self.batchDbManager.exec_()

    def unload(self):
        """
        Removes GUI components.
        """
        pass