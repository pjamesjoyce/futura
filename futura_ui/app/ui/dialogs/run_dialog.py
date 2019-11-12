from PySide2 import QtWidgets
from futura_ui.app.ui.utils import load_ui_file
from futura_ui.app.signals import signals
import os


class RunDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RunDialog, self).__init__(parent)

        ui_path = 'onrun.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.buttonPressed = None

        self.pushButton_2.pressed.connect(self.pushButton_2_pressed)


    def pushButton_2_pressed(self):
        self.close()
        signals.load_tree_data.emit()


