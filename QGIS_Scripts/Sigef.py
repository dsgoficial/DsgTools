##DSG=group
##Perimetro=vector
##Dados_SIGEF=output table

from qgis.core import *
import csv

def dd2dms_sigef(dd):
    # calculos com numeros
    d = int(dd)
    m = abs(int(60*(dd-int(dd))))
    s = abs((dd-d-m/60)*60)
    s_int = int(s)
    s_d = s - s_int
    # fazendo as strings
    d = str(d).zfill(2)
    m = str(m).zfill(2)
    s_int = str(s_int).zfill(2)
    s_d = str(s_d).split('.')[-1]
    # fazendo o retorno
    dms_sigef = d+','+m+s_int+'%0.3s'%s_d
    return dms_sigef
    
def createCSV(input, output):
    layer = processing.getObject(input)
    features = layer.selectedFeatures()
    if len(features) != 1:
        progress.setInfo('Selecione uma e somente uma geometria!')
        return
        
    csvfile = open(output, 'wb')
    outwriter = csv.writer(csvfile)
    outwriter.writerow(['id', 'Long', 'Lat'])

    feature = features[0]
    geom = feature.geometry()
    polygon = geom.asPolygon()
    outring = polygon[0]
    count = 0
    for point in outring:
        outwriter.writerow([str(count), dd2dms_sigef(point[0]), dd2dms_sigef(point[1])])
        count += 1
    csvfile.close()
        
createCSV(Perimetro, Dados_SIGEF)