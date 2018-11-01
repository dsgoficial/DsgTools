# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-03-03
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import range
from builtins import object
class DsgEnums(object):
    #generic manager and database enumerate
    Property, Database = list(range(2))
    #generic validation property
    ProcessName, ClassName = list(range(2))
    #property enum
    PermissionProperty, FieldToolboxProperty, EarthCoverageProperty, AttributeRuleProperty, SpatialRuleProperty, ValidationWorkflowProperty = list(range(6))
    # datasource selection widgets enum
    NoDriver, PostGIS, NewPostGIS, SpatiaLite, NewSpatiaLite, Shapefile, NewShapefile, Geopackage, NewGeopackage = list(range(9))
    # node types enum
    Flag, Sink, WaterwayBegin, UpHillNode, DownHillNode, Confluence, Ramification, AttributeChange, NodeNextToWaterBody, AttributeChangeFlag, NodeOverload, DisconnectedLine = list(range(12))
