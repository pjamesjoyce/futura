from PySide2 import QtWidgets
from ..utils import load_ui_file
import os


class FuturaFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(FuturaFrame, self).__init__(parent)

        ui_path = 'panel.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

    def clear(self):
        for i in reversed(range(self.widget_layout.count())):
            self.widget_layout.itemAt(i).widget().setParent(None)

    def connect_signals(self):
        pass
