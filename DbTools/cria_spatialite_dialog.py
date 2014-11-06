# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CriaSpatialiteDialog
                                 A QGIS plugin
Create spatialite database built according to Brazilian's EDGV
                             -------------------
        begin                : 2014-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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

from PyQt4 import QtGui, uic, QtCore

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'carrega_categoria_dialog_base.ui'))
import cria_spatialite_dialog_base
import sqlite3, os
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis
from PyQt4 import QtGui
import sys

# class CarregaCategoriaDialog(QtGui.QDialog, FORM_CLASS):
class CriaSpatialiteDialog(QtGui.QDialog, cria_spatialite_dialog_base.Ui_CriaSpatialite):
    def __init__(self, parent=None):
        """Constructor."""
#         super(QtGui.QDialog).__init__(parent)

        super(CriaSpatialiteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
#         self.connect(self.pushButtonBuscarArquivo, QtCore.SIGNAL("clicked()"), self.carregaSpatialite)
        self.filepath = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsgCriaSpatialite = 0
        self.srsCriaSpatialite = ''
        self.sqliteFileName = ''

        self.setupUi(self)
        self.seedFile = os.path.dirname(__file__)+'/template/semente_edgv_com_codelists.sqlite'
        self.seedFile.replace('\\','/')

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(1)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

#         self.bar.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
#         self.addWidget(self.bar)

#
        QtCore.QObject.connect(self.pushButtonBuscarPastaDestinoCriaSpatialite, QtCore.SIGNAL(("clicked()")), self.definePastaDestino)
        QtCore.QObject.connect(self.pushButtonBuscarSistCoordCriaSpatialite, QtCore.SIGNAL(("clicked()")), self.setaSistCoordCriaSpatialite)
        QtCore.QObject.connect(self.pushButtonOkCriaSpatialite, QtCore.SIGNAL(("clicked()")), self.okselecionadoCriaSpatialite)
#
    def restauraInicio(self):
        self.filepath = ""
        self.carregado = False
        self.coordSysDefinido = False
        self.epsgCriaSpatialite = 0
        self.srsCriaSpatialite = ''
        self.sqliteFileName = ''
        self.pastaDestinoCriaSpatialiteLineEdit.setText("")
        self.coordSysCriaSpatialiteLineEdit.setText("")
        self.nomeLineEdit.setText("")



    def definePastaDestino(self):
        fd = QtGui.QFileDialog()
        self.filepath = fd.getExistingDirectory()
        if self.filepath <> "":
            self.carregado = True
            self.pastaDestinoCriaSpatialiteLineEdit.setText(self.filepath)



    def setaSistCoordCriaSpatialite(self):
        projSelector = QgsGenericProjectionSelector()
        projSelector.setMessage(theMessage='Selecione o Sistema de Coordenadas')
        projSelector.exec_()
        try:
            self.epsgCriaSpatialite = int(projSelector.selectedAuthId().split(':')[-1])
            self.srsCriaSpatialite = QgsCoordinateReferenceSystem(self.epsgCriaSpatialite, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.srsCriaSpatialite <> "":
                self.coordSysDefinido = True
                self.coordSysCriaSpatialiteLineEdit.setText(self.srsCriaSpatialite.description())
        except:
            self.bar.pushMessage("", "Selecione o sistema de coordenadas", level=QgsMessageBar.WARNING)
            pass

    def copiaSemente(self,destino,srid):
        f = open(self.seedFile,'rb')
        g = open(destino,'wb')
        x = f.readline()
        while x:
            g.write(x)
            x = f.readline()

        g.close()

        con = sqlite3.connect(destino)
        cursor = con.cursor()
        srid_sql = (srid,)
        cursor.execute("UPDATE geometry_columns SET srid=?",srid_sql)
        con.commit()
        con.close()



    def okselecionadoCriaSpatialite(self):

#
        if self.carregado and self.coordSysDefinido and len(self.nomeLineEdit.text()) > 0:

            try:
                self.sqliteFileName = self.filepath+'/'+self.nomeLineEdit.text()+'.sqlite'
                destino = self.sqliteFileName
                self.copiaSemente(destino,self.epsgCriaSpatialite)
                self.close()
                self.restauraInicio()
            except:
                qgis.utils.iface.messageBar().pushMessage("Erro!", "Entre com os par�metros corretamente!", level=QgsMessageBar.CRITICAL)
                self.restauraInicio()
                pass

        else:
#             qgis.utils.iface.messageBar().pushMessage("Erro!", "Selecione o sistema de coordenadas e o banco de dados corretamente!", level=QgsMessageBar.CRITICAL)
            if self.coordSysDefinido == False:
                self.bar.pushMessage("Erro!", "Selecione o sistema de coordenadas corretamente!", level=QgsMessageBar.CRITICAL)
            if self.carregado == False:
                self.bar.pushMessage("Erro!", "Selecione a pasta de Destino!", level=QgsMessageBar.CRITICAL)
            if len(self.nomeLineEdit.text()) == 0:
                self.bar.pushMessage("Erro!", "Entre com o nome do arquivo!", level=QgsMessageBar.CRITICAL)


#             self.pushMessage("Erro!", "Selecione o sistema de coordenadas e o banco de dados corretamente!", level=QgsMessageBar.WARNING)


