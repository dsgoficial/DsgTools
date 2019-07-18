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
        return dict(), dict() 

    commandList = data.split('#')
    createList = [command for command in commandList if 'CREATE TABLE' in command]
    
    notNullDict = dict()

    otherAttrDict = dict()
    for item in createList:
        item = item.replace('CREATE TABLE ','').replace('\n','')
        tableName = item.split('(')[0]
        
        if isSpatialite:
            tableKey = tableName.replace('.','_')# is spatialite and we should use '_' as separator between schema and table
        else:
            tableKey = tableName
            
        if tableName.split('.')[0] not in ['dominios', 'public']:
            notNullDict[tableKey] = []
            otherAttrDict[tableKey] = []    
                          
        attString = item.split(tableName)[-1].replace('\n','').replace('\t','').replace('\n\t','').replace('(','').replace(')','')
        
        for field in attString.split(','):
            if 'NOT NULL' in field:
                att = field.split(' ')[0]
                if att not in  ['','id','geom']:
                    if tableKey in list(notNullDict.keys()):
                        notNullDict[tableKey].append(att)
            else:
                att = field.split(' ')[0]
                if  att not in  ['','id','geom'] and 'id_' not in att and 'CONSTRAINT' not in att:
                    if tableKey in list(otherAttrDict.keys()):
                        if att not in otherAttrDict[tableKey]:
                            otherAttrDict[tableKey].append(att)
                        
        if 'INHERITS' in item:
            parent = item.split('INHERITS(')[-1].split(')')[0]

            if isSpatialite:
                parentKey = parent.replace('.','_')# is spatialite and we should use '_' as separator between schema and table
            else:
                parentKey = parent

            if parentKey in list(notNullDict.keys()):
                notNullDict[tableKey] += notNullDict[parentKey]
            
            if parentKey in list(otherAttrDict.keys()):
                for item in otherAttrDict[parentKey]:
                    if item not in otherAttrDict[tableKey]:
                        otherAttrDict[tableKey].append(item)
                    
                        
    for key in list(notNullDict.keys()):
        if notNullDict[key] == []:
            notNullDict.pop(key)
    
    for key in list(otherAttrDict.keys()):
        if otherAttrDict[key] == []:
            otherAttrDict.pop(key)
            
    return notNullDict, otherAttrDict
