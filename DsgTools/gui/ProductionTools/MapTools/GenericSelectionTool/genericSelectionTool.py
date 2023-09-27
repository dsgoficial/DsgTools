# -*- coding: utf-8 -*-
"""
/***************************************************************************
multiLayerSelect
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
                               (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
                               borba.philipe@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin MultipleLayerSelection
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
from functools import partial

from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import (
    QgsPointXY,
    QgsRectangle,
    QgsFeatureRequest,
    QgsVectorLayer,
    QgsProject,
    QgsWkbTypes,
    QgsRasterLayer,
)
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QMenu, QApplication

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler


class GenericSelectionTool(QgsMapTool):
    def __init__(self, iface):
        """
        Tool Behaviours: (all behaviours start edition, except for rectangle one)
        1- Left Click: Clears previous selection, selects feature, sets feature layer as active layer.
        The selection is done with the following priority: Point, Line then Polygon.
        Selection is only done in visible layer.
        2- Control + Left Click: Adds to selection selected feature. This selection follows the priority in item 1.
        3- Right Click: Opens feature form
        4- Control + Right Click: clears selection and set feature's layer as activeLayer. activeLayer's definition
        follows priority of item 1;
        5- Shift + drag and drop: draws a rectangle, then features that intersect this rectangl'e are added to selection
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.toolAction = None
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.hoverRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        mFillColor = QColor(254, 178, 76, 63)
        self.rubberBand.setColor(mFillColor)
        self.hoverRubberBand.setColor(QColor(255, 0, 0, 90))
        self.rubberBand.setWidth(1)
        self.reset()
        self.blackList = self.getBlackList()
        self.cursorChanged = False
        self.menuHovered = False  # indicates hovering actions over context menu
        self.geometryHandler = GeometryHandler(iface=self.iface)

    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + "/genericSelect.png"
        toolTip = self.tr(
            "DSGTools: Generic Selector\nLeft Click: select feature's layer and put it on edit mode\nRight Click: Open feature's form\nControl+Left Click: add/remove feature from selection\nShift+Left Click+drag and drop: select all features that intersects rubberband."
        )
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Generic Selector"),
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentToolbar=parentMenu,
            isCheckable=True,
        )
        self.setAction(action)

    def getBlackList(self):
        settings = QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        valueList = settings.value("valueList")
        if valueList:
            valueList = valueList.split(";")
            return valueList
        else:
            return ["moldura"]

    def reset(self):
        """
        Resets rubber band.
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)

    def canvasMoveEvent(self, e):
        """
        Used only on rectangle select.
        """
        if self.menuHovered:
            # deactivates rubberband when the context menu is "destroyed"
            self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        """
        Builds rubberband rect.
        """
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)  # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        """
        Builds rectangle from self.startPoint and self.endPoint
        """
        if self.startPoint is None or self.endPoint is None:
            return None
        elif (
            self.startPoint.x() == self.endPoint.x()
            or self.startPoint.y() == self.endPoint.y()
        ):
            return None
        return QgsRectangle(self.startPoint, self.endPoint)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)

    def canvasReleaseEvent(self, e):
        """
        After the rectangle is built, here features are selected.
        """
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            firstGeom = self.checkSelectedLayers()
            self.isEmittingPoint = False
            r = self.rectangle()
            if r is None:
                return
            layers = self.canvas.layers()
            for layer in layers:
                # ignore layers on black list and features that are not vector layers
                if not isinstance(layer, QgsVectorLayer) or (
                    self.layerHasPartInBlackList(layer.name())
                ):
                    continue
                if firstGeom is not None and layer.geometryType() != firstGeom:
                    # if there are features already selected, shift will only get the same type geometry
                    # if more than one ty of geometry is present, only the strongest will be selected
                    continue
                # builds bbRect and select from layer, adding selection
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                layer.selectByRect(bbRect, behavior=QgsVectorLayer.AddToSelection)
            self.rubberBand.hide()

    def canvasPressEvent(self, e):
        """
        Method used to build rectangle if shift is held, otherwise, feature select/deselect and identify is done.
        """
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.isEmittingPoint = True
            self.startPoint = self.toMapCoordinates(e.pos())
            self.endPoint = self.startPoint
            self.isEmittingPoint = True
            self.showRect(self.startPoint, self.endPoint)
        else:
            self.isEmittingPoint = False
            self.createContextMenu(e)

    def getCursorRect(self, e):
        """
        Calculates small cursor rectangle around mouse position. Used to facilitate operations
        """
        p = self.toMapCoordinates(e.pos())
        w = self.canvas.mapUnitsPerPixel() * 10
        return QgsRectangle(p.x() - w, p.y() - w, p.x() + w, p.y() + w)

    def layerHasPartInBlackList(self, lyrName):
        """
        Verifies if terms in black list appear on lyrName
        """
        for item in self.getBlackList():
            if item.lower() in lyrName.lower():
                return True
        return False

    def getPrimitiveDict(self, e, hasControlModifier=False, hasAltModifier=False):
        """
        Builds a dict with keys as geometryTypes of layer, which are Qgis.Point (value 0), Qgis.Line (value 1) or Qgis.Polygon (value 2),
        and values as layers from self.iface.mapCanvas().layers(). When self.iface.mapCanvas().layers() is called, a list of
        layers ordered according to lyr order in TOC is returned.
        """
        # these layers are ordered by view order
        primitiveDict = dict()
        firstGeom = self.checkSelectedLayers()
        visibleLayers = QgsProject.instance().layerTreeRoot().checkedLayers()
        iterator = (
            self.iface.mapCanvas().layers()
            if not hasAltModifier
            else [self.iface.activeLayer()]
        )
        for lyr in iterator:  # ordered layers
            # layer types other than VectorLayer are ignored, as well as layers in black list and layers that are not visible
            if (
                not isinstance(lyr, QgsVectorLayer)
                or (self.layerHasPartInBlackList(lyr.name()))
                or lyr not in visibleLayers or lyr.readOnly()
            ):
                continue
            if (
                hasControlModifier
                and (not firstGeom)
                and (not primitiveDict or lyr.geometryType() < firstGeom)
            ):
                firstGeom = lyr.geometryType()
            geomType = lyr.geometryType()
            if geomType not in primitiveDict:
                primitiveDict[geomType] = []
            # removes selection
            if (not hasControlModifier and e.button() == Qt.LeftButton) or (
                hasControlModifier and e.button() == Qt.RightButton
            ):
                lyr.removeSelection()
            primitiveDict[geomType].append(lyr)
        if hasControlModifier and firstGeom in [0, 1, 2]:
            return {firstGeom: primitiveDict[firstGeom]}
        else:
            return primitiveDict

    def deactivate(self):
        """
        Deactivate tool.
        """
        QApplication.restoreOverrideCursor()
        self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        try:
            self.rubberBand.reset()
            if self.toolAction:
                self.toolAction.setChecked(False)
            if self is not None:
                QgsMapTool.deactivate(self)
        except:
            pass

    def activate(self):
        """
        Activate tool.
        """
        if self.toolAction:
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)

    def setSelectionFeature(
        self, layer, feature, selectAll=False, setActiveLayer=False
    ):
        """
        Selects a given feature on canvas.
        :param layer: (QgsVectorLayer) layer containing the target feature.
        :param feature: (QgsFeature) taget feature to be selected.
        :param selectAll: (bool) indicates whether or not this fuction was called from a select all command.
                          so it doesn't remove selection from those that are selected already from the list.
        :param setActiveLayer: (bool) indicates whether method should set layer as active.
        """
        idList = layer.selectedFeatureIds()
        self.iface.setActiveLayer(layer)
        layer.startEditing()
        featId = feature.id()
        if featId not in idList:
            idList.append(featId)
        elif not selectAll:
            idList.pop(idList.index(featId))
        layer.selectByIds(idList)
        if setActiveLayer:
            layer.startEditing()
            self.iface.setActiveLayer(layer)
        return

    def setSelectionListFeature(self, dictLayerFeature, selectAll=True):
        """
        Selects all features on canvas of a given dict.
        :param dictLayerFeature: (dict) dict of layers/features to be selected.
        :param selectAll: (bool) indicates if "All"-command comes from a "Select All". In that case, selected features
                          won't be deselected.
        """
        for layer, listOfFeatures in dictLayerFeature.items():
            geomType = layer.geometryType()
            # ID list of features already selected
            idList = layer.selectedFeatureIds()
            # restart feature ID list for each layer
            featIdList = []
            for feature in listOfFeatures:
                featId = feature.id()
                if featId not in idList:
                    idList.append(featId)
                elif not selectAll:
                    idList.pop(idList.index(featId))
            layer.selectByIds(idList)
            layer.startEditing()
        # last layer is set active and
        self.iface.setActiveLayer(layer)

    def openMultipleFeatureForm(self, dictLayerFeature):
        """
        Opens all features Feature Forms of a given list.
        :param dictLayerFeature: (dict) dict of layers/features to have their feature form exposed.
        """
        for layer, features in dictLayerFeature.items():
            for feat in features:
                self.iface.openFeatureForm(layer, feat, showModal=False)

    def filterStrongestGeometry(self, dictLayerFeature):
        """
        Filter a given dict of features for its strongest geometry.
        :param dictLayerFeature: (dict) a dict of layers and its features to be filtered.
        :return: (dict) filtered dict with only layers of the strongest geometry on original dict.
        """
        strongest_geometry = 3
        outDict = dict()
        if dictLayerFeature:
            for lyr in dictLayerFeature:
                # to retrieve strongest geometry value
                if strongest_geometry > lyr.geometryType():
                    strongest_geometry = lyr.geometryType()
                if strongest_geometry == 0:
                    break
        for lyr in dictLayerFeature:
            if lyr.geometryType() == strongest_geometry:
                outDict[lyr] = dictLayerFeature[lyr]
        return outDict

    def createRubberBand(self, feature, layer, geom):
        """
        Creates a rubber band around from a given a standard feature string.
        :param feature: taget feature to be highlighted
        :param layer: layer containing the target feature
        :param geom: int indicating geometry type of target feature
        """
        if geom == 0:
            self.hoverRubberBand.reset(QgsWkbTypes.PointGeometry)
        elif geom == 1:
            self.hoverRubberBand.reset(QgsWkbTypes.LineGeometry)
        else:
            self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        self.hoverRubberBand.addGeometry(feature.geometry(), layer)
        # to inform the code that menu has been hovered over
        self.menuHovered = True

    def createMultipleRubberBand(self, dictLayerFeature):
        """
        Creates rubberbands around features.
        :param dictLayerFeature: (dict) dict of layer/features to have rubberbands built around.
        """
        # only one type of geometry at a time will have rubberbands around it
        geom = list(dictLayerFeature.keys())[0].geometryType()
        if geom == 0:
            self.hoverRubberBand.reset(QgsWkbTypes.PointGeometry)
        elif geom == 1:
            self.hoverRubberBand.reset(QgsWkbTypes.LineGeometry)
        else:
            self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        for layer, features in dictLayerFeature.items():
            for feat in features:
                self.hoverRubberBand.addGeometry(feat.geometry(), layer)
        self.menuHovered = True

    def checkSelectedLayers(self):
        """
        Checks if there are layers selected on canvas. If there are, returns the geometry type of
        selected feature(s). If more than one type of feature is selected, the "strongest" geometry
        is returned.
        """
        geom = None
        for layer in self.iface.mapCanvas().layers():
            if not isinstance(layer, QgsVectorLayer):
                continue
            selection = layer.selectedFeatures()
            if not len(selection):
                continue
            if geom == None:
                geom = layer.geometryType()
                continue
            elif layer.geometryType() < geom:
                geom = layer.geometryType()
                continue
        return geom

    def addCallBackToAction(self, action, onTriggeredAction, onHoveredAction=None):
        """
        Adds action the command to the action. If onHoveredAction is given, signal "hovered" is applied with given action.
        :param action: (QAction) associated with target context menu.
        :param onTriggeredAction: (object) action to be executed when the given action is triggered.
        :param onHoveredAction: (object) action to be executed whilst the given action is hovered.
        """
        action.triggered.connect(onTriggeredAction)
        if onHoveredAction:
            action.hovered.connect(onHoveredAction)

    def getCallback(self, e, layer, feature, geomType=None, selectAll=True):
        """
        Gets the callback for an action.
        :param e: (QMouseEvent) mouse event on canvas.
        :param layer: (QgsVectorLayer) layer to be treated.
        :param feature: (QgsFeature) feature to be treated.
        :param geomType: (int) code indicating layer geometry type. It is retrieved OTF in case it's not given.
        :return: (tuple-of function_lambda) callbacks for triggered and hovered signals.
        """
        if not geomType:
            geomType = layer.geometryType()
        if e.button() == Qt.LeftButton:
            # line added to make sure the action is associated with current loop value,
            # lambda function is used with standard parameter set to current loops value.
            # triggeredAction = lambda t=[layer, feature] : self.setSelectionFeature(t[0], feature=t[1], selectAll=selectAll, setActiveLayer=True)
            triggeredAction = partial(
                self.setSelectionFeature,
                layer=layer,
                feature=feature,
                selectAll=selectAll,
                setActiveLayer=True,
            )
            hoveredAction = partial(
                self.createRubberBand, feature=feature, layer=layer, geom=geomType
            )
        elif e.button() == Qt.RightButton:
            selected = QApplication.keyboardModifiers() == Qt.ControlModifier
            if selected:
                triggeredAction = partial(self.iface.setActiveLayer, layer)
                hoveredAction = None
            else:
                triggeredAction = partial(
                    self.iface.openFeatureForm, layer, feature, showModal=False
                )
                hoveredAction = partial(
                    self.createRubberBand, feature=feature, layer=layer, geom=geomType
                )
        return triggeredAction, hoveredAction

    def getCallbackMultipleFeatures(self, e, dictLayerFeature, selectAll=True):
        """
        Sets the callback of an action with a list features as target.
        :param e: (QMouseEvent) mouse event on canvas.
        :param dictLayerFeature: (dict) dictionary containing layers/features to be treated.
        :return: (tuple-of function_lambda) callbacks for triggered and hovered signals.
        """
        # setting the action for the "All" options
        if e.button() == Qt.LeftButton:
            triggeredAction = partial(
                self.setSelectionListFeature,
                dictLayerFeature=dictLayerFeature,
                selectAll=selectAll,
            )
        else:
            triggeredAction = partial(
                self.openMultipleFeatureForm, dictLayerFeature=dictLayerFeature
            )
        # to trigger "Hover" signal on QMenu for the multiple options
        hoveredAction = partial(
            self.createMultipleRubberBand, dictLayerFeature=dictLayerFeature
        )
        return triggeredAction, hoveredAction

    def createSubmenu(self, e, parentMenu, menuDict, genericAction, selectAll):
        """
        Creates a submenu in a given parent context menu and populates it, with classes/feature sublevels from the menuDict.
        :param e: (QMouseEvent) mouse event on canvas. If menuDict has only 1 class in it, method will populate parent QMenu.
        :param parentMenu: (QMenu) menu containing the populated submenu
        :param menuDict: (dict) dictionary containing all classes and their features to be filled into submenu.
        :param genericAction: (str) text to be shown into generic action description on the outter level of submenu.
        :return: (dict) mapping of classes and their own QMenu object.
        """
        # creating a dict to handle all "menu" for each class
        submenuDict = dict()
        # sort the layers from diciotnary
        classIdDict = {cl.id(): cl for cl in menuDict}
        for classId, cl in classIdDict.items():
            # menu for features of each class
            className = cl.name()
            geomType = cl.geometryType()
            # get layer database name
            dsUri = cl.dataProvider().dataSourceUri()
            temp = []
            if "/" in dsUri or "\\" in dsUri:
                db_name = dsUri.split("|")[0] if "|" in dsUri else dsUri
                db_name = os.path.basename(
                    db_name.split("'")[1] if "'" in db_name else db_name
                )
            elif "memory" in dsUri:
                db_name = self.tr(f"{cl.name()} (Memory Layer)")
            else:
                db_name = dsUri.split("'")[1]
            if len(menuDict) == 1:
                # if dictionaty has only 1 class, no need for an extra QMenu - features will be enlisted directly
                # order features by ID to be displayer ordered
                featDict = {feat.id(): feat for feat in menuDict[cl]}
                orderedFeatIdList = sorted(list(featDict.keys()))
                for featId in orderedFeatIdList:
                    feat = featDict[featId]
                    s = f"{db_name} | {className} (feat_id = {featId})"
                    # inserting action for each feature
                    action = parentMenu.addAction(s)
                    triggeredAction, hoveredAction = self.getCallback(
                        e=e,
                        layer=cl,
                        feature=feat,
                        geomType=geomType,
                        selectAll=selectAll,
                    )
                    self.addCallBackToAction(
                        action=action,
                        onTriggeredAction=triggeredAction,
                        onHoveredAction=hoveredAction,
                    )
                # inserting generic action, if necessary
                if len(menuDict[cl]) > 1:
                    # if there are more than 1 feature to be filled, "All"-command should be added
                    action = parentMenu.addAction(
                        self.tr("{0} from layer {1}").format(genericAction, className)
                    )
                    triggeredAction, hoveredAction = self.getCallbackMultipleFeatures(
                        e=e, dictLayerFeature=menuDict, selectAll=selectAll
                    )
                    self.addCallBackToAction(
                        action=action,
                        onTriggeredAction=triggeredAction,
                        onHoveredAction=hoveredAction,
                    )
                # there is no mapping of class to be exposed, only information added to parent QMenu itself
                return dict()
            title = f"{db_name} | {className}"
            submenuDict[cl] = QMenu(title=title, parent=parentMenu)
            parentMenu.addMenu(submenuDict[cl])
            # inserting an entry for every feature of each class in its own context menu
            # order features by ID to be displayer ordered
            featDict = {feat.id(): feat for feat in menuDict[cl]}
            orderedFeatIdList = sorted(list(featDict.keys()))
            for featId in orderedFeatIdList:
                feat = featDict[featId]
                s = "feat_id = {0}".format(featId)
                action = submenuDict[cl].addAction(s)
                triggeredAction, hoveredAction = self.getCallback(
                    e=e, layer=cl, feature=feat, geomType=geomType, selectAll=selectAll
                )
                self.addCallBackToAction(
                    action=action,
                    onTriggeredAction=triggeredAction,
                    onHoveredAction=hoveredAction,
                )
                # set up list for the "All"-commands
                temp.append([cl, feat, geomType])
            # adding generic action for each class
            if len(menuDict[cl]) > 1:
                # if there are more than 1 feature to be filled, "All"-command should be added
                action = submenuDict[cl].addAction(
                    self.tr("{0} from layer {1}").format(genericAction, className)
                )
                triggeredAction, hoveredAction = self.getCallbackMultipleFeatures(
                    e=e, dictLayerFeature={cl: menuDict[cl]}, selectAll=selectAll
                )
                self.addCallBackToAction(
                    action=action,
                    onTriggeredAction=triggeredAction,
                    onHoveredAction=hoveredAction,
                )
        return submenuDict

    def setContextMenuStyle(self, e, dictMenuSelected, dictMenuNotSelected):
        """
        Defines how many "submenus" the context menu should have.
        There are 3 context menu scenarios to be handled:
        :param e: (QMouseEvent) mouse event on canvas.
        :param dictMenuSelected: (dict) dictionary of classes and its selected features being treatead.
        :param dictMenuNotSelected: (dict) dictionary of classes and its non selected features being treatead.
        """
        # finding out filling conditions
        selectedDict = bool(dictMenuSelected)
        notSelectedDict = bool(dictMenuNotSelected)
        # finding out if one of either dictionaty are filled ("Exclusive or")
        selectedXORnotSelected = selectedDict != notSelectedDict
        # setting "All"-command name
        if e.button() == Qt.RightButton:
            genericAction = self.tr("Open All Feature Forms")
        else:
            genericAction = self.tr("Select All Features")
        # in case one of given dict is empty
        if selectedXORnotSelected:
            if selectedDict:
                menuDict, menu = dictMenuSelected, QMenu(
                    title=self.tr("Selected Features")
                )
                genericAction = self.tr("Deselect All Features")
                # if the dictionary is from selected features, we want commands to be able to deselect them
                selectAll = False
            else:
                menuDict, menu = dictMenuNotSelected, QMenu(
                    title=self.tr("Not Selected Features")
                )
                genericAction = self.tr("Select All Features")
                # if the dictionary is from non-selected features, we want commands to be able to select them
                selectAll = True
            if e.button() == Qt.RightButton:
                genericAction = self.tr("Open All Feature Forms")
            self.createSubmenu(
                e=e,
                parentMenu=menu,
                menuDict=menuDict,
                genericAction=genericAction,
                selectAll=selectAll,
            )
            if len(menuDict) != 1 and len(list(menuDict.values())) > 1:
                # if there's only one class, "All"-command is given by createSubmenu method
                action = menu.addAction(genericAction)
                triggeredAction, hoveredAction = self.getCallbackMultipleFeatures(
                    e=e, dictLayerFeature=menuDict, selectAll=selectAll
                )
                self.addCallBackToAction(
                    action=action,
                    onTriggeredAction=triggeredAction,
                    onHoveredAction=hoveredAction,
                )
        elif selectedDict:
            # if both of them is empty one more QMenu level is added
            menu = QMenu()
            selectedMenu = QMenu(title=self.tr("Selected Features"))
            notSelectedMenu = QMenu(title=self.tr("Not Selected Features"))
            menu.addMenu(selectedMenu)
            menu.addMenu(notSelectedMenu)
            selectedGenericAction = self.tr("Deselect All Features")
            notSelectedGenericAction = self.tr("Select All Features")
            # selectAll is set to True as now we want command to Deselect Features in case they are selected
            self.createSubmenu(
                e=e,
                parentMenu=selectedMenu,
                menuDict=dictMenuSelected,
                genericAction=selectedGenericAction,
                selectAll=False,
            )
            if len(dictMenuSelected) != 1 and len(list(dictMenuSelected.values())) > 1:
                # if there's only one class, "All"-command is given by createSubmenu method
                action = selectedMenu.addAction(selectedGenericAction)
                triggeredAction, hoveredAction = self.getCallbackMultipleFeatures(
                    e=e, dictLayerFeature=dictMenuSelected, selectAll=False
                )
                self.addCallBackToAction(
                    action=action,
                    onTriggeredAction=triggeredAction,
                    onHoveredAction=hoveredAction,
                )
            self.createSubmenu(
                e=e,
                parentMenu=notSelectedMenu,
                menuDict=dictMenuNotSelected,
                genericAction=notSelectedGenericAction,
                selectAll=True,
            )
            if (
                len(dictMenuNotSelected) != 1
                and len(list(dictMenuNotSelected.values())) > 1
            ):
                # if there's only one class, "All"-command is given by createSubmenu method
                action = notSelectedMenu.addAction(notSelectedGenericAction)
                triggeredAction, hoveredAction = self.getCallbackMultipleFeatures(
                    e=e, dictLayerFeature=dictMenuNotSelected, selectAll=True
                )
                self.addCallBackToAction(
                    action=action,
                    onTriggeredAction=triggeredAction,
                    onHoveredAction=hoveredAction,
                )
        menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))

    def checkSelectedFeaturesOnDict(self, menuDict):
        """
        Checks all selected features from a given dictionary ( { (QgsVectorLayer)layer : [ (QgsFeature)feat ] } ).
        :param menuDict: (dict) dictionary with layers and their features to be analyzed.
        :return: (tuple-of-dict) both dictionaries of selected and non-selected features of each layer.
        """
        selectedFeaturesDict, notSelectedFeaturesDict = dict(), dict()
        for cl, features in menuDict.items():
            selectedFeats = [f.id() for f in cl.selectedFeatures()]
            for feat in features:
                if feat.id() in selectedFeats:
                    if cl not in selectedFeaturesDict:
                        selectedFeaturesDict[cl] = [feat]
                    else:
                        selectedFeaturesDict[cl].append(feat)
                else:
                    if cl not in notSelectedFeaturesDict:
                        notSelectedFeaturesDict[cl] = [feat]
                    else:
                        notSelectedFeaturesDict[cl].append(feat)
        return selectedFeaturesDict, notSelectedFeaturesDict

    def addRasterMenu(self, menu, rasters):
        rasterMenu = QMenu(title="Rasters", parent=menu)
        for raster in rasters:
            action = rasterMenu.addAction(raster.name())
            action.triggered.connect(lambda: self.iface.setActiveLayer(raster))
        menu.addMenu(rasterMenu)

    def createContextMenu(self, e):
        """
        Creates the context menu for overlapping layers.
        :param e: mouse event caught from canvas.
        """
        selected = QApplication.keyboardModifiers() == Qt.ControlModifier
        if selected:
            firstGeom = self.checkSelectedLayers()
        # setting a list of features to iterate over
        layerList = self.getPrimitiveDict(
            e,
            hasControlModifier=selected,
            hasAltModifier=QApplication.keyboardModifiers() == Qt.AltModifier,
        )
        layers = []
        for key in layerList:
            layers += layerList[key]
        if not layers:
            return
        rect = self.getCursorRect(e)
        lyrFeatDict = dict()
        for layer in layers:
            if not isinstance(layer, QgsVectorLayer):
                continue
            geomType = layer.geometryType()
            # iterate over features inside the mouse bounding box
            bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
            for feature in layer.getFeatures(QgsFeatureRequest(bbRect)):
                geom = feature.geometry()
                if not geom:
                    continue
                searchRect = self.geometryHandler.reprojectSearchArea(layer, rect)
                if selected:
                    # if Control was held, appending behaviour is different
                    if not firstGeom:
                        firstGeom = geomType
                    elif firstGeom > geomType:
                        firstGeom = geomType
                    if geomType == firstGeom and geom.intersects(searchRect):
                        # only appends features if it has the same geometry as first selected feature
                        if layer in lyrFeatDict:
                            lyrFeatDict[layer].append(feature)
                        else:
                            lyrFeatDict[layer] = [feature]
                else:
                    if not geom.intersects(searchRect):
                        continue
                    if layer in lyrFeatDict:
                        lyrFeatDict[layer].append(feature)
                    else:
                        lyrFeatDict[layer] = [feature]
        lyrFeatDict = self.filterStrongestGeometry(lyrFeatDict)
        if not lyrFeatDict:
            return
        moreThanOneFeat = (
            len(list(lyrFeatDict.values())) > 1
            or len(list(lyrFeatDict.values())[0]) > 1
        )
        if moreThanOneFeat:
            # if there are overlapping features (valid candidates only)
            (
                selectedFeaturesDict,
                notSelectedFeaturesDict,
            ) = self.checkSelectedFeaturesOnDict(menuDict=lyrFeatDict)
            self.setContextMenuStyle(
                e=e,
                dictMenuSelected=selectedFeaturesDict,
                dictMenuNotSelected=notSelectedFeaturesDict,
            )
        else:
            layer = list(lyrFeatDict.keys())[0]
            feature = lyrFeatDict[layer][0]
            selected = QApplication.keyboardModifiers() == Qt.ControlModifier
            if e.button() == Qt.LeftButton:
                # if feature is selected, we want it to be de-selected
                self.setSelectionFeature(
                    layer=layer,
                    feature=feature,
                    selectAll=False,
                    setActiveLayer=True,
                )
            elif selected:
                self.iface.setActiveLayer(layer)
            else:
                self.iface.openFeatureForm(layer, feature, showModal=False)

    def unload(self):
        self.deactivate()
