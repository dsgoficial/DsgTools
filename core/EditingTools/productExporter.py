# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-02-27
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
from builtins import object
from qgis.core import QgsLayoutExporter, QgsProject, QgsPrintLayout, QgsReadWriteContext
from qgis.PyQt.QtXml import QDomDocument

class ProductExporter(object):
    def __init__(self):
        self.layout = QgsPrintLayout(QgsProject.instance())
    
    def populateTemplate(self, templateXMLContent):
        templateDomDoc = QDomDocument()
        templateDomDoc.setContent(templateXMLContent)
        self.layout.loadFromTemplate(templateDomDoc, QgsReadWriteContext())
    
    def export(self, parameterDict):
        pass
    
    def exportPdf(self, outputPath, feedback=None):
        exporter = QgsLayoutExporter(self.layout)
        result, error = exporter.exportToPdfs(self.layout.atlas(),
                                              outputPath,
                                              settings=QgsLayoutExporter.PdfExportSettings(),
                                              feedback=feedback
                                            )
        return result, error

    def exportTiff(self):
        pass
    
    def generateProductionStepsHTML(self, parameterDict):
        """
        Para gerar a tabela de etapas de produção.
        Nos parâmetros deve vir a ordem de supressão caso seja necessário.
        """
        pass
    
    def exportPopulatedQPT(self, parameterDict):
        """
        easter egg
        """
        pass