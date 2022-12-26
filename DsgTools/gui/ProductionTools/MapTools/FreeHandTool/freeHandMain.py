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


class FreeHandMain(QObject):
    def __init__(self, iface):
        # construtor
        super(FreeHandMain, self).__init__()
        self.iface = iface
        self.acquisitionFree = AcquisitionFree(iface)
        self.acquisitionFreeController = AcquisitionFreeController(
            self.acquisitionFree, iface
        )

    def addTool(
        self,
        manager,
        callback,
        parentMenu,
        iconBasePath,
        parentButton=None,
        defaultButton=False,
    ):
        self.parentButton = parentButton
        icon_path = iconBasePath + "free_hand.png"
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Free Hand Acquisition"),
            callback=self.run,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=self.tr(
                "DSGTools: Free Hand Acquisition\nAcquires polygon or line features from mouse movement."
            ),
            parentToolbar=parentMenu,
            parentButton=parentButton,
        )
        self.setAction(action)
        if defaultButton:
            self.parentButton.setDefaultAction(action)

    def setAcquisitionFreeController(self, acquisitionFreeController):
        self.acquisitionFreeController = acquisitionFreeController

    def getAcquisitionFreeController(self):
        return self.acquisitionFreeController

    @property
    def toolAction(self):
        return self.getAction()

    def setIface(self, iface):
        self.iface = iface

    def getIface(self):
        return self.iface

    def registerActionOnController(self, action):
        acquisitionFreeController = self.getAcquisitionFreeController()
        acquisitionFreeController.setActionAcquisitionFree(action)

    def setAction(self, action):
        self.registerActionOnController(action)
        self.action = action

    def getAction(self):
        return self.action

    def run(self):
        try:
            self.parentButton.setDefaultAction(self.action)
        except:
            pass
