#! -*- coding: UTF-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin FreeHandEditting
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from builtins import range
from builtins import object
from qgis.PyQt import QtGui, QtCore
from qgis import core, gui

class AcquisitionFreeController(object):

    def __init__(self, acquisitionFree, iface):
        #Construtor
        super(AcquisitionFreeController, self).__init__()
        self.acquisitionFree = acquisitionFree
        self.iface = iface
        self.active = False
           
    def setIface(self, iface):
        #Método para definir classe iface
        #Parâmetro de entrada: iface (classe iface do Qgis)
        self.iface = i

    def getIface(self):
        #Método para obter classe iface do Qgis
        #Parâmetro de retorno: iface (classe do Qgis)
        return self.iface

    def setActionAcquisitionFree(self, actionAcquisitionFree):
        #Método para definir a classe ActionAcquisitionFree
        #Parâmetro de entrada: actionAcquisitionFree (classe ActionAcquisitionFree)
        self.actionAcquisitionFree = actionAcquisitionFree
        
    def getActionAcquisitionFree(self):
        #Método para obter a classe ActionAcquisitionFree
        #Parâmetro de retorno: self.actionAcquisitionFree (classe ActionAcquisitionFree)
        return self.actionAcquisitionFree 

    def setAcquisitionFree(self, acquisitionFree):
        #Método para definir a classe AcquisitionFree
        #Parâmetro de entrada: acquisitionFree (classe AcquisitionFree)
        self.acquisitionFree = acquisitionFree

    def getAcquisitionFree(self):
        #Método para obter a classe AcquisitionFree
        #Parâmetro de retorno: self.acquisitionFree (classe AcquisitionFree)
        return self.acquisitionFree

    def setActiveState(self, state):
        #Método para definir estado da ferramento (ativada ou desativada)
        #Parâmetro de entrada: state (boleano)
        self.active = state
    
    def getActiveState(self):
        #Método para obter estado da tool (ativada ou desativada)
        #Parâmetro de retorno: state (boleano)
        return self.active
    
    def connectToolSignals(self):
        #Método para iniciar sinais do plugin 
        iface = self.getIface()
        iface.actionToggleEditing().triggered.connect(self.checkToActiveAction)
        iface.mapCanvas().mapToolSet['QgsMapTool*'].connect(self.deactivateTool)
        actionAcquisitionFree = self.getActionAcquisitionFree()
        actionAcquisitionFree.triggered.connect(self.activateTool)

    def checkToActiveAction(self):
        #Método para testar se a camada ativa é valida para ativar a ferramenta
        actionAcquisitionFree = self.getActionAcquisitionFree()
        layer = self.getIface().activeLayer()
        if layer and layer.isEditable() and  (layer.type() == core.QgsMapLayer.VectorLayer) and (layer.geometryType() in [core.QGis.Line, core.QGis.Polygon]):
            actionAcquisitionFree.setEnabled(True)
        else:
            actionAcquisitionFree.setEnabled(False)
    
    def getParametersFromConfig(self):
        #Método para obter as configurações da tool do QSettings
        #Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        parameters = {
            u'freeHandTolerance' : settings.value('freeHandTolerance'),
            u'freeHandSmoothIterations' : settings.value('freeHandSmoothIterations'),
            u'freeHandSmoothOffset' : settings.value('freeHandSmoothOffset'),
            u'algIterations' : settings.value('algIterations'),
            u'undoPoints' : settings.value('undoPoints')
        }
        settings.endGroup()
        return parameters

    def getTolerance(self, layer):
        #Método para obter tolerância para simplificação de geometria
        #Parâmetro de entrada: layer (camada em uso)
        #Parâmetro de retorno: sGeom (Geometria simplificada)
        parameters = self.getParametersFromConfig()
        if layer.crs().projectionAcronym() == "longlat":
            return 0.000
        return parameters[u'freeHandTolerance']

    def simplifyGeometry(self, geom, tolerance):
        #Método para simplificar geometria
        #Parâmetro de entrada: geom (Geometria adquirida), tolerance (Tolerância para simplificação)
        #Parâmetro de retorno: sGeom (Geometria simplificada)
        parameters = self.getParametersFromConfig()
        sGeom = geom
        for x in range(int(parameters[u'algIterations'])):
            sGeom = sGeom.simplify(float(tolerance))
            sGeom = sGeom.smooth(
                int(parameters[u'freeHandSmoothIterations']),
                float(parameters[u'freeHandSmoothOffset'])
            )
        return sGeom

    def reprojectGeometry(self, geom):
        # Defining the crs from src and destiny
        iface = self.getIface()
        canvas = iface.mapCanvas()
        epsg = canvas.mapSettings().destinationCrs().authid()
        crsSrc = core.QgsCoordinateReferenceSystem(epsg)
        #getting srid from something like 'EPSG:31983'
        layer = canvas.currentLayer()
        srid = layer.crs().authid()
        crsDest = core.QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        if srid != epsg:
            # Creating a transformer
            coordinateTransformer = core.QgsCoordinateTransform(crsSrc, crsDest)
            lyrType = iface.activeLayer().geometryType()
            # Transforming the points
            if lyrType == core.QGis.Line:
                geomList = geom.asPolyline()
            elif lyrType == core.QGis.Polygon:
                geomList = geom.asPolygon()
            newGeom = []
            for j in range(len(geomList)):
                if lyrType == core.QGis.Line:
                    newGeom.append(coordinateTransformer.transform(geomList[j]))
                elif lyrType == core.QGis.Polygon:
                    line = geomList[j]
                    for i in range(len(line)):
                        point = line[i]
                        newGeom.append(coordinateTransformer.transform(point))
            if lyrType == core.QGis.Line:
                return core.QgsGeometry.fromPolyline(newGeom)
            elif lyrType == core.QGis.Polygon:
                return core.QgsGeometry.fromPolygon([newGeom])
        return geom        

    def createFeature(self, geom):
        #Método para criar feição
        #Parâmetro de entrada: geom (geometria adquirida)
        if geom :
            settings = QtCore.QSettings()
            canvas = self.getIface().mapCanvas()
            layer = canvas.currentLayer() 
            tolerance = self.getTolerance(layer)
            geom = self.reprojectGeometry(geom)
            simplifyGeometry = self.simplifyGeometry(geom, tolerance)
            fields = layer.pendingFields()
            feature = core.QgsFeature()
            feature.setGeometry(simplifyGeometry)
            feature.initAttributes(fields.count())            
            provider = layer.dataProvider()              
            for i in range(fields.count()):
                feature.setAttribute(i, provider.defaultValue(i))
            formSuppressOnLayer = layer.featureFormSuppress()
            formSuppressOnSettings = self.getFormSuppressStateSettings()
            if formSuppressOnLayer or (formSuppressOnSettings == u"true"):
                self.addFeatureWithoutForm(layer, feature)
            else:
                self.addFeatureWithForm(layer, feature)
            
    def getFormSuppressStateSettings(self):
        #Método para verificar se o formulário de aquisição está suprimido nas configurações do projeto
        #Parâmetro de retorno: suppressForm ( boleano )
        s = QtCore.QSettings()
        suppressForm = s.value(u"Qgis/digitizing/disable_enter_attribute_values_dialog")
        return suppressForm

    def addFeatureWithForm(self, layer, feature):
        #Método para adicionar a feição com formulário
        #Parâmetro de entrada: layer (Camada ativa), feature (Feição adquirida)
        attrDialog = gui.QgsAttributeDialog(layer, feature, False)
        attrDialog.setMode(gui.QgsAttributeForm.AddFeatureMode)
        result = attrDialog.exec_()

    def addFeatureWithoutForm(self, layer, feature):
        #Método para adicionar a feição sem formulário
        #Parâmetro de entrada: layer (Camada ativa), feature (Feição adquirida)
        layer.addFeatures([feature])
        layer.removeSelection()

    def activateTool(self):
        #Método para iniciar a ferramenta 
        tool = self.getAcquisitionFree()
        tool.acquisitionFinished['QgsGeometry*'].connect(self.createFeature)
        canvas = self.getIface().mapCanvas()
        canvas.setMapTool(tool)
        actionAcquisitionFree = self.getActionAcquisitionFree()
        actionAcquisitionFree.setChecked(True)
        self.setActiveState(True)
                                        
    def deactivateTool(self):
        #Método para desativar a ferramenta
        actionAcquisitionFree = self.getActionAcquisitionFree()
        actionAcquisitionFree.setChecked(False)
        if self.getActiveState():
            tool = self.getAcquisitionFree()
            tool.acquisitionFinished['QgsGeometry*'].disconnect(self.createFeature)
        self.setActiveState(False)
      