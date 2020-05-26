# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2020-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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
from datetime import datetime
from functools import partial
from collections import defaultdict

from qgis.utils import iface
from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, QObject
from qgis.PyQt.QtWidgets import QPushButton, QShortcut, QAction
from qgis.PyQt.QtGui import QIcon, QColor, QPalette, QKeySequence

from DsgTools.core.Utils.utils import Utils
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

utils = Utils()

class CustomFeatureButton(QObject):
    """
    Class designed to handle actions, properties and settings for buttons. It
    includes info about its styling, shortcuts and other user-defined
    characteristics. This object MUST be serializable, since it'll be used for
    data perpetuation and state definition/loading.
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1
    toggled = pyqtSignal(bool)

    def __init__(self, props=None, callback=None):
        """
        Class constructor.
        :param props: (dict) a map to button's properties.
        :param callback: (*) any callable object to be set as callback for the
                         push button event.
        """
        super(CustomFeatureButton, self).__init__()
        self._props = {
            "name": self.tr("New button"),
            "openForm": False,
            "useColor": True,
            "color": (255, 255, 255, 255),
            "tooltip": "",
            "size": QPushButton().font().pointSize(),
            "category": "",
            "shortcut": "",
            "layer": "",
            "keywords": set(),
            "attributeMap": dict(),
            "digitizingTool": "default",
            "isCheckable": False,
            "isChecked": False,
            "isEnabled": False
        }
        self._widgets = list()
        self._callback = callback if callback else lambda: None
        self.setAction()
        self.setProperties(props)
        self.setShortcut(self.shortcut())
        # temp var to handle disabled status
        self.__shortcut = self.shortcut()

    def __eq__(self, obj):
        """
        Method reimplementation for object comparison. This comparison is
        stablished through property comparison, hence buttons that share the
        same set of attributes, even if they are different objects, will return
        when compared for object equality.
        :param obj: (*) any other object that is compared to this instance.
        :return: (bool) whether this is instance is equal to the reference obj.
        """
        if not hasattr(obj, "_props"):
            return False
        return obj._props == self._props

    def __str__(self):
        """
        Method reimplementation for object stringfication.
        :return: (str) stringfied instance.
        """
        return "<DSGTools CustomFeatureButton instance\n{0}>"\
                .format(str(self._props))

    def __hash__(self):
        """
        Method reimplementation for object hashing in order to allow
        CustomFeatureButton as dictionary keys (main reason).
        :return: (int) instance's hash value.
        """
        return hash(str(self))

    def __del__(self):
        """
        Reimplementation of object removal method.
        """
        self.setEnabled(False)
        self._shortcut.activated.disconnect(self.action().trigger)
        self._shortcut.setKey(QKeySequence.fromString(""))
        self._shortcut.setParent(None)
        del self._shortcut
        self.action().blockSignals(True)
        for w in self.widgets():
            w.blockSignals(True)
            w.setParent(None)
            del w
        self.clearWidgets()
        del self._widgets
        del self._action
        self.setParent(None)

    def copy(self):
        """
        Provides a copy of current CustomFeatureButton object.
        :return: (CustomFeatureButton) copy of current's instance.
        """
        b = CustomFeatureButton(self.properties())
        b.setCallback(self._callback)
        return b

    def setProperties(self, props):
        """
        Modify current button properties. Only valid properties are modified.
        :param props: (dict) a map to button's new properties.
        :return: (dict) a map to current button properties.
        """
        if props is not None:
            methodMap = {
                "name": lambda x: self.setName(x),
                "openForm": lambda x: self.setOpenForm(x),
                "useColor": lambda x: self.setUseColor(x),
                "color": lambda x: self.setColor(x),
                "size": lambda x: self.setSize(x),
                "tooltip": lambda x: self.setToolTip(x),
                "category": lambda x: self.setCategory(x),
                "shortcut": lambda x: self.setShortcut(x),
                "layer": lambda x: self.setLayer(x),
                "keywords": lambda x: self.setKeywords(x),
                "attributeMap": lambda x: self.setAttributeMap(x),
                "digitizingTool": lambda x: self.setDigitizingTool(x),
                "isCheckable": lambda x: self.setCheckable(x),
                "isChecked": lambda x: self.setChecked(x),
                "isEnabled": lambda x: self.setEnabled(x)
            }
            for prop, value in props.items():
                if prop in methodMap:
                    methodMap[prop](value)
        return self.properties()

    def update(self, newProps):
        """
        Updates current button properties from a given property map.
        :param newProps: (dict) new properties value map.
        :return: (bool) whether any property value was set from newProps.
        """
        updated = False
        oldProps = self.properties()
        tempButton = CustomFeatureButton(newProps)
        methodMap = {
            "name": lambda x: self.setName(x),
            "openForm": lambda x: self.setOpenForm(x),
            "useColor": lambda x: self.setUseColor(x),
            "color": lambda x: self.setColor(x),
            "size": lambda x: self.setSize(x),
            "tooltip": lambda x: self.setToolTip(x),
            "category": lambda x: self.setCategory(x),
            "shortcut": lambda x: self.setShortcut(x),
            "layer": lambda x: self.setLayer(x),
            "keywords": lambda x: self.setKeywords(x),
            "attributeMap": lambda x: self.setAttributeMap(x),
            "digitizingTool": lambda x: self.setDigitizingTool(x),
            "isCheckable": lambda x: self.setCheckable(x),
            "isChecked": lambda x: self.setChecked(x),
            "isEnabled": lambda x: self.setEnabled(x)
        }
        try:
            for propName, propValue in tempButton.properties().items():
                if propName in newProps and propValue == newProps[propName]:
                    # only non-defaulted values will be applied to the button
                    methodMap[propName](propValue)
                    updated = True
        except Exception as e:
            # reset previous props and re-raise the error message
            self.update(oldProps)
            updated = False
            raise Exception(self.tr("Error while updating '{0}' ({1})")\
                                .format(propName, str(e)))
        return updated

    def properties(self):
        """
        Retrieves button's properties.
        :return: (dict) a map to current button properties.
        """
        # methods should return a copy of value entry in order for it no to be
        # accidentally modified
        return {
            "name": self.name(),
            "openForm": self.openForm(),
            "useColor": self.useColor(),
            "color": self.color(),
            "size": self.size(),
            "tooltip": self.toolTip(),
            "category": self.category(),
            "layer": self.layer(),
            "shortcut": self.shortcut(),
            "keywords": self.keywords(),
            "attributeMap": self.attributeMap(),
            "digitizingTool": self.digitizingTool(),
            "isCheckable": self.isCheckable(),
            "isChecked": self.isChecked(),
            "isEnabled": self.isEnabled()
        }

    def widget(self):
        """
        This instance's widget configured with current defined properties. It's
        an alias for newWidget method.
        :return: (QPushButton) current widget.
        """
        return self.newWidget()

    def widgets(self):
        """
        All created widgets from this custom button is tracked from a list.
        These widgets might be deleted from the interface and Python reference
        is kept even though the C++ object is removed. This method "clears" the
        list every time it is called.
        :return: (list-of-QPushButton) all valid managed buttons.
        """
        newList = list()
        for b in self._widgets:
            try:
                b.objectName() # any calls to invalids them raises errors here
                newList.append(b)
            except RuntimeError:
                # invalid buttons shall raise the lost reference error
                pass
        del self._widgets
        self._widgets = newList
        return self._widgets

    def clearWidgets(self):
        """
        Clears all registered widgets for a given button. This method should be
        carefully used as it might simply remove the reference to a set of
        managed widgets and not propagating button properties updates to them.
        :param name: (str) name for the button to have its wigdets references
                     cleaned.
        """
        while self._widgets:
            self._widgets.pop()

    def newWidget(self):
        """
        A new instance of widget configured with current defined properties.
        :return: (QPushButton) new instance of a widget with current defined
                 properties.
        """
        pb = QPushButton()
        pb.setCheckable(self.isCheckable())
        pb.toggled.connect(self.setChecked)
        pb.toggled.connect(self.toggled)
        pb.setChecked(self.isChecked())
        if not self.isCheckable():
            pb.clicked.connect(self.action().trigger)
        pb.setText(self.displayName())
        pb.setToolTip(self.toolTip())
        pal = QPalette()
        if self.useColor():
            col = self.color()
            if isinstance(col, str):
                col = QColor(col)
            else:
                col = QColor(*col)
            pal.setColor(pal.Button, col)
        pb.setPalette(pal)
        font = pb.font()
        font.setPointSize(self.size())
        pb.setFont(font)
        pb.update()
        # keeping track of all created widgets is necessary in order to update
        # accordingly to CustomFeatureButton's properties
        self._widgets.append(pb)
        return pb

    def setName(self, name):
        """
        Defines button's name, which is used to compose the display name.
        :param name: (str) button's name.
        """
        if type(name) == str: 
            self._props["name"] = name
            for w in self.widgets():
                w.setText(self.displayName())
                w.update()
            if hasattr(self, "_action"):
                self.action().setText(
                    self.tr("DSGTools: Custom Feature Toolbox - button {0}")\
                        .format(self.name())
                )
        else:
            raise TypeError(
                self.tr("Policy must be a str ({0}).").format(type(name))
            )

    def name(self):
        """
        Retrives button's name.
        :return: (str) button's name.
        """
        return str(self._props["name"])

    def displayName(self):
        """
        Retrives button's display text (the one which will be exposed on GUI).
        """
        if self.shortcut():
            return "{0} [{1}]".format(self.name(), self.shortcut())
        return self.name()

    def setOpenForm(self, policy):
        """
        Defines whether current button suppresses feature form.
        :param policy: (bool) whether form should be displayed.
        """
        if type(policy) == bool: 
            self._props["openForm"] = policy
        else:
            raise TypeError(
                self.tr("Policy must be a boolean ({0}).").format(type(policy))
            )

    def openForm(self):
        """
        Retrieves current form displaying policy.
        :return: (bool) whether form is set to be displayed.
        """
        return bool(self._props["openForm"])

    def setColor(self, color):
        """
        Defines button color.
        :param color: (str) button's color.
        """
        if type(color) in (str, tuple): 
            self._props["color"] = color
            if self.useColor():
                pal = QPalette()
                col = self.color()
                if isinstance(col, str):
                    col = QColor(col)
                else:
                    col = QColor(*col)
                pal.setColor(pal.Button, col)
                for w in self.widgets():
                    w.setPalette(pal)
                    w.update()
        else:
            raise TypeError(
                self.tr("Color must be a str or tuple of int ({0}).")\
                    .format(type(color))
            )

    def color(self):
        """
        Button's color.
        :return: (str/tuple-of-int) button's color.
        """
        c = self._props["color"]
        if isinstance(c, str):
            c = str(c)
        else:
            c = tuple([n for n in c])
        return c

    def setUseColor(self, useColor):
        """
        Sets if widget will use defined color or QGIS default palette.
        :param useColor: (bool) whether custom color will be applied.
        """
        if type(useColor) == bool: 
            self._props["useColor"] = useColor
            if not useColor:
                for w in self.widgets():
                    w.setPalette(QPalette())
            else:
                self.setColor(self.color())
        else:
            raise TypeError(
                self.tr("Color usage must be a bool ({0}).")\
                    .format(type(useColor))
            )

    def useColor(self):
        """
        Checks if widget will use a custom coloring palette or the default one.
        :return: (bool) whether custom color will be applied.
        """
        return bool(self._props["useColor"])

    def setSize(self, size):
        """
        Defines displaying text's font size on the widget.
        :param size: (int) text's font size in pixels.
        """
        if type(size) == int: 
            self._props["size"] = size
            for w in self.widgets():
                # setSize in here
                font = w.font()
                font.setPointSize(size)
                w.setFont(font)
                w.update()
        else:
            raise TypeError(
                self.tr("Category must be an int ({0}).").format(type(size))
            )

    def size(self):
        """
        Retrieves displaying text's font size on the widget.
        :return: (int) text's size in pixels.
        """
        return int(self._props["size"])

    def setToolTip(self, tooltip):
        """
        Defines button tool tip text.
        :param tooltip: (str) button's tool tip text.
        """
        if type(tooltip) == str: 
            self._props["tooltip"] = tooltip
            for w in self.widgets():
                w.setToolTip(tooltip)
        else:
            raise TypeError(
                self.tr("Tool tip must be a str ({0}).").format(type(tooltip))
            )

    def toolTip(self):
        """
        Button's tool tip text.
        :return: (str) button's tool tip text.
        """
        return str(self._props["tooltip"])

    def setCategory(self, cat):
        """
        Sets button's category property, which is used for button grouping.
        :param cat: (str) button's tool tip text.
        """
        if type(cat) == str: 
            self._props["category"] = cat
        else:
            raise TypeError(
                self.tr("Category must be a str ({0}).").format(type(cat))
            )

    def category(self):
        """
        Property used for button grouping.
        :return: (str) button's tool tip text.
        """
        return str(self._props["category"])

    def setShortcut(self, s):
        """
        Sets button's action shortcut.
        :param s: (str) button's action shortcut.
        """
        if type(s) == str: 
            self._props["shortcut"] = s
            self.__shortcut = s
            sKeySeq = QKeySequence.fromString(s)
            self._shortcut.setKey(sKeySeq)
            for w in self.widgets():
                w.setText(self.displayName())
                w.update()
        else:
            raise TypeError(
                self.tr("Action shortcut must be a str ({0}).").format(type(s))
            )

    def shortcut(self):
        """
        Retrieves button's action shortcut.
        :return: (str) button's action shortcut.
        """
        return str(self._props["shortcut"])

    def shortcutId(self):
        """
        This object's shortcut (QShortcut) may be used for its own callback and
        identifying the button from it may be requested. This method provides
        this button instance's shortcut object identifier.
        :return: (int) shortcut's object identifier.
        """
        return self._shortcut.id()

    def addKeyword(self, kw):
        """
        Adds a keyword to button's keywords set.
        :param kw: (str) keyword to be added.
        """
        if type(kw) == str: 
            self._props["keywords"].add(kw)
        else:
            raise TypeError(
                self.tr("Keyword must be a str ({0}).").format(type(kw))
            )

    def addKeywords(self, kws):
        """
        Adds a set of keywords to the current keyword set.
        :param kws: (set) set of keywords to be added.
        """
        if type(kws) == set: 
            self._props["keywords"] |= kws
        else:
            raise TypeError(
                self.tr("Keyword must be a set ({0}).").format(type(kws))
            )

    def removeKeyword(self, kw):
        """
        Removes a keyword from button's keywords set.
        :param kw: (str) keyword to be removed.
        """
        self._props["keywords"].discard(kw)

    def setKeywords(self, kws):
        """
        Replaces button's registered keywords.
        :param kws: (set) button's new keywords.
        """
        if type(kws) == set: 
            self._props["keywords"] = kws
        else:
            raise TypeError(
                self.tr("Keyword must be a set ({0}).").format(type(kws))
            )

    def keywords(self):
        """
        Retrieves button's registered keywords.
        :return: (set) button's keywords.
        """
        return set(self._props["keywords"])

    def checkKeyword(self, word, checkShortcut=False):
        """
        Checks if a given word is among button's keywords or name. It may look
        into shortcut as well.
        :word: (str) word to be checked.
        :param checkShortcut: (bool) whether word should be matched to shortcut
                              as well.
        :return: (bool) whether word is found among button's metadata.
        """
        word = word.lower().strip()
        if word in self.name().lower():
            return True
        if word in self.layer().lower():
            return True
        for kw in self.keywords():
            if word in kw.lower():
                return True
        if checkShortcut and word in self.shortcut().lower().replace(" ", ""):
            # this ignores spacing - 'Alt+R' = 'Alt + R'
            return True
        return False

    def setCallback(self, callback=None):
        """
        Sets callback to be triggered whenever button is pushed.
        :param callback: (*) any callable object.
        """
        if callback is None:
            callback = lambda: None
        if not callable(callback):
            raise Exception(self.tr("Callback must be a callable object."))
        if self.callbackIsConnected():
            self.action().triggered.disconnect(self._callback)
        def callbackWrapper():
            if self.isEnabled():
                callback()
        self._callback = callbackWrapper
        self.action().triggered.connect(self._callback)
        self.__callbackConnected = True

    def setAction(self):
        """
        Sets callback to be triggered whenever button is pushed.
        """
        self._action = QAction()
        self._action.setText(
            self.tr("DSGTools: Custom Feature Toolbox - button {0}")\
                .format(self.name())
        )
        self._action.setIcon(
            QIcon(':/plugins/DsgTools/icons/customFeatureToolBox.png')
        )
        self._shortcut = QShortcut(iface.mainWindow())
        self._shortcut.setContext(Qt.ApplicationShortcut)
        sKeySeq = QKeySequence.fromString(self.shortcut())
        self._action.setShortcut(sKeySeq)
        self._shortcut.setKey(sKeySeq)
        self._shortcut.activated.connect(self.action().trigger)
        if self.isEnabled():
            iface.registerMainWindowAction(self._action, self.shortcut())
        self._action.triggered.connect(self._callback)
        self.__callbackConnected = True

    def action(self):
        """
        Gets the QAction associated with the button push event.
        :return: (QAction) current action.
        """
        return self._action

    def callbackIsConnected(self):
        """
        Identifies if callback is currently connected to action trigger signal.
        :return: (bool) whether callback is connected to action.
        """
        return bool(self.__callbackConnected)

    def handleActionCallback(self):
        """
        Checks button behaviour and connects or disconnects callback from
        action accordingly. Action may trigger the callback when:
        1- button is not checkable;
        2- button is checkable and it is currently checked
        """
        if self.isCheckable():
            if self.isChecked() and not self.callbackIsConnected():
                self.action().triggered.connect(self._callback)
                self.__callbackConnected = True
            elif not self.isChecked() and self.callbackIsConnected():
                self.action().triggered.disconnect(self._callback)
                self.__callbackConnected = False
        elif not self.callbackIsConnected():
            self.action().triggered.connect(self._callback)
            self.__callbackConnected = True

    def setShortcutCallback(self, callback=None):
        """
        Button may be used in a toggled mode and a callback might be associated
        with the event of shortcur triggering despite of button's action
        callback. This method sets a callable to be triggered on button's 
        shortcut triggering event.
        :param callback: (callable) any callable object to be triggered.
        """
        if callback is None:
            callback = lambda: None
        if not callable(callback):
            raise Exception(self.tr("Callback must be a callable object."))
        def callbackWrapper():
            if self.isEnabled():
                callback()
        try:
            self._shortcut.activated.disconnect(self._sCallback)
        except:
            pass
        self._sCallback = callbackWrapper
        self._shortcut.activated.connect(self._sCallback)

    def setLayer(self, layer):
        """
        Updates target layer name property.
        :param layer: (str) new layer name to be worked on.
        """
        if type(layer) == str: 
            self._props["layer"] = layer
        else:
            raise TypeError(
                self.tr("Layer name must be a str ({0}).").format(type(layer))
            )

    def layer(self):
        """
        Name for the layer that will be targeted for button's reclassification
        or feature creation.
        :return: (str) name for the layer to be used.
        """
        return str(self._props["layer"])

    def vectorLayer(self):
        """
        Reads the vector layer object from canvas using the layer property.
        :return: (str) name for the layer to be used.
        """
        vl = QgsProject.instance().mapLayersByName(self.layer())
        return vl[0] if vl else None

    def checkLayer(self):
        """
        Checks whether current layer is loaded on canvas.
        :return: (bool) whether layer is found on canvas.
        """
        return self.vectorLayer() is not None

    def valueMaps(self):
        """
        Retrieves value maps for currently selected layer.
        :return: (dict) object that maps each field from selected layer to its
                 value map.
        """
        if self.checkLayer():
            return LayerHandler().valueMaps(self.vectorLayer())
        return dict()

    def setAttributeMap(self, attrMap):
        """
        Updates the attribute map for output features on reclassification or
        feature creation.
        :param attrMap: (str) new attribute map.
        """
        prevAttrMap = self.attributeMap()
        if type(attrMap) == dict:
            if self.checkLayer():
                fMap = self.valueMaps()
                vl = self.vectorLayer()
                fields = vl.fields()
                pkIdxList = vl.primaryKeyAttributes()
                for field in fields:
                    fieldName = field.name()
                    if fieldName not in attrMap:
                        self._props["attributeMap"][fieldName] = {
                            "value": None,
                            "editable": True,
                            "ignored": True,
                            "isPk": fields.lookupField(fieldName) in pkIdxList
                        }
                        continue
                    value = attrMap[fieldName]["value"]
                    if fieldName in fMap and value is not None \
                       and value not in fMap[fieldName].values():
                        self._props["attributeMap"] = prevAttrMap
                        raise ValueError(
                            self.tr("{0} is not a valid value for field {1}.")\
                                .format(value, fieldName)
                        )
                    self._props["attributeMap"][fieldName] = {
                        "value": value,
                        "editable": attrMap[fieldName]["editable"],
                        "ignored": attrMap[fieldName]["ignored"],
                        "isPk": fields.lookupField(fieldName) in pkIdxList
                    }
            else:
                # for now, attribute is not validated layer is not provided
                self._props["attributeMap"] = attrMap
        else:
            raise TypeError(
                self.tr("Attribute map must be a dict ({0}).")\
                    .format(type(attr))
            )

    def attributeMap(self):
        """
        Attribute map for output features on reclassification or feature
        creation.
        :return: (dict) attribute map for new/updated features.
        """
        return dict(self._props["attributeMap"])

    def supportedTools(self):
        """
        A map from supported feature extraction tools to their user-friendly
        names. 
        """
        return {
            "default": self.tr("QGIS default feature extraction tool"),
            "freeHandAcquisiton": self.tr("DSGTools: Free Hand Acquisition"),
            "circle2points": self.tr("QGIS Circle extraction tool"),
            "acquisition": self.tr("DSGTools: Right Degree Angle Digitizing")
        }

    def setDigitizingTool(self, tool):
        """
        Defines button's name, which is used to compose the display name.
        :param tool: (str) button's name.
        """
        if type(tool) == str:
            if tool not in self.supportedTools():
                raise ValueError(self.tr("'{0}' not supported.").format(tool))
            self._props["digitizingTool"] = tool
        else:
            raise TypeError(
                self.tr("Digitizing tool prop must be a str ({0}).")\
                    .format(type(tool))
            )

    def digitizingTool(self):
        """
        Retrives button's name.
        :return: (str) button's name.
        """
        return str(self._props["digitizingTool"])

    def setCheckable(self, checkable):
        """
        Defines if button may be toggled (or "clickable").
        :param checkable: (bool) whether button may be toggled.
        """
        if type(checkable) == bool:
            self._props["isCheckable"] = checkable
            for w in self.widgets():
                w.setCheckable(checkable)
                try:
                    # signal may or may not be connected. case when it needs to
                    # stay connected is handled by the connect command below
                    w.clicked.disconnect(self.action().trigger)
                except:
                    pass
                if not checkable:
                    self.setChecked(False)
                    w.clicked.connect(self.action().trigger)
            if checkable:
                # action should be handled only once
                self.handleActionCallback()
        else:
            raise TypeError(
                self.tr("Toggling usage must be a bool ({0}).")\
                    .format(type(checkable))
            )

    def isCheckable(self):
        """
        Checks if button may be toggled (or "clickable").
        :return: (bool) whether button may be toggled.
        """
        return bool(self._props["isCheckable"])

    @pyqtSlot(bool)
    def setChecked(self, checked):
        """
        Defines if button is toggled (or "clickable").
        :param checked: (bool) whether button is toggled.
        """
        if type(checked) == bool:
            checked = self.isCheckable() and checked
            before = self.isChecked()
            self._props["isChecked"] = checked
            for w in self.widgets():
                # we don't want to notify toggling N times
                w.blockSignals(True)
                w.setChecked(checked)
                w.update()
                w.blockSignals(False)
            self.handleActionCallback()
        else:
            raise TypeError(
                self.tr("Toggling status must be a bool ({0}).")\
                    .format(type(checked))
            )

    def isChecked(self):
        """
        Checks if button is toggled (or "clickable").
        :return: (bool) whether button may be toggled.
        """
        return bool(self._props["isChecked"])

    def setWidgetsEnabled(self, enabled):
        """
        Modifies all managed widgets' enabled status.
        :param enabled: (bool) whether buttons should be enabled.
        """
        for w in self.widgets():
            w.setEnabled(enabled)

    def setEnabled(self, enabled, updateWidgets=False):
        """
        Disables or enables button from QGIS interface. When a button is
        active, its action is registered to the main window and shortcut, if
        set, is enabled. While enabled, button's actions are registered onto
        the QGIS main window.
        :param enabled: (bool) whether buttons should be enabled.
        :param updateWidgets: (bool) indicates whether widgets are also enabled
                              or disabled.
        """
        if type(enabled) == bool:
            if self.isEnabled() and not enabled:
                s = self.shortcut()
                self.setShortcut("")
                self.__shortcut = s
                iface.unregisterMainWindowAction(self.action())
            elif not self.isEnabled() and enabled:
                self.setShortcut(self.__shortcut)
                iface.registerMainWindowAction(self.action(), self.shortcut())
            if updateWidgets:
                self.setWidgetsEnabled(enabled)
            self._props["isEnabled"] = enabled
        else:
            raise TypeError(
                self.tr("Enabled status must be a bool ({0}).")\
                    .format(type(enabled))
            )

    def isEnabled(self):
        """
        Checks if button is enabled.
        :return: (bool) whether button is enabled.
        """
        return bool(self._props["isEnabled"])

class CustomButtonSetup(QObject):
    """
    Class designed to provide objects for button management. 
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1
    buttonAdded = pyqtSignal(CustomFeatureButton)
    buttonRemoved = pyqtSignal(CustomFeatureButton)
    buttonUpdated = pyqtSignal(CustomFeatureButton)

    def __init__(self, buttonsProps=None, displayName=None, description=None):
        """
        Class constructor.
        :param buttonsProps: (set) a set of buttons' properties to be loaded to
                             the interface.
        :param displayName: (str) friendly name for the button collection to be
                            displayed on the interface.
        :param description: (str) a short text to describe current set of
                            buttons.
        """
        super(CustomButtonSetup, self).__init__()
        self._buttons = dict()
        self._name = displayName or self.tr("Custom Button Setup")
        self._description = description
        self._dynamicShortcut = False
        if buttonsProps:
            self.setButtons(buttonsProps)

    def __del__(self):
        """
        Method reimplementation for correctly cleaning any created buttons or
        shortcuts on QGIS main window.
        """
        while self._buttons:
            _, b = self._buttons.popitem()
            b.__del__() # del was not being called and buttons were lingering

    def setName(self, name):
        """
        Defines setup's display name.
        :param name: (str) new setup's display name.
        """
        self._name = name

    def name(self):
        """
        Retrives button's name.
        :return: (str) button's name.
        """
        return str(self._name)

    def setDescription(self, description):
        """
        Defines setup's description text.
        :param description: (str) new setup's description text.
        """
        self._description = description

    def description(self):
        """
        Retrives button's description.
        :return: (str) setup's description text.
        """
        return str(self._description)

    def setDynamicShortcut(self, ds):
        """
        Defines if setup will assign shortcuts from 1-9 for the first 9 buttons
        displayed on GUI (current category).
        :param ds: (bool) whether setup should assign dynamic shortcuts.
        """
        self._dynamicShortcut = ds

    def dynamicShortcut(self):
        """
        Whether setup will assign shortcuts from 1-9 for the first 9 buttons
        displayed on GUI (current category).
        :return: (bool) whether setup should assign dynamic shortcuts.
        """
        return bool(self._dynamicShortcut)

    def setButtons(self, buttons):
        """
        Replaces current active buttons for new ones from thei properties set.
        Buttons with the same are not tolerated and only one of them will be
        kept.
        :param buttons: (list) a list of buttons' properties to be setup.
        """
        for key in list(self._buttons.keys()):
            self.removeButton(key)
        del self._buttons
        self._buttons = dict()
        for props in buttons:
            self.addButton(props)

    def button(self, name):
        """
        Retrieves a button from its name.
        :param name: (str) button's name.
        :return: (CustomFeatureButton) identified button.
        """
        if name in self._buttons:
            return self._buttons[name]

    def buttonWidget(self, name):
        """
        Retrieves a new instance of button's widget from its name.
        :param name: (str) button's name.
        :return: (QPushButton) button GUI-ready (e.g. with all props applied).
        """
        return self._buttons[name].newWidget()

    def buttons(self):
        """
        Retrieves all registered buttons.
        :return: (list-of-CustomFeatureButton) identified button.
        """
        return list(self._buttons.values())

    def buttonNames(self):
        """
        Retrieves the names for all registered buttons.
        :return: (list-of-str) names for the buttons.
        """
        return list(self._buttons.keys())

    def newButton(self):
        """
        Creates a new button and sets it to the setup.
        :return: (CustomFeatureButton) created button.
        """
        b = CustomFeatureButton()
        baseName = b.name()
        i = 0
        while b.name() in self.buttonNames():
            i += 1
            b.setName("{0} {1}".format(baseName, i))
        self.addButton(b.properties())
        return self.button(b.name())

    def widgets(self):
        """
        Retrieves a map of all button widgets of registered buttons.
        :return: (dict) a map from button name to an instance of its widget.
        """
        return {n: self.buttonWidget(n) for n in self._buttons}

    def setButtonsCheckable(self, checkable):
        """
        Sets all buttons checkable behaviour.
        :param checkable: (bool) whether buttons are checkable.
        """
        for b in self.buttons():
            b.setCheckable(checkable)

    def setButtonSize(self, button, size):
        """
        Updates a button's font size.
        :param button: (str) button's name.
        :param size: (int) button's new font size in pixels.
        """
        self.button(button).setSize(size)

    def setButtonsSize(self, size):
        """
        Updates all buttons' font size.
        :param size: (int) button's new font size in pixels.
        """
        for b in self._buttons.values():
            b.setSize(size)

    def addButton(self, props, replace=False):
        """
        Adds a button to the set of controlled buttons.
        :param props: (dict) a map to buttons properties.
        :param replace: (bool) whether a button with the same name, if found,
                        should be replaced.
        :return: (bool) operation status
        """
        if props["name"] in self._buttons and not replace:
            return False
        button = CustomFeatureButton(props)
        button.toggled.connect(partial(self.toggleButton, button))
        self._buttons[props["name"]] = button
        self.buttonAdded.emit(self.button(props["name"]))
        return True

    def updateButton(self, prevName, newProps):
        """
        Updates button's properties.
        :param prevName: (str) name for the button that will be updated.
        :param newProps: (dict) a map to new attributes to be set.
        :return: (bool) whether button was updated.
        """
        button = self.button(prevName)
        if button is None:
            # button is not registered
            return False
        updated = button.update(newProps)
        if prevName != button.name():
            self._buttons[button.name()] = self._buttons.pop(prevName)
        if updated:
            self.buttonUpdated.emit(button)
        return updated

    def removeButton(self, name):
        """
        Removes a button from setup config.
        :param name: (str) button's name to be removed.
        """
        if name in self._buttons:
            button = self.button(name)
            del self._buttons[name]
            self.buttonRemoved.emit(button)
            return True
        return False

    def checkKeyword(self, word, checkShortcut=False):
        """
        Checks for a keyword match on buttons metadata.
        :param word: (str) word or expression to be matched.
        :param checkShortcut: (bool) whether shortcuts should be checked.
        :return: (list-of-CustomFeatureButton) buttons that have matched the
                 expression.
        """
        matches = []
        for button in self._buttons.values():
            if button.checkKeyword(word, checkShortcut):
                matches.append(button)
        return matches

    def checkKeywordSet(self, kws, checkShortcut=False):
        """
        Match a set of keywords to all registered buttons.
        :param kws: (set-of-str) keywords to be matched.
        :param checkShortcut: (bool) whether shortcuts should be checked.
        :return: (list-of-CustomFeatureButton) matched buttons.
        """
        matches = None
        for w in kws:
            if matches is None:
                matches = set(self.checkKeyword(w, checkShortcut))
            else:
                matches &= set(self.checkKeyword(w, checkShortcut))
        return list(matches)

    def categories(self, reverse=False):
        """
        Identifies all categories comprising current set of buttons.
        :param reverse: (bool) whether oredering should descending.
        :return: (list-of-str) ordered list of categories.
        """
        return sorted(
            set(button.category() for button in self._buttons.values()),
            reverse=reverse
        )

    def groupButtons(self):
        """
        Maps and groups all buttons in regard to their categories.
        :return: (dict) map to all buttons using category as key.
        """
        groups = defaultdict(set)
        for b in self._buttons.values():
            groups[b.category()].add(b)
        return groups

    def now(self):
        """
        Gets time and date from the system. Format: "dd/mm/yyyy HH:MM:SS".
        :return: (str) current's date and time
        """
        paddle = lambda n : str(n) if n > 9 else "0{0}".format(n)
        now = datetime.now()
        return "{day}/{month}/{year} {hour}:{minute}:{second}".format(
            year=now.year,
            month=paddle(now.month),
            day=paddle(now.day),
            hour=paddle(now.hour),
            minute=paddle(now.minute),
            second=paddle(now.second)
        )

    def state(self):
        """
        Exports current setup instance to a map object.
        :return: (dict) a map to all instances attributes.
        """
        return {
            "name": self.name(),
            "description": self.description(),
            "dynamicShortcut": self.dynamicShortcut(),
            "version": self.__MAP_VERSION,
            "lastModified": self.now(),
            "buttons": [b.properties() for b in self.buttons()]
        }

    def setState(self, state):
        """
        Tries to import state from a map object.
        :param state: (dict) a map to state to be imported.
        """
        if self.__MAP_VERSION != state["version"]:
            # warn user that versions are different and state may be
            # incompatible
            pass
        # clear current state
        self.setButtons({})
        self.setName(state["name"])
        self.setDynamicShortcut(state["dynamicShortcut"])
        self.setDescription(state["description"])
        for props in state["buttons"]:
            self.addButton(props)

    def clearWidgetsFromButton(self, name):
        """
        Clears all registered widgets for a given button. This method should be
        carefully used as it might simply remove the reference to a set of
        managed widgets and not propagating button properties updates to them.
        :param name: (str) name for the button to have its wigdets references
                     cleaned.
        """
        self.button(name).clearWidgets()

    def clearWidgets(self):
        """
        Widgets are created as requested and might get the application to
        slowdown. This method clears the reference list of all widgets from all
        buttons.
        """
        for b in self.buttons():
            b.clearWidgets()

    def toggleButton(self, button, toggled=False):
        """
        Handles all button widgets in order to allow only one of them button to
        be toggled at any time.
        :param bw: (QPushButton) push button to be managed.
        """
        if not toggled:
            return
        for b in self.buttons():
            b.blockSignals(True)
            b.setChecked(False)
            b.blockSignals(False)
        button.blockSignals(True)
        button.setChecked(True)
        button.blockSignals(False)

    def checkedButton(self):
        """
        Identifies whether a button is toggled and retrieves it.
        :return: (CustomFeatureButton) currently checked button.
        """
        for b in self.buttons():
            if b.isChecked():
                return b

    def setButtonEnabled(self, button, enabled):
        """
        Disables or enables a button from QGIS interface. When a button is
        active, its action is registered to the main window and shortcut, if
        set, is enabled.
        :param button: (str) button name to have its enabled status set.
        :param enabled: (bool) whether button should be enabled.
        """
        b = self.button(button)
        if b is not None:
            b.setEnabled(enabled)

    def setEnabled(self, enabled):
        """
        Disables or enables all buttons from QGIS interface. When a button is
        active, its action is registered to the main window and shortcut, if
        set, is enabled.
        :param enabled: (bool) whether buttons should be enabled.
        """
        for b in self.buttons():
            b.setEnabled(enabled)

    def isEnabled(self):
        """
        For a setup to be considered enabled, at least one of its buttons
        should be enabled. This method identifies that.
        :return: (bool) whether setup has any enabled buttons.
        """
        for b in self.buttons():
            if b.isEnabled():
                return True
        return False

    def hasDisabledButtons(self):
        """
        Identifies whether setup has any disabled button.
        :return: (bool) if setup has any disabled button.
        """
        for b in self.buttons():
            if not b.isEnabled():
                return True
        return False

    def disabledButtons(self):
        """
        Identifies all disabled buttons registered to setup.
        :return: (list-of-CustomFeatureButton) all disabled buttons.
        """
        bl = list()
        for b in self.buttons():
            if not b.isEnabled():
                bl.append(b)
        return bl
