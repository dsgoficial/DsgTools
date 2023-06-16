# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-01-10
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from typing import List
from dataclasses import MISSING, dataclass
from qgis.PyQt.QtWidgets import QMessageBox, QApplication
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtCore import QObject, Qt
from abc import ABC

import processing


@dataclass
class ExternalFileHandlerConfig(ABC):
    url: str = MISSING
    file_name: str = MISSING
    output_folder: str = MISSING


class ExternalFileDownloadProcessor(QObject):
    def __init__(self, parent=None):
        super(ExternalFileDownloadProcessor, self).__init__()
        self.parent = parent

    def getFullPath(self, config: ExternalFileHandlerConfig):
        return os.path.join(config.output_folder, config.file_name)

    def isFileDownloaded(self, config: ExternalFileHandlerConfig) -> bool:
        """
        Checks if the file is already downloaded.
        """
        return os.path.isfile(self.getFullPath(config))

    def promptForDownload(
        self, externalFileConfigList: List[ExternalFileHandlerConfig]
    ) -> bool:
        """
        Prompts the user to download the file if it is not already downloaded.
        """
        fileName = ""
        for file in externalFileConfigList:
            if len(fileName) > 100:
                fileName = fileName + " and others"
            if fileName == "":
                fileName = file.file_name
            else:
                fileName = fileName + ", " + file.file_name
        reply = QMessageBox.question(
            self.parent,
            self.tr("Download Files"),
            self.tr(
                "The following files: {} are not downloaded. Do you want to download them?".format(
                    fileName
                )
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.No:
            return False
        return True

    def process(
        self, fileConfigList: List[ExternalFileHandlerConfig], prompt=True
    ) -> int:
        """
        Processes the list of files.
        """
        downloadList = (
            [i for i in fileConfigList if not self.isFileDownloaded(i)]
            if prompt
            else fileConfigList
        )
        if len(downloadList) == 0:
            return 1
        reply = self.promptForDownload(fileConfigList)
        if not reply:
            return 0
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for file in fileConfigList:
            if not os.path.isdir(file.output_folder):
                os.makedirs(file.output_folder)
        try:
            for fileConfig in downloadList:
                processing.run(
                    "native:filedownloader",
                    {
                        "URL": fileConfig.url,
                        "OUTPUT": self.getFullPath(fileConfig),
                    },
                )
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                self.tr("Error"),
                self.tr("Could not download the following files: {}".format(e)),
            )
        QApplication.restoreOverrideCursor()
        return 2
