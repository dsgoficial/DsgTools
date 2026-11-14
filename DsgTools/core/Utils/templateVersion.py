# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Brazilian Army - Geographic Service Bureau
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Decides whether an EDGV template database installed on a server must be
rebuilt from the creation SQL shipped with the plugin. Pure Python on purpose
(no QGIS import), so it can be tested anywhere.
"""

import re

_METADATA_INSERT = re.compile(
    r"INSERT\s+INTO\s+public\.db_metadata\s*\(\s*edgvversion\s*,\s*dbimplversion\s*\)"
    r"\s*VALUES\s*\(\s*'([^']*)'\s*,\s*'([^']*)'\s*\)",
    re.IGNORECASE,
)


def parseMetadataFromSql(sql):
    """
    Reads the db_metadata row a creation SQL inserts.
    :param sql: (str) contents of the creation SQL file.
    :return: (tuple) (edgvversion, dbimplversion), or (None, None) when the
        file inserts no metadata.
    """
    match = _METADATA_INSERT.search(sql or "")
    if match is None:
        return None, None
    return match.group(1), match.group(2)


def parseImplementationVersion(version):
    """
    '1.1.6' -> (1, 1, 6). Returns None when it is not a dotted number.
    """
    try:
        return tuple(int(i) for i in str(version).strip().split("."))
    except (TypeError, ValueError):
        return None


def isTemplateOutdated(
    templateEdgvVersion, templateImplVersion, fileEdgvVersion, fileImplVersion
):
    """
    True when the installed template must be dropped and rebuilt from the file.

    The implementation number alone does not order the models: EDGV 3.0 went
    from ('3.0', '4') to ('EDGV 3.0', '1.1'), renumbering domain codes, and a
    comparison of the numbers kept the old template forever (issue #857). The
    edgvversion label identifies the lineage, so a template whose label differs
    from the file's is always rebuilt. Inside the same lineage the newer one
    wins, compared number by number ('1.4.10' is newer than '1.4.4').
    """
    if fileEdgvVersion is None or fileImplVersion is None:
        # nothing to rebuild the template from
        return False
    if templateEdgvVersion != fileEdgvVersion:
        return True
    templateTuple = parseImplementationVersion(templateImplVersion)
    fileTuple = parseImplementationVersion(fileImplVersion)
    if templateTuple is None or fileTuple is None:
        return str(templateImplVersion) != str(fileImplVersion)
    size = max(len(templateTuple), len(fileTuple))
    templateTuple += (0,) * (size - len(templateTuple))
    fileTuple += (0,) * (size - len(fileTuple))
    return templateTuple < fileTuple
