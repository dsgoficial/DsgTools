# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-08
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

from qgis.PyQt.QtCore import QObject 
from .BDGExTools import BDGExTools

class BDGExGuiManager(QObject):

    def __init__(self, manager, iface, parentMenu = None, toolbar = None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(BDGExGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.BDGExTools = BDGExTools()
        self.menu = self.manager.addMenu(u'bdgex', self.tr('BDGEx'),'eb.png')
        self.iconBasePath = ':/plugins/DsgTools/icons/'
    
    def initGui(self):
        self.topocharts = self.manager.addMenu(u'topocharts', self.tr('Topographic Charts'),'eb.png', parentMenu = self.menu)
        self.coverageLyr = self.manager.addMenu(u'coverageLyr', self.tr('Coverage Layers'),'eb.png', parentMenu = self.menu)
        self.indexes = self.manager.addMenu(u'indexes', self.tr('Product Indexes'),'eb.png', parentMenu = self.menu)
        self.rasterIndex = self.manager.addMenu(u'rasterindex', self.tr('Topographic Charts'),'eb.png', parentMenu = self.indexes)
        self.vectorIndex = self.manager.addMenu(u'vectorindex', self.tr('Vectorial Charts'),'eb.png', parentMenu = self.indexes)
        self.loadMenus()

    def loadMenus(self):
        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kLayer,
            parent=self.topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        self.topocharts.addAction(action)
        
        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kLayer,
            parent=self.topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        self.topocharts.addAction(action)
        
        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kLayer,
            parent=self.topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        self.topocharts.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kLayer,
            parent=self.topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        self.topocharts.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('Landsat 7'),
            callback=self.loadLandsatLayer,
            parent=self.coverageLyr,
            add_to_menu=False,
            add_to_toolbar=False)
        self.coverageLyr.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('RapidEye'),
            callback=self.loadRapidEyeLayer,
            parent=self.coverageLyr,
            add_to_menu=False,
            add_to_toolbar=False)
        self.coverageLyr.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kRasterIndex,
            parent=self.rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kRasterIndex,
            parent=self.rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kRasterIndex,
            parent=self.rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kRasterIndex,
            parent=self.rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kVectorIndex,
            parent=self.vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kVectorIndex,
            parent=self.vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kVectorIndex,
            parent=self.vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.manager.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kVectorIndex,
            parent=self.vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        self.vectorIndex.addAction(action)

    def unload(self):
        pass

    def loadRapidEyeLayer(self):
        """
        Loads rapideye layer
        """
        urlWithParams = self.BDGExTools.getTileCache('RapidEye')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, 'RapidEye','wms')

    def loadLandsatLayer(self):
        """
        Loads landsat layer
        """
        urlWithParams = self.BDGExTools.getTileCache('Landsat7')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, 'Landsat7', 'wms')
    
    def loadMultiScaleLayer(self):
        """
        Loads landsat layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:MultiScale')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, 'MultiScale', 'wms')

    def load250kLayer(self):
        """
        Loads landsat layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:250k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:250k', 'wms')
    
    def load100kLayer(self):
        """
        Loads 100k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:100k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:100k', 'wms')

    def load50kLayer(self):
        """
        Loads 50k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:50k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:50k', 'wms')

    def load25kLayer(self):
        """
        Loads 25k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:25k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:25k', 'wms')

    def load250kRasterIndex(self):
        """
        Loads 250k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Raster Charts'), 'wms')

    def load100kRasterIndex(self):
        """
        Loads 100k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Raster Charts'), 'wms')

    def load50kRasterIndex(self):
        """
        Loads 50 raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Raster Charts'), 'wms')

    def load25kRasterIndex(self):
        """
        Loads 25k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Raster Charts'), 'wms')

    def load250kVectorIndex(self):
        """
        Loads 250k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Vectorial Charts'), 'wms')

    def load100kVectorIndex(self):
        """
        Loads 100k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Vectorial Charts'), 'wms')

    def load50kVectorIndex(self):
        """
        Loads 50k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Vectorial Charts'), 'wms')

    def load25kVectorIndex(self):
        """
        Loads 25k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Vectorial Charts'),'wms')
