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
        """
        Reutilizo a interface do DsgTools para criar o spatialite desativando alguns elementos dela
        """
        super(CreateSqlite, self).__init__(parent)        
        self.versionComboBox.setVisible(False)
        self.label_4.setVisible(False)
        self.start()
        self.exec_()
    
    def start(self):
        """
        inicio as variáveis do ambiente
        """
        self.nameSqlite = None
        self.pathSqlite = None

    def stop(self):
        """
        apago as variáveis do ambiente
        """
        del self.nameSqlite
        del self.pathSqlite
            
    def getTemplateLocation(self):
        """redefino a função da classe CriaSpatialiteDialog para meu caso especifico ,ou seja,
        apontando para o meu modelo de Sqlite
        """
        self.nameSqlite = self.nomeLineEdit.text()
        self.stop()
        path  = os.path.join(os.path.dirname(__file__), 'templates', 'template.sqlite')        
        return path
    
    def definePastaDestino(self):
        """
        redefino a função da classe CriaSpatialiteDialog para o destino do Sqlite
        """
        fd = QtGui.QFileDialog()
        self.filepath = fd.getExistingDirectory()
        if self.filepath <> "":
            self.carregado = True
            self.pastaDestinoCriaSpatialiteLineEdit.setText(self.filepath)
            self.pathSqlite = self.filepath

