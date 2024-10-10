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
from typing import List, Set

from qgis.PyQt import QtGui, QtCore
from qgis.PyQt.QtWidgets import QMessageBox
from qgis import core, gui
from qgis.utils import iface
from qgis.core import (
    QgsPoint,
    QgsLineString,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsGeometry,
    QgsMessageLog,
    Qgis,
    QgsFeature,
    QgsPointXY,
)

from DsgTools.gui.ProductionTools.MapTools.FreeHandTool.models.acquisitionFree import (
    AcquisitionFree,
)


class AcquisitionFreeController(object):
    def __init__(self, acquisitionFree, iface):
        """
        Class constructor.
        :param acquisitionFree: (AcquisitionFree) AcquisitionFree object.
        :param iface: (QgisInterface) QGIS interface object to be set.
        """
        super(AcquisitionFreeController, self).__init__()
        self.acquisitionFree = acquisitionFree
        self.iface = iface
        self.active = False
        self.lastAddedFeatureId = None

    def setIface(self, iface):
        """
        Sets a QGIS interface object to iface attribute from AcquisitionFreeController object.
        :param iface: (QgisInterface) QGIS interface object to be set.
        """
        self.iface = iface

    def getIface(self):
        """
        Gets the QGIS interface object from AcquisitionFreeController object iface attribute.
        """
        return self.iface

    def setActionAcquisitionFree(self, actionAcquisitionFree):
        # Método para definir a classe ActionAcquisitionFree
        # Parâmetro de entrada: actionAcquisitionFree (classe ActionAcquisitionFree)
        self.actionAcquisitionFree = actionAcquisitionFree

    def getActionAcquisitionFree(self):
        # Método para obter a classe ActionAcquisitionFree
        # Parâmetro de retorno: self.actionAcquisitionFree (classe ActionAcquisitionFree)
        return self.actionAcquisitionFree

    @property
    def toolAction(self):
        return self.actionAcquisitionFree

    def setAcquisitionFree(self, acquisitionFree):
        # Método para definir a classe AcquisitionFree
        # Parâmetro de entrada: acquisitionFree (classe AcquisitionFree)
        self.acquisitionFree = acquisitionFree

    def getAcquisitionFree(self):
        # Método para obter a classe AcquisitionFree
        # Parâmetro de retorno: self.acquisitionFree (classe AcquisitionFree)
        return self.acquisitionFree

    def setActiveState(self, state):
        # Método para definir estado da ferramento (ativada ou desativada)
        # Parâmetro de entrada: state (boleano)
        self.active = state

    def getActiveState(self):
        # Método para obter estado da tool (ativada ou desativada)
        # Parâmetro de retorno: state (boleano)
        return self.active

    def checkToActiveAction(self):
        # Método para testar se a camada ativa é valida para ativar a ferramenta
        layer = self.getIface().activeLayer()
        if (
            core is not None
            and layer
            and layer.isEditable()
            and (layer.type() == core.QgsMapLayer.VectorLayer)
            and (
                layer.geometryType()
                in [core.QgsWkbTypes.LineGeometry, core.QgsWkbTypes.PolygonGeometry]
            )
        ):
            if not self.actionAcquisitionFree.isEnabled():
                self.actionAcquisitionFree.setEnabled(True)
            return True
        else:
            self.actionAcquisitionFree.setEnabled(False)
            self.uncheckTool(checkActivationtatus=False)
        return False

    def setToolEnabled(self):
        layer = self.iface.activeLayer()
        if (
            not isinstance(layer, QgsVectorLayer)
            or layer.geometryType() == QgsWkbTypes.PointGeometry
            or not layer.isEditable()
        ):
            enabled = False
        else:
            enabled = True
        self.uncheckTool(enabled)
        self.actionAcquisitionFree.setEnabled(enabled)
        return enabled

    def uncheckTool(self, enabled):
        if enabled or not self.acquisitionFree:
            return
        self.acquisitionFree.deactivate()
        self.iface.mapCanvas().unsetMapTool(self.acquisitionFree)
        self.actionAcquisitionFree.setChecked(False)
        try:
            self.iface.mapCanvas().mapToolSet.disconnect(self.activateFilterMapTool)
        except TypeError:
            pass

    def getParametersFromConfig(self):
        # Método para obter as configurações da tool do QSettings
        # Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        parameters = {
            "freeHandTolerance": settings.value("freeHandTolerance"),
            "freeHandFinalSimplifyTolerance": settings.value(
                "freeHandFinalSimplifyTolerance"
            ),
            "freeHandSmoothIterations": settings.value("freeHandSmoothIterations"),
            "freeHandSmoothOffset": settings.value("freeHandSmoothOffset"),
            "algIterations": settings.value("algIterations"),
            "undoPoints": settings.value("undoPoints"),
        }
        settings.endGroup()
        return parameters

    def getTolerance(self, layer):
        # Método para obter tolerância para simplificação de geometria
        # Parâmetro de entrada: layer (camada em uso)
        # Parâmetro de retorno: sGeom (Geometria simplificada)
        parameters = self.getParametersFromConfig()
        return parameters["freeHandTolerance"]

    def getFinalTolerance(self):
        parameters = self.getParametersFromConfig()
        finalTolerance = parameters["freeHandFinalSimplifyTolerance"]
        return 0 if finalTolerance is None else float(finalTolerance)

    def simplifyGeometry(self, geom, tolerance):
        # Método para simplificar geometria
        # Parâmetro de entrada: geom (Geometria adquirida), tolerance (Tolerância para simplificação)
        # Parâmetro de retorno: sGeom (Geometria simplificada)
        parameters = self.getParametersFromConfig()
        firstVertex = geom.vertexAt(0)
        lastVertex = geom.vertexAt(geom.constGet().nCoordinates() - 1)
        sGeom = geom
        source_crs = self.iface.activeLayer().crs()
        dest_crs = core.QgsCoordinateReferenceSystem(3857)
        tr = core.QgsCoordinateTransform(
            source_crs, dest_crs, core.QgsCoordinateTransformContext()
        )
        sGeom.transform(tr)
        for x in range(int(parameters["algIterations"])):
            sGeom = sGeom.simplify(float(tolerance))
            try:
                sGeom = sGeom.smooth(
                    int(parameters["freeHandSmoothIterations"]),
                    float(parameters["freeHandSmoothOffset"]),
                )
            except:
                msg = QMessageBox().tr(
                    "Probably too many smoothing iteration, try reducing it (3 usually is enough). Geometry was not smoothened."
                )
                QMessageBox.warning(
                    self.iface.mainWindow(), QMessageBox().tr("Error!"), msg
                )
                QgsMessageLog.logMessage(msg, "DSGTools Plugin", Qgis.Critical)
                return geom
        finalGeom = sGeom.simplify(self.getFinalTolerance())
        tr = core.QgsCoordinateTransform(
            dest_crs, source_crs, core.QgsCoordinateTransformContext()
        )
        finalGeom.transform(tr)
        if self.iface.activeLayer().geometryType() == core.QgsWkbTypes.PolygonGeometry:
            return finalGeom
        finalGeom.moveVertex(firstVertex.x(), firstVertex.y(), 0)
        finalGeom.moveVertex(
            lastVertex.x(), lastVertex.y(), finalGeom.constGet().nCoordinates() - 1
        )
        return finalGeom

    def reprojectGeometry(self, geom):
        # Defining the crs from src and destiny
        canvas = iface.mapCanvas()
        layer = iface.activeLayer()
        epsgSrc = canvas.mapSettings().destinationCrs().authid()
        epsgDest = layer.crs().authid()
        if epsgSrc != epsgDest:
            ct = canvas.mapSettings().layerTransform(layer)
            geom.transform(ct, core.QgsCoordinateTransform.ReverseTransform)
        return geom

    def createFeature(self, geom, closeLine):
        # Método para criar feição
        # Parâmetro de entrada: geom (geometria adquirida)
        if not geom:
            return
        settings = QtCore.QSettings()
        canvas = self.getIface().mapCanvas()
        layer = canvas.currentLayer()
        tolerance = self.getTolerance(layer)
        geom = self.reprojectGeometry(geom)
        simplifyGeometry = self.simplifyGeometry(geom, tolerance)
        fields = layer.fields()
        feature = core.QgsFeature()
        feature.setFields(fields)
        feature.setGeometry(simplifyGeometry)
        provider = layer.dataProvider()
        for i in range(fields.count()):
            defaultClauseCandidate = provider.defaultValueClause(i)
            if defaultClauseCandidate:
                feature.setAttribute(i, defaultClauseCandidate)
        formSuppressOnLayer = layer.editFormConfig().suppress()
        formSuppressOnSettings = self.getFormSuppressStateSettings()
        featureAdded = True
        if formSuppressOnLayer == core.QgsEditFormConfig.SuppressOn or (
            formSuppressOnLayer == core.QgsEditFormConfig.SuppressDefault
            and formSuppressOnSettings == "true"
        ):
            self.addFeatureWithoutForm(layer, feature, closeLine)
        else:
            featureAdded = self.addFeatureWithForm(layer, feature, closeLine)
        if featureAdded and core.QgsProject.instance().topologicalEditing():
            self.createTopology(feature)

    def createTopology(self, feature):
        currentLayer = iface.activeLayer()
        otherLayers = [
            layer
            for layer in iface.mapCanvas().layers()
            if (
                layer.id() != currentLayer.id()
                and layer.isEditable()
                and layer.type() == core.QgsMapLayer.VectorLayer
            )
        ]
        createdGeometry = feature.geometry()
        for layer in otherLayers:
            layer.addTopologicalPoints(createdGeometry)
        currentLayer.addTopologicalPoints(createdGeometry)
        iface.mapCanvas().refresh()

    def reshapeSimplify(self, reshapeLine):
        canvas = self.getIface().mapCanvas()
        layer = canvas.currentLayer()
        tolerance = self.getTolerance(layer)
        reshapeLine_ = self.reprojectGeometry(reshapeLine)
        rsLine = self.simplifyGeometry(reshapeLine_, tolerance)
        request = core.QgsFeatureRequest().setFilterRect(rsLine.boundingBox())
        for feat in (
            layer.getSelectedFeatures(request)
            if layer.selectedFeatureCount() > 0
            else layer.getFeatures(request)
        ):
            geom = feat.geometry()  # geometria que receberá o reshape.
            if geom.intersects(
                rsLine
            ):  # Se intersecta e transforma frompolyline em geometria.
                geom.reshapeGeometry(
                    QgsLineString([QgsPoint(p) for p in rsLine.asPolyline()])
                )  # realiza o reshape entre a linha e a geometria.
                layer.changeGeometry(feat.id(), geom)

        canvas.refresh()  # Refresh para atualizar, mas não salvar as alterações.

    def getFormSuppressStateSettings(self):
        # Método para verificar se o formulário de aquisição está suprimido nas configurações do projeto
        # Parâmetro de retorno: suppressForm ( boleano )
        s = QtCore.QSettings()
        suppressForm = s.value("qgis/digitizing/disable_enter_attribute_values_dialog")
        return suppressForm == "true"

    def loadDefaultFields(self, layer, feature):
        attributesValues = {}
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for fieldIndex in layer.attributeList():
            fieldName = layer.fields().field(fieldIndex).name()
            if fieldIndex in primaryKeyIndexes:
                continue
            attributeExpression = layer.defaultValueDefinition(fieldIndex).expression()
            if attributeExpression == "":
                continue
            evaluatedExpression = self.evaluateExpression(
                layer, layer.defaultValueDefinition(fieldIndex).expression()
            )
            if evaluatedExpression is None:
                feature[fieldName] = attributeExpression
                continue
            feature[fieldName] = evaluatedExpression

    def evaluateExpression(self, layer, expression):
        context = core.QgsExpressionContext()
        context.appendScopes(
            core.QgsExpressionContextUtils.globalProjectLayerScopes(layer)
        )
        return core.QgsExpression(expression).evaluate(context)

    def addFeatureWithForm(self, layer: QgsVectorLayer, feature, closeLine=False):
        # Método para adicionar a feição com formulário
        # Parâmetro de entrada: layer (Camada ativa), feature (Feição adquirida)
        layer.beginEditCommand("dsgtools freehand feature added")
        self.loadDefaultFields(layer, feature)
        if closeLine:
            layer.featureAdded.connect(self.featureAdded)
        attrDialog = gui.QgsAttributeDialog(layer, feature, False)
        attrDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        attrDialog.setMode(int(gui.QgsAttributeForm.AddFeatureMode))
        res = attrDialog.exec_()
        if res == 0:
            layer.destroyEditCommand()
            return res
        if closeLine:
            layer.featureAdded.disconnect(self.featureAdded)
            self.closeLine(layer, feature, self.lastAddedFeatureId)
        layer.endEditCommand()
        return res

    def featureAdded(self, featureId):
        self.lastAddedFeatureId = featureId

    def addFeatureWithoutForm(self, layer, feature, closeLine=False):
        # Método para adicionar a feição sem formulário
        # Parâmetro de entrada: layer (Camada ativa), feature (Feição adquirida)
        layer.beginEditCommand("dsgtools freehand feature added")
        self.loadDefaultFields(layer, feature)
        featuresToAdd = {feature}
        if closeLine:
            newFeats = self.closeLine(layer, feature)
            featuresToAdd = newFeats if newFeats is not None else featuresToAdd
        layer.addFeatures(featuresToAdd)
        layer.removeSelection()
        layer.endEditCommand()

    def activateFilterMapTool(self, mapTool):
        state = isinstance(mapTool, AcquisitionFree)
        changedAcquisitionFree = state
        if state:
            changedAcquisitionFree = (
                mapTool.controlPressed == self.acquisitionFree.controlPressed
            )
        enabled = state and changedAcquisitionFree
        self.uncheckTool(enabled=enabled)

    def activateTool(self):
        # Método para iniciar a ferramenta
        state = self.actionAcquisitionFree.isChecked()
        self.setActiveState(state)
        if state:
            self.iface.mapCanvas().setMapTool(self.acquisitionFree)
            self.iface.mapCanvas().mapToolSet.connect(self.activateFilterMapTool)
        else:
            self.iface.mapCanvas().unsetMapTool(self.acquisitionFree)
            try:
                self.iface.mapCanvas().mapToolSet.disconnect(self.activateFilterMapTool)
            except TypeError:
                pass
        self.setToolEnabled()

    def closeLine(self, layer: QgsVectorLayer, feature: QgsFeature, fid=None):
        if not layer:
            iface.messageBar().pushMessage(
                "Erro", "Selecione uma camada válida", level=Qgis.Warning, duration=5
            )
            return None
        # if fid is None:
        #     iface.messageBar().pushMessage(
        #         "Erro", "Erro ao fechar linha (id invalido)", level=Qgis.Critical, duration=5
        #     )
        #     return
        geom = feature.geometry()
        new_geom = self.snapLastPointToFirstPoint(geom)
        geometries = self.splitLineGeometry(new_geom)
        if len(geometries) == 0:
            iface.messageBar().pushMessage(
                "Erro", "Linha não fechada", level=Qgis.Warning, duration=5
            )
            return None
        geomsToAdd = geometries
        if fid is not None:
            updateGeom = geometries[0]
            layer.changeGeometry(fid, updateGeom)
            geomsToAdd = geometries[1:]
        featuresToAdd = self.getFeaturesBasedOnAnother(layer, feature, geomsToAdd)
        if fid is not None:
            layer.addFeatures(featuresToAdd)
        iface.messageBar().pushMessage(
            "Executado",
            f"Linha fechada",
            level=Qgis.Success,
            duration=3,
        )
        features = {feature}
        features = features.union(featuresToAdd)
        return features

    def snapLastPointToFirstPoint(self, geometry: QgsGeometry) -> QgsGeometry:

        if not geometry.wkbType() in (
            QgsWkbTypes.LineString,
            QgsWkbTypes.MultiLineString,
        ):
            return geometry
        if geometry.isMultipart():
            new_parts = []
            for part in geometry.asMultiPolyline():
                if len(part) > 1:
                    new_part = part
                    new_part.append(part[0])
                    new_parts.append(new_part)
                else:
                    new_parts.append(part)
            new_geometry = QgsGeometry.fromMultiPolylineXY(new_parts)
            return new_geometry
        line = geometry.asPolyline()
        if len(line) < 2:
            return geometry
        new_line = line + [line[0]]
        if isinstance(line[0], QgsPointXY):
            new_geometry = QgsGeometry.fromPolylineXY(new_line)
            return new_geometry
        return QgsGeometry.fromPolyline(new_line)

    def getFeaturesBasedOnAnother(self, layer, feature, geometries):
        featsToAdd = set()
        attrs = feature.attributes()
        primary_key_indices = layer.primaryKeyAttributes()
        for pk_index in primary_key_indices:
            attrs[pk_index] = None
        fields = feature.fields()
        for newGeom in geometries:
            new_feature = QgsFeature(fields)
            new_feature.setGeometry(newGeom)
            new_feature.setAttributes(attrs)
            featsToAdd.add(new_feature)
        return featsToAdd

    def splitLineGeometry(self, geometry) -> List[QgsGeometry]:
        geometries = []
        if geometry.isNull() or geometry.isEmpty():
            return [geometry]
        if not geometry.wkbType() in (
            QgsWkbTypes.LineString,
            QgsWkbTypes.MultiLineString,
        ):
            return [geometry]
        allPartsHaveLessThan3Vertices = True
        isMulti = geometry.isMultipart()
        multiline = geometry.asMultiPolyline() if isMulti else [geometry.asPolyline()]
        transformGeom = (
            lambda x: QgsGeometry.fromPolylineXY(x)
            if isinstance(x[0], QgsPointXY)
            else QgsGeometry.fromPolyline(x)
        )
        for line in multiline:
            num_vertices = len(line)
            if num_vertices < 3:
                geometryToAdd = transformGeom(line)
                geometries.append(geometryToAdd)
                continue  # Ignora geometria com menos de 4 vértices
            allPartsHaveLessThan3Vertices = False
            mid_index = num_vertices // 2
            first_half = line[: mid_index + 1]
            second_half = line[mid_index:]
            first_half_geometry = transformGeom(first_half)
            second_half_geometry = transformGeom(second_half)
            if isMulti:
                first_half_geometry.convertToMultiType()
                second_half_geometry.convertToMultiType()
            geometries.extend([first_half_geometry, second_half_geometry])
        return geometries if not allPartsHaveLessThan3Vertices else [geometry]
