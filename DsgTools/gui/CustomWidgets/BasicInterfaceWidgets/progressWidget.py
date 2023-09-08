# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProgressWidget
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-10
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.gui import QgsMessageBar, QgsMessageBarItem
from qgis.core import Qgis
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QProgressBar, QSizePolicy
import time


class ProgressWidget(QgsMessageBar):
    def __init__(self, min, max, message, parent=None, timeout=2):
        """
        Constructs a progress widget
        """
        super(self.__class__, self).__init__(parent)
        self.min = min
        self.max = max
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        if parent:
            self.setMinimumSize(parent.width(), 40)
        else:
            self.setMinimumSize(766, 40)
        self.setSizePolicy(sizePolicy)
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(min)
        self.progressBar.setMaximum(max)
        self.parent = parent
        self.msgBarItem = QgsMessageBarItem(
            self.tr("INFO: "),
            message,
            self.progressBar,
            level=Qgis.MessageLevel.Info,
            duration=timeout,
            parent=self.parent,
        )
        self.pushItem(self.msgBarItem)
        self.parent.repaint()

    def initBar(self):
        """
        Initializes the progress bar
        """
        self.progressBar.setValue(0)

    def step(self):
        """
        Increments the progress bar
        """
        value = self.progressBar.value() + 1
        self.progressBar.setValue(value)
        if value == self.max:
            time.sleep(1)
            self.close()
