# -*- coding: utf-8 -*-
"""
/***************************************************************************
InspectFeatures
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
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
import os
from qgis.PyQt.QtWidgets import QMessageBox, QSpinBox, QAction, QWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings, pyqtSignal, pyqtSlot, QObject, Qt
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.Qt import QObject

from qgis.core import (
    QgsMapLayer,
    Qgis,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsProject,
)
from qgis.gui import QgsMessageBar

from .inspectFeatures_ui import Ui_Form

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'inspectFeatures.ui'))


class InspectFeatures(QWidget, Ui_Form):
    # idxChanged = pyqtSignal(int)
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(InspectFeatures, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.splitter2.hide()
        self.iface = iface
        # self.iface.currentLayerChanged.connect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.connect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.connect(
            self.mFieldExpressionWidget.setLayer
        )
        self.mMapLayerComboBox.layerChanged.connect(self.mFieldComboBox.setLayer)
        if not self.iface.activeLayer():
            self.enableTool(False)
        # self.iface.currentLayerChanged.connect(self.enableTool)
        self.mMapLayerComboBox.layerChanged.connect(self.enableTool)
        self.zoomPercentageSpinBox.setMinimum(0)
        self.zoomPercentageSpinBox.setMaximum(100)
        self.zoomPercentageSpinBox.setDecimals(3)
        self.zoomPercentageSpinBox.setSingleStep(1)
        self.zoomPercentageSpinBox.setSuffix("%")
        self.zoomPercentageSpinBox.setValue(100)
        self.zoomPercentageSpinBox.setEnabled(False)
        self.zoomPercentageSpinBox.hide()
        self.mScaleWidget.setScaleString("1:40000")
        self.mScaleWidget.setEnabled(False)
        self.mScaleWidget.hide()
        self.enableScale()
        self.canvas = self.iface.mapCanvas()
        self.allLayers = {}
        # self.idxChanged.connect(self.setNewId)
        self.setToolTip("")
        icon_path = ":/plugins/DsgTools/icons/inspectFeatures.png"
        text = self.tr("DSGTools: Inspect Features")
        self.activateToolAction = self.add_action(
            icon_path, text, self.inspectPushButton.toggle, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.activateToolAction, "")
        icon_path = ":/plugins/DsgTools/icons/backInspect.png"
        text = self.tr("DSGTools: Back Inspect")
        self.backButtonAction = self.add_action(
            icon_path, text, self.backInspectButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.backButtonAction, "")
        icon_path = ":/plugins/DsgTools/icons/nextInspect.png"
        text = self.tr("DSGTools: Next Inspect")
        self.nextButtonAction = self.add_action(
            icon_path, text, self.nextInspectButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.nextButtonAction, "")
        icon_path = ":/plugins/DsgTools/icons/reload.png"
        text = self.tr("DSGTools: Set Active Layer on Feature Inspector")
        self.refreshPushButtonAction = self.add_action(
            icon_path, text, self.refreshPushButton.click, parent=self.parent
        )
        self.iface.registerMainWindowAction(self.refreshPushButtonAction, "")
        self.refreshPushButton.setToolTip(
            self.tr("Set current layer as selected layer on inspect tool")
        )
        self.sortPushButton.setToolTip(self.tr("Sort by attribute"))
        self.mFieldExpressionWidget.fieldChanged.connect(self.resetCurrentIndex)

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def getIterateLayer(self):
        return self.mMapLayerComboBox.currentLayer()

    def enableTool(self, enabled=True):
        allowed = (
            False
            if enabled == None or not isinstance(enabled, QgsVectorLayer)
            else True
        )
        toggled = self.inspectPushButton.isChecked()
        enabled = allowed and toggled
        self.backInspectButton.setEnabled(enabled)
        self.nextInspectButton.setEnabled(enabled)
        self.idSpinBox.setEnabled(enabled)
        self.sortPushButton.setEnabled(enabled)

    def enableScale(self):
        """
        The scale combo should only be enabled for point layers
        """
        currentLayer = self.getIterateLayer()
        if not currentLayer:
            return
        if currentLayer.type() != QgsMapLayer.VectorLayer:
            return
        if currentLayer.geometryType() == QgsWkbTypes.PointGeometry:
            self.mScaleWidget.setEnabled(True)
            self.mScaleWidget.show()
            self.zoomPercentageSpinBox.setEnabled(False)
            self.zoomPercentageSpinBox.hide()
        else:
            self.mScaleWidget.setEnabled(False)
            self.mScaleWidget.hide()
            self.zoomPercentageSpinBox.setEnabled(True)
            self.zoomPercentageSpinBox.show()

    @pyqtSlot(bool)
    def on_nextInspectButton_clicked(self):
        """
        Inspects the next feature
        """
        if self.nextInspectButton.isEnabled():
            method = getattr(self, "testIndexFoward")
            self.iterateFeature(method)

    def testIndexFoward(self, index, maxIndex, minIndex):
        """
        Gets the next index
        """
        index += 1
        if index > maxIndex:
            index = minIndex
        return index

    def testIndexBackwards(self, index, maxIndex, minIndex):
        """
        gets the previous index
        """
        index -= 1
        if index < minIndex:
            index = maxIndex
        return index

    @pyqtSlot(bool)
    def on_backInspectButton_clicked(self):
        """
        Inspects the previous feature
        """
        if self.backInspectButton.isEnabled():
            method = getattr(self, "testIndexBackwards")
            self.iterateFeature(method)

    @pyqtSlot(int, name="on_idSpinBox_valueChanged")
    def setNewId(self, newId):
        if not isinstance(self.sender(), QSpinBox):
            self.idSpinBox.setValue(newId)
        else:
            currentLayer = self.getIterateLayer()
            lyrId = currentLayer.id()
            if lyrId not in list(self.allLayers.keys()):
                self.allLayers[lyrId] = 0
                return
            oldIndex = self.allLayers[lyrId]
            if oldIndex == 0:
                return
            featIdList = self.getFeatIdList(currentLayer)
            if oldIndex not in featIdList:
                oldIndex = 0
            zoom = (
                self.mScaleWidget.scale()
                if currentLayer.geometryType() == QgsWkbTypes.PointGeometry
                else self.zoomPercentageSpinBox.value()
            )
            if oldIndex == newId:
                # self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=Qgis.Warning, duration=2)
                return
            try:
                index = featIdList.index(newId)
                self.allLayers[lyrId] = index
                self.makeZoom(zoom, currentLayer, newId)
                self.idSpinBox.setSuffix(f" ({index + 1}/{len(featIdList)})")
            except:
                # self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=Qgis.Warning, duration=2)
                self.idSpinBox.setValue(oldIndex)
                self.makeZoom(zoom, currentLayer, oldIndex)

    def getFeatIdList(self, currentLayer):
        # getting all features ids
        if (
            self.mFieldExpressionWidget.currentText() != ""
            and not self.mFieldExpressionWidget.isValidExpression()
        ):
            self.iface.messageBar().pushMessage(
                self.tr("Warning!"),
                self.tr("Invalid attribute filter!"),
                level=Qgis.Warning,
                duration=2,
            )
            return []
        request = QgsFeatureRequest()
        request.setFlags(QgsFeatureRequest.NoGeometry)
        if self.mFieldExpressionWidget.currentText() != "":
            request.setFilterExpression(self.mFieldExpressionWidget.asExpression())
        clauseList = []
        if self.sortPushButton.isChecked():
            # order by some attribute
            clause = QgsFeatureRequest.OrderByClause(
                self.mFieldComboBox.currentField(),
                self.ascRadioButton.isChecked(),
                False,
            )
            clauseList.append(clause)
        clauseId = QgsFeatureRequest.OrderByClause(
            "$id", ascending=self.ascRadioButton.isChecked()
        )
        clauseList.append(clauseId)
        orderby = QgsFeatureRequest.OrderBy(clauseList)
        request.setOrderBy(orderby)
        featIdList = [i.id() for i in currentLayer.getFeatures(request)]
        # sort is faster than sorted (but sort is just available for lists)
        return featIdList

    def iterateFeature(self, method):
        """
        Iterates over the features selecting and zooming to the desired one
        method: method used to determine the desired feature index
        """
        currentLayer = self.getIterateLayer()
        lyrName = currentLayer.name()

        zoom = (
            self.mScaleWidget.scale()
            if currentLayer.geometryType() == QgsWkbTypes.PointGeometry
            else self.zoomPercentageSpinBox.value()
        )

        featIdList = self.getFeatIdList(currentLayer)

        if not currentLayer or len(featIdList) == 0:
            self.errorMessage()
            return

        # checking if this is the first time for this layer (currentLayer)
        first = False
        if lyrName not in list(self.allLayers.keys()):
            self.allLayers[lyrName] = 0
            first = True

        # getting the current index
        index = self.allLayers[lyrName]

        # getting max and min ids
        # this was made because the list is already sorted, there's no need to calculate max and min
        maxIndex = len(featIdList) - 1
        minIndex = 0

        self.idSpinBox.setMaximum(maxIndex)
        self.idSpinBox.setMinimum(minIndex)

        # getting the new index
        if not first:
            index = method(index, maxIndex, minIndex)
        self.idSpinBox.setSuffix(" ({0}/{1})".format(index + 1, len(featIdList)))
        self.allLayers[lyrName] = index

        # getting the new feature id
        id = featIdList[index]

        # adjustin the spin box value
        # self.idxChanged.emit(id)

        self.makeZoom(zoom, currentLayer, id)
        self.selectLayer(id, currentLayer)

    def errorMessage(self):
        """
        Shows am error message
        """
        QMessageBox.warning(
            self.iface.mainWindow(),
            self.tr("ERROR:"),
            self.tr(
                "<font color=red>There are no features in the current layer:<br></font><font color=blue>Add features and try again!</font>"
            ),
            QMessageBox.Close,
        )

    def selectLayer(self, index, currentLayer):
        """
        Remove current layer feature selection
        currentLayer: layer that will have the feature selection removed
        """
        if currentLayer:
            currentLayer.removeSelection()
            currentLayer.select(index)

    def zoomToLayer(self, layer, zoom=None):
        box = layer.boundingBoxOfSelected()
        if zoom is not None:
            box.grow(min(box.width(), box.height()) * (100 - zoom) / 100)
        # Defining the crs from src and destiny
        epsg = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        crsDest = QgsCoordinateReferenceSystem(epsg)
        # getting srid from something like 'EPSG:31983'
        if not layer:
            layer = self.iface.mapCanvas().currentLayer()
        srid = layer.crs().authid()
        crsSrc = QgsCoordinateReferenceSystem(
            srid
        )  # here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(
            crsSrc, crsDest, QgsProject.instance()
        )
        newBox = coordinateTransformer.transform(box)

        self.iface.mapCanvas().setExtent(newBox)
        self.iface.mapCanvas().refresh()

    def zoomFeature(self, zoom, idDict=None):
        """
        Zooms to current layer selected features according to a specific zoom
        zoom: zoom to be applied
        """
        idDict = dict() if idDict is None else idDict
        currentLayer = self.getIterateLayer()
        if idDict == {}:
            self.zoomToLayer(currentLayer, zoom=float(zoom))
        else:
            id = idDict["id"]
            lyr = idDict["lyr"]
            selectIdList = lyr.selectedFeatureIds()
            lyr.removeSelection()
            lyr.selectByIds([id])
            self.zoomToLayer(layer=lyr, zoom=float(zoom))
            lyr.selectByIds(selectIdList)

        if self.getIterateLayer().geometryType() == QgsWkbTypes.PointGeometry:
            self.iface.mapCanvas().zoomScale(float(zoom))

    @pyqtSlot(bool, name="on_inspectPushButton_toggled")
    def toggleBar(self, toggled=None):
        """
        Shows/Hides the tool bar
        """
        if toggled is None:
            toggled = self.inspectPushButton.isChecked()
        if toggled:
            self.splitter.show()
            self.enableTool(self.mMapLayerComboBox.currentLayer())
            self.setToolTip(self.tr("Select a vector layer to enable tool"))
        else:
            self.splitter.hide()
            self.enableTool(False)
            self.setToolTip("")

    @pyqtSlot(bool, name="on_sortPushButton_toggled")
    def toggleSort(self, toggled=None):
        """
        Shows/hides the sort options
        """
        if toggled is None:
            toggled = self.sortPushButton.isChecked()
        if toggled:
            self.splitter2.show()
            self.resetCurrentIndex()
        else:
            self.splitter2.hide()

    def resetCurrentIndex(self, indexName=None):
        lyr = self.mMapLayerComboBox.currentLayer()
        if lyr is not None:
            lyrId = lyr.id()
            self.allLayers[lyrId] = 0

    def setValues(self, featIdList, currentLayer):
        lyrId = currentLayer.id()
        featIdList.sort()
        self.allLayers[lyrId] = 0

        maxIndex = len(featIdList) - 1
        minIndex = 0

        self.idSpinBox.setMaximum(featIdList[maxIndex])
        self.idSpinBox.setMinimum(featIdList[minIndex])

        # getting the new feature id
        id = featIdList[0]

        # adjustin the spin box value
        # self.idxChanged.emit(id)
        # self.idSpinBox.setValue(id)

        zoom = self.mScaleWidget.scale()
        self.makeZoom(zoom, currentLayer, id)

    def makeZoom(self, zoom, currentLayer, id):
        # selecting and zooming to the feature
        # if not self.onlySelectedRadioButton.isChecked():
        #     self.selectLayer(id, currentLayer)
        #     self.zoomFeature(zoom)
        # else:
        if self.usePanCkb.isChecked():
            currentLayer.select(id)
            self.iface.mapCanvas().panToFeatureIds(currentLayer, [id])
            return
        self.zoomFeature(zoom, idDict={"id": id, "lyr": currentLayer})

    @pyqtSlot(bool)
    def on_onlySelectedRadioButton_toggled(self, toggled):
        currentLayer = self.getIterateLayer()
        if toggled:
            featIdList = currentLayer.selectedFeatureIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(False)
        else:
            featIdList = currentLayer.allFeatureIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(True)

    @pyqtSlot(bool)
    def on_refreshPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if isinstance(activeLayer, QgsVectorLayer):
            self.mMapLayerComboBox.setLayer(activeLayer)
        else:
            self.iface.messageBar().pushMessage(
                self.tr("Warning!"),
                self.tr("Active layer is not valid to be used in this tool."),
                level=Qgis.Warning,
                duration=2,
            )
        self.mFieldExpressionWidget.setExpression("")

    def unload(self):
        try:
            self.iface.unregisterMainWindowAction(self.activateToolAction)
        except:
            pass
        try:
            self.iface.unregisterMainWindowAction(self.backButtonAction)
        except:
            pass
        try:
            self.iface.unregisterMainWindowAction(self.nextButtonAction)
        except:
            pass
        try:
            self.iface.unregisterMainWindowAction(self.refreshPushButtonAction)
        except:
            pass

    def getToolState(self) -> dict:
        currentLayer = self.mMapLayerComboBox.currentLayer()
        return {
            "bar_is_toggled": self.inspectPushButton.isChecked(),
            "current_layer": currentLayer.id(),
            "current_feature_state_dict": self.allLayers,
            "current_zoom": self.mScaleWidget.scale()
            if currentLayer.geometryType() == QgsWkbTypes.PointGeometry
            else self.zoomPercentageSpinBox.value(),
            "use_pan": self.usePanCkb.isChecked(),
            "current_filter_expression": self.mFieldExpressionWidget.currentText(),
            "sort_is_toggled": self.sortPushButton.isChecked(),
            "current_sort_field": self.mFieldComboBox.currentField(),
            "is_ascending": self.ascRadioButton.isChecked(),
        }

    def setToolState(self, stateDict: dict) -> bool:
        isBarToggled = stateDict.get("bar_is_toggled", None)
        if isBarToggled is None:
            return False
        if self.inspectPushButton.isChecked():
            self.inspectPushButton.click()  # sim, é intencional clicar duas vezes
        if isBarToggled:
            self.inspectPushButton.click()
        currentLayerId = stateDict.get("current_layer", None)
        if currentLayerId is None:
            return False
        currentLayer = QgsProject.instance().mapLayers().get(currentLayerId, None)
        if currentLayer is None:
            return False
        self.mMapLayerComboBox.setLayer(currentLayer)
        currentStateDict = stateDict.get("current_feature_state_dict", None)
        if currentStateDict is None:
            return False
        self.allLayers.update(currentStateDict)
        currentZoom = stateDict.get("current_zoom", None)
        if currentLayer.geometryType() == QgsWkbTypes.PointGeometry:
            self.mScaleWidget.setScale(currentZoom)
        else:
            self.zoomPercentageSpinBox.setValue(currentZoom)
        usePan = stateDict.get("use_pan", None)
        if usePan is None:
            return False
        self.usePanCkb.setChecked(usePan)
        currentFilterExpression = stateDict.get("current_filter_expression", None)
        if currentFilterExpression is None:
            return False
        self.mFieldExpressionWidget.setExpression(currentFilterExpression)
        isSortToggled = stateDict.get("sort_is_toggled", None)
        if not isSortToggled:
            return True
        self.sortPushButton.click()
        currentSortField = stateDict.get("current_sort_field", None)
        if currentSortField is None:
            return False
        self.mFieldComboBox.setField(currentSortField)
        isAscending = stateDict.get("is_ascending", None)
        if isAscending is None:
            return False
        if not isAscending:
            self.descRadioButton.click()
        return True
