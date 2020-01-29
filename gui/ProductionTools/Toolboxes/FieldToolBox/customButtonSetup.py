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
from collections import defaultdict

from qgis.utils import iface
from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.PyQt.QtWidgets import QPushButton, QAction
from qgis.PyQt.QtGui import QIcon, QColor, QPalette, QKeySequence

class CustomFeatureButton(QObject):
    """
    Class designed to handle actions, properties and settings for buttons. It
    includes info about its styling, shortcuts and other user-defined
    characteristics. This object MUST be serializable, since it'll be used for
    data perpetuation and state definition/loading.
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1
    categoryChanged = pyqtSignal(QObject)

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
            "color": "#ffffff",
            "tooltip": "",
            "category": "",
            "shortcut": "",
            "layer": "",
            "keywords": set()
        }
        self._callback = callback if callback else lambda: None
        self.setProperties(props)
        self.setAction(QAction())

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
        iface.unregisterMainWindowAction(self._action)
        self._action.blockSignals(True)
        self._widget.clicked.disconnect(self._action.trigger)
        self._widget.blockSignals(True)
        del self._widget
        del self._action
        del self

    def copy(self):
        """
        Provides a copy of current CustomFeatureButton object.
        :return: (CustomFeatureButton) copy of current's instance.
        """
        b = CustomFeatureButton(self.properties())
        b.setCallback(self._callback)
        b.setAction(self._action)
        return b

    def setProperties(self, props):
        """
        Modify current button properties. Only valid properties are modified
        (caveat: it still may accept invalid values).
        :param props: (dict) a map to button's new properties.
        :return: (dict) a map to current button properties.
        """
        if props is not None:
            for prop in self._props.keys():
                if prop in props:
                    self._props[prop] = props[prop]
                    if prop == "category":
                        self.categoryChanged.emit(self)
        # set properties to the push button related to this obj
        self._widget = self.newWidget()
        return dict(self._props)

    def update(self, newProps):
        """
        Updates current button properties from a given property map.
        :param newProps: (dict) new properties value map.
        :return: (bool) whether any property value was set from newProps.
        """
        updated = False
        tempButton = CustomFeatureButton(newProps)
        methodMap = {
            "name": lambda x: self.setName(x),
            "openForm": lambda x: self.setOpenForm(x),
            "useColor": lambda x: self.setUseColor(x),
            "color": lambda x: self.setColor(x),
            "tooltip": lambda x: self.setToolTip(x),
            "category": lambda x: self.setCategory(x),
            "shortcut": lambda x: self.setShortcut(x),
            "layer": lambda x: self.setLayer(x),
            "keywords": lambda x: self.setKeywords(x)
        }
        for propName, propValue in tempButton.properties().items():
            if propName in newProps and propValue == newProps[propName]:
                # only non-defaulted values will be applied to the button
                methodMap[propName](propValue)
                updated = True
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
            "tooltip": self.toolTip(),
            "category": self.category(),
            "layer": self.layer(),
            "shortcut": self.shortcut(),
            "keywords": self.keywords()
        }

    def widget(self):
        """
        This instance's widget configured with current defined properties.
        :return: (QPushButton) current widget.
        """
        return self._widget

    def newWidget(self):
        """
        A new instance of widget configured with current defined properties.
        :return: (QPushButton) new instance of a widget with current defined
                 properties.
        """
        pb = QPushButton()
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
        pb.update()
        if hasattr(self, "_action"):
            pb.clicked.connect(self._action.trigger)
        return pb

    def setName(self, name):
        """
        Defines button's name, which is used to compose the display name.
        :param name: (str) button's name.
        """
        if type(name) == str: 
            self._props["name"] = name
            self.widget().setText(self.displayName())
            self.widget().update()
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
        return str(self._props["name"])

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
                self.widget().setPalette(pal)
                self.widget().update()
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
                self.widget().setPalette(QPalette())
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

    def setToolTip(self, tooltip):
        """
        Defines button tool tip text.
        :param tooltip: (str) button's tool tip text.
        """
        if type(tooltip) == str: 
            self._props["tooltip"] = tooltip
            self.widget().setToolTip(tooltip)
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
            self.widget().setText(self.displayName())
            self.widget().update()
        else:
            raise TypeError(
                self.tr("Category must be a str ({0}).").format(type(s))
            )

    def shortcut(self):
        """
        Retrieves button's action shortcut.
        :return: (str) button's action shortcut.
        """
        return str(self._props["shortcut"])

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
        self._action.triggered.disconnect(self._callback)
        self._callback = callback
        self._action.triggered.connect(self._callback)

    def setAction(self, action):
        """
        Sets callback to be triggered whenever button is pushed.
        :param action: (QAction) action to be set.
        """
        if not isinstance(action, QAction):
            raise Exception(self.tr("Action must be instance of QAction."))
        if hasattr(self, "_action"):
            # first call does not an "_action" attribute
            self._action.triggered.disconnect(self._callback)
            # other callbacks might have been associated with current action
            iface.unregisterMainWindowAction(self._action)
            self._action.blockSignals(True)
            self.widget().clicked.disconnect(self._action.trigger)
            del self._action
        self._action = action
        self._action.setText(
            self.tr("DSGTools: Custom Feature Toolbox - button {0}")\
                .format(self.name())
        )
        self._action.setIcon(
            QIcon(':/plugins/DsgTools/icons/fieldToolbox.png')
        )
        self._action.triggered.connect(self._callback)
        self.widget().clicked.connect(self._action.trigger)
        self._action.setShortcut(QKeySequence.fromString(self.shortcut()))
        self.widget().setShortcut(QKeySequence.fromString(self.shortcut()))
        iface.registerMainWindowAction(self._action, self.shortcut())

    def action(self):
        """
        Gets the QAction associated with the button push event.
        :return: (QAction) current action.
        """
        return self._action if hasattr(self, "_action") else None

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

    def checkLayer(self):
        """
        Checks whether current layer is loaded on canvas.
        :return: (bool) whether layer is found on canvas.
        """
        return len(QgsProject.instance().mapLayersByName(self.layer())) > 0

    def fieldMap(self):
        """
        Retrieves field map for current select layer.
        :return: (dict) object that maps each field from selected layer to its
                 value map.
        """
        fm = dict()
        if self.checkLayer():
            # do things
            pass
        return fm

    def setAttributeMap(self, attr):
        """
        Updates the attribute map for output features on reclassification or
        feature creation.
        :param attr: (str) new attribute map.
        """
        if type(attr) == dict:
            # validate attribute map and update property
            # self._props["layer"] = layer
        else:
            raise TypeError(
                self.tr("Attribute map must be a dict ({0}).")
                    .format(type(attr))
            )

    def attributeMap(self):
        """
        Attribute map for output features on reclassification or feature
        creation.
        :return: (dict) attribute map for new/updated features.
        """
        return dict()

class CustomButtonSetup(QObject):
    """
    Class designed to provide objects for button management. 
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1
    buttonAdded = pyqtSignal(CustomFeatureButton)
    buttonRemoved = pyqtSignal(CustomFeatureButton)
    buttonUpdated = pyqtSignal(CustomFeatureButton)

    def __init__(self, buttonsProps=None):
        """
        Class constructor.
        :param buttonsProps: (set) a set of buttons' properties to be loaded to
                             the interface.
        """
        super(CustomButtonSetup, self).__init__()
        self._buttons = dict()
        if buttonsProps:
            self.setButtons(buttonsProps)

    def setButtons(self, buttons):
        """
        Replaces current active buttons for new ones from thei properties set.
        Buttons with the same are not tolerated and only one of them will be
        kept.
        :param buttons: (list) a list of buttons' properties to be setup.
        """
        if not buttons:
            for key in list(self._buttons.keys()):
                del self._buttons[key]
            del self._buttons
            self._buttons = dict()
        for props in buttons:
            button = CustomFeatureButton(props)
            self._buttons[props["name"]] = button
            # button.categoryChanged.connect(self.buttonUpdated)

    def button(self, name):
        """
        Retrieves a button from its name.
        :param name: (str) button's name.
        :return: (CustomFeatureButton) identified button.
        """
        if name in self._buttons:
            return self._buttons[name]

    def buttonWidget(self, name, newInstance=False):
        """
        Retrieves an instance of button's widget from its name.
        :param name: (str) button's name.
        :param newInstance: (bool) indicates whether widget should be a new
                            instance setup with current button's properties.
        :return: (QPushButton) button GUI-ready (e.g. with all props applied).
        """
        return self._buttons[name].newWidget() if newInstance \
                else self._buttons[name].widget()

    def buttons(self):
        """
        Retrieves all registered buttons.
        :return: (list-of-CustomFeatureButton) identified button.
        """
        return list(self._buttons.values())

    def buttonNames(self):
        """
        Retrieves the names for all registered buttons.
        :return: (list-of-CustomFeatureButton) names for the buttons.
        """
        return list(self._buttons.keys())

    def widgets(self, newInstance=False):
        """
        Retrieves a map of all button widgets of registered buttons.
        :param newInstance: (bool) indicates whether widget should be a new
                            instance setup with current button's properties.
        :return: (dict) a map from button name to its widget instance.
        """
        return { n: self.buttonWidget(n, newInstance) for n in self._buttons }

    def addButton(self, props, replace=False):
        """
        Adds a button the set of controlled buttons.
        :param props: (dict) a map to buttons properties.
        :param replace: (bool) whether a button with the same name, if found,
                        should be replaced.
        :return: (bool) operation status
        """
        if props["name"] in self._buttons and not replace:
            return False
        self._buttons[props["name"]] = CustomFeatureButton(props)
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
        for props in state["buttons"]:
            self.addButton(props)
