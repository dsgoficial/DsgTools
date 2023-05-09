# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-02-21
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSlot, pyqtSignal
from qgis.PyQt.QtWidgets import QLabel, QWidget, QSlider, QHBoxLayout

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "switchButton.ui")
)


class SwitchButton(QWidget, FORM_CLASS):
    stateChanged = pyqtSignal(int)

    def __init__(self, parent=None, stateA=None, stateB=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget parent to Switch Button.
        :param stateA: (str) name for state A that will be set to GUI.
        :param stateB: (str) name for state B that will be set to GUI.
        """
        super(SwitchButton, self).__init__(parent)
        self.setupUi(self)
        self.setStateAName(stateA or self.tr("State A"))
        self.setStateBName(stateB or self.tr("State B"))
        self._state = 0
        self.slider.setPageStep(50)
        self.slider.valueChanged.connect(self.valueChanged)
        self.slider.sliderReleased.connect(self.updateState)
        self.min_ = self.slider.minimum()
        self.max_ = self.slider.maximum()

    def setStateAName(self, name):
        """
        Updates the name for state A.
        :param name: (str) state A's name
        """
        self.stateA = name
        self.stateALabel.setText(name)

    def setStateBName(self, name):
        """
        Updates the name for state B.
        :param name: (str) state B's name
        """
        self.stateB = name
        self.stateBLabel.setText(name)

    def currentState(self):
        """
        Reads state defined by current slider position - read from GUI.
        :return: (int) current state (0 for A, 1 for B).
        """
        return int(self.slider.value() >= (self.min_ + self.max_) / 2)

    def state(self):
        """
        Reads state current set for Switch Button.
        :return: (int) current defined state (0 for A, 1 for B).
        """
        return int(self._state)

    def setState(self, state):
        """
        Defines Switch Button's state.
        :return: (int) state to be set (0 for A, 1 for B).
        """
        self._state = state
        self.slider.setValue({0: self.min_, 1: self.max_}[state])

    def toggleState(self):
        """
        Alternates Switch Button's state defined state.
        """
        self._state = self.state() ^ 1
        self.setState(self._state)

    def stateName(self):
        """
        Retrieves the name for current defined state.
        :return: (str) defined state's name (exposed text on GUI).
        """
        return {0: self.stateA, 1: self.stateB}[self.state()]

    @pyqtSlot()
    def updateState(self):
        """
        Updates defined state based on current state read from GUI (slider
        position).
        """
        newState = self.currentState()
        prevState = self.state()
        self.setState(newState)
        if prevState != newState:
            self.stateChanged.emit(newState)

    @pyqtSlot(int)
    def valueChanged(self, value):
        """
        Updates defined state based on current state read from GUI (slider
        position).
        """
        if value in (49, 50):
            self.toggleState()
            self.stateChanged.emit(self.state())
