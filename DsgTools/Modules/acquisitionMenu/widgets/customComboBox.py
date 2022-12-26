from PyQt5.QtWidgets import QComboBox, QApplication, QCompleter
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5 import QtGui


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def loadItems(self, items):
        self.items = items
        model = QtGui.QStandardItemModel()
        [
            model.setItem(i, 0, QtGui.QStandardItem(word))
            for i, word in enumerate(self.items)
        ]
        self.setModel(model)
        self.setModelColumn(0)
        self.setInsertPolicy(QComboBox.NoInsert)

    def setModel(self, model):
        super(CustomComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(CustomComboBox, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
