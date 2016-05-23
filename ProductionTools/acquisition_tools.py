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

def sqlParser(sqlFile, isSpatialite):
    try:
        file = open(sqlFile, 'r')
        data = file.read()
        file.close()
    except:
        return dict()     

    commandList = data.split('#')
    createList = [command for command in commandList if 'CREATE TABLE' in command]
    
    notNullDict = dict()
    for item in createList:
        item = item.replace('CREATE TABLE ','').replace('\n','')
        tableName = item.split('(')[0]
        
        if isSpatialite:
            tableKey = tableName.replace('.','_')# is spatialite and we should use '_' as separator between schema and table
        else:
            tableKey = tableName
            
        if tableName.split('.')[0] not in ['dominios', 'public']:
            notNullDict[tableKey] = []  
                          
        attString = item.split(tableName)[-1].replace('\n','').replace('\t','').replace('\n\t','').replace('(','').replace(')','')
        
        for field in attString.split(','):
            if 'NOT NULL' in field:
                att = field.split(' ')[0]
                if att not in  ['','id','geom']:
                    if tableKey in notNullDict.keys():
                        notNullDict[tableKey].append(att)
                        
        if 'INHERITS' in item:
            parent = item.split('INHERITS(')[-1].split(')')[0]

            if isSpatialite:
                parentKey = parent.replace('.','_')# is spatialite and we should use '_' as separator between schema and table
            else:
                parentKey = parent

            if parentKey in notNullDict.keys():
                notNullDict[tableKey] += notNullDict[parentKey]
                        
    for key in notNullDict.keys():
        if notNullDict[key] == []:
            notNullDict.pop(key)
            
    return notNullDict

# coisa = sqlParser('/home/luiz/.qgis2/python/plugins/DsgTools/DbTools/PostGISTool/sqls/FTer_2a_Ed/edgvFter_2a_Ed.sql', True)
# coisa = sqlParser('/home/luiz/.qgis2/python/plugins/DsgTools/DbTools/PostGISTool/sqls/213/edgv213.sql', True)
# print coisa['ge_emu_acesso_a']