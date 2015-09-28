##DSG=group
##Inventario=vector
##Moldura=vector
##Pasta=folder

import processing
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from qgis.core import QgsRasterLayer, QgsSpatialIndex, QgsFeatureRequest, QgsCoordinateTransform
import os

def reprojectLayer(inventario, frame):
    ret = []
    coordinateTransformer = QgsCoordinateTransform(inventario.crs(), frame.crs())
    for feat in inventario.getFeatures():
        f = feat
        f.geometry().transform(coordinateTransformer)
        ret.append(f)
    return ret

inventario = processing.getObject(Inventario)
frame = processing.getObject(Moldura)
frameidx = QgsSpatialIndex()

#reprojecting inventory layer
reprojectedFeatures = reprojectLayer(inventario, frame)

#Populating a spatial index
for inom in frame.getFeatures():
    frameidx.insertFeature(inom)

ids = frameidx.intersects(inventario.extent())
candidates = []
for id in ids:
    candidates.append(frame.getFeatures(QgsFeatureRequest().setFilterFid(id)).next())
    
vrt = dict()
for candidate in candidates:
    map_index = candidate['map_index']
    print map_index
    vrt[map_index] = []
    for feat in reprojectedFeatures:
        if candidate.geometry().intersects(feat.geometry()):
            vrt[map_index].append(feat)
            
count = 0
size = len(vrt.keys())
p = 0
progress.setPercentage(p)    
for key in vrt.keys():
    vrtfilename = os.path.join(Pasta, key+'.vrt')
    print vrtfilename
    features = vrt[key]

    rasterList = []
    
    for feat in features:
        filename = feat['fileName']
        raster = QgsRasterLayer(filename, filename)
        rasterList.append(raster)
        ovr = filename+'.ovr'
        if not os.path.isfile(ovr):
            progress.setText('Fazendo Pirâmides...')
            #('gdalogr:overviews', input, levels=8, clean=False, resampling_method=0(nearest), format=1(Gtiff .ovr))
            processing.runalg('gdalogr:overviews', raster, 8, False, 0, 1)
    
    if int(float(count)/size*100) != p:
        p = int(float(count)/size*100)
        progress.setPercentage(p)    

    progress.setText('Fazendo raster virtual...')
    processing.runalg('gdalogr:buildvirtualraster', rasterList, 0, False, False, vrtfilename)