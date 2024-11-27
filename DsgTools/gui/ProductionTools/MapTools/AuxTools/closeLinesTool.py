# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                :  pedromartins.souza@eb.mil.br
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
from typing import Set
from qgis.core import (
    Qgis,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
)
from qgis.gui import QgsMapTool
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QMessageBox


class CloseLinesTool(QgsMapTool):
    def __init__(self, iface):
        self.iface = iface
        self.toolAction = None
        self.canvas = self.iface.mapCanvas()
        super(CloseLinesTool, self).__init__(self.canvas)

    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + "/closedLines.png"
        toolTip = self.tr("DSGTools: Close Selected Lines")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Close Selected Lines"),
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentToolbar=parentMenu,
        )
        self.setAction(action)

    def activate(self):
        """
        Activates tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(False)

    def setAction(self, action):
        """
        Defines an action for tool.
        action: QAction to be set.
        """
        self.toolAction = action

    def setToolEnabled(self, layer=None):
        """
        Checks if it is possible to use tool given layer editing conditions and type.
        :param layer: (QgsVectorLayer) layer that may have its lines closed.
        :return: (bool) whether tool may be used.
        """
        if not isinstance(layer, QgsVectorLayer):
            layer = self.iface.mapCanvas().currentLayer()
        if (
            not layer
            or not isinstance(layer, QgsVectorLayer)
            or layer.geometryType() != QgsWkbTypes.LineGeometry
            or not layer.isEditable()
        ):
            enabled = False
        else:
            enabled = True
        self.toolAction.setEnabled(enabled) if self.toolAction else None
        return enabled

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.canvas.unsetMapTool(self)

    def unload(self):
        self.deactivate()
        try:
            self.iface.unregisterMainWindowAction(self.toolAction)
        except:
            pass

    def closeSelectedLines(self):
        layer = iface.activeLayer()
        if not layer:
            iface.messageBar().pushMessage(
                "Erro", "Selecione uma camada válida", level=Qgis.Critical, duration=5
            )
            return
        selectedFeatures = layer.selectedFeatureCount()
        if selectedFeatures == 0:
            iface.messageBar().pushMessage(
                "Erro", "Nenhuma feição selecionada", level=Qgis.Critical, duration=5
            )
            return
        confirmation = self.confirmAction(selectedFeatures)
        if not confirmation:
            iface.messageBar().pushMessage(
                "Cancelado",
                "Ação cancelada pelo usuário",
                level=Qgis.Warning,
                duration=5,
            )
            return
        featuresToAdd = set()
        featuresIdsToDelete = set()
        for feature in layer.getSelectedFeatures():
            geom = feature.geometry()
            new_geom = self.snapLastPointToFirstPoint(geom)
            feature.setGeometry(new_geom)
            features = self.splitLine(layer, feature)
            if features is None:
                continue
            featuresIdsToDelete.add(feature.id())
            featuresToAdd = featuresToAdd.union(features)
        if featuresIdsToDelete:
            layer.startEditing()
            layer.beginEditCommand(f"Fechando linhas {layer.name()}")
            layer.deleteFeatures(list(featuresIdsToDelete))
            layer.addFeatures(list(featuresToAdd))
            layer.endEditCommand()
        iface.messageBar().pushMessage(
            "Executado",
            f"{len(featuresIdsToDelete)} linha(s) fechada(s)",
            level=Qgis.Success,
            duration=5,
        )

    def confirmAction(self, selectedFeatures):
        reply = QMessageBox.question(
            iface.mainWindow(),
            "Continuar?",
            f"As linhas selecionadas com vértices iniciais e finais próximos serão fechadas ({selectedFeatures} feição(ões) selecionada(s)). Deseja continuar?",
            QMessageBox.Yes,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    # Não está sendo usado, usar caso queira verificar proximidade para fechar linhas
    def isFirstPointCloseToLastPoint(self, geometry: QgsGeometry, tolerance):
        # Método para verificar se o primeiro ponto é proximo do último ponto da linha
        # Parâmetro de entrada: geometry ( QgsGeometry ), tolerance ( float )

        if not geometry.wkbType() in (
            QgsWkbTypes.LineString,
            QgsWkbTypes.MultiLineString,
        ):
            return False
        if geometry.isNull() or geometry.isEmpty():
            return False
        if geometry.isMultipart():
            for part in geometry.asMultiPolyline():
                if part[0].distance(part[-1]) > tolerance:
                    return False
                else:
                    return True
        else:
            # Para linhas simples
            line = geometry.asPolyline()
            if line[0].distance(line[-1]) > tolerance:
                return False
            else:
                return True

    def snapLastPointToFirstPoint(self, geometry: QgsGeometry):
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
        else:
            # Para linhas simples
            line = geometry.asPolyline()
            if len(line) > 1:
                new_line = line + [line[0]]
                if isinstance(line[0], QgsPointXY):
                    new_geometry = QgsGeometry.fromPolylineXY(new_line)
                else:
                    new_geometry = QgsGeometry.fromPolyline(new_line)
            else:
                new_geometry = geometry
        return new_geometry

    def splitLine(self, layer, feature) -> Set[QgsFeature]:
        geometry = feature.geometry()
        if not geometry.wkbType() in (
            QgsWkbTypes.LineString,
            QgsWkbTypes.MultiLineString,
        ):
            return feature, None
        if geometry.isMultipart():
            allPartsHaveLessThan3Vertices = True
            newFeatures = set()
            multiline = geometry.asMultiPolyline()
            for line in multiline:
                num_vertices = len(line)
                if num_vertices <= 3:
                    newFeatures.add(feature)
                    continue  # Ignora geometria com menos de 4 vértices
                allPartsHaveLessThan3Vertices = False
                mid_index = num_vertices // 2
                first_half = line[: mid_index + 1]
                second_half = line[mid_index:]

                if isinstance(line[0], QgsPointXY):
                    first_half_geometry = QgsGeometry.fromPolylineXY(first_half)
                    second_half_geometry = QgsGeometry.fromPolylineXY(second_half)
                else:
                    first_half_geometry = QgsGeometry.fromPolyline(first_half)
                    second_half_geometry = QgsGeometry.fromPolyline(second_half)
                attrs = feature.attributes()
                primary_key_indices = layer.primaryKeyAttributes()
                for pk_index in primary_key_indices:
                    attrs[pk_index] = None
                new_feature1 = QgsFeature(feature.fields())
                new_feature1.setGeometry(first_half_geometry)
                new_feature1.setAttributes(attrs)

                new_feature2 = QgsFeature(feature.fields())
                new_feature2.setGeometry(second_half_geometry)
                new_feature2.setAttributes(attrs)
                newFeatures.add(new_feature1)
                newFeatures.add(new_feature2)
            return newFeatures if not allPartsHaveLessThan3Vertices else None
        line = geometry.asPolyline()
        num_vertices = len(line)
        if not num_vertices > 3:
            return None
        mid_index = num_vertices // 2
        first_half = line[: mid_index + 1]
        second_half = line[mid_index:]
        if isinstance(line[0], QgsPointXY):
            first_half_geometry = QgsGeometry.fromPolylineXY(first_half)
            second_half_geometry = QgsGeometry.fromPolylineXY(second_half)
        else:
            first_half_geometry = QgsGeometry.fromPolyline(first_half)
            second_half_geometry = QgsGeometry.fromPolyline(second_half)

        attrs = feature.attributes()
        primary_key_indices = layer.primaryKeyAttributes()
        for pk_index in primary_key_indices:
            attrs[pk_index] = None
        new_feature1 = QgsFeature(feature.fields())
        new_feature1.setGeometry(first_half_geometry)
        new_feature1.setAttributes(attrs)

        new_feature2 = QgsFeature(feature.fields())
        new_feature2.setGeometry(second_half_geometry)
        new_feature2.setAttributes(attrs)
        return new_feature1, new_feature2
