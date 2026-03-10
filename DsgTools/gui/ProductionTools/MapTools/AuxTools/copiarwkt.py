# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-14
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsCoordinateTransformContext,
)
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QApplication
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt import uic
from qgis.utils import iface
import os


class GetCrsDialog(QDialog):
    def __init__(self):
        super(GetCrsDialog, self).__init__()
        uic.loadUi(self.getUiPath(), self)
        self.buttonBox.addButton("Sim", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Não mudar", QDialogButtonBox.RejectRole)

    def setCrsValue(self, value):
        self.selectCRS.setCrs(value)

    def getUiPath(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "changeCRS.ui")

    def getCrs(self):
        return self.selectCRS.crs()


def copywkt():
    layer = iface.activeLayer()
    if layer is None:
        iface.messageBar().pushMessage(
            "Warning",
            "Selecione uma camada antes de rodar o processo",
            level=Qgis.MessageLevel.Warning,
            duration=5,
        )

    result, destCrs = callDialog(layer.crs())
    wktcoord = []
    for feature in layer.getSelectedFeatures():
        geom = feature.geometry()
        if result:
            transformcrs = getGeometryTransforms(layer.crs(), destCrs)
            geom.transform(transformcrs)
        wktcoord.append(geom.asWkt())
    QApplication.clipboard().setText("\n".join(wktcoord))
    iface.messageBar().pushMessage(
        "Executado",
        " As coordenadas das feições selecionadas foram copiadas em WKT para o sistema {}".format(
            destCrs.authid()
        ),
        level=Qgis.MessageLevel.Success,
        duration=5,
    )


def callDialog(crsvalue):
    getCrsDialog = GetCrsDialog()
    getCrsDialog.setCrsValue(crsvalue)
    result = getCrsDialog.exec()
    crs = getCrsDialog.getCrs()
    if result and not crs.isValid():
        errorAction()
        return callDialog()
    return result, crs


def errorAction():
    reply = QMessageBox.question(
        iface.mainWindow(),
        "CRS Invalido",
        "Se deseja mudar o CRS, selecione um CRS valido",
        QMessageBox.StandardButton.Ok,
    )
    return False


def getGeometryTransforms(sourceCrs, destCrs):
    destTransform = QgsCoordinateTransform(
        sourceCrs, destCrs, QgsCoordinateTransformContext()
    )
    return destTransform
