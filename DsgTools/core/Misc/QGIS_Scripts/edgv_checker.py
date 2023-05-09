##DSG=group
##Pasta_de_Busca=folder
##Relatorio=output table

import csv, os
from osgeo import ogr


def edgv_checker(folder, output):
    """
    Checks if a spatialite is a dsgtools database
    """
    csvfile = open(output, "wb")
    outwriter = csv.writer(csvfile)
    outwriter.writerow(["arquivo", "edgv"])

    for root, dirs, files in os.walk(folder):
        count = 0
        size = len(files)
        p = 0
        progress.setPercentage(p)
        for file in files:
            if ".sqlite" not in file:
                continue
            file = os.path.join(root, file)
            ogrSrc = ogr.Open(file)
            isEdgv = False
            if ogrSrc:
                layer = ogrSrc.GetLayerByName("cb_adm_area_pub_civil_a")
                isEdgv = True if layer else False
            outwriter.writerow([file, isEdgv])

            if int(float(count) / size * 100) != p:
                p = int(float(count) / size * 100)
                progress.setPercentage(p)

    csvfile.close()


edgv_checker(Pasta_de_Busca, Relatorio)
