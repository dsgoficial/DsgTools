# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-30
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from collections import defaultdict
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from qgis.PyQt.QtXml import QDomDocument
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterString,
    QgsProcessingOutputMultipleLayers,
    QgsProcessingParameterString,
)


class ApplyStylesFromDatabaseToLayersAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYERS = "INPUT_LAYERS"
    STYLE_NAME = "STYLE_NAME"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr("Input Layers"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(self.STYLE_NAME, self.tr("Style Name"))
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT, self.tr("Original layers with styles applied column")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.

        This process matches the layer name to the qml name.
        """
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        styleName = self.parameterAsString(parameters, self.STYLE_NAME, context)
        listSize = len(inputLyrList)
        progressStep = 100 / listSize if listSize else 0
        styleDict = self.getStyleDict(inputLyrList, feedback)

        for current, lyr in enumerate(inputLyrList):
            if feedback.isCanceled():
                break
            if lyr.providerType() != "postgres":
                continue
            uri = lyr.dataProvider().uri()
            dbName = uri.database()
            if dbName not in styleDict:
                continue
            if styleName not in styleDict[dbName]:
                continue
            schema = uri.schema()
            tableName = uri.table()
            geometryColumn = uri.geometryColumn()
            key = f"{schema}.{tableName}({geometryColumn})"
            if key not in styleDict[dbName][styleName]:
                continue
            self.applyStyle(lyr, styleDict[dbName][styleName][key])
            feedback.setProgress(current * progressStep)

        return {self.OUTPUT: [i.id() for i in inputLyrList]}

    def applyStyle(self, lyr, styleQml):
        styleDoc = QDomDocument("qgis")
        styleDoc.setContent(styleQml)
        lyr.importNamedStyle(styleDoc)
        lyr.triggerRepaint()
    
    def getAbstractDb(self, host, port, database, user, password):
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(host, port, database, user, password)
        return abstractDb
    
    def getDbDict(self, lyrList, feedback):
        dbDict = dict()
        for lyr in lyrList:
            if feedback.isCanceled():
                return dbDict
            if lyr.providerType() != "postgres":
                continue
            uri = lyr.dataProvider().uri()
            dbName = uri.database()
            if dbName in dbDict:
                continue
            host = uri.host()
            port = uri.port()
            user = uri.username()
            password = uri.password()
            dbDict[dbName] = self.getAbstractDb(host, port, dbName, user, password)
        return dbDict
    
    def getStyleDict(self, lyrList, feedback):
        dbDict = self.getDbDict(lyrList, feedback)
        dbStyleDict = dict()
        for dbName, abstractDb in dbDict.items():
            if feedback.isCanceled():
                break
            dbStyleDict[dbName] = abstractDb.getStyleDict()
        del dbDict
        return dbStyleDict

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "applystylesfromdatabasetolayersalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Apply Styles from Database to Layers")

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
        return QCoreApplication.translate(
            "ApplyStylesFromDatabaseToLayersAlgorithm", string
        )

    def createInstance(self):
        return ApplyStylesFromDatabaseToLayersAlgorithm()
