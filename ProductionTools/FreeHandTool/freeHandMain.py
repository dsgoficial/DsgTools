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

from models.acquisitionFree import AcquisitionFree
from controllers.acquisitionFreeController import AcquisitionFreeController

class FreeHandMain:    

    def __init__(self, iface):
        #construtor
        self.iface = iface

    def setIface(self, iface):
        self.iface = iface 

    def getIface(self):
        return self.iface

    def setAction(self, action):
        self.action = action

    def getAction(self):
        return self.action

    def run(self, action):
        iface = self.getIface()
        self.acquisitionFree = AcquisitionFree(iface.mapCanvas())
        self.acquisitionFreeController = AcquisitionFreeController(
            self.acquisitionFree, 
            self.getAction(), 
            iface
        )
