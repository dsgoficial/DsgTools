from qgis import core, gui
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import json
from DsgTools.Modules.qgis.factories.actionsFactory import ActionsFactory

class QgisCtrl:
    
    def __init__(
            self,
            actionsFactory=ActionsFactory()
        ):
        self.actionsFactory = actionsFactory

    def getLoadedVectorLayerNames(self):
        return [
            l.dataProvider().uri().table()
            for l in core.QgsProject.instance().mapLayers().values()
            if l.type() == core.QgsMapLayer.VectorLayer
        ]

    def getLoadedVectorLayers(self):
        return [
            l
            for l in core.QgsProject.instance().mapLayers().values()
            if l.type() == core.QgsMapLayer.VectorLayer
        ]

    def getVectorLayersByName(self, layerName):
        return [
            l
            for l in core.QgsProject.instance().mapLayers().values()
            if l.dataProvider().uri().table() == layerName and l.type() == core.QgsMapLayer.VectorLayer
        ]

    def getAttributesConfigByLayerName(
            self, 
            layerName,
            withPrimaryKey=False,
            withVirtualField=False
        ):
        for l in core.QgsProject.instance().mapLayers().values():
            if not( l.name() == layerName ):
                continue
            return self.getAttributesConfigByLayer( l, withPrimaryKey,  withVirtualField )
        return {}

    def getAttributesConfigByLayer(self, layer, withPrimaryKey,  withVirtualField):
        attrConfig = {}
        for fieldIndex in layer.attributeList():
            if not( withPrimaryKey ) and ( fieldIndex in self.getLayerPrimaryKeyIndexes( layer ) ):
                continue
            if not( withVirtualField ) and ( self.getFieldTypeName( layer, fieldIndex ) == '' ) :
                continue
            fieldName = layer.fields().field( fieldIndex ).name()
            fieldConfig = layer.fields().field( fieldIndex ).editorWidgetSetup().config()
            attrConfig[ fieldName ] = fieldConfig
        return attrConfig
    
    def getLayerPrimaryKeyIndexes(self, layer):
        return layer.dataProvider().pkAttributeIndexes()

    def getFieldTypeName(self, layer, fieldIndex):
        return layer.fields().field( fieldIndex ).typeName()

    def getAcquisitionToolNames(self):
        return {
           'Padrão': None,
           'Ângulo Reto': 'RightDegreeAngleDigitizing',
           'Mão Livre': 'FreeHand'
        }

    def addDockWidget(self, dockWidget, side=QtCore.Qt.LeftDockWidgetArea):
        iface.addDockWidget(side, dockWidget)

    def removeDockWidget(self, dockWidget):
        iface.removeDockWidget( dockWidget )

    def registerShortcut(self, shortcut):
        gui.QgsGui.shortcutsManager().registerShortcut( shortcut )
    
    def unregisterShortcut(self, shortcut):
        gui.QgsGui.shortcutsManager().unregisterShortcut( shortcut )

    def setDefaultFields(self, layer, attributes, reset=False):
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for attributeName in attributes:
            fieldIndex = layer.fields().indexFromName( attributeName )
            if fieldIndex in primaryKeyIndexes:
                continue
            attributeValue = attributes[ attributeName ]
            configField = layer.defaultValueDefinition( fieldIndex )
            isMapValue = ( 'map' in layer.editorWidgetSetup( fieldIndex ).config() )
            if isMapValue:
                valueMap = layer.editorWidgetSetup( fieldIndex ).config()['map']
                if not( attributeValue is None ) and attributeValue in valueMap:
                    configField.setExpression("{0}".format( valueMap[ attributeValue ] ) )
                elif reset:
                    configField.setExpression("")
            else:
                if attributeValue != '':
                    configField.setExpression("'{0}'".format( attributeValue ) )
                elif reset:
                    configField.setExpression("")
            layer.setDefaultValueDefinition( fieldIndex, configField )

    def getDefaultFields(self, layer):
        attributesValues = {}
        primaryKeyIndexes = layer.dataProvider().pkAttributeIndexes()
        for fieldIndex in layer.attributeList():
            fieldName = layer.fields().field( fieldIndex ).name()
            if fieldIndex in primaryKeyIndexes:
                continue
            configField = layer.defaultValueDefinition( fieldIndex )
            attributesValues[ fieldName ] = configField.expression()
        return attributesValues

    def setActiveLayer(self, layer):
        iface.setActiveLayer( layer )
        layer.startEditing()
        iface.actionAddFeature().trigger() 

    def setLayerVariable(self, layer, key, value):
        core.QgsExpressionContextUtils.setLayerVariable(
            layer,
            key,
            value
        )

    def getLayerVariable(self, layer, key):
        return core.QgsExpressionContextUtils.layerScope( layer ).variable( key )

    def attributeSelectedFeatures(self, layer, attributes):
        features = layer.selectedFeatures()
        for feature in features:
            for fieldName in attributes:
                indx = layer.fields().indexFromName( fieldName )
                if indx < 0:
                    continue
                config = layer.editorWidgetSetup( indx ).config()
                isMapValue = ('map' in config)
                attributeValue  = attributes[ fieldName ]
                if isMapValue:
                    valueMap = config['map']
                    if attributeValue in valueMap:
                        feature.setAttribute( indx, valueMap[ attributeValue ] )
                elif attributeValue and not( attributeValue in ['NULL', 'IGNORAR'] ):
                    """ if re.match('^\@value\(".+"\)$', value):
                        variable = value.split('"')[-2]
                        value = ProjectQgis(self.iface).getVariableProject(variable) """
                    feature.setAttribute( indx, attributeValue )   
            layer.updateFeature( feature )

    def startToolByName(self, name):
        action = self.actionsFactory.getAction( name )
        action.execute()

    def connectSignal(self, signalName, callback):
        signals = self.getSignals()
        signal = signals[ signalName ] if signalName in signals else None
        if not signal:
            return
        signal.connect( callback )

    def disconnectSignal(self, signalName, callback):
        signals = self.getSignals()
        signal = signals[ signalName ] if signalName in signals else None
        if not signal:
            return
        try:
            signal.disconnect( callback )
        except Exception as e:
            pass

    def getSignals(self):
        return {
            'StartAddFeature': iface.actionAddFeature().toggled,
            'ClickLayerTreeView': iface.layerTreeView().clicked,
            'AddLayerTreeView': core.QgsProject.instance().legendLayersAdded,
            'StartEditing': iface.actionToggleEditing().triggered
        }
        
    def suppressLayerForm(self, layer, suppress):
        setup = layer.editFormConfig()
        setup.setSuppress(
            core.QgsEditFormConfig.SuppressOn if suppress else core.QgsEditFormConfig.SuppressOff
        )
        layer.setEditFormConfig(setup)