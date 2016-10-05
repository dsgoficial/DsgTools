# -*- coding: utf-8 -*-
"""
/***************************************************************************
militarySymbology
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-10-05
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
# Qt imports
from PyQt4 import uic, QtGui

# lib python imports
import sqlite3, os

#DsgTools imports
from DsgTools.DbTools.SpatialiteTool.cria_spatialite_dialog import CriaSpatialiteDialog

class CreateSqlite(CriaSpatialiteDialog):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(CreateSqlite, self).__init__(parent)        
        self.versionComboBox.setVisible(False)
        self.label_4.setVisible(False)
        self.start()
        self.exec_()
                         
    def start(self):
        self.nameSqlite = None
        self.pathSqlite = None
    
    def stop(self):
        del self.nameSqlite
        del self.pathSqlite
            
    def getTemplateLocation(self):
        self.nameSqlite = self.nomeLineEdit.text()
        self.stop()
        path  = os.path.join(os.path.dirname(__file__), 'templates', 'template.sqlite')        
        return path
    
    def definePastaDestino(self):
        fd = QtGui.QFileDialog()
        filepath = fd.getExistingDirectory()
        if filepath <> "":
            self.carregado = True
            self.pastaDestinoCriaSpatialiteLineEdit.setText(filepath)
            self.pathSqlite = filepath
            
        