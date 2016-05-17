# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
import os
from osgeo import ogr

def sqlParser(sqlFile):
    f =  open(sqlFile,'r')
    data = f.read()
    commandList = data.split('#')
    createList = [command for command in commandList if 'CREATE TABLE' in command]
    
    nullFieldDict = dict()
    for item in createList:
        item = item.replace('CREATE TABLE ','').replace('\n','')
        tableName = item.split('(')[0]
        if tableName.split('.')[0] not in ['dominios', 'public']:
            nullFieldDict[tableName] = []
        attString = item.split(tableName)[-1].replace('\n','').replace('\t','').replace('\n\t','').replace('(','').replace(')','')
        for field in attString.split(','):
            if 'NOT NULL' in field:
                att = field.split(' ')[0]
                if att not in  ['','id','geom']:
                    if tableName in nullFieldDict.keys():
                        nullFieldDict[tableName].append(att)
        for key in nullFieldDict.keys():
            if nullFieldDict[key] == []:
                nullFieldDict.pop(key)
            
    return nullFieldDict

print sqlParser('/home/luiz/.qgis2/python/plugins/DsgTools/DbTools/PostGISTool/sqls/213/edgv213.sql')