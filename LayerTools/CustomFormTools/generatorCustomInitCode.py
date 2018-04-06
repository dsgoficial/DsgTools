# -*- coding: utf-8 -*-
"""
/***************************************************************************

                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2018-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br

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
from builtins import object
import json
import os

class GeneratorCustomInitCode(object):
    def __init__(self):
        # contrutor
        super(GeneratorCustomInitCode, self).__init__() 

    def getInitCodeWithFilter(self, tableFilter, rules):
        tableFilterFormated = self.formatTableFilter(tableFilter)
        initCode = self.getTemplateInitCodeWithFilter()
        initCode = initCode.replace(
            '{filter}', 
            json.dumps(tableFilterFormated, ensure_ascii=False)
        )
        initCode = initCode.replace(
            '{rules}', 
            json.dumps(rules, ensure_ascii=False)
        )
        return initCode

    def getInitCodeNotFilter(self, rules):
        initCode = self.getTemplateInitCodeNotFilter()
        initCode = initCode.replace(
            '{rules}', 
            json.dumps(rules, ensure_ascii=False)
        )
        return initCode

    def formatTableFilter(self, tableFilter):
        tableFilterFormated = {}
        for line in tableFilter:
            tableFilterFormated[line['filter']] = line['code']
        return tableFilterFormated

    def getTemplateInitCodeNotFilter(self):
        initCodeTemplate = u""
        pathCode = os.path.join(
            os.path.dirname(__file__),
            'formInitCodeNotFilterTemplate'
        )
        codeFile = open(pathCode, "r")
        for line in codeFile.readlines():
            initCodeTemplate += line.decode("utf-8")
        codeFile.close()
        return initCodeTemplate

    def getTemplateInitCodeWithFilter(self):
        initCodeTemplate = u""
        pathCode = os.path.join(
            os.path.dirname(__file__),
            'formInitCodeWithFilterTemplate'
        )
        codeFile = open(pathCode, "r")
        for line in codeFile.readlines():
            initCodeTemplate += line.decode("utf-8")
        codeFile.close()
        return initCodeTemplate