# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Ronaldo Martins da Silva Junior - Cartographic Engineer @ Brazilian Army
        email                : ronaldomartins.silva@eb.mil.br
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

from PyQt5.QtWidgets import QToolTip

class ToolTip(object):
	def __init__(self, iface):
		self.iface = iface
		self.canvas = iface.mapCanvas()		
   		   
	def show(self, text, toolTipPoint):
		QToolTip.showText(self.canvas.mapToGlobal(self.canvas.mouseLastXY()),str(text), self.canvas)
        
	def deactivate(self):
		QToolTip.hideText()

