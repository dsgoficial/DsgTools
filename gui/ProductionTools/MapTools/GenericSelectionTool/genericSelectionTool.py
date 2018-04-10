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
from builtins import range
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import Qgis, QgsPointXY, QgsRectangle, QgsMapLayer, QgsFeatureRequest, QgsVectorLayer, QgsDataSourceUri, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsGeometry, QgsWkbTypes, QgsProject
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QMenu

import numpy as np
from qgis.PyQt.QtCore import Qt
from functools import partial

class GenericSelectionTool(QgsMapTool):
    finished = QtCore.pyqtSignal(list)
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
        mFillColor = QColor( 254, 178, 76, 63 )
        self.rubberBand.setColor(mFillColor)
        self.hoverRubberBand.setColor(QColor( 255, 0, 0, 90 ))
        self.rubberBand.setWidth(1)
        self.reset()
        self.blackList = self.getBlackList()
        self.cursorChanged = False
        self.cursorChangingHotkey = QtCore.Qt.Key_Alt
        self.menuHovered = False # indicates hovering actions over context menu
    
    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + '/genericSelect.png'
        toolTip = self.tr("DSGTools: Generic Selector\nLeft Click: select feature's layer and put it on edit mode\nRight Click: Open feature's form\nControl+Left Click: add/remove feature from selection\nShift+Left Click+drag and drop: select all features that intersects rubberband.")
        manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Generic Selector'),
            callback=callback,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar =parentMenu,
            isCheckable = True
        )
    
    def keyPressEvent(self, e):
        """
        Reimplemetation of keyPressEvent() in order to handle cursor changing hotkey (Alt).
        """
        if e.key() == self.cursorChangingHotkey and not self.cursorChanged:
            self.cursorChanged = True
            QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.cursorChanged = False
            QtWidgets.QApplication.restoreOverrideCursor()
    
    def getBlackList(self):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        valueList = settings.value('valueList')
        if valueList:
            valueList = valueList.split(';')
            return valueList
        else:
            return ['moldura']
    
    def reset(self):
        """
        Resets rubber band.
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
    
    def keyPressEvent(self, e):
        """
        Reimplemetation of keyPressEvent() in order to handle cursor changing hotkey (F2).
        """
        if e.key() == self.cursorChangingHotkey and not self.cursorChanged:
            self.cursorChanged = True
            QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.cursorChanged = False
            QtWidgets.QApplication.restoreOverrideCursor()         

    def canvasMoveEvent(self, e):
        """
        Used only on rectangle select.
        """
        if self.menuHovered:
            # deactivates rubberband when the context menu is "destroyed" 
            self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates( e.pos() )
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
        self.rubberBand.addPoint(point4, True)    # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        """
        Builds rectangle from self.startPoint and self.endPoint
        """
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None
        return QgsRectangle(self.startPoint, self.endPoint)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
    
    def canvasReleaseEvent(self, e):
        """
        After the rectangle is built, here features are selected.
        """
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            firstGeom = self.checkSelectedLayers()
            self.isEmittingPoint = False
            r = self.rectangle()
            if r is None:
                return
            layers = self.canvas.layers()
            for layer in layers:
                #ignore layers on black list and features that are not vector layers
                if not isinstance(layer, QgsVectorLayer) or (self.layerHasPartInBlackList(layer.name())):
                    continue
                if firstGeom is not None and layer.geometryType() != firstGeom:
                    # if there are features already selected, shift will only get the same type geometry
                    # if more than one ty of geometry is present, only the strongest will be selected
                    continue
                #builds bbRect and select from layer, adding selection
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, r)
                layer.selectByRect(bbRect, behavior = QgsVectorLayer.AddToSelection)
            self.rubberBand.hide()

    def canvasPressEvent(self, e):
        """
        Method used to build rectangle if shift is held, otherwise, feature select/deselect and identify is done.
        """
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
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
        return QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
    
    def layerHasPartInBlackList(self, lyrName):
        """
        Verifies if terms in black list appear on lyrName
        """
        for item in self.getBlackList():
            if item.lower() in lyrName.lower():
                return True
        return False
    
    def getPrimitiveDict(self, e, hasControlModifyer=False):
        """
        Builds a dict with keys as geometryTypes of layer, which are Qgis.Point (value 0), Qgis.Line (value 1) or Qgis.Polygon (value 2),
        and values as layers from self.iface.mapCanvas().layers(). When self.iface.mapCanvas().layers() is called, a list of
        layers ordered according to lyr order in TOC is returned.
        """
        #these layers are ordered by view order
        primitiveDict = dict()
        firstGeom = self.checkSelectedLayers()
        visibleLayers = QgsProject.instance().layerTreeRoot().checkedLayers()
        for lyr in self.iface.mapCanvas().layers(): #ordered layers
            #layer types other than VectorLayer are ignored, as well as layers in black list and layers that are not visible
            if (lyr.type() != QgsMapLayer.VectorLayer) or (self.layerHasPartInBlackList(lyr.name())) or lyr not in visibleLayers:
                continue
            if hasControlModifyer and (not firstGeom) and (not list(primitiveDict.keys()) or lyr.geometryType() < firstGeom):
                firstGeom = lyr.geometryType()
            geomType = lyr.geometryType()
            if geomType not in list(primitiveDict.keys()):
                primitiveDict[geomType] = []
            #removes selection
            if (not hasControlModifyer and e.button() == QtCore.Qt.LeftButton) or (hasControlModifyer and e.button() == QtCore.Qt.RightButton):
                lyr.removeSelection()
            primitiveDict[geomType].append(lyr)
        if hasControlModifyer and firstGeom in [0, 1, 2]:
            return { firstGeom : primitiveDict[firstGeom] }
        else:
            return primitiveDict

    def selectFeatures(self, e, bbRect=None, hasControlModifyer=False):
        """
        Method to select features acoording to mouse event e.
        Optional parameters:
        bbRect: if supplied, other rectangle is used
        hasControlModifyer: used to add to selection or not.
        """
        rect = self.getCursorRect(e)
        primitiveDict = self.getPrimitiveDict(e, hasControlModifyer = hasControlModifyer)
        primitives = list(primitiveDict.keys())
        primitives.sort() #this sort enables search to be done in the order of Point (value 0), Line (value 1) and Polygon (value 2)
        for primitive in primitives:
            for lyr in primitiveDict[primitive]:
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(lyr, rect)
                for feat in lyr.getFeatures(QgsFeatureRequest(bbRect)):
                    selectedIds = lyr.selectedFeatureIds() #list of selected ids
                    featGeom = feat.geometry()
                    if not featGeom:
                        continue
                    if featGeom.intersects(bbRect): #tests if feature intersects tool bounding box, otherwise skip it
                        lyr.startEditing() #starts layer editting
                        if e.button() == QtCore.Qt.RightButton:
                            #set target, start edit and stop
                            if hasControlModifyer:
                                #sets active layer. Since hasControlModifyer indicates to this method to clear selection, this part of
                                #the code completes the  control + right click behaviour.
                                self.iface.setActiveLayer(lyr)
                                return
                            else:
                                #opens feature form. The tag showModal is to lock qgis window or not. 
                                #Current procedure is to imitate qgis way of doing things, so showModal = False
                                self.iface.setActiveLayer(lyr)
                                self.iface.openFeatureForm(lyr,feat, showModal=False)
                                return
                        #if code reaches here, it means that it is an incremental selection.
                        if feat.id() in selectedIds:
                            lyr.modifySelection([],[feat.id()])
                        else:
                            lyr.modifySelection([feat.id()],[])
                        if not hasControlModifyer:
                            x = self.iface.setActiveLayer(lyr)
                            return
                       
    def deactivate(self):
        """
        Deactivate tool.
        """
        QtWidgets.QApplication.restoreOverrideCursor()
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
    
    def openFeatureForm(self, layer, feature):
        self.iface.setActiveLayer(layer)
        self.iface.openFeatureForm(layer, feature, showModal=False)

    def setSelectionFeature(self, layer, feature, selectAll=False):
        """
        Selects a given feature on canvas. 
        :param layer: layer containing the target feature
        :param feature: taget feature to be selected
        :param selectAll: boolean indicating whether or not this fuction was called from a select all command
                          so it doesn't remove selection from those that are selected already from the list
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
        return 

    def setSelectionListFeature(self, listLayerFeature):
        """
        Selects all features in a given list on canvas.        
        :param listLayerFeature: a list os items as of [layer, feature[, geometry_type]]
        """
        for item in listLayerFeature:
            self.setSelectionFeature(layer=item[0], feature=item[1], selectAll=True)
        return

    def openMultipleFeatureForm(self, listLayerFeature):
        """
        Opens all features Attribute Tables of a given list.
        :param listLayerFeature: a list os items as of [layer, feature[, geometry_type]]
        """
        for item in listLayerFeature:
            self.iface.openFeatureForm(item[0], item[1], showModal=False)

    def filterStrongestGeometry(self, listLayerFeature):
        """
        Filter a given list of features for its strongest geometry
        :param listLayerFeature: a list os items as of [layer, feature, geometry_type]
        :return: a list [layer, feature]
        """
        if listLayerFeature:
            strongest_geometry = np.array(np.array(listLayerFeature)[:,2], 'int').min()
        else:
            return []
        l = []
        for i in listLayerFeature:
            if i[2] == strongest_geometry:
                l.append(i)
        return l
    
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

    def createMultipleRubberBand(self, featureList):
        """
        Creates rubberbands around features.
        :param featureList: a list os items as of [layer, feature, geometry_type]
        """
        geom = featureList[0][2]
        if geom == 0:
            self.hoverRubberBand.reset(QgsWkbTypes.PointGeometry)
        elif geom == 1:
            self.hoverRubberBand.reset(QgsWkbTypes.LineGeometry)
        else:
            self.hoverRubberBand.reset(QgsWkbTypes.PolygonGeometry)
        for item in featureList:
            self.hoverRubberBand.addGeometry(item[1].geometry(), item[0])
        self.menuHovered = True

    def checkSelectedLayers(self):
        """
        Checks if there are layers selected on canvas. If there are, returns the geometry type of
        selected feature(s). If more than one type of feature is selected, the "strongest" geometry
        is returned.
        """
        geom = None
        for layer in self.iface.mapCanvas().layers():
            if isinstance(layer, QgsVectorLayer):
                selection = layer.selectedFeatures()
                if len(selection):
                    if geom == None:
                        geom = layer.geometryType()
                        continue
                    elif layer.geometryType() < geom:
                        geom = layer.geometryType()
                        continue
        return geom
    
    def addActionToMenu(self, action, onTriggeredAction=None, onHoveredAction=None):
        """
        Adds action the command to the action. If onHoveredAction is given, signal "hovered" is applied with given action.
        :param action: QAction associated with target context menu
        :param onTriggeredAction: action to be executed when the given action is triggered
        :param onHoveredAction: action to be executed whilst the given action is hovered
        """
        action.triggered.connect(onTriggeredAction)
        if onHoveredAction:
            action.hovered.connect(onHoveredAction)

    # def createMenuDict(self, featureList):
    #     """
    #     Creates a dictionary ({ (str)Layer_Name : [(int)feature_id] }) from a given list
    #     :param featureList: a list os items as of [layer, feature[, geometry_type]]
    #     """
    #     menuDict = dict()
    #     for item in featureList:
    #         if item[0].name() not in menuDict.keys():
    #             menuDict[item[0].name()] = [item[1].id()]
    #         else:
    #             menuDict[item[0].name()].append(item[1].id())
    #     return menuDict

    # def setContextMenuStyle(self, dictMenuSelected, dictMenuNotSelected):
    #     """
    #     Defines how many "submenus" the context menu should have.
    #     There are 3 context menu scenarios to be handled:
    #     1- both dicts are filled and context menu should have 2 "submenus" - DB.Classes > Selected / Not Selected > Feature IDs;
    #     2- one of them is filled and there are more than 1 class to be enlisted (1 submenu necessary) - DB.Class > Feature IDs; and
    #     3- one of them is filled and there is only one class with features selected - DB.Class (feat_id = NR)
    #     """
    #     # finding out filling conditions
    #     selectedDict = bool(dictMenuSelected)
    #     notSelectedDict = bool(dictMenuNotSelected)
    #     # finding out if one of either dictionaty are filled ("Exclusive or")
    #     selectedXORnotSelected = (selectedDict != notSelectedDict)
    #     # finding out if there is more than one class to be listed on menu
    #     nrClass = max(len(dictMenuSelected), len(dictMenuNotSelected))
    #     # Case 1: 2 submenus to be filled = "3 context menus"
    #     if selectedDict and notSelectedDict:
    #         # setting up menus
    #         menu = QtGui.QMenu()
    #         selectedMenu = QtGui.QAction(self.tr('Selected Features'), menu)
    #         notSelectedMenu = QtGui.QAction(self.tr(''), menu)
    #         # get the list of all classes to be enlisted
    #         classes = dictMenuSelected.keys() + dictMenuNotSelected.keys()
    #         # getting unique classes
    #         classes = list(set(classes))
    #         for cl in classes:
    #             { cl : menu.addAction(cl) }

    def createContextMenu(self, e):
        """
        Creates the context menu for overlapping layers.
        :param e: mouse event caught from canvas.
        """
        selected = (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
        if selected:
            firstGeom = self.checkSelectedLayers()
        # setting a list of features to iterate over
        layerList = self.getPrimitiveDict(e, hasControlModifyer=selected)
        layers = []
        for key in list(layerList.keys()):
            layers += layerList[key]
        if layers:
            menu = QtWidgets.QMenu()
            rect = self.getCursorRect(e)
            t = []
            for layer in layers:
                if not isinstance(layer, QgsVectorLayer):
                    continue
                # iterate over features inside the mouse bounding box
                bbRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)
                for feature in layer.getFeatures(QgsFeatureRequest(bbRect)):
                    geom = feature.geometry()
                    if geom:
                        searchRect = self.reprojectSearchArea(layer, rect)
                        if selected:
                            # if Control was held, appending behaviour is different
                            if not firstGeom or firstGeom > layer.geometryType():
                                firstGeom = layer.geometryType()
                            if geom.intersects(searchRect) and layer.geometryType() == firstGeom:
                                # only appends features if it has the same geometry as first selected feature
                                t.append([layer, feature, layer.geometryType()])
                        else:
                            if geom.intersects(searchRect):
                                t.append([layer, feature, layer.geometryType()])
            t = self.filterStrongestGeometry(t)
            if len(t) > 1:
                pop = 0 # number of features 
                for i in range(0, len(t)):
                    [layer, feature, geom] = t[i-pop] # geom to avoid dimension issues
                    # layers from different dabases may have the same name
                    # hence the need of db_name
                    self.iface.setActiveLayer(layer) # a layer must be active in order to get db_name
                    dsUri = self.iface.activeLayer().dataProvider().dataSourceUri()
                    if '/' in dsUri or '\\' in dsUri:
                        db_name = dsUri
                    else:
                        db_name = self.iface.activeLayer().dataProvider().dataSourceUri().split("'")[1]
                    s = '{0}.{1} (feat_id = {2})'.format(db_name, layer.name(), feature.id())
                    action = menu.addAction(s) # , lambda feature=feature : self.setSelectionFeature(layer, feature))
                    # handling CTRL key and left/right click actions
                    if e.button() == QtCore.Qt.LeftButton: 
                        # line added to make sure the action is associated with current loop value,
                        # lambda function is used with standard parameter set to current loops value.
                        triggeredAction = partial(self.setSelectionFeature, t[i][0], t[i][1])
                        hoveredAction = lambda t=t[i] : self.createRubberBand(feature=t[1], layer=t[0], geom=t[2])
                    elif e.button() == QtCore.Qt.RightButton:
                        if selected:                        
                            triggeredAction = lambda layer=layer : self.iface.setActiveLayer(layer)
                            hoveredAction = None
                            # remove feature from candidates of selection and set layer for selection
                            t.pop(i-pop)
                            pop += 1
                            continue
                        else:
                            triggeredAction = partial(self.iface.openFeatureForm, t[i][0], t[i][1], showModal=False)
                            hoveredAction = lambda t=t[i] : self.createRubberBand(feature=t[1], layer=t[0], geom=t[2])
                    self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
                # setting the action for the "All" options
                if e.button() == QtCore.Qt.LeftButton:
                    action = menu.addAction(self.tr('Select All'))
                    triggeredAction = lambda t=t: self.setSelectionListFeature(t)
                else:
                    action = menu.addAction(self.tr('Open All Attribute Tables'))
                    triggeredAction = lambda t=t: self.openMultipleFeatureForm(t)
                # to trigger "Hover" signal on QMenu for the multiple options
                hoveredAction = lambda t=t : self.createMultipleRubberBand(featureList=t)
                self.addActionToMenu(action=action, onTriggeredAction=triggeredAction, onHoveredAction=hoveredAction)
                menu.exec_(self.canvas.viewport().mapToGlobal(e.pos()))
            elif t:
                t = t[0]
                selected =  (QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)
                if e.button() == QtCore.Qt.LeftButton:
                    self.selectFeatures(e, hasControlModifyer = selected)
                elif selected:
                    self.iface.setActiveLayer(t[0])
                else:
                    self.iface.openFeatureForm(t[0], t[1], showModal=False)

    def reprojectSearchArea(self, layer, geom):
        #geom always have canvas coordinates
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        #getting srid from something like 'EPSG:31983'
        srid = layer.crs().authid()
        if epsg == srid:
            return geom
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        crsDest = QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        auxGeom = QgsGeometry.fromRect(geom)
        auxGeom.transform(coordinateTransformer)
        return auxGeom.boundingBox()
    
    def unload(self):
        self.deactivate()
