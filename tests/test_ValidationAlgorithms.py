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
import re
import sys
import warnings
from osgeo import ogr

import processing
from qgis.utils import iface
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsLayerTreeLayer,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsCoordinateReferenceSystem,
)

from qgis.testing import unittest


def _normalize_geo_attr(val):
    """Normalize geometry-list attributes (e.g. 'reason') for order-independent comparison.

    Some algorithm outputs embed a comma-separated list of geometries (e.g.
    "near edge(s) LineString (...), LineString (...)") whose order depends on
    spatial-index traversal and is therefore non-deterministic. Sorting the
    individual geometry strings makes the comparison stable.
    """
    if not isinstance(val, str) or "near edge(s)" not in val:
        return val
    marker = "near edge(s) "
    idx = val.find(marker)
    if idx == -1:
        return val
    prefix = val[: idx + len(marker)]
    rest = val[idx + len(marker) :]
    trailing = ""
    if rest.endswith("."):
        rest = rest[:-1]
        trailing = "."
    edges = re.findall(r"[A-Z][a-zA-Z]+ \([^)]+\)", rest)
    if not edges:
        return val
    return prefix + ", ".join(sorted(edges)) + trailing


class Tester(unittest.TestCase):

    CURRENT_PATH = os.path.dirname(__file__)
    DEFAULT_ALG_PATH = os.path.join(
        CURRENT_PATH, "..", "core", "DSGToolsProcessingAlgs", "Algs", "ValidationAlgs"
    )
    datasets = dict()
    REGEN = False  # set to True via conftest when --regen flag is passed

    def readAvailableAlgs(self, path):
        """
        Reads all available .py files from a path. To get the algorithms,
        the path to the DSGTools algorithms should be passed.
        :param path: (str) path to DSGTools algorithms.
        :return: (list-of-str) list of all found algorithms.
        """
        return [
            "dsgtools:{0}".format(os.path.splitext(x)[0].lower())
            for x in os.popen(
                "ls {path} | grep .py | grep -v __init__ | grep -v pycache".format(
                    path=path
                )
            ).readlines()
        ]

    def readSpatiaLite(self, path):
        """
        Reads a SpatiaLite database and gets its vector layers via OGR.
        :param path: (str) path to the SpatiaLite database.
        :return: (dict) map to the SpatiaLite database's layers.
        """
        layers = dict()
        for layer in ogr.Open(path):
            layername = layer.GetName()
            layers[layername] = QgsVectorLayer(
                "{0}|layername={1}".format(path, layername), layername, "ogr"
            )
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
                "{0}|layername={1}".format(path, layername), layername, "ogr"
            )
        return layers

    def readGeojson(self, path):
        """
        Reads a folder with Geojson files.
        :param path: (str) path do the geojson folder.
        :return: (dict) map to the geojson folder's layers.
        """
        layers = dict()
        fileList = [f for f in next(os.walk(path))[2] if ".geojson" in f]
        for f in fileList:
            fullPath = os.path.join(path, f)
            for layer in ogr.Open(fullPath):
                layername = os.path.splitext(f)[0]
                layers[layername] = QgsVectorLayer(fullPath, layername, "ogr")
        return layers

    def _loadDataset(self, driver, dataset):
        """
        Reads a GeoJSON dataset (folder of .geojson files).

        The ``driver`` parameter is kept for backwards compatibility but is
        ignored — all datasets are now stored as GeoJSON folders.

        :param driver: (str) ignored; kept for API compatibility.
        :param dataset: (str) dataset folder name inside testing_datasets/GeoJSON/.
        :return: (dict) layer-name → QgsVectorLayer.
        """
        geojsonPaths = os.path.join(self.CURRENT_PATH, "testing_datasets", "GeoJSON")
        datasets = {
            "banco_capacitacao": os.path.join(geojsonPaths, "banco_capacitacao"),
            "testes_sirgas2000_23s": os.path.join(
                geojsonPaths, "testes_sirgas2000_23s"
            ),
            "testes_wgs84": os.path.join(geojsonPaths, "testes_wgs84"),
            "land_cover_layers": os.path.join(geojsonPaths, "land_cover_layers"),
            "terrain_model_layers": os.path.join(geojsonPaths, "terrain_model_layers"),
            "testes_sirgas2000_24s": os.path.join(
                geojsonPaths, "testes_sirgas2000_24s"
            ),
            "spatial_rules_alg": os.path.join(geojsonPaths, "spatial_rules_alg"),
            "create_frames_layers": os.path.join(geojsonPaths, "create_frames_layers"),
            "identify_angles_in_invalid_range_layers": os.path.join(
                geojsonPaths, "identify_angles_in_invalid_range_layers"
            ),
            "douglas_peucker": os.path.join(geojsonPaths, "douglas_peucker"),
            "build_polygons_from_center_points": os.path.join(
                geojsonPaths, "build_polygons_from_center_points"
            ),
            "enforce_attribute_rules": os.path.join(
                geojsonPaths, "enforce_attribute_rules"
            ),
            "polygon_sliver": os.path.join(geojsonPaths, "polygon_sliver"),
        }
        layers = dict()
        if dataset in datasets:
            key = "geojson:{dataset}".format(dataset=dataset)
            if key not in self.datasets:
                self.datasets[key] = self.readGeojson(datasets[dataset])
            else:
                try:
                    [lyr.rollBack() for lyr in self.datasets[key].values()]
                except RuntimeError:
                    # C++ layer objects deleted (e.g., after QgsProject.clear()); reload
                    self.datasets[key] = self.readGeojson(datasets[dataset])
            layers = self.datasets[key]
        return layers

    def getInputLayers(
        self, driver, dataset, layers, addControlKey=False, idsToSelect=None
    ):
        """
        Gets the vector layers from an input dataset.
        :param driver: (str) driver's to be read.
        :param dataset: (str) dataset's name.
        :param layers: (list-of-str) layers to be read.
        :param idsToSelect: (list-of-int) list of feature IDs to be selected on
                            input.
        :return: (list-of-QgsVectorLayer) vector layers read from the dataset.
        """
        out = []
        # (vls) a map from layer name to vector layer read from database.
        vls = self._loadDataset(driver, dataset)
        for l in layers:
            if idsToSelect is not None:
                # vls[l].rollBack()
                lyr = vls[l] if not addControlKey else self.addControlKey(vls[l])
                lyr.select(idsToSelect)
                out.append(lyr)
            else:
                vls[l].rollBack()
                lyr = vls[l] if not addControlKey else self.addControlKey(vls[l])
                out.append(lyr)
        return out

    def addControlKey(self, lyr):
        # Sort by WKT before assigning AUTO so the numbering is deterministic
        # regardless of the internal feature-iteration order of the layer.
        ctx = QgsProcessingContext()
        ctx.setProject(QgsProject.instance())
        return processing.run(
            "native:addautoincrementalfield",
            {
                "INPUT": lyr,
                "FIELD_NAME": "AUTO",
                "START": 0,
                "GROUP_FIELDS": [],
                "SORT_EXPRESSION": "geom_to_wkt($geometry)",
                "SORT_ASCENDING": True,
                "SORT_NULLS_FIRST": False,
                "OUTPUT": "memory:",
            },
            context=ctx,
            feedback=QgsProcessingFeedback(),
        )["OUTPUT"]

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
            "dsgtools:topologicaldouglaspeuckerareasimplification": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "douglas_peucker",
                        ["cb_veg_campo_a"],
                        addControlKey=True,
                        idsToSelect=None,
                    )[0],
                    "SELECTED": False,
                    "SNAP": 1,
                    "DOUGLASPARAMETER": 150,
                    "FLAGS": "memory:",
                    "OUTPUT": "memory:",
                },
                {
                    "__comment": "Second test: checks if it works with onlySelected=True.",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "douglas_peucker",
                        ["cb_veg_campo_a"],
                        addControlKey=True,
                        idsToSelect=[1, 2],
                    )[0],
                    "SELECTED": True,
                    "SNAP": 1,
                    "DOUGLASPARAMETER": 150,
                    "FLAGS": "memory:",
                    "OUTPUT": "memory:",
                },
            ],
            "dsgtools:topologicaldouglaspeuckerlinesimplification": [
                {
                    "__comment": "First test: checks if it works.",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "douglas_peucker",
                        ["cb_tra_trecho_rodoviario_l"],
                        addControlKey=True,
                        idsToSelect=None,
                    )[0],
                    "SELECTED": False,
                    "SNAP": 1,
                    "DOUGLASPARAMETER": 2.5,
                    "FLAGS": "memory:",
                    "OUTPUT": "memory:",
                },
                {
                    "__comment": "Second test: checks if it works with onlySelected=True.",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "douglas_peucker",
                        ["cb_tra_trecho_rodoviario_l"],
                        addControlKey=True,
                        idsToSelect=[19, 20, 21],
                    )[0],
                    "SELECTED": True,
                    "SNAP": 1,
                    "DOUGLASPARAMETER": 2.5,
                    "FLAGS": "memory:",
                    "OUTPUT": "memory:",
                },
            ],
            "dsgtools:identifyduplicatedfeatures": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "ATTRIBUTE_BLACK_LIST": [],
                    "FLAGS": "memory:",
                    "IGNORE_PK_FIELDS": True,
                    "IGNORE_VIRTUAL_FIELDS": True,
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_rel_ponto_cotado_altimetrico_p"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifyoutofboundsangles": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_hid_terreno_suj_inundacao_a"],
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 10,
                }
            ],
            "dsgtools:identifyoutofboundsanglesincoverage": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_trecho_drenagem_l"]
                    ),
                    "SELECTED": False,
                    "TOLERANCE": 10,
                }
            ],
            "dsgtools:identifyanglesininvalidrangealgorithm": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "identify_angles_in_invalid_range_layers", ["lines1"]
                    )[0],
                    "SELECTED": False,
                    "MIN_ANGLE": 80,
                    "MAX_ANGLE": 100,
                }
            ],
            "dsgtools:identifygaps": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_hid_terreno_suj_inundacao_a"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifyandfixinvalidgeometries": [
                {
                    "__comment": "'Normal' test: checks if it works. This test does not check fixes!",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_veg_campo_a"]
                    )[0],
                    "IGNORE_CLOSED": False,
                    "SELECTED": False,
                    "TYPE": False,
                }
            ],
            "dsgtools:identifyduplicatedgeometries": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_rel_ponto_cotado_altimetrico_p"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifyduplicatedlinesoncoverage": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_hid_corredeira_l", "cb_hid_trecho_drenagem_l"],
                    ),
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifysmalllines": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_trecho_drenagem_l"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 5,
                }
            ],
            "dsgtools:identifyduplicatedpolygonsoncoverage": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_veg_campo_a", "cb_veg_floresta_a"],
                    ),
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifysmallpolygons": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_veg_campo_a"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 625,
                }
            ],
            "dsgtools:identifydangles": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "IGNORE_DANGLES_ON_UNSEGMENTED_LINES": False,
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_trecho_drenagem_l"]
                    )[0],
                    "LINEFILTERLAYERS": [],
                    "POLYGONFILTERLAYERS": [],
                    "SELECTED": False,
                    "TOLERANCE": 2,
                    "INPUT_IS_BOUDARY_LAYER": False,
                }
            ],
            "dsgtools:identifyduplicatedpointsoncoverage": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUTLAYERS": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        [
                            "cb_adm_edif_pub_civil_p",
                            "cb_rel_ponto_cotado_altimetrico_p",
                        ],
                    ),
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifyoverlaps": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_ilha_a"]
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:identifyvertexnearedges": [
                {
                    "__comment": "'Normal' test: checks if it works with polygon.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_24s", ["test1_vertexnearedge_a"]
                    )[0],
                    "SEARCH_RADIUS": 1,
                    "SELECTED": False,
                },
                {
                    "__comment": "'Normal' test: checks if it works with line.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_24s", ["test2_vertexnearedge_l"]
                    )[0],
                    "SEARCH_RADIUS": 1,
                    "SELECTED": False,
                },
            ],
            "dsgtools:removeduplicatedfeatures": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "ATTRIBUTE_BLACK_LIST": [],
                    "IGNORE_PK_FIELDS": True,
                    "IGNORE_VIRTUAL_FIELDS": True,
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_rel_ponto_cotado_altimetrico_p"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:removeduplicatedgeometries": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "FLAGS": "memory:",
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "banco_capacitacao",
                        ["cb_rel_ponto_cotado_altimetrico_p"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:removesmalllines": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_trecho_drenagem_l"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 5,
                }
            ],
            "dsgtools:removesmallpolygons": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_veg_campo_a"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 625,
                }
            ],
            "dsgtools:overlayelementswithareas": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "BEHAVIOR": 0,
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_linha_1"]
                    )[0],
                    "OVERLAY": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_poligono_1"]
                    )[0],
                    "SELECTED": False,
                    "SELECTED_OVERLAY": False,
                }
            ],
            "dsgtools:deaggregategeometries": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson",
                        "testes_sirgas2000_23s",
                        ["camada_linha_1"],
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:dissolvepolygonswithsameattributes": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "ATTRIBUTE_BLACK_LIST": [],
                    "IGNORE_PK_FIELDS": True,
                    "IGNORE_VIRTUAL_FIELDS": True,
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_poligono_1"]
                    )[0],
                    "MIN_AREA": None,
                    "SELECTED": False,
                }
            ],
            "dsgtools:removeemptyandupdate": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_linha_2"]
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:lineonlineoverlayer": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_linha_4"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 1,
                }
            ],
            "dsgtools:mergelineswithsameattributeset": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "ATTRIBUTE_BLACK_LIST": ["OGC_FID"],
                    "IGNORE_NETWORK": True,
                    "IGNORE_PK_FIELDS": True,
                    "IGNORE_VIRTUAL_FIELDS": True,
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_linha_3"]
                    )[0],
                    "SELECTED": False,
                }
            ],
            "dsgtools:snaplayeronlayer": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "BEHAVIOR": 0,
                    "INPUT": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_poligono_1"]
                    )[0],
                    "REFERENCE_LAYER": self.getInputLayers(
                        "geojson", "testes_sirgas2000_23s", ["camada_poligono_2"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 25,
                    "BUILD_CACHE": False,
                }
            ],
            "dsgtools:adjustnetworkconnectivity": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT": self.getInputLayers(
                        "geojson", "banco_capacitacao", ["cb_hid_trecho_drenagem_l"]
                    )[0],
                    "SELECTED": False,
                    "TOLERANCE": 2,
                }
            ],
            "dsgtools:identifyunsharedvertexonintersectionsalgorithm": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_LINES": self.getInputLayers(
                        "geojson", "testes_wgs84", ["line_input"]
                    )[0],
                    "INPUT_POLYGONS": self.getInputLayers(
                        "geojson", "testes_wgs84", ["polygon_input"]
                    )[0],
                    "SELECTED": False,
                    "FLAGS": "memory:",
                }
            ],
            "dsgtools:unbuildpolygonsalgorithm": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_POLYGONS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["vegetation"]
                    )[0],
                    "SELECTED": False,
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "OUTPUT_CENTER_POINTS": "memory:",
                    "OUTPUT_BOUNDARIES": "memory:",
                }
            ],
            "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm": [
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test1"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road", "boundaries"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test2"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road", "boundaries"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test3"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road", "boundaries"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test4"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road", "boundaries"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "'Normal' test: checks if it works.",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test5"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["fence", "road", "boundaries"]
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": "",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 6 - same as test 1, but with geo bounds",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test1"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "land_cover_layers",
                        ["fence", "road", "boundaries_within_geo_bounds"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "land_cover_layers", ["geographic_bounds"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 7 - same as test 2, but with geo bounds",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test2"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "land_cover_layers",
                        ["fence", "road", "boundaries_within_geo_bounds"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "land_cover_layers", ["geographic_bounds"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 8 - same as test 3, but with geo bounds",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test3"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "land_cover_layers",
                        ["fence", "road", "boundaries_within_geo_bounds"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "land_cover_layers", ["geographic_bounds"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 9 - same as test 4, but with geo bounds",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test4"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "land_cover_layers",
                        ["fence", "road", "boundaries_within_geo_bounds"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "land_cover_layers", ["geographic_bounds"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 10 - same as test 5, but with geo bounds",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["center_points_test5"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "land_cover_layers",
                        ["fence", "road", "boundaries_within_geo_bounds"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": self.getInputLayers(
                        "geojson", "land_cover_layers", ["water"]
                    ),
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "land_cover_layers", ["geographic_bounds"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 11 - without polygons, just lines, with attributeblacklist",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "build_polygons_from_center_points", ["pontos"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [
                        "id",
                        "nome",
                        "tipo_comprovacao",
                        "tipo_insumo",
                        "observacao",
                        "data_modificacao",
                        "controle_id",
                        "ultimo_usuario",
                    ],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "build_polygons_from_center_points",
                        ["linhas1", "linhas2"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": None,
                    "GEOGRAPHIC_BOUNDARY": None,
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 12 - without polygons, just lines, with attributeblacklist and geoboundary. Should create 5 pol, not 6. The tip of the triangle is outside of the boundary ",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "build_polygons_from_center_points", ["pontos"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [
                        "id",
                        "nome",
                        "tipo_comprovacao",
                        "tipo_insumo",
                        "observacao",
                        "data_modificacao",
                        "controle_id",
                        "ultimo_usuario",
                    ],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "build_polygons_from_center_points",
                        ["linhas1", "linhas2"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": None,
                    "GEOGRAPHIC_BOUNDARY": self.getInputLayers(
                        "geojson", "build_polygons_from_center_points", ["moldura"]
                    )[0],
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "test 13 - without polygons, just lines, with a different attributeblacklist",
                    "INPUT_CENTER_POINTS": self.getInputLayers(
                        "geojson", "build_polygons_from_center_points", ["pontos"]
                    )[0],
                    "SELECTED": False,
                    "ATTRIBUTE_BLACK_LIST": [
                        "id",
                        "nome",
                        "tipo_comprovacao",
                        "tipo_insumo",
                        "observacao",
                    ],
                    "CONSTRAINT_LINE_LAYERS": self.getInputLayers(
                        "geojson",
                        "build_polygons_from_center_points",
                        ["linhas1", "linhas2"],
                    ),
                    "CONSTRAINT_POLYGON_LAYERS": None,
                    "GEOGRAPHIC_BOUNDARY": None,
                    "GROUP_BY_SPATIAL_PARTITION": False,
                    "OUTPUT_POLYGONS": "memory:",
                    "INVALID_POLYGON_LOCATION": "memory:",
                    "UNUSED_BOUNDARY_LINES": "memory:",
                    "FLAGS": "memory:",
                },
            ],
            "dsgtools:identifyterrainmodelerrorsalgorithm": [
                {
                    "__comment": "test 1",
                    "INPUT": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["contours_test1"]
                    )[0],
                    "SELECTED": False,
                    "CONTOUR_ATTR": "contour",
                    "CONTOUR_INTERVAL": 10,
                    "TOPOLOGY_RADIUS": 2,
                    "GEOGRAPHIC_BOUNDS": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["geographic_bounds_test1"]
                    )[0],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                },
                {
                    "__comment": "test 2",
                    "INPUT": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["contours_test2"]
                    )[0],
                    "SELECTED": False,
                    "CONTOUR_ATTR": "contour",
                    "CONTOUR_INTERVAL": 10,
                    "TOPOLOGY_RADIUS": 2,
                    "GEOGRAPHIC_BOUNDS": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["geographic_bounds_test2"]
                    )[0],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                },
                {
                    "__comment": "test 3",
                    "INPUT": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["contours_test3"]
                    )[0],
                    "SELECTED": False,
                    "CONTOUR_ATTR": "contour",
                    "CONTOUR_INTERVAL": 10,
                    "TOPOLOGY_RADIUS": 2,
                    "GEOGRAPHIC_BOUNDS": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["geographic_bounds_test3"]
                    )[0],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                },
                {
                    "__comment": "test 4",
                    "INPUT": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["contours_test4"]
                    )[0],
                    "SELECTED": False,
                    "CONTOUR_ATTR": "contour",
                    "CONTOUR_INTERVAL": 10,
                    "TOPOLOGY_RADIUS": 2,
                    "GEOGRAPHIC_BOUNDS": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["geographic_bounds_test4"]
                    )[0],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                },
                {
                    "__comment": "test 5",
                    "INPUT": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["contours_test5"]
                    )[0],
                    "SELECTED": False,
                    "CONTOUR_ATTR": "contour",
                    "CONTOUR_INTERVAL": 10,
                    "TOPOLOGY_RADIUS": 2,
                    "GEOGRAPHIC_BOUNDS": self.getInputLayers(
                        "geojson", "terrain_model_layers", ["geographic_bounds_test5"]
                    )[0],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                    "GROUP_BY_SPATIAL_PARTITION": False,
                },
            ],
            # '__comment' : "'Normal' test: checks if it works."
            "dsgtools:enforcespatialrules": [
                {
                    "__comment": "Tests 1 - tests all topological relation",
                    "RULES_SET": [
                        {
                            "cardinality": "1..1",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "rel_pico_p",
                            "layer_b": "rel_ponto_cotado_altimetrico_p",
                            "name": "Pico deve estar em cima de um ponto cotado",
                            "predicate": 0,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "rel_ponto_cotado_altimetrico_p",
                            "layer_b": "hid_massa_dagua_a",
                            "name": "Pontos cotados altimétricos não podem estar sobre massa d’água",
                            "predicate": 2,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "enc_torre_energia_p",
                            "layer_b": "enc_trecho_energia_l",
                            "name": "Torres de energia devem estar sobre um ou mais trechos de energia",
                            "predicate": 3,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "2..2",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_barragem_p",
                            "layer_b": "hid_trecho_drenagem_l",
                            "name": "Barragens tipo ponto estão entre 2 e somente trechos de drenagem",
                            "predicate": 5,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..1",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "veg_brejo_pantano_a",
                            "layer_b": "hid_area_umida_a",
                            "name": "Brejo/Pantano deve estar contido por uma Área Úmida",
                            "predicate": 9,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "modaluso = 5",
                            "filter_b": "",
                            "layer_a": "tra_ponte_l",
                            "layer_b": "fer_trecho_ferroviario_l",
                            "name": "O modalUso de Ponte deve ser Ferroviario se esta intersectar um Trecho Ferroviario.",
                            "predicate": 3,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "modaluso != 5",
                            "filter_b": "",
                            "layer_a": "tra_ponte_l",
                            "layer_b": "fer_trecho_ferroviario_l",
                            "name": "O modalUso de Ponte deve ser Ferroviario se esta intersectar um Trecho Ferroviario.",
                            "predicate": 4,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_trecho_drenagem_l",
                            "layer_b": "hid_vala_l",
                            "name": "Valas não são sobrepostas por drenagens",
                            "predicate": 12,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "0..1",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "hid_barragem_a",
                            "layer_b": "hid_trecho_drenagem_l",
                            "name": "Barragens do tipo área contêm até uma drenagem",
                            "predicate": 13,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "0..1",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas",
                            "layer_b": "poligonos",
                            "name": "Teste: 'linhas' não cruza 'poligonos'",
                            "predicate": 7,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos_2",
                            "layer_b": "poligonos",
                            "name": "Teste: 'poligonos_2' sobrepõe 'poligonos'",
                            "predicate": 11,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas_2",
                            "layer_b": "linhas",
                            "name": "Teste: 'linhas_2' não é igual a 'linhas'",
                            "predicate": 1,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'poligonos' não toca 'poligonos_2'",
                            "predicate": 6,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "linhas_2",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'linhas_2' não cruza 'poligonos_2'",
                            "predicate": 8,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "points",
                            "layer_b": "poligonos_2",
                            "name": "Teste: 'points' não está contido em 'poligonos_2'",
                            "predicate": 10,
                            "useDE9IM": False,
                        },
                        {
                            "cardinality": "1..*",
                            "de9im_predicate": "",
                            "filter_a": "",
                            "filter_b": "",
                            "layer_a": "poligonos_2",
                            "layer_b": "points",
                            "name": "Teste: 'poligonos_2' não contém 'points'",
                            "predicate": 14,
                            "useDE9IM": False,
                        },
                    ],
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                }
            ],
            "dsgtools:enforceattributerulesalgorithm": [
                {
                    "__comment": "Test 1",
                    "RULES_SET": {
                        "0": {
                            "description": "regime - Preencher atributo",
                            "layerField": ["hid_trecho_drenagem_l", "regime"],
                            "expression": '"regime" not in  (0,1,2,3,4,5)',
                            "errorType": "Preencher atributo",
                            "color": "#b6a500",
                        }
                    },
                    "SELECTED": False,
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                },
                {
                    "__comment": "Test 2",
                    "RULES_SET": {
                        "0": {
                            "description": "nome - Nome deve iniciar com letra maiuscula e nao deve ter espacos desnecessarios",
                            "layerField": ["hid_ilha_a", "nome"],
                            "expression": "regexp_match ( \"nome\" , '^ ' ) or regexp_match ( \"nome\" , '  ' ) or regexp_match ( \"nome\" , ' $' ) or regexp_match ( \"nome\" , '^[a-z]' )",
                            "errorType": "Atributo com valor incorreto",
                            "color": "#ff0000",
                        }
                    },
                    "SELECTED": True,
                    "POINT_FLAGS": "memory:",
                    "LINE_FLAGS": "memory:",
                    "POLYGON_FLAGS": "memory:",
                },
            ],
            "dsgtools:identifypolygonsliver": [
                {
                    "__comment": "Checks if simple cases are identified.",
                    "INPUT_LAYERS": self.getInputLayers(
                        "geojson", "polygon_sliver", ["poligonos_1"]
                    ),
                    "RATIO_TOL": 10,
                    "SELECTED": False,
                    "SILENT": True,
                    "FLAGS": "memory:",
                },
                {
                    "__comment": "Checks if the algorithm works with selected"
                    " features option on.",
                    "INPUT_LAYERS": self.getInputLayers(
                        "geojson", "polygon_sliver", ["poligonos_1"], idsToSelect=[0, 1]
                    ),
                    "RATIO_TOL": 10,
                    "SELECTED": True,
                    "SILENT": True,
                    "FLAGS": "memory:",
                },
            ],
            "dsgtools:ALG": [{"__comment": "'Normal' test: checks if it works."}],
        }
        return parameters[algName] if algName in parameters else dict()

    def runAlg(
        self, algName, parameters, feedback=None, context=None, addControlKey=False
    ):
        """
        Executes a given algorithm.
        :param algName: (str) target algorithm's name.
        :param parameters: (dict) set of arguments for target algorithm.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental parameters.
        """
        context = context or QgsProcessingContext()
        context.setProject(QgsProject.instance())
        for v in parameters.values():
            if isinstance(v, QgsVectorLayer) and context.temporaryLayerStore().mapLayer(v.id()) is None:
                context.temporaryLayerStore().addMapLayer(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, QgsVectorLayer) and context.temporaryLayerStore().mapLayer(item.id()) is None:
                        context.temporaryLayerStore().addMapLayer(item)
        out = processing.run(
            algName,
            parameters,
            None,
            feedback or QgsProcessingFeedback(),
            context,
        )
        outputstr = "FLAGS" if "FLAGS" in out else "OUTPUT" if "OUTPUT" in out else ""
        if outputstr:
            out = out[outputstr]
        return out

    def runAlgWithMultipleOutputs(
        self, algName, parameters, feedback=None, context=None
    ):
        """
        Executes a given algorithm that has multiple outputs. Returns a dict
        with the returned layers in the format {'OUTPUT_LAYER_KEY':(QgsVectorLayer) OutputLayer}
        :param algName: (str) target algorithm's name.
        :param parameters: (dict) set of arguments for target algorithm.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental parameters.
        """
        feedback = QgsProcessingFeedback() if feedback is None else feedback
        context = context or QgsProcessingContext()
        context.setProject(QgsProject.instance())
        for v in parameters.values():
            if isinstance(v, QgsVectorLayer) and context.temporaryLayerStore().mapLayer(v.id()) is None:
                context.temporaryLayerStore().addMapLayer(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, QgsVectorLayer) and context.temporaryLayerStore().mapLayer(item.id()) is None:
                        context.temporaryLayerStore().addMapLayer(item)
        return processing.run(algName, parameters, context=context, feedback=feedback)

    def expectedOutput(self, algName, test, multipleOutputs=False):
        """
        Gets the expected output layer(s) for a given algorithm test.

        All expected outputs are stored as GeoJSON:
          - multi-output tests: expected_outputs/<alg>/test_N/   (folder)
          - single-output tests: expected_outputs/<alg>/test_N/test_N.geojson

        :param algName: (str) target algorithm's name.
        :param test: (int) test index (1-based).
        :param multipleOutputs: (bool) whether the algorithm has multiple outputs.
        :return: dict (multipleOutputs) or QgsVectorLayer (single output), or None.
        """
        rootPath = os.path.join(
            self.CURRENT_PATH, "expected_outputs", algName.split(":")[-1]
        )
        folderPath = os.path.join(rootPath, "test_{n}".format(n=test))
        if not os.path.isdir(folderPath):
            return None
        if multipleOutputs:
            return self.readGeojson(folderPath)
        geojsonPath = os.path.join(folderPath, "test_{n}.geojson".format(n=test))
        if not os.path.exists(geojsonPath):
            return None
        return QgsVectorLayer(
            geojsonPath,
            "{alg}_test_{n}_output".format(alg=algName.split(":")[-1], n=test),
            "ogr",
        )

    def compareLayers(
        self,
        target,
        reference,
        attributeBlackList=None,
        addControlKey=False,
        distTol=1e-5,
        areaTol=1e-10,
    ):
        """
        Compares two vector layers using a deterministic WKT-based sort so that
        feature ordering never causes spurious failures.

        :param target: (QgsVectorLayer) layer produced by the algorithm.
        :param reference: (QgsVectorLayer) expected-output layer.
        :param attributeBlackList: (list-of-str) attribute names to skip.
        :param addControlKey: (bool) whether an AUTO control column was added.
        :param distTol: (float) max centroid distance for approximate geometry match.
        :param areaTol: (float) max relative area difference for approximate match.
        :return: (str) non-empty string describing the first difference found, or "".
        """
        skipFields = {"fid", "AUTO", "_otf"}
        blackList = set(attributeBlackList or [])
        if addControlKey:
            blackList.add("AUTO")

        if target.featureCount() == 0 and reference.featureCount() == 0:
            return ""
        if target.geometryType() != reference.geometryType():
            return "Incorrect geometry type for the output layer."
        if target.featureCount() != reference.featureCount():
            return (
                "Feature count mismatch: output has {out}, expected {ref}.".format(
                    out=target.featureCount(), ref=reference.featureCount()
                )
            )

        # Validate that every reference attribute exists in the output.
        targetFieldNames = [
            f.name()
            for f in target.fields()
            if f.name() not in skipFields and "_otf" not in f.name()
        ]
        for f in reference.fields():
            if f.name() in skipFields or "_otf" in f.name():
                continue
            if f.name() not in targetFieldNames:
                return "Missing attribute '{attr}' in output layer.".format(
                    attr=f.name()
                )

        compareFields = [n for n in targetFieldNames if n not in blackList]

        def _sort_key(feat):
            # WKT with fixed precision guarantees identical strings for equal
            # geometries regardless of internal QGIS iteration order.
            wkt = feat.geometry().asWkt(precision=8)
            attrs = tuple(str(feat[f]) for f in compareFields)
            return (wkt,) + attrs

        targetFeats = sorted(target.getFeatures(), key=_sort_key)
        refFeats = sorted(reference.getFeatures(), key=_sort_key)

        for idx, (tf, rf) in enumerate(zip(targetFeats, refFeats)):
            tGeom = tf.geometry()
            rGeom = rf.geometry()
            geom_ok = tGeom.isGeosEqual(rGeom) or tGeom.equals(rGeom)
            if not geom_ok:
                dist = tGeom.distance(rGeom)
                if dist > distTol:
                    return (
                        "Feature #{idx}: geometry mismatch.\n"
                        "  output:   {out}\n"
                        "  expected: {ref}"
                    ).format(
                        idx=idx,
                        out=tGeom.asWkt(),
                        ref=rGeom.asWkt(),
                    )
                rArea = rGeom.area()
                tArea = tGeom.area()
                if rArea and abs(tArea - rArea) / rArea > areaTol:
                    return "Feature #{idx}: area mismatch.".format(idx=idx)

            for attr in compareFields:
                if tf[attr] != rf[attr]:
                    t_val = _normalize_geo_attr(tf[attr])
                    r_val = _normalize_geo_attr(rf[attr])
                    if t_val != r_val:
                        return (
                            "Feature #{idx}: attribute '{attr}' mismatch.\n"
                            "  output:   {out}\n"
                            "  expected: {ref}"
                        ).format(
                            idx=idx,
                            attr=attr,
                            out=tf[attr],
                            ref=rf[attr],
                        )

        return ""

    def loadLayerToCanvas(self, layer):
        """
        Load a layer to canvas in order for it to be accessible using the
        processing context.
        :param layer: (QgsVectorLayer) layer object to be loaded to canvas.
        """
        proj = QgsProject.instance()
        if not proj.mapLayersByName(layer.name()):
            return
        proj.addMapLayer(layer, True)

    def clearProject(self):
        """
        Clears all loaded layers from canvas.
        """
        QgsProject.instance().clear()

    def runAlgTest(
        self,
        algName,
        feedback=None,
        context=None,
        loadLayers=False,
        multipleOutputs=False,
        attributeBlackList=None,
        addControlKey=False,
    ):
        """
        Tests if the output of a given algorithm is the expected one.
        :param algName: (str) target algorithm's name.
        :param feedback: (QgsProcessingFeedback) QGIS progress tracking object.
        :param context: (QgsProcessingContext) execution's environmental
                        parameters.
        :param loadLayers: (bool) indicates whether expected and output layers
                            should be loaded to canvas.
        :param multipleOutputs: (bool) whether the algorithm tested outputs
                                more than 1 layer.
        :param attributeBlackList: (list-of-str) attributes to be ignored when
                                   comparing features.
        :param addControlKey: (bool) creates a new column to be used as ID on
                              the output layers.
        :return: (str) failing reason.
        """
        parameters = self.algorithmParameters(algName)
        context = context or QgsProcessingContext()
        context.setProject(QgsProject.instance())
        output = None
        expected = None
        if parameters == dict():
            return "Unable to read a set of parameters for {alg}'s tests.".format(
                alg=algName
            )
        try:
            for i, param in enumerate(parameters):
                output = (
                    self.runAlgWithMultipleOutputs(algName, param, feedback, context)
                    if multipleOutputs
                    else self.runAlg(
                        algName, param, feedback, context, addControlKey=addControlKey
                    )
                )
                expected = self.expectedOutput(
                    algName, i + 1, multipleOutputs=multipleOutputs
                )
                if isinstance(output, QgsVectorLayer):
                    self.compareInputLayerWithOutputLayer(
                        i,
                        algName,
                        output,
                        expected,
                        loadLayers=loadLayers,
                        attributeBlackList=attributeBlackList,
                        addControlKey=addControlKey,
                    )
                    if isinstance(output, QgsVectorLayer):
                        output.rollBack()
                    if isinstance(expected, QgsVectorLayer):
                        expected.rollBack()
                elif isinstance(output, dict):
                    for key, outputLyr in output.items():
                        if isinstance(outputLyr, list):
                            for idx, outLayer in enumerate(outputLyr):
                                if "{0}_{1}".format(key, idx) not in expected:
                                    raise Exception(
                                        "Output dictionary key {k} was not "
                                        "found in expected output dictionary.".format(
                                            k="{0}_{1}".format(key, idx)
                                        )
                                    )
                                expectedLyr = expected["{0}_{1}".format(key, idx)]
                                self.compareInputLayerWithOutputLayer(
                                    i,
                                    algName,
                                    outLayer,
                                    expectedLyr,
                                    loadLayers=loadLayers,
                                    addControlKey=addControlKey,
                                    attributeBlackList=attributeBlackList,
                                )
                                if isinstance(expectedLyr, QgsVectorLayer):
                                    expectedLyr.rollBack()
                            if isinstance(outLayer, QgsVectorLayer):
                                outLayer.rollBack()
                            # from now on commands are for single output only
                            continue
                        elif key not in expected:
                            if self.REGEN:
                                self.compareInputLayerWithOutputLayer(
                                    i,
                                    algName,
                                    outputLyr,
                                    None,
                                    loadLayers=loadLayers,
                                    addControlKey=addControlKey,
                                    attributeBlackList=attributeBlackList,
                                    save_name=key,
                                )
                            else:
                                # No expected file for this output key — skip.
                                # This happens when an algorithm gains a new output
                                # that hasn't had expected data generated yet.
                                if isinstance(outputLyr, QgsVectorLayer):
                                    outputLyr.rollBack()
                        else:
                            self.compareInputLayerWithOutputLayer(
                                i,
                                algName,
                                outputLyr,
                                expected[key],
                                loadLayers=loadLayers,
                                addControlKey=addControlKey,
                                attributeBlackList=attributeBlackList,
                                save_name=key,
                            )
                            if isinstance(outputLyr, QgsVectorLayer):
                                outputLyr.rollBack()
                            if isinstance(expected[key], QgsVectorLayer):
                                expected[key].rollBack()
        except Exception as e:
            try:
                if isinstance(output, QgsVectorLayer):
                    output.rollBack()
                elif isinstance(output, dict):
                    [
                        lyr.rollBack()
                        for key, lyr in output.items()
                        if isinstance(lyr, QgsVectorLayer)
                    ]
                if isinstance(expected, QgsVectorLayer):
                    expected.rollBack()
                elif isinstance(expected, dict):
                    [
                        lyr.rollBack()
                        for key, lyr in expected.items()
                        if isinstance(lyr, QgsVectorLayer)
                    ]
            except:
                pass
            return "Test #{nr} for '{alg}' has failed:\n'{msg}'".format(
                msg=", ".join(map(str, e.args)), nr=i + 1, alg=algName
            )
        # missing the output testing
        return ""

    def saveLayerAsGeojson(self, layer, path):
        """Save a QgsVectorLayer to a GeoJSON file, creating parent dirs as needed."""
        from qgis.core import QgsVectorFileWriter, QgsCoordinateTransformContext
        os.makedirs(os.path.dirname(path), exist_ok=True)
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GeoJSON"
        options.fileEncoding = "UTF-8"
        QgsVectorFileWriter.writeAsVectorFormatV3(
            layer, path, QgsCoordinateTransformContext(), options
        )

    def compareInputLayerWithOutputLayer(
        self,
        i,
        algName,
        output,
        expected,
        loadLayers=False,
        attributeBlackList=None,
        addControlKey=False,
        save_name=None,
    ):
        if not output.isValid():
            raise Exception(
                "Output is an INVALID vector layer.".format(alg=algName, nr=i + 1)
            )
        if self.REGEN:
            # --regen mode: save actual output as new expected file
            algShort = algName.split(":")[-1]
            folderPath = os.path.join(
                self.CURRENT_PATH, "expected_outputs", algShort, "test_{n}".format(n=i + 1)
            )
            name = save_name if save_name else "test_{n}".format(n=i + 1)
            geojsonPath = os.path.join(folderPath, "{name}.geojson".format(name=name))
            self.saveLayerAsGeojson(output, geojsonPath)
            if isinstance(output, QgsVectorLayer):
                output.rollBack()
            return
        if expected is None:
            raise Exception(
                "No expected output registered for the test, yet an output was generated.".format(
                    alg=algName, nr=i + 1
                )
            )
        msg = self.compareLayers(
            output,
            expected,
            attributeBlackList=attributeBlackList,
            addControlKey=addControlKey,
        )
        if isinstance(output, QgsVectorLayer):
            output.rollBack()
        if isinstance(expected, QgsVectorLayer):
            expected.rollBack()
        if msg:
            raise Exception(msg)
        if loadLayers:
            self.addLayerToGroup(output, "DSGTools Algorithm Tests")
            self.addLayerToGroup(expected, "DSGTools Algorithm Tests")

    def _testAllAlgorithms(self):
        """
        Executes all registered tests. Note that algorithms run in here should only
        output one layer.
        :return: (dict) a map to the algorithm found and all tests and their results.
        """
        # still missing how to define default datasets
        results = dict()
        algs = [
            # identification algs
            "dsgtools:identifyoutofboundsangles",
            "dsgtools:identifyoutofboundsanglesincoverage",
            "dsgtools:identifygaps",
            "dsgtools:identifyandfixinvalidgeometries",
            "dsgtools:identifyduplicatedfeatures",
            "dsgtools:identifyduplicatedgeometries",
            "dsgtools:identifyduplicatedlinesoncoverage",
            "dsgtools:identifysmalllines",
            "dsgtools:identifyduplicatedpolygonsoncoverage",
            "dsgtools:identifysmallpolygons",
            "dsgtools:identifydangles",
            "dsgtools:identifyduplicatedpointsoncoverage",
            "dsgtools:identifyoverlaps",
            "dsgtools:identifyvertexnearedges",
            "dsgtools:identifyunsharedvertexonintersectionsalgorithm"
            # correction algs
            "dsgtools:removeduplicatedfeatures",
            "dsgtools:removeduplicatedgeometries",
            "dsgtools:removesmalllines",
            "dsgtools:removesmallpolygons",
            # manipulation algs
            "dsgtools:lineonlineoverlayer",
            "dsgtools:mergelineswithsameattributeset",
            "dsgtools:overlayelementswithareas",
            "dsgtools:deaggregategeometries",
            "dsgtools:dissolvepolygonswithsameattributes",
            "dsgtools:removeemptyandupdate",
            "dsgtools:snaplayeronlayer",
            # network algs
            "dsgtools:adjustnetworkconnectivity",
        ]
        multipleOutputAlgs = [
            # identification algs
            "dsgtools:enforceattributerulesalgorithm",
            # manipulation algs
            "dsgtools:unbuildpolygonsalgorithm",
            "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm",
            # manipulation algs
            "dsgtools:topologicaldouglaspeuckerlinesimplification",
            "dsgtools:topologicaldouglaspeuckerareasimplification",
        ]
        # for alg in self.readAvailableAlgs(self.DEFAULT_ALG_PATH):
        for alg in algs:
            try:
                results[alg] = self.runAlgTest(alg)
            except KeyError:
                results[alg] = "No tests registered."
        for alg in multipleOutputAlgs:
            try:
                results[alg] = self.runAlgTest(
                    alg, multipleOutputs=True, attributeBlackList=["path"]
                )
            except KeyError:
                results[alg] = "No tests registered."
        return results

    def test_identifyoutofboundsangles(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifyoutofboundsangles"), "")

    def test_identifyanglesininvalidrangealgorithm(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:identifyanglesininvalidrangealgorithm",
                multipleOutputs=True,
                addControlKey=True,
            ),
            "",
        )

    def test_identifyoutofboundsanglesincoverage(self):
        self.assertEqual(
            self.runAlgTest("dsgtools:identifyoutofboundsanglesincoverage"), ""
        )

    def test_identifygaps(self):
        from qgis.core import QgsApplication
        if QgsApplication.processingRegistry().algorithmById("grass7:v.overlay") is None:
            self.skipTest("GRASS7 not available in this environment")
        self.assertEqual(self.runAlgTest("dsgtools:identifygaps"), "")

    def test_identifyandfixinvalidgeometries(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifyandfixinvalidgeometries"), "")

    def test_identifyduplicatedfeatures(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifyduplicatedfeatures"), "")

    def test_identifyduplicatedgeometries(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifyduplicatedgeometries"), "")

    def test_identifyduplicatedlinesoncoverage(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifyduplicatedlinesoncoverage"), "")

    def test_identifyduplicatedpointsoncoverage(self):
        self.assertEqual(
            self.runAlgTest("dsgtools:identifyduplicatedpointsoncoverage"), ""
        )

    def test_identifysmalllines(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifysmalllines"), "")

    def test_identifyduplicatedpolygonsoncoverage(self):
        self.assertEqual(
            self.runAlgTest("dsgtools:identifyduplicatedpolygonsoncoverage"), ""
        )

    def test_identifysmallpolygons(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifysmallpolygons"), "")

    def test_identifydangles(self):
        self.assertEqual(self.runAlgTest("dsgtools:identifydangles"), "")

    def test_identifyunsharedvertexonintersectionsalgorithm(self):
        self.assertEqual(
            self.runAlgTest("dsgtools:identifyunsharedvertexonintersectionsalgorithm"), ""
        )

    def test_identifyvertexnearedges(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:identifyvertexnearedges",
                addControlKey=True,
                multipleOutputs=True,
            ),
            "",
        )

    def test_overlayelementswithareas(self):
        self.assertEqual(self.runAlgTest("dsgtools:overlayelementswithareas"), "")

    def test_deaggregategeometries(self):
        self.assertEqual(
            self.runAlgTest("dsgtools:deaggregategeometries", addControlKey=True), ""
        )

    def test_dissolvepolygonswithsameattributes(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:dissolvepolygonswithsameattributes", addControlKey=True
            ),
            "",
        )

    def test_removeemptyandupdate(self):
        self.assertEqual(self.runAlgTest("dsgtools:removeemptyandupdate"), "")

    def test_snaplayeronlayer(self):
        self.assertEqual(self.runAlgTest("dsgtools:snaplayeronlayer"), "")

    def test_adjustnetworkconnectivity(self):
        self.assertEqual(self.runAlgTest("dsgtools:adjustnetworkconnectivity"), "")

    def test_unbuildpolygonsalgorithm(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:unbuildpolygonsalgorithm",
                multipleOutputs=True,
                attributeBlackList=["path"],
                addControlKey=True,
            ),
            "",
        )

    def test_buildpolygonsfromcenterpointsandboundariesalgorithm(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:buildpolygonsfromcenterpointsandboundariesalgorithm",
                multipleOutputs=True,
                addControlKey=True,
            ),
            "",
        )

    def test_identifyterrainmodelerrorsalgorithm(self):
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:identifyterrainmodelerrorsalgorithm",
                multipleOutputs=True,
                addControlKey=True,
            ),
            "",
        )

    def test_topologicaldouglaspeuckerlinesimplification(self):
        from qgis.core import QgsApplication
        if QgsApplication.processingRegistry().algorithmById("grass7:v.clean") is None:
            self.skipTest("GRASS7 not available in this environment")
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:topologicaldouglaspeuckerlinesimplification",
                multipleOutputs=True,
                addControlKey=True,
            ),
            "",
        )

    def test_topologicaldouglaspeuckerareasimplification(self):
        from qgis.core import QgsApplication
        if QgsApplication.processingRegistry().algorithmById("grass7:v.generalize") is None:
            self.skipTest("GRASS7 not available in this environment")
        self.assertEqual(
            self.runAlgTest(
                "dsgtools:topologicaldouglaspeuckerareasimplification",
                multipleOutputs=True,
                addControlKey=True,
            ),
            "",
        )

    def test_enforceattributerulesalgorithm(self):
        """Tests for Enforce Attribute Rules algorithm"""

        proj = QgsProject.instance()
        idsToSelect = [0, 3]
        testsParams = self.algorithmParameters(
            "dsgtools:enforceattributerulesalgorithm"
        )
        # this algorithm, specifically has to set layers Context-reading ready
        layers = self._loadDataset("geojson", "enforce_attribute_rules")

        layers = {l.split("-")[-1]: vl for l, vl in layers.items()}

        for parameters in testsParams:
            for key, values in parameters["RULES_SET"].items():
                if isinstance(layers, list):
                    vl = layers[0]
                    proj.addMapLayer(vl)
                    if parameters["SELECTED"]:
                        vl.selectByIds(idsToSelect)
                else:
                    vl = layers[values["layerField"][0]]
                    proj.addMapLayer(vl)
                    if parameters["SELECTED"]:
                        vl.selectByIds(idsToSelect)

        msg = self.runAlgTest(
            "dsgtools:enforceattributerulesalgorithm",
            multipleOutputs=True,
            addControlKey=True,
        )

        del self.datasets["geojson:enforce_attribute_rules"]
        self.clearProject()
        self.assertEqual(msg, "")

    def test_identifypolygonsliver(self):
        """Tests for Polygon Sliver Algorithm"""
        self.assertEqual(
            self.runAlgTest("dsgtools:identifypolygonsliver", addControlKey=True), ""
        )

    def test_enforcespatialrules(self):
        """Tests for Enforce Spatial Rules algorithm"""
        # this algo uses layers read from canvas using their names as inputs
        # hence it needs to be loaded to project's canvas
        proj = QgsProject.instance()
        proj.clear()
        crs = proj.crs()
        proj.setCrs(QgsCoordinateReferenceSystem(4326))
        layers = self._loadDataset("geojson", "spatial_rules_alg")
        for l, vl in layers.items():
            # vl = layers[l]
            # vl.setName(l)
            proj.addMapLayer(layers[l])
        msg = self.runAlgTest(
            "dsgtools:enforcespatialrules", multipleOutputs=True, addControlKey=True
        )
        # since layers were manually removed, cache is going to refer to
        # non-existing layers
        del self.datasets["geojson:spatial_rules_alg"]
        proj.clear()
        if crs and crs.isValid():
            proj.setCrs(crs)
        self.assertEqual(msg, "")

def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Tester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
