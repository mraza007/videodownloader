import os

from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class HistoryTab(QWidget):

    display_name = 'History'

    def __init__(self):
        super().__init__()
        loadUi(os.path.abspath('tabs/tab_not_yet.ui'), self)
        self.show()
