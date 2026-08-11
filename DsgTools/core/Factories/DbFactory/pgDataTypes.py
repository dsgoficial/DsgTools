# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-01-01
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GeomTableEntry:
    """
    Metadata for a single geometry table entry inside GeomDictResult.

    Attributes
    ----------
    schema : str
        PostgreSQL schema name (e.g. ``"cb"``).
    srid : int
        Spatial reference identifier as returned natively by psycopg2.
    geometryColumn : str
        Name of the geometry column.
    geometryType : str
        PostGIS geometry type string (e.g. ``"MULTIPOLYGON"``).
    tableName : str
        Actual table name in the database.
    category : str
        EDGV category prefix derived from the table name.  Empty string for
        non-EDGV databases.
    """

    schema: str
    srid: int
    geometryColumn: str
    geometryType: str
    tableName: str
    category: str = ""


@dataclass
class GeomDictResult:
    """
    Return type of ``PostgisDb.getGeomDict``.

    Attributes
    ----------
    primitivePerspective : dict
        The ``geomTypeDict`` passed by the caller (primitive → list of layers).
    tablePerspective : Dict[str, GeomTableEntry]
        Layer-name-keyed mapping to geometry metadata.
    """

    primitivePerspective: dict
    tablePerspective: Dict[str, GeomTableEntry] = field(default_factory=dict)


@dataclass
class ColumnDomainInfo:
    """
    Domain / constraint information for a single column in a geometry table.

    Attributes
    ----------
    references : Optional[str]
        Fully qualified domain table (e.g. ``'"dominios"."situacaofisica"'``).
        ``None`` for multi-valued columns without a FK.
    refPk : Optional[str]
        Primary-key column name in the domain table.
    otherKey : Optional[str]
        Human-readable column name in the domain table (usually ``"code_name"``).
    values : dict
        ``{pk_value: label}`` mapping built from the domain table.
    constraintList : List
        CHECK constraint allowed values extracted from the database.
    isMulti : bool
        ``True`` when the column stores array (multi-valued) data.
    nullable : bool
        ``False`` when the column has a NOT NULL constraint.
    """

    references: Optional[str]
    refPk: Optional[str]
    otherKey: Optional[str]
    values: dict = field(default_factory=dict)
    constraintList: List = field(default_factory=list)
    isMulti: bool = False
    nullable: bool = True


@dataclass
class TableDomainInfo:
    """
    Domain / constraint information for a geometry table.

    Attributes
    ----------
    columns : Dict[str, ColumnDomainInfo]
        Column-name-keyed mapping to domain information.
    """

    columns: Dict[str, ColumnDomainInfo] = field(default_factory=dict)


@dataclass
class DatabaseLayerInfo:
    """
    Single-row output of ``PostgisDb.databaseInfo``.

    Attributes
    ----------
    schema : str
        PostgreSQL schema name.
    layer : str
        Table / layer name.
    geomCol : str
        Geometry column name.
    geomType : str
        PostGIS geometry type string.
    srid : int
        Spatial reference identifier as returned natively by psycopg2.
    """

    schema: str
    layer: str
    geomCol: str
    geomType: str
    srid: int
