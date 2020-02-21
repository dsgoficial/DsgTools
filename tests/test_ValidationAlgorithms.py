# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-07-04
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

"""
Script designed to test each validation algorithm from DSGTools 4.X.
It is supposed to be run through QGIS with DSGTools installed.
* This is merely a prototype for our unit test suite. *
"""

import os
import sys
import warnings
from osgeo import ogr

import processing
from qgis.utils import iface
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProcessingFeedback,\
                      QgsProcessingContext, QgsLayerTreeLayer, QgsProject
from qgis.PyQt.QtSql import QSqlDatabase

from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory
from qgis.testing import unittest

class Tester(unittest.TestCase):
    
    CURRENT_PATH = os.path.dirname(__file__)
    DEFAULT_ALG_PATH = os.path.join(
                            CURRENT_PATH, '..', 'core', 'DSGToolsProcessingAlgs',
                            'Algs', 'ValidationAlgs'
                        )
    datasets = dict()

    def readAvailableAlgs(self, path):
        """
        Reads all available .py files from a path. To get the algorithms,
        the path to the DSGTools algorithms should be passed.
        :param path: (str) path to DSGTools algorithms.
        :return: (list-of-str) list of all found algorithms.
        """
        return [
            "dsgtools:{0}".format(os.path.splitext(x)[0].lower()) for x in os.popen(
                "ls {path} | grep .py | grep -v __init__ | grep -v pycache".format(
                    path=path
                )
            ).readlines()
        ]

    def connectToSpatialite(self, path):
        """
        Stablishes connection to a SpatiaLite database.
        :param path: (str) path to the SpatiaLite database.
        # :return: (QSqlDatabase) the database object.
        :return: (AbstracDb) DSGTools database object.
        """
        db = None
        if os.path.exists(path):
            db = DbFactory().createDbFactory(driver=DsgEnums.DriverSpatiaLite)
            db.connectDatabase(conn=path)
        return db

    def setSqliteUri(self, uri, layer, geomColumn, sql, pkColumn='id'):
        """
        Configures the URI for a layer from a SpatiaLite dataset.
        :param uri: (QgsDataSourceUri) URI object to be configured.
        :param layer: (str) name for the layer to have its URI set.
        :param geomColumn: (str) name for the geometric column.
        :param sql: (str) query for feature filtering on layer load.
        :param pkColumn: (str) string containing all columns names for attributes
                         composing the table's primary key.
        """
        uri.setDataSource('', layer, geomColumn, sql, pkColumn)
        if sql == '':
            uri.disableSelectAtId(False)
        else:
            uri.disableSelectAtId(True)

    def readSpatiaLite(self, path):
        """
        Reads a SpatiaLite database and gets its vector layers.
        :param path: (str) path do the SpatiaLite database.
        :return: (dict) map to the SpatiaLite database's layers.
        """
        uri = QgsDataSourceUri()
        uri.setDatabase(path)
        db = self.connectToSpatialite(path)
        layerLoader = LayerLoaderFactory().makeLoader(iface, db)
        layers = dict()
        for l in list(db.listClassesWithElementsFromDatabase([]).keys()):
            layers[l] = layerLoader.getLayerByName(l)
        for l in db.listComplexClassesFromDatabase():
            layers[l] = layerLoader.getComplexLayerByName(l)
        return layers

    def readGeopackage(self, path):
        """
        Reads a Geopackage database.
        :param path: (str) path do the Geopackage database.
        :return: (dict) map to the Geopackage database's layers.
        """
        layers = dict()
        for layer in ogr.Open(path):
            layername = layer.GetName()
            layers[layername] = QgsVectorLayer(
                "{0}|layername={1}".format(path, layername), 
                layername,
                "ogr"
            )
        return layers

    def readGeojson(self, path):
        """
        Reads a folder with Geojson files.
        :param path: (str) path do the geojson folder.
        :return: (dict) map to the geojson folder's layers.
        """
        layers = dict()
        fileList = [f for f in next(os.walk(path))[2] if '.geojson' in f]
        for f in fileList:
            fullPath = os.path.join(path, f)
            for layer in ogr.Open(fullPath):
                layername = layer.GetName()
                layers[layername] = QgsVectorLayer(
                    fullPath,
                    layername,
                    "ogr"
                )
        return layers

    def testingDataset(self, driver, dataset):
        """
        Reads a dataset accordingly to its driver.
        :param driver: (str) driver's to be read.
        :param dataset: (str) dataset's name. If not given, a default one will
                        be given.
        :return: (dict) a map from layer name to vector layer read from database.
        """
        spatiaLitePaths = os.path.join(self.CURRENT_PATH, "testing_datasets", 'SpatiaLite')
        gpkgPaths = os.path.join(self.CURRENT_PATH, "testing_datasets", 'Geopackage')
        geojsonPaths = os.path.join(self.CURRENT_PATH, "testing_datasets", 'GeoJSON')
        datasets = {
            "sqlite" : {
                "banco_capacitacao" : os.path.join(spatiaLitePaths, 'banco_capacitacao.sqlite')
            },
            "gpkg" : {
                "testes_wgs84" : os.path.join(gpkgPaths, 'testes_wgs84.gpkg'),
                "testes_sirgas2000_23s" : os.path.join(gpkgPaths, 'testes_sirgas2000_23s.gpkg'),
                "test_dataset_unbuild_polygons" : os.path.join(gpkgPaths, 'test_dataset_unbuild_polygons.gpkg')
            },
            "geojson" : {
                "land_cover_layers" : os.path.join(geojsonPaths, 'land_cover_layers'),
                "terrain_model_layers" : os.path.join(geojsonPaths, 'terrain_model_layers'),
                "testes_sirgas2000_24s" : os.path.join(geojsonPaths, 'testes_sirgas2000_24s'),
                "spatial_rules_alg" : os.path.join(geojsonPaths, 'spatial_rules_alg')
            }
        }
        # switch-case for dataset reading
        funcs = {
            "sqlite" : lambda ds: self.readSpatiaLite(datasets["sqlite"][ds]),
            "gpkg" : lambda ds: self.readGeopackage(datasets["gpkg"][ds]),
            "geojson" : lambda ds: self.readGeojson(datasets["geojson"][ds])
        }
        layers = dict()
        if driver in datasets and dataset in datasets[driver]:
            key = "{driver}:{dataset}".format(driver=driver, dataset=dataset)
            if key not in self.datasets:
                self.datasets[key] = funcs[driver](dataset)
            else:
                [lyr.rollBack() for lyr in self.datasets[key].values()]
            layers = self.datasets[key]
        return layers

    def getInputLayers(self, driver, dataset, layers, addControlKey=False):
        """
        Gets the vector layers from an input dataset.
        :param driver: (str) driver's to be read.
        :param dataset: (str) dataset's name.
        :param layers: (list-of-str) layers to be read.
        :return: (list-of-QgsVectorLayer) vector layers read from the dataset.
        """
        out = []
        vls = self.testingDataset(driver, dataset)
        for l in layers:
            vls[l].rollBack()
            lyr = vls[l] if not addControlKey else \
                self.addControlKey(vls[l])
            out.append(lyr)
        return out
    
    def addControlKey(self, lyr):
        return processing.run(
                    'native:addautoincrementalfield',
                    {
                        'INPUT' : lyr,
                        'FIELD_NAME' : 'AUTO',
                        'START' : 0,
                        'GROUP_FIELDS' : [],
                        'SORT_EXPRESSION' : '',
                        'SORT_ASCENDING' : True,
                        'SORT_NULLS_FIRST' : False,
                        'OUTPUT' : 'memory:'
                    },
                    context = QgsProcessingContext(),
                    feedback = QgsProcessingFeedback()
                )['OUTPUT']

    def addLayerToGroup(self, layer, groupname):
        """
        Adds a layer to a group.
        :param layer: (QgsMapLayer) layer to be added to canvas.
        :param groupname: (str) name for group to nest the layer.
        """
        root = QgsProject.instance().layerTreeRoot()
        for g in root.children():
            if g.name() == groupname:
                group = g
                break
        else:
            group = root.addGroup(groupname)
        QgsProject.instance().addMapLayer(layer, False)
        group.insertChildNode(1, QgsLayerTreeLayer(layer))

    def algorithmParameters(self, algName):
        """
        Gets an algorithm's set of parameters for every test registered.
        :param algName: (str) target algorithm's name.
        :return: (list-of-dict) list of sets - maps -  of parameters to an algorithm's
                 tests.
        """
        parameters = {
            "dsgtools:identifyduplicatedfeatures" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'FLAGS' : "memory:",
                    'IGNORE_PK_FIELDS' : True,
                    'IGNORE_VIRTUAL_FIELDS' : True,
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao',
                            ['cb_rel_ponto_cotado_altimetrico_p']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:identifyoutofboundsangles" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_terreno_suj_inundacao_a']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 10
                }
            ],

            "dsgtools:identifyoutofboundsanglesincoverage" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUTLAYERS' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_trecho_drenagem_l']
                        ),
                    'SELECTED' : False,
                    'TOLERANCE' : 10
                }
            ],

            "dsgtools:identifygaps" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_terreno_suj_inundacao_a']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:identifyandfixinvalidgeometries" : [
                {
                    '__comment' : "'Normal' test: checks if it works. This test does not check fixes!",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_veg_campo_a']
                        )[0],
                    'IGNORE_CLOSED' : False,
                    'SELECTED' : False,
                    'TYPE' : False
                }
            ],

            "dsgtools:identifyduplicatedgeometries" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_rel_ponto_cotado_altimetrico_p']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:identifyduplicatedlinesoncoverage" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUTLAYERS' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao',
                            ['cb_hid_corredeira_l', 'cb_hid_trecho_drenagem_l']
                        ),
                    'SELECTED' : False
                }
            ],

            "dsgtools:identifysmalllines" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_trecho_drenagem_l']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 5
                }
            ],

            "dsgtools:identifyduplicatedpolygonsoncoverage" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUTLAYERS' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao',
                            ['cb_veg_campo_a', 'cb_veg_floresta_a']
                        ),
                    'SELECTED' : False
                    
                }
            ],

            "dsgtools:identifysmallpolygons" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS': 'memory:',
                    'INPUT': self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_veg_campo_a']
                        )[0],
                    'SELECTED': False,
                    'TOLERANCE': 625
                }
            ],

            "dsgtools:identifydangles" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'IGNOREINNER' : False,
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_trecho_drenagem_l']
                        )[0],
                    'LINEFILTERLAYERS' : '',
                    'POLYGONFILTERLAYERS' : '',
                    'SELECTED' : False,
                    'TOLERANCE' : 2,
                    'TYPE' : False
                }
            ],

            "dsgtools:identifyduplicatedpointsoncoverage" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUTLAYERS' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao',
                            ['cb_adm_edif_pub_civil_p', 'cb_rel_ponto_cotado_altimetrico_p']
                        ),
                    'SELECTED' : False
                }
            ],

            "dsgtools:identifyoverlaps" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS': "memory:",
                    'INPUT': self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_ilha_a']
                        )[0],
                    'SELECTED': False
                }
            ],
            "dsgtools:identifyvertexnearedges" : [
                {
                    '__comment' : "'Normal' test: checks if it works with polygon.",
                    'FLAGS': "memory:",
                    'INPUT': self.getInputLayers(
                            'geojson', 'testes_sirgas2000_24s', ['test1_vertexnearedge_a']
                        )[0],
                    'SEARCH_RADIUS':1,
                    'SELECTED': False
                },
                {
                    '__comment' : "'Normal' test: checks if it works with polygon.",
                    'FLAGS': "memory:",
                    'INPUT': self.getInputLayers(
                            'geojson', 'testes_sirgas2000_24s', ['test2_vertexnearedge_l']
                        )[0],
                    'SEARCH_RADIUS':1,
                    'SELECTED': False
                }
            ],
            "dsgtools:removeduplicatedfeatures" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'IGNORE_PK_FIELDS' : True,
                    'IGNORE_VIRTUAL_FIELDS' : True,
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_rel_ponto_cotado_altimetrico_p']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:removeduplicatedgeometries" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'FLAGS' : 'memory:',
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_rel_ponto_cotado_altimetrico_p']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:removesmalllines" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_trecho_drenagem_l']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 5
                }
            ],

            "dsgtools:removesmallpolygons" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_veg_campo_a']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 625
                }
            ],
            
            "dsgtools:overlayelementswithareas" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'BEHAVIOR' : 0,
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_1']
                        )[0],
                    'OVERLAY' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_poligono_1']
                        )[0],
                    'SELECTED' : False,
                    'SELECTED_OVERLAY' : False
                }
            ],

            "dsgtools:deaggregategeometries" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_1'], addControlKey=True
                        )[0],
                    'SELECTED' : False
                }
            ],
            
            "dsgtools:dissolvepolygonswithsameattributes" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'IGNORE_PK_FIELDS' : True,
                    'IGNORE_VIRTUAL_FIELDS' : True,
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_poligono_1']
                        )[0],
                    'MIN_AREA' : None,
                    'SELECTED' : False
                }
            ],

            "dsgtools:removeemptyandupdate" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_2']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:lineonlineoverlayer" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_4']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 1
                }
            ],

            "dsgtools:mergelineswithsameattributeset" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'ATTRIBUTE_BLACK_LIST' : ['OGC_FID'],
                    'IGNORE_NETWORK' : True,
                    'IGNORE_PK_FIELDS' : True,
                    'IGNORE_VIRTUAL_FIELDS' : True,
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_3']
                        )[0],
                    'SELECTED' : False
                }
            ],

            "dsgtools:snaplayeronlayer" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'BEHAVIOR' : 0,
                    'INPUT' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_poligono_1']
                        )[0],
                    'REFERENCE_LAYER' : self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_23s', ['camada_poligono_2']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 25
                }
            ],

            "dsgtools:adjustnetworkconnectivity" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT' : self.getInputLayers(
                            'sqlite', 'banco_capacitacao', ['cb_hid_trecho_drenagem_l']
                        )[0],
                    'SELECTED' : False,
                    'TOLERANCE' : 2
                }
            ],

            "dsgtools:identifyunsharedvertexonintersectionsalgorithm" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT_LINES' : self.getInputLayers(
                        'gpkg', 'testes_wgs84', ['line_input']
                    )[0],
                    'INPUT_POLYGONS' : self.getInputLayers(
                        'gpkg', 'testes_wgs84', ['polygon_input']
                    )[0],
                    'SELECTED' : False,
                    'FLAGS' : "memory:"
                }
            ],

            "dsgtools:unbuildpolygonsalgorithm" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    'INPUT_POLYGONS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['vegetation']
                    )[0],
                    'SELECTED' : False,
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_CENTER_POINTS' : "memory:",
                    'OUTPUT_BOUNDARIES' : "memory:"
                }
            ],
            "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm" : [
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test1']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test2']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test3']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test4']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test5']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 6 - same as test 1, but with geo bounds",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test1']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries_within_geo_bounds']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['geographic_bounds']
                    )[0],
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 7 - same as test 2, but with geo bounds",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test2']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries_within_geo_bounds']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['geographic_bounds']
                    )[0],
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 8 - same as test 3, but with geo bounds",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test3']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries_within_geo_bounds']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['geographic_bounds']
                    )[0],
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 9 - same as test 4, but with geo bounds",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test4']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries_within_geo_bounds']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['geographic_bounds']
                    )[0],
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 10 - same as test 5, but with geo bounds",
                    "INPUT_CENTER_POINTS" : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['center_points_test5']
                    )[0],
                    'SELECTED' : False,
                    'ATTRIBUTE_BLACK_LIST' : [],
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['fence', 'road', 'boundaries_within_geo_bounds']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : self.getInputLayers(
                        'geojson', 'land_cover_layers', ['geographic_bounds']
                    )[0],
                    'OUTPUT_POLYGONS' : "memory:",
                    'FLAGS' : "memory:"
                }  
            ],
            "dsgtools:identifyterrainmodelerrorsalgorithm" : [
                {
                    '__comment' : "test 1",
                    "INPUT" : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['contours_test1']
                    )[0],
                    'SELECTED' : False,
                    'CONTOUR_ATTR':'contour',
                    'CONTOUR_INTERVAL':10,
                    'TOPOLOGY_RADIUS':2,
                    'GEOGRAPHIC_BOUNDS' : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['geographic_bounds_test1']
                    )[0],
                    'POINT_FLAGS' : "memory:",
                    'LINE_FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 2",
                    "INPUT" : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['contours_test2']
                    )[0],
                    'SELECTED' : False,
                    'CONTOUR_ATTR':'contour',
                    'CONTOUR_INTERVAL':10,
                    'TOPOLOGY_RADIUS':2,
                    'GEOGRAPHIC_BOUNDS' : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['geographic_bounds_test2']
                    )[0],
                    'POINT_FLAGS' : "memory:",
                    'LINE_FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 3",
                    "INPUT" : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['contours_test3']
                    )[0],
                    'SELECTED' : False,
                    'CONTOUR_ATTR':'contour',
                    'CONTOUR_INTERVAL':10,
                    'TOPOLOGY_RADIUS':2,
                    'GEOGRAPHIC_BOUNDS' : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['geographic_bounds_test3']
                    )[0],
                    'POINT_FLAGS' : "memory:",
                    'LINE_FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 4",
                    "INPUT" : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['contours_test4']
                    )[0],
                    'SELECTED' : False,
                    'CONTOUR_ATTR':'contour',
                    'CONTOUR_INTERVAL':10,
                    'TOPOLOGY_RADIUS':2,
                    'GEOGRAPHIC_BOUNDS' : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['geographic_bounds_test4']
                    )[0],
                    'POINT_FLAGS' : "memory:",
                    'LINE_FLAGS' : "memory:"
                },
                {
                    '__comment' : "test 5",
                    "INPUT" : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['contours_test5']
                    )[0],
                    'SELECTED' : False,
                    'CONTOUR_ATTR':'contour',
                    'CONTOUR_INTERVAL':10,
                    'TOPOLOGY_RADIUS':2,
                    'GEOGRAPHIC_BOUNDS' : self.getInputLayers(
                        'geojson', 'terrain_model_layers', ['geographic_bounds_test5']
                    )[0],
                    'POINT_FLAGS' : "memory:",
                    'LINE_FLAGS' : "memory:"
                }
            ],
                    # '__comment' : "'Normal' test: checks if it works."

            "dsgtools:enforcespatialrules" : [
                {
                    '__comment' : "Tests 1 - tests every single topological relation to its simplest state",
                    "RULES_SET":[
                        {
                            "cardinality": "1..1",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "rel_pico_p",
                            "layer_b": "rel_ponto_cotado_altimetrico_p",
                            "name": "Pico deve estar em cima de um ponto cotado",
                            "predicate": 0
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "rel_ponto_cotado_altimetrico_p",
                            "layer_b": "hid_massa_dagua_a",
                            "name": "Pontos cotados altimétricos não podem estar sobre massa d’água",
                            "predicate": 2
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "enc_torre_energia_p",
                            "layer_b": "enc_trecho_energia_l",
                            "name": "Torres de energia devem estar sobre um ou mais trechos de energia",
                            "predicate": 3
                        },
                        {
                            "cardinality": "2..2",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_barragem_p",
                            "layer_b": "hid_trecho_drenagem_l",
                            "name": "Barragens tipo ponto estão entre 2 e somente trechos de drenagem",
                            "predicate": 5
                        },
                        {
                            "cardinality": "1..1",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "veg_brejo_pantano_a",
                            "layer_b": "hid_area_umida_a",
                            "name": "Brejo/Pantano deve estar contido por uma Área Úmida",
                            "predicate": 9
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "\"modaluso\" = '5'",
                            "filter_b": "",
                            "layer_a": "tra_ponte_l",
                            "layer_b": "fer_trecho_ferroviario_l",
                            "name": "O modalUso de Ponte deve ser Ferroviario se esta intersectar um Trecho Ferroviario.",
                            "predicate": 3
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "\"modaluso\" != '5'",
                            "filter_b": "",
                            "layer_a": "tra_ponte_l",
                            "layer_b": "fer_trecho_ferroviario_l",
                            "name": "O modalUso de Ponte deve ser Ferroviario se esta intersectar um Trecho Ferroviario.",
                            "predicate": 4
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_trecho_drenagem_l",
                            "layer_b": "hid_vala_l",
                            "name": "Valas não são sobrepostas por drenagens",
                            "predicate": 12
                        },
                        {
                            "cardinality": "0..1",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_barragem_a",
                            "layer_b": "hid_trecho_drenagem_l",
                            "name": "Barragens do tipo área contêm até uma drenagem",
                            "predicate": 13
                        },
                        {
                            "cardinality": "0..1",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas",
                            "layer_b": "poligonos",
                            "name": "Teste: 'linhas' não cruza 'poligonos'",
                            "predicate": 7
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos_2",
                            "layer_b": "poligonos",
                            "name": "Teste: 'poligonos_2' sobrepõe 'poligonos'",
                            "predicate": 11
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas_2",
                            "layer_b": "linhas",
                            "name": "Teste: 'linhas_2' não é igual a 'linhas'",
                            "predicate": 1
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'poligonos' não toca 'poligonos_2'",
                            "predicate": 6
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas_2",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'linhas_2' não cruza 'poligonos_2'",
                            "predicate": 8
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "points",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'points' não está contido em 'poligonos_2'",
                            "predicate": 10
                        },
                        {
                            "cardinality": "1..*",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos_2",
                            "layer_b": "points",
                            "name": "Teste: 'poligonos_2' não contém 'points'",
                            "predicate": 14
                        }
                    ],
                    "POINT_FLAGS":"memory:",
                    "LINE_FLAGS":"memory:",
                    "POLYGON_FLAGS":"memory:"
                }
            ],

            "dsgtools:ALG" : [
                {
                    '__comment' : "'Normal' test: checks if it works."
                }
            ]
        }
        return parameters[algName] if algName in parameters else dict()

    def runAlg(self, algName, parameters, feedback=None, context=None, addControlKey=False):
        """
        Executes a given algorithm.
        :param algName: (str) target algorithm's name.
        :param parameters: (dict) set of arguments for target algorithm.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental parameters.
        """
        out = processing.run(algName, parameters, None,\
                    feedback or QgsProcessingFeedback(),
                    context or QgsProcessingContext()
                )
        outputstr = 'FLAGS' if 'FLAGS' in out else 'OUTPUT' if 'OUTPUT' in out else ''
        if outputstr:
            out = out[outputstr]
        return out if not addControlKey else self.addControlKey(out)
    
    def runAlgWithMultipleOutputs(self, algName, parameters, feedback=None, context=None):
        """
        Executes a given algorithm that has multiple outputs. Returns a dict 
        with the returned layers in the format {'OUTPUT_LAYER_KEY':(QgsVectorLayer) OutputLayer}
        :param algName: (str) target algorithm's name.
        :param parameters: (dict) set of arguments for target algorithm.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental parameters.
        """
        return processing.run(algName, parameters, None,\
                    feedback or QgsProcessingFeedback(),
                    context or QgsProcessingContext()
                )

    def expectedOutput(self, algName, test, multipleOutputs=False):
        """
        Gets the expect output layer.
        :param algName: (str) target algorithm's name.
        :param test: (int) test being run.
        :return: (QgsVectorLayer) expected output layer.
        """
        rootPath = os.path.join(
            self.CURRENT_PATH, 'expected_outputs', algName.split(':')[-1]
        )
        gpkgOutput = False
        for f in next(os.walk(rootPath))[2]:
            if '.gpkg' in f:
                gpkgOutput = True
                break
        path = os.path.join(
                    rootPath,
                    'test_{test_number}{extension}'.format(
                        test_number=test,
                        extension='.gpkg' if gpkgOutput else ''
                        )
                )
        if os.path.exists(path):
            if multipleOutputs:
                return self.readGeopackage(path) if gpkgOutput else self.readGeojson(path)
            else:
                path = path if gpkgOutput else os.path.join(
                    path,
                    'test_{test_number}.geojson'.format(test_number=test)
                )
                return QgsVectorLayer(
                            path, 
                            "{alg}_test_{test}_output".format(alg=algName.split(':')[-1], test=test),
                            "ogr"
                        )

    def compareLayers(self, target, reference, attributeBlackList=None, addControlKey=False):
        """
        Compares two vector layers. The algorithm stops on the first difference found.
        :param target: (QgsVectorLayer) layer to be checked.
        :param reference: (QgsVectorLayer) layer to be used as reference for comparison.
        :return: (str) message containing identified differences.
        """
        # geometry type check
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        attributeBlackList += ['AUTO'] if addControlKey else []
        if target.featureCount() == 0 and reference.featureCount() == 0:
            return ""
        if target.geometryType() != reference.geometryType():
            return "Incorrect geometry type for the output layer."
        # feature check
        targetFeatDict = {f.id():f for f in target.getFeatures()}
        refFeatDict = {f.id():f for f in reference.getFeatures()}
        targetFeaureIds = set(targetFeatDict.keys())
        refFeaureIds = set(refFeatDict.keys())
        if target.featureCount() != reference.featureCount():    
            msg = ""
            if targetFeaureIds - refFeaureIds:
                msg += "Output layer has more features than the control layer (Exceeding ID: {idlist}).\n".format(
                        idlist=", ".join(map(str, targetFeaureIds - refFeaureIds))
                    )
            if refFeaureIds - targetFeaureIds:
                msg += "Output layer has fewer features than the control layer (Missing ID: {idlist}).".format(
                        idlist=", ".join(map(str, refFeaureIds - targetFeaureIds))
                    )
            return msg
        # attribute names check
        targetFieldNames = [f.name() for f in target.fields()]
        for f in reference.fields():
            fieldname = f.name()
            if fieldname in ['fid', 'AUTO'] or '_otf' in fieldname:
                # not sure if this should happen...
                continue
            if fieldname not in targetFieldNames:
                return "Incorrect set of attributes for output layer (missing '{attr}').".format(attr=fieldname)
        for featId, refFeat in refFeatDict.items():
            if featId not in targetFeatDict:
                return "Feature id={0} was not found on output layer.".format(featId)
            testFeat = targetFeatDict[featId]
            if not (testFeat.geometry().isGeosEqual(refFeat.geometry()) or\
                testFeat.geometry().equals(refFeat.geometry())):
                return "Feature {fid} has incorrect geometry.".format(fid=featId)
            for attr in targetFieldNames:
                if attr not in attributeBlackList and testFeat[attr] != refFeat[attr]:
                    return "Incorrect set of attributes for feature {fid}:\nAttribute {attr} in the test feature is: {test_attr}\nAttribute {attr} in the reference feature is: {ref_attr}".format(
                        fid=featId,
                        attr=attr,
                        test_attr=testFeat[attr],
                        ref_attr=refFeat[attr]
                    )
        return ""

    def loadLayerToCanvas(self, layer):
        """
        Load a layer to canvas in order for it to be accessible using the
        processing context.
        :param layer: (QgsVectorLayer) layer object to be loaded to canvas.
        """
        QgsProject.instance().addMapLayer(layer, True)

    def clearProject(self):
        """
        Clears all loaded layers from canvas.
        """
        QgsProject.instance().clear()

    def testAlg(self, algName, feedback=None, context=None, loadLayers=False, multipleOutputs=False, attributeBlackList=None, addControlKey=False):
        """
        Tests if the output of a given algorithm is the expected one.
        :param algName: (str) target algorithm's name.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental parameters.
        :param loadLayers: (bool) indicates whether expected and output layers
                            should be loaded to canvas.
        :return: (str) failing reason.
        """
        parameters = self.algorithmParameters(algName)
        context = context or QgsProcessingContext()
        context.setProject(QgsProject.instance())
        if parameters == dict():
            return "Unable to read a set of parameters for {alg}'s tests.".format(
                    alg=algName
                )
        try:
            for i, param in enumerate(parameters):
                output = self.runAlgWithMultipleOutputs(algName, param, feedback, context) \
                    if multipleOutputs else self.runAlg(algName, param, feedback, context, addControlKey=addControlKey)
                expected = self.expectedOutput(
                    algName,
                    i + 1,
                    multipleOutputs=multipleOutputs
                )
                if isinstance(output, QgsVectorLayer):
                    self.compareInputLayerWithOutputLayer(
                        i,
                        algName,
                        output,
                        expected,
                        loadLayers=loadLayers,
                        attributeBlackList=attributeBlackList,
                        addControlKey=addControlKey
                    )
                    if isinstance(output, QgsVectorLayer):
                        output.rollBack()
                    if isinstance(expected, QgsVectorLayer):
                        expected.rollBack()
                elif isinstance(output, dict):
                    for key, outputLyr in output.items():
                        if key not in expected:
                            raise Exception("Output dictionary key was not found in expected output dictionary.".\
                                format(alg=algName, nr=i + 1)
                            )
                        self.compareInputLayerWithOutputLayer(
                            i,
                            algName,
                            outputLyr,
                            expected[key],
                            loadLayers=loadLayers,
                            addControlKey=addControlKey,
                            attributeBlackList=attributeBlackList
                        )
                        if isinstance(outputLyr, QgsVectorLayer):
                            outputLyr.rollBack()
                        if isinstance(expected[key], QgsVectorLayer):
                            expected[key].rollBack()
                    for key, expectedLyr in expected.items():
                        if key not in expected:
                            raise Exception("Output dictionary key was not found in expected output dictionary.".\
                                format(alg=algName, nr=i + 1)
                            )

        except Exception as e:
            if isinstance(output, QgsVectorLayer):
                output.rollBack()
            elif isinstance(output, dict):
                [lyr.rollBack() for key, lyr in output.items() if isinstance(lyr, QgsVectorLayer)]
            if isinstance(expected, QgsVectorLayer):
                expected.rollBack()
            elif isinstance(expected, dict):
                [lyr.rollBack() for key, lyr in expected.items() if isinstance(lyr, QgsVectorLayer)]
            return "Test #{nr} for '{alg}' has failed:\n'{msg}'".format(
                    msg=", ".join(map(str, e.args)), nr=i + 1, alg=algName
                )
        # missing the output testing
        return ""
    
    def compareInputLayerWithOutputLayer(self, i, algName, output, expected, loadLayers=False, attributeBlackList=None, addControlKey=False):
        if not output.isValid():
            raise Exception("Output is an INVALID vector layer.".\
                    format(alg=algName, nr=i + 1)
                )
        if expected is None:
            raise Exception("No expected output registered for the test, yet an output was generated.".\
                    format(alg=algName, nr=i + 1)
                )
        expected = self.addControlKey(expected) if addControlKey else expected
        msg = self.compareLayers(output, expected, attributeBlackList=attributeBlackList, addControlKey=addControlKey)
        # once layer is compared, revert all modifications in order to not compromise layer reusage
        if isinstance(output, QgsVectorLayer):
            output.rollBack()
        if isinstance(expected, QgsVectorLayer):
            expected.rollBack()
        if msg:
            raise Exception(msg)
        if loadLayers:
            self.addLayerToGroup(output, "DSGTools Algorithm Tests")
            self.addLayerToGroup(expected, "DSGTools Algorithm Tests")

    def testAllAlgorithms(self):
        """
        Executes all registered tests. Note that algorithms run in here should only
        output one layer.
        :return: (dict) a map to the algorithm found and all tests and their results.
        """
        # still missing how to define default datasets
        results = dict()
        algs = [
                # identification algs
                "dsgtools:identifyoutofboundsangles", "dsgtools:identifyoutofboundsanglesincoverage",
                "dsgtools:identifygaps", "dsgtools:identifyandfixinvalidgeometries",
                "dsgtools:identifyduplicatedfeatures", "dsgtools:identifyduplicatedgeometries",
                "dsgtools:identifyduplicatedlinesoncoverage", "dsgtools:identifysmalllines",
                "dsgtools:identifyduplicatedpolygonsoncoverage", "dsgtools:identifysmallpolygons",
                "dsgtools:identifydangles", "dsgtools:identifyduplicatedpointsoncoverage",
                "dsgtools:identifyoverlaps", "dsgtools:identifyvertexnearedges",
                "dsgtools:identifyunsharedvertexonintersectionsalgorithm"
                # correction algs
                "dsgtools:removeduplicatedfeatures", "dsgtools:removeduplicatedgeometries",
                "dsgtools:removesmalllines", "dsgtools:removesmallpolygons",
                # manipulation algs
                "dsgtools:lineonlineoverlayer", "dsgtools:mergelineswithsameattributeset",
                "dsgtools:overlayelementswithareas", "dsgtools:deaggregategeometries",
                "dsgtools:dissolvepolygonswithsameattributes", "dsgtools:removeemptyandupdate",
                "dsgtools:snaplayeronlayer",
                # network algs
                "dsgtools:adjustnetworkconnectivity"
            ]
        multipleOutputAlgs = [
            "dsgtools:unbuildpolygonsalgorithm",
            "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm"
        ]
        # for alg in self.readAvailableAlgs(self.DEFAULT_ALG_PATH):
        for alg in algs:
            try:
                results[alg] = self.testAlg(alg)
            except KeyError:
                results[alg] = "No tests registered."
        for alg in multipleOutputAlgs:
            try:
                results[alg] = self.testAlg(
                    alg,
                    multipleOutputs=True,
                    attributeBlackList=['path']
                )
            except KeyError:
                results[alg] = "No tests registered."
        return results
    
    def test_identifyoutofboundsangles(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyoutofboundsangles"), ""
        )

    # def test_identifyoutofboundsanglesincoverage(self):
    #     with warnings.catch_warnings():
    #         warnings.simplefilter("ignore")
    #         self.assertEqual(
    #             self.testAlg("dsgtools:identifyoutofboundsanglesincoverage"), ""
    #         )

    # def test_identifygaps(self):
    #     with warnings.catch_warnings():
    #         warnings.simplefilter("ignore")
    #         self.assertEqual(
    #             self.testAlg("dsgtools:identifygaps"), ""
    #         )
    
    def test_identifyandfixinvalidgeometries(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyandfixinvalidgeometries"), ""
        )
    
    def test_identifyduplicatedfeatures(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyduplicatedfeatures"), ""
        )

    def test_identifyduplicatedgeometries(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyduplicatedgeometries"), ""
        )

    def test_identifyduplicatedlinesoncoverage(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyduplicatedlinesoncoverage"), ""
        )
    
    def test_identifyduplicatedpointsoncoverage(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyduplicatedpointsoncoverage"), ""
        )

    def test_identifysmalllines(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifysmalllines"), ""
        )

    def test_identifyduplicatedpolygonsoncoverage(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyduplicatedpolygonsoncoverage"), ""
        )

    def test_identifysmallpolygons(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifysmallpolygons"), ""
        )

    def test_identifydangles(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifydangles"), ""
        )

    def test_identifyunsharedvertexonintersectionsalgorithm(self):
        self.assertEqual(
            self.testAlg("dsgtools:identifyunsharedvertexonintersectionsalgorithm"), ""
        )
    
    def test_identifyvertexnearedges(self):
        self.assertEqual(
            self.testAlg(
                "dsgtools:identifyvertexnearedges",
                addControlKey=True,
                multipleOutputs=True
            ), ""
        )
    
    # def test_overlayelementswithareas(self):
    #     self.assertEqual(
    #         self.testAlg("dsgtools:overlayelementswithareas"), ""
    #     )
    
    def test_deaggregategeometries(self):
        self.assertEqual(
            self.testAlg("dsgtools:deaggregategeometries", addControlKey=True), ""
        )
    
    def test_dissolvepolygonswithsameattributes(self):
        self.assertEqual(
            self.testAlg("dsgtools:dissolvepolygonswithsameattributes", addControlKey=True), ""
        )
    
    def test_removeemptyandupdate(self):
        self.assertEqual(
            self.testAlg("dsgtools:removeemptyandupdate"), ""
        )
    
    def test_snaplayeronlayer(self):
        self.assertEqual(
            self.testAlg("dsgtools:snaplayeronlayer"), ""
        )

    def test_adjustnetworkconnectivity(self):
        self.assertEqual(
            self.testAlg("dsgtools:adjustnetworkconnectivity"), ""
        )
    
    def test_unbuildpolygonsalgorithm(self):
        self.assertEqual(
            self.testAlg(
                "dsgtools:unbuildpolygonsalgorithm",
                multipleOutputs=True,
                attributeBlackList=['path'],
                addControlKey=True
            ),
            ""
        )
    
    def test_buildpolygonsfromcenterpointsandboundariesalgorithm(self):
        self.assertEqual(
            self.testAlg(
                "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm",
                multipleOutputs=True,
                addControlKey=True
            ),
            ""
        )

    def test_identifyterrainmodelerrorsalgorithm(self):
        self.assertEqual(
            self.testAlg(
                "dsgtools:identifyterrainmodelerrorsalgorithm",
                multipleOutputs=True,
                addControlKey=True
            ),
            ""
        )
    
    def test_enforcespatialrules(self):
        """Tests for Enforce Spatial Rules algorithm"""
        testsParams = self.algorithmParameters("dsgtools:enforcespatialrules")
        # this algorithm, specifically, has to set layers Context-reading ready
        layers = self.testingDataset("geojson", "spatial_rules_alg")
        for lyrName, lyr in layers.items():
            self.loadLayerToCanvas(lyr)
        msg = self.testAlg(
                "dsgtools:enforcespatialrules",
                multipleOutputs=True,
                addControlKey=True
            )
        del self.datasets["geojson:spatial_rules_alg"]
        self.clearProject()
        self.assertEqual(
            msg,
            ""
        )

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = 'test_' if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Tester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
