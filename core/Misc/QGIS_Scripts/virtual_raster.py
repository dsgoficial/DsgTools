# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-05-15
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
##DSG=group
##Inventario=vector
##Moldura=vector
##Pasta=folder

import processing
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsSpatialIndex, QgsFeatureRequest, QgsCoordinateTransform, QgsFeature
import os
import shutil, stat

#script methods
def createReprojectedLayer(layer, crs):
    """
    Creates a reprojected layer
    layer: layer used
    crs: crs used
    """
    temp = QgsVectorLayer('%s?crs=%s'% ('Multipolygon', crs.authid()), 'temp', 'memory')
    if not layer.isValid():
        raise GeoAlgorithmExecutionException('Problema ao criar camada reprojetada!')
        return None
    
    provider = temp.dataProvider()
    provider.addAttributes(layer.dataProvider().fields().toList())
    temp.updateFields()
    
    coordinateTransformer = QgsCoordinateTransform(layer.crs(), crs)
    features = []
    for feature in layer.getFeatures():
        feat = QgsFeature(feature)
        geom = feat.geometry()
        geom.transform(coordinateTransformer)
        feat.setGeometry(geom)
        features.append(feat)
        
    provider.addFeatures(features)
    
    return temp

def reprojectLayer(fromLayer, toLayer):
    """
    Reprojects all features fromLayer crs to toLayer crs
    fromLayer: origin layer
    toLayer: destination layer
    """
    ret = []
    coordinateTransformer = QgsCoordinateTransform(fromLayer.crs(), toLayer.crs())
    for feat in fromLayer.getFeatures():
        f = feat
        f.geometry().transform(coordinateTransformer)
        ret.append(f)
    return ret

def populateIndex(idx, layer):
    """
    Populates the layer index
    """
    for feat in layer.getFeatures():
        idx.insertFeature(feat)
        
def getCandidates(idx, layer, bbox):
    """
    Gets candidates to be processed using the index to speedup the process
    """
    ids = idx.intersects(bbox)
    candidates = []
    for id in ids:
        candidates.append(next(layer.getFeatures(QgsFeatureRequest().setFilterFid(id))))
    return candidates
    
def makeVrtDict(candidates, camada):
    """
    Makes a VRT dictionary
    """
    vrt = dict()
    for candidate in candidates:
        map_index = candidate['map_index']
        vrt[map_index] = []
        for feat in camada.getFeatures():
            if candidate.geometry().intersects(feat.geometry()):
                vrt[map_index].append(feat)
    return vrt            
            
def createVrt(vrt):
    """
    Creates a VRT file
    """
    count = 0
    size = len(list(vrt.keys()))
    p = 0
    progress.setPercentage(p)    
    for key in list(vrt.keys()):
        vrtfilename = os.path.join(Pasta, key, key+'.vrt')
        features = vrt[key]
        rasterList = []
        for feat in features:
            filename = feat['fileName']
            newfilename = copyFileSet(Pasta, key, filename)
            raster = QgsRasterLayer(newfilename, newfilename)
            rasterList.append(raster)
            ovr = newfilename+'.ovr'
            if not os.path.isfile(ovr):
                progress.setText('Fazendo Pirâmides...')
                #('gdalogr:overviews', input, levels=8, clean=False, resampling_method=0(nearest), format=1(Gtiff .ovr))
                processing.runalg('gdalogr:overviews', raster, '4 8 32 128', True, 0, 1)
        
        if int(float(count)/size*100) != p:
            p = int(float(count)/size*100)
            progress.setPercentage(p)    
        count += 1
    
        progress.setText('Fazendo raster virtual...')
        processing.runalg('gdalogr:buildvirtualraster', rasterList, 0, False, False, vrtfilename)
        
def copyFileSet(parent, folder, filename):
    """
    Copy files to the destination folder
    parent: parent folder
    folder: folder within parent
    filename: file name
    """
    path = os.path.dirname(filename)
    basename = os.path.basename(filename)
    texto = 'Copiando %s e arquivos relacionados...' % basename
    progress.setText(texto)
    
    destination = os.path.join(parent, folder)
    if not os.path.exists(destination):
        os.makedirs(destination)
        
    for root, dirs, files in os.walk(path):
        for file in files:
            if basename.split('.')[0] in file:
                try:
                    dir = os.path.join(destination, 'imagens')
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    f = os.path.join(root, file)
                    newf = os.path.join(parent, folder, 'imagens', file)
                    shutil.copy2(f, newf)
                except:
                    raise GeoAlgorithmExecutionException('Problema ao copiar arquivos!')
    return os.path.join(parent, folder, 'imagens', basename)
    
#end of script methods
        
#Making the actual work
#Camada de inventario
inventario = processing.getObject(Inventario)

#Camada de moldura
frame = processing.getObject(Moldura)

#Indice espacial
frameidx = QgsSpatialIndex()

#Populating a spatial index
populateIndex(frameidx, frame)

#checking crs's, if different, reproject
destCrs = frame.crs()
srcCrs = inventario.crs()
if srcCrs.authid() != destCrs.authid():
    progress.setText('CRS diferentes, reprojetando...')
    camada = createReprojectedLayer(inventario, frame.crs())
else:
    camada = inventario
    
#Obtaining candidates
candidates = getCandidates(frameidx, frame, camada.extent())

#making vrt dict
vrt = makeVrtDict(candidates, camada)

#creating vrt files
createVrt(vrt)
#ending the actual work