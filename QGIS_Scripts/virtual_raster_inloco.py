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
##CRS=crs
##VRT=output raster


import processing
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsSpatialIndex, QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsCoordinateReferenceSystem
import os
import shutil, stat

#script methods
def createVrt(inventario, vrt):
    #Camada de inventario
    layer = processing.getObject(Inventario)
    
    count = 0
    size = layer.featureCount()
    p = 0
    progress.setPercentage(p)    
    rasterList = []
    for feature in layer.getFeatures():
        filename = feature['fileName']
        
        raster = QgsRasterLayer(filename, filename)
        raster.setCrs( QgsCoordinateReferenceSystem(32723, QgsCoordinateReferenceSystem.EpsgCrsId) )
           
        rasterList.append(raster)
        ovr = filename+'.ovr'
        if not os.path.isfile(ovr):
            progress.setText('Fazendo Pirâmides...')
            #('gdalogr:overviews', input, levels=8, clean=False, resampling_method=0(nearest), format=1(Gtiff .ovr))
            processing.runalg('gdalogr:overviews', raster, '4 8 32 128', True, 0, 1)

        if int(float(count)/size*100) != p:
            p = int(float(count)/size*100)
            progress.setPercentage(p)    
        count += 1
    progress.setText('Fazendo raster virtual...')
    processing.runalg('gdalogr:buildvirtualraster', rasterList, 0, False, False, vrt)
#end of script methods
        
#Making the actual work
createVrt(Inventario, VRT)
#ending the actual work