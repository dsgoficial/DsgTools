# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-31
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
# Qt Imports
from builtins import str
from qgis.PyQt.Qt import QObject


class DbCustomization(QObject):
    def __init__(self, validatedJSONDict):
        super(DbCustomization, self).__init__()
        self.log = ""
        self.errorLog = ""
        self.jsonDict = validatedJSONDict

    def getName(self):
        return (
            str(self.__class__)
            .split(".")[-1]
            .replace("'>", "")
            .replace("Customization", "")
        )

    def getLog(self):
        return self.log

    def logEvent(self, event):
        self.log += event

    def buildSql(self):
        # Abstract method. Must be reimplemented in each child.
        pass

    def buildUndoSql(self):
        # Abstract method. Must be reimplemented in each child.
        pass
