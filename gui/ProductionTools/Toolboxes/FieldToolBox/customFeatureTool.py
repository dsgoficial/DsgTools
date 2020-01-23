# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2020-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, QObject
from qgis.PyQt.QtGui import QIcon, QColor, QPalette
from qgis.PyQt.QtWidgets import QDockWidget, QLineEdit, QPushButton

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonPropWidget import ButtonPropWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self.tableSetup()

    def tableSetup(self):
        """
        Configures table for button display.
        """
        table = self.orderedTableWidget
        table.clear()
        table.setHeaders({
            0 : {
                "header" : self.tr("Custom button"),
                "type" : "widget",
                "widget" : self.newButton,
                "setter" : "setText",
                "getter" : "text"
            }
        })
        table.setSectionResizeMode(0, "interactive")
        table.setSectionResizeMode(0, "resizetocontents")
        table.moveUpPushButton.hide()
        table.moveDownPushButton.hide()
        # table.addPushButton.hide()
        # table.removePushButton.hide()

    def newButton(self, props=None):
        """
        Get a new instance of a CustomFeatureButton based on its properties.
        :param props: (dict) a map to custom button properties.
        :return: (QPushButton/CustomFeatureButton) new custom feature button.
        """
        from random import randint
        if props is None:
            pb = QPushButton()
            pb.setText("Created button [{0}]".format(chr(randint(48, 57))))
            pb.setToolTip(self.tr("No button property was given."))
        else:
            # handle CustomFeatureButton obj in here
            pb = QPushButton()
        pal = QPalette()
        pal.setColor(
            pal.Button,
            QColor(randint(0, 255), randint(0, 255), randint(0, 255), 100)
        )
        pb.setPalette(pal)
        pb.update()
        return pb

    @pyqtSlot(bool, name="on_buttonPropsPushButton_clicked")
    def setupCurrentButton(self):
        """
        Opens setup form.
        """
        # button = self.currentButton()
        # props = button.properties()
        # dlg = ButtonPropWidget(props)
        dlg = ButtonPropWidget()
        ret = dlg.exec_()
        if ret:
            pass

class CustomFeatureButton(QObject):
    """
    Class designed to handle actions, properties and settings for buttons. It
    includes info about its styling, shortcuts and other user-defined
    characteristics. This object MUST be serializable, since it'll be used for
    data perpetuation and state definition/loading.
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1

    def __init__(self, props=None):
        """
        Class constructor.
        :param props: (dict) a map to button's properties.
        """
        super(CustomFeatureButton, self).__init__()
        self._props = {
            "name": self.tr("New button"),
            "openForm": False,
            "color": "#ffffff",
            "tooltip": "",
            "category": "",
            "shortcut": "",
            "keywords": set()
        }
        self.setProperties(props)

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

    def copy(self):
        """
        Provides a copy of current CustomFeatureButton object.
        :return: (CustomFeatureButton) copy of current's instance.
        """
        return CustomFeatureButton(self.properties())

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
        # set properties to the push button related to this obj
        self._widget = self.newWidget()
        return dict(self._props)

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
            "color": self.color(),
            "tooltip": self.toolTip(),
            "category": self.category(),
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
        col = self.color()
        if isinstance(col, str):
            col = QColor(col)
        else:
            col = QColor(*col)
        pal.setColor(pal.Button, col)
        pb.setPalette(pal)
        pb.update()
        return pb

    def setName(self, name):
        """
        Defines button's name, which is used to compose the display name.
        :param name: (str) button's name.
        """
        if type(name) == str: 
            self._props["name"] = name
            self._widget.setText(self.displayName())
            self._widget.update()
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
            pal = QPalette()
            col = self.color()
            if isinstance(col, str):
                col = QColor(col)
            else:
                col = QColor(*col)
            pal.setColor(pal.Button, col)
            self._widget.setPalette(pal)
            self._widget.update()
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

    def setToolTip(self, tooltip):
        """
        Defines button tool tip text.
        :param tooltip: (str) button's tool tip text.
        """
        if type(tooltip) == str: 
            self._props["tooltip"] = tooltip
            self._widget.setToolTip(tooltip)
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
            self._widget.setText(self.displayName())
            self._widget.update()
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
        for kw in self.keywords():
            if word in kw.lower():
                return True
        if checkShortcut and word in self.shortcut().lower().replace(" ", ""):
            # this ignores spacing - 'Alt+R' = 'Alt + R'
            return True
        return False

class CustomFeatureSetup(QObject):
    """
    Class designed to provide objects for button management. 
    """
    # metadata of current properties map version
    __MAP_VERSION = 0.1

    def __init__(self, buttonsProps=None):
        """
        Class constructor.
        :param buttonsProps: (set) a set of buttons' properties to be loaded to
                             the interface.
        """
        super(CustomFeatureSetup, self).__init__()
        self._buttons = dict()
        if buttonsProps:
            self.setButtons(buttonsProps)

    def setButtons(self, buttons):
        """
        Replaces current active buttons for new ones from thei properties set.
        Buttons with the same are not tolerated and only one of them will be
        kept.
        :param buttons: (set) a set of buttons' properties to be setup.
        """
        if not buttons:
            for key in self._buttons:
                del self._buttons[key]
            del self._buttons
            self._buttons = dict()
        for props in buttons:
            self._buttons[props["name"]] = CustomFeatureButton(props)

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
        :param name: (str) button's name.
        :return: (list-of-CustomFeatureButton) identified button.
        """
        return list(self._buttons.values())

    def widgets(self, newInstance=False):
        """
        Retrieves a map of all button widgets of registered buttons.
        :param newInstance: (bool) indicates whether widget should be a new
                            instance setup with current button's properties.
        :return: (dict) a map from button name to its widget instance.
        """
        return { self.buttonWidget(n, newInstance) for n in self._buttons }

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
        return True

    def removeButton(self, name):
        """
        Removes a button from setup config.
        :param name: (str) button's name to be removed.
        """
        if name in self._props:
            del self._props[name]
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
