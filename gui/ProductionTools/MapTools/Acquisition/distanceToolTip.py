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

from qgis.core import QgsDistanceArea, QgsCoordinateTransformContext

from DsgTools.gui.ProductionTools.MapTools.Acquisition.toolTip import ToolTip

class DistanceToolTip(ToolTip):
	def __init__(self, iface):
		super(DistanceToolTip, self).__init__(iface, minSegmentDistance)
		self.iface = iface
		self.canvas = iface.mapCanvas()      
		self.last_distance = 0  
		self.showing = False
		self.minSegmentDistance = minSegmentDistance

	def calculateDistance(self, p1, p2):
		distance = QgsDistanceArea()
		distance.setSourceCrs(self.iface.activeLayer().crs(), QgsCoordinateTransformContext())
		# Sirgas 2000
		distance.setEllipsoid('GRS1980')
		m = distance.measureLine(p1, p2) 
		return m

	def canvasMoveEvent(self, last_p, current_p):
		m =  int(self.calculateDistance(last_p, current_p))
		if self.showing:
			if m != self.last_distance:
				color = 'red'
				if m >= self.minSegmentDistance:
					color = 'green'				
				txt = "<p style='color:{color}'><b>{distance}</b></p>".format(color=color, distance=str(m))
				self.show(txt, current_p)		
				self.last_distance = m  
		else:
			if m > 1:
				color = 'red'
				if m >= self.minSegmentDistance:
					color = 'green'				
				txt = "<p style='color:{color}'><b>{distance}</b></p>".format(color=color, distance=str(m))
				super(DistanceToolTip, self).show(txt, current_p)		  	
				self.last_distance = m
				self.showing = True

	def deactivate(self):
		self.deactivate()
		self.showing = False
