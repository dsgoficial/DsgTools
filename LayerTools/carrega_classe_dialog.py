# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CarregaClasseDialog
                                 A QGIS plugin
 Load database classes.
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
import carrega_classe_dialog_base
import sqlite3, os
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis
from PyQt4 import QtGui
import sys

# class CarregaClasseDialog(QtGui.QDialog, FORM_CLASS):
class CarregaClasseDialog(QtGui.QDialog, carrega_classe_dialog_base.Ui_CarregaClasse):
    def __init__(self, parent=None):
        """Constructor."""
#         super(QtGui.QDialog).__init__(parent)

        super(CarregaClasseDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
#         self.connect(self.pushButtonBuscarArquivo, QtCore.SIGNAL("clicked()"), self.carregaSpatialite)
        self.filename = ""
        self.bdCarregado = False
        self.coordSysDefinido = False
        self.boolSomenteComElementos = False
        self.epsg = 0
        self.srs = ''
        self.classes = []
        self.classesSelecionadas = []
        self.setupUi(self)
        #qmlPath will be set as /qml_qgis/qgis_22/edgv_213/, but in a further version, there will be an option to detect from db
        version = qgis.core.QGis.QGIS_VERSION
        if version == '2.6.0-Brighton':
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_26/edgv_213/'
        else:
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_22/edgv_213/'
        self.qmlPath.replace('\\','/')


        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)


        QtCore.QObject.connect(self.pushButtonBuscarArquivo, QtCore.SIGNAL(("clicked()")), self.carregaSpatialite)
        QtCore.QObject.connect(self.arquivoLineEditCarregaClasse, QtCore.SIGNAL(("textChanged(QString)")), self.listaCategorias)
        QtCore.QObject.connect(self.pushButtonCancelarCarregaClasse, QtCore.SIGNAL(("clicked()")), self.cancela)
        QtCore.QObject.connect(self.checkBoxTodosCarregaClasse, QtCore.SIGNAL(("stateChanged(int)")), self.selecionaTodas)
        QtCore.QObject.connect(self.pushButtonOkCarregaClasse, QtCore.SIGNAL(("clicked()")), self.okselecionado)

    def restauraInicio(self):
        self.filename = ""
        self.bdCarregado = False
        self.coordSysDefinido = False
        self.boolSomenteComElementos = False
        self.epsg = 0
        self.srs = ''
        self.classes = []
        self.classesSelecionadas = []
        self.arquivoLineEditCarregaClasse.setText(self.filename)
        self.coordSysLineEditCarregaClasse.setText(self.srs)
        self.coordSysLineEditCarregaClasse.setReadOnly(False)


        tam = self.listWidgetOrigemCategoriaCarregaClasse.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetOrigemCategoriaCarregaClasse.takeItem(i-2)


        self.checkBoxTodosCarregaClasse.setCheckState(0)





    def carregaSpatialite(self):
        fd = QtGui.QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.bdCarregado = True
            self.arquivoLineEditCarregaClasse.setText(self.filename)

    def updateBDField(self):
        if self.bdCarregado == True:
            self.arquivoLineEditCarregaClasse.setText(self.filename)
        else:
            self.filename = ""
            self.arquivoLineEditCarregaClasse.setText(self.filename)



    def setaSistCoord(self):
        projSelector = QgsGenericProjectionSelector()
        projSelector.setMessage(theMessage='Selecione o Sistema de Coordenadas')
        projSelector.exec_()
        try:
            self.epsg = int(projSelector.selectedAuthId().split(':')[-1])
            self.srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.srs <> "":
                self.coordSysDefinido = True
                self.coordSysLineEdit.setText(self.srs.description())
        except:
            self.bar.pushMessage("", "Selecione o sistema de coordenadas", level=QgsMessageBar.WARNING)
            pass

    def contaElementos(self,lista):
        con = sqlite3.connect(self.filename)
        cursor = con.cursor()
        listaQuantidades = []
        for i in lista:
            cursor.execute("SELECT count() FROM "+i[0]+";")
            listaQuantidades.append(cursor.fetchall()[0][0])

        return listaQuantidades

    def defineCamadasComElementos(self):
        pontoAux = self.contaElementos(self.ponto)
        linhaAux = self.contaElementos(self.linha)
        areaAux = self.contaElementos(self.area)
        count = 0
        for i in pontoAux:
            if i > 0:
                self.pontoComElemento.append(self.ponto[count])
            count+=1
        count = 0
        for i in linhaAux:
            if i > 0:
                self.linhaComElemento.append(self.linha[count])
            count+=1
        count = 0

        for i in areaAux:
            if i > 0:
                self.areaComElemento.append(self.area[count])
            count+=1


    def listaCategorias(self):
        con = sqlite3.connect(self.filename)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tableList = cursor.fetchall()

        for i in tableList:

            if (i[0].split("_")[-1] == "p"):
                self.classes.append(i[0])
            if (i[0].split("_")[-1] == "l"):
                self.classes.append(i[0])
            if (i[0].split("_")[-1] == "a"):
                self.classes.append(i[0])

        self.classes.sort() #coloca em ordem alfabetica


        for i in self.classes:
            item = QtGui.QListWidgetItem(i)
            self.listWidgetOrigemCategoriaCarregaClasse.addItem(item)
        try:
            self.epsg = self.descobreEPSG(cursor)

            if self.epsg == -1:
                self.bar.pushMessage("", "Sistema de Coordenadas n�o definido ou inv�lido", level=QgsMessageBar.WARNING)
            else:
                self.srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                self.coordSysLineEditCarregaClasse.setText(self.srs.description())
                self.coordSysLineEditCarregaClasse.setReadOnly(True)
                self.bdCarregado = True
        except:
           # self.bar.pushMessage("", "Sistema de Coordenadas n�o definido ou inv�lido", level=QgsMessageBar.WARNING)
            pass



    def descobreEPSG(self,cursor):
        cursor.execute("SELECT srid from geometry_columns;")
        lista = cursor.fetchall()
        return lista[0][0]

    def cancela(self):
        self.restauraInicio()


    def selecionaTodas(self):
        if self.checkBoxTodosCarregaClasse.isChecked():
            tam = self.listWidgetOrigemCategoriaCarregaClasse.__len__()
            for i in range(tam+1):
                item = self.listWidgetOrigemCategoriaCarregaClasse.item(i-1)
                self.listWidgetOrigemCategoriaCarregaClasse.setItemSelected(item,2)
                #self.listWidgetDestinoCategoria.addItem(item)
            #self.listWidgetDestinoCategoria.sortItems()
        else:
            tam = self.listWidgetOrigemCategoriaCarregaClasse.__len__()
            for i in range(tam+1):
                item = self.listWidgetOrigemCategoriaCarregaClasse.item(i-1)
                self.listWidgetOrigemCategoriaCarregaClasse.setItemSelected(item,0)



    def setaDiretorioQml(self):
        fd = QtGui.QFileDialog()
        dir = fd.getExistingDirectory()
        return dir.replace('\\','/')+'/'

    def geraListaSelecionados(self):
        lista = self.listWidgetOrigemCategoriaCarregaClasse.selectedItems()
        self.classesSelecionadas = []
        tam = len(lista)
        for i in range(tam):
            self.classesSelecionadas.append(lista[i].text())
        self.classesSelecionadas.sort()

        #self.classes


    def okselecionado(self):
        f = self.filename
        xmlfilepath = self.qmlPath
        coordSys = self.srs
        self.geraListaSelecionados()
        uri = QgsDataSourceURI()
        uri.setDatabase(f)
        schema = ''
        geom_column = 'GEOMETRY'
        if len(self.classesSelecionadas)>0:
            try:
                for i in self.classesSelecionadas:
                    self.carregaCamada(uri, i, schema, geom_column, coordSys, xmlfilepath)
                self.restauraInicio()
                self.close()
            except:
                self.bar.pushMessage("Erro!", "Entre com os par�metros corretamente!", level=QgsMessageBar.CRITICAL)
        else:
            self.bar.pushMessage("Erro!", "Selecione pelo menos uma classe!", level=QgsMessageBar.CRITICAL)

    def carregaCamada(self,uri, nome_camada,schema,geom_column, coordSys,xmlfilepath):
        uri.setDataSource(schema, nome_camada, geom_column)
        display_name = nome_camada
        vlayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        vlayer.setCrs(coordSys)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        vlayer.loadNamedStyle(xmlfilepath+nome_camada.replace('\r','')+'.qml',False)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
