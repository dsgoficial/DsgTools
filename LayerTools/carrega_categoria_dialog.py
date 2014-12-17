# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CarregaClasseDialog
                                 A QGIS plugin
 Load database classes grouping them by EDGV's categories.
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
import carrega_categoria_dialog_base
import sqlite3, os
from PyQt4.QtCore import QFileInfo,QSettings
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry
from qgis.gui import QgsGenericProjectionSelector,QgsMessageBar
import qgis as qgis
from PyQt4 import QtGui
import sys

# class CarregaCategoriaDialog(QtGui.QDialog, FORM_CLASS):
class CarregaCategoriaDialog(QtGui.QDialog, carrega_categoria_dialog_base.Ui_Form):
    def __init__(self, parent=None):
        """Constructor."""
        super(CarregaCategoriaDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.filename = ""
        self.bdCarregado = False
        self.coordSysDefinido = False
        self.boolSomenteComElementos = False
        self.epsg = 0
        self.srs = ''
        self.ponto = []
        self.linha = []
        self.area = []
        self.categorias = []
        self.categoriasSelecionadas = []
        self.setupUi(self)
        #qmlPath will be set as /qml_qgis/qgis_22/edgv_213/, but in a further version, there will be an option to detect from db
        version = qgis.core.QGis.QGIS_VERSION
        if version == '2.6.0-Brighton':
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_26/edgv_213/'
        else:
            self.qmlPath = os.path.dirname(__file__)+'/qml_qgis/qgis_22/edgv_213/'
        self.qmlPath.replace('\\','/')
        self.pontoComElemento = []
        self.linhaComElemento = []
        self.areaComElemento = []

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(1)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        QtCore.QObject.connect(self.pushButtonBuscarArquivo, QtCore.SIGNAL(("clicked()")), self.carregaSpatialite)
        QtCore.QObject.connect(self.arquivoLineEdit, QtCore.SIGNAL(("textChanged(QString)")), self.listaCategorias)
        QtCore.QObject.connect(self.pushButtonBuscarSistCoord, QtCore.SIGNAL(("clicked()")), self.setaSistCoord)
        QtCore.QObject.connect(self.pushButtonSelecionaTodas, QtCore.SIGNAL(("clicked()")), self.selecionaTodas)
        QtCore.QObject.connect(self.pushButtonDeselecionaTodas, QtCore.SIGNAL(("clicked()")), self.deselecionaTodas)
        QtCore.QObject.connect(self.pushButtonSelecionaUma, QtCore.SIGNAL(("clicked()")), self.selecionaUma)
        QtCore.QObject.connect(self.pushButtonDeselecionaUma, QtCore.SIGNAL(("clicked()")), self.deselecionaUma)
        QtCore.QObject.connect(self.checkBoxTodos, QtCore.SIGNAL(("stateChanged(int)")), self.setaBoolTodos)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(("clicked()")), self.okselecionado)
        QtCore.QObject.connect(self.pushButtonCancelar, QtCore.SIGNAL(("clicked()")), self.cancela)

    def restauraInicio(self):
        self.filename = ""
        self.bdCarregado = False
        self.coordSysDefinido = False
        self.boolSomenteComElementos = False
        self.epsg = 0
        self.srs = ''
        self.ponto = []
        self.linha = []
        self.area = []
        self.pontoComElemento = []
        self.linhaComElemento = []
        self.areaComElemento = []
        self.categorias = []
        self.categoriasSelecionadas = []
        self.arquivoLineEdit.setText(self.filename)
        self.coordSysLineEdit.setText(self.srs)
        self.categoriasSelecionadas = []

        tam = self.listWidgetOrigemCategoria.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetOrigemCategoria.takeItem(i-2)

        tam1 = self.listWidgetDestinoCategoria.__len__()
        for i in range(tam1+1,1,-1):
            item = self.listWidgetDestinoCategoria.takeItem(i-2)

        self.checkBoxPonto.setCheckState(0)
        self.checkBoxLinha.setCheckState(0)
        self.checkBoxArea.setCheckState(0)
        self.checkBoxTodos.setCheckState(0)
        self.checkBoxSomenteElementos.setCheckState(0)
        self.pushButtonBuscarSistCoord.setEnabled(True)

    def carregaSpatialite(self):
        fd = QtGui.QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.carregado = True
            self.arquivoLineEdit.setText(self.filename)


    def updateBDField(self):
        if self.bdCarregado == True:
            self.arquivoLineEdit.setText(self.filename)
            self.arquivoLineEdit.setReadOnly(True)
            if self.coordSysDefinido == False:
                self.updateSistCoordField()    #problema aqui

        else:
            self.filename = ""
            self.arquivoLineEdit.setText(self.filename)
            self.srs = ""
            self.coordSysLineEdit.setText(self.srs)

    def descobreEPSG(self):
        con = sqlite3.connect(self.filename)
        cursor = con.cursor()
        cursor.execute("SELECT srid from geometry_columns;")
        lista = cursor.fetchall()
        return lista[0][0]

    def updateSistCoordField(self):
        try:

            epsg = self.descobreEPSG()

            if epsg == -1:
                self.bar.pushMessage("", "Sistema de coordenadas n�o definido.", level=QgsMessageBar.WARNING)
                self.coordSysLineEdit.setReadOnly(False)
                self.pushButtonBuscarSistCoord.setEnabled(True)
            else:
                self.pushButtonBuscarSistCoord.setEnabled(False)
                self.epsg = epsg
                self.srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                if self.srs <> "":
                    self.coordSysDefinido = True
                    self.coordSysLineEdit.setText(self.srs.description())
                    self.coordSysLineEdit.setReadOnly(True)
        except:
            pass

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
                self.ponto.append(i)
            if (i[0].split("_")[-1] == "l"):
                self.linha.append(i)
            if (i[0].split("_")[-1] == "a"):
                self.area.append(i)

        categoriasAux = []
        for i in self.ponto:
            categoriasAux.append(i[0].split("_")[0])
        for i in self.linha:
            categoriasAux.append(i[0].split("_")[0])
        for i in self.area:
            categoriasAux.append(i[0].split("_")[0])

        for j in categoriasAux:
            if j not in self.categorias:
                self.categorias.append(j)
        self.categorias.sort() #coloca em ordem alfabetica
        self.ponto.sort()
        self.linha.sort()
        self.area.sort()
        for i in self.categorias:
            item = QtGui.QListWidgetItem(i)
            self.listWidgetOrigemCategoria.addItem(item)
        self.bdCarregado = True
        self.updateBDField()

    def selecionaTodas(self):
        tam = self.listWidgetOrigemCategoria.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetOrigemCategoria.takeItem(i-2)
            self.listWidgetDestinoCategoria.addItem(item)
        self.listWidgetDestinoCategoria.sortItems()

    def deselecionaTodas(self):
        tam = self.listWidgetDestinoCategoria.__len__()
        for i in range(tam+1,1,-1):
            item = self.listWidgetDestinoCategoria.takeItem(i-2)
            self.listWidgetOrigemCategoria.addItem(item)
        self.listWidgetOrigemCategoria.sortItems()

    def selecionaUma(self):
        listedItems = self.listWidgetOrigemCategoria.selectedItems()
        for i in listedItems:
            item = self.listWidgetOrigemCategoria.takeItem(self.listWidgetOrigemCategoria.row(i))
            self.listWidgetDestinoCategoria.addItem(item)
        self.listWidgetDestinoCategoria.sortItems()

    def deselecionaUma(self):
        listedItems = self.listWidgetDestinoCategoria.selectedItems()
        for i in listedItems:
            item = self.listWidgetDestinoCategoria.takeItem(self.listWidgetDestinoCategoria.row(i))
            self.listWidgetOrigemCategoria.addItem(item)
        self.listWidgetOrigemCategoria.sortItems()

    def setaBoolPonto(self):
        if self.checkBoxPonto.isChecked() and self.checkBoxLinha.isChecked() and self.checkBoxArea.isChecked():
            self.checkBoxTodos.setCheckState(2)
        else:
            self.checkBoxTodos.setCheckState(0)

    def setaBoolLinha(self):
        if self.checkBoxPonto.isChecked() and self.checkBoxLinha.isChecked() and self.checkBoxArea.isChecked():
            self.checkBoxTodos.setCheckState(2)
        else:
            self.checkBoxTodos.setCheckState(0)

    def setaBoolArea(self):
        if self.checkBoxPonto.isChecked() and self.checkBoxLinha.isChecked() and self.checkBoxArea.isChecked():
            self.checkBoxTodos.setCheckState(2)
        else:
            self.checkBoxTodos.setCheckState(0)

    def setaBoolTodos(self):
        if self.checkBoxTodos.isChecked():
            self.checkBoxPonto.setCheckState(2)
            self.checkBoxLinha.setCheckState(2)
            self.checkBoxArea.setCheckState(2)
        else:
            self.checkBoxPonto.setCheckState(0)
            self.checkBoxLinha.setCheckState(0)
            self.checkBoxArea.setCheckState(0)

    def setaDiretorioQml(self):
        fd = QtGui.QFileDialog()
        dir = fd.getExistingDirectory()
        return dir.replace('\\','/')+'/'

    def okselecionado(self):
        f = self.filename
        xmlfilepath = self.qmlPath
        print xmlfilepath
        coordSys = self.srs

        if self.checkBoxSomenteElementos.isChecked():
            self.defineCamadasComElementos()
            ponto = self.pontoComElemento
            linha = self.linhaComElemento
            area = self.areaComElemento
        else:
            ponto = self.ponto
            linha = self.linha
            area = self.area

        if self.bdCarregado and self.coordSysDefinido and len(self.listWidgetDestinoCategoria)>0:
            self.categoriasSelecionadas = []

            for i in range(self.listWidgetDestinoCategoria.__len__()):
                self.categoriasSelecionadas.append(self.listWidgetDestinoCategoria.item(i).text())

            try:
                if self.checkBoxPonto.isChecked():
                    self.carregaCamadas(f,xmlfilepath,coordSys,'p',self.categoriasSelecionadas,ponto)

                if self.checkBoxLinha.isChecked():
                    self.carregaCamadas(f,xmlfilepath,coordSys,'l',self.categoriasSelecionadas,linha)

                if self.checkBoxArea.isChecked():
                    self.carregaCamadas(f,xmlfilepath,coordSys,'a',self.categoriasSelecionadas,area)

                if self.checkBoxPonto.isChecked()== False and self.checkBoxLinha.isChecked() == False and self.checkBoxArea.isChecked() == False:
                    self.bar.pushMessage("Erro!", "Selecione pelo menos uma primitiva geom�trica!", level=QgsMessageBar.CRITICAL)
                else:
                    self.close()
                    self.restauraInicio()
            except:
                qgis.utils.iface.messageBar().pushMessage("Erro!", "Entre com os par�metros corretamente!", level=QgsMessageBar.CRITICAL)
                pass

        else:
            if self.bdCarregado == True and self.coordSysDefinido == False:
                self.bar.pushMessage("Erro!", "Selecione o sistema de coordenadas corretamente!", level=QgsMessageBar.CRITICAL)
            if self.bdCarregado == False and self.coordSysDefinido == False:
                self.bar.pushMessage("Erro!", "Selecione o banco de dados corretamente!", level=QgsMessageBar.CRITICAL)
                self.bar.pushMessage("Erro!", "Selecione o sistema de coordenadas corretamente!", level=QgsMessageBar.CRITICAL)
            if len(self.listWidgetDestinoCategoria)==0:
                self.bar.pushMessage("Erro!", "Selecione pelo menos uma categoria!", level=QgsMessageBar.CRITICAL)
            self.categoriasSelecionadas = []
            self.pontoComElemento = []
            self.linhaComElemento = []
            self.areaComElemento = []

    def carregaCamada(self,uri, nome_camada,schema,geom_column, coordSys,grupo,xmlfilepath):
        uri.setDataSource(schema, nome_camada[0], geom_column)
        display_name = nome_camada[0]
        vlayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        vlayer.setCrs(coordSys)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        vlayer.loadNamedStyle(xmlfilepath+nome_camada[0].replace('\r','')+'.qml',False)

        grupo.append(vlayer)
        return vlayer

    def carregaCamadaPrimitivaCategoria(self,uri,nomeCategoria,listaCamadas,schema,geom_column, coordSys,idGrupo,xmlfilepath):
        grupoCarga = []
        idSubgrupo = qgis.utils.iface.legendInterface().addGroup(nomeCategoria,True,idGrupo)
        for camada in listaCamadas:
            if camada[0].split("_")[0] == nomeCategoria:
                self.carregaCamada(uri,camada,schema,geom_column, coordSys,grupoCarga,xmlfilepath)

        QgsMapLayerRegistry.instance().addMapLayers(grupoCarga)
        for i in grupoCarga:

            qgis.utils.iface.legendInterface().moveLayer(i, idSubgrupo)


    def carregaCamadaPrimitiva(self,uri,primitiva,listaCategorias,listaCamadas,schema,geom_column, coordSys,xmlfilepath):
        if primitiva == 'p':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Ponto", -1)
            for categoria in listaCategorias:
                self.carregaCamadaPrimitivaCategoria(uri,categoria,listaCamadas,schema,geom_column, coordSys,idGrupo,xmlfilepath)
        if primitiva == 'l':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Linha", -1)
            for categoria in listaCategorias:
                self.carregaCamadaPrimitivaCategoria(uri,categoria,listaCamadas,schema,geom_column, coordSys,idGrupo,xmlfilepath)
        if primitiva == 'a':
            idGrupo = qgis.utils.iface.legendInterface (). addGroup ("Area", -1)
            for categoria in listaCategorias:
                self.carregaCamadaPrimitivaCategoria(uri,categoria,listaCamadas,schema,geom_column, coordSys,idGrupo,xmlfilepath)

    def carregaCamadas(self,filename,xmlfilepath,coordSys,primitiva,listaCategorias,listaCamadas):
        s = QSettings()
        oldValidation = s.value("/Projections/defaultBehaviour")
        s.setValue("/Projections/defaultBehaviour","useGlobal")

        uri = QgsDataSourceURI()
        uri.setDatabase(filename)
        schema = ''
        geom_column = 'GEOMETRY'

        self.carregaCamadaPrimitiva(uri,primitiva,listaCategorias,listaCamadas,schema,geom_column, coordSys,xmlfilepath)
        s.setValue("/Projections/defaultBehaviour",oldValidation)

    def cancela(self):
        self.restauraInicio()
