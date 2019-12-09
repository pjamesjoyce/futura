from PySide2 import QtWidgets
from ..utils import load_ui_file
from ...signals import signals
import os


class LoadWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoadWidget, self).__init__(parent)

        ui_path = 'load_actions.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.newButton.pressed.connect(signals.new_recipe.emit)
        self.loadButton.pressed.connect(signals.load_recipe.emit)
        self.loaderButton.pressed.connect(signals.load_loader.emit)

