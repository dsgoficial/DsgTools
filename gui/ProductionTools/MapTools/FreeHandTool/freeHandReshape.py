#! -*- coding: utf-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin FreeHandEditting
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
from qgis.PyQt.QtCore import QObject
from .models.acquisitionFree import AcquisitionFree
from .controllers.acquisitionFreeController import AcquisitionFreeController
from .freeHandMain import FreeHandMain

class FreeHandReshape(FreeHandMain):    

    def __init__(self, iface):
        #construtor
        super(FreeHandReshape, self).__init__(iface)
        self.acquisitionFree.controlPressed = True

    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + 'free_hand_reshape.png'
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Free Hand Reshape'),
            callback=self.run,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip = self.tr('DSGTools: Free Hand Reshape\nReshapes polygon or line features from mouse movement.'),
            parentToolbar=parentMenu
        )
        self.setAction(action)
