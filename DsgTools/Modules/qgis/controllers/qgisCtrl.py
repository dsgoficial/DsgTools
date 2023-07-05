from qgis import core, gui
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import json
from DsgTools.Modules.qgis.factories.actionsFactory import ActionsFactory
from qgis.core import QgsWkbTypes

class QgisCtrl:
    def __init__(self, actionsFactory=None):
        self.actionsFactory = actionsFactory if actionsFactory is not None else ActionsFactory()

    def getLoadedVectorLayerNames(self):
        layerNames = []
        for l in core.QgsProject.instance().mapLayers().values():
            if not (l.type() == core.QgsMapLayer.VectorLayer):
                continue
            layerName = None
            if l.providerType() == "postgres":
                layerName = l.dataProvider().uri().table()
            elif l.providerType() == "ogr":
                layerName = (
                    l.dataProvider().uri().uri().split("|")[-1].split("=")[-1][1:-1]
                )
                if layerName == '':
                    layerName = l.name()
            else:
                layerName = l.name()
            if not layerName:
                continue
            layerNames.append(layerName)
        return layerNames

    def getVectorLayerNames(self, layers):
        layerNames = []
        for l in layers:
            if not (l.type() == core.QgsMapLayer.VectorLayer):
                continue
            layerName = None
            if l.providerType() == "postgres":
                layerName = l.dataProvider().uri().table()
            elif l.providerType() == "ogr":
                layerName = (
                    l.dataProvider().uri().uri().split("|")[-1].split("=")[-1][1:-1]
                )
                if layerName == '':
                    layerName = l.name()
            else:
                layerName = l.name()
            if not layerName:
                continue
            layerNames.append(layerName)
        return layerNames

    def getLoadedVectorLayers(self):
        return [
            l
            for l in core.QgsProject.instance().mapLayers().values()
            if l.type() == core.QgsMapLayer.VectorLayer
        ]

    def getVectorLayersByName(self, name):
        layers = []
        for l in core.QgsProject.instance().mapLayers().values():
            if not (l.type() == core.QgsMapLayer.VectorLayer):
                continue
            layerName = None
            if l.providerType() == "postgres":
                layerName = l.dataProvider().uri().table()
            elif l.providerType() == "ogr":
                layerName = (
                    l.dataProvider().uri().uri().split("|")[-1].split("=")[-1][1:-1]
                )
                if layerName == '':
                    layerName = l.name()
            else:
                layerName = l.name()
            if not layerName or layerName != name:
                continue
            layers.append(l)
        return layers

    def getVectorLayerByName(self, name):
        layers = self.getVectorLayersByName(name)
        if not layers:
            return None
        return layers[0]

    def getAttributesConfigByLayerName(
        self, layerName, withPrimaryKey=False, withVirtualField=False
    ):
        layer = self.getVectorLayerByName(layerName)
        if not layer:
            return {}
        return self.getAttributesConfigByLayer(layer, withPrimaryKey, withVirtualField)

    def getAttributesConfigByLayer(self, layer, withPrimaryKey, withVirtualField):
        attrConfig = {}
        for fieldIndex in layer.attributeList():
            if not (withPrimaryKey) and (
                fieldIndex in self.getLayerPrimaryKeyIndexes(layer)
            ):
                continue
            if not (withVirtualField) and (
                self.getFieldTypeName(layer, fieldIndex) == ""
            ):
                continue
            fieldName = layer.fields().field(fieldIndex).name()
            fieldConfig = layer.fields().field(fieldIndex).editorWidgetSetup().config()
            attrConfig[fieldName] = fieldConfig
        return attrConfig

    def getLayerPrimaryKeyIndexes(self, layer):
        return layer.dataProvider().pkAttributeIndexes()

    def getFieldTypeName(self, layer, fieldIndex):
        return layer.fields().field(fieldIndex).typeName()

    def getAcquisitionToolNames(self):
        return {
            "Padrão": None,
            "Ângulo Reto": "RightDegreeAngleDigitizing",
            "Mão Livre": "FreeHand",
        }

    def addDockWidget(self, dockWidget, side=QtCore.Qt.LeftDockWidgetArea):
        iface.addDockWidget(side, dockWidget)

    def removeDockWidget(self, dockWidget):
        iface.removeDockWidget(dockWidget)

    def registerShortcut(self, shortcut):
        gui.QgsGui.shortcutsManager().registerShortcut(shortcut)

    def unregisterShortcut(self, shortcut):
        gui.QgsGui.shortcutsManager().unregisterShortcut(shortcut)

    def setDefaultFields(self, layer, attributes, reset=False):
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for attributeName in attributes:
            fieldIndex = layer.fields().indexFromName(attributeName)
            if fieldIndex in primaryKeyIndexes:
                continue
            attributeValue = attributes[attributeName]
            configField = layer.defaultValueDefinition(fieldIndex)
            isMapValue = "map" in layer.editorWidgetSetup(fieldIndex).config()
            if isMapValue:
                valueMap = self.formatMapValues(
                    layer.editorWidgetSetup(fieldIndex).config()["map"]
                )
                if not (attributeValue is None) and attributeValue in valueMap:
                    configField.setExpression("{0}".format(valueMap[attributeValue]))
                elif reset:
                    configField.setExpression("")
            else:
                if attributeValue != "":
                    configField.setExpression("'{0}'".format(attributeValue))
                elif reset:
                    configField.setExpression("")
            layer.setDefaultValueDefinition(fieldIndex, configField)

    def formatMapValues(self, mapValues):
        if not (type(mapValues) is list):
            return mapValues
        newMapValues = {}
        for field in mapValues:
            newMapValues.update(field)
        return newMapValues

    def getDefaultFields(self, layer):
        attributesValues = {}
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for fieldIndex in layer.attributeList():
            fieldName = layer.fields().field(fieldIndex).name()
            if fieldIndex in primaryKeyIndexes:
                continue
            configField = layer.defaultValueDefinition(fieldIndex)
            attributesValues[fieldName] = configField.expression()
        return attributesValues

    def setActiveLayer(self, layer):
        iface.setActiveLayer(layer)
        layer.startEditing()
        iface.actionAddFeature().trigger()

    def setLayerVariable(self, layer, key, value):
        core.QgsExpressionContextUtils.setLayerVariable(layer, key, value)

    def getLayerVariable(self, layer, key):
        return core.QgsExpressionContextUtils.layerScope(layer).variable(key)

    def attributeSelectedFeatures(self, layer, attributes):
        layer.startEditing()
        features = layer.selectedFeatures()
        for feature in features:
            self.attributeFeature(feature, layer, attributes)
            layer.updateFeature(feature)
        self.canvasRefresh()

    def attributeFeature(self, feature, layer, attributes):
        for fieldName in attributes:
            indx = layer.fields().indexFromName(fieldName)
            if indx < 0:
                continue
            config = layer.editorWidgetSetup(indx).config()
            isMapValue = "map" in config
            attributeValue = attributes[fieldName]
            if isMapValue:
                valueMap = self.formatMapValues(config["map"])
                if attributeValue in valueMap:
                    feature.setAttribute(indx, valueMap[attributeValue])
            elif attributeValue and not (attributeValue in ["NULL", "IGNORAR"]):
                """if re.match('^\@value\(".+"\)$', value):
                variable = value.split('"')[-2]
                value = ProjectQgis(self.iface).getVariableProject(variable)"""
                feature.setAttribute(indx, attributeValue)

    def cutAndPasteSelectedFeatures(self, layer, destinatonLayer, attributes):
        geometryFilterDict = {
            QgsWkbTypes.PointGeometry: (QgsWkbTypes.PointGeometry,),
            QgsWkbTypes.LineGeometry: (QgsWkbTypes.LineGeometry,),
            QgsWkbTypes.PolygonGeometry: (QgsWkbTypes.PointGeometry, QgsWkbTypes.PolygonGeometry)
        }
        if destinatonLayer.geometryType() not in geometryFilterDict[layer.geometryType()]:
            return
        layer.startEditing()
        destinatonLayer.startEditing()
        features = layer.selectedFeatures()
        newFeatures = []
        for feature in features:
            newFeat = core.QgsFeature()
            newFeat.setFields(destinatonLayer.fields())
            newGeom = feature.geometry().pointOnSurface() \
                if destinatonLayer.geometryType() == core.QgsWkbTypes.PointGeometry \
                    and layer.geometryType() == core.QgsWkbTypes.PolygonGeometry \
                else feature.geometry()
            newFeat.setGeometry(newGeom)
            self.attributeFeature(newFeat, destinatonLayer, attributes)
            newFeatures.append(newFeat)
        layer.deleteSelectedFeatures()
        destinatonLayer.addFeatures(newFeatures)
        self.canvasRefresh()

    def startToolByName(self, name):
        action = self.actionsFactory.getAction(name)
        action.execute()

    def connectSignal(self, signalName, callback):
        signals = self.getSignals()
        signal = signals[signalName] if signalName in signals else None
        if not signal:
            return
        signal.connect(callback)

    def disconnectSignal(self, signalName, callback):
        signals = self.getSignals()
        signal = signals[signalName] if signalName in signals else None
        if not signal:
            return
        try:
            signal.disconnect(callback)
        except Exception as e:
            pass

    def getSignals(self):
        return {
            "StartAddFeature": iface.actionAddFeature().toggled,
            "ClickLayerTreeView": iface.layerTreeView().clicked,
            "AddLayerTreeView": core.QgsProject.instance().legendLayersAdded,
            "StartEditing": iface.actionToggleEditing().triggered,
        }

    def suppressLayerForm(self, layer, suppress):
        setup = layer.editFormConfig()
        setup.setSuppress(
            core.QgsEditFormConfig.SuppressOn
            if suppress
            else core.QgsEditFormConfig.SuppressOff
        )
        layer.setEditFormConfig(setup)

    def canvasRefresh(self):
        iface.mapCanvas().refresh()
