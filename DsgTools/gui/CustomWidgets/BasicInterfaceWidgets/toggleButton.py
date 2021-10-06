from qgis.PyQt.QtCore import (Qt,
                              QSize,
                              QPoint,
                              QRectF,
                              QPointF,
                              pyqtSlot,
                              QEasingCurve,
                              pyqtProperty,
                              QPropertyAnimation,
                              QSequentialAnimationGroup)
from qgis.PyQt.QtWidgets import QCheckBox
from qgis.PyQt.QtGui import QPen, QColor, QBrush, QPainter, QPaintEvent

class Toggle(QCheckBox):
    # This widget was originally implemented by Martin Fitzpatrick
    # @ https://github.com/learnpyqt/python-qtwidgets
    # It is slightly modified to be used as a state toggle button
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
                 parent=None,
                 bar_color=Qt.gray,
                 checked_color="#00B0FF",
                 handle_color=Qt.white,
                 labels=None):
        super().__init__(parent)
        self.setLabels(labels)
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        # Setup the rest of the widget.

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.stateChanged.connect(self.handle_state_change)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def setLabels(self, labels: tuple):
        """
        Sets the labels to be displayed for each state the button may
        represent.
        :param labels: (tuple-of-str) text to be displayed for each toggling
                       state.
        """
        if labels is None or len(labels) != 2:
            return
        self._labels = labels

    def getLabel(self, state: bool):
        """
        Gets the label to be displyed on the button accordingly to its state.
        :param state: (bool) whether this button is toggle (checked).
        :return: (str) label to be displayed 
        """
        if self._labels is None:
            return ""
        return self._labels[int(state)]

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            # p.drawText(barRect, self.getLabel(True))
            p.setBrush(self._handle_checked_brush)
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            # p.drawText(barRect, self.getLabel(False))
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtSlot(int)
    def handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()
