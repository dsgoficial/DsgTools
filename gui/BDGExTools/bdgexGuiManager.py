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
from functools import partial

from qgis.core import QgsVectorLayer, QgsProject
from qgis.PyQt.QtCore import QObject 
from DsgTools.core.NetworkTools.BDGExRequestHandler import BDGExRequestHandler

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
        self.BDGExRequestHandler = BDGExRequestHandler()
        self.menu = self.manager.addMenu(u'bdgex', self.tr('BDGEx'),'eb.png')
        self.iconBasePath = ':/plugins/DsgTools/icons/'
        self.availableServices = {
            'topocharts' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Multi scale mosaic'),
                    'layers' : [
                        'ctm25',
                        'ctm50',
                        'ctm100',
                        'ctm250'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS',
                    'separator' : True
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:250,000'),
                    'layers' : [
                        'ctm250'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:100,000'),
                    'layers' : [
                        'ctm100'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:50,000'),
                    'layers' : [
                        'ctm50'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:25,000'),
                    'layers' : [
                        'ctm25'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                }                
            ],
            'coverage' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Rapideye Imagery (2013 mosaic)'),
                    'layers' : [
                        'rapideye'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Landsat 7 Imagery (2000 mosaic)'),
                    'layers' : [
                        'landsat7'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Orthorectified True Color Imagery compatible with 1:25,000 scale'),
                    'layers' : [
                        'ortoimagem_scn25'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Artificial SAR Imagery compatible with 1:50,000 scale'),
                    'layers' : [
                        'ram_colorimetria_50'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Artificial SAR Imagery compatible with 1:25,000 scale'),
                    'layers' : [
                        'ram_colorimetria_25'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                }                     
            ],
            'terrain' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Surface Digital Model compatible with scale 1:25,000'),
                    'layers' : [
                        'mds25'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Contour lines compatible with scale 1:25,000'),
                    'layers' : [
                        'curva_nivel25'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS',
                    'separator' : True
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Surface Digital Model compatible with scale 1:50,000'),
                    'layers' : [
                        'mds50'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Contour lines compatible with scale 1:50,000'),
                    'layers' : [
                        'curva_nivel50'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS',
                    'separator' : True
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Contour lines compatible with scale 1:100,000'),
                    'layers' : [
                        'curva_nivel100'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Surface Digital Model compatible with scale 1:250,000 (SRTM)'),
                    'layers' : [
                        'mds250'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Contour lines compatible with scale 1:250,000'),
                    'layers' : [
                        'curva_nivel250'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS'
                }
            ],
            'aux_layers' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Brazilian Political Information'),
                    'layers' : [
                        'municipios',
                        'estados',
                        'capitais'
                    ],
                    'service' : 'mapcache',
                    'service_type' : 'WMS',
                    'separator' : True
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Brazilian Cities'),
                    'layers' : [
                        'municipios'
                    ],
                    'service' : 'auxlayers',
                    'service_type' : 'WFS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Brazilian States'),
                    'layers' : [
                        'estados'
                    ],
                    'service' : 'auxlayers',
                    'service_type' : 'WFS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('Brazilian State Capitals'),
                    'layers' : [
                        'capitais'
                    ],
                    'service' : 'auxlayers',
                    'service_type' : 'WFS'
                }
            ],
            'raster_mapindex' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:250,000'),
                    'layers' : [
                        'F250_WGS84_MATRICIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:100,000'),
                    'layers' : [
                        'F100_WGS84_MATRICIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:50,000'),
                    'layers' : [
                        'F50_WGS84_MATRICIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:25,000'),
                    'layers' : [
                        'F25_WGS84_MATRICIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                }
            ],
            'vector_mapindex' : [
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:250,000'),
                    'layers' : [
                        'F250_WGS84_VETORIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:100,000'),
                    'layers' : [
                        'F100_WGS84_VETORIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:50,000'),
                    'layers' : [
                        'F50_WGS84_VETORIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                },
                {
                    'icon' : ':/plugins/DsgTools/icons/eb.png',
                    'menu_entry' : self.tr('1:25,000'),
                    'layers' : [
                        'F25_WGS84_VETORIAL'
                    ],
                    'service' : 'mapindex',
                    'service_type' : 'WMS'
                }
            ]
        }

    
    def initGui(self):
        self.topocharts = self.manager.addMenu(u'topocharts', self.tr('Topographic Charts'),'eb.png', parentMenu = self.menu)
        self.load_menus('topocharts', self.topocharts)
        self.coverageLyr = self.manager.addMenu(u'coverageLyr', self.tr('Coverage Layers'),'eb.png', parentMenu = self.menu)
        self.load_menus('coverage', self.coverageLyr)
        self.terrainLyr = self.manager.addMenu(u'terrainLyr', self.tr('Terrain Information'),'eb.png', parentMenu = self.menu)
        self.load_menus('terrain', self.terrainLyr)
        self.auxLyr = self.manager.addMenu(u'auxLyr', self.tr('Auxiliar Information'),'eb.png', parentMenu = self.menu)
        self.load_menus('aux_layers', self.auxLyr)
        self.indexes = self.manager.addMenu(u'indexes', self.tr('Product Indexes'),'eb.png', parentMenu = self.menu)
        self.rasterIndex = self.manager.addMenu(u'rasterindex', self.tr('Topographic Charts'),'eb.png', parentMenu = self.indexes)
        self.load_menus('raster_mapindex', self.rasterIndex)
        self.vectorIndex = self.manager.addMenu(u'vectorindex', self.tr('Vectorial Charts'),'eb.png', parentMenu = self.indexes)
        self.load_menus('vector_mapindex', self.vectorIndex)

    def loadServiceLayer(self, legendName, service, layerList, serviceType='WMS'):
        urlWithParams = self.BDGExRequestHandler.get_url_string(service, layerList, serviceType)
        if not urlWithParams:
            return
        if serviceType == 'WMS':
            self.iface.addRasterLayer(urlWithParams, legendName, serviceType.lower())
        if serviceType == 'WFS':
            vlayer = QgsVectorLayer(urlWithParams, legendName, serviceType)
            QgsProject.instance().addMapLayer(vlayer)
    
    def load_menus(self, menu_type, parentMenu):
        for serviceDict in self.availableServices[menu_type]:
            callback = partial(
                self.loadServiceLayer,
                legendName=serviceDict['menu_entry'],
                service=serviceDict['service'],
                layerList=serviceDict['layers'],
                serviceType=serviceDict['service_type']
                )
            action = self.manager.add_action(
                icon_path=serviceDict['icon'],
                text=serviceDict['menu_entry'],
                callback= callback,
                parent=parentMenu,
                add_to_menu=False,
                add_to_toolbar=False
                )
            parentMenu.addAction(action)
            if 'separator' in serviceDict and serviceDict['separator']:
                parentMenu.addSeparator()

    def unload(self):
        pass
