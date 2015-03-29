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
"""# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QRunnable, pyqtSignal

class GenericThread(QRunnable):
    rangeCalculated = pyqtSignal(int)
    stepProcessed = pyqtSignal()
    processingFinished = pyqtSignal(int, str)
    
    def __init__(self):
        """Constructor.
        """
        super(GenericThread, self).__init__()

    def run(self):
        pass
