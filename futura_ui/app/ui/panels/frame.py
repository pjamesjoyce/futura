from PySide2 import QtWidgets
from ..utils import load_ui_file
import os
from ..ui_files import Ui_PanelWidget

class FuturaFrame(Ui_PanelWidget, QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(FuturaFrame, self).__init__(parent)

        self.setupUi(self)

    def clear(self):
        for i in reversed(range(self.widget_layout.count())):
            self.widget_layout.itemAt(i).widget().setParent(None)

    def connect_signals(self):
        pass
