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
 *************
"""

import os
from typing import List
import requests
from dataclasses import MISSING, dataclass
from DsgTools.core.Utils.utils import Utils
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
    
    def downloadFile(self, config: ExternalFileHandlerConfig, proxyInfo=None, proxyAuth=None) -> bool:
        """
        Downloads the file.
        """
        if not self.isFileDownloaded(config):
            r = requests.get(config.url, stream=True, proxies=proxyInfo, auth=proxyAuth)
            with open(self.getFullPath(config), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            return True
        else:
            return False

    def promptForDownload(self, externalFileConfigList: List[ExternalFileHandlerConfig]) -> List[ExternalFileHandlerConfig]:
        """
        Prompts the user to download the file if it is not already downloaded.
        """
        notDownloadedList = [i for i in externalFileConfigList if not self.isFileDownloaded(i)]
        if len(notDownloadedList) == 0:
            return []
        reply = QMessageBox.question(
            self.parent,
            self.tr('Download Files'),
            self.tr('The following files are not downloaded. Do you want to download them?'), 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        return notDownloadedList

    def process(self, fileConfigList: List[ExternalFileHandlerConfig], prompt=True) -> bool:
        """
        Processes the list of files.
        """
        downloadList = self.promptForDownload(fileConfigList) if prompt else fileConfigList
        if len(downloadList) == 0:
            return False
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            for fileConfig in downloadList:
                processing.run(
                    "native:filedownloader",
                    {
                        'URL': fileConfig.url,
                        'OUTPUT': self.getFullPath(fileConfig),
                    }
                )
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                self.tr('Error'),
                self.tr('Could not download the following files: {}'.format(e))
            )
        QApplication.restoreOverrideCursor()
        return True
