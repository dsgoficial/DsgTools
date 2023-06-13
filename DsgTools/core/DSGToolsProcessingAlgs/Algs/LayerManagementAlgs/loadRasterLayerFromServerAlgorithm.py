# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-13
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
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

import psycopg2
import psycopg2.extras
from processing.gui.wrappers import WidgetWrapper
from qgis.core import (
    QgsDataSourceUri,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProject,
    QgsRasterLayer,
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QLineEdit
from qgis.utils import iface


class LoadRasterLayerFromServerAlgorithm(QgsProcessingAlgorithm):
    SERVER_IP = "SERVER_IP"
    PORT = "PORT"
    DB_NAME = "DB_NAME"
    TABLE_NAME = "TABLE_NAME"
    USER = "USER"
    PASSWORD = "PASSWORD"
    OUTPUT = "OUTPUT"
    LOAD_TO_CANVAS = "LOAD_TO_CANVAS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """

        self.addParameter(
            QgsProcessingParameterString(self.SERVER_IP, self.tr("Server Address"))
        )

        self.addParameter(QgsProcessingParameterNumber(self.PORT, self.tr("Port")))

        self.addParameter(
            QgsProcessingParameterString(
                self.DB_NAME,
                self.tr("Database name"),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.TABLE_NAME,
                self.tr("Table name"),
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.USER,
                self.tr("User"),
            )
        )

        password = QgsProcessingParameterString(
            self.PASSWORD,
            self.tr("Password"),
        )
        password.setMetadata({"widget_wrapper": {"class": PasswordWrapper}})
        self.addParameter(password)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_TO_CANVAS, self.tr("Load layers to canvas"), defaultValue=True
            )
        )

    @staticmethod
    def connectToServerDict(server_ip, port, db_name, user, password, table_name):
        conn = psycopg2.connect(
            host=server_ip, dbname=db_name, port=port, user=user, password=password
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "select r_raster_column, r_table_schema , r_table_name  from public.raster_columns where r_table_name = %s",
            (table_name,),
        )
        output = cur.fetchone()
        conn.close()
        return output

    def returnLayer(
        self,
        server_ip,
        port,
        db_name,
        user,
        password,
        table_name,
        feedback=None,
    ):
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
            multiStepFeedback.setCurrentStep(0)
        else:
            multiStepFeedback = None
        uriRaster = QgsDataSourceUri()
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Connecting..."))
            multiStepFeedback.setCurrentStep(1)
        uriRaster.setConnection(
            server_ip,
            str(port),
            db_name,
            user,
            password,
            sslmode=QgsDataSourceUri.SslDisable,
        )
        serverDict = self.connectToServerDict(
            server_ip, port, db_name, user, password, table_name
        )
        uriRaster.setDataSource(
            serverDict["r_table_schema"],
            serverDict["r_table_name"],
            serverDict["r_raster_column"],
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
        raster = QgsRasterLayer(
            uriRaster.uri(), table_name, providerType="postgresraster"
        )
        return raster

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        server_ip = self.parameterAsString(parameters, self.SERVER_IP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        db_name = self.parameterAsString(parameters, self.DB_NAME, context)
        table_name = self.parameterAsString(parameters, self.TABLE_NAME, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)
        loadToCanvas = self.parameterAsBool(parameters, self.LOAD_TO_CANVAS, context)
        if loadToCanvas:
            iface.mapCanvas().freeze(True)
        raster = self.returnLayer(
            server_ip,
            port,
            db_name,
            user,
            password,
            table_name,
            feedback=feedback,
        )
        QgsProject.instance().addMapLayer(raster, addToLegend=loadToCanvas)
        if loadToCanvas:
            iface.mapCanvas().freeze(False)
        return {self.OUTPUT: raster.id()}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "loadrasterlayerfromserveralgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Load Raster Layer from Server")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Layer Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Layer Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("loadRasterLayerFromServerAlgorithm", string)

    def createInstance(self):
        return LoadRasterLayerFromServerAlgorithm()


class PasswordWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = args[0]

    def createWidget(self):
        self._lineEdit = QLineEdit()
        self._lineEdit.setEchoMode(QLineEdit.Password)
        return self._lineEdit

    def value(self):
        return self._lineEdit.text()
