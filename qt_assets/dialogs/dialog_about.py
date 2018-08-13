import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        loadUi(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'About.ui')), self)

    def show_dialog(self):
        self.show()
        self.exec_()
