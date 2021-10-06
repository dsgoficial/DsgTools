import os
from PyQt5 import QtWidgets, uic

class QuestionMessageBox:

    def __init__(self):
        super(QuestionMessageBox, self).__init__()

    def show(self, parent, title, text):
        result = QtWidgets.QMessageBox.question(
            parent,
            title, 
            text
        )
        return result == 16384