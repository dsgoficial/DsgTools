# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QFile, QIODevice

def generateQml(filename, attrs, codelists):
    xmlWriter = QXmlStreamWriter()
    xmlFile = QFile(filename)

    if (xmlFile.open(QIODevice.WriteOnly) == False):
        QMessageBox.warning(0, "Error!", "Error opening file")
    else :
        xmlWriter.setDevice(xmlFile)
        #starting xml file
        xmlWriter.writeStartDocument()

        #starting QGIS element
        xmlWriter.writeStartElement("qgis")
        xmlWriter.writeAttribute("version","2.6.0-Brighton")
        xmlWriter.writeAttribute("minimumScale","1")
        xmlWriter.writeAttribute("maximumScale","1")
        xmlWriter.writeAttribute("simplifyDrawingHints","0")
        xmlWriter.writeAttribute("minLabelScale","0")
        xmlWriter.writeAttribute("maxLabelScale","1e+08")
        xmlWriter.writeAttribute("simplifyDrawingTol","1")
        xmlWriter.writeAttribute("simplifyMaxScale","1")
        xmlWriter.writeAttribute("hasScaleBasedVisibilityFlag","0")
        xmlWriter.writeAttribute("simplifyLocal","1")
        xmlWriter.writeAttribute("scaleBasedLabelVisibilityFlag","0")

        #starting edittypes element
        xmlWriter.writeStartElement("edittypes")

        #satrting edittype elements
        for attr in attrs:
            #starting edittype
            xmlWriter.writeStartElement("edittype")
            xmlWriter.writeAttribute("widgetv2type","TextEdit")
            xmlWriter.writeAttribute("name",attr)

            #starting widgetv2config
            xmlWriter.writeStartElement("widgetv2config")
            xmlWriter.writeAttribute("IsMultiline","0")
            xmlWriter.writeAttribute("fieldEditable","0")
            xmlWriter.writeAttribute("UseHtml","0")
            xmlWriter.writeAttribute("labelOnTop","0")
            #closing widgetv2config
            xmlWriter.writeEndElement()

            #closing edittype
            xmlWriter.writeEndElement()

        for key in list(codelists.keys()):
            #starting edittype
            xmlWriter.writeStartElement("edittype")
            xmlWriter.writeAttribute("widgetv2type","ValueMap")
            xmlWriter.writeAttribute("name",key)

            #starting widgetv2config
            xmlWriter.writeStartElement("widgetv2config")
            xmlWriter.writeAttribute("fieldEditable","1")
            xmlWriter.writeAttribute("labelOnTop","0")

            #Writing pair key-value
            codelist = codelists[key]
            for codeValue in list(codelist.keys()):
                code = codelist[codeValue]

                #starting value
                xmlWriter.writeStartElement("value")
                xmlWriter.writeAttribute("key",codeValue)
                xmlWriter.writeAttribute("value",code)
                #closing value
                xmlWriter.writeEndElement()

            #closing widgetv2config
            xmlWriter.writeEndElement()

            #closing edittype
            xmlWriter.writeEndElement()

        #closing edittypes
        xmlWriter.writeEndElement()

        #closing QGIS
        xmlWriter.writeEndElement()

        #closing xml file
        xmlWriter.writeEndDocument()

if __name__ == '__main__':
    attrs = list()
    attrs.append("a")
    attrs.append("b")
    attrs.append("c")

    codelists = dict()

    codelist = dict()
    codelist["SIM"] = "1"
    codelist["NÃO"] = "2"

    codelists["d"] = codelist

    generateQml("teste.qml", attrs, codelists)
    
    qml = open("teste.qml", "r")
    fileData = qml.read()
    qml.close()    
    newData = fileData.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>")
    qml = open("teste.qml", "w")
    qml.write(newData)
    qml.close()

