# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os

from pathlib import Path
import zipfile

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterFile,
)


class BuildZipPackageAlgorithm(QgsProcessingAlgorithm):

    INPUT_SHAPEFILE_FOLDER = "INPUT_SHAPEFILE_FOLDER"
    OUTPUT_PREFIX = "OUTPUT_PREFIX"
    OUTPUT_ZIP_FOLDER = "OUTPUT_ZIP_FOLDER"

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_SHAPEFILE_FOLDER,
                self.tr("Pasta com Shapefiles"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_PREFIX,
                description=self.tr("Output files prefix"),
                multiLine=False,
                defaultValue="Carta_Topografica_",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_ZIP_FOLDER,
                self.tr("Pasta de destino"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        

    def processAlgorithm(self, parameters, context, feedback):
        folderPath = self.parameterAsString(parameters, self.INPUT_SHAPEFILE_FOLDER, context)
        outputPrefix = self.parameterAsString(parameters, self.OUTPUT_PREFIX, context)
        outputFolderPath = self.parameterAsString(parameters, self.OUTPUT_ZIP_FOLDER, context)
        p = Path(folderPath)
        folderList = [f.stem for f in p.iterdir() if f.is_dir()]
        if len(folderList) == 0:
            return {}
        stepSize = 100/len(folderList)
        for current, folderName in enumerate(folderList):
            if feedback.isCanceled():
                break
            outputZipName = f"{outputPrefix}{folderName}"
            with zipfile.ZipFile(
                Path(outputFolderPath, f'{outputZipName}.zip'), 'w', zipfile.ZIP_DEFLATED
            ) as zf:
                for item in Path(p / folderName).glob("*"):
                    if '.DS_Store' in str(item) or '__MACOSX/' in str(item):
                        continue
                    zf.write(item, Path(folderName / item.relative_to(os.path.dirname(item))))

            feedback.setProgress(current * stepSize)
        return {}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "buildzippackagealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Builds shapefile package")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Layer Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Layer Management Algorithms"

    def tr(self, string):
        """
        Translates input string.
        """
        return QCoreApplication.translate("BuildZipPackageAlgorithm", string)

    def createInstance(self):
        """
        Creates an instance of this class
        """
        return BuildZipPackageAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
    
    def shortHelpString(self):
        return self.tr("This algorithm loads shapefiles from folders. If a folder with subfolders is selected, one extra node is created for each subfolder")
