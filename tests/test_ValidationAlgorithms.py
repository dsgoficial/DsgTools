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
        datasets = {
            "sqlite" : {
                "banco_capacitacao" : os.path.join(spatiaLitePaths, 'banco_capacitacao.sqlite')
            },
            "gpkg" : {
                "testes_wgs84" : os.path.join(gpkgPaths, 'testes_wgs84.gpkg'),
                "testes_sirgas2000_23s" : os.path.join(gpkgPaths, 'testes_sirgas2000_23s.gpkg'),
                "testes_sirgas2000_24s" : os.path.join(gpkgPaths, 'testes_sirgas2000_24s.gpkg'),
                "test_dataset_unbuild_polygons" : os.path.join(gpkgPaths, 'test_dataset_unbuild_polygons.gpkg')
            }
        }
        # switch-case for dataset reading
        funcs = {
            "sqlite" : lambda ds : self.readSpatiaLite(datasets["sqlite"][ds]),
            "gpkg" : lambda ds : self.readGeopackage(datasets["gpkg"][ds])
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

    def getInputLayers(self, driver, dataset, layers):
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
            out.append(vls[l])
        return out

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
                            'gpkg', 'testes_sirgas2000_24s', ['test1_vertexnearedge_a']
                        )[0],
                    'SEARCH_RADIUS':1,
                    'SELECTED': False
                },
                {
                    '__comment' : "'Normal' test: checks if it works with polygon.",
                    'FLAGS': "memory:",
                    'INPUT': self.getInputLayers(
                            'gpkg', 'testes_sirgas2000_24s', ['test2_vertexnearedge_l']
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
                            'gpkg', 'testes_sirgas2000_23s', ['camada_linha_1']
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
                        'gpkg', 'test_dataset_unbuild_polygons', ['vegetation']
                    )[0],
                    'SELECTED' : False,
                    'CONSTRAINT_LINE_LAYERS' : self.getInputLayers(
                        'gpkg', 'test_dataset_unbuild_polygons', ['fence', 'road']
                    ),
                    'CONSTRAINT_POLYGON_LAYERS' : self.getInputLayers(
                        'gpkg', 'test_dataset_unbuild_polygons', ['water']
                    ),
                    'GEOGRAPHIC_BOUNDARY' : '',
                    'OUTPUT_CENTER_POINTS' : "memory:",
                    'OUTPUT_BOUNDARIES' : "memory:"
                }
            ],

            "dsgtools:ALG" : [
                {
                    '__comment' : "'Normal' test: checks if it works."
                }
            ]
        }
        return parameters[algName] if algName in parameters else dict()

    def runAlg(self, algName, parameters, feedback=None, context=None):
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
            # out.setName(algName.split(':')[-1])
            return out
        return out
    
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
        path = os.path.join(
                    self.CURRENT_PATH, 'expected_outputs', algName.split(':')[-1],
                    'test_{0}.gpkg'.format(test)
                )
        if os.path.exists(path):
            if multipleOutputs:
                return self.readGeopackage(path)
            else:
                return QgsVectorLayer(
                            path, 
                            "{alg}_test_{test}_output".format(alg=algName.split(':')[-1], test=test),
                            "ogr"
                        )

    def compareLayers(self, target, reference):
        """
        Compares two vector layers. The algorithm stops on the first difference found.
        :param target: (QgsVectorLayer) layer to be checked.
        :param reference: (QgsVectorLayer) layer to be used as reference for comparison.
        :return: (str) message containing identified differences.
        """
        # geometry type check
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
            if fieldname == 'fid' or '_otf' in fieldname:
                # not sure if this should happen...
                continue
            if fieldname not in targetFieldNames:
                return "Incorrect set of attributes for output layer (missing '{attr}').".format(attr=fieldname)
        for featId, refFeat in refFeatDict.items():
            if featId not in targetFeatDict:
                return "Feature id={0} was not found on output layer.".format(featId)
            testFeat = targetFeatDict[featId]
            if not testFeat.geometry().equals(refFeat.geometry()):
                return "Feature {fid} has incorrect geometry.".format(fid=featId)
            for attr in targetFieldNames:
                if testFeat[attr] != refFeat[attr]:
                    return "Incorrect set of attributes for feature {fid}:\nAttribute {attr} in the test feature is: {test_attr}\nAttribute {attr} in the reference feature is: {ref_attr}".format(
                        fid=featId,
                        attr=attr,
                        test_attr=testFeat[attr],
                        ref_attr=refFeat[attr]
                    )
        return ""

    def testAlg(self, algName, feedback=None, context=None, loadLayers=False, multipleOutputs=False):
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
        if parameters == dict():
            return "Unable to read a set of parameters for {alg}'s tests.".format(
                    alg=algName
                )
        try:
            for i, param in enumerate(parameters):
                output = self.runAlgWithMultipleOutputs(algName, param, feedback, context) \
                    if multipleOutputs else self.runAlg(algName, param, feedback, context)
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
                        loadLayers=loadLayers
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
                            loadLayers=loadLayers
                        )
                        if isinstance(outputLyr, QgsVectorLayer):
                            output.rollBack()
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
    
    def compareInputLayerWithOutputLayer(self, i, algName, output, expected, loadLayers=False):
        if not output.isValid():
            raise Exception("Output is an INVALID vector layer.".\
                    format(alg=algName, nr=i + 1)
                )
        if expected is None:
            raise Exception("No expected output registered for the test, yet an output was generated.".\
                    format(alg=algName, nr=i + 1)
                )
        msg = self.compareLayers(output, expected)
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
        # for alg in self.readAvailableAlgs(self.DEFAULT_ALG_PATH):
        for alg in algs:
            try:
                results[alg] = self.testAlg(alg)
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
            self.testAlg("dsgtools:identifyvertexnearedges"), ""
        )
    
    # def test_overlayelementswithareas(self):
    #     self.assertEqual(
    #         self.testAlg("dsgtools:overlayelementswithareas"), ""
    #     )
    
    def test_deaggregategeometries(self):
        self.assertEqual(
            self.testAlg("dsgtools:deaggregategeometries"), ""
        )
    
    def test_dissolvepolygonswithsameattributes(self):
        self.assertEqual(
            self.testAlg("dsgtools:dissolvepolygonswithsameattributes"), ""
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
            self.testAlg("dsgtools:unbuildpolygonsalgorithm", multipleOutputs=True), ""
        )

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = 'test_' if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Tester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)