# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jossan Costa - Surveying Technician @ Brazilian Army
                               (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.core import QgsProject, Qgis, QgsVectorLayer
from qgis.utils import iface
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QMessageBox
from .copiarwkt import copywkt


class OtherTools(QObject):
    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton
        icon_path = iconBasePath + "/tempLayer.png"
        toolTip = self.tr("DSGTools: Copy Features to Temporary Layer")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Copy Features to Temporary Layer"),
            callback=self.copyToTempLayer,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=False,
        )
        self.stackButton.setDefaultAction(action)

        icon_path = iconBasePath + "/copywkt.png"
        toolTip = self.tr("DSGTools: Copy Feature's Coordinates as WKT")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Copy Feature's Coordinates as WKT"),
            callback=copywkt,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=False,
        )

    def unload(self):
        pass

    def copyToTempLayer(self):
        confirmation = self.confirmAction()
        if not confirmation:
            iface.messageBar().pushMessage(
                "Cancelado",
                "ação cancelada pelo usuário",
                level=Qgis.Warning,
                duration=5,
            )
            return
        layer = iface.activeLayer()
        if not layer:
            iface.messageBar().pushMessage(
                "Erro", "Selecione uma camada válida", level=Qgis.Critical, duration=5
            )
            return
        features = layer.selectedFeatures()
        newFields = layer.fields()
        name = layer.name()
        geomtype = layer.geometryType()
        print(geomtype)
        print(type(geomtype))
        newName = name + "_temp"
        geomdict = {0: "multipoint", 1: "multilinestring", 2: "multipolygon"}
        selection = QgsVectorLayer(geomdict[int(geomtype)], newName, "memory")
        selection.startEditing()
        selection.setCrs(layer.crs())
        dp = selection.dataProvider()
        dp.addAttributes(newFields)
        dp.addFeatures(features)
        selection.commitChanges()
        selection.updateExtents()
        QgsProject.instance().addMapLayer(selection)
        iface.messageBar().pushMessage(
            "Executado",
            "Camada temporária criada: " + newName,
            level=Qgis.Success,
            duration=5,
        )

    def confirmAction(self):
        reply = QMessageBox.question(
            iface.mainWindow(),
            "Continuar?",
            "Será criado uma nova camada com as feições selecionadas. Deseja continuar?",
            QMessageBox.Yes,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes
