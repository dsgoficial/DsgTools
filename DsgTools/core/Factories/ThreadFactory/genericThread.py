# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
from builtins import str
from qgis.PyQt.QtCore import QObject, pyqtSignal, QRunnable

from uuid import uuid4


class ProcessSignals(QObject):
    rangeCalculated = pyqtSignal(int, str)
    stepProcessed = pyqtSignal(str)
    processingFinished = pyqtSignal(int, str, str)
    loadFile = pyqtSignal(str, bool)


class GenericThread(QRunnable):
    def __init__(self):
        """
        Constructor.
        """
        super(GenericThread, self).__init__()

        self.id = str(uuid4())

        self.signals = ProcessSignals()

    def run(self):
        pass

    def getId(self):
        return self.id
